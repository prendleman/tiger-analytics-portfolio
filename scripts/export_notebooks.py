"""
Export all Python notebooks to HTML for static viewing (e.g. docs or GitHub Pages).
Requires: pip install nbconvert
Run from repo root: python scripts/export_notebooks.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NB_DIR = REPO_ROOT / "notebooks" / "python"
OUT_DIR = REPO_ROOT / "docs" / "notebooks"
OUT_DIR.mkdir(parents=True, exist_ok=True)

try:
    import nbconvert
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
    import nbconvert

from nbconvert import HTMLExporter
import nbformat

for path in sorted(NB_DIR.glob("*.ipynb")):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(nb)
    out_path = OUT_DIR / (path.stem + ".html")
    out_path.write_text(body, encoding="utf-8")
    print(f"  {path.name} -> {out_path.relative_to(REPO_ROOT)}")
print("Done. Open docs/notebooks/*.html in a browser.")
