# Convenience targets. Use Python directly if make is not available (e.g. Windows).
.PHONY: install demo test validate data-demo data-full pipeline export-notebooks

install:
	pip install -r requirements.txt

data-demo:
	python src/python/generate_healthcare_data.py --config config/demo.yaml

data-full:
	python src/python/generate_healthcare_data.py

demo: data-demo
	python src/python/readmission_model.py
	python src/python/time_series_forecast.py

validate:
	python src/python/validate_data.py --data-dir data/raw

test:
	pytest tests/ -v --tb=short

pipeline:
	python pipelines/run_pipeline.py --skip-data

export-notebooks:
	python scripts/export_notebooks.py
