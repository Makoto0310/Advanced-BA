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

# ===== WAR RESILIENCE ANALYSIS FUNCTIONS =====

def calculate_resilience_metrics(market_data, war_start, ticker, recovery_periods=[5, 10, 30, 60, 90]):
    """
    Calculate resilience metrics for a ticker during war period.
    Resilience measured by recovery speed and stability.

    Parameters:
    - market_data: DataFrame with market data
    - war_start: datetime of war start
    - ticker: ticker symbol to analyze
    - recovery_periods: list of days to measure recovery

    Returns:
    - dict with resilience scores for each period
    """
    if ticker not in market_data.columns:
        return {}

    # Find war start index
    war_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(war_start.date())))

    resilience_scores = {}

    for days in recovery_periods:
        end_idx = min(war_idx + days, len(market_data) - 1)

        if end_idx > war_idx:
            start_price = market_data[ticker].iloc[war_idx]
            end_price = market_data[ticker].iloc[end_idx]

            if not (pd.isna(start_price) or pd.isna(end_price) or start_price == 0):
                pct_change = (end_price - start_price) / start_price * 100
                resilience_scores[f'{days}d_recovery'] = pct_change

    return resilience_scores

def calculate_volatility_resilience(market_data, war_start, window_days=30):
    """
    Calculate volatility-based resilience metrics.
    Compares volatility before vs during/after war.

    Parameters:
    - market_data: DataFrame with market data
    - war_start: datetime of war start
    - window_days: days to analyze before and after war

    Returns:
    - dict with volatility resilience scores
    """
    war_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(war_start.date())))

    # Pre-war period
    pre_start = max(0, war_idx - window_days)
    pre_war_data = market_data.iloc[pre_start:war_idx]

    # Post-war period
    post_end = min(len(market_data), war_idx + window_days)
    post_war_data = market_data.iloc[war_idx:post_end]

    resilience_metrics = {}

    for ticker in ['SPY', '^VIX', 'XLE', 'USO', 'GLD', 'ITA']:
        if ticker in market_data.columns and not pre_war_data[ticker].isna().all() and not post_war_data[ticker].isna().all():
            # Calculate daily returns
            pre_returns = pre_war_data[ticker].pct_change().dropna()
            post_returns = post_war_data[ticker].pct_change().dropna()

            if len(pre_returns) > 0 and len(post_returns) > 0:
                pre_vol = pre_returns.std() * np.sqrt(252)  # Annualized volatility
                post_vol = post_returns.std() * np.sqrt(252)

                # Resilience score: lower post-war volatility = more resilient
                if pre_vol > 0:
                    vol_ratio = post_vol / pre_vol
                    resilience_score = 1 / vol_ratio if vol_ratio > 0 else 0
                    resilience_metrics[f'{ticker}_vol_resilience'] = resilience_score

    return resilience_metrics

def rank_sector_resilience(market_data, war_events):
    """
    Rank sectors by average resilience across multiple wars.

    Parameters:
    - market_data: DataFrame with market data
    - war_events: dict of war names to datetime objects

    Returns:
    - list of tuples (ticker, avg_resilience_score) sorted by resilience
    """
    resilience_scores = {}

    for war_name, war_date in war_events.items():
        war_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(war_date.date())))

        # 30-day recovery period
        end_idx = min(war_idx + 30, len(market_data) - 1)

        for ticker in ['SPY', 'XLE', 'XLF', 'ITA', 'USO', 'GLD', '^VIX']:
            if ticker in market_data.columns:
                start_price = market_data[ticker].iloc[war_idx]
                end_price = market_data[ticker].iloc[end_idx]

                if not pd.isna(start_price) and not pd.isna(end_price) and start_price != 0:
                    recovery = (end_price - start_price) / start_price * 100

                    if ticker not in resilience_scores:
                        resilience_scores[ticker] = []
                    resilience_scores[ticker].append(recovery)

    # Calculate average resilience across wars
    avg_resilience = {}
    for ticker, scores in resilience_scores.items():
        if len(scores) > 0:
            avg_resilience[ticker] = np.mean(scores)

    # Sort by resilience (highest first)
    return sorted(avg_resilience.items(), key=lambda x: x[1], reverse=True)

def analyze_safe_haven_effectiveness(market_data, war_events, safe_havens=None):
    """
    Measure how well traditional safe havens perform during wars.

    Parameters:
    - market_data: DataFrame with market data
    - war_events: dict of war names to datetime objects
    - safe_havens: dict of ticker to name mappings

    Returns:
    - dict with safe haven effectiveness scores
    """
    if safe_havens is None:
        safe_havens = {
            'GLD': 'Gold',
            'TLT': 'Treasury Bonds',
            '^VIX': 'Volatility (inverse)'
        }

    effectiveness = {}

    for war_name, war_date in war_events.items():
        war_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(war_date.date())))

        # During war period (first 30 days)
        end_idx = min(war_idx + 30, len(market_data) - 1)
        war_period = market_data.iloc[war_idx:end_idx]

        if len(war_period) < 2:
            continue

        # Market performance during same period
        if 'SPY' in war_period.columns and not war_period['SPY'].isna().all():
            spy_start = war_period['SPY'].iloc[0]
            spy_end = war_period['SPY'].iloc[-1]

            if not pd.isna(spy_start) and not pd.isna(spy_end) and spy_start != 0:
                spy_performance = (spy_end - spy_start) / spy_start * 100

                for ticker, name in safe_havens.items():
                    if ticker in war_period.columns and not war_period[ticker].isna().all():
                        haven_start = war_period[ticker].iloc[0]
                        haven_end = war_period[ticker].iloc[-1]

                        if not pd.isna(haven_start) and not pd.isna(haven_end) and haven_start != 0:
                            haven_perf = (haven_end - haven_start) / haven_start * 100

                            # Effectiveness: how well it performs when market falls
                            if spy_performance < 0:  # Market down
                                effectiveness_score = haven_perf - spy_performance  # Outperformance
                            else:  # Market up
                                effectiveness_score = haven_perf  # Absolute performance

                            effectiveness[f"{name}_{war_name.replace(' ', '_')}"] = effectiveness_score

    return effectiveness

def create_resilience_report(market_data, war_events, output_dir=REPORTS_DIR):
    """
    Generate a comprehensive resilience analysis report.

    Parameters:
    - market_data: DataFrame with market data
    - war_events: dict of war names to datetime objects
    - output_dir: directory to save report

    Returns:
    - path to generated report file
    """
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'war_resilience_analysis_report.txt')

    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("WAR RESILIENCE ANALYSIS REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Data Range: {market_data.index.min()} to {market_data.index.max()}\n\n")

        # Sector Resilience Ranking
        f.write("SECTOR RESILIENCE RANKING (30-day recovery)\n")
        f.write("-" * 50 + "\n")
        sector_ranking = rank_sector_resilience(market_data, war_events)
        for i, (ticker, score) in enumerate(sector_ranking, 1):
            f.write(f"{i:2d}. {ticker:<6} {score:>8.2f}%\n")
        f.write("\n")

        # Individual War Analysis
        for war_name, war_date in war_events.items():
            f.write(f"WAR: {war_name.upper()}\n")
            f.write(f"Date: {war_date.strftime('%Y-%m-%d')}\n")
            f.write("-" * 30 + "\n")

            # Recovery Metrics
            f.write("Recovery Metrics (days after war start):\n")
            for ticker in ['SPY', 'XLE', 'USO', 'GLD', 'ITA', '^VIX']:
                resilience = calculate_resilience_metrics(market_data, war_date, ticker, [5, 30])
                if resilience:
                    f.write(f"  {ticker}: ")
                    metrics = []
                    for period, score in resilience.items():
                        metrics.append(f"{period}={score:.1f}%")
                    f.write(", ".join(metrics) + "\n")
            f.write("\n")

            # Volatility Resilience
            vol_resilience = calculate_volatility_resilience(market_data, war_date)
            if vol_resilience:
                f.write("Volatility Resilience (lower post-war vol = more resilient):\n")
                for metric, score in vol_resilience.items():
                    f.write(f"  {metric}: {score:.2f}\n")
            f.write("\n")

        # Safe Haven Analysis
        safe_haven_effect = analyze_safe_haven_effectiveness(market_data, war_events)
        if safe_haven_effect:
            f.write("SAFE HAVEN EFFECTIVENESS\n")
            f.write("-" * 30 + "\n")
            for haven, score in safe_haven_effect.items():
                f.write(f"{haven:<25}: {score:>8.2f}%\n")

        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")

    print(f"✓ Resilience report saved: {report_path}")
    return report_path
