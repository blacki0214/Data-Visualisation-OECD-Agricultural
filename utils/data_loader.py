import pandas as pd
import os

def load_data(path="data/cleaned_arg_env_data.csv"):
    """
    Load cleaned OECD agricultural environmental data.
    
    Parameters:
    - path: Path to the cleaned data CSV file
    
    Returns:
    - DataFrame with loaded data
    """
    if not os.path.exists(path):
        print(f"Warning: File {path} not found. Attempting to load raw data and clean it.")
        from utils.data_cleaner import clean_data
        raw_path = "data/arg_env_data.csv"
        if os.path.exists(raw_path):
            return clean_data(raw_path, path)
        else:
            raise FileNotFoundError(f"Neither {path} nor {raw_path} found")
    
    # Load the dataset
    df = pd.read_csv(path)
    print(f"Loaded data from {path}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Basic info about the dataset
    if 'year' in df.columns:
        years = df['year'].unique()
        print(f"Years covered: {min(years)}-{max(years)}")
    
    if 'country_code' in df.columns:
        countries = df['country_code'].nunique()
        print(f"Number of countries: {countries}")
    
    if 'nutrient_type' in df.columns:
        nutrients = df['nutrient_type'].unique()
        print(f"Nutrient types: {', '.join(nutrients)}")
    
    return df

def get_countries(df):
    """Get unique countries from the dataset"""
    if 'country_code' in df.columns:
        return df['country_code'].unique()
    return []

def get_years(df):
    """Get unique years from the dataset"""
    if 'year' in df.columns:
        return sorted(df['year'].unique())
    return []

def get_measures(df):
    """Get unique measures from the dataset"""
    if 'Measure' in df.columns:
        return df['Measure'].unique()
    elif 'measure_code' in df.columns:
        return df['measure_code'].unique()
    return []

def filter_data(df, countries=None, years=None, measures=None, nutrients=None):
    """
    Filter the dataset based on multiple criteria
    
    Parameters:
    - df: Input DataFrame
    - countries: List of country codes to include
    - years: List of years to include
    - measures: List of measures to include
    - nutrients: List of nutrient types to include
    
    Returns:
    - Filtered DataFrame
    """
    filtered_df = df.copy()
    
    if countries and 'country_code' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['country_code'].isin(countries)]
    
    if years and 'year' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['year'].isin(years)]
    
    if measures:
        if 'Measure' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Measure'].isin(measures)]
        elif 'measure_code' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['measure_code'].isin(measures)]
    
    if nutrients and 'nutrient_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['nutrient_type'].isin(nutrients)]
    
    return filtered_df

if __name__ == "__main__":
    # Example usage when script is run directly
    df = load_data()
    print("\nData sample:")
    if df is not None:
        print(df.head())
    else:
        print("No data loaded.")