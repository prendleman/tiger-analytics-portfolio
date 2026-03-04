# Contributing

This is a portfolio repo; contributions are welcome as suggestions or pull requests.

## How to run and test

1. **Clone and install**
   ```bash
   git clone https://github.com/prendleman/tiger-analytics-portfolio.git
   cd tiger-analytics-portfolio
   pip install -r requirements.txt
   ```

2. **Quick demo**
   ```bash
   python scripts/run_demo.py
   ```

3. **Tests**
   ```bash
   pytest tests/ -v
   ```
   (Tests generate data with `config/demo.yaml` and run the readmission model.)

4. **Validate data**
   ```bash
   python src/python/validate_data.py --data-dir data/raw
   ```

## Suggesting changes

- Open an issue to describe a bug or enhancement.
- For code: fork, create a branch, make changes, run tests, then open a pull request against `main`.

## Code and data

- **Data** in `data/raw/*.csv` is generated; do not commit large CSVs (they are gitignored). Commit only code, config, and docs.
- **Notebooks**: keep outputs cleared or minimal so diffs stay readable, or use `nbstripout` if you use it.
