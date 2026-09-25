"""End-to-end tests for scripts/audit_website.py against local fixture sites.

The fixtures are fictional sites served on 127.0.0.1 (plain HTTP, or HTTPS with
a throwaway self-signed certificate), so the tests need no internet access.
"""
import functools
import http.server
import shutil
import ssl
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import audit_website as A  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class ForbiddenHandler(QuietHandler):
    def do_GET(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>Access denied</body></html>")

    do_HEAD = do_GET


@contextmanager
def serve(directory: Path, handler=QuietHandler, tls: tuple | None = None):
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(handler, directory=str(directory)))
    if tls:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(*tls)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        yield httpd.server_address[1]
    finally:
        httpd.shutdown()
        httpd.server_close()


def make_pdf(path: Path, created: str):
    from pypdf import PdfWriter
    w = PdfWriter()
    w.add_blank_page(width=200, height=200)
    w.add_metadata({"/CreationDate": created, "/Title": "Company Profile"})
    with open(path, "wb") as f:
        w.write(f)


@pytest.fixture(scope="module")
def sites(tmp_path_factory):
    root = tmp_path_factory.mktemp("sites")
    for name in ("oldsite", "modernsite", "jsshell", "parked"):
        shutil.copytree(FIXTURES / name, root / name)
    make_pdf(root / "oldsite" / "brochure.pdf", "D:20150310120000+05'30'")
    make_pdf(root / "modernsite" / "downloads" / "company-brochure-2025.pdf", "D:20250704093000+05'30'")
    (root / "robots").mkdir()
    (root / "robots" / "index.html").write_text("<html><body>hello</body></html>")
    (root / "robots" / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    cert, key = root / "cert.pem", root / "key.pem"
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(key),
                    "-out", str(cert), "-days", "2", "-subj", "/CN=127.0.0.1",
                    "-addext", "subjectAltName=IP:127.0.0.1"], check=True, capture_output=True)
    return root, (str(cert), str(key))


def fetcher(verify=True):
    return A.Fetcher(delay=0, timeout=5, verify=verify)


def test_decayed_site_scores_nine_of_nine(sites):
    root, _ = sites
    with serve(root / "oldsite") as port:
        r = A.audit(f"http://127.0.0.1:{port}/", fetcher(), use_psi=False)
    assert r["status"] == "OK"
    hits = {k for k, c in r["checks"].items() if c["hit"]}
    assert hits == {"1_copyright_year", "2_withdrawn_standards", "3_https", "4_viewport", "5_free_email",
                    "6_legacy_tech", "8_broken_or_placeholder", "9_thin_content", "10_brochure_pdf"}
    assert r["score"] == 9
    ev = r["decay_evidence"]
    for piece in ("© 2014", "ISO 9001:2008", "gmail contact", "no viewport", "marquee", "jQuery 1.8.3",
                  "WordPress 4.9", "table layout", "visitor counter", "1 broken image", "1 broken link",
                  "thin: 3 product", "brochure PDF 2015"):
        assert piece in ev, piece
    assert "—" not in ev
    assert r["checks"]["7_pagespeed"]["skipped"]
    mobiles = [m["mobile"] for m in r["contacts_found"]["mobiles"]]
    assert mobiles == ["+91 98140 12345"]          # the 01871 landline is not taken as a mobile
    assert "Proprietor" in r["contacts_found"]["mobiles"][0]["context"]
    assert r["contacts_found"]["emails"] == ["fictionalworks@gmail.com"]
    assert r["suggested"]["Corporate_Profile_Status"].startswith("Old (2015)")


def test_modern_https_site_scores_zero(sites):
    root, tls = sites
    with serve(root / "modernsite", tls=tls) as port:
        r = A.audit(f"https://127.0.0.1:{port}/", fetcher(verify=tls[0]), use_psi=False)
    assert r["status"] == "OK", r
    assert r["score"] == 0, r["decay_evidence"]
    assert r["suggested"]["Corporate_Profile_Status"].startswith("Current (2025)")
    assert "6 product/capability pages" in r["checks"]["9_thin_content"]["notes"][0]


def test_js_shell_is_flagged_not_scored_blind(sites):
    root, _ = sites
    with serve(root / "jsshell") as port:
        r = A.audit(f"http://127.0.0.1:{port}/", fetcher(), use_psi=False)
    assert r["status"] == "PARTIAL_JS" and r["manual_check"]
    for n in ("1_copyright_year", "5_free_email", "8_broken_or_placeholder", "9_thin_content", "10_brochure_pdf"):
        assert r["checks"][n]["skipped"] and not r["checks"][n]["hit"]


def test_parked_domain_counts_as_no_site(sites):
    root, _ = sites
    with serve(root / "parked") as port:
        r = A.audit(f"http://127.0.0.1:{port}/", fetcher(), use_psi=False)
    assert r["status"] == "DEAD_SITE" and r["score"] == 10 and "SEG-NOWEB" in r["segments"]


def test_robots_disallow_is_respected(sites):
    root, _ = sites
    with serve(root / "robots") as port:
        r = A.audit(f"http://127.0.0.1:{port}/", fetcher(), use_psi=False)
    assert r["status"] == "ROBOTS_DISALLOWED" and r["score"] is None


def test_anti_bot_block_is_not_bypassed_or_scored(sites):
    root, _ = sites
    with serve(root / "parked", handler=ForbiddenHandler) as port:
        r = A.audit(f"http://127.0.0.1:{port}/", fetcher(), use_psi=False)
    assert r["status"] == "SITE_BLOCKED" and r["score"] is None and r["manual_check"]


def test_unreachable_is_never_scored_as_no_website():
    r = A.audit("http://127.0.0.1:1/", fetcher(), use_psi=False)
    assert r["status"] == "UNREACHABLE" and r["score"] is None and r["manual_check"]


def test_environment_block_is_classified():
    err = A.Fetcher.classify(requests.exceptions.ProxyError("Tunnel connection failed: 403 Forbidden"))
    assert err.kind == "ENV_BLOCKED"
    err = A.Fetcher.classify(requests.exceptions.ProxyError("Tunnel connection failed: 502 Bad Gateway"))
    assert err.kind == "CONNECT"


def test_marketplace_storefront_is_platform_only():
    r = A.audit("https://www.indiamart.com/fictional-works/")
    assert r["status"] == "PLATFORM_ONLY" and r["score"] == 10


def test_cloudflare_email_decoding():
    # "info@example.com" XOR-encoded with key 0x42, the way Cloudflare obfuscates emails.
    enc = "42" + "".join(f"{ord(c) ^ 0x42:02x}" for c in "info@example.com")
    assert A.decode_cfemail(enc) == "info@example.com"
