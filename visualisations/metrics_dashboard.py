import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from dash import html, dcc

def create_metrics_dashboard(df, nutrient_type, measure_code, selected_year):
    """
    Create a comprehensive metrics dashboard with multiple KPIs
    
    Parameters:
    - df: DataFrame containing the data
    - nutrient_type: Selected nutrient type
    - measure_code: Selected measure code
    - selected_year: Selected year
    
    Returns:
    - Plotly figure object with subplots
    """
    # Filter data
    filtered_df = df[
        (df['nutrient_type'] == nutrient_type) & 
        (df['measure_code'] == measure_code) &
        (df['year'] == selected_year)
    ].copy()
    
    if filtered_df.empty:
        return create_empty_metrics_dashboard()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Top 10 Countries',
            'Distribution Analysis', 
            'Regional Summary',
            'Trend Indicators'
        ),
        specs=[[{"type": "bar"}, {"type": "box"}],
               [{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # 1. Top 10 Countries (Bar Chart)
    top_countries = filtered_df.nlargest(10, 'value')
    fig.add_trace(
        go.Bar(
            x=top_countries['country_code'],
            y=top_countries['value'],
            name='Top Countries',
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # 2. Distribution Analysis (Box Plot)
    fig.add_trace(
        go.Box(
            y=filtered_df['value'],
            name='Value Distribution',
            boxpoints='outliers',
            marker_color='lightgreen'
        ),
        row=1, col=2
    )
    
    # 3. Regional Summary (if region data available)
    if 'region' in filtered_df.columns:
        regional_data = filtered_df.groupby('region')['value'].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(
                x=regional_data.index,
                y=regional_data.values,
                name='Regional Averages',
                marker_color='orange'
            ),
            row=2, col=1
        )
    else:
        # Alternative: Show continent averages if available
        continent_mapping = get_continent_mapping()
        if continent_mapping:
            filtered_df['continent'] = filtered_df['country_code'].map(continent_mapping)
            continental_data = filtered_df.groupby('continent')['value'].mean().sort_values(ascending=False)
            fig.add_trace(
                go.Bar(
                    x=continental_data.index,
                    y=continental_data.values,
                    name='Continental Averages',
                    marker_color='orange'
                ),
                row=2, col=1
            )
    
    # 4. Key Metrics (Indicator)
    total_value = filtered_df['value'].sum()
    avg_value = filtered_df['value'].mean()
    max_value = filtered_df['value'].max()
    
    fig.add_trace(
        go.Indicator(
            mode="number+delta+gauge",
            value=avg_value,
            delta={'reference': max_value * 0.7},
            gauge={
                'axis': {'range': [0, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "lightgray"},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            },
            title={'text': f"Average {nutrient_type}"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        title_text=f"Metrics Dashboard - {nutrient_type} ({measure_code}) - {selected_year}",
        showlegend=False
    )
    
    return fig

def create_time_series_metrics(df, nutrient_type, measure_code, countries):
    """
    Create time series metrics showing trends over time
    
    Parameters:
    - df: DataFrame containing the data
    - nutrient_type: Selected nutrient type  
    - measure_code: Selected measure code
    - countries: List of selected countries
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['nutrient_type'] == nutrient_type) & 
        (df['measure_code'] == measure_code) &
        (df['country_code'].isin(countries))
    ].copy()
    
    if filtered_df.empty:
        return create_empty_metrics_dashboard()
    
    # Create subplots for multiple metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Individual Country Trends',
            'Year-over-Year Growth Rate',
            'Cumulative Values',
            'Volatility Analysis'
        )
    )
    
    # 1. Individual country trends
    for country in countries[:5]:  # Limit to 5 countries for readability
        country_data = filtered_df[filtered_df['country_code'] == country].sort_values('year')
        if not country_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=country_data['year'],
                    y=country_data['value'],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2)
                ),
                row=1, col=1
            )
    
    # 2. Year-over-year growth rate
    growth_data = []
    for country in countries:
        country_data = filtered_df[filtered_df['country_code'] == country].sort_values('year')
        if len(country_data) > 1:
            country_data['growth_rate'] = country_data['value'].pct_change() * 100
            growth_data.append(country_data)
    
    if growth_data:
        combined_growth = pd.concat(growth_data)
        avg_growth = combined_growth.groupby('year')['growth_rate'].mean()
        
        fig.add_trace(
            go.Scatter(
                x=avg_growth.index,
                y=avg_growth.values,
                mode='lines+markers',
                name='Avg Growth Rate',
                line=dict(color='red', width=3)
            ),
            row=1, col=2
        )
    
    # 3. Cumulative values
    yearly_totals = filtered_df.groupby('year')['value'].sum().cumsum()
    fig.add_trace(
        go.Scatter(
            x=yearly_totals.index,
            y=yearly_totals.values,
            mode='lines+markers',
            fill='tonexty',
            name='Cumulative Total',
            line=dict(color='green', width=3)
        ),
        row=2, col=1
    )
    
    # 4. Volatility (Standard deviation by year)
    yearly_volatility = filtered_df.groupby('year')['value'].std()
    fig.add_trace(
        go.Bar(
            x=yearly_volatility.index,
            y=yearly_volatility.values,
            name='Volatility',
            marker_color='purple'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text=f"Time Series Metrics - {nutrient_type} ({measure_code})",
        showlegend=True
    )
    
    return fig

def create_kpi_cards(df, nutrient_type, measure_code, selected_year):
    """
    Create KPI cards showing key metrics
    
    Parameters:
    - df: DataFrame containing the data
    - nutrient_type: Selected nutrient type
    - measure_code: Selected measure code
    - selected_year: Selected year
    
    Returns:
    - HTML Div containing KPI cards
    """
    # Filter data
    filtered_df = df[
        (df['nutrient_type'] == nutrient_type) & 
        (df['measure_code'] == measure_code) &
        (df['year'] == selected_year)
    ].copy()
    
    if filtered_df.empty:
        return html.Div("No data available for KPI calculations")
    
    # Calculate KPIs
    total_countries = len(filtered_df['country_code'].unique())
    total_value = filtered_df['value'].sum()
    avg_value = filtered_df['value'].mean()
    max_value = filtered_df['value'].max()
    min_value = filtered_df['value'].min()
    std_value = filtered_df['value'].std()
    
    # Get unit
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    
    # Create KPI cards
    kpi_cards = html.Div([
        html.Div([
            html.H3(f"{total_countries}", style={'margin': '0', 'color': '#1f77b4'}),
            html.P("Countries", style={'margin': '0', 'font-size': '14px'})
        ], className='kpi-card', style=kpi_card_style),
        
        html.Div([
            html.H3(f"{total_value:,.0f}", style={'margin': '0', 'color': '#ff7f0e'}),
            html.P(f"Total {unit}", style={'margin': '0', 'font-size': '14px'})
        ], className='kpi-card', style=kpi_card_style),
        
        html.Div([
            html.H3(f"{avg_value:,.1f}", style={'margin': '0', 'color': '#2ca02c'}),
            html.P(f"Average {unit}", style={'margin': '0', 'font-size': '14px'})
        ], className='kpi-card', style=kpi_card_style),
        
        html.Div([
            html.H3(f"{max_value:,.0f}", style={'margin': '0', 'color': '#d62728'}),
            html.P(f"Maximum {unit}", style={'margin': '0', 'font-size': '14px'})
        ], className='kpi-card', style=kpi_card_style),
        
        html.Div([
            html.H3(f"{std_value:,.1f}", style={'margin': '0', 'color': '#9467bd'}),
            html.P(f"Std Dev {unit}", style={'margin': '0', 'font-size': '14px'})
        ], className='kpi-card', style=kpi_card_style)
    ], style={'display': 'flex', 'justify-content': 'space-around', 'margin': '20px 0'})
    
    return kpi_cards

# Helper functions
def get_continent_mapping():
    """Return a simplified continent mapping for countries"""
    return {
        'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
        'DEU': 'Europe', 'FRA': 'Europe', 'GBR': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe',
        'CHN': 'Asia', 'JPN': 'Asia', 'IND': 'Asia', 'KOR': 'Asia', 'IDN': 'Asia',
        'BRA': 'South America', 'ARG': 'South America', 'CHL': 'South America',
        'AUS': 'Oceania', 'NZL': 'Oceania',
        'ZAF': 'Africa', 'EGY': 'Africa', 'NGA': 'Africa'
    }

def create_empty_metrics_dashboard():
    """Create an empty metrics dashboard"""
    fig = go.Figure()
    fig.add_annotation(
        text="No data available for metrics calculation",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        title="Metrics Dashboard",
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

# CSS style for KPI cards
kpi_card_style = {
    'border': '1px solid #ddd',
    'border-radius': '8px',
    'padding': '20px',
    'text-align': 'center',
    'background-color': '#f9f9f9',
    'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
    'width': '150px'
}
