# Macroeconomic Intelligence Dashboard

> Live macro surveillance tool tracking 18+ economic
> indicators across 10 countries — including Ghana and
> key African markets. Powered by FRED and World Bank APIs.
> No data subscriptions required.

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
| Ghana | West Africa | Home market — unique local context |
| South Africa | Southern Africa | Most industrialised African economy |
| Kenya | East Africa | East Africa financial hub |

---

## The Ghana angle

Most macro dashboards cover the US, Europe, and China.
This dashboard deliberately includes Ghana and three
other African markets — providing context that
institutional tools often omit entirely.

Ghana context tracked:
- GDP growth — including the 2011 oil discovery spike
- Inflation — including the 2022 crisis where inflation
  exceeded 50% before the IMF programme
- FDI inflows — tracking international capital flows
- GDP per capita — rising living standards over time

Africa is the world's fastest-growing fintech market.
For companies expanding into frontier markets this
local economic context is invaluable and rare.

---

## Data sources

| Source | What it provides | Update frequency |
|--------|-----------------|-----------------|
| FRED (Federal Reserve) | 18 US macro series | Hourly cache |
| World Bank REST API | 10-country comparisons | Daily cache |

All data pulled live — no static files, no stale data.
Both sources are completely free with no subscription.

---

## Tech stack

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-red?style=flat)
![FRED API](https://img.shields.io/badge/FRED%20API-green?style=flat)
![World Bank](https://img.shields.io/badge/World%20Bank-orange?style=flat)
![Plotly](https://img.shields.io/badge/Plotly-purple?style=flat)

---

## Architecture