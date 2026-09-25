"""wayback_check.py against a local fake archive (no internet needed)."""
import http.server
import json
import sys
import threading
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import audit_website as A  # noqa: E402
import wayback_check as W  # noqa: E402

OLD = """<html><head><link rel="stylesheet" href="/css/style-2014.css"><script src="/js/jquery-1.8.3.js"></script></head>
<body><table class="maintable"><tr><td><img src="/img/logo_old.gif" alt="logo">
<a href="/">Home</a><a href="/aboutus.htm">About Us</a><a href="/products.htm">Our Products</a></td></tr></table></body></html>"""
NEW = """<html><head><link rel="stylesheet" href="/assets/app.3f9a2b7c1d.css"><script src="/assets/app.9c1e2f3a4b.js"></script>
<meta name="generator" content="Elementor 3.21"></head><body><header class="site-header"><nav class="main-nav">
<a href="/">Home</a><a href="/company">Company</a><a href="/solutions">Solutions</a><a href="/careers">Careers</a></nav>
<img class="brand-logo" src="/assets/logo.svg" alt="logo"></header><section class="hero-banner"></section></body></html>"""
MONTHS = [f"{y}{m:02d}15093000" for y in range(2021, 2027) for m in range(1, 13) if f"{y}{m:02d}" <= "202608"]
BOUNDARY = "202501"


class FakeArchive(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith("/cdx/search/cdx"):
            body = json.dumps([["timestamp", "digest", "statuscode"]] + [[t, f"D{t}", "200"] for t in MONTHS]).encode()
        elif path.startswith("/web/"):
            ts = path.split("/")[2][:14]
            body = (NEW if ts[:6] >= BOUNDARY else OLD).encode()
        else:
            self.send_response(404); self.end_headers(); return
        self.send_response(200); self.end_headers(); self.wfile.write(body)


def test_binary_search_finds_redesign_month(monkeypatch):
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FakeArchive)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    monkeypatch.setattr(W, "ARCHIVE_BASE", f"http://127.0.0.1:{httpd.server_address[1]}")
    try:
        r = W.check("fictional-tools.example.com", A.Fetcher(delay=0, timeout=5), live_html=NEW,
                    today=date(2026, 9, 25))
    finally:
        httpd.shutdown()
    assert r["status"] == "OK"
    assert r["current_design_first_seen"] == "15-Jan-2025"
    assert r["recent_redesign"] is True and r["confidence"] == "high"
    assert r["fetches"] <= 8, r["fetches"]


def test_fingerprint_ignores_build_hashes_and_versions():
    a = W.fingerprint('<link rel="stylesheet" href="/a/main.1a2b3c4d5e.css"><script src="/j/jquery-3.6.0.min.js"></script>')
    b = W.fingerprint('<link rel="stylesheet" href="/a/main.9f8e7d6c5b.css"><script src="/j/jquery-3.7.1.min.js"></script>')
    assert a == b and W.similarity(W.fingerprint(OLD), W.fingerprint(NEW)) < W.CLEAR_CHANGE
