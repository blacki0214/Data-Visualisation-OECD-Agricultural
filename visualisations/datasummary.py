from dash import html
import pandas as pd

def create_data_summary(filtered_df, nutrient, measure):
    """
    Create a data summary component with unit-aware formatting
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    
    Returns:
    - Dash HTML component
    """
    if filtered_df.empty:
        return html.P("No data available for the selected filters.")
    
    # Get unit information
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    
    # Create unit display
    if unit:
        if unit == 'T':
            unit_display = 'Tonnes'
        elif unit == 'KG':
            unit_display = 'Kilograms'
        elif unit == 'HA':
            unit_display = 'Hectares'
        elif unit == 'T_CO2E':
            unit_display = 'Tonnes CO₂ equivalent'
        elif unit == 'TOE':
            unit_display = 'Tonnes Oil Equivalent'
        else:
            unit_display = unit
    else:
        unit_display = 'Unknown'
    
    # Calculate statistics
    min_val = filtered_df['value'].min()
    max_val = filtered_df['value'].max()
    avg_val = filtered_df['value'].mean()
    median_val = filtered_df['value'].median()
    std_val = filtered_df['value'].std()
    
    # Get the country with highest and lowest values
    max_country = filtered_df.loc[filtered_df['value'].idxmax(), 'country_code']
    min_country = filtered_df.loc[filtered_df['value'].idxmin(), 'country_code']
    
    # Get measure description
    measure_desc = filtered_df['Measure'].iloc[0] if 'Measure' in filtered_df.columns else measure
    
    # Format values based on unit
    def format_value_with_unit(val, unit_type):
        if pd.isna(val):
            return "N/A"
        
        if unit_type in ['T', 'T_CO2E', 'TOE']:
            if val >= 1000000:
                return f"{val/1000000:.2f}M {unit_display}"
            elif val >= 1000:
                return f"{val/1000:.1f}K {unit_display}"
            else:
                return f"{val:.2f} {unit_display}"
        elif unit_type == 'HA':
            if val >= 1000000:
                return f"{val/1000000:.2f}M {unit_display}"
            elif val >= 1000:
                return f"{val/1000:.1f}K {unit_display}"
            else:
                return f"{val:.1f} {unit_display}"
        elif unit_type == 'KG':
            if val >= 1000:
                return f"{val/1000:.2f} Tonnes"
            else:
                return f"{val:.2f} {unit_display}"
        else:
            return f"{val:.2f} {unit_display}"
    
    # Create summary
    summary = [
        html.Div([
            html.Div([
                html.H4("Statistics", style={'textAlign': 'center'}),
                html.P(f"Minimum Value: {format_value_with_unit(min_val, unit)} ({min_country})"),
                html.P(f"Maximum Value: {format_value_with_unit(max_val, unit)} ({max_country})"),
                html.P(f"Average Value: {format_value_with_unit(avg_val, unit)}"),
                html.P(f"Median Value: {format_value_with_unit(median_val, unit)}"),
                html.P(f"Standard Deviation: {format_value_with_unit(std_val, unit)}")
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H4("Dataset Info", style={'textAlign': 'center'}),
                html.P(f"Number of Countries: {filtered_df['country_code'].nunique()}"),
                html.P(f"Year Range: {filtered_df['year'].min()} - {filtered_df['year'].max()}"),
                html.P(f"Nutrient: {nutrient}"),
                html.P(f"Measure: {measure_desc}"),
                html.P(f"Unit: {unit_display}"),
                html.P(f"Total Data Points: {len(filtered_df)}")
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ])
    ]
    
    return summary