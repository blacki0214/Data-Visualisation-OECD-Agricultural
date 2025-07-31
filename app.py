from dash import Dash, Input, Output, html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import re
import os

# Import data loader - now from database
from utils.database import load_data_from_db
from utils.country_mapper import clean_country_codes

# Import layout
from components.layout import create_layout, create_basic_charts_tab, create_advanced_analytics_tab, create_metrics_dashboard_tab, create_comparative_analysis_tab

# Import visualization components
from visualisations.timeseries import create_time_series
from visualisations.choroplethMap import create_choropleth
from visualisations.barchart import create_bar_chart
from visualisations.boxplot import create_box_plot
from visualisations.scatterplot import create_scatter_plot
from visualisations.datasummary import create_data_summary
from visualisations.combined_chart import create_combined_chart

# Import new advanced visualizations
from visualisations.heatmap import create_country_year_heatmap, create_nutrient_comparison_heatmap, create_correlation_heatmap
from visualisations.metrics_dashboard import create_metrics_dashboard, create_time_series_metrics, create_kpi_cards
from visualisations.radar_chart import create_radar_chart, create_nutrient_balance_radar, create_multi_year_radar
from visualisations.sunburst_chart import create_sunburst_chart, create_nutrient_measure_sunburst, create_temporal_sunburst

# Load data from database
print("🔄 Loading data from Neon database...")
df = load_data_from_db()

if df is None:
    print("❌ Failed to load data from database!")
    # Fallback to file-based loading if database fails
    from utils.data_loader import load_data
    print("🔄 Falling back to file-based data loading...")
    df = load_data()
    
    if df is None:
        print("❌ Failed to load data from both database and files!")
        raise Exception("Could not load data from any source")
else:
    print(f"✅ Successfully loaded {len(df)} rows from database")

# Clean country codes for dropdown options
df_cleaned = clean_country_codes(df)

# Check if country codes in the data are ISO-3 compatible
def check_country_codes():
    """Check if country codes in the data are ISO-3 compatible"""
    
    # Ensure df is available and not None
    if df is None:
        print("❌ Cannot check country codes: no data available")
        return
    
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

# Call the function to check country codes (only if df was loaded successfully)
if df is not None:
    check_country_codes()

# Initialize app
app = Dash(__name__, 
           suppress_callback_exceptions=True,
           external_stylesheets=[
               'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
               'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap'
           ])

# Expose server for deployment - MUST be before the layout
server = app.server

app.layout = create_layout(df_cleaned)

# Function to filter data based on user selections
def filter_data(countries, nutrient, measure, years):
    """
    Filter data based on user selections, with country code cleaning
    """
    if df is None:
        print("❌ No data available for filtering")
        return pd.DataFrame()  # Return empty DataFrame
        
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
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient, and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
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
        fig = go.Figure()
        fig.update_layout(
            title="Please select nutrient and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
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
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient, and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
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

# Tab Content Callback
@app.callback(
    Output('tab-content', 'children'),
    [Input('visualization-tabs', 'value')]
)
def update_tab_content(selected_tab):
    if selected_tab == 'basic-tab':
        return create_basic_charts_tab(df)
    elif selected_tab == 'advanced-tab':
        return create_advanced_analytics_tab(df)
    elif selected_tab == 'metrics-tab':
        return create_metrics_dashboard_tab(df)
    elif selected_tab == 'comparative-tab':
        return create_comparative_analysis_tab(df)
    else:
        return create_basic_charts_tab(df)

# New Visualization Callbacks

# Country-Year Heatmap Callback
@app.callback(
    Output('country-year-heatmap', 'figure'),
    [Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_country_year_heatmap(nutrient, measure):
    if not nutrient or not measure:
        fig = go.Figure()
        fig.update_layout(
            title="Please select nutrient and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    return create_country_year_heatmap(df, nutrient, measure)

# Correlation Heatmap Callback
@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_correlation_heatmap(countries, years):
    if not countries or not years:
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries and years",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    return create_correlation_heatmap(df, countries, list(range(years[0], years[1] + 1)))

# Radar Chart Callback
@app.callback(
    Output('radar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('map-year-dropdown', 'value')]  # Use map-year-dropdown for single year selection
)
def update_radar_chart(countries, year):
    if not countries or not year:
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries and year",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    # Limit to 5 countries for readability
    limited_countries = countries[:5] if len(countries) > 5 else countries
    return create_radar_chart(df, limited_countries, year)

# Sunburst Chart Callback
@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('map-year-dropdown', 'value')]  # Use single year for sunburst
)
def update_sunburst_chart(year):
    if not year:
        fig = go.Figure()
        fig.update_layout(
            title="Please select a year",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    return create_sunburst_chart(df, year)

# Metrics Dashboard Callback
@app.callback(
    Output('metrics-dashboard', 'figure'),
    [Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('map-year-dropdown', 'value')]
)
def update_metrics_dashboard(nutrient, measure, year):
    if not nutrient or not measure or not year:
        fig = go.Figure()
        fig.update_layout(
            title="Please select nutrient, measure, and year",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    return create_metrics_dashboard(df, nutrient, measure, year)

# Time Series Metrics Callback
@app.callback(
    Output('time-series-metrics', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_time_series_metrics(countries, nutrient, measure):
    if not countries or not nutrient or not measure:
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient, and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    # Limit to 5 countries for readability
    limited_countries = countries[:5] if len(countries) > 5 else countries
    return create_time_series_metrics(df, nutrient, measure, limited_countries)

# KPI Cards Callback
@app.callback(
    Output('kpi-cards', 'children'),
    [Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('map-year-dropdown', 'value')]
)
def update_kpi_cards(nutrient, measure, year):
    if not nutrient or not measure or not year:
        return html.Div("Please select nutrient, measure, and year")
    return create_kpi_cards(df, nutrient, measure, year)

# Box Plot Callback (update ID to match new layout)
@app.callback(
    Output('box-plot-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_box_plot_chart(countries, nutrient, measure, years):
    if not countries or not nutrient or not measure:
        fig = go.Figure()
        fig.update_layout(
            title="Please select countries, nutrient, and measure",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
    filtered = filter_data(countries, nutrient, measure, years)
    return create_box_plot(filtered, nutrient, measure)

# Add this before running the app
print(f"Data summary:")
print(f"- Total rows: {len(df)}")
print(f"- Years: {sorted(df['year'].unique())}")
print(f"- Countries: {len(df['country_code'].unique())}")
print(f"- Nutrients: {df['nutrient_type'].unique()}")
print(f"- Measures: {df['measure_code'].unique()}")

# Sample data for choropleth visualization
# Find a combination that actually has data
sample_combinations = df.groupby(['year', 'nutrient_type', 'measure_code']).size().reset_index(name='count')
sample_combinations = sample_combinations.sort_values('count', ascending=False)

if not sample_combinations.empty:
    sample_year = sample_combinations.iloc[0]['year']
    sample_nutrient = sample_combinations.iloc[0]['nutrient_type']
    sample_measure = sample_combinations.iloc[0]['measure_code']
    
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
else:
    print("\nNo valid combinations found in the data")

# Add client-side callback to reset scroll position when tabs change (visualization sections only)
app.clientside_callback(
    """
    function(selected_tab) {
        // Reset scroll position to top when tab changes (only for visualization sections)
        setTimeout(function() {
            // Reset scrollable sections within tabs (visualization areas only)
            var scrollableSections = document.querySelectorAll('.scrollable-section');
            scrollableSections.forEach(function(section) {
                section.scrollTop = 0;
            });
            
            // Reset chart containers scroll
            var chartContainers = document.querySelectorAll('.chart-container');
            chartContainers.forEach(function(container) {
                container.scrollTop = 0;
            });
            
            // Reset tab content scroll
            var tabContent = document.getElementById('tab-content');
            if (tabContent) {
                tabContent.scrollTop = 0;
            }
        }, 100); // Small delay to ensure DOM is updated
        
        return selected_tab; // Return the selected tab value
    }
    """,
    Output('scroll-reset-trigger', 'children'),  # We'll use a hidden div for this
    Input('visualization-tabs', 'value')
)

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
