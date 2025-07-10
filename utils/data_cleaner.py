import pandas as pd
import numpy as np
import os

def clean_data(input_path="data/arg_env_data.csv", output_path="data/cleaned_arg_env_data.csv"):
    """
    Clean and process OECD agricultural environmental data.
    
    Parameters:
    - input_path: Path to the raw data CSV file
    - output_path: Path to save the cleaned data
    
    Returns:
    - DataFrame with cleaned data
    """
    # Check if the file exists and fix path if needed
    if not os.path.exists(input_path):
        # Try to find the file relative to the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alternative_path = os.path.join(project_root, input_path)
        
        if os.path.exists(alternative_path):
            input_path = alternative_path
            # Also adjust output path
            output_path = os.path.join(project_root, output_path)
        else:
            raise FileNotFoundError(f"Could not find data file at {input_path} or {alternative_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the dataset
    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path)
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Check data quality
    print(f"\nMissing values in OBS_VALUE: {df['OBS_VALUE'].isna().sum()}")
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Clean column names - remove spaces and special characters
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # Convert TIME_PERIOD to numeric
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
    
    # Only rename columns that exist
    column_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df.rename(columns=column_mapping)
    
    # Replace coded values with more meaningful ones
    if 'nutrient_type' in df.columns:
        df['nutrient_type'] = df['nutrient_type'].replace({
            'NITROGEN': 'Nitrogen',
            'PHOSPHORUS': 'Phosphorus'
        })
    
    # Handle special values
    for col in ['erosion_level', 'water_type', 'nutrient_type']:
        if col in df.columns:
            df[col] = df[col].replace('_Z', 'Not applicable')
    
    # Add a column with more descriptive measure names
    if 'measure_code' in df.columns:
        df['Measure'] = df['measure_code']
        
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Sort by country, year, and measure for better organization
    sort_cols = [col for col in ['country_code', 'year', 'measure_code'] if col in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"\nCleaned dataset shape: {df.shape}")
    print(f"Columns after cleaning: {df.columns.tolist()}")
    
    if 'year' in df.columns:
        print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    
    if 'country_code' in df.columns:
        print(f"Countries: {df['country_code'].nunique()}")
    
    if 'measure_code' in df.columns:
        print(f"Unique measures: {df['measure_code'].nunique()}")
    
    # Display sample of cleaned data
    print("\nSample of cleaned data:")
    print(df.head(5))
    
    # Check for any remaining data quality issues
    print(f"\nMissing values per column:")
    print(df.isnull().sum())
    
    # Save the cleaned data
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to {output_path}")
    
    return df

if __name__ == "__main__":
    # Execute the cleaning process when the script is run directly
    clean_data()