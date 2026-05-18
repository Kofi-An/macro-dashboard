import pandas as pd
import numpy as np
import streamlit as st
from fredapi import Fred
import requests
import warnings
warnings.filterwarnings("ignore")


# === FRED API SETUP ===
def get_fred_client():
    """Initialise FRED client with API key."""
    try:
        api_key = st.secrets["api_keys"]["FRED_API_KEY"]
        return Fred(api_key=api_key)
    except Exception as e:
        st.error(f"FRED API key error: {e}")
        return None


@st.cache_data(ttl=3600)
def fetch_fred_series(series_id: str,
                      start: str = "2000-01-01") -> pd.Series:
    """Fetch a single FRED series. Cached 1 hour."""
    try:
        fred = get_fred_client()
        if fred is None:
            return pd.Series(dtype=float)
        data = fred.get_series(
            series_id,
            observation_start=start
        )
        return data.dropna()
    except Exception as e:
        st.warning(f"Could not fetch {series_id}: {e}")
        return pd.Series(dtype=float)


@st.cache_data(ttl=3600)
def fetch_us_indicators() -> dict:
    """Fetch 18 US macro indicators from FRED."""
    indicators = {
        "gdp_growth":      "A191RL1Q225SBEA",
        "gdp_level":       "GDP",
        "real_gdp":        "GDPC1",
        "cpi":             "CPIAUCSL",
        "core_cpi":        "CPILFESL",
        "pce":             "PCEPI",
        "unemployment":    "UNRATE",
        "nonfarm_payroll": "PAYEMS",
        "labour_force":    "CIVPART",
        "fed_funds":       "FEDFUNDS",
        "rate_10y":        "GS10",
        "rate_2y":         "GS2",
        "rate_3m":         "TB3MS",
        "rate_30y":        "GS30",
        "oil_wti":         "DCOILWTICO",
        "vix":             "VIXCLS",
        "sp500":           "SP500",
        "m2":              "M2SL",
    }
    result = {}
    for name, series_id in indicators.items():
        result[name] = fetch_fred_series(series_id)
    return result


@st.cache_data(ttl=3600)
def fetch_yield_curve() -> pd.DataFrame:
    """Build US Treasury yield curve from FRED."""
    maturities = {
        "3M":  "TB3MS",
        "6M":  "TB6MS",
        "1Y":  "GS1",
        "2Y":  "GS2",
        "3Y":  "GS3",
        "5Y":  "GS5",
        "7Y":  "GS7",
        "10Y": "GS10",
        "20Y": "GS20",
        "30Y": "GS30"
    }
    data = {}
    for mat, series_id in maturities.items():
        series = fetch_fred_series(
            series_id, start="2015-01-01")
        if not series.empty:
            data[mat] = series
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    return df.dropna(how="all")


# ============================================
# WORLD BANK — direct REST API (no wbgapi)
# ============================================
def fetch_wb_series(indicator: str,
                    country_code: str,
                    start: int = 2000,
                    end: int = 2024) -> pd.Series:
    """
    Fetch one World Bank indicator for one country
    using the standard REST API directly.
    Much more reliable than wbgapi for bulk queries.
    """
    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{country_code}/indicator/{indicator}"
        f"?date={start}:{end}&format=json&per_page=100"
    )
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return pd.Series(dtype=float)
        data = response.json()
        if len(data) < 2 or not data[1]:
            return pd.Series(dtype=float)
        records = {
            int(item["date"]): item["value"]
            for item in data[1]
            if item["value"] is not None
        }
        series = pd.Series(records).sort_index()
        return series
    except Exception:
        return pd.Series(dtype=float)


@st.cache_data(ttl=86400)
def fetch_global_gdp_growth() -> pd.DataFrame:
    """
    GDP growth for 10 countries via World Bank REST API.
    Fetched one country at a time — most reliable approach.
    """
    countries = {
        "US": "United States",
        "GB": "United Kingdom",
        "DE": "Germany",
        "CN": "China",
        "NG": "Nigeria",
        "GH": "Ghana",
        "ZA": "South Africa",
        "KE": "Kenya",
        "IN": "India",
        "BR": "Brazil"
    }
    result = {}
    for code, name in countries.items():
        series = fetch_wb_series(
            "NY.GDP.MKTP.KD.ZG", code)
        if not series.empty:
            result[name] = series

    if not result:
        return pd.DataFrame()
    df = pd.DataFrame(result).sort_index()
    return df.dropna(how="all")


@st.cache_data(ttl=86400)
def fetch_global_inflation() -> pd.DataFrame:
    """
    CPI inflation for 10 countries via World Bank REST API.
    """
    countries = {
        "US": "United States",
        "GB": "United Kingdom",
        "DE": "Germany",
        "CN": "China",
        "NG": "Nigeria",
        "GH": "Ghana",
        "ZA": "South Africa",
        "KE": "Kenya",
        "IN": "India",
        "BR": "Brazil"
    }
    result = {}
    for code, name in countries.items():
        series = fetch_wb_series(
            "FP.CPI.TOTL.ZG", code)
        if not series.empty:
            result[name] = series

    if not result:
        return pd.DataFrame()
    df = pd.DataFrame(result).sort_index()
    return df.dropna(how="all")


@st.cache_data(ttl=86400)
def fetch_ghana_indicators() -> dict:
    """
    Ghana-specific indicators via World Bank REST API.
    """
    indicators = {
        "gdp_growth":     "NY.GDP.MKTP.KD.ZG",
        "inflation":      "FP.CPI.TOTL.ZG",
        "unemployment":   "SL.UEM.TOTL.ZS",
        "gdp_per_capita": "NY.GDP.PCAP.CD",
        "fdi_inflows":    "BX.KLT.DINV.WD.GD.ZS",
        "exports_gdp":    "NE.EXP.GNFS.ZS",
    }
    result = {}
    for name, indicator in indicators.items():
        series = fetch_wb_series(indicator, "GH")
        result[name] = series
    return result


def calculate_yoy_change(series: pd.Series,
                          periods: int = 12) -> pd.Series:
    """Year-over-year percentage change."""
    return series.pct_change(periods=periods) * 100


def get_latest_value(series: pd.Series) -> tuple:
    """Get latest value and date. Returns (value, date)."""
    if series is None or series.empty:
        return None, "N/A"
    clean = series.dropna()
    if clean.empty:
        return None, "N/A"
    return float(clean.iloc[-1]), str(clean.index[-1])[:10]


def get_recession_periods() -> list:
    """US recession periods for chart shading."""
    return [
        ("2001-03-01", "2001-11-01"),
        ("2007-12-01", "2009-06-01"),
        ("2020-02-01", "2020-04-01"),
    ]