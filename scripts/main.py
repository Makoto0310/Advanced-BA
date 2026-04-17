"""
Main entry point for market war impact analysis
Orchestrates all analyses
"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.insert(0, os.path.dirname(__file__))

from config import *
from utils import create_output_dirs, print_analysis_header

def main():
    """Main entry point"""
    print_analysis_header("Advanced Business Analytics - Market War Impact Analysis")
    print(f"Analysis Date: {DATA_END_DATE}")
    print(f"Data Range: {DATA_START_DATE} to {DATA_END_DATE}")
    print(f"Tickers Analyzed: {', '.join(TICKERS)}")
    
    # Create output directories
    create_output_dirs()
    
    print("\n" + "="*80)
    print("Available Analysis Scripts:")
    print("="*80)
    print("1. python market_data_downloader.py    - Download and save market data")
    print("2. python iraq_war_analysis.py         - Analyze Iraq War (2003)")
    print("3. python middle_east_conflicts.py     - Analyze Israel-Gaza & US/Israel-Iran")
    print("4. python comprehensive_analysis.py    - All conflicts comparison")
    print("\n💡 Run individual scripts or use this as import for other projects")
    print("="*80)

if __name__ == "__main__":
    main()
