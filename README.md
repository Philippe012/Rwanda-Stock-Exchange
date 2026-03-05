# Rwanda Stock Exchange Prediction Framework

> A lightweight Python toolkit for analyzing and forecasting Rwanda Stock Exchange (RSE) market data across equities, bonds, and forex — designed for educational use and integration with fintech platforms like **Pongo**.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output Interpretation](#-output-interpretation)
- [Key Results Summary](#-key-results-summary)
- [Limitations & Disclaimer](#-limitations--disclaimer)
- [Next Steps & Enhancements](#-next-steps--enhancements)
- [License](#-license)

---

## 🎯 Overview

This project analyzes real-time Rwanda Stock Exchange data from a multi-sheet Excel dataset to:
- Parse market indicators, equity prices, bond yields, and forex rates
- Generate simple trend-based predictions for next-day price movements

**Built for**: Developers, analysts, and fintech founders exploring East African capital markets.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 Multi-Market Analysis | Equities, bonds, forex, and macro indicators in one pipeline |
| 🔮 Trend-Based Forecasting | Simple projections using current momentum (safe for limited data) |
| 🎨 Automated Visualizations | 4 PNG charts + 1 summary dashboard saved to `output/` |
| 🌍 Path-Safe Design | Uses `pathlib` for cross-platform compatibility (Windows/Linux/Mac) |

---

## 📁 Project Structure

```
Stocks Prediction/
├── data/
│   └── Rwanda Stock Exchange.xlsx    # Source data (4 sheets)
├── training/
│   └── training.py                   # Main analysis script
├── output/                           # Generated visualizations
│   ├── indicators_comparison.png
│   ├── equity_analysis.png
│   ├── bond_analysis.png
│   ├── forex_analysis.png
│   └── rse_dashboard.png             # Summary dashboard
├── requirements.txt                  # Python dependencies
├── .venv/                            # Virtual environment
└── README.md                         # This file
```

---

## ⚙️ Installation

```bash
# 1. Clone or navigate to project
cd "C:\Users\USER\PycharmProjects\Stocks Prediction"

# 2. Create & activate virtual environment (Windows)
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# Or manually:
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels openpyxl
```

**requirements.txt**:
```txt
pandas>=3.0.0
numpy>=2.4.0
matplotlib>=3.10.0
seaborn>=0.13.0
scikit-learn>=1.8.0
statsmodels>=0.14.0
openpyxl>=3.1.0
```

---

## ▶️ Usage

```powershell
# From project root:
python training\training.py
```

**Expected Output**:
```
📂 Loading data from: .../data/Rwanda Stock Exchange.xlsx
✅ File exists: True
🇷🇼 Rwanda Stock Exchange Prediction Framework
...
✅ Saved: output/rse_dashboard.png
✨ All analyses complete!
```

---

## 📊 Output Interpretation

### 🔹 Market Indicators (Sheet 1)
| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI | 164.81 ↑ | Bullish momentum |
| ALSI | 187.10 ↓ | Minor consolidation |
| EAESI | 100.34 → | Regional stability |
| Market Cap | 4.78T FRW | Large institutional base |
| Equity Turnover | 107M FRW | Low retail participation |

### 🔹 Equity Markets (Sheet 2)
```
✅ Active Stocks (2 of 10):
• Bank of Kigali: 425 FRW ↑1.19% | 250K vol | 106M FRW value
• Bralirwa: 430 FRW → | 2.8K vol | 1.2M FRW value
❌ 8 stocks: Zero volume → liquidity opportunity
```

### 🔹 Bond Market (Sheet 3)
```
🏆 Most Liquid: FXD6/2021/7Yrs Treasury
• Volume: 421.8M shares | Value: 447.8M FRW | ↑0.47%
→ Bonds are 4x more active than equities
```

### 🔹 Exchange Rates (Sheet 4)
```
💱 USD/FRW: 1,458.11 (Avg) | Spread: 10 FRW (0.68%)
→ Tight spread = efficient forex market
→ Regional currencies stable → cross-border potential
```

---

## 📈 Key Results Summary

| Metric | Value | Insight |
|--------|-------|---------|
| **Market Cap** | 4.78T FRW | Mature, institutional-grade market |
| **Equity Liquidity** | 107M FRW/day | Only ~2.2% of cap trades daily |
| **Bond Liquidity** | 475M FRW/day | Fixed income drives activity |
| **Active Stocks** | 2 of 10 | 80% illiquidity = whitespace opportunity |
| **USD/FRW Spread** | 0.68% | Efficient, low-friction forex |
| **Prediction Method** | Trend-based | Safe for limited data; extensible to ML |

---

## ⚠️ Limitations & Disclaimer

> 🔹 **Educational Use Only**: Predictions are simplified trend projections, not financial advice.  
> 🔹 **Data Constraints**: Limited historical points → no complex time-series modeling yet.  
> 🔹 **No Risk Modeling**: Does not account for volatility, macro shocks, or liquidity risk.  
> 🔹 **Static Snapshot**: Reflects single-day data; real trading requires continuous updates.

**For production use**: Integrate historical time-series, ensemble ML models, confidence intervals, and real-time data feeds.

---

## 🚀 Next Steps & Enhancements

### Short-Term (1-2 weeks)
- [ ] Export predictions to CSV/JSON for Django API consumption
- [ ] Add confidence intervals to forecasts
- [ ] Schedule daily runs via Windows Task Scheduler

### Medium-Term (1 month)
- [ ] Integrate with Pongo backend: cache predictions in Redis
- [ ] Build Streamlit dashboard for interactive stakeholder demos
- [ ] Add multilingual labels (Kinyarwanda/Swahili) to visualizations

### Long-Term (Quarterly)
- [ ] Ingest historical RSE data for ARIMA/Prophet modeling
- [ ] Add user behavior signals for personalized recommendations
- [ ] Expand to Kenya (NSE) and Tanzania (DSE) exchanges

---

## 🔗 Integration with Pongo

Since this project supports **Pongo Inc** (real estate + fintech platform):

```python
# Example: Market Confidence Score for property listings
def get_market_badge():
    score = 0
    if equity_turnover > 50_000_000: score += 1
    if bond_volume > 200_000_000: score += 1
    if usd_spread < 15: score += 1
    return "●" * score + "○" * (3-score)  # e.g., "●●○"
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/awesome-forecast`)
3. Commit changes (`git commit -m 'Add ARIMA support'`)
4. Push (`git push origin feature/awesome-forecast`)
5. Open a Pull Request

---
