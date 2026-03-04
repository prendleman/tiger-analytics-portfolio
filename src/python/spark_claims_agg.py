"""
Spark job: aggregate claims by month (PMPM-style) from CSV.
Runnable with: spark-submit src/python/spark_claims_agg.py
  or from repo root: python -m pyspark < src/python/spark_claims_agg.py (inline).
Requires PySpark: pip install pyspark
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "raw"
OUT_DIR = REPO_ROOT / "data" / "processed"

claims_path = DATA_DIR / "claims.csv"
out_path = OUT_DIR / "claims_by_month"

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
except ImportError:
    print("PySpark required: pip install pyspark")
    raise

spark = SparkSession.builder.appName("healthcare_claims_agg").getOrCreate()
df = spark.read.option("header", "true").option("inferSchema", "true").csv(str(claims_path))
df = df.withColumn("month", F.date_trunc("month", F.to_date(F.col("submitted_date"))))
agg = (
    df.groupBy("month")
    .agg(
        F.sum("total_paid").alias("total_paid"),
        F.sum("total_charge").alias("total_charge"),
        F.countDistinct("patient_id").alias("member_count"),
        F.count("claim_id").alias("claim_count"),
    )
    .withColumn("pmpm_paid", F.col("total_paid") / F.col("member_count"))
)
OUT_DIR.mkdir(parents=True, exist_ok=True)
agg.write.mode("overwrite").parquet(str(out_path))
print(f"Wrote {out_path}")
spark.stop()
