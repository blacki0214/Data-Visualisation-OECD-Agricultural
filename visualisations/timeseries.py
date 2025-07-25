import plotly.express as px
import plotly.graph_objects as go

def create_time_series(filtered_df, nutrient, measure):
    """
    Create a time series visualization for the filtered dataset with proper units
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
    
    # Get unit information
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    
    # Create unit-aware value label
    if unit:
        if unit == 'T':
            value_label = 'Value (Tonnes)'
        elif unit == 'KG':
            value_label = 'Value (kg)'
        elif unit == 'HA':
            value_label = 'Value (Hectares)'
        elif unit == 'T_CO2E':
            value_label = 'Value (Tonnes CO₂ equivalent)'
        elif unit == 'TOE':
            value_label = 'Value (Tonnes Oil Equivalent)'
        else:
            value_label = f'Value ({unit})'
    else:
        value_label = 'Value'
    
    # Create time series plot
    fig = px.line(
        filtered_df, 
        x='year', 
        y='value', 
        color='country_code',
        markers=True,
        title='',  # We'll handle title in the layout
        labels={'value': value_label, 'year': 'Year', 'country_code': 'Country'},
        color_discrete_sequence=px.colors.qualitative.G10
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=value_label,
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
    
    # Format y-axis based on unit
    if unit in ['T', 'T_CO2E', 'TOE']:
        fig.update_yaxes(tickformat='.2s')
    elif unit == 'HA':
        fig.update_yaxes(tickformat='.1f')
    else:
        fig.update_yaxes(tickformat='.2f')
    
    return fig