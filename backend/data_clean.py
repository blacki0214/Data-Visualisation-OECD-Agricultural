import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("./data/arg_env_data.csv")

print(f"Original dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Check data quality
print(f"\nMissing values in OBS_VALUE: {df['OBS_VALUE'].isna().sum()}")
print(f"Non-null values in OBS_VALUE: {df['OBS_VALUE'].notna().sum()}")

# Remove completely empty rows
df = df.dropna(how='all')

# Clean column names - remove spaces and special characters
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Convert TIME_PERIOD to datetime format (keep as year for this dataset)
if 'TIME_PERIOD' in df.columns:
    df['TIME_PERIOD'] = pd.to_numeric(df['TIME_PERIOD'], errors='coerce')

# Convert OBS_VALUE to numeric
if 'OBS_VALUE' in df.columns:
    df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')

# Remove rows where OBS_VALUE is null (these are likely empty data points)
df = df.dropna(subset=['OBS_VALUE'])

# Clean up redundant columns - keep the code versions, drop descriptive ones
columns_to_drop = [
    'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION',
    'Reference_area', 'Frequency_of_observation', 'Erosion_risk_level',
    'Water_type', 'Unit_of_measure', 'Time_period', 'Observation_value',
    'Observation_status', 'Unit_multiplier', 'Base_period'
]

# Only drop columns that actually exist
columns_to_drop = [col for col in columns_to_drop if col in df.columns]
df = df.drop(columns=columns_to_drop)

# Rename remaining columns for clarity
column_mapping = {
    'REF_AREA': 'country_code',
    'FREQ': 'frequency',
    'MEASURE': 'measure_code', 
    'EROSION_LEVEL': 'erosion_level',
    'WATER_TYPE': 'water_type',
    'NUTRIENTS': 'nutrient_type',
    'UNIT_MEASURE': 'unit',
    'TIME_PERIOD': 'year',
    'OBS_VALUE': 'value',
    'DECIMALS': 'decimals',
    'OBS_STATUS': 'status'
}

df = df.rename(columns=column_mapping)

# Replace coded values with more meaningful ones
df['nutrient_type'] = df['nutrient_type'].replace({
    'NITROGEN': 'Nitrogen',
    'PHOSPHORUS': 'Phosphorus'
})

# Handle special values
df['erosion_level'] = df['erosion_level'].replace('_Z', 'Not applicable')
df['water_type'] = df['water_type'].replace('_Z', 'Not applicable')
df['nutrient_type'] = df['nutrient_type'].replace('_Z', 'Not applicable')

# Remove duplicate rows
df = df.drop_duplicates()

# Sort by country, year, and measure for better organization
df = df.sort_values(['country_code', 'year', 'measure_code'])

# Reset index
df = df.reset_index(drop=True)

print(f"\nCleaned dataset shape: {df.shape}")
print(f"Columns after cleaning: {df.columns.tolist()}")
print(f"Year range: {df['year'].min()} - {df['year'].max()}")
print(f"Countries: {df['country_code'].nunique()}")
print(f"Unique measures: {df['measure_code'].nunique()}")

# Display sample of cleaned data
print("\nSample of cleaned data:")
print(df.head(10))

# Check for any remaining data quality issues
print(f"\nData quality check:")
print(f"Missing values per column:")
print(df.isnull().sum())

# Save the cleaned data
df.to_csv("./data/cleaned_arg_env_data.csv", index=False)
print(f"\nCleaned data saved to ./data/cleaned_arg_env_data.csv")

# Optional: Create a summary report
summary_stats = {
    'total_records': len(df),
    'countries': df['country_code'].nunique(),
    'years': df['year'].nunique(),
    'measures': df['measure_code'].nunique(),
    'year_range': f"{df['year'].min()}-{df['year'].max()}",
    'nutrients': df['nutrient_type'].value_counts().to_dict()
}

print(f"\nSummary Statistics:")
for key, value in summary_stats.items():
    print(f"{key}: {value}")