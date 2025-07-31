import plotly.graph_objs as go
import pandas as pd
import numpy as np

def create_sunburst_chart(df, selected_year):
    """
    Create a sunburst chart showing hierarchical breakdown of nutrients by region/country
    
    Parameters:
    - df: DataFrame containing the data
    - selected_year: Selected year for analysis
    
    Returns:
    - Plotly figure object
    """
    # Filter data for selected year
    filtered_df = df[df['year'] == selected_year].copy()
    
    if filtered_df.empty:
        return create_empty_sunburst("No data available for selected year")
    
    # Add continent information
    continent_mapping = get_continent_mapping()
    filtered_df['continent'] = filtered_df['country_code'].map(continent_mapping)
    filtered_df['continent'] = filtered_df['continent'].fillna('Other')
    
    # Create hierarchical structure: Continent -> Country -> Nutrient Type
    hierarchical_data = []
    
    # Level 1: Continents
    continent_totals = filtered_df.groupby('continent')['value'].sum().reset_index()
    
    # Level 2: Countries within continents
    country_data = filtered_df.groupby(['continent', 'country_code'])['value'].sum().reset_index()
    
    # Level 3: Nutrients within countries
    nutrient_data = filtered_df.groupby(['continent', 'country_code', 'nutrient_type'])['value'].sum().reset_index()
    
    # Prepare data for sunburst
    ids = []
    labels = []
    parents = []
    values = []
    
    # Add root
    ids.append("World")
    labels.append("World")
    parents.append("")
    values.append(filtered_df['value'].sum())
    
    # Add continents
    for _, row in continent_totals.iterrows():
        continent = row['continent']
        ids.append(continent)
        labels.append(continent)
        parents.append("World")
        values.append(row['value'])
    
    # Add countries (limit to top countries per continent to avoid overcrowding)
    for continent in continent_totals['continent'].unique():
        continent_countries = country_data[country_data['continent'] == continent].nlargest(5, 'value')
        for _, row in continent_countries.iterrows():
            country_id = f"{continent}-{row['country_code']}"
            ids.append(country_id)
            labels.append(row['country_code'])
            parents.append(continent)
            values.append(row['value'])
    
    # Add nutrients (limit to top nutrients per country)
    for continent in continent_totals['continent'].unique():
        continent_countries = country_data[country_data['continent'] == continent].nlargest(5, 'value')
        for _, country_row in continent_countries.iterrows():
            country_id = f"{continent}-{country_row['country_code']}"
            country_nutrients = nutrient_data[
                (nutrient_data['continent'] == continent) & 
                (nutrient_data['country_code'] == country_row['country_code'])
            ].nlargest(3, 'value')  # Top 3 nutrients per country
            
            for _, nutrient_row in country_nutrients.iterrows():
                nutrient_id = f"{country_id}-{nutrient_row['nutrient_type']}"
                ids.append(nutrient_id)
                labels.append(nutrient_row['nutrient_type'])
                parents.append(country_id)
                values.append(nutrient_row['value'])
    
    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f}<br>Percentage: %{percentParent}<extra></extra>',
        maxdepth=3,
    ))
    
    fig.update_layout(
        title=f"Agricultural Data Hierarchy - {selected_year}<br>" +
              '<sub>Click segments to drill down: World → Continents → Countries → Nutrients</sub>',
        height=600,
        font=dict(size=12),
        margin=dict(l=20, r=20, t=100, b=50),
        annotations=[
            dict(
                x=0.5,
                y=-0.05,
                xref='paper',
                yref='paper',
                text='💡 Tip: Click on segments to zoom in and explore the hierarchy. Hover for details.',
                showarrow=False,
                font=dict(size=10, color='gray'),
                xanchor='center'
            )
        ]
    )
    
    return fig

def create_nutrient_measure_sunburst(df, selected_countries, selected_year):
    """
    Create a sunburst chart showing nutrient-measure breakdown for selected countries
    
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
        return create_empty_sunburst("No data available for selected filters")
    
    # Create hierarchical structure: Country -> Nutrient -> Measure
    ids = ["Root"]
    labels = ["Agricultural Data"]
    parents = [""]
    values = [filtered_df['value'].sum()]
    
    # Add countries
    country_totals = filtered_df.groupby('country_code')['value'].sum().reset_index()
    for _, row in country_totals.iterrows():
        country = row['country_code']
        ids.append(country)
        labels.append(country)
        parents.append("Root")
        values.append(row['value'])
    
    # Add nutrients within countries
    nutrient_data = filtered_df.groupby(['country_code', 'nutrient_type'])['value'].sum().reset_index()
    for _, row in nutrient_data.iterrows():
        nutrient_id = f"{row['country_code']}-{row['nutrient_type']}"
        ids.append(nutrient_id)
        labels.append(row['nutrient_type'])
        parents.append(row['country_code'])
        values.append(row['value'])
    
    # Add measures within nutrients (limit to avoid overcrowding)
    measure_data = filtered_df.groupby(['country_code', 'nutrient_type', 'measure_code'])['value'].sum().reset_index()
    for _, row in measure_data.iterrows():
        # Only add if value is significant (top measures)
        nutrient_total = nutrient_data[
            (nutrient_data['country_code'] == row['country_code']) & 
            (nutrient_data['nutrient_type'] == row['nutrient_type'])
        ]['value'].iloc[0]
        
        if row['value'] / nutrient_total > 0.1:  # Only show measures that are >10% of nutrient total
            measure_id = f"{row['country_code']}-{row['nutrient_type']}-{row['measure_code']}"
            parent_id = f"{row['country_code']}-{row['nutrient_type']}"
            ids.append(measure_id)
            labels.append(row['measure_code'])
            parents.append(parent_id)
            values.append(row['value'])
    
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f}<br>Percentage: %{percentParent}<extra></extra>',
        maxdepth=4,
    ))
    
    fig.update_layout(
        title=f"Nutrient-Measure Breakdown - {selected_year}",
        height=600,
        font=dict(size=12)
    )
    
    return fig

def create_temporal_sunburst(df, nutrient_type, measure_code):
    """
    Create a sunburst chart showing temporal evolution of data
    
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
        return create_empty_sunburst("No data available for selected filters")
    
    # Create decade groupings for temporal analysis
    filtered_df['decade'] = (filtered_df['year'] // 10) * 10
    filtered_df['decade_label'] = filtered_df['decade'].astype(str) + 's'
    
    # Add continent information
    continent_mapping = get_continent_mapping()
    filtered_df['continent'] = filtered_df['country_code'].map(continent_mapping)
    filtered_df['continent'] = filtered_df['continent'].fillna('Other')
    
    # Create hierarchical structure: Decade -> Continent -> Country
    ids = ["Root"]
    labels = [f"{nutrient_type} - {measure_code}"]
    parents = [""]
    values = [filtered_df['value'].sum()]
    
    # Add decades
    decade_totals = filtered_df.groupby('decade_label')['value'].sum().reset_index()
    for _, row in decade_totals.iterrows():
        decade = row['decade_label']
        ids.append(decade)
        labels.append(decade)
        parents.append("Root")
        values.append(row['value'])
    
    # Add continents within decades
    continent_data = filtered_df.groupby(['decade_label', 'continent'])['value'].sum().reset_index()
    for _, row in continent_data.iterrows():
        continent_id = f"{row['decade_label']}-{row['continent']}"
        ids.append(continent_id)
        labels.append(row['continent'])
        parents.append(row['decade_label'])
        values.append(row['value'])
    
    # Add top countries within continents (limit to avoid overcrowding)
    country_data = filtered_df.groupby(['decade_label', 'continent', 'country_code'])['value'].sum().reset_index()
    for decade in decade_totals['decade_label']:
        for continent in continent_data[continent_data['decade_label'] == decade]['continent'].unique():
            continent_countries = country_data[
                (country_data['decade_label'] == decade) & 
                (country_data['continent'] == continent)
            ].nlargest(3, 'value')  # Top 3 countries per continent per decade
            
            parent_id = f"{decade}-{continent}"
            for _, row in continent_countries.iterrows():
                country_id = f"{parent_id}-{row['country_code']}"
                ids.append(country_id)
                labels.append(row['country_code'])
                parents.append(parent_id)
                values.append(row['value'])
    
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f}<br>Percentage: %{percentParent}<extra></extra>',
        maxdepth=4,
    ))
    
    fig.update_layout(
        title=f"Temporal Evolution - {nutrient_type} ({measure_code})",
        height=600,
        font=dict(size=12)
    )
    
    return fig

def get_continent_mapping():
    """Extended continent mapping for more countries"""
    return {
        # North America
        'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
        
        # Europe  
        'DEU': 'Europe', 'FRA': 'Europe', 'GBR': 'Europe', 'ITA': 'Europe', 
        'ESP': 'Europe', 'POL': 'Europe', 'NLD': 'Europe', 'BEL': 'Europe',
        'AUT': 'Europe', 'CHE': 'Europe', 'CZE': 'Europe', 'DNK': 'Europe',
        'FIN': 'Europe', 'GRC': 'Europe', 'HUN': 'Europe', 'IRL': 'Europe',
        'NOR': 'Europe', 'PRT': 'Europe', 'SVK': 'Europe', 'SVN': 'Europe',
        'SWE': 'Europe', 'TUR': 'Europe',
        
        # Asia
        'CHN': 'Asia', 'JPN': 'Asia', 'IND': 'Asia', 'KOR': 'Asia', 
        'IDN': 'Asia', 'THA': 'Asia', 'VNM': 'Asia', 'MYS': 'Asia',
        'SGP': 'Asia', 'PHL': 'Asia', 'BGD': 'Asia', 'PAK': 'Asia',
        'LKA': 'Asia', 'IRN': 'Asia', 'IRQ': 'Asia', 'ISR': 'Asia',
        
        # South America
        'BRA': 'South America', 'ARG': 'South America', 'CHL': 'South America',
        'COL': 'South America', 'PER': 'South America', 'VEN': 'South America',
        'ECU': 'South America', 'URY': 'South America', 'PRY': 'South America',
        
        # Oceania
        'AUS': 'Oceania', 'NZL': 'Oceania',
        
        # Africa
        'ZAF': 'Africa', 'EGY': 'Africa', 'NGA': 'Africa', 'KEN': 'Africa',
        'GHA': 'Africa', 'ETH': 'Africa', 'MAR': 'Africa', 'TUN': 'Africa',
        'DZA': 'Africa', 'LBY': 'Africa'
    }

def create_empty_sunburst(message):
    """Create an empty sunburst chart with a message"""
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
        title="Sunburst Chart",
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig
