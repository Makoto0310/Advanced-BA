# Time Series Analysis: Market Data & War Impact Study

## Project Overview
This project analyzes how major geopolitical conflicts impact financial markets over a 25-year period (2001-2026).

## Contents

### Main Script
- **`Time series data.py`** - Complete analysis script that:
  - Downloads historical market data for 10 tickers using yfinance
  - Saves data to CSV for further analysis
  - Creates multiple visualizations showing war impacts
  - Generates detailed zoomed views around conflict dates

### Data
- **`market_data.csv`** - Market close prices for all 10 tickers (2001-2026)

### Visualizations
1. **`war_effects_zoomed.png`** - Zoomed analysis of 5 major wars (3 months before → war start → 1 month after)
   - Shows normalized price changes for war-sensitive sectors
   - Displays: USO (Oil), XLE (Energy), ITA (Defense), ^VIX (Fear Index)

2. **`recent_war_detailed.png`** - 4-panel detailed analysis of US/Israel-Iran Conflict (Feb 2026)
   - Individual charts for each war-affected sector
   - Shows before/after price movements

## Market Tickers Analyzed

| Ticker | Description |
|--------|-------------|
| SPY | S&P 500 Index |
| ^VIX | CBOE Volatility Index (Fear Index) |
| XLY | Consumer Discretionary Sector |
| JETS | Airlines Industry ETF |
| XLE | Energy Sector |
| XLF | Financials Sector |
| ITA | Defense/Aerospace Sector |
| GLD | Gold Commodity |
| TLT | 10-Year Treasury Bonds |
| USO | WTI Crude Oil |

## War Events Tracked

| War/Conflict | Start Date | Status |
|-------------|-----------|--------|
| Iraq War | Mar 20, 2003 | Ended Dec 2011 |
| Syrian Civil War | Mar 15, 2011 | Ongoing |
| Russia-Ukraine War | Feb 24, 2022 | Ongoing |
| Israel-Gaza War | Oct 7, 2023 | Ongoing |
| US/Israel-Iran | Feb 6, 2026 | **Ongoing** |

## Key Findings

### Most War-Sensitive Sectors
1. **USO (Crude Oil)** - Most volatile during conflicts due to supply disruptions
2. **XLE (Energy)** - Direct correlation with geopolitical tensions
3. **ITA (Defense)** - Benefits from military spending during wars
4. **^VIX (Fear Index)** - Spikes at conflict onset, indicating market stress

### Iraq War Impact (2003)
- Energy prices surged
- Defense stocks benefited
- General market uncertainty (VIX elevated)

### Recent Conflicts (2022-2026)
- Russia-Ukraine War: Major oil price spike (USO +40%)
- Israel-Gaza War: Moderate energy impact
- US/Israel-Iran Conflict (Feb 2026): Ongoing analysis

## Usage

### Requirements
```bash
pip install yfinance pandas matplotlib numpy
```

### Run the Analysis
```bash
python "Time series data.py"
```

This will:
1. Download market data (automatically cached)
2. Save data to `market_data.csv`
3. Generate 2 PNG visualization files:
   - `war_effects_zoomed.png`
   - `recent_war_detailed.png`

### Data Format
The CSV contains:
- **Index:** Dates (2001-01-01 to 2026-04-17)
- **Columns:** Ticker symbols (SPY, ^VIX, XLY, JETS, XLE, XLF, ITA, GLD, TLT, USO)
- **Values:** Close prices in USD

## Analysis Methodology

1. **Normalization:** Prices indexed to 100 at war start for easy comparison
2. **Time Window:** 3 months before → war date → 1 month after
3. **Visualization:** Multiple zoom levels to see immediate and short-term impacts

## Future Enhancements
- [ ] Add correlation analysis between conflicts and market returns
- [ ] Machine learning predictions for market response
- [ ] Include sentiment analysis from news sources
- [ ] Add more historical conflicts
- [ ] Monthly/quarterly aggregation for clearer trends

## Author
Advanced Business Analytics Project

## Date
Project completed: April 17, 2026

---
**Note:** This analysis is for educational purposes. Market movements have multiple factors beyond geopolitical events.
