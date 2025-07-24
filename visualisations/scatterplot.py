import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_scatter_plot(filtered_df, nutrient, measure, x_axis='year'):
    """
    Create a scatter plot visualization
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    - x_axis: Selected x-axis variable (default: 'year')
    
    Returns:
    - Plotly figure object
    """
    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available for the selected filters",
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_white"
        )
        return fig
    
    # Get unit information for meaningful labels
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns else ''
    value_label = f'Value ({unit})' if unit else 'Value'
    
    # Create scatter plot
    if x_axis == 'year':
        try:
            fig = px.scatter(
                filtered_df,
                x='year',
                y='value',
                color='country_code',
                size='value',
                size_max=30,
                title=f'{measure} for {nutrient} Over Time',
                labels={'value': value_label, 'year': 'Year', 'country_code': 'Country'},
                hover_data={'year': True, 'value': ':.2f', 'country_code': True, 'unit': True}
            )
            
            # Add trendlines if there are enough data points
            if len(filtered_df['year'].unique()) > 2:
                for country in filtered_df['country_code'].unique():
                    country_data = filtered_df[filtered_df['country_code'] == country]
                    if len(country_data) > 2:  # Need at least 3 points for a meaningful trendline
                        # Add trendline for this country
                        z = np.polyfit(country_data['year'], country_data['value'], 1)
                        p = np.poly1d(z)
                        x_range = np.linspace(country_data['year'].min(), country_data['year'].max(), 100)
                        fig.add_trace(
                            go.Scatter(
                                x=x_range, 
                                y=p(x_range), 
                                mode='lines', 
                                name=f'Trend {country}',
                                line=dict(dash='dash'),
                                opacity=0.7,
                                hovertemplate=f'<b>Trend {country}</b><br>Year: %{{x}}<br>{value_label}: %{{y:.2f}}<extra></extra>'
                            )
                        )
        except Exception as e:
            print(f"Error creating year-based scatter plot: {e}")
            # Fallback to a simple scatter
            fig = px.scatter(
                filtered_df,
                x='year',
                y='value',
                color='country_code',
                title=f'{measure} for {nutrient} Over Time',
                labels={'value': value_label, 'year': 'Year', 'country_code': 'Country'}
            )
    else:
        # Create a value distribution scatter plot
        try:
            # Group by country and year, count occurrences
            count_df = filtered_df.groupby(['country_code', 'year']).size().reset_index(name='count')
            # Join back with original data
            plot_df = pd.merge(filtered_df, count_df, on=['country_code', 'year'])
            
            fig = px.scatter(
                plot_df,
                x='value',
                y='count',
                color='country_code',
                size='value',
                size_max=30,
                title=f'Value Distribution of {measure} for {nutrient}',
                labels={'value': value_label, 'count': 'Count', 'country_code': 'Country'},
                hover_data={'year': True, 'value': ':.2f', 'country_code': True, 'unit': True}
            )
        except Exception as e:
            print(f"Error creating value-based scatter plot: {e}")
            # Fallback to a simple scatter
            fig = px.scatter(
                filtered_df,
                x='value',
                y='value',  # Just to have something on y-axis
                color='country_code',
                title=f'Value Distribution of {measure} for {nutrient}',
                labels={'value': value_label, 'country_code': 'Country'}
            )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='closest',
        legend_title='Country',
        xaxis_title=x_axis.capitalize(),
        yaxis_title=value_label if x_axis == 'year' else 'Count'
    )
    
    # Update hover template to include unit information
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      f'{value_label}: %{{y:.2f}}<br>' +
                      '<extra></extra>'
    )
    
    return fig