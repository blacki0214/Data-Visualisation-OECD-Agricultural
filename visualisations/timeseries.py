import plotly.express as px
import plotly.graph_objects as go

def create_time_series(filtered_df, nutrient, measure):
    """
    Create a time series visualization for the filtered dataset
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
    
    # Create time series plot
    fig = px.line(
        filtered_df, 
        x='year', 
        y='value', 
        color='country_code',
        markers=True,
        title='',  # We'll handle title in the layout
        labels={'value': 'Value', 'year': 'Year', 'country_code': 'Country'},
        color_discrete_sequence=px.colors.qualitative.G10
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Value',
        legend_title='Country',
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
        )
    )
    
    return fig