import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Import the categorizer to add category information
try:
    from utils.measure_categorizer import get_measure_category_mapping, get_category_color_map
except ImportError:
    # Fallback if import fails
    def get_measure_category_mapping():
        return {}
    def get_category_color_map():
        return {}

def create_measure_country_heatmap(df, selected_category, nutrient_type, selected_year=None, selected_countries=None):
    """
    Create a heatmap showing individual measures (y-axis) vs countries (x-axis)
    
    This section builds a heatmap to compare environmental measures across countries.
    Each row represents a specific measure (e.g., 'Cropland', 'Fertilisers'), and each 
    column represents a country (using ISO country codes). The color intensity reflects 
    the total value reported for that measure in that country across all available years.
    
    Parameters:
    - df: DataFrame containing the data
    - selected_category: Selected measure category
    - nutrient_type: Selected nutrient type
    - selected_year: Selected year (not used - we aggregate across all years)
    - selected_countries: List of selected country codes (optional filter)
    
    Returns:
    - Plotly figure object
    """
    try:
        # Filter by nutrient type
        filtered_df = df[df['nutrient_type'] == nutrient_type].copy()
        
        if filtered_df.empty:
            return create_empty_heatmap(f"No data available for nutrient: {nutrient_type}")
        
        # Get measure category mapping
        mapping = get_measure_category_mapping()
        if not mapping:
            return create_empty_heatmap("No measure category mapping available")
        
        # Get all measure codes for this category
        category_measures = [code for code, info in mapping.items() if info['category'] == selected_category]
        
        if not category_measures:
            return create_empty_heatmap(f"No measures found for category: {selected_category}")
        
        # Filter to only include measures from this category
        filtered_df = filtered_df[filtered_df['measure_code'].isin(category_measures)]
        
        if filtered_df.empty:
            return create_empty_heatmap(f"No data available for category: {selected_category}")
        
        # Filter by selected countries if provided
        if selected_countries:
            filtered_df = filtered_df[filtered_df['country_code'].isin(selected_countries)]
            
            if filtered_df.empty:
                return create_empty_heatmap("No data available for selected countries")
        
        # Aggregate values across ALL YEARS for each measure-country combination
        # This gives us the total value reported for each measure in each country
        agg_df = filtered_df.groupby(['measure_code', 'country_code'])['value'].sum().reset_index()
        
        if agg_df.empty:
            return create_empty_heatmap("No data to aggregate")
        
        # Create pivot table: rows = measures, columns = countries
        pivot_df = agg_df.pivot(index='measure_code', columns='country_code', values='value')
        
        # Fill NaN values with 0 for better visualization
        pivot_df = pivot_df.fillna(0)
        
        # Get unit information
        unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df.empty else ""
        unit_text = f" ({unit})" if unit else ""
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,  # Countries
            y=pivot_df.index,    # Measures
            colorscale='Viridis',
            showscale=True,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Country: %{x}<br>Total Value' + unit_text + ': %{z:.1f}<br><extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Environmental Measures vs Countries<br>{selected_category} - {nutrient_type}<br>(Total values across all years)',
            xaxis_title='Countries',
            yaxis_title='Environmental Measures',
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=150, r=50, t=100, b=50),
            height=max(400, len(pivot_df.index) * 25 + 150),
            xaxis=dict(
                tickangle=45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                tickfont=dict(size=10)
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating heatmap: {str(e)}")
        return create_empty_heatmap(f"Error creating heatmap: {str(e)}")


def create_empty_heatmap(message="No data available"):
    """Create an empty heatmap with a message"""
    fig = go.Figure()
    fig.update_layout(
        title=message,
        plot_bgcolor='rgba(38, 45, 65, 0.2)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="#f2f2f2"),
        margin=dict(l=40, r=20, t=50, b=40),
        height=400
    )
    return fig
