# ============================================================
# app.py — RBI Banking Fraud Risk Dashboard
# Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from rbi_data import (
    get_overall_fraud_trends, get_fraud_by_bank_type,
    get_fraud_by_instrument, get_fraud_by_sector,
    get_detection_lag_data, get_risk_benchmarks
)
from fraud_analysis import (
    compute_risk_flags, get_bank_type_shares, generate_risk_brief
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="RBI Banking Fraud Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .stMetric { border-radius: 8px; padding: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    [data-testid="stMetricValue"] { color: inherit !important; }
    [data-testid="stMetricLabel"] { color: inherit !important; }
    .rag-card {
        border-radius: 10px; padding: 14px 18px; margin: 6px 0;
        display: flex; justify-content: space-between; align-items: center;
        font-size: 0.9rem; box-shadow: 0 1px 4px rgba(0,0,0,0.07); gap: 12px;
    }
    .rag-green { background: rgba(46,204,113,0.15); border-left: 5px solid #2ecc71; }
    .rag-amber { background: rgba(243,156,18,0.15);  border-left: 5px solid #f39c12; }
    .rag-red   { background: rgba(231,76,60,0.15);   border-left: 5px solid #e74c3c; }
    .section-header { font-size: 1.05rem; font-weight: 700; margin: 16px 0 8px 0; }
    .banner {
        border-radius: 12px; padding: 16px 24px; text-align: center;
        font-size: 1.2rem; font-weight: 700; margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .insight-box {
        border-radius: 8px; padding: 12px 16px; margin: 8px 0;
        background: rgba(52,152,219,0.1); border-left: 4px solid #3498db;
        font-size: 0.88rem;
    }
    .disclaimer { font-size: 0.75rem; color: #888; margin-top: 30px;
        border-top: 1px solid #ddd; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Shared chart layout ───────────────────────────────────────
CHART = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=40, b=20)
)

# ── Load data ────────────────────────────────────────────────
trends_df    = get_overall_fraud_trends()
bank_df      = get_fraud_by_bank_type()
instrument_df= get_fraud_by_instrument()
sector_df    = get_fraud_by_sector()
lag_df       = get_detection_lag_data()
benchmarks   = get_risk_benchmarks()

YEARS = trends_df["Year"].tolist()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image("https://logo.clearbit.com/rbi.org.in", width=100)
    st.markdown("## Fraud Risk Dashboard")
    st.markdown("**Indian Banking Sector**  \nFraud Pattern Analysis")
    st.divider()

    selected_year = st.selectbox("📅 Reporting Year", YEARS[1:], index=len(YEARS)-2)
    st.divider()

    st.markdown("**Risk Flags**")
    st.markdown("""
    | Status | Meaning |
    |--------|---------|
    | 🟢 GREEN | Within normal range |
    | 🟡 AMBER | Elevated — monitor |
    | 🔴 RED   | High risk — escalate |
    """)
    st.divider()
    st.markdown("**Data Sources**")
    st.caption("RBI Trend & Progress Report  \nRBI Financial Stability Report  \nRBI Central Fraud Registry")
    st.divider()
    st.caption("Academic simulation using public RBI data.")

# ── Filter to year ───────────────────────────────────────────
yr_idx   = YEARS.index(selected_year)
t_df     = trends_df.iloc[:yr_idx + 1].reset_index(drop=True)
b_df     = bank_df.iloc[:yr_idx + 1].reset_index(drop=True)
latest   = t_df.iloc[-1]
prev     = t_df.iloc[-2]

flags    = compute_risk_flags(t_df, instrument_df, benchmarks)
red_ct   = sum(1 for f in flags if f["Status"] == "RED")
amb_ct   = sum(1 for f in flags if f["Status"] == "AMBER")
grn_ct   = len(flags) - red_ct - amb_ct

overall  = "RED" if red_ct > 0 else ("AMBER" if amb_ct > 0 else "GREEN")
o_emoji  = {"RED": "🔴", "AMBER": "🟡", "GREEN": "🟢"}[overall]
o_color  = {"RED": "#e74c3c", "AMBER": "#f39c12", "GREEN": "#2ecc71"}[overall]
o_bg     = {"RED": "rgba(231,76,60,0.15)", "AMBER": "rgba(243,156,18,0.15)", "GREEN": "rgba(46,204,113,0.15)"}[overall]

# ── Header ───────────────────────────────────────────────────
st.markdown(f"## 🏦 RBI Banking Fraud Risk Dashboard — FY {selected_year}")
st.markdown("*Fraud pattern analysis across Indian scheduled commercial banks using RBI public disclosures*")

# ── Banner ───────────────────────────────────────────────────
st.markdown(f"""
<div class="banner" style="border: 2px solid {o_color}; background:{o_bg};">
    {o_emoji} Overall Fraud Risk: <span style="color:{o_color}">{overall}</span>
    &nbsp;|&nbsp; {grn_ct} GREEN &nbsp; {amb_ct} AMBER &nbsp; {red_ct} RED
    &nbsp;|&nbsp; {int(latest['Fraud_Cases']):,} Cases &nbsp;|&nbsp; ₹{latest['Fraud_Amount_Cr']:,.0f} Cr
</div>
""", unsafe_allow_html=True)

# ── KPI row ──────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
cases_chg = int(latest["Fraud_Cases"] - prev["Fraud_Cases"])
amt_chg   = latest["Fraud_Amount_Cr"] - prev["Fraud_Amount_Cr"]
c1.metric("Total Fraud Cases", f"{int(latest['Fraud_Cases']):,}", f"{cases_chg:+,}")
c2.metric("Amount Involved", f"₹{latest['Fraud_Amount_Cr']/1000:.1f}K Cr", f"₹{amt_chg/1000:+.1f}K Cr")
c3.metric("Avg Fraud Size", f"₹{latest['Avg_Fraud_Size_Cr']:.2f} Cr",
          f"₹{latest['Avg_Fraud_Size_Cr'] - prev['Avg_Fraud_Size_Cr']:+.2f} Cr")
c4.metric("Cases YoY Growth", f"{latest['Cases_YoY_pct']:.1f}%")

st.divider()

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trends", "🏛️ Bank Type", "💳 By Instrument", "⏱️ Detection Lag", "📋 Risk Brief"
])

def render_rag_cards(flags):
    for f in flags:
        css = {"GREEN": "rag-green", "AMBER": "rag-amber", "RED": "rag-red"}[f["Status"]]
        st.markdown(f"""
        <div class="rag-card {css}">
            <span><strong>{f['Emoji']} {f['Metric']}</strong></span>
            <span><strong>{f['Value']}</strong></span>
            <span style="font-size:0.82rem">{f['Note']}</span>
            <span><strong>{f['Status']}</strong></span>
        </div>""", unsafe_allow_html=True)

# ── Tab 1: Overall Trends ────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Fraud Risk Indicators</div>', unsafe_allow_html=True)
    render_rag_cards(flags)

    st.markdown('<div class="section-header">Fraud Trends — Cases & Amount</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=t_df["Year"], y=t_df["Fraud_Cases"],
            marker_color="#3498db", name="Fraud Cases"))
        fig.update_layout(title="Total Fraud Cases Reported", height=300,
            yaxis_title="No. of Cases", **CHART)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=t_df["Year"], y=t_df["Fraud_Amount_Cr"],
            marker_color="#e74c3c", name="Fraud Amount"))
        fig.update_layout(title="Total Fraud Amount (₹ Crore)", height=300,
            yaxis_title="₹ Crore", **CHART)
        st.plotly_chart(fig, use_container_width=True)

    # Avg fraud size trend
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t_df["Year"], y=t_df["Avg_Fraud_Size_Cr"],
        mode="lines+markers+text",
        text=[f"₹{v:.1f}Cr" for v in t_df["Avg_Fraud_Size_Cr"]],
        textposition="top center",
        line=dict(color="#9b59b6", width=2.5), fill="tozeroy",
        fillcolor="rgba(155,89,182,0.1)"))
    fig3.update_layout(title="Average Fraud Size per Case (₹ Crore)",
        height=240, yaxis_title="₹ Crore", **CHART)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key Insight:</strong> While fraud <em>cases</em> have surged post-2021,
    average fraud <em>size</em> has declined sharply — indicating a shift from large
    concentrated frauds (infrastructure loans) to high-volume small-ticket digital fraud.
    This requires different monitoring strategies for each segment.
    </div>""", unsafe_allow_html=True)

# ── Tab 2: Bank Type ─────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Fraud by Bank Category</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    shares = get_bank_type_shares(b_df)

    with col_l:
        fig = go.Figure(data=[go.Pie(
            labels=list(shares.keys()),
            values=list(shares.values()),
            hole=0.45,
            marker_colors=["#3498db", "#e74c3c", "#2ecc71"]
        )])
        fig.update_layout(title=f"Fraud Case Share by Bank Type — FY {selected_year}",
            height=320, **CHART)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Bar(name="Public Sector", x=b_df["Year"],
            y=b_df["Public_Sector_Cases"], marker_color="#3498db"))
        fig.add_trace(go.Bar(name="Private Sector", x=b_df["Year"],
            y=b_df["Private_Sector_Cases"], marker_color="#e74c3c"))
        fig.add_trace(go.Bar(name="Foreign Banks", x=b_df["Year"],
            y=b_df["Foreign_Banks_Cases"], marker_color="#2ecc71"))
        fig.update_layout(title="Cases by Bank Type Over Time", barmode="group",
            height=320, legend=dict(orientation="h", y=-0.2), **CHART)
        st.plotly_chart(fig, use_container_width=True)

    # Amount comparison
    fig2 = make_subplots(rows=1, cols=1)
    fig2.add_trace(go.Scatter(x=b_df["Year"], y=b_df["Public_Sector_Amount_Cr"],
        mode="lines+markers", name="Public Sector", line=dict(color="#3498db", width=2)))
    fig2.add_trace(go.Scatter(x=b_df["Year"], y=b_df["Private_Sector_Amount_Cr"],
        mode="lines+markers", name="Private Sector", line=dict(color="#e74c3c", width=2)))
    fig2.add_trace(go.Scatter(x=b_df["Year"], y=b_df["Foreign_Banks_Amount_Cr"],
        mode="lines+markers", name="Foreign Banks", line=dict(color="#2ecc71", width=2)))
    fig2.update_layout(title="Fraud Amount by Bank Type (₹ Crore)",
        height=280, yaxis_title="₹ Crore",
        legend=dict(orientation="h", y=-0.2), **CHART)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key Insight:</strong> Public sector banks historically reported higher fraud
    amounts due to large corporate loan frauds. Private sector banks are now catching up
    in case volume, driven by retail and digital fraud growth.
    </div>""", unsafe_allow_html=True)

# ── Tab 3: By Instrument ─────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Fraud by Payment Instrument / Area</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        fig = go.Figure(go.Bar(
            x=instrument_df["Cases_2023"],
            y=instrument_df["Instrument"],
            orientation="h",
            marker_color=["#e74c3c", "#3498db", "#f39c12",
                          "#9b59b6", "#2ecc71", "#1abc9c", "#95a5a6"]
        ))
        fig.update_layout(title="Fraud Cases by Instrument — FY 2023",
            height=340, xaxis_title="No. of Cases", **CHART)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig = go.Figure(go.Bar(
            x=instrument_df["Amount_Cr_2023"],
            y=instrument_df["Instrument"],
            orientation="h",
            marker_color=["#e74c3c", "#3498db", "#f39c12",
                          "#9b59b6", "#2ecc71", "#1abc9c", "#95a5a6"]
        ))
        fig.update_layout(title="Fraud Amount by Instrument — FY 2023 (₹ Crore)",
            height=340, xaxis_title="₹ Crore", **CHART)
        st.plotly_chart(fig, use_container_width=True)

    # YoY comparison
    fig2 = make_subplots(rows=1, cols=1)
    fig2.add_trace(go.Bar(name="FY 2021", x=instrument_df["Instrument"],
        y=instrument_df["Cases_2021"], marker_color="rgba(52,152,219,0.6)"))
    fig2.add_trace(go.Bar(name="FY 2022", x=instrument_df["Instrument"],
        y=instrument_df["Cases_2022"], marker_color="rgba(243,156,18,0.8)"))
    fig2.add_trace(go.Bar(name="FY 2023", x=instrument_df["Instrument"],
        y=instrument_df["Cases_2023"], marker_color="#e74c3c"))
    fig2.update_layout(title="Fraud Cases by Instrument — 3 Year Comparison",
        barmode="group", height=320,
        legend=dict(orientation="h", y=-0.2), **CHART)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key Insight:</strong> Card & Internet fraud cases have grown nearly 2x in
    3 years — the fastest growing category. However, Loans & Advances still dominates
    by amount, pointing to two distinct fraud profiles requiring separate control frameworks.
    </div>""", unsafe_allow_html=True)

# ── Tab 4: Detection Lag ─────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Fraud Detection Lag Analysis</div>', unsafe_allow_html=True)
    st.markdown("*Time between fraud occurrence and detection — a critical operational risk gap*")

    col_l, col_r = st.columns(2)
    with col_l:
        colors = ["#2ecc71", "#2ecc71", "#f39c12", "#e74c3c", "#e74c3c"]
        fig = go.Figure(go.Bar(
            x=lag_df["Avg_Detection_Lag_Yrs"],
            y=lag_df["Amount_Bucket"],
            orientation="h",
            marker_color=colors,
            text=[f"{v} yrs" for v in lag_df["Avg_Detection_Lag_Yrs"]],
            textposition="outside"
        ))
        fig.update_layout(title="Avg Detection Lag by Fraud Size",
            height=340, xaxis_title="Years", **CHART)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=lag_df["Amount_Bucket"],
            y=lag_df["Amount_Cr_2023"],
            marker_color=colors,
            name="Fraud Amount"
        ))
        fig2.update_layout(title="Fraud Amount by Size Bucket — FY 2023 (₹ Crore)",
            height=340, yaxis_title="₹ Crore", **CHART)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key Insight:</strong> Large frauds (>₹100 Cr) take an average of <strong>3.8 years</strong>
    to detect — well above the 2-year regulatory amber threshold. This systemic detection gap
    means losses compound significantly before intervention. RBI's Early Warning Signal (EWS)
    framework and Central Fraud Registry (CFR) aim to address this, but implementation gaps remain.
    </div>""", unsafe_allow_html=True)

    # Bubble chart — cases vs amount vs lag
    fig3 = go.Figure(go.Scatter(
        x=lag_df["Avg_Detection_Lag_Yrs"],
        y=lag_df["Amount_Cr_2023"],
        mode="markers+text",
        text=lag_df["Amount_Bucket"],
        textposition="top center",
        marker=dict(
            size=lag_df["Cases_2023"].apply(lambda x: x/100),
            color=colors,
            opacity=0.7,
            line=dict(width=1, color="white")
        )
    ))
    fig3.update_layout(
        title="Risk Matrix: Detection Lag vs Fraud Amount (bubble = case volume)",
        xaxis_title="Avg Detection Lag (Years)",
        yaxis_title="Total Fraud Amount (₹ Crore)",
        height=350, **CHART
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Tab 5: Risk Brief ────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">📋 Fraud Risk Monitoring Brief</div>', unsafe_allow_html=True)
    st.markdown(f"*Regulatory-style risk brief for FY {selected_year}*")

    brief = generate_risk_brief(flags, trends_df, selected_year)
    st.download_button(
        label="⬇️ Download Risk Brief (.txt)",
        data=brief,
        file_name=f"RBI_Fraud_Risk_Brief_{selected_year}.txt",
        mime="text/plain"
    )
    st.code(brief, language=None)

# ── Disclaimer ───────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Disclaimer:</strong> Academic simulation using publicly available RBI data
(Trend & Progress of Banking in India, Financial Stability Reports).
Not affiliated with or endorsed by the Reserve Bank of India.
Built by Navya Behl for educational and portfolio purposes.
</div>
""", unsafe_allow_html=True)
