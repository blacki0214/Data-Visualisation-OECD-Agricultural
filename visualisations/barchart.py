import plotly.express as px
import plotly.graph_objects as go

# Import the categorizer to add category information
try:
    from utils.measure_categorizer import categorize_measure, get_category_color_map
except ImportError:
    # Fallback if import fails
    def categorize_measure(measure_code):
        return {'category': 'Other', 'subcategory': 'Unknown'}
    def get_category_color_map():
        return {}

def create_bar_chart(filtered_df, nutrient, category, year_range):
    """
    Create a bar chart comparison visualization for measure categories
    """
    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available for the selected filters",
            plot_bgcolor='rgba(38, 45, 65, 0.2)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color="#f2f2f2"),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        return fig
    
    # Get category color
    color_map = get_category_color_map()
    category_color = color_map.get(category, '#607D8B')  # Default to blue-grey
    
    # Calculate average values by country and sort
    country_avg = filtered_df.groupby('country_code')['value'].mean().reset_index()
    country_avg = country_avg.sort_values('value', ascending=False).head(10)
    
    # Get unit for title
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    unit_text = f" ({unit})" if unit else ""
    
    # Create bar chart with category-specific color
    fig = go.Figure(data=[
        go.Bar(
            x=country_avg['country_code'],
            y=country_avg['value'],
            marker_color=category_color,
            marker_line=dict(width=1, color='rgba(255, 255, 255, 0.3)'),
            hovertemplate='<b>%{x}</b><br>' +
                         f'Value: %{{y:.2f}}{unit_text}<br>' +
                         f'Category: {category}<br>' +
                         f'Nutrient: {nutrient}<br>' +
                         f'Years: {year_range[0]}-{year_range[1]}<br>' +
                         '<extra></extra>'
        )
    ])
    
    # Add title with category information
    title_text = f'{category}<br>' + \
                f'Top 10 Countries - {nutrient}{unit_text}<br>' + \
                f'<sub>Average values for {year_range[0]}-{year_range[1]} - Aggregated measures in {category}</sub>'
    
    fig.update_layout(
        title=title_text,
        xaxis_title='Country',
        yaxis_title=f'Average Value{unit_text}',
        template="plotly_dark",
        plot_bgcolor='rgba(38, 45, 65, 0.2)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="#f2f2f2"),
        margin=dict(l=40, r=20, t=100, b=40),
        showlegend=False
    )
    
    return fig