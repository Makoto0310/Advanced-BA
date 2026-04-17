"""
Configuration file for Advanced Business Analytics - Market War Impact Analysis
"""

import os
from datetime import datetime

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'outputs')
VISUALIZATIONS_DIR = os.path.join(OUTPUT_DIR, 'visualizations')
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')

# Market tickers
TICKERS = [
    "SPY",   # S&P 500
    "^VIX",  # CBOE Volatility Index (Fear index)
    "XLY",   # Consumer Discretionary Sector
    "JETS",  # Airlines Industry ETF
    "XLE",   # Energy Sector
    "XLF",   # Financials Sector
    "ITA",   # Defense/Aerospace Sector
    "GLD",   # Gold Commodity
    "TLT",   # 10-Year Treasury Bonds
    "USO"    # WTI Crude Oil
]

# War-sensitive tickers (most affected by geopolitical events)
AFFECTED_TICKERS = ['USO', 'XLE', 'ITA', '^VIX', 'GLD']

# Data settings
DATA_START_DATE = "2001-01-01"
DATA_END_DATE = "2026-04-17"  # Current date
MARKET_DATA_CSV = os.path.join(DATA_DIR, 'market_data.csv')

# War events with dates
WAR_EVENTS = {
    'iraq_war': {
        'name': 'Iraq War',
        'start_date': '2003-03-20',
        'end_date': '2011-12-31',
        'description': 'Iraq War (2003-2011)'
    },
    'syrian_civil_war': {
        'name': 'Syrian Civil War',
        'start_date': '2011-03-15',
        'end_date': '2026-04-17',
        'description': 'Syrian Civil War (2011-Ongoing)'
    },
    'russia_ukraine_war': {
        'name': 'Russia-Ukraine War',
        'start_date': '2022-02-24',
        'end_date': '2026-04-17',
        'description': 'Russia-Ukraine War (2022-Ongoing)'
    },
    'israel_gaza_war': {
        'name': 'Israel-Gaza War',
        'start_date': '2023-10-07',
        'end_date': '2026-04-17',
        'description': 'Israel-Gaza War (2023-Ongoing)'
    },
    'us_israel_iran': {
        'name': 'US/Israel-Iran Conflict',
        'start_date': '2026-02-06',
        'end_date': '2026-04-17',
        'description': 'US/Israel-Iran Conflict (2026-Ongoing)'
    }
}

# Visualization settings
PLOT_FIGSIZE_DEFAULT = (16, 8)
PLOT_FIGSIZE_MULTI = (16, 10)
PLOT_DPI = 100
PLOT_ALPHA_WAR_REGION = 0.1
PLOT_LINE_WIDTH = 2.0

# Color scheme
COLORS = {
    'war_start': 'red',
    'before_war': 'green',
    'after_war': 'red',
    'default': 'blue',
    'safe_haven': 'gold'
}

# Time windows for analysis (in months)
TIME_WINDOWS = {
    'short': 1,      # 1 month
    'medium': 3,     # 3 months
    'long': 6,       # 6 months
    'extended': 12   # 1 year
}

print(f"✓ Configuration loaded from {__file__}")
