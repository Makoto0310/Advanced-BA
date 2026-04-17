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
python scripts/middle_east_conflicts.py
```

## 📈 Key Features

✅ Multi-scale zoom analysis (1yr, 6mo, 3mo, 1mo)
✅ Normalized price comparison (indexed to war start)
✅ War-sensitive sector deep dive
✅ Daily percentage change tracking
✅ Statistical quantification of market impact
✅ Organized output structure
✅ Configurable for custom analysis

## 🔍 Key Findings

**Iraq War (2003)**: Markets recovered quickly (+6.17% in 30 days)
**Israel-Gaza War (2023)**: Resilient response (+4.95% in 30 days)  
**US/Israel-Iran (2026)**: Bearish trend (-4.84%), Oil surge +43.60% ⚠️

## 📚 Documentation

- **config/config.py** - Centralized configuration
- **scripts/utils.py** - Reusable utility functions
- **outputs/visualizations/** - Analysis charts organized by war

## 🤝 Contributing

Fork → Create Feature Branch → Commit → Push → Pull Request

## 📄 License

MIT License - See LICENSE file

---

**Status**: Active Development  
**Last Updated**: April 17, 2026  
**Data Coverage**: 2001-2026