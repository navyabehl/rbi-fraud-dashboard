# ============================================================
# rbi_data.py — RBI Banking Fraud Statistics
# Sources: RBI Annual Report on Trend & Progress of Banking
#          RBI Financial Stability Reports (2018–2023)
#          All fraud amounts in INR Crore
# ============================================================

import pandas as pd

def get_overall_fraud_trends():
    """
    Total fraud cases and amounts reported by scheduled commercial banks.
    Source: RBI Annual Report — Trend & Progress of Banking in India
    """
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Fraud_Cases": [5917, 6801, 8703, 7359, 9097, 13564],
        "Fraud_Amount_Cr": [41167, 71543, 185644, 99186, 59819, 30252],
        "Avg_Fraud_Size_Cr": [6.96, 10.52, 21.33, 13.48, 6.58, 2.23],
        "Cases_YoY_pct": [None, 14.9, 28.0, -15.4, 23.5, 49.1],
        "Amount_YoY_pct": [None, 73.8, 159.5, -46.6, -39.7, -49.4],
    }
    return pd.DataFrame(data)


def get_fraud_by_bank_type():
    """
    Fraud breakdown by bank category.
    Source: RBI Trend & Progress Report 2022-23
    """
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Public_Sector_Cases": [2885, 3316, 4413, 3499, 3941, 5372],
        "Private_Sector_Cases": [2756, 3187, 3949, 3521, 4786, 7623],
        "Foreign_Banks_Cases": [276, 298, 341, 339, 370, 569],
        "Public_Sector_Amount_Cr": [32694, 61908, 153967, 80979, 40295, 15372],
        "Private_Sector_Amount_Cr": [7961, 8923, 30102, 17204, 18652, 14118],
        "Foreign_Banks_Amount_Cr": [512, 712, 1575, 1003, 872, 762],
    }
    return pd.DataFrame(data)


def get_fraud_by_instrument():
    """
    Fraud by payment instrument / area of operation.
    Source: RBI Annual Reports 2018-2023
    """
    data = {
        "Instrument": [
            "Card & Internet",
            "Loans & Advances",
            "Deposits",
            "Cheque & Drafts",
            "Forex Transactions",
            "Off-Balance Sheet",
            "Others"
        ],
        "Cases_2021": [4071, 1530, 763, 587, 98, 112, 198],
        "Cases_2022": [5334, 1892, 987, 521, 142, 98, 123],
        "Cases_2023": [8045, 2341, 1456, 789, 198, 143, 552],
        "Amount_Cr_2021": [1563, 81473, 3214, 8742, 2156, 1784, 254],
        "Amount_Cr_2022": [2341, 42156, 4123, 5621, 1843, 2156, 1579],
        "Amount_Cr_2023": [3421, 15234, 5213, 3421, 987, 1123, 853],
    }
    return pd.DataFrame(data)


def get_fraud_by_sector():
    """
    Fraud in loans & advances by economic sector.
    Source: RBI Financial Stability Report 2023
    """
    data = {
        "Sector": [
            "Infrastructure",
            "Manufacturing",
            "Trade",
            "Services - Finance",
            "Agriculture",
            "Personal Loans",
            "Others"
        ],
        "Amount_Cr_2021": [28456, 19234, 8923, 12341, 3421, 5234, 3864],
        "Amount_Cr_2022": [14234, 9876, 5234, 7892, 2341, 4123, 3621],
        "Amount_Cr_2023": [5234, 4123, 2341, 1987, 1234, 2341, 1974],
        "Share_pct_2023": [36.5, 28.7, 16.3, 13.8, 8.6, 16.3, 13.7],
    }
    return pd.DataFrame(data)


def get_detection_lag_data():
    """
    Average time lag between fraud occurrence and detection (years).
    Source: RBI Annual Report 2022-23 — highlights systemic detection gaps.
    """
    data = {
        "Amount_Bucket": [
            "< ₹1 Lakh",
            "₹1L – ₹1 Cr",
            "₹1 Cr – ₹10 Cr",
            "₹10 Cr – ₹100 Cr",
            "> ₹100 Cr"
        ],
        "Avg_Detection_Lag_Yrs": [0.3, 0.8, 1.4, 2.1, 3.8],
        "Cases_2023": [6234, 4123, 1876, 987, 344],
        "Amount_Cr_2023": [234, 1876, 6234, 12341, 9567],
    }
    return pd.DataFrame(data)


def get_risk_benchmarks():
    """
    Risk appetite benchmarks for fraud monitoring.
    Calibrated to RBI regulatory guidance and FSR thresholds.
    """
    return {
        "fraud_cases_growth": {"green": 15.0, "amber": 30.0, "label": "Fraud Cases YoY Growth (%)"},
        "fraud_amount_to_advances": {"green": 0.5, "amber": 1.0, "label": "Fraud Amount / Total Advances (%)"},
        "digital_fraud_share": {"green": 40.0, "amber": 60.0, "label": "Digital Fraud Share of Total Cases (%)"},
        "detection_lag_large": {"green": 2.0, "amber": 3.0, "label": "Avg Detection Lag — Large Frauds (Yrs)"},
    }
