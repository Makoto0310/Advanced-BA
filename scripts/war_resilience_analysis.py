"""
War Resilience Analysis Script
Analyzes how financial markets and sectors demonstrate resilience during geopolitical conflicts
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.insert(0, os.path.dirname(__file__))

from config import *
from utils import *

def create_resilience_visualizations(market_data, war_events):
    """Create comprehensive resilience analysis visualizations"""

    print("🎨 Generating resilience visualizations...")

    # 1. Sector Resilience Heatmap
    fig, ax = plt.subplots(figsize=(12, 8))

    sector_ranking = rank_sector_resilience(market_data, war_events)
    tickers = [t[0] for t in sector_ranking]
    scores = [t[1] for t in sector_ranking]

    colors = ['green' if s > 0 else 'red' for s in scores]
    bars = ax.bar(tickers, scores, color=colors, alpha=0.7)

    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.set_title('Sector Resilience Ranking\n(30-Day Recovery After War Start)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average % Recovery')
    ax.set_xlabel('Sector/Index')

    # Add value labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (1 if height >= 0 else -3),
                f'{score:.1f}%', ha='center', va='bottom' if height >= 0 else 'top', fontweight='bold')

    plt.xticks(rotation=45)
    plt.tight_layout()
    save_figure(fig, 'sector_resilience_ranking.png')

    # 2. Recovery Speed Comparison Across Wars
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    recovery_periods = [5, 10, 30, 60]
    war_names = list(war_events.keys())

    for i, days in enumerate(recovery_periods):
        ax = axes[i]

        recovery_data = []
        for war_name, war_date in war_events.items():
            war_recoveries = {}
            for ticker in ['SPY', 'XLE', 'USO', 'GLD']:
                resilience = calculate_resilience_metrics(market_data, war_date, ticker, [days])
                if resilience:
                    war_recoveries[ticker] = list(resilience.values())[0]

            if war_recoveries:
                recovery_data.append((war_name, war_recoveries))

        if recovery_data:
            wars = [d[0] for d in recovery_data]
            x = np.arange(len(wars))
            width = 0.2

            for j, ticker in enumerate(['SPY', 'XLE', 'USO', 'GLD']):
                values = [d[1].get(ticker, 0) for d in recovery_data]
                ax.bar(x + j*width, values, width, label=ticker, alpha=0.8)

            ax.set_title(f'{days}-Day Recovery After War Start', fontsize=12, fontweight='bold')
            ax.set_xticks(x + width*1.5)
            ax.set_xticklabels([w.replace('_', ' ').title() for w in wars], rotation=45)
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_figure(fig, 'recovery_speed_comparison.png')

    # 3. Volatility Resilience Analysis
    fig, ax = plt.subplots(figsize=(14, 8))

    vol_data = []
    for war_name, war_date in war_events.items():
        vol_resilience = calculate_volatility_resilience(market_data, war_date)
        if vol_resilience:
            vol_data.append((war_name, vol_resilience))

    if vol_data:
        wars = [d[0] for d in vol_data]
        x = np.arange(len(wars))

        # Plot each ticker's volatility resilience
        for ticker in ['SPY_vol_resilience', 'XLE_vol_resilience', 'USO_vol_resilience', 'GLD_vol_resilience']:
            ticker_name = ticker.split('_')[0]
            values = []
            for war_data in vol_data:
                val = war_data[1].get(ticker, np.nan)
                values.append(val if not np.isnan(val) else 0)

            ax.plot(x, values, marker='o', linewidth=2, label=ticker_name)

        ax.set_title('Volatility Resilience Across Wars\n(Higher = More Stable Post-War)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([w.replace('_', ' ').title() for w in wars], rotation=45)
        ax.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='Neutral')
        ax.set_ylabel('Volatility Resilience Score')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_figure(fig, 'volatility_resilience_analysis.png')

    # 4. Safe Haven Effectiveness
    fig, ax = plt.subplots(figsize=(12, 8))

    safe_haven_data = analyze_safe_haven_effectiveness(market_data, war_events)

    if safe_haven_data:
        havens = list(safe_haven_data.keys())
        scores = list(safe_haven_data.values())

        colors = ['gold' if 'Gold' in h else 'blue' if 'Treasury' in h else 'purple' for h in havens]
        bars = ax.barh(havens, scores, color=colors, alpha=0.7)

        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        ax.set_title('Safe Haven Effectiveness During Wars\n(Positive = Effective)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Effectiveness Score (%)')

        # Add value labels
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.text(width + (1 if width >= 0 else -5), bar.get_y() + bar.get_height()/2,
                    f'{score:.1f}%', ha='left' if width >= 0 else 'right', va='center', fontweight='bold')

    plt.tight_layout()
    save_figure(fig, 'safe_haven_effectiveness.png')

def main():
    """Main resilience analysis function"""
    print_analysis_header("War Resilience Analysis")

    try:
        # Load market data
        market_data = load_market_data()

        # Define war events for analysis
        war_events = {
            'iraq_war': pd.to_datetime('2003-03-20'),
            'israel_gaza_war': pd.to_datetime('2023-10-07'),
            'us_israel_iran_conflict': pd.to_datetime('2026-02-06')
        }

        print(f"📊 Analyzing resilience for {len(war_events)} conflicts")
        print(f"🎯 Focus sectors: SPY, XLE, USO, GLD, ITA, ^VIX")

        # Generate comprehensive report
        report_path = create_resilience_report(market_data, war_events)

        # Create visualizations
        create_resilience_visualizations(market_data, war_events)

        print("\n" + "="*80)
        print("✅ WAR RESILIENCE ANALYSIS COMPLETE")
        print("="*80)
        print(f"📄 Report: {report_path}")
        print(f"📊 Visualizations saved to: {VISUALIZATIONS_DIR}")
        print("\n🔍 KEY FINDINGS:")
        print("- Sector resilience ranking shows recovery strength")
        print("- Recovery speed varies by conflict type and duration")
        print("- Volatility analysis reveals market stability patterns")
        print("- Safe haven effectiveness measures portfolio protection")

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()