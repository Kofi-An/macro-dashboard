# Macroeconomic Intelligence Dashboard

> Live macro surveillance tool tracking 18+ economic
> indicators across 10 countries, including Ghana and
> key African markets. Powered by FRED and World Bank APIs.

## Live app

[Launch Dashboard](https://macro-dashboard-vrv4nb2apxku83.streamlit.app/)

---

## What it tracks

| Section | Indicators |
|---------|------------|
| US Dashboard | GDP growth, CPI, Core CPI, unemployment, Fed funds, 10Y Treasury, WTI oil |
| Yield Curve | 10 maturities (3M to 30Y), 2Y-10Y spread, inversion alerts, recession shading |
| Global Comparison | GDP growth and CPI inflation for 10 countries |
| Ghana and Africa | GDP, inflation, unemployment, FDI inflows, GDP per capita |
| Markets | WTI crude oil, S&P 500, VIX fear index, M2 money supply |

---

## The 10 countries

| Country | Region | Why included |
|---------|--------|--------------|
| United States | North America | Global benchmark |
| United Kingdom | Europe | Major financial centre |
| Germany | Europe | Largest EU economy |
| China | Asia | Second largest economy |
| India | Asia | Fastest growing major economy |
| Brazil | Latin America | Largest LatAm economy |
| Nigeria | West Africa | Largest African economy by GDP |
| Ghana | West Africa | Home market: unique local context |
| South Africa | Southern Africa | Most industrialised African economy |
| Kenya | East Africa | East Africa financial hub |

---

## The Ghana angle

Most macro dashboards cover the US, Europe, and China.
This dashboard deliberately includes Ghana and three
other African markets, providing context that
institutional tools often omit entirely.

Ghana context tracked:
- GDP growth: including the 2011 oil discovery spike
- Inflation: including the 2022 crisis where inflation
  exceeded 50% before the IMF programme
- FDI inflows: tracking international capital flows
- GDP per capita: rising living standards over time

Africa is the world's fastest-growing fintech market.
For companies expanding into frontier markets this
local economic context is invaluable and rare.

---

## Data sources

| Source | What it provides | Update frequency |
|--------|-----------------|-----------------|
| FRED (Federal Reserve) | 18 US macro series | Hourly cache |
| World Bank REST API | 10-country comparisons | Daily cache |

All data pulled live, no static files, no stale data.

---

## Tech stack

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-red?style=flat)
![FRED API](https://img.shields.io/badge/FRED%20API-green?style=flat)
![World Bank](https://img.shields.io/badge/World%20Bank-orange?style=flat)
![Plotly](https://img.shields.io/badge/Plotly-purple?style=flat)

---

## Architecture

Modular design, data logic fully separated from
display logic. Adding a new indicator requires editing
only data_engine.py.

---

## How to run locally

```bash
git clone https://github.com/Kofi-An/macro-dashboard
cd macro-dashboard
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Create .streamlit/secrets.toml and add:
# [api_keys]
# FRED_API_KEY = "your_fred_key_here"

streamlit run app.py
```

---

## Limitations

- FRED data covers US indicators only
- World Bank data lags by 1-2 years for some countries
- Ghana informal economy is not fully captured in
  official unemployment statistics
- VIX and S&P 500 reflect US market conditions only

---

## Related projects

- [Credit Risk Scorecard](https://github.com/Kofi-An/credit-risk-scorecard)
  — AUC 0.71, $275M loss reduction
- [Portfolio Risk Dashboard](https://kofi-an-portfolio-risk-dashboard.streamlit.app)
  — Live VaR, CVaR, Monte Carlo app
- [Fraud Detection](https://github.com/Kofi-An/fraud-detection)
  — AUC-PR 0.80, 479x over random baseline

---

## Author

Kofi Anku | Financial Data Scientist
Accra, Ghana | Open to remote roles globally

[GitHub](https://github.com/Kofi-An)
[LinkedIn](www.linkedin.com/in/wka7)
[Portfolio](https://kofi-an.github.io)