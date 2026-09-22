from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException


# ============================================================
# Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = ROOT_DIR / "data" / "processed"


# ============================================================
# Load Data
# ============================================================

risk_path = PROCESSED_DIR / "inventory_risk_scores.csv"
forecast_path = PROCESSED_DIR / "forecast_predictions.csv"

risk_df = pd.read_csv(risk_path)

forecast_df = pd.read_csv(forecast_path)

forecast_df["week_start"] = pd.to_datetime(
    forecast_df["week_start"]
)


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="FORESIGHT API",
    description="Demand forecasting and inventory intelligence API",
    version="1.0.0"
)


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FORESIGHT API"
    }


# ============================================================
# Summary
# ============================================================

@app.get("/summary")
def summary():

    total_skus = risk_df["sku_id"].nunique()

    stockout_risk = (
        risk_df["risk_category"]
        == "Stockout Risk"
    ).sum()

    overstock_risk = (
        risk_df["risk_category"]
        == "Overstock Risk"
    ).sum()

    healthy = (
        risk_df["risk_category"]
        == "Healthy"
    ).sum()

    return {
        "total_skus": int(total_skus),
        "stockout_risk": int(stockout_risk),
        "overstock_risk": int(overstock_risk),
        "healthy": int(healthy)
    }


# ============================================================
# Inventory Risk
# ============================================================

@app.get("/risk")
def inventory_risk():

    return risk_df.to_dict(
        orient="records"
    )


# ============================================================
# Single SKU Risk
# ============================================================

@app.get("/risk/{sku_id}")
def sku_risk(sku_id: str):

    result = risk_df[
        risk_df["sku_id"] == sku_id
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"SKU {sku_id} not found"
        )

    return result.iloc[0].to_dict()


# ============================================================
# Forecast
# ============================================================

@app.get("/forecast/{sku_id}")
def sku_forecast(sku_id: str):

    result = forecast_df[
        forecast_df["sku_id"] == sku_id
    ].copy()

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"SKU {sku_id} not found"
        )

    result["week_start"] = (
        result["week_start"]
        .dt.strftime("%Y-%m-%d")
    )

    return result.to_dict(
        orient="records"
    )