import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('data/market_data.csv', parse_dates=['Date'])

print("Dataset Overview:")
print(f"Shape: {df.shape}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Total days: {(df['Date'].max() - df['Date'].min()).days + 1}")
print(f"Actual records: {len(df)}")
print(f"Missing dates: {(df['Date'].max() - df['Date'].min()).days + 1 - len(df)}")

print("\nMissing Values Summary:")
missing_summary = df.isnull().sum()
print(missing_summary)

print("\nPercentage of missing values:")
print((missing_summary / len(df) * 100).round(2))

print("\nData Types:")
print(df.dtypes)

print("\nBasic Statistics:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(df[numeric_cols].describe())

print("\nNegative values check:")
for col in numeric_cols:
    neg_count = (df[col] < 0).sum()
    if neg_count > 0:
        print(f"{col}: {neg_count} negative values")

print("\nZero values check:")
for col in numeric_cols:
    zero_count = (df[col] == 0).sum()
    if zero_count > 0:
        print(f"{col}: {zero_count} zero values")

print("\nOutlier detection (values > 3 std from mean):")
for col in numeric_cols:
    mean = df[col].mean()
    std = df[col].std()
    outliers = ((df[col] - mean) / std).abs() > 3
    outlier_count = outliers.sum()
    if outlier_count > 0:
        print(f"{col}: {outlier_count} outliers")

print("\nDate continuity check:")
df = df.sort_values('Date')
date_diff = df['Date'].diff().dt.days
gaps = date_diff[date_diff > 1]
if len(gaps) > 0:
    print(f"Found {len(gaps)} gaps in dates:")
    for i, gap in gaps.items():
        print(f"Gap of {gap-1} days before {df.loc[i, 'Date']}")
else:
    print("No gaps in dates larger than 1 day")