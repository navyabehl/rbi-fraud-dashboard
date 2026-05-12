# ============================================================
# fraud_analysis.py — Fraud Risk Analysis Utilities
# ============================================================

import pandas as pd


def get_rag_status(value, green_threshold, amber_threshold, higher_is_worse=True):
    if higher_is_worse:
        if value <= green_threshold:
            return "GREEN", "🟢", "#2ecc71"
        elif value <= amber_threshold:
            return "AMBER", "🟡", "#f39c12"
        else:
            return "RED", "🔴", "#e74c3c"
    else:
        if value >= green_threshold:
            return "GREEN", "🟢", "#2ecc71"
        elif value >= amber_threshold:
            return "AMBER", "🟡", "#f39c12"
        else:
            return "RED", "🔴", "#e74c3c"


def compute_risk_flags(trends_df, instrument_df, benchmarks):
    """Compute RAG flags for key fraud risk indicators."""
    results = []
    latest = trends_df.iloc[-1]
    prev   = trends_df.iloc[-2]

    # 1. Fraud cases YoY growth
    yoy = ((latest["Fraud_Cases"] - prev["Fraud_Cases"]) / prev["Fraud_Cases"]) * 100
    b = benchmarks["fraud_cases_growth"]
    status, emoji, color = get_rag_status(yoy, b["green"], b["amber"])
    results.append({
        "Metric": b["label"], "Value": f"{yoy:.1f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "Note": f"{int(latest['Fraud_Cases']):,} cases reported"
    })

    # 2. Digital fraud share of total cases
    digital = instrument_df[instrument_df["Instrument"] == "Card & Internet"]["Cases_2023"].values[0]
    total   = instrument_df["Cases_2023"].sum()
    share   = (digital / total) * 100
    b = benchmarks["digital_fraud_share"]
    status, emoji, color = get_rag_status(share, b["green"], b["amber"])
    results.append({
        "Metric": b["label"], "Value": f"{share:.1f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "Note": "Card & internet fraud dominates"
    })

    # 3. Detection lag for large frauds
    b = benchmarks["detection_lag_large"]
    status, emoji, color = get_rag_status(3.8, b["green"], b["amber"])
    results.append({
        "Metric": b["label"], "Value": "3.8 years",
        "Status": status, "Emoji": emoji, "Color": color,
        "Note": "Frauds > ₹100 Cr detected after avg 3.8 yrs"
    })

    # 4. Concentration — top instrument share
    top_amount = instrument_df["Amount_Cr_2023"].max()
    total_amount = instrument_df["Amount_Cr_2023"].sum()
    conc = (top_amount / total_amount) * 100
    results.append({
        "Metric": "Top Instrument Fraud Concentration (%)",
        "Value": f"{conc:.1f}%",
        "Status": "AMBER" if conc > 40 else "GREEN",
        "Emoji": "🟡" if conc > 40 else "🟢",
        "Color": "#f39c12" if conc > 40 else "#2ecc71",
        "Note": "Loans & Advances dominates fraud amount"
    })

    return results


def get_bank_type_shares(bank_df):
    """Calculate % share of fraud cases by bank type for latest year."""
    latest = bank_df.iloc[-1]
    total = latest["Public_Sector_Cases"] + latest["Private_Sector_Cases"] + latest["Foreign_Banks_Cases"]
    return {
        "Public Sector": round((latest["Public_Sector_Cases"] / total) * 100, 1),
        "Private Sector": round((latest["Private_Sector_Cases"] / total) * 100, 1),
        "Foreign Banks": round((latest["Foreign_Banks_Cases"] / total) * 100, 1),
    }


def generate_risk_brief(flags, trends_df, selected_year):
    """Generate a regulatory-style fraud risk brief."""
    latest = trends_df[trends_df["Year"] == selected_year].iloc[0]
    red    = [f for f in flags if f["Status"] == "RED"]
    amber  = [f for f in flags if f["Status"] == "AMBER"]

    brief = f"""
================================================================================
    FRAUD RISK MONITORING BRIEF — INDIAN BANKING SECTOR
    Reporting Period: FY {selected_year}
    Prepared by: Navya Behl | ERM Research Dashboard
    Data Source: RBI Annual Report — Trend & Progress of Banking in India
================================================================================

EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
Total fraud cases reported by Scheduled Commercial Banks in FY {selected_year}:
  Cases Reported  : {int(latest['Fraud_Cases']):,}
  Amount Involved : ₹{latest['Fraud_Amount_Cr']:,.0f} Crore
  Avg Fraud Size  : ₹{latest['Avg_Fraud_Size_Cr']:.2f} Crore per case

RISK FLAGS SUMMARY
--------------------------------------------------------------------------------
  🔴 RED   (High Risk) : {len(red)} indicators
  🟡 AMBER (Watch)     : {len(amber)} indicators
  🟢 GREEN (Normal)    : {len(flags) - len(red) - len(amber)} indicators

"""
    if red:
        brief += "HIGH RISK INDICATORS — IMMEDIATE ATTENTION\n"
        brief += "-" * 48 + "\n"
        for f in red:
            brief += f"  🔴 {f['Metric']}: {f['Value']}\n"
            brief += f"     → {f['Note']}\n\n"

    if amber:
        brief += "WATCH LIST — ELEVATED RISK\n"
        brief += "-" * 48 + "\n"
        for f in amber:
            brief += f"  🟡 {f['Metric']}: {f['Value']}\n"
            brief += f"     → {f['Note']}\n\n"

    brief += """KEY OBSERVATIONS
--------------------------------------------------------------------------------
1. DIGITAL FRAUD SURGE: Card & internet fraud cases have risen sharply,
   reflecting growing digital payment volumes and evolving attack vectors.
   Banks must strengthen real-time transaction monitoring controls.

2. DETECTION LAG: Large-value frauds (>₹100 Cr) take an average of 3.8 years
   to detect — a critical operational risk gap requiring enhanced early warning
   systems and continuous credit monitoring frameworks.

3. LOANS & ADVANCES: Remains the highest fraud amount category, particularly
   in infrastructure and manufacturing sectors, indicating credit appraisal
   and post-disbursement monitoring gaps.

4. PRIVATE SECTOR GROWTH: Private sector banks now account for a growing share
   of fraud cases, reflecting their expanding retail and digital footprint.

REGULATORY CONTEXT
--------------------------------------------------------------------------------
RBI's Central Fraud Registry (CFR) mandates reporting of all frauds above
₹1 lakh. The Early Warning Signal (EWS) framework requires banks to flag
stress accounts before NPA classification — a key preventive control.

================================================================================
DISCLAIMER: Academic simulation using publicly available RBI data.
Not affiliated with or endorsed by the Reserve Bank of India.
================================================================================
"""
    return brief
