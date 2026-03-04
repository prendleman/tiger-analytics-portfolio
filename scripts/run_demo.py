"""
One-command demo: generate small dataset (config/demo.yaml) then run readmission + time series.
Run from repo root: python scripts/run_demo.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list, desc: str) -> bool:
    print(f"[Demo] {desc}...")
    r = subprocess.run(cmd, cwd=REPO_ROOT)
    if r.returncode != 0:
        print(f"[Demo] {desc} failed.")
        return False
    print(f"[Demo] {desc} done.")
    return True


def main():
    demo_config = REPO_ROOT / "config" / "demo.yaml"
    if not demo_config.exists():
        print("[Demo] config/demo.yaml not found. Run full generator: python src/python/generate_healthcare_data.py")
        sys.exit(1)
    if not run(
        [sys.executable, "src/python/generate_healthcare_data.py", "--config", "config/demo.yaml"],
        "Generate data (demo config)",
    ):
        sys.exit(1)
    if not run([sys.executable, "src/python/readmission_model.py"], "Readmission model"):
        sys.exit(1)
    if not run([sys.executable, "src/python/time_series_forecast.py"], "Time series (PMPM)"):
        sys.exit(1)
    print("[Demo] All steps completed. Open notebooks in notebooks/python/ to explore.")


if __name__ == "__main__":
    main()
