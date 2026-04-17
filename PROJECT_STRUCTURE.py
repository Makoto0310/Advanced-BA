"""
Project Structure Visualization
Generated: April 17, 2026
"""

PROJECT_TREE = """
Advanced-BA/
├── 📁 config/
│   ├── config.py                    ⚙️  Main configuration module
│   └── __init__.py                  📦 Package init
│
├── 📁 scripts/
│   ├── __init__.py                  📦 Package init
│   ├── main.py                      🚀 Main entry point
│   ├── utils.py                     🛠️  Utility functions
│   ├── market_data_downloader.py    📥 Download market data
│   ├── iraq_war_analysis.py         📊 Iraq War (2003) analysis
│   └── middle_east_conflicts.py     📊 Middle East conflicts analysis
│
├── 📁 data/
│   └── market_data.csv              💾 Market close prices (2001-2026)
│
├── 📁 outputs/
│   ├── 📁 visualizations/
│   │   ├── 📁 iraq-war/
│   │   │   ├── iraq_war_timeline.png
│   │   │   ├── iraq_war_normalized.png
│   │   │   ├── iraq_war_affected_sectors.png
│   │   │   └── iraq_war_weekly_changes.png
│   │   │
│   │   ├── 📁 israel-gaza-war/
│   │   │   ├── israel-gaza_war_timeline.png
│   │   │   ├── israel-gaza_war_normalized.png
│   │   │   ├── israel-gaza_war_affected_sectors.png
│   │   │   └── israel-gaza_war_weekly_changes.png
│   │   │
│   │   └── 📁 us-israel-iran-conflict/
│   │       ├── us-israel-iran_conflict_timeline.png
│   │       ├── us-israel-iran_conflict_normalized.png
│   │       ├── us-israel-iran_conflict_affected_sectors.png
│   │       └── us-israel-iran_conflict_weekly_changes.png
│   │
│   └── 📁 reports/
│       └── [Generated analysis reports]
│
├── 📁 docs/
│   ├── ANALYSIS.md                  📖 Detailed methodology
│   ├── FINDINGS.md                  📖 Key findings summary
│   └── STRUCTURE.md                 📖 Project structure guide
│
├── 📄 README.md                     📖 Main documentation
├── 📄 requirements.txt              📦 Python dependencies
├── 📄 .gitignore                    🚫 Git ignore rules
└── 📄 LICENSE                       ⚖️  MIT License

TOTAL FILES: 25+
TOTAL LINES OF CODE: 2000+
VISUALIZATION FILES: 12+ charts
DATA FILES: 1 CSV (25+ years)
"""

CONFIGURATION_SUMMARY = """
CONFIG/CONFIG.PY DEFINES:
═════════════════════════

📍 Paths:
   - PROJECT_ROOT     = Base directory
   - DATA_DIR         = data/
   - SCRIPTS_DIR      = scripts/
   - VISUALIZATIONS_DIR = outputs/visualizations/
   - REPORTS_DIR      = outputs/reports/

📊 Market Data:
   - TICKERS          = 10 major indicators
   - AFFECTED_TICKERS = 5 war-sensitive sectors
   - TIME_RANGE       = 2001-01-01 to 2026-04-17

🌍 War Events:
   - Iraqi War (2003-2011)
   - Syrian Civil War (2011-2026)
   - Russia-Ukraine War (2022-2026)
   - Israel-Gaza War (2023-2026)
   - US/Israel-Iran Conflict (2026-present)

📈 Visualization Settings:
   - Default figsize  = (16, 8)
   - DPI             = 100
   - Alpha blending  = 0.1 for war regions
   - Line width      = 2.0
"""

SCRIPTS_SUMMARY = """
SCRIPTS OVERVIEW:
═════════════════

main.py
───────
Purpose: Entry point and orchestration
Usage:   python scripts/main.py
Output:  Guide to available analyses

market_data_downloader.py
─────────────────────────
Purpose: Download market data from Yahoo Finance
Usage:   python scripts/market_data_downloader.py
Output:  data/market_data.csv

iraq_war_analysis.py
────────────────────
Purpose: Detailed analysis of Iraq War (Mar 20, 2003)
Usage:   python scripts/iraq_war_analysis.py
Output:  4 PNG files to outputs/visualizations/iraq-war/
Charts:
  1. Multi-scale timeline (1yr, 6mo, 3mo, 1mo)
  2. Normalized price comparison
  3. War-sensitive sectors detail
  4. Weekly percentage changes

middle_east_conflicts.py
────────────────────────
Purpose: Analysis of Israel-Gaza and US/Israel-Iran conflicts
Usage:   python scripts/middle_east_conflicts.py
Output:  8 PNG files
Charts:
  1-4. Israel-Gaza War (Oct 7, 2023)
  5-8. US/Israel-Iran Conflict (Feb 6, 2026)

utils.py
────────
Purpose: Shared utility functions
Functions:
  - load_market_data()
  - save_figure()
  - normalize_to_war_start()
  - calculate_price_changes()
  - print_analysis_header()
  - create_output_dirs()
"""

USAGE_WORKFLOW = """
TYPICAL WORKFLOW:
═════════════════

1️⃣  SETUP
    python -m venv .venv
    .venv\\Scripts\\activate
    pip install -r requirements.txt

2️⃣  DOWNLOAD DATA
    python scripts/market_data_downloader.py
    ✓ Creates: data/market_data.csv

3️⃣  RUN ANALYSES
    python scripts/iraq_war_analysis.py
    ✓ Creates: outputs/visualizations/iraq-war/[4 files]
    
    python scripts/middle_east_conflicts.py
    ✓ Creates: outputs/visualizations/israel-gaza-war/[4 files]
    ✓ Creates: outputs/visualizations/us-israel-iran-conflict/[4 files]

4️⃣  VIEW RESULTS
    📊 outputs/visualizations/
       ├── iraq-war/
       ├── israel-gaza-war/
       └── us-israel-iran-conflict/

5️⃣  ANALYZE DATA
    import pandas as pd
    
    # Load from config
    from config.config import *
    from scripts.utils import load_market_data, create_output_dirs
    
    # Load data
    market_data = load_market_data()
    
    # Run custom analysis...
"""

if __name__ == "__main__":
    print(PROJECT_TREE)
    print("\n" + "="*80 + "\n")
    print(CONFIGURATION_SUMMARY)
    print("\n" + "="*80 + "\n")
    print(SCRIPTS_SUMMARY)
    print("\n" + "="*80 + "\n")
    print(USAGE_WORKFLOW)
