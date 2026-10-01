"""Export the built .pptx to PDF with LibreOffice (same DRAFT / v1 name).

Set SOFFICE to a wrapper if bare `soffice` hangs in your environment.
"""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
build = json.loads((ROOT / "output/.build.json").read_text())
pptx = ROOT / "output" / build["file"]
cmd = shlex.split(os.environ.get("SOFFICE", "soffice")) + [
    "--headless", "--convert-to", "pdf", "--outdir", str(ROOT / "output"), str(pptx)]
sys.exit(subprocess.call(cmd))
