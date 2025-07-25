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
    
    # Get unit information for meaningful labels
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
    
    # Get measure description for title
    measure_desc = filtered_df['Measure'].iloc[0] if 'Measure' in filtered_df.columns else measure
    
    # Create figure
    fig = go.Figure()
    
    # Format values based on unit for better readability
    def format_value(val, unit_type):
        if pd.isna(val):
            return "N/A"
        
        if unit_type in ['T', 'T_CO2E', 'TOE']:
            # For tonnes, show with appropriate decimal places
            if val >= 1000000:
                return f"{val/1000000:.2f}M"
            elif val >= 1000:
                return f"{val/1000:.1f}K"
            else:
                return f"{val:.2f}"
        elif unit_type == 'HA':
            # For hectares
            if val >= 1000000:
                return f"{val/1000000:.2f}M"
            elif val >= 1000:
                return f"{val/1000:.1f}K"
            else:
                return f"{val:.1f}"
        elif unit_type == 'KG':
            # For kilograms
            if val >= 1000:
                return f"{val/1000:.2f}T"
            else:
                return f"{val:.2f}"
        else:
            return f"{val:.2f}"
    
    # Add bars for average values
    fig.add_trace(
        go.Bar(
            x=yearly_data['year'],
            y=yearly_data['mean'],
            name='Average',
            marker_color='rgba(133, 92, 248, 0.7)',
            hovertemplate='<b><span style="color:#f2f2f2">Average</span></b><br>' +
                         '<span style="color:#f2f2f2">Year: %{x}</span><br>' +
                         f'<span style="color:#f2f2f2">{value_label}: %{{y:.2f}}</span><br>' +
                         '<extra></extra>',
            # Add custom hover text with formatted values
            customdata=[format_value(val, unit) for val in yearly_data['mean']],
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
            marker=dict(size=8),
            hovertemplate='<b><span style="color:#f2f2f2">Median</span></b><br>' +
                         '<span style="color:#f2f2f2">Year: %{x}</span><br>' +
                         f'<span style="color:#f2f2f2">{value_label}: %{{y:.2f}}</span><br>' +
                         '<extra></extra>',
            customdata=[format_value(val, unit) for val in yearly_data['median']],
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
                    line=dict(color='#4099ff', width=2, dash='dash'),
                    hovertemplate='<b><span style="color:#f2f2f2">Trend Line</span></b><br>' +
                                 '<span style="color:#f2f2f2">Year: %{x}</span><br>' +
                                 f'<span style="color:#f2f2f2">{value_label}: %{{y:.2f}}</span><br>' +
                                 '<extra></extra>'
                )
            )
        except Exception as e:
            print(f"Error creating trend line: {str(e)}")
    
    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=value_label,
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
        hovermode='closest',
        # Add hoverlabel styling to control the hover box
        hoverlabel=dict(
            bgcolor="rgba(38, 45, 65, 0.95)",
            bordercolor="#f2f2f2",
            font_size=12,
            font_family="Arial",
            font_color="#f2f2f2"
        ),
        # Add title with measure and nutrient info
        title=dict(
            text=f"{measure_desc} - {nutrient}",
            x=0.5,
            xanchor='center',
            font=dict(size=14, color="#f2f2f2")
        )
    )
    
    # Format y-axis based on unit
    if unit in ['T', 'T_CO2E', 'TOE']:
        # For large values, use engineering notation
        fig.update_yaxes(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='.2s'  # Scientific notation
        )
    elif unit == 'HA':
        fig.update_yaxes(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='.1f'
        )
    else:
        fig.update_yaxes(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='.2f'
        )
    
    # Ensure proper axis formatting
    fig.update_xaxes(
        tickmode='linear',
        tick0=yearly_data['year'].min(),
        dtick=1,
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.1)'
    )
    
    return fig