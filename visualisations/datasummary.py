from dash import html

def create_data_summary(filtered_df, nutrient, measure):
    """
    Create a data summary component
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    
    Returns:
    - Dash HTML component
    """
    if filtered_df.empty:
        return html.P("No data available for the selected filters.")
    
    # Calculate statistics
    min_val = filtered_df['value'].min()
    max_val = filtered_df['value'].max()
    avg_val = filtered_df['value'].mean()
    median_val = filtered_df['value'].median()
    std_val = filtered_df['value'].std()
    
    # Get the country with highest and lowest values
    max_country = filtered_df.loc[filtered_df['value'].idxmax(), 'country_code']
    min_country = filtered_df.loc[filtered_df['value'].idxmin(), 'country_code']
    
    # Create summary
    summary = [
        html.Div([
            html.Div([
                html.H4("Statistics", style={'textAlign': 'center'}),
                html.P(f"Minimum Value: {min_val:.2f} ({min_country})"),
                html.P(f"Maximum Value: {max_val:.2f} ({max_country})"),
                html.P(f"Average Value: {avg_val:.2f}"),
                html.P(f"Median Value: {median_val:.2f}"),
                html.P(f"Standard Deviation: {std_val:.2f}")
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H4("Dataset Info", style={'textAlign': 'center'}),
                html.P(f"Number of Countries: {filtered_df['country_code'].nunique()}"),
                html.P(f"Year Range: {filtered_df['year'].min()} - {filtered_df['year'].max()}"),
                html.P(f"Nutrient: {nutrient}"),
                html.P(f"Measure: {measure}"),
                html.P(f"Total Data Points: {len(filtered_df)}")
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ])
    ]
    
    return summary