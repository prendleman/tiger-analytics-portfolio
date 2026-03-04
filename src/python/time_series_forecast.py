"""
PMPM time series forecasting script (runnable without notebook).
Builds member-month aggregates from claims, fits SARIMA, prints RMSE/MAPE.
Run from repo root: python src/python/time_series_forecast.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "raw"


def main():
    claims = pd.read_csv(DATA_DIR / "claims.csv")
    claims["service_month"] = pd.to_datetime(claims["submitted_date"]).dt.to_period("M")
    member_months = claims.groupby("service_month").agg(
        total_paid=("total_paid", "sum"),
        member_count=("patient_id", "nunique"),
    ).reset_index()
    member_months["service_month"] = member_months["service_month"].dt.to_timestamp()
    member_months["pmpm_paid"] = (
        member_months["total_paid"] / member_months["member_count"].replace(0, np.nan)
    )
    ts_cost = member_months.set_index("service_month")["pmpm_paid"].dropna().sort_index()
    ts_cost = ts_cost.asfreq("MS").ffill().bfill()

    from statsmodels.tsa.statespace.sarimax import SARIMAX

    n = len(ts_cost)
    train_size = max(1, int(0.8 * n))
    train, test = ts_cost.iloc[:train_size], ts_cost.iloc[train_size:]
    model = SARIMAX(train, order=(1, 0, 1), seasonal_order=(0, 0, 0, 12), enforce_stationarity=False)
    fit = model.fit(disp=False)
    pred = fit.forecast(steps=len(test))
    rmse = np.sqrt(mean_squared_error(test, pred))
    mape = mean_absolute_percentage_error(test, pred) * 100
    print(f"PMPM SARIMA forecast — RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")


if __name__ == "__main__":
    main()
