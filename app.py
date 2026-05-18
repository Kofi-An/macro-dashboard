import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

from data_engine import (
    fetch_us_indicators,
    fetch_yield_curve,
    fetch_global_gdp_growth,
    fetch_global_inflation,
    fetch_ghana_indicators,
    get_latest_value,
    calculate_yoy_change,
    get_recession_periods
)

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Macro Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === SIDEBAR ===
with st.sidebar:
    st.title("🌍 Macro Intelligence")
    st.markdown("*Built by Kofi-An | Financial Data Scientist*")
    st.divider()

    section = st.radio(
        "Navigate to",
        options=[
            "📊 US Dashboard",
            "📈 Yield Curve",
            "🌐 Global Comparison",
            "🇬🇭 Ghana & Africa",
            "🛢️ Markets"
        ]
    )

    st.divider()
    st.markdown("""
    **Data sources**
    - FRED (Federal Reserve)
    - World Bank Open Data
    - Updated: hourly (FRED)
    - Updated: daily (World Bank)
    """)
    st.divider()
    st.caption(
        "All data pulled live from official government "
        "and multilateral sources. No data subscriptions "
        "required."
    )

# === LOAD DATA ===
with st.spinner("Loading macroeconomic data..."):
    us_data    = fetch_us_indicators()
    yc_data    = fetch_yield_curve()
    gdp_data   = fetch_global_gdp_growth()
    inf_data   = fetch_global_inflation()
    gh_data    = fetch_ghana_indicators()
    recessions = get_recession_periods()


# ============================================
# SECTION 1 — US DASHBOARD
# ============================================
if section == "📊 US Dashboard":
    st.title("United States — Macroeconomic Dashboard")
    st.caption("Source: Federal Reserve Economic Data (FRED)")

    # KPI row
    gdp_val,  _ = get_latest_value(us_data["gdp_growth"])
    cpi_val,  _ = get_latest_value(
        calculate_yoy_change(us_data["cpi"]))
    unem_val, _ = get_latest_value(us_data["unemployment"])
    ff_val,   _ = get_latest_value(us_data["fed_funds"])
    r10_val,  _ = get_latest_value(us_data["rate_10y"])
    oil_val,  _ = get_latest_value(us_data["oil_wti"])

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("GDP Growth",
              f"{gdp_val:.1f}%" if gdp_val else "N/A",
              help="Real GDP QoQ annualised")
    c2.metric("CPI Inflation",
              f"{cpi_val:.1f}%" if cpi_val else "N/A",
              help="Year-over-year CPI change")
    c3.metric("Unemployment",
              f"{unem_val:.1f}%" if unem_val else "N/A")
    c4.metric("Fed Funds Rate",
              f"{ff_val:.2f}%" if ff_val else "N/A")
    c5.metric("10Y Treasury",
              f"{r10_val:.2f}%" if r10_val else "N/A")
    c6.metric("WTI Oil",
              f"${oil_val:.1f}" if oil_val else "N/A")

    st.divider()

    # Chart row 1 — GDP and Inflation
    col1, col2 = st.columns(2)

    with col1:
        if not us_data["gdp_growth"].empty:
            gdp_df = us_data["gdp_growth"].reset_index()
            gdp_df.columns = ["Date", "GDP Growth %"]
            fig = px.bar(
                gdp_df.tail(40),
                x="Date",
                y="GDP Growth %",
                title="US Real GDP Growth (QoQ Annualised)",
                color="GDP Growth %",
                color_continuous_scale=[
                    "#D85A30", "#FAEEDA", "#1D9E75"]
            )
            fig.add_hline(
                y=0, line_dash="dash",
                line_color="grey")
            fig.update_layout(
                height=350, showlegend=False)
            st.plotly_chart(
                fig, use_container_width=True)

    with col2:
        if not us_data["cpi"].empty:
            cpi_yoy  = calculate_yoy_change(
                us_data["cpi"]).dropna()
            core_yoy = calculate_yoy_change(
                us_data["core_cpi"]).dropna()

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=cpi_yoy.index,
                y=cpi_yoy,
                name="CPI",
                line=dict(color="#D85A30", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=core_yoy.index,
                y=core_yoy,
                name="Core CPI",
                line=dict(color="#378ADD", width=2)
            ))
            fig.add_hline(
                y=2, line_dash="dash",
                line_color="green",
                annotation_text="Fed 2% target"
            )
            fig.update_layout(
                title="US Inflation — CPI vs Core CPI (YoY)",
                height=350,
                yaxis_title="%"
            )
            st.plotly_chart(
                fig, use_container_width=True)

    # Chart row 2 — Labour and Rates
    col3, col4 = st.columns(2)

    with col3:
        if not us_data["unemployment"].empty:
            unem_df = us_data["unemployment"].reset_index()
            unem_df.columns = ["Date", "Rate"]
            fig = px.area(
                unem_df,
                x="Date", y="Rate",
                title="US Unemployment Rate",
                color_discrete_sequence=["#378ADD"]
            )
            for start, end in recessions:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="red", opacity=0.1,
                    layer="below", line_width=0
                )
            fig.update_layout(height=350)
            fig.update_yaxes(ticksuffix="%")
            st.plotly_chart(
                fig, use_container_width=True)
            st.caption(
                "Red shading = US recessions "
                "(dot-com 2001, GFC 2008, COVID 2020)"
            )

    with col4:
        if not us_data["fed_funds"].empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=us_data["fed_funds"].index,
                y=us_data["fed_funds"],
                name="Fed Funds",
                line=dict(color="#D85A30", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=us_data["rate_10y"].index,
                y=us_data["rate_10y"],
                name="10Y Treasury",
                line=dict(color="#378ADD", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=us_data["rate_2y"].index,
                y=us_data["rate_2y"],
                name="2Y Treasury",
                line=dict(
                    color="#7F77DD",
                    width=2,
                    dash="dash")
            ))
            fig.update_layout(
                title="US Interest Rates",
                height=350,
                yaxis_title="%"
            )
            st.plotly_chart(
                fig, use_container_width=True)


# ============================================
# SECTION 2 — YIELD CURVE
# ============================================
elif section == "📈 Yield Curve":
    st.title("US Treasury Yield Curve")
    st.markdown(
        "The yield curve plots Treasury yields across "
        "maturities. An **inverted curve** (short rates "
        "> long rates) has preceded every US recession "
        "since 1955."
    )

    if not yc_data.empty:
        dates = yc_data.dropna(how="all").index

        # Safe index — handles fewer than 252 data points
        n = len(dates)
        idx_1y  = max(0, n - 252)
        idx_3m  = max(0, n - 63)
        idx_now = n - 1

        default_dates = list(dict.fromkeys([
            str(dates[idx_now])[:10],
            str(dates[idx_3m])[:10],
            str(dates[idx_1y])[:10]
        ]))

        selected_dates = st.multiselect(
            "Select dates to compare",
            options=[str(d)[:10]
                     for d in dates[-252:]],
            default=default_dates
        )

        if selected_dates:
            fig = go.Figure()
            colors = ["#378ADD", "#D85A30",
                      "#1D9E75", "#7F77DD", "#BA7517"]
            maturities = yc_data.columns.tolist()

            for i, date in enumerate(selected_dates):
                date_data = yc_data[
                    yc_data.index.astype(str
                    ).str[:10] == date]
                if not date_data.empty:
                    fig.add_trace(go.Scatter(
                        x=maturities,
                        y=date_data.iloc[0].values,
                        name=date,
                        line=dict(
                            color=colors[
                                i % len(colors)],
                            width=2.5
                        ),
                        mode="lines+markers"
                    ))

            fig.update_layout(
                title="US Treasury Yield Curve",
                xaxis_title="Maturity",
                yaxis_title="Yield (%)",
                height=450
            )
            fig.update_yaxes(ticksuffix="%")
            st.plotly_chart(
                fig, use_container_width=True)

        # 2Y-10Y spread
        st.subheader(
            "2Y-10Y Spread — Recession Predictor")
        if ("rate_2y" in us_data and
                "rate_10y" in us_data):
            spread = (
                us_data["rate_10y"] -
                us_data["rate_2y"]
            ).dropna()
            spread_df = spread.reset_index()
            spread_df.columns = ["Date", "Spread"]

            fig2 = px.area(
                spread_df,
                x="Date", y="Spread",
                title="10Y-2Y Treasury Spread",
                color_discrete_sequence=["#378ADD"]
            )
            fig2.add_hline(
                y=0, line_dash="dash",
                line_color="red",
                annotation_text="Inversion threshold"
            )
            for start, end in recessions:
                fig2.add_vrect(
                    x0=start, x1=end,
                    fillcolor="red", opacity=0.1,
                    layer="below", line_width=0
                )
            fig2.update_layout(height=350)
            fig2.update_yaxes(ticksuffix="%")
            st.plotly_chart(
                fig2, use_container_width=True)
            st.caption(
                "Red shading = US recessions. "
                "Curve inverts before each recession."
            )


# ============================================
# SECTION 3 — GLOBAL COMPARISON
# ============================================
elif section == "🌐 Global Comparison":
    st.title("Global Macroeconomic Comparison")
    st.caption("Source: World Bank Open Data")

    tab1, tab2 = st.tabs(["GDP Growth", "Inflation"])

    with tab1:
        if not gdp_data.empty:
            latest_gdp = gdp_data.iloc[-1].dropna()
            fig = px.bar(
                x=latest_gdp.index,
                y=latest_gdp.values,
                title="GDP Growth Rate — Latest Year",
                labels={
                    "x": "Country",
                    "y": "GDP Growth %"
                },
                color=latest_gdp.values,
                color_continuous_scale=[
                    "#D85A30", "#FAEEDA", "#1D9E75"]
            )
            fig.add_hline(
                y=0, line_dash="dash",
                line_color="grey")
            fig.update_layout(
                height=400, showlegend=False)
            st.plotly_chart(
                fig, use_container_width=True)

            selected_countries = st.multiselect(
                "Select countries for time series",
                options=gdp_data.columns.tolist(),
                default=[
                    "United States", "Ghana",
                    "China", "Nigeria"
                ]
            )
            if selected_countries:
                fig2 = px.line(
                    gdp_data[selected_countries],
                    title="GDP Growth — Historical",
                    labels={
                        "value": "Growth %",
                        "index": "Year"
                    }
                )
                fig2.add_hline(
                    y=0, line_dash="dash",
                    line_color="grey")
                fig2.update_layout(height=400)
                st.plotly_chart(
                    fig2, use_container_width=True)

    with tab2:
        if not inf_data.empty:
            latest_inf = inf_data.iloc[-1].dropna()
            fig = px.bar(
                x=latest_inf.index,
                y=latest_inf.values,
                title="CPI Inflation — Latest Year",
                labels={
                    "x": "Country",
                    "y": "Inflation %"
                },
                color=latest_inf.values,
                color_continuous_scale=[
                    "#1D9E75", "#FAEEDA", "#D85A30"]
            )
            fig.add_hline(
                y=2, line_dash="dash",
                line_color="green",
                annotation_text="2% benchmark"
            )
            fig.update_layout(
                height=400, showlegend=False)
            st.plotly_chart(
                fig, use_container_width=True)

            selected_inf = st.multiselect(
                "Select countries for time series",
                options=inf_data.columns.tolist(),
                default=[
                    "United States", "Ghana",
                    "Nigeria", "United Kingdom"
                ]
            )
            if selected_inf:
                fig3 = px.line(
                    inf_data[selected_inf],
                    title="Inflation — Historical",
                    labels={
                        "value": "Inflation %",
                        "index": "Year"
                    }
                )
                fig3.add_hline(
                    y=2, line_dash="dash",
                    line_color="green")
                fig3.update_layout(height=400)
                st.plotly_chart(
                    fig3, use_container_width=True)


# ============================================
# SECTION 4 — GHANA AND AFRICA
# ============================================
elif section == "🇬🇭 Ghana & Africa":
    st.title("Ghana & African Markets")
    st.markdown("""
        Ghana is one of West Africa's most dynamic economies,
        a constitutional democracy with significant natural
        resources (gold, oil, cocoa) and a rapidly growing
        fintech sector. Africa is the world's fastest-growing
        fintech market.
""")
    st.caption("Source: World Bank Open Data")

    if gh_data:
        # KPI row
        gdp_g, _ = get_latest_value(
            gh_data["gdp_growth"])
        inf_g, _ = get_latest_value(
            gh_data["inflation"])
        unem_g, _ = get_latest_value(
            gh_data["unemployment"])
        gpc_g, _ = get_latest_value(
            gh_data["gdp_per_capita"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ghana GDP Growth",
                  f"{gdp_g:.1f}%" if gdp_g else "N/A")
        c2.metric("Ghana Inflation",
                  f"{inf_g:.1f}%" if inf_g else "N/A")
        c3.metric("Unemployment",
                  f"{unem_g:.1f}%" if unem_g else "N/A")
        c4.metric("GDP per Capita",
                  f"${gpc_g:,.0f}" if gpc_g else "N/A")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if not gh_data["gdp_growth"].empty:
                gh_gdp = gh_data[
                    "gdp_growth"].reset_index()
                gh_gdp.columns = ["Year", "Growth %"]
                fig = px.bar(
                    gh_gdp,
                    x="Year", y="Growth %",
                    title="Ghana GDP Growth Rate",
                    color="Growth %",
                    color_continuous_scale=[
                        "#D85A30", "#FAEEDA", "#1D9E75"]
                )
                fig.add_hline(
                    y=0, line_dash="dash",
                    line_color="grey")
                fig.update_layout(
                    height=350, showlegend=False)
                st.plotly_chart(
                    fig, use_container_width=True)

        with col2:
            if not gh_data["inflation"].empty:
                gh_inf = gh_data[
                    "inflation"].reset_index()
                gh_inf.columns = ["Year", "Inflation %"]
                fig = px.line(
                    gh_inf,
                    x="Year", y="Inflation %",
                    title="Ghana Inflation Rate",
                    color_discrete_sequence=["#D85A30"]
                )
                fig.add_hline(
                    y=0, line_dash="dash",
                    line_color="grey")
                fig.update_layout(height=350)
                st.plotly_chart(
                    fig, use_container_width=True)

        # FDI and exports
        col3, col4 = st.columns(2)

        with col3:
            if not gh_data["fdi_inflows"].empty:
                fdi_df = gh_data[
                    "fdi_inflows"].reset_index()
                fdi_df.columns = ["Year", "FDI % GDP"]
                fig = px.bar(
                    fdi_df,
                    x="Year", y="FDI % GDP",
                    title="Ghana FDI Inflows (% of GDP)",
                    color_discrete_sequence=["#378ADD"]
                )
                fig.update_layout(height=320)
                st.plotly_chart(
                    fig, use_container_width=True)

        with col4:
            if not gh_data["gdp_per_capita"].empty:
                gpc_df = gh_data[
                    "gdp_per_capita"].reset_index()
                gpc_df.columns = [
                    "Year", "GDP per Capita ($)"]
                fig = px.line(
                    gpc_df,
                    x="Year", y="GDP per Capita ($)",
                    title="Ghana GDP per Capita (USD)",
                    color_discrete_sequence=["#1D9E75"]
                )
                fig.update_layout(height=320)
                fig.update_yaxes(tickprefix="$")
                st.plotly_chart(
                    fig, use_container_width=True)

        # Africa comparison
        st.subheader(
            "African Markets — GDP Growth Comparison")
        if not gdp_data.empty:
            africa = [
                c for c in [
                    "Ghana", "Nigeria",
                    "South Africa", "Kenya"
                ]
                if c in gdp_data.columns
            ]
            if africa:
                fig = px.line(
                    gdp_data[africa],
                    title="GDP Growth — West & East Africa",
                    labels={
                        "value": "Growth %",
                        "index": "Year"
                    }
                )
                fig.add_hline(
                    y=0, line_dash="dash",
                    line_color="grey")
                fig.update_layout(height=400)
                st.plotly_chart(
                    fig, use_container_width=True)
                st.caption(
                    "Ghana's 2011 GDP spike reflects "
                    "the start of oil production. "
                    "The 2022 dip reflects the debt "
                    "crisis and IMF programme."
                )


# ============================================
# SECTION 5 — MARKETS
# ============================================
elif section == "🛢️ Markets":
    st.title("Market Indicators")
    st.caption("Source: Federal Reserve Economic Data (FRED)")

    col1, col2 = st.columns(2)

    with col1:
        if not us_data["oil_wti"].empty:
            oil_df = us_data["oil_wti"].reset_index()
            oil_df.columns = ["Date", "WTI Price"]
            fig = px.line(
                oil_df,
                x="Date", y="WTI Price",
                title="WTI Crude Oil Price ($/barrel)",
                color_discrete_sequence=["#BA7517"]
            )
            for start, end in recessions:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="red", opacity=0.1,
                    layer="below", line_width=0
                )
            fig.update_layout(height=350)
            fig.update_yaxes(tickprefix="$")
            st.plotly_chart(
                fig, use_container_width=True)

    with col2:
        if not us_data["m2"].empty:
            m2_df = us_data["m2"].reset_index()
            m2_df.columns = ["Date", "M2 ($B)"]
            fig = px.area(
                m2_df,
                x="Date", y="M2 ($B)",
                title="US M2 Money Supply ($B)",
                color_discrete_sequence=["#7F77DD"]
            )
            fig.update_layout(height=350)
            st.plotly_chart(
                fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        if not us_data["sp500"].empty:
            sp_df = us_data["sp500"].reset_index()
            sp_df.columns = ["Date", "S&P 500"]
            fig = px.line(
                sp_df,
                x="Date", y="S&P 500",
                title="S&P 500 Index",
                color_discrete_sequence=["#1D9E75"]
            )
            for start, end in recessions:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="red", opacity=0.1,
                    layer="below", line_width=0
                )
            fig.update_layout(height=350)
            st.plotly_chart(
                fig, use_container_width=True)

    with col4:
        if not us_data["vix"].empty:
            vix_df = us_data["vix"].reset_index()
            vix_df.columns = ["Date", "VIX"]
            fig = px.line(
                vix_df,
                x="Date", y="VIX",
                title="VIX Volatility Index (Fear Index)",
                color_discrete_sequence=["#D85A30"]
            )
            fig.add_hline(
                y=30, line_dash="dash",
                line_color="red",
                annotation_text="High fear threshold"
            )
            fig.add_hline(
                y=20, line_dash="dash",
                line_color="orange",
                annotation_text="Elevated fear"
            )
            for start, end in recessions:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="red", opacity=0.1,
                    layer="below", line_width=0
                )
            fig.update_layout(height=350)
            st.plotly_chart(
                fig, use_container_width=True)
            st.caption(
                "VIX above 30 signals significant "
                "market stress. Peaked at 80+ during "
                "COVID March 2020."
            )


# === FOOTER ===
st.divider()
st.markdown("""
Built by **Kofi-Anku** | Financial Data Scientist |
Accra, Ghana |
[GitHub](https://github.com/Kofi-An) |
[Portfolio Risk App](https://kofi-an-portfolio-risk-dashboard.streamlit.app)
""")