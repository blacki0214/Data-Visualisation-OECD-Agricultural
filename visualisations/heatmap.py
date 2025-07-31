import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

def create_country_year_heatmap(df, nutrient_type, measure_code):
    """
    Create a heatmap showing values across countries and years
    
    Parameters:
    - df: DataFrame containing the data
    - nutrient_type: Selected nutrient type
    - measure_code: Selected measure code
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['nutrient_type'] == nutrient_type) & 
        (df['measure_code'] == measure_code)
    ].copy()
    
    if filtered_df.empty:
        return create_empty_heatmap("No data available for selected filters")
    
    # Create pivot table for heatmap
    pivot_df = filtered_df.pivot_table(
        values='value', 
        index='country_code', 
        columns='year', 
        aggfunc='mean'
    )
    
    # Sort countries by total values (descending)
    country_totals = pivot_df.sum(axis=1).sort_values(ascending=False)
    pivot_df = pivot_df.reindex(country_totals.index)
    
    # Get unit for title
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    unit_text = f" ({unit})" if unit else ""
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis',
        showscale=True,
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>' +
                     'Year: %{x}<br>' +
                     'Value: %{z:.2f}' + unit_text + '<br>' +
                     '<i>Darker colors = Higher values</i>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{nutrient_type} - {measure_code} Heatmap{unit_text}<br>' +
              '<sub>Compare values across countries and years - darker colors indicate higher values</sub>',
        xaxis_title='Year',
        yaxis_title='Country',
        height=max(400, len(pivot_df) * 20),  # Dynamic height based on number of countries
        font=dict(size=12),
        margin=dict(l=100, r=50, t=100, b=50),
        annotations=[
            dict(
                x=0.5,
                y=-0.15,
                xref='paper',
                yref='paper',
                text='💡 Tip: Hover over cells to see exact values. Countries are sorted by total values (highest first).',
                showarrow=False,
                font=dict(size=10, color='gray'),
                xanchor='center'
            )
        ]
    )
    
    return fig

def create_nutrient_comparison_heatmap(df, selected_countries, selected_year):
    """
    Create a heatmap comparing different nutrients across selected countries
    
    Parameters:
    - df: DataFrame containing the data
    - selected_countries: List of selected country codes
    - selected_year: Selected year
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['country_code'].isin(selected_countries)) & 
        (df['year'] == selected_year)
    ].copy()
    
    if filtered_df.empty:
        return create_empty_heatmap("No data available for selected filters")
    
    # Create a comprehensive nutrient-measure combination
    filtered_df['nutrient_measure'] = filtered_df['nutrient_type'] + ' - ' + filtered_df['measure_code']
    
    # Create pivot table
    pivot_df = filtered_df.pivot_table(
        values='value',
        index='nutrient_measure',
        columns='country_code',
        aggfunc='mean'
    )
    
    # Remove rows/columns with all NaN values
    pivot_df = pivot_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
    
    if pivot_df.empty:
        return create_empty_heatmap("No data available after filtering")
    
    # Normalize data for better visualization (z-score normalization)
    pivot_normalized = pivot_df.apply(lambda x: (x - x.mean()) / x.std() if x.std() > 0 else x, axis=1)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_normalized.values,
        x=pivot_normalized.columns,
        y=pivot_normalized.index,
        colorscale='RdBu_r',
        zmid=0,
        showscale=True,
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>Country: %{x}<br>Normalized Value: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Nutrient Comparison Heatmap - {selected_year} (Normalized)',
        xaxis_title='Country',
        yaxis_title='Nutrient - Measure',
        height=max(500, len(pivot_normalized) * 25),
        font=dict(size=12),
        margin=dict(l=200, r=50, t=80, b=50)
    )
    
    return fig

def create_correlation_heatmap(df, selected_countries, selected_years):
    """
    Create a correlation heatmap between different nutrients/measures
    
    Parameters:
    - df: DataFrame containing the data
    - selected_countries: List of selected country codes
    - selected_years: List of selected years
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['country_code'].isin(selected_countries)) & 
        (df['year'].isin(selected_years))
    ].copy()
    
    if filtered_df.empty:
        return create_empty_heatmap("No data available for selected filters")
    
    # Create nutrient-measure combinations
    filtered_df['nutrient_measure'] = filtered_df['nutrient_type'] + ' - ' + filtered_df['measure_code']
    
    # Create pivot table for correlation analysis
    pivot_df = filtered_df.pivot_table(
        values='value',
        index=['country_code', 'year'],
        columns='nutrient_measure',
        aggfunc='mean'
    )
    
    # Calculate correlation matrix
    corr_matrix = pivot_df.corr()
    
    # Create correlation heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        showscale=True,
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>vs<br><b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Nutrient-Measure Correlation Matrix',
        xaxis_title='Nutrient - Measure',
        yaxis_title='Nutrient - Measure',
        height=max(600, len(corr_matrix) * 25),
        font=dict(size=10),
        margin=dict(l=200, r=50, t=80, b=200),
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_empty_heatmap(message):
    """Create an empty heatmap with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        title="Heatmap",
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig
