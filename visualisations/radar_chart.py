import plotly.graph_objs as go
import pandas as pd
import numpy as np
import math

def create_radar_chart(df, countries, year, nutrients=None):
    """
    Create a radar chart comparing countries across multiple nutrients/measures
    
    Parameters:
    - df: DataFrame containing the data
    - countries: List of country codes to compare
    - year: Selected year
    - nutrients: List of nutrients to include (if None, uses top nutrients)
    
    Returns:
    - Plotly figure object
    """
    # Filter data for selected year
    filtered_df = df[df['year'] == year].copy()
    
    if filtered_df.empty:
        return create_empty_radar_chart("No data available for selected year")
    
    # If nutrients not specified, get the most common ones
    if nutrients is None:
        nutrient_counts = filtered_df['nutrient_type'].value_counts()
        nutrients = nutrient_counts.head(6).index.tolist()  # Top 6 nutrients
    
    # Create nutrient-measure combinations for comprehensive analysis
    filtered_df['nutrient_measure'] = filtered_df['nutrient_type'] + '_' + filtered_df['measure_code']
    
    # Get the most common measures for each nutrient
    radar_metrics = []
    for nutrient in nutrients:
        nutrient_data = filtered_df[filtered_df['nutrient_type'] == nutrient]
        if not nutrient_data.empty:
            # Get the most common measure for this nutrient
            top_measure = nutrient_data['measure_code'].value_counts().index[0]
            radar_metrics.append(f"{nutrient}_{top_measure}")
    
    if not radar_metrics:
        return create_empty_radar_chart("No suitable metrics found")
    
    # Create pivot table
    pivot_df = filtered_df.pivot_table(
        values='value',
        index='country_code',
        columns='nutrient_measure',
        aggfunc='mean'
    )
    
    # Filter to include only our radar metrics and selected countries
    available_metrics = [m for m in radar_metrics if m in pivot_df.columns]
    available_countries = [c for c in countries if c in pivot_df.index]
    
    if not available_metrics or not available_countries:
        return create_empty_radar_chart("No data available for selected countries and metrics")
    
    radar_data = pivot_df.loc[available_countries, available_metrics]
    
    # Normalize data (0-1 scale) for better radar chart visualization
    radar_data_norm = radar_data.div(radar_data.max(axis=0), axis=1).fillna(0)
    
    # Create radar chart
    fig = go.Figure()
    
    # Color palette for countries
    colors = ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 
              'rgba(255, 205, 86, 0.6)', 'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)']
    
    for idx, country in enumerate(available_countries):
        values = radar_data_norm.loc[country].values.tolist()
        # Close the radar chart by adding the first value at the end
        values_closed = values + [values[0]]
        metrics_closed = available_metrics + [available_metrics[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=metrics_closed,
            fill='toself',
            fillcolor=colors[idx % len(colors)],
            line=dict(color=colors[idx % len(colors)].replace('0.6', '1.0')),
            name=country,
            hovertemplate=f'<b>{country}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickmode='linear',
                tick0=0,
                dtick=0.2,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        title=f"Country Comparison Radar Chart - {year}<br>" +
              '<sub>Each axis represents a different metric (normalized 0-1). Larger areas indicate better overall performance.</sub>',
        height=600,
        font=dict(size=12),
        margin=dict(l=50, r=50, t=100, b=50),
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                xref='paper',
                yref='paper',
                text='💡 Tip: Values are normalized (0-1 scale) for comparison. Hover over lines to see details.',
                showarrow=False,
                font=dict(size=10, color='gray'),
                xanchor='center'
            )
        ]
    )
    
    return fig

def create_nutrient_balance_radar(df, country, year):
    """
    Create a radar chart showing nutrient balance for a specific country
    
    Parameters:
    - df: DataFrame containing the data
    - country: Country code
    - year: Selected year
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['country_code'] == country) & 
        (df['year'] == year)
    ].copy()
    
    if filtered_df.empty:
        return create_empty_radar_chart(f"No data available for {country} in {year}")
    
    # Group by nutrient and get average values
    nutrient_data = filtered_df.groupby('nutrient_type')['value'].mean().reset_index()
    
    if len(nutrient_data) < 3:
        return create_empty_radar_chart("Insufficient nutrients for radar chart")
    
    # Normalize values for radar chart
    max_val = nutrient_data['value'].max()
    min_val = nutrient_data['value'].min()
    nutrient_data['normalized'] = (nutrient_data['value'] - min_val) / (max_val - min_val) if max_val > min_val else 0.5
    
    # Create radar chart
    values = nutrient_data['normalized'].tolist()
    nutrients = nutrient_data['nutrient_type'].tolist()
    
    # Close the radar chart
    values_closed = values + [values[0]]
    nutrients_closed = nutrients + [nutrients[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=nutrients_closed,
        fill='toself',
        fillcolor='rgba(54, 162, 235, 0.3)',
        line=dict(color='rgba(54, 162, 235, 1.0)', width=2),
        name=country,
        hovertemplate=f'<b>{country}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickmode='linear',
                tick0=0,
                dtick=0.2
            )
        ),
        showlegend=False,
        title=f"Nutrient Balance - {country} ({year})",
        height=500
    )
    
    return fig

def create_multi_year_radar(df, country, nutrient_type, measure_code):
    """
    Create a radar chart showing evolution over multiple years for a country
    
    Parameters:
    - df: DataFrame containing the data
    - country: Country code
    - nutrient_type: Selected nutrient type
    - measure_code: Selected measure code
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    filtered_df = df[
        (df['country_code'] == country) & 
        (df['nutrient_type'] == nutrient_type) &
        (df['measure_code'] == measure_code)
    ].copy()
    
    if filtered_df.empty:
        return create_empty_radar_chart("No data available for selected filters")
    
    # Get available years (limit to reasonable number for radar chart)
    years = sorted(filtered_df['year'].unique())
    if len(years) > 8:
        # Take every nth year to keep radar readable
        step = len(years) // 8
        years = years[::step]
    
    # Create year-based data
    year_data = []
    for year in years:
        year_value = filtered_df[filtered_df['year'] == year]['value'].iloc[0] if len(filtered_df[filtered_df['year'] == year]) > 0 else 0
        year_data.append(year_value)
    
    # Normalize for radar chart
    if max(year_data) > min(year_data):
        normalized_data = [(val - min(year_data)) / (max(year_data) - min(year_data)) for val in year_data]
    else:
        normalized_data = [0.5] * len(year_data)
    
    # Close the radar chart
    values_closed = normalized_data + [normalized_data[0]]
    years_closed = [str(y) for y in years] + [str(years[0])]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=years_closed,
        fill='toself',
        fillcolor='rgba(255, 99, 132, 0.3)',
        line=dict(color='rgba(255, 99, 132, 1.0)', width=2),
        name=f"{country} - {nutrient_type}",
        hovertemplate=f'<b>{country}</b><br>Year %{{theta}}: %{{r:.2f}}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickmode='linear',
                tick0=0,
                dtick=0.2
            )
        ),
        showlegend=False,
        title=f"Temporal Evolution - {country} ({nutrient_type} - {measure_code})",
        height=500
    )
    
    return fig

def create_empty_radar_chart(message):
    """Create an empty radar chart with a message"""
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
        title="Radar Chart",
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig
