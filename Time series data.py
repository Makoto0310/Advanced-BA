import matplotlib
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 10 US market tickers specified in the document
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

# The document states fetching data from 2001 to present
start_date = "2001-01-01"
end_date = "2026-04-17" # Current date

print(f"Downloading data for {len(tickers)} tickers from {start_date}...")

# Download daily OHLCV data; we'll isolate 'Close' for trend analysis
data = yf.download(tickers, start=start_date, end=end_date)
market_data = data['Close']

# Save the market data to CSV
market_data.to_csv('market_data.csv')
print("Market data saved to 'market_data.csv'") 

print("Download complete. Here are the latest 5 rows:")
print(market_data.tail())

# War periods with corrected dates - Most affected tickers: USO (Oil), XLE (Energy), ITA (Defense)
war_events = [
    ('2003-03-20', 'Iraq War Start'),
    ('2011-03-15', 'Syrian Civil War Start'),
    ('2022-02-24', 'Russia-Ukraine War Start'),
    ('2023-10-07', 'Israel-Gaza War Start'),
    ('2026-02-06', 'US/Israel-Iran Conflict Start')
]

# Most war-affected tickers
affected_tickers = ['USO', 'XLE', 'ITA', '^VIX']

# Create figure with subplots for each war event - zoomed view
fig, axes = plt.subplots(len(war_events), 1, figsize=(16, 4*len(war_events)))

for idx, (war_date, war_name) in enumerate(war_events):
    war_date_obj = pd.to_datetime(war_date)
    
    # 3 months before and 1 month after
    start_zoom = war_date_obj - pd.DateOffset(months=3)
    end_zoom = war_date_obj + pd.DateOffset(months=1)
    
    # Filter data
    zoom_data = market_data[(market_data.index >= start_zoom) & (market_data.index <= end_zoom)]
    
    ax = axes[idx] if len(war_events) > 1 else axes
    
    # Plot affected tickers
    for ticker in affected_tickers:
        if ticker in zoom_data.columns and not zoom_data[ticker].isna().all():
            # Normalize to 100 at war start for comparison
            closest_idx = np.argmin(np.abs(zoom_data.index.values.astype('datetime64[D]') - np.datetime64(war_date_obj.date())))
            baseline = zoom_data[ticker].iloc[closest_idx]
            normalized = (zoom_data[ticker] / baseline * 100) if baseline != 0 else zoom_data[ticker]
            ax.plot(zoom_data.index, normalized, marker='o', label=ticker, linewidth=2)
    
    # Mark war start
    ax.axvline(war_date_obj, color='red', linestyle='--', linewidth=2, label='War Start')
    ax.set_title(f'{war_name} ({war_date}) - Zoomed View (3mo before, 1mo after)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (Indexed to War Start = 100)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('war_effects_zoomed.png', dpi=100, bbox_inches='tight')
plt.close()
print("Zoomed war effects plot saved as 'war_effects_zoomed.png'")

# Create a detailed plot for the most recent war (US/Israel-Iran 2026)
print("\nDetailed analysis of US/Israel-Iran Conflict (Feb 2026):")
recent_war_date = pd.to_datetime('2026-02-06')
start_recent = recent_war_date - pd.DateOffset(months=3)
end_recent = recent_war_date + pd.DateOffset(months=2)

recent_data = market_data[(market_data.index >= start_recent) & (market_data.index <= end_recent)]

fig, axes_recent = plt.subplots(2, 2, figsize=(16, 10))

# Plot each affected ticker
plot_data = {'USO': axes_recent[0, 0], 'XLE': axes_recent[0, 1], 'ITA': axes_recent[1, 0], '^VIX': axes_recent[1, 1]}

for ticker, ax in plot_data.items():
    if ticker in recent_data.columns:
        ax.plot(recent_data.index, recent_data[ticker], linewidth=2.5, color='blue')
        ax.axvline(recent_war_date, color='red', linestyle='--', linewidth=2, label='War Start (Feb 6, 2026)')
        ax.fill_between(recent_data.index, recent_data[ticker].min(), recent_data[ticker].max(), 
                         where=(recent_data.index >= recent_war_date), alpha=0.1, color='red')
        ax.set_title(f'{ticker} - Before and After US/Israel-Iran Conflict', fontsize=11, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price (USD)')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('recent_war_detailed.png', dpi=100, bbox_inches='tight')
plt.close()
print("Detailed recent war analysis saved as 'recent_war_detailed.png'")