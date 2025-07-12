import plotly.express as px
import plotly.graph_objects as go

def create_box_plot(filtered_df, nutrient, measure):
    """
    Create a box plot visualization
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    
    Returns:
    - Plotly figure object
    """
    if filtered_df.empty:
        return go.Figure().update_layout(title="No data available for the selected filters")
    
    # Create box plot
    fig = px.box(
        filtered_df,
        x='country_code',
        y='value',
        color='country_code',
        title=f'Distribution of {measure} for {nutrient} by Country',
        labels={'value': 'Value', 'country_code': 'Country'},
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Value',
        template='plotly_white',
        showlegend=False,  # Hide legend as it's redundant with x-axis
        xaxis={'categoryorder': 'mean descending'}  # Order by mean value
    )
    
    return fig