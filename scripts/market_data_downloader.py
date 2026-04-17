"""
Market Data Downloader
Downloads historical market data and saves to CSV
"""
import sys
import os
import pandas as pd
import yfinance as yf

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.insert(0, os.path.dirname(__file__))

from config import *
from utils import print_analysis_header, create_output_dirs

def download_market_data(tickers=TICKERS, start=DATA_START_DATE, end=DATA_END_DATE):
    """Download market data from Yahoo Finance"""
    print_analysis_header("Downloading Market Data")
    print(f"Downloading {len(tickers)} tickers from {start} to {end}...")
    
    data = yf.download(tickers, start=start, end=end)
    market_data = data['Close']
    
    print(f"✓ Downloaded {len(market_data)} rows of data")
    print(f"✓ Columns: {', '.join(market_data.columns)}")
    return market_data

def save_market_data(market_data, output_path=MARKET_DATA_CSV):
    """Save market data to CSV"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    market_data.to_csv(output_path)
    print(f"✓ Data saved to: {output_path}")
    return output_path

def main():
    """Main function"""
    # Create output directories
    create_output_dirs()
    
    # Download data
    market_data = download_market_data()
    
    # Save data
    save_market_data(market_data)
    
    # Display summary
    print("\n" + "="*80)
    print("Data Summary:")
    print("="*80)
    print(market_data.tail(5))
    print("\n✅ Market data download complete!")

if __name__ == "__main__":
    main()
