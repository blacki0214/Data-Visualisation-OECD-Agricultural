import plotly.express as px
import plotly.graph_objects as go

def create_bar_chart(filtered_df, nutrient, measure, year_range):
    """
    Create a bar chart comparison visualization
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
    
    # Calculate average values by country and sort
    country_avg = filtered_df.groupby('country_code')['value'].mean().reset_index()
    country_avg = country_avg.sort_values('value', ascending=False).head(10)
    
    # Create bar chart
    fig = px.bar(
        country_avg,
        x='country_code',
        y='value',
        title='',  # We'll handle title in the layout
        labels={'value': 'Average Value', 'country_code': 'Country'},
        color='value',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Value',
        template="plotly_dark",
        plot_bgcolor='rgba(38, 45, 65, 0.2)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="#f2f2f2"),
        margin=dict(l=40, r=20, t=10, b=40),
        coloraxis_colorbar=dict(
            title="Value",
            thickness=15,
            len=0.5,
            y=0.5
        )
    )
    
    return fig