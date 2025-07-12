from dash import Dash, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import re

# Import data loader
from utils.data_loader import load_data
from utils.country_mapper import clean_country_codes

# Import layout
from components.layout import create_layout

# Import visualization components
from visualisations.timeseries import create_time_series
from visualisations.choroplethMap import create_choropleth
from visualisations.barchart import create_bar_chart
from visualisations.boxplot import create_box_plot
from visualisations.scatterplot import create_scatter_plot
from visualisations.datasummary import create_data_summary
from visualisations.combined_chart import create_combined_chart

# Load data
df = load_data()

# Clean country codes for dropdown options
df_cleaned = clean_country_codes(df)

# Check if country codes in the data are ISO-3 compatible
def check_country_codes():
    """Check if country codes in the data are ISO-3 compatible"""
    
    iso_3_pattern = r'^[A-Z]{3}$'  # ISO-3 country codes are 3 uppercase letters
    
    # Get unique country codes
    country_codes = df['country_code'].unique()
    
    # Check if they match the pattern
    valid_codes = [code for code in country_codes if re.match(iso_3_pattern, code)]
    invalid_codes = [code for code in country_codes if not re.match(iso_3_pattern, code)]
    
    print(f"Valid ISO-3 country codes: {len(valid_codes)} out of {len(country_codes)}")
    
    if invalid_codes:
        print(f"Warning: Found {len(invalid_codes)} invalid country codes: {invalid_codes[:10]}")
        print("These may cause issues with the choropleth map.")

# Call the function to check country codes
check_country_codes()

# Initialize app
app = Dash(__name__, 
           suppress_callback_exceptions=True,
           external_stylesheets=[
               'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
               'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap'
           ])
app.layout = create_layout(df_cleaned)

# Function to filter data based on user selections
def filter_data(countries, nutrient, measure, years):
    """
    Filter data based on user selections, with country code cleaning
    """
    filtered = df.copy()
    
    if countries:
        filtered = filtered[filtered['country_code'].isin(countries)]
    
    if nutrient:
        filtered = filtered[filtered['nutrient_type'] == nutrient]
        
    if measure:
        filtered = filtered[filtered['measure_code'] == measure]
    
    if years:
        filtered = filtered[(filtered['year'] >= years[0]) & (filtered['year'] <= years[1])]
    
    # Clean country codes for choropleth compatibility
    filtered = clean_country_codes(filtered)
        
    return filtered

# Time Series Chart Callback
@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_time_series(countries, nutrient, measure, years):
    if not countries or not nutrient or not measure:
        return {}
    
    filtered = filter_data(countries, nutrient, measure, years)
    return create_time_series(filtered, nutrient, measure)

# Choropleth Map Callback
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('map-year-dropdown', 'value'),
     Input('eu-data-option', 'value')]
)
def update_choropleth(nutrient, measure, selected_year, eu_option):
    if not nutrient or not measure or not selected_year:
        fig = go.Figure()
        fig.update_layout(
            title="Please select nutrient, measure, and year",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
    # Add debug print
    print(f"Choropleth callback: nutrient={nutrient}, measure={measure}, year={selected_year}, eu_option={eu_option}")
    
    # Use a flag to indicate whether to distribute EU data
    distribute_eu = (eu_option == 'distribute')
    
    return create_choropleth(df, nutrient, measure, selected_year, distribute_eu)

# Bar Chart Callback
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_bar_chart(nutrient, measure, years):
    if not nutrient or not measure:
        return {}
    
    filtered = filter_data(None, nutrient, measure, years)
    return create_bar_chart(filtered, nutrient, measure, years)

# Box Plot Callback
@app.callback(
    Output('box-plot', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_box_plot(countries, nutrient, measure, years):
    if not countries or not nutrient or not measure:
        return {}
    
    filtered = filter_data(countries, nutrient, measure, years)
    return create_box_plot(filtered, nutrient, measure)

# Scatter Chart Callback
@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('x-axis-dropdown', 'value')]
)
def update_scatter_chart(countries, nutrient, measure, years, x_axis):
    # Handle empty selections
    if not countries or not nutrient or not measure or not years:
        # Return an empty figure with a message
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient, measure and years",
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_white"
        )
        return fig
    
    # Filter data
    filtered = filter_data(countries, nutrient, measure, years)
    
    # Return the scatter plot
    return create_scatter_plot(filtered, nutrient, measure, x_axis)

# Combined Chart Callback
@app.callback(
    Output('combined-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_combined_chart(countries, nutrient, measure, years):
    if not countries or not nutrient or not measure:
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
    # Filter data
    filtered = filter_data(countries, nutrient, measure, years)
    
    # Debug info
    print(f"Combined chart: {len(filtered)} rows, {filtered['country_code'].nunique()} countries")
    
    # Return the combined chart
    return create_combined_chart(filtered, nutrient, measure)

# Data Table Callback
@app.callback(
    Output('data-table', 'data'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_table(countries, nutrient, measure, years):
    filtered = filter_data(countries, nutrient, measure, years)
    return filtered.to_dict('records')

# Data Summary Callback
@app.callback(
    Output('data-summary', 'children'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_summary(countries, nutrient, measure, years):
    filtered = filter_data(countries, nutrient, measure, years)
    return create_data_summary(filtered, nutrient, measure)

# Add this before running the app
print(f"Data summary:")
print(f"- Total rows: {len(df)}")
print(f"- Years: {sorted(df['year'].unique())}")
print(f"- Countries: {len(df['country_code'].unique())}")
print(f"- Nutrients: {df['nutrient_type'].unique()}")
print(f"- Measures: {df['measure_code'].unique()}")

# Sample data for choropleth visualization
sample_year = df['year'].max()
sample_nutrient = df['nutrient_type'].iloc[0]
sample_measure = df['measure_code'].iloc[0]

sample_data = df[
    (df['year'] == sample_year) & 
    (df['nutrient_type'] == sample_nutrient) &
    (df['measure_code'] == sample_measure)
]

print(f"\nSample data for choropleth ({sample_year}, {sample_nutrient}, {sample_measure}):")
print(f"- Rows: {len(sample_data)}")
print(f"- Countries: {sample_data['country_code'].nunique()}")
if not sample_data.empty:
    print(f"- Sample: {sample_data[['country_code', 'value']].head(3).to_dict('records')}")
else:
    print("- No data found for this combination")

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8050)
