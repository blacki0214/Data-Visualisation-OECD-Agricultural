import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.country_mapper import clean_country_codes, distribute_eu_data

def create_choropleth(df, nutrient, measure, selected_year, distribute_eu=True):
    """
    Create a choropleth map visualization
    
    Parameters:
    - df: DataFrame containing all data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    - selected_year: Selected year for visualization
    
    Returns:
    - Plotly figure object
    """
    # Check for required inputs
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
    
    # Filter data for the selected year, nutrient, and measure
    filtered = df[(df['year'] == selected_year) & 
                 (df['nutrient_type'] == nutrient) &
                 (df['measure_code'] == measure)]
    
    # Distribute EU data if requested
    if distribute_eu:
        filtered = distribute_eu_data(filtered)
    else:
        # Just remove EU entities
        filtered = filtered[~filtered['country_code'].isin(['EU', 'EU27', 'EU28', 'EU27_2020'])]
    
    # Clean other country codes
    filtered = clean_country_codes(filtered)
    
    # Check if data exists after filtering
    if filtered.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"No data available for {measure} ({nutrient}) in {selected_year}",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
    # Debug info
    print(f"Creating choropleth for {selected_year}, {nutrient}, {measure}")
    print(f"- Found {len(filtered)} rows with {filtered['country_code'].nunique()} countries")
    print(f"- Countries: {sorted(filtered['country_code'].unique())[:10]}...")
    
    # Aggregate by country - use mean for multiple values per country (in case we have duplicates)
    country_data = filtered.groupby('country_code')['value'].mean().reset_index()
    
    try:
        # Create choropleth map
        fig = px.choropleth(
            country_data,
            locations='country_code',
            color='value',
            locationmode='ISO-3',
            color_continuous_scale=px.colors.sequential.Plasma,
            title='',
            labels={'value': 'Value', 'country_code': 'Country'},
            # Add hover data
            hover_name='country_code',
            hover_data={'country_code': False, 'value': ':.2f'}
        )
        
        # Update layout for dark theme
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth',
                bgcolor='rgba(38, 45, 65, 0.2)',
                lakecolor='rgba(38, 45, 65, 0.2)',
                landcolor='rgba(60, 70, 95, 0.5)',
                showland=True,
                showlakes=True,
                showcountries=True,
                countrycolor='rgba(255, 255, 255, 0.2)',
                # Set to global scope instead of just Europe
                scope='world',
                # Center on a more balanced view
                center=dict(lon=0, lat=30),
                # Add some projection options
                projection=dict(
                    scale=1.0  # Adjust scale as needed
                )
            ),
            template="plotly_dark",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(
                title="Value",
                thickness=15,
                len=0.5,
                y=0.5
            )
        )
        
        # Add buttons to allow user to select regions
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"geo.scope": "world", 
                                   "geo.center": dict(lon=0, lat=30),
                                   "geo.projection.scale": 1.0}],
                            label="World",
                            method="relayout"
                        ),
                        dict(
                            args=[{"geo.scope": "europe",
                                   "geo.center": dict(lon=15, lat=55),
                                   "geo.projection.scale": 1.5}],
                            label="Europe",
                            method="relayout"
                        ),
                        dict(
                            args=[{"geo.scope": "asia",
                                   "geo.center": dict(lon=100, lat=35),
                                   "geo.projection.scale": 1.2}],
                            label="Asia",
                            method="relayout"
                        ),
                        dict(
                            args=[{"geo.scope": "north america",
                                   "geo.center": dict(lon=-100, lat=40),
                                   "geo.projection.scale": 1.2}],
                            label="North America",
                            method="relayout"
                        ),
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.01,
                    yanchor="bottom",
                    # Update these styling properties for better visibility
                    bgcolor="#252e3f",
                    font=dict(color="#ffffff", size=12),
                    bordercolor="#666666",  # Add a border for definition
                    borderwidth=1,
                    # Make the dropdown menu more visible
                    active=0
                ),
            ]
        )
    
    except Exception as e:
        print(f"Error creating choropleth: {str(e)}")
        fig = go.Figure()
        fig.update_layout(
            title=f"Error creating map: {str(e)}",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
    
    return fig