import pandas as pd
from .EU_mapping import get_eu_members

def clean_country_codes(df):
    """
    Clean and standardize country codes in the dataset
    
    Parameters:
    - df: DataFrame containing country_code column
    
    Returns:
    - DataFrame with cleaned country codes
    """
    # Make a copy of the dataframe to avoid modifying the original
    cleaned_df = df.copy()
    
    # Map of problematic codes to valid ISO-3 codes
    country_code_map = {
        'BE2': 'BEL',  # Belgium (Flemish Region)
        'BE3': 'BEL',  # Belgium (Wallonia)
    }
    
    # Apply direct mapping
    cleaned_df['country_code'] = cleaned_df['country_code'].map(
        lambda x: country_code_map.get(x, x)
    )
    
    return cleaned_df

def distribute_eu_data(df, method='equal'):
    """
    Distribute EU aggregate data to member countries
    
    Parameters:
    - df: DataFrame containing country_code column
    - method: How to distribute values ('equal', 'gdp', 'population', etc.)
    
    Returns:
    - DataFrame with EU data distributed to member countries
    """
    # Make a copy of the dataframe
    result_df = df.copy()
    
    # Get EU members mapping
    eu_mappings = get_eu_members()
    
    # For each EU entity
    eu_entities = ['EU27', 'EU28', 'EU27_2020', 'EU']
    
    # Create a list to collect the new rows
    new_rows = []
    
    for eu_entity in eu_entities:
        # Filter rows with this EU entity
        eu_rows = result_df[result_df['country_code'] == eu_entity]
        
        if not eu_rows.empty:
            print(f"Found {len(eu_rows)} rows for {eu_entity}")
            
            # Get the member countries
            members = eu_mappings.get(eu_entity, [])
            
            if not members:
                continue
                
            # For each EU row, create individual rows for each member
            for _, row in eu_rows.iterrows():
                for member in members:
                    # Create a new row for this member
                    new_row = row.copy()
                    new_row['country_code'] = member
                    
                    # Adjust value based on distribution method
                    if method == 'equal':
                        # Equal distribution - each country gets the same value
                        new_row['value'] = row['value']
                    elif method == 'proportional':
                        # You could implement proportional distribution based on GDP, area, population
                        # This would require additional data sources
                        # For now, just use equal distribution
                        new_row['value'] = row['value']
                        
                    new_rows.append(new_row)
    
    # Add the new rows to the dataframe
    if new_rows:
        new_rows_df = pd.DataFrame(new_rows)
        result_df = pd.concat([result_df, new_rows_df], ignore_index=True)
        
        # Drop the original EU entity rows
        result_df = result_df[~result_df['country_code'].isin(eu_entities)]
    
    return result_df