# 🏦 RBI Banking Fraud Risk Dashboard

An interactive fraud risk monitoring dashboard analyzing patterns, trends, and risk concentrations across Indian scheduled commercial banks using the Reserve Bank of India's publicly disclosed fraud statistics.

> **Built by:** Navya Behl | M.Sc. Economics, Dr. B.R. Ambedkar School of Economics University  
> **Purpose:** Academic portfolio project demonstrating fraud risk analysis and regulatory monitoring frameworks

---
## 🚀 Live Demo
**[▶ Try the app here](https://navyabehl-rbi-fraud-dashboard.streamlit.app)**

## 🎯 Project Motivation

Fraud risk is one of the four core risk domains monitored by Enterprise Risk Management (ERM) functions at banks. The RBI mandates that all scheduled commercial banks report fraud data to the **Central Fraud Registry (CFR)** — making this one of the richest public datasets for banking risk analysis.

This dashboard:
- Tracks fraud trends across the Indian banking sector (2018–2023)
- Identifies high-risk segments by bank type, instrument, and fraud size
- Analyses the **detection lag problem** — a critical operational risk gap
- Generates regulatory-style fraud risk briefs with RAG status flags

---

## 📊 Analysis Modules

| Module | What It Shows |
|---|---|
| **Overall Trends** | Total cases, amounts, avg fraud size YoY — with RAG risk flags |
| **By Bank Type** | Public vs Private vs Foreign bank fraud breakdown |
| **By Instrument** | Card & internet, loans, deposits, cheques, forex — cases and amounts |
| **Detection Lag** | Time between fraud occurrence and detection by fraud size bucket |
| **Risk Brief** | Auto-generated regulatory-style monitoring brief |

---

## 🔍 Key Findings

1. **Digital fraud surge** — Card & internet fraud cases nearly doubled between FY2021–2023, now the largest category by case count
2. **Detection lag crisis** — Large frauds (>₹100 Cr) take an average of **3.8 years** to detect, far exceeding the 2-year amber threshold
3. **Dual fraud profiles** — High-volume small-ticket digital fraud vs. low-volume large corporate loan fraud require entirely different control frameworks
4. **Declining average size** — Average fraud size fell from ₹21.3 Cr (2020) to ₹2.2 Cr (2023), reflecting the shift from corporate to retail fraud

---

## 🛠️ Tech Stack

| Tool | Use |
|---|---|
| Python | Core analysis and data pipeline |
| Streamlit | Interactive dashboard UI |
| Plotly | Charts, bubble plots, pie charts, trend lines |
| Pandas | Data wrangling and metric computation |

---

## 📁 Project Structure

```
rbi-fraud-dashboard/
├── app.py                # Main Streamlit dashboard
├── rbi_data.py           # RBI public fraud data + benchmarks
├── fraud_analysis.py     # RAG engine + risk brief generator
└── requirements.txt
```

---

## 🚀 How to Run

```bash
git clone https://github.com/navyabehl/rbi-fraud-dashboard.git
cd rbi-fraud-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Data Sources

- **RBI Annual Report — Trend & Progress of Banking in India** (2018–2023)
- **RBI Financial Stability Reports** — fraud concentration and detection lag data
- **RBI Central Fraud Registry (CFR)** — instrument and sector-wise fraud disclosures

---

## 📌 ERM Concepts Demonstrated

- **Fraud Risk Monitoring** — trend analysis, concentration risk, YoY growth flags
- **Operational Risk** — detection lag as a systemic control failure indicator
- **Regulatory Compliance** — alignment with RBI CFR and EWS frameworks
- **RAG Status Framework** — green/amber/red thresholds for risk escalation
- **Risk Segmentation** — separate analysis by bank type, instrument, and fraud size

---

## ⚠️ Disclaimer

Academic simulation using publicly available RBI data. Not affiliated with or endorsed by the Reserve Bank of India.
