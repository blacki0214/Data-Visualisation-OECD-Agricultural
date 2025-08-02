"""
Utility functions for categorizing and grouping measure codes into logical categories
"""

def get_measure_category_mapping():
    """
    Returns a dictionary mapping actual measure codes to their categories
    Based on real measure codes in the OECD data
    """
    mapping = {
        # 🏞️ Land Use - Forest land, Grassland, Cropland, Wetlands, Settlements
        'A_LAND': {'category': '🏞️ Land Use', 'subcategory': 'Forest land'},
        'TOTAGR_LAND': {'category': '🏞️ Land Use', 'subcategory': 'Grassland'},
        'PERMA': {'category': '🏞️ Land Use', 'subcategory': 'Cropland'},
        'PERMPASTURE': {'category': '🏞️ Land Use', 'subcategory': 'Grassland'},
        'T_CROP': {'category': '🏞️ Land Use', 'subcategory': 'Cropland'},
        'UA': {'category': '🏞️ Land Use', 'subcategory': 'Cropland'},
        'SF': {'category': '🏞️ Land Use', 'subcategory': 'Settlements'},
        'GL_CO2': {'category': '🏞️ Land Use', 'subcategory': 'Grassland'},
        'CL_CO2': {'category': '🏞️ Land Use', 'subcategory': 'Cropland'},
        'SETT_CO2': {'category': '🏞️ Land Use', 'subcategory': 'Settlements'},
        'WET_CO2': {'category': '🏞️ Land Use', 'subcategory': 'Wetlands'},
        'F_CO2': {'category': '🏞️ Land Use', 'subcategory': 'Forest land'},
        
        # 🐄 Livestock & Manure - Livestock manure production, Pigs, Poultry, Other livestock, Manure management
        'A12': {'category': '🐄 Livestock & Manure', 'subcategory': 'Livestock manure production'},
        'MANURE': {'category': '🐄 Livestock & Manure', 'subcategory': 'Manure management'},
        'MANUR': {'category': '🐄 Livestock & Manure', 'subcategory': 'Manure management'},
        'C1': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C21': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C211': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C212': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C213': {'category': '🐄 Livestock & Manure', 'subcategory': 'Pigs'},
        'C217': {'category': '🐄 Livestock & Manure', 'subcategory': 'Poultry'},
        'C22': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C221': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        'C222': {'category': '🐄 Livestock & Manure', 'subcategory': 'Other livestock'},
        
        # 🌾 Crop Production - Cereals, Other crops, Harvested crops
        'A11': {'category': '🌾 Crop Production', 'subcategory': 'Harvested crops'},
        'A_P_CROP': {'category': '🌾 Crop Production', 'subcategory': 'Other crops'},
        'RICE': {'category': '🌾 Crop Production', 'subcategory': 'Cereals'},
        'C000': {'category': '🌾 Crop Production', 'subcategory': 'Other crops'},
        'BRN': {'category': '🌾 Crop Production', 'subcategory': 'Other crops'},
        'RES': {'category': '🌾 Crop Production', 'subcategory': 'Other crops'},
        
        # 🌿 Nutrient Inputs - Fertilisers, Inorganic fertilisers, Net input of manure
        'F1': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Fertilisers'},
        'F11': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Inorganic fertilisers'},
        'F12': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Fertilisers'},
        'LIM': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Inorganic fertilisers'},
        'M1': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Net input of manure'},
        'M21': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Net input of manure'},
        'M23': {'category': '🌿 Nutrient Inputs', 'subcategory': 'Net input of manure'},
        
        # 💧 Nutrient Outputs - Nutrient outputs, Crop uptake
        'O1': {'category': '💧 Nutrient Outputs', 'subcategory': 'Nutrient outputs'},
        'OO': {'category': '💧 Nutrient Outputs', 'subcategory': 'Nutrient outputs'},
        'O_F': {'category': '💧 Nutrient Outputs', 'subcategory': 'Crop uptake'},
        
        # ⚖️ Nutrient Balances - Balance (inputs minus outputs), Balance per hectare
        'B0': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance (inputs minus outputs)'},
        'B0_H': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance per hectare'},
        'B1': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance (inputs minus outputs)'},
        'PB_S': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance per hectare'},
        'PB_S2': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance per hectare'},
        'FB_AR': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance (inputs minus outputs)'},
        'FB_AR2': {'category': '⚖️ Nutrient Balances', 'subcategory': 'Balance (inputs minus outputs)'},
    }
    
    return mapping

def categorize_measure(measure_code):
    """
    Categorize a measure code into its appropriate category and subcategory
    """
    mapping = get_measure_category_mapping()
    
    if measure_code in mapping:
        return mapping[measure_code]
    
    # Default category for unmatched measures
    return {
        'category': '📊 Other Indicators',
        'subcategory': 'Miscellaneous'
    }

def get_category_options_for_dropdown():
    """
    Get dropdown options for just the measure categories (without subcategories)
    
    Returns:
        List of dictionaries with 'label' and 'value' keys for category dropdown
    """
    # Get all unique categories from the measure mapping
    mapping = get_measure_category_mapping()
    categories = set(info['category'] for info in mapping.values())
    
    # Create simple category options
    return [
        {'label': category, 'value': category}
        for category in sorted(categories)
    ]

def filter_and_aggregate_by_category_only(df, selected_category, countries=None, nutrient=None, years=None):
    """
    Filter data by category only and return aggregated data
    
    Parameters:
    - df: Original dataframe
    - selected_category: Selected measure category
    - countries: Optional list of countries to filter
    - nutrient: Optional nutrient type to filter
    - years: Optional tuple of (start_year, end_year)
    
    Returns:
    - Aggregated DataFrame for the selected category
    """
    if not selected_category:
        return df
    
    # Get all measure codes for this category
    mapping = get_measure_category_mapping()
    category_measures = [code for code, info in mapping.items() if info['category'] == selected_category]
    
    # Filter data to only include measures from this category
    filtered_df = df[df['measure_code'].isin(category_measures)].copy()
    
    # Apply additional filters
    if countries:
        filtered_df = filtered_df[filtered_df['country_code'].isin(countries)]
    
    if nutrient:
        filtered_df = filtered_df[filtered_df['nutrient_type'] == nutrient]
    
    if years:
        filtered_df = filtered_df[(filtered_df['year'] >= years[0]) & (filtered_df['year'] <= years[1])]
    
    # Aggregate by summing all measures in the category
    aggregated = filtered_df.groupby(['country_code', 'nutrient_type', 'year']).agg({
        'value': 'sum',  # Sum all measures in the category
        'unit': 'first'  # Take the first unit (should be consistent within category)
    }).reset_index()
    
    # Add category information
    aggregated['category'] = selected_category
    
    return aggregated

def get_category_color_map():
    """
    Get a color mapping for each category for consistent visualization
    
    Returns:
    - Dictionary mapping categories to colors
    """
    return {
        '🏞️ Land Use': '#4CAF50',                    # Green
        '🐄 Livestock & Manure': '#FF9800',          # Orange
        '🌾 Crop Production': '#FFC107',              # Yellow/Amber
        '🌿 Nutrient Inputs': '#8BC34A',             # Light Green
        '💧 Nutrient Outputs': '#2196F3',            # Blue
        '⚖️ Nutrient Balances': '#9C27B0',           # Purple
        '📊 Other Indicators': '#795548'              # Brown
    }

def create_measure_country_heatmap_data(df, selected_category, nutrient_type, selected_year, selected_countries):
    """
    Create data for heatmap showing individual measures (y-axis) vs countries (x-axis)
    
    Parameters:
    - df: Original dataframe
    - selected_category: Selected measure category
    - nutrient_type: Selected nutrient type
    - selected_year: Selected year
    - selected_countries: List of selected country codes
    
    Returns:
    - Pivot table ready for heatmap
    """
    # Get all measure codes for this category
    mapping = get_measure_category_mapping()
    category_measures = [code for code, info in mapping.items() if info['category'] == selected_category]
    
    # Filter data
    filtered_df = df[
        (df['measure_code'].isin(category_measures)) &
        (df['nutrient_type'] == nutrient_type) &
        (df['year'] == selected_year) &
        (df['country_code'].isin(selected_countries))
    ].copy()
    
    if filtered_df.empty:
        return None, None
    
    # Add readable measure names
    def get_measure_label(measure_code):
        info = mapping.get(measure_code, {'subcategory': measure_code})
        return f"{measure_code} - {info['subcategory']}"
    
    filtered_df['measure_label'] = filtered_df['measure_code'].apply(get_measure_label)
    
    # Create pivot table (measures as rows, countries as columns)
    pivot_df = filtered_df.pivot_table(
        values='value',
        index='measure_label',
        columns='country_code',
        aggfunc='mean',
        fill_value=0
    )
    
    # Sort countries by total values (descending)
    country_totals = pivot_df.sum(axis=0).sort_values(ascending=False)
    pivot_df = pivot_df.reindex(columns=country_totals.index)
    
    return pivot_df, filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns else ''
