"""
Utility functions for market analysis
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add config to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
from config import *

def load_market_data(csv_path=MARKET_DATA_CSV):
    """Load market data from CSV file"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Market data file not found: {csv_path}")
    
    print(f"📊 Loading market data from: {csv_path}")
    market_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    print(f"✓ Loaded data: {len(market_data)} rows × {len(market_data.columns)} columns")
    return market_data

def save_figure(fig, filename, output_dir=VISUALIZATIONS_DIR):
    """Save figure to output directory"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=PLOT_DPI, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close(fig)
    return filepath

def normalize_to_war_start(data, war_date):
    """Normalize prices to 100 at war start date"""
    closest_idx = np.argmin(np.abs(data.index.values.astype('datetime64[D]') - np.datetime64(war_date.date())))
    baseline = data.iloc[closest_idx]
    normalized = (data / baseline * 100)
    return normalized

def calculate_price_changes(data, war_date, days_before=5, days_after=30):
    """Calculate percentage changes from war start date"""
    war_idx = np.argmin(np.abs(data.index.values.astype('datetime64[D]') - np.datetime64(war_date.date())))
    
    before_idx = max(0, war_idx - days_before)
    after_idx = min(len(data) - 1, war_idx + days_after)
    
    price_war = data.iloc[war_idx]
    price_before = data.iloc[before_idx]
    price_after = data.iloc[after_idx]
    
    pct_change_before = ((price_war - price_before) / price_before * 100) if price_before != 0 else 0
    pct_change_after = ((price_after - price_war) / price_war * 100) if price_war != 0 else 0
    
    return {
        'price_war': price_war,
        'price_after': price_after,
        'pct_change_before': pct_change_before,
        'pct_change_after': pct_change_after
    }

def print_analysis_header(title):
    """Print formatted analysis header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def create_output_dirs():
    """Create all required output directories"""
    for key, event in WAR_EVENTS.items():
        war_dir = os.path.join(VISUALIZATIONS_DIR, key.replace('_', '-'))
        os.makedirs(war_dir, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    print("✓ Output directories created")
