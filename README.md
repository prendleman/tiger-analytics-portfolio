# Healthcare Analytics Portfolio

Portfolio project demonstrating **Lead Data Scientist** skills: Python and R, ML (classification), complex SQL, dimensional/relational data modeling, and healthcare-domain analytics. Aligned with roles in analytics consulting (e.g. Tiger Analytics) and healthcare/life sciences.

## Skills mapped to JD

| JD requirement | Where demonstrated |
|----------------|--------------------|
| **Python & R** | Python: data generation, readmission model, EDA notebook. R: descriptive analytics and visualization (Rmd + script). |
| **Machine learning** | 30-day readmission binary classification (Random Forest); feature engineering from encounters, diagnoses, labs. |
| **Complex SQL** | `sql/feature_readmission.sql` (joins, CTEs, aggregations); `sql/report_utilization_kpis.sql` (reporting KPIs). |
| **Dimensional / relational modeling** | `data/schema/ddl.sql` and `data/schema/README.md`: star-style relationships, reference tables, data dictionary, ER overview. |
| **Healthcare / pharma domain** | Mock schema and data: patients, encounters, diagnoses, procedures, medications, labs, claims, readmissions, risk scores. |
| **Reproducibility & communication** | README, `docs/methodology.md`, requirements.txt, clear paths and run instructions. |

## Repository structure

```
README.md                 # This file
data/
  raw/                     # Generated CSVs (run generator first)
  schema/                 # DDL, data dictionary, ER (see schema/README.md)
notebooks/
  python/                  # Jupyter: readmission prediction (EDA + ML)
  r/                       # R Markdown: descriptive analytics & viz
src/
  python/                  # Data generation, readmission model script
  r/                       # R script: EDA summary
sql/                       # Feature table + utilization KPIs
docs/                      # Methodology, assumptions, limitations
requirements.txt
```

## Setup and run

### 1. Environment

```bash
cd tiger-analytics-portfolio
pip install -r requirements.txt
```

### 2. Generate mock data

Output is written to `data/raw/` (CSVs). Config (row counts, date range) is in `src/python/generate_healthcare_data.py`.

```bash
python src/python/generate_healthcare_data.py
```

### 3. Python: readmission model

```bash
python src/python/readmission_model.py
```

Or open and run `notebooks/python/readmission_prediction.ipynb` (Jupyter).

### 4. R: descriptive analytics

From repo root:

```bash
Rscript src/r/healthcare_eda.R
```

Or knit `notebooks/r/healthcare_eda.Rmd` to HTML (RStudio or `rmarkdown::render()`).

### 5. SQL

- Load schema: run `data/schema/ddl.sql` in your database (SQL Server or PostgreSQL).
- Load CSVs into the tables (bulk insert or ETL), then run:
  - `sql/feature_readmission.sql` — encounter-level feature set for ML/reporting.
  - `sql/report_utilization_kpis.sql` — utilization and cost by facility and payer.

## Data summary

- **Reference**: facility types, specialties, ICD/CPT/NDC codes.
- **Core**: patients, encounters, diagnoses, procedures, medications, labs, vitals.
- **Utilization**: claims, claim lines, utilization events.
- **Outcomes**: readmissions (30-day flag), adverse events, risk scores.

See `data/schema/README.md` for the full data dictionary and ER diagram.

## Methodology and limitations

- **Methodology**: `docs/methodology.md` — target definition, features, model choice, and reproducibility notes.
- **Limitations**: Data is synthetic (Faker + pandas); not for clinical or production use. Model is for portfolio demonstration only.

## Resume

Resume available on request.
