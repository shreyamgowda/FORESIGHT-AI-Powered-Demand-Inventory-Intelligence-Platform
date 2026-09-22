import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="FORESIGHT | Demand & Inventory",
    page_icon="📊",
    layout="wide"
)

# API_URL = "http://127.0.0.1:8000"
API_URL = "https://foresight-api-5wxt.onrender.com"


# ============================================================
# API Helper
# ============================================================

def api_get(endpoint):

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        st.error(
            "Unable to connect to the FORESIGHT API."
        )

        st.code(str(e))

        st.stop()


# ============================================================
# API Health Check
# ============================================================

health = api_get("/health")

if health.get("status") != "healthy":

    st.error("FORESIGHT API is not healthy.")
    st.stop()


# ============================================================
# Load API Data
# ============================================================

summary = api_get("/summary")

risk_data = api_get("/risk")

risk = pd.DataFrame(risk_data)


# ============================================================
# Title
# ============================================================

st.title("FORESIGHT")

st.subheader(
    "Demand Forecasting & Inventory Intelligence"
)

st.caption(
    "Forecast demand, identify inventory risks, "
    "and prioritize inventory actions."
)


# ============================================================
# KPI Metrics
# ============================================================

total_skus = summary["total_skus"]

stockout_skus = summary["stockout_risk"]

overstock_skus = summary["overstock_risk"]

healthy_skus = summary["healthy"]


# Get forecast data for the dashboard
all_forecast = []

for sku in risk["sku_id"]:

    try:

        sku_forecast = api_get(
            f"/forecast/{sku}"
        )

        all_forecast.extend(
            sku_forecast
        )

    except Exception:
        continue


forecast = pd.DataFrame(
    all_forecast
)


def wape(actual, forecast):

    denominator = np.abs(actual).sum()

    if denominator == 0:
        return np.nan

    return (
        np.abs(actual - forecast).sum()
        / denominator
    ) * 100


if not forecast.empty:

    forecast["week_start"] = pd.to_datetime(
        forecast["week_start"]
    )

    forecast_wape = wape(
        forecast["units_sold"],
        forecast["prediction"]
    )

else:

    forecast_wape = np.nan


# ============================================================
# KPI Cards
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total SKUs",
        f"{total_skus:,}"
    )

with col2:

    st.metric(
        "Stockout Risk",
        f"{stockout_skus:,}"
    )

with col3:

    st.metric(
        "Overstock Risk",
        f"{overstock_skus:,}"
    )

with col4:

    st.metric(
        "LightGBM WAPE",
        f"{forecast_wape:.2f}%"
        if not np.isnan(forecast_wape)
        else "N/A"
    )


# ============================================================
# Forecast Section
# ============================================================

st.divider()

st.header("Forecast Performance")


if not forecast.empty:

    forecast_chart = (
        forecast
        .groupby("week_start")[
            ["units_sold", "prediction"]
        ]
        .sum()
    )

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        forecast_chart.index,
        forecast_chart["units_sold"],
        label="Actual"
    )

    ax.plot(
        forecast_chart.index,
        forecast_chart["prediction"],
        label="LightGBM Forecast"
    )

    ax.set_xlabel("Week")
    ax.set_ylabel("Units Sold")

    ax.set_title(
        "Actual vs LightGBM Forecast"
    )

    ax.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

else:

    st.warning(
        "Forecast data is unavailable."
    )


# ============================================================
# Inventory Risk Distribution
# ============================================================

st.divider()

st.subheader("Business Impact")

impact_col1, impact_col2 = st.columns(2)

with impact_col1:
    stockout_impact = risk["stockout_sales_at_risk"].sum()

    st.metric(
        "Potential Stockout Sales at Risk",
        f"₹{stockout_impact:,.0f}"
    )

with impact_col2:
    overstock_impact = risk["overstock_capital_locked"].sum()

    st.metric(
        "Overstock Capital Locked",
        f"₹{overstock_impact:,.0f}"
    )

st.header("Inventory Risk Overview")

col1, col2 = st.columns(2)


with col1:

    risk_counts = (
        risk["risk_category"]
        .value_counts()
    )

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    risk_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Inventory Risk Distribution"
    )

    ax.set_xlabel(
        "Risk Category"
    )

    ax.set_ylabel(
        "Number of SKUs"
    )

    plt.xticks(rotation=0)

    plt.tight_layout()

    st.pyplot(fig)


with col2:

    st.subheader(
        "Risk Summary"
    )

    summary_table = (
        risk["risk_category"]
        .value_counts()
        .rename_axis("Risk Category")
        .reset_index(
            name="SKU Count"
        )
    )

    st.dataframe(
        summary_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SKU Risk Analysis
# ============================================================

st.divider()

st.header("SKU Risk Analysis")


risk_options = [
    "All",
    "Stockout Risk",
    "Overstock Risk",
    "Healthy"
]


selected_risk = st.selectbox(
    "Filter by risk category",
    risk_options
)


if selected_risk == "All":

    filtered_risk = risk.copy()

else:

    filtered_risk = risk[
        risk["risk_category"]
        == selected_risk
    ].copy()


display_columns = [
    "sku_id",
    "forecast_12w",
    "stockout_sales_at_risk",
    "overstock_capital_locked",
    "on_hand_units",
    "on_order_units",
    "lead_time_days",
    "reorder_point",
    "weeks_of_cover",
    "risk_category",
    "recommended_action"
]


available_columns = [
    column
    for column in display_columns
    if column in filtered_risk.columns
]


st.dataframe(
    filtered_risk[
        available_columns
    ].sort_values(
        "weeks_of_cover"
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# Individual SKU Lookup
# ============================================================

st.divider()

st.header("SKU Details")

selected_sku = st.selectbox(
    "Select SKU",
    sorted(
        risk["sku_id"].unique()
    )
)


sku_details = api_get(
    f"/risk/{selected_sku}"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Risk Category",
        sku_details["risk_category"]
    )


with col2:

    st.metric(
        "Weeks of Cover",
        sku_details["weeks_of_cover"]
    )


with col3:

    st.metric(
        "On Hand",
        sku_details["on_hand_units"]
    )


st.info(
    f"Recommended action: "
    f"{sku_details['recommended_action']}"
)


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "FORESIGHT — Streamlit frontend powered by FastAPI"
)