"""Write docs/notebooks/index.html linking exported notebook HTML files."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "docs" / "notebooks"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = sorted(p for p in OUT.glob("*.html") if p.name != "index.html")
    items = "\n".join(
        f'    <li><a href="{p.name}">{p.stem.replace("_", " ")}</a></li>' for p in pages
    )
    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Portfolio notebooks (static)</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ font-size: 1.25rem; }}
    ul {{ line-height: 1.8; }}
  </style>
</head>
<body>
  <h1>Healthcare analytics portfolio — notebooks (HTML)</h1>
  <p>Exported from <code>notebooks/python/*.ipynb</code>. Regenerate locally with
  <code>python scripts/export_notebooks.py</code>.</p>
  <ul>
{items}
  </ul>
</body>
</html>
"""
    (OUT / "index.html").write_text(body, encoding="utf-8")
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
