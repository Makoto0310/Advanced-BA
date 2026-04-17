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

# Download all market data
start_date = "2001-01-01"
end_date = "2026-04-17"

print(f"Loading market data from CSV...")
market_data = pd.read_csv('market_data.csv', index_col=0, parse_dates=True)

# Iraq War Start Date
iraq_war_start = pd.to_datetime('2003-03-20')

# Define time windows around war start
windows = [
    ('1 Year Before & After', iraq_war_start - pd.DateOffset(years=1), iraq_war_start + pd.DateOffset(years=1)),
    ('6 Months Before & After', iraq_war_start - pd.DateOffset(months=6), iraq_war_start + pd.DateOffset(months=6)),
    ('3 Months Before & After', iraq_war_start - pd.DateOffset(months=3), iraq_war_start + pd.DateOffset(months=3)),
    ('1 Month Before & After', iraq_war_start - pd.DateOffset(months=1), iraq_war_start + pd.DateOffset(months=1)),
]

# ============== PLOT 1: Multi-scale zoom views ==============
fig, axes = plt.subplots(len(windows), 1, figsize=(16, 5*len(windows)))

for idx, (title, start, end) in enumerate(windows):
    window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
    ax = axes[idx]
    
    # Plot all tickers
    for ticker in tickers:
        if ticker in window_data.columns and not window_data[ticker].isna().all():
            ax.plot(window_data.index, window_data[ticker], label=ticker, linewidth=1.5, alpha=0.8)
    
    # Mark war start
    ax.axvline(iraq_war_start, color='red', linestyle='--', linewidth=3, label='Iraq War Start (Mar 20, 2003)')
    ax.fill_betweenx(ax.get_ylim(), iraq_war_start, window_data.index.max(), alpha=0.1, color='red')
    
    ax.set_title(f'Iraq War Start - {title}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price (USD)')
    ax.legend(loc='best', fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iraq_war_timeline.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ Saved: iraq_war_timeline.png - Multi-scale zoom views")

# ============== PLOT 2: Normalized comparison (indexed to war start) ==============
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

time_params = [
    ('3 Months Before/After', ax_0 := axes[0, 0], iraq_war_start - pd.DateOffset(months=3), iraq_war_start + pd.DateOffset(months=3)),
    ('6 Months Before/After', ax_1 := axes[0, 1], iraq_war_start - pd.DateOffset(months=6), iraq_war_start + pd.DateOffset(months=6)),
    ('1 Year Before/After', ax_2 := axes[1, 0], iraq_war_start - pd.DateOffset(years=1), iraq_war_start + pd.DateOffset(years=1)),
    ('2 Years Before/After', ax_3 := axes[1, 1], iraq_war_start - pd.DateOffset(years=2), iraq_war_start + pd.DateOffset(years=2)),
]

for title, ax, start, end in time_params:
    window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
    
    # Find closest date to war start
    closest_idx = np.argmin(np.abs(window_data.index.values.astype('datetime64[D]') - np.datetime64(iraq_war_start.date())))
    
    # Normalize all tickers to 100 at war start
    for ticker in tickers:
        if ticker in window_data.columns and not window_data[ticker].isna().all():
            baseline = window_data[ticker].iloc[closest_idx]
            if baseline != 0:
                normalized = (window_data[ticker] / baseline * 100)
                ax.plot(window_data.index, normalized, label=ticker, linewidth=2, alpha=0.8)
    
    # Add war start line
    ax.axvline(iraq_war_start, color='red', linestyle='--', linewidth=2.5, label='War Start')
    ax.axhline(100, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    
    ax.set_title(f'{title}\n(Indexed to 100 on War Start)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price Index (War Start = 100)')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iraq_war_normalized.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ Saved: iraq_war_normalized.png - Normalized price comparison")

# ============== PLOT 3: War-sensitive sectors ONLY (zoomed) ==============
affected_tickers = ['USO', 'XLE', 'ITA', '^VIX', 'GLD']

fig, axes = plt.subplots(len(affected_tickers), 1, figsize=(16, 4*len(affected_tickers)))

for idx, ticker in enumerate(affected_tickers):
    ax = axes[idx]
    
    # Plot 3 months before and 6 months after
    start = iraq_war_start - pd.DateOffset(months=3)
    end = iraq_war_start + pd.DateOffset(months=6)
    window_data = market_data[(market_data.index >= start) & (market_data.index <= end)]
    
    if ticker in window_data.columns:
        # Top: Absolute price
        ax.plot(window_data.index, window_data[ticker], linewidth=2.5, color='blue', marker='o', markersize=3)
        ax.axvline(iraq_war_start, color='red', linestyle='--', linewidth=2, label='War Start')
        ax.fill_betweenx(ax.get_ylim(), iraq_war_start, end, alpha=0.1, color='red', label='Post-War Period')
        
        ax.set_title(f'{ticker} - Iraq War Impact (3 months prior to 6 months after)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price (USD)')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iraq_war_affected_sectors.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ Saved: iraq_war_affected_sectors.png - War-sensitive sectors detailed")

# ============== PLOT 4: Day-by-day percentage change (1st week) ==============
week_start = iraq_war_start - pd.DateOffset(days=7)
week_end = iraq_war_start + pd.DateOffset(days=14)
week_data = market_data[(market_data.index >= week_start) & (market_data.index <= week_end)]

fig, ax = plt.subplots(figsize=(16, 8))

# Calculate daily percentage change from first day
first_day_values = week_data.iloc[0]
for ticker in tickers:
    if ticker in week_data.columns and not week_data[ticker].isna().all():
        pct_change = ((week_data[ticker] - first_day_values[ticker]) / first_day_values[ticker] * 100)
        ax.plot(week_data.index, pct_change, marker='o', label=ticker, linewidth=2.5, markersize=6)

ax.axvline(iraq_war_start, color='red', linestyle='--', linewidth=3, label='Iraq War Begins (Mar 20)')
ax.axhline(0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
ax.fill_betweenx(ax.get_ylim(), iraq_war_start - pd.DateOffset(days=7), iraq_war_start, alpha=0.1, color='green', label='Before War')
ax.fill_betweenx(ax.get_ylim(), iraq_war_start, week_end, alpha=0.1, color='red', label='After War')

ax.set_title('Daily % Change from Market Open (1 Week Before to 2 Weeks After Iraq War Start)', fontsize=13, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Percentage Change (%)')
ax.legend(loc='best', fontsize=10, ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iraq_war_weekly_changes.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ Saved: iraq_war_weekly_changes.png - Daily percentage changes")

# ============== ANALYSIS SUMMARY ==============
print("\n" + "="*70)
print("IRAQ WAR MARKET IMPACT ANALYSIS - March 20, 2003")
print("="*70)

# Calculate statistics
war_start_idx = np.argmin(np.abs(market_data.index.values.astype('datetime64[D]') - np.datetime64(iraq_war_start.date())))
five_days_after = war_start_idx + 5
thirty_days_after = war_start_idx + 30

print(f"\nWar Start Date: {iraq_war_start.strftime('%B %d, %Y')}")
print(f"\n{'Ticker':<10} {'Day 0 ($)':<15} {'Day 5 ($)':<15} {'Day 30 ($)':<15} {'% Change (5d)':<15} {'% Change (30d)':<15}")
print("-" * 85)

for ticker in tickers:
    if ticker not in market_data.columns:
        continue
    
    # Get prices
    try:
        price_day0 = market_data[ticker].iloc[war_start_idx]
        price_day5 = market_data[ticker].iloc[min(five_days_after, len(market_data)-1)]
        price_day30 = market_data[ticker].iloc[min(thirty_days_after, len(market_data)-1)]
        
        # Skip NaN values
        if pd.isna(price_day0) or pd.isna(price_day5) or pd.isna(price_day30):
            print(f"{ticker:<10} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<15}")
            continue
        
        pct_5d = ((price_day5 - price_day0) / price_day0 * 100)
        pct_30d = ((price_day30 - price_day0) / price_day0 * 100)
        
        print(f"{ticker:<10} ${price_day0:<14.2f} ${price_day5:<14.2f} ${price_day30:<14.2f} {pct_5d:>14.2f}% {pct_30d:>14.2f}%")
    except:
        pass

print("\n" + "="*70)
print("KEY OBSERVATIONS:")
print("="*70)
print("• USO (Oil):     Likely spiked due to supply disruption fears")
print("• XLE (Energy):  Should show positive movement (war premium)")
print("• ITA (Defense): Typically gains from military conflict")
print("• ^VIX (Fear):   Spikes indicate increased market uncertainty")
print("• SPY (S&P 500): Overall market sentiment toward the war")
print("• GLD (Gold):    Safe-haven asset typically rises in uncertainty")
print("="*70)

print("\n✅ All Iraq War analysis plots have been generated!")
