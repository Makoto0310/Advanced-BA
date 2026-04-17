import matplotlib
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 10 US market tickers
tickers = [
    "SPY",   # S&P 500
    "^VIX",  # Fear index
    "XLY",   # Consumer discretionary
    "JETS",  # Airlines
    "XLE",   # Energy
    "XLF",   # Financials
    "ITA",   # Defence
    "GLD",   # Gold
    "TLT",   # 10-year Treasuries
    "USO"    # WTI crude oil
]

print("Loading market data from CSV...")
market_data = pd.read_csv('market_data.csv', index_col=0, parse_dates=True)

# War start dates
wars = [
    ('Israel-Gaza War', pd.to_datetime('2023-10-07')),
    ('US/Israel-Iran Conflict', pd.to_datetime('2026-02-06'))
]

for war_name, war_start in wars:
    print(f"\n{'='*70}")
    print(f"ANALYZING: {war_name}")
    print(f"War Start Date: {war_start.strftime('%B %d, %Y')}")
    print(f"{'='*70}")
    
    # ============== PLOT 1: Multi-scale zoom views ==============
    windows = [
        ('1 Year Before & After', war_start - pd.DateOffset(years=1), war_start + pd.DateOffset(years=1)),
        ('6 Months Before & After', war_start - pd.DateOffset(months=6), war_start + pd.DateOffset(months=6)),
        ('3 Months Before & After', war_start - pd.DateOffset(months=3), war_start + pd.DateOffset(months=3)),
        ('1 Month Before & After', war_start - pd.DateOffset(months=1), war_start + pd.DateOffset(months=1)),
    ]
    
    fig, axes = plt.subplots(len(windows), 1, figsize=(16, 5*len(windows)))
    
    for idx, (title, start, end) in enumerate(windows):
        window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
        ax = axes[idx]
        
        # Plot all tickers
        for ticker in tickers:
            if ticker in window_data.columns and not window_data[ticker].isna().all():
                ax.plot(window_data.index, window_data[ticker], label=ticker, linewidth=1.5, alpha=0.8)
        
        # Mark war start
        ax.axvline(war_start, color='red', linestyle='--', linewidth=3, label=f'{war_name} Start')
        ax.fill_betweenx(ax.get_ylim(), war_start, window_data.index.max(), alpha=0.1, color='red')
        
        ax.set_title(f'{war_name} - {title}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price (USD)')
        ax.legend(loc='best', fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"{war_name.lower().replace(' ', '_').replace('/', '-')}_timeline.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")
    
    # ============== PLOT 2: Normalized comparison ==============
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    time_params = [
        ('3 Months Before/After', axes[0, 0], war_start - pd.DateOffset(months=3), war_start + pd.DateOffset(months=3)),
        ('6 Months Before/After', axes[0, 1], war_start - pd.DateOffset(months=6), war_start + pd.DateOffset(months=6)),
        ('1 Year Before/After', axes[1, 0], war_start - pd.DateOffset(years=1), war_start + pd.DateOffset(years=1)),
        ('2 Years Before/After', axes[1, 1], war_start - pd.DateOffset(years=2), war_start + pd.DateOffset(years=2)),
    ]
    
    for title, ax, start, end in time_params:
        window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
        
        # Find closest date to war start
        closest_idx = np.argmin(np.abs(window_data.index.values.astype('datetime64[D]') - np.datetime64(war_start.date())))
        
        # Normalize
        for ticker in tickers:
            if ticker in window_data.columns and not window_data[ticker].isna().all():
                baseline = window_data[ticker].iloc[closest_idx]
                if baseline != 0:
                    normalized = (window_data[ticker] / baseline * 100)
                    ax.plot(window_data.index, normalized, label=ticker, linewidth=2, alpha=0.8)
        
        ax.axvline(war_start, color='red', linestyle='--', linewidth=2.5, label='War Start')
        ax.axhline(100, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        
        ax.set_title(f'{title}\n(Indexed to 100 on War Start)', fontsize=11, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price Index (War Start = 100)')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"{war_name.lower().replace(' ', '_').replace('/', '-')}_normalized.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")
    
    # ============== PLOT 3: War-sensitive sectors ONLY ==============
    affected_tickers_list = ['USO', 'XLE', 'ITA', '^VIX', 'GLD']
    
    fig, axes = plt.subplots(len(affected_tickers_list), 1, figsize=(16, 4*len(affected_tickers_list)))
    
    for idx, ticker in enumerate(affected_tickers_list):
        ax = axes[idx]
        
        start = war_start - pd.DateOffset(months=3)
        end = war_start + pd.DateOffset(months=6)
        window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
        
        if ticker in window_data.columns and not window_data[ticker].isna().all():
            ax.plot(window_data.index, window_data[ticker], linewidth=2.5, color='blue', marker='o', markersize=3)
            ax.axvline(war_start, color='red', linestyle='--', linewidth=2, label='War Start')
            ax.fill_betweenx(ax.get_ylim(), war_start, end, alpha=0.1, color='red', label='Post-War Period')
            
            ax.set_title(f'{ticker} - {war_name} Impact (3 months prior to 6 months after)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price (USD)')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"{war_name.lower().replace(' ', '_').replace('/', '-')}_affected_sectors.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")
    
    # ============== PLOT 4: Weekly changes ==============
    week_start = war_start - pd.DateOffset(days=7)
    week_end = war_start + pd.DateOffset(days=14)
    week_data = market_data[(market_data.index >= week_start) & (market_data.index <= week_end)]
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    first_day_values = week_data.iloc[0]
    for ticker in tickers:
        if ticker in week_data.columns and not week_data[ticker].isna().all():
            pct_change = ((week_data[ticker] - first_day_values[ticker]) / first_day_values[ticker] * 100)
            ax.plot(week_data.index, pct_change, marker='o', label=ticker, linewidth=2.5, markersize=6)
    
    ax.axvline(war_start, color='red', linestyle='--', linewidth=3, label=f'{war_name} Begins')
    ax.axhline(0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
    ax.fill_betweenx(ax.get_ylim(), week_start, war_start, alpha=0.1, color='green', label='Before War')
    ax.fill_betweenx(ax.get_ylim(), war_start, week_end, alpha=0.1, color='red', label='After War')
    
    ax.set_title(f'Daily % Change from Market Open - {war_name}\n(1 Week Before to 2 Weeks After)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Percentage Change (%)')
    ax.legend(loc='best', fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"{war_name.lower().replace(' ', '_').replace('/', '-')}_weekly_changes.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")
    
    # ============== ANALYSIS SUMMARY ==============
    war_start_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(war_start.date())))
    five_days_after = min(war_start_idx + 5, len(market_data)-1)
    thirty_days_after = min(war_start_idx + 30, len(market_data)-1)
    
    print(f"\n{'Ticker':<10} {'Day 0 ($)':<15} {'Day 5 ($)':<15} {'Day 30 ($)':<15} {'% Change (5d)':<15} {'% Change (30d)':<15}")
    print("-" * 85)
    
    for ticker in tickers:
        if ticker not in market_data.columns:
            continue
        
        try:
            price_day0 = market_data[ticker].iloc[war_start_idx]
            price_day5 = market_data[ticker].iloc[five_days_after]
            price_day30 = market_data[ticker].iloc[thirty_days_after]
            
            if pd.isna(price_day0) or pd.isna(price_day5) or pd.isna(price_day30):
                print(f"{ticker:<10} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<15}")
                continue
            
            pct_5d = ((price_day5 - price_day0) / price_day0 * 100)
            pct_30d = ((price_day30 - price_day0) / price_day0 * 100)
            
            print(f"{ticker:<10} ${price_day0:<14.2f} ${price_day5:<14.2f} ${price_day30:<14.2f} {pct_5d:>14.2f}% {pct_30d:>14.2f}%")
        except:
            pass
    
    print("\n" + "="*70)

print("\n✅ All analyses complete!")
