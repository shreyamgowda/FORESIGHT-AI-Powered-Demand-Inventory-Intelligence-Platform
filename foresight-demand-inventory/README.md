# FORESIGHT — Demand Forecasting & Inventory Intelligence

## 1. Project Overview

FORESIGHT is a demand forecasting and inventory decision-support system designed to help businesses anticipate product demand and identify inventory risks at the SKU level.

The system combines:

- Data quality checks and exploratory analysis
- Demand forecasting
- Baseline comparison
- LightGBM forecasting
- Inventory risk scoring
- Recommended inventory actions
- FastAPI backend
- Streamlit dashboard

---

## 2. Business Problem

Poor demand forecasting can lead to:

- Stockouts and lost sales
- Excess inventory
- Capital being tied up in inventory
- Inefficient replenishment decisions

FORESIGHT uses historical sales, product information, calendar information, and inventory snapshots to forecast demand and provide actionable SKU-level inventory insights.

---

## 3. Objectives

The main objectives are to:

1. Forecast future SKU-level demand.
2. Compare the machine-learning model against a simple baseline.
3. Identify SKUs with potential stockout risk.
4. Estimate potential sales at risk from insufficient inventory.
5. Identify excess inventory where supported by the available data.
6. Provide recommended inventory actions.
7. Expose the results through an API and interactive dashboard.

---

## 4. Dataset

The project uses a structured retail-style dataset containing four main sources.

### SKU Master

Contains product-level information:

- SKU ID
- Category
- Subcategory
- Launch date
- Unit cost
- List price

### Daily Sales

Contains:

- Date
- SKU ID
- Units sold
- Revenue
- Unit price
- Promotion flag

### Calendar

Contains:

- Date
- Week
- Month
- Season
- Holiday indicator
- Promotional event

### Inventory Snapshots

Contains:

- Date
- SKU ID
- On-hand units
- On-order units
- Lead time
- Reorder point

---

## 5. Project Structure

```text
foresight-demand-inventory/
│
├── app/
│   └── streamlit_app.py
│
├── service/
│   └── main.py
│
├── src/
│   ├── forecast.py
│   ├── pipeline.py
│   └── risk.py
│
├── notebooks/
│   ├── 01_data_quality_eda.ipynb
│   ├── 02_baseline.ipynb
│   ├── 03_forecasting_model.ipynb
│   └── 04_inventory_risk.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
└── README.md
```

---

## 6. Workflow

```text
Raw Data
   ↓
Data Quality & EDA
   ↓
Baseline Forecast
   ↓
LightGBM Forecast
   ↓
Inventory Risk Scoring
   ↓
FastAPI Backend
   ↓
Streamlit Dashboard
```

---

## 7. Data Quality & EDA

The first notebook performs data inspection and exploratory analysis.

The analysis includes:

- Dataset shape and structure
- Missing-value checks
- Duplicate checks
- Data-type validation
- Zero-sales analysis
- Promotional activity analysis
- Sales distribution
- Category-level analysis
- Time-based demand patterns

The cleaned and validated data is then used for downstream forecasting.

---

## 8. Forecasting

### Baseline

A seasonal-naive forecasting approach is used as the baseline.

The baseline provides a simple benchmark against which the machine-learning model can be evaluated.

### LightGBM

The forecasting model uses LightGBM regression.

Features include time-based and historical demand information derived from the available sales and calendar data.

The model predicts future SKU-level demand.

---

## 9. Forecasting Results

The current evaluation produced the following results:

| Model | WAPE |
|---|---:|
| Seasonal-Naive Baseline | 30.34% |
| LightGBM | 13.44% |

### Improvement

The LightGBM model improved WAPE by:

**16.90 percentage points**

This corresponds to a substantial reduction in forecast error compared with the baseline.

---

## 10. Inventory Risk Scoring

The inventory risk layer combines:

- Forecasted demand
- Current on-hand inventory
- On-order inventory
- Lead time
- Reorder point
- Unit cost
- List price

Each SKU receives:

- 12-week forecast
- Average weekly forecast
- Lead-time demand
- Weeks of inventory cover
- Stockout units at risk
- Potential stockout sales at risk
- Excess inventory units
- Overstock capital locked
- Risk category
- Recommended action

### Risk Categories

The system classifies SKUs into:

- **Stockout Risk**
- **Overstock Risk**
- **Healthy**

---

## 11. Current Risk Results

The current dataset contains 200 SKUs.

| Risk Category | SKU Count |
|---|---:|
| Healthy | 105 |
| Stockout Risk | 95 |
| Overstock Risk | 0 |

The current dataset did not produce any overstock-risk SKUs under the defined inventory threshold.

This result is reported as observed rather than artificially generating overstock cases.

---

## 12. Business Impact

The current risk assessment estimates:

### Potential Stockout Sales at Risk

**₹7.49 crore**

This represents potential sales associated with forecast demand that may not be covered by available inventory during the estimated lead-time period.

It should be interpreted as **potential sales at risk**, not guaranteed financial loss.

### Overstock Capital Locked

**₹0**

No overstock capital was identified under the current dataset and defined threshold.

---

## 13. Recommended Actions

The system provides SKU-level recommendations.

### Stockout Risk

**Prioritize replenishment**

### Overstock Risk

**Reduce or defer replenishment**

### Healthy

**Maintain current inventory**

---

## 14. FastAPI Backend

FORESIGHT includes a FastAPI backend that exposes forecasting and inventory-risk results through API endpoints.

The backend is located at:

`service/main.py`

The API is used by the Streamlit application to retrieve dashboard data.

### Local API

`http://127.0.0.1:8000`

The FastAPI documentation can be accessed locally at:

`http://127.0.0.1:8000/docs`

---

## 15. Streamlit Dashboard

The Streamlit application provides an interactive interface for:

- Forecast performance
- Inventory risk distribution
- Business-impact metrics
- SKU-level risk analysis
- Recommended inventory actions
- Individual SKU lookup

The dashboard is located at:

`app/streamlit_app.py`

The Streamlit frontend communicates with the FastAPI backend.

---

## 16. Running the Project Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd foresight-demand-inventory
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scriptsctivate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI backend

```bash
uvicorn service.main:app --reload
```

The API will run at:

`http://127.0.0.1:8000`

### 6. Run the Streamlit dashboard

Open another terminal and run:

```bash
streamlit run app/streamlit_app.py
```

The dashboard will open in the browser.

---

## 17. Notebooks

### Notebook 1 — Data Quality & EDA

Performs data validation, cleaning, and exploratory analysis.

### Notebook 2 — Baseline

Builds and evaluates the baseline forecasting approach.

### Notebook 3 — Forecasting Model

Trains the LightGBM forecasting model and evaluates it against the baseline.

### Notebook 4 — Inventory Risk

Combines forecasts with inventory information to generate risk scores and recommended actions.

---

## 18. Limitations

The current implementation has several limitations:

- The dataset is a structured retail-style dataset and may not represent every real-world retail environment.
- Forecast accuracy can vary across individual SKUs.
- Potential sales at risk should not be interpreted as guaranteed lost revenue.
- The current dataset produced no overstock-risk SKUs under the defined threshold.
- Inventory decisions should consider operational constraints and business policies in addition to model outputs.
- Further validation on real production data would be required before operational deployment.

---


## 19. Conclusion

FORESIGHT combines demand forecasting with inventory intelligence to support better replenishment decisions.

The LightGBM model achieved a WAPE of **13.44%**, compared with **30.34%** for the seasonal-naive baseline.

The system extends forecasting into an operational decision-support layer by estimating inventory risk, potential sales at risk, and recommended actions at the SKU level.

The final system provides both:

- A **FastAPI backend** for programmatic access
- A **Streamlit dashboard** for interactive business analysis

## 20. Deployment

FORESIGHT is deployed using separate frontend and backend services.

### Streamlit Dashboard

The Streamlit dashboard is deployed on Streamlit Community Cloud.

**Live Dashboard:**

https://foresight-dashboard-83ro.onrender.com

The dashboard provides:

- Forecast performance
- Inventory risk overview
- SKU-level risk analysis
- Business-impact metrics
- Recommended inventory actions

### FastAPI Backend

The FastAPI backend is deployed on Render.

**Live API:**

https://foresight-api-5wxt.onrender.com

**API Documentation:**

https://foresight-api-5wxt.onrender.com/docs

The FastAPI backend provides the forecasting and inventory-risk data consumed by the Streamlit dashboard.

The Streamlit frontend communicates with the deployed FastAPI backend through HTTPS.

## 21. System Architecture

### Application Workflow

```text
Raw Data
   ↓
Data Quality & EDA
   ↓
Baseline Forecast
   ↓
LightGBM Forecast
   ↓
Inventory Risk Scoring
   ↓
FastAPI Backend
   ↓
Streamlit Dashboard
   ↓
Business Decisions

User
  ↓
Streamlit Community Cloud
  ↓
HTTPS
  ↓
Render FastAPI Backend
  ↓
Forecast & Inventory Risk Data
  ↓
Business Insights

```


## 22. Live API

### FastAPI Backend

**Base URL:**

https://foresight-demand-inventory.onrender.com

### API Documentation

https://foresight-demand-inventory.onrender.com/docs

The `/docs` endpoint provides interactive Swagger documentation for the deployed FastAPI service.

### Health Check

```text
GET /health


### Section 23 — Final Project Results

```markdown
## 23. Final Project Results

### Forecasting Performance

| Model | WAPE |
|---|---:|
| Seasonal-Naive Baseline | 30.34% |
| LightGBM | 13.44% |

**Improvement: 16.90 percentage points**

### Inventory Risk

| Risk Category | SKU Count |
|---|---:|
| Healthy | 105 |
| Stockout Risk | 95 |
| Overstock Risk | 0 |

### Business Impact

- **Total SKUs analyzed:** 200
- **Potential stockout sales at risk:** ₹7.49 crore
- **Overstock capital locked:** ₹0

The stockout sales figure represents potential sales exposure based on forecast demand and available inventory during the estimated lead-time period. It should not be interpreted as guaranteed lost revenue.

