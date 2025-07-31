from dash import html
import pandas as pd

def create_data_summary(filtered_df, nutrient, measure):
    """
    Create a data summary component with unit-aware formatting
    
    Parameters:
    - filtered_df: DataFrame containing filtered data
    - nutrient: Selected nutrient type
    - measure: Selected measure code
    
    Returns:
    - Dash HTML component
    """
    if filtered_df.empty:
        return html.Div([
            html.Div([
                html.I(className="fas fa-exclamation-triangle", 
                       style={'fontSize': '48px', 'color': '#ffd43b', 'marginBottom': '15px'}),
                html.H4("No Data Available", 
                        style={'color': '#f2f2f2', 'marginBottom': '10px'}),
                html.P("Please adjust your filters to see data analysis.",
                       style={'color': '#a9a9a9', 'fontSize': '14px'})
            ], style={
                'textAlign': 'center',
                'padding': '40px',
                'backgroundColor': 'rgba(40, 45, 65, 0.6)',
                'borderRadius': '8px',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            })
        ])
    
    # Get unit information
    unit = filtered_df['unit'].iloc[0] if 'unit' in filtered_df.columns and not filtered_df['unit'].isna().iloc[0] else ''
    
    # Create unit display
    if unit:
        if unit == 'T':
            unit_display = 'Tonnes'
        elif unit == 'KG':
            unit_display = 'Kilograms'
        elif unit == 'HA':
            unit_display = 'Hectares'
        elif unit == 'T_CO2E':
            unit_display = 'Tonnes CO₂ equivalent'
        elif unit == 'TOE':
            unit_display = 'Tonnes Oil Equivalent'
        else:
            unit_display = unit
    else:
        unit_display = 'Unknown'
    
    # Calculate statistics
    min_val = filtered_df['value'].min()
    max_val = filtered_df['value'].max()
    avg_val = filtered_df['value'].mean()
    median_val = filtered_df['value'].median()
    std_val = filtered_df['value'].std()
    
    # Get the country with highest and lowest values
    max_country = filtered_df.loc[filtered_df['value'].idxmax(), 'country_code']
    min_country = filtered_df.loc[filtered_df['value'].idxmin(), 'country_code']
    
    # Get measure description
    measure_desc = filtered_df['Measure'].iloc[0] if 'Measure' in filtered_df.columns else measure
    
    # Format values based on unit
    def format_value_with_unit(val, unit_type):
        if pd.isna(val):
            return "N/A"
        
        if unit_type in ['T', 'T_CO2E', 'TOE']:
            if val >= 1000000:
                return f"{val/1000000:.2f}M {unit_display}"
            elif val >= 1000:
                return f"{val/1000:.1f}K {unit_display}"
            else:
                return f"{val:.2f} {unit_display}"
        elif unit_type == 'HA':
            if val >= 1000000:
                return f"{val/1000000:.2f}M {unit_display}"
            elif val >= 1000:
                return f"{val/1000:.1f}K {unit_display}"
            else:
                return f"{val:.1f} {unit_display}"
        elif unit_type == 'KG':
            if val >= 1000:
                return f"{val/1000:.2f} Tonnes"
            else:
                return f"{val:.2f} {unit_display}"
        else:
            return f"{val:.2f} {unit_display}"
    
    # Create modern card-based summary that matches the dashboard design
    summary = [
        # Title Section
        html.Div([
            html.H3("📊 Data Analysis Summary", 
                   style={
                       'color': '#4a9eff', 
                       'marginBottom': '20px', 
                       'textAlign': 'center',
                       'fontSize': '20px',
                       'fontWeight': '600'
                   })
        ]),
        
        # Key Statistics Cards Row
        html.Div([
            # Min Value Card
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(min_val, unit), className="metric-value", style={'fontSize': '18px'}),
                        html.I(className="fas fa-arrow-down metric-icon", style={'color': '#ff6b6b'})
                    ]),
                    html.Div("MINIMUM VALUE", className="metric-label"),
                    html.Div(f"Country: {min_country}", style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px'})
                ])
            ], className="metric-card", style={'backgroundColor': 'rgba(255, 107, 107, 0.1)', 'border': '1px solid rgba(255, 107, 107, 0.3)'}),
            
            # Max Value Card
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(max_val, unit), className="metric-value", style={'fontSize': '18px'}),
                        html.I(className="fas fa-arrow-up metric-icon", style={'color': '#51cf66'})
                    ]),
                    html.Div("MAXIMUM VALUE", className="metric-label"),
                    html.Div(f"Country: {max_country}", style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px'})
                ])
            ], className="metric-card", style={'backgroundColor': 'rgba(81, 207, 102, 0.1)', 'border': '1px solid rgba(81, 207, 102, 0.3)'}),
            
            # Average Value Card
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(avg_val, unit), className="metric-value", style={'fontSize': '18px'}),
                        html.I(className="fas fa-chart-line metric-icon", style={'color': '#4a9eff'})
                    ]),
                    html.Div("AVERAGE VALUE", className="metric-label"),
                    html.Div(f"Median: {format_value_with_unit(median_val, unit)}", style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px'})
                ])
            ], className="metric-card", style={'backgroundColor': 'rgba(74, 158, 255, 0.1)', 'border': '1px solid rgba(74, 158, 255, 0.3)'}),
            
            # Data Points Card
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(f"{len(filtered_df)}", className="metric-value", style={'fontSize': '18px'}),
                        html.I(className="fas fa-database metric-icon", style={'color': '#ffd43b'})
                    ]),
                    html.Div("DATA POINTS", className="metric-label"),
                    html.Div(f"Countries: {filtered_df['country_code'].nunique()}", style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px'})
                ])
            ], className="metric-card", style={'backgroundColor': 'rgba(255, 212, 59, 0.1)', 'border': '1px solid rgba(255, 212, 59, 0.3)'})
        ], className="card-container", style={'marginBottom': '25px'}),
        
        # Detailed Information Section
        html.Div([
            html.Div([
                # Statistical Analysis Panel
                html.Div([
                    html.Div([
                        html.H4([
                            html.I(className="fas fa-chart-bar", style={'marginRight': '8px', 'color': '#4a9eff'}),
                            "Statistical Analysis"
                        ], style={'color': '#f2f2f2', 'marginBottom': '15px', 'fontSize': '16px'}),
                        
                        html.Div([
                            html.Div([
                                html.Span("Standard Deviation", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(format_value_with_unit(std_val, unit), style={'float': 'right', 'color': '#f2f2f2'})
                            ], style={'marginBottom': '8px', 'borderBottom': '1px solid rgba(255,255,255,0.1)', 'paddingBottom': '8px'}),
                            
                            html.Div([
                                html.Span("Year Range", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(f"{filtered_df['year'].min()} - {filtered_df['year'].max()}", style={'float': 'right', 'color': '#f2f2f2'})
                            ], style={'marginBottom': '8px', 'borderBottom': '1px solid rgba(255,255,255,0.1)', 'paddingBottom': '8px'}),
                            
                            html.Div([
                                html.Span("Unit", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(unit_display, style={'float': 'right', 'color': '#f2f2f2'})
                            ], style={'marginBottom': '8px'})
                        ])
                    ], style={
                        'backgroundColor': 'rgba(40, 45, 65, 0.6)',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'border': '1px solid rgba(255, 255, 255, 0.1)'
                    })
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                # Data Information Panel
                html.Div([
                    html.Div([
                        html.H4([
                            html.I(className="fas fa-info-circle", style={'marginRight': '8px', 'color': '#4a9eff'}),
                            "Data Information"
                        ], style={'color': '#f2f2f2', 'marginBottom': '15px', 'fontSize': '16px'}),
                        
                        html.Div([
                            html.Div([
                                html.Span("Nutrient Type", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(nutrient, style={'float': 'right', 'color': '#f2f2f2'})
                            ], style={'marginBottom': '8px', 'borderBottom': '1px solid rgba(255,255,255,0.1)', 'paddingBottom': '8px'}),
                            
                            html.Div([
                                html.Span("Measure", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(measure_desc[:50] + "..." if len(str(measure_desc)) > 50 else measure_desc, 
                                         style={'float': 'right', 'color': '#f2f2f2', 'textAlign': 'right', 'maxWidth': '60%'})
                            ], style={'marginBottom': '8px', 'borderBottom': '1px solid rgba(255,255,255,0.1)', 'paddingBottom': '8px'}),
                            
                            html.Div([
                                html.Span("Coverage", style={'fontWeight': 'bold', 'color': '#a9a9a9'}),
                                html.Span(f"{filtered_df['country_code'].nunique()} Countries", style={'float': 'right', 'color': '#f2f2f2'})
                            ], style={'marginBottom': '8px'})
                        ])
                    ], style={
                        'backgroundColor': 'rgba(40, 45, 65, 0.6)',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'border': '1px solid rgba(255, 255, 255, 0.1)'
                    })
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
            ])
        ])
    ]
    
    return summary