# 📊 Advanced Business Analytics - Market War Impact Analysis

## Project Overview

This project analyzes how major geopolitical conflicts impact financial markets from 2001-2026. It tracks 10 key market indicators including commodities, equities, and volatility indices across multiple wars and conflicts.

## 🏗️ Project Structure

```
Advanced-BA/
│
├── 📁 config/                    # Configuration files
│   ├── config.py                # Main configuration (tickers, paths, dates)
│   └── __init__.py
│
├── 📁 scripts/                   # Analysis scripts
│   ├── __init__.py
│   ├── main.py                  # Main entry point
│   ├── utils.py                 # Utility functions
│   ├── market_data_downloader.py # Download market data
│   ├── iraq_war_analysis.py     # Iraq War analysis (2003)
│   └── middle_east_conflicts.py # Israel-Gaza & US/Israel-Iran conflicts
│
├── 📁 data/                      # Market data
│   └── market_data.csv          # Historical close prices (2001-2026)
│
├── 📁 outputs/                   # Analysis outputs
│   ├── visualizations/          # Charts and plots
│   │   ├── iraq_war/           # Iraq War visualizations
│   │   ├── israel_gaza_war/    # Israel-Gaza War visualizations
│   │   └── us_israel_iran_conflict/  # US/Israel-Iran visualizations
│   └── reports/                # Generated reports
│
├── 📁 docs/                      # Documentation
│   ├── ANALYSIS.md              # Detailed analysis methodology
│   └── FINDINGS.md              # Key findings summary
│
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore               # Git ignore rules
└── 📄 LICENSE                  # Project license
```

## 📊 Market Tickers Analyzed

| Symbol | Description | Category |
|--------|-------------|----------|
| **SPY** | S&P 500 Index | Equities |
| **^VIX** | CBOE Volatility Index | Fear Gauge |
| **XLY** | Consumer Discretionary | Sector |
| **JETS** | Airlines ETF | Sector |
| **XLE** | Energy Sector | **War-Sensitive** |
| **XLF** | Financials Sector | Sector |
| **ITA** | Defense/Aerospace | **War-Sensitive** |
| **GLD** | Gold Commodity | **Safe-Haven** |
| **TLT** | 10-Year Treasuries | Bonds |
| **USO** | WTI Crude Oil | **War-Sensitive** |

## 🌍 Wars & Conflicts Included

| War | Period | Status | Analysis |
|-----|--------|--------|----------|
| **Iraq War** | Mar 2003 - Dec 2011 | Ended | ✅ Detailed |
| **Syria Civil War** | Mar 2011 - Present | Ongoing | ✅ Tracked |
| **Russia-Ukraine War** | Feb 2022 - Present | Ongoing | ✅ Tracked |
| **Israel-Gaza War** | Oct 2023 - Present | Ongoing | ✅ Detailed |
| **US/Israel-Iran Conflict** | Feb 2026 - Present | **Ongoing** | ✅ Detailed |

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/Makoto0310/Advanced-BA.git
cd Advanced-BA

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis
```bash
# Download market data
python scripts/market_data_downloader.py

# Run Iraq War analysis
python scripts/iraq_war_analysis.py

# Run Middle East conflicts analysis
python scripts/israel_iran_analysis.py

# Run War Resilience Analysis ⭐ NEW
python scripts/war_resilience_analysis.py

# Run Conflict Resilience Forecasting 🤖 NEW
python scripts/conflict_resilience_forecast.py

# View all available scripts
python scripts/main.py
```

## 📈 Key Features

✅ Multi-scale zoom analysis (1yr, 6mo, 3mo, 1mo)
✅ Normalized price comparison (indexed to war start)
✅ War-sensitive sector deep dive
✅ Daily percentage change tracking
✅ Statistical quantification of market impact
✅ **War Resilience Analysis** ⭐ NEW
✅ Safe haven effectiveness measurement
✅ Sector resilience ranking
✅ Recovery speed metrics
✅ Volatility-based stability analysis
✅ **Conflict Resilience Forecasting** 🤖 NEW
✅ Machine learning predictions for future conflicts
✅ Multi-model ensemble forecasting (Random Forest, Gradient Boosting)
✅ Feature importance analysis
✅ Scenario-based future conflict predictions
✅ Organized output structure
✅ Configurable for custom analysis

## 🔍 Key Findings

**War Resilience Rankings** (30-day recovery):
- **USO (Oil)**: Most resilient (+19.50% avg)
- **XLE (Energy)**: Strong recovery (+3.77%)
- **ITA (Defense)**: Benefits from spending (+3.37%)
- **XLF (Financials)**: Moderate resilience (+2.41%)
- **SPY (S&P 500)**: Steady recovery (+2.09%)
- **GLD (Gold)**: Mixed performance (-1.53%)
- **^VIX (Fear Index)**: Most impacted (-8.26%)

**Individual War Performance**:
- **Iraq War (2003)**: SPY recovered +6.2% in 30 days
- **Israel-Gaza War (2023)**: ITA surged +11.2%, GLD +8.2%
- **US/Israel-Iran (2026)**: USO exploded +43.6%, XLE +12.7%

**Safe Haven Effectiveness**:
- Gold and Treasury Bonds show mixed protection during crises
- Recent conflicts demonstrate better market resilience than historical wars
- Energy sectors show volatile but often strong recovery patterns

**Forecasting Insights** 🤖:
- **Red Sea Crisis 2027**: Moderate positive resilience (+0.9% across sectors)
- **South China Sea 2028**: Minimal impact (+0.1% recovery)
- **Eastern Europe 2029**: Significant negative impact (-5.0% across sectors)
- Model accuracy: Random Forest achieves 4.93% mean absolute error
- **config/config.py** - Centralized configuration
- **scripts/utils.py** - Reusable utility functions
- **outputs/visualizations/** - Analysis charts organized by war

## � Conflict Resilience Forecasting

**Machine Learning Models**: Random Forest, Gradient Boosting, Linear Regression
**Training Data**: Historical conflict responses (2003-2026)
**Features**: Market conditions, conflict type, timing, volatility, geopolitical factors
**Predictions**: 30-day recovery percentages for key sectors
**Accuracy**: Best model achieves ~5% mean absolute error

### Forecast Scenarios
- **Red Sea Crisis 2027**: Oil-related Middle East conflict
- **South China Sea 2028**: Asia-Pacific territorial dispute  
- **Eastern Europe 2029**: Major European security crisis

### Key Predictive Factors
- Pre-conflict market volatility
- Conflict location (Middle East vs. other regions)
- Oil involvement
- Market trend leading into conflict
- VIX fear index levels

---

**Status**: Active Development  
**Last Updated**: April 17, 2026  
**Data Coverage**: 2001-2026