import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_combined_chart(filtered_df, nutrient, measure):
    """
    Create a visualization that combines bar chart with line chart
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    
    Returns:
    - Plotly figure object
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
    
    # Group by year and calculate metrics
    yearly_data = filtered_df.groupby('year')['value'].agg(['mean', 'median', 'count']).reset_index()
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for average values
    fig.add_trace(
        go.Bar(
            x=yearly_data['year'],
            y=yearly_data['mean'],
            name='Average',
            marker_color='rgba(133, 92, 248, 0.7)'
        )
    )
    
    # Add line for median values
    fig.add_trace(
        go.Scatter(
            x=yearly_data['year'],
            y=yearly_data['median'],
            name='Median',
            mode='lines+markers',
            line=dict(color='#FF5757', width=3),
            marker=dict(size=8)
        )
    )
    
    # Add a trend line if there are enough data points
    if len(yearly_data) > 2:
        try:
            # Calculate trend using polynomial fit
            x = yearly_data['year']
            y = yearly_data['mean']
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            
            # Create smooth x values
            x_range = np.linspace(min(x), max(x), 100)
            
            # Add trend line
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=p(x_range),
                    mode='lines',
                    name='Trend',
                    line=dict(color='#4099ff', width=2, dash='dash')
                )
            )
        except Exception as e:
            print(f"Error creating trend line: {str(e)}")
    
    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=f'{measure} Value',
        legend_title='Metrics',
        template="plotly_dark",
        plot_bgcolor='rgba(38, 45, 65, 0.2)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="#f2f2f2"),
        margin=dict(l=40, r=20, t=10, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    return fig