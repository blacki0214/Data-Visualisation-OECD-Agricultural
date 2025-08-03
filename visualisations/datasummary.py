from dash import html
import pandas as pd

def create_data_summary(filtered_df, nutrient, measure):
    """
    Create a comprehensive data summary component that combines statistical analysis and overview
    
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
    
    # Get overview data
    total_records = len(filtered_df)
    countries_count = filtered_df['country_code'].nunique()
    years_span = f"{filtered_df['year'].min()}-{filtered_df['year'].max()}"
    top_countries = filtered_df.groupby('country_code')['value'].mean().nlargest(3)
    
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
    
    # Create comprehensive summary layout
    summary = [
        # Title Section - More Compact
        html.Div([
            html.H3("📊 Data Analysis Summary & Overview", 
                   style={
                       'color': '#4a9eff', 
                       'marginBottom': '10px', 
                       'textAlign': 'center',
                       'fontSize': '18px',
                       'fontWeight': '600'
                   })
        ]),
        
        # Quick Overview Stats Row - More Compact
        html.Div([
            html.Div([
                html.Span(str(total_records), style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#4a9eff'}),
                html.Div("Records", style={'fontSize': '10px', 'color': '#a9a9a9'})
            ], style={'textAlign': 'center', 'flex': '1'}),
            
            html.Div([
                html.Span(str(countries_count), style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#51cf66'}),
                html.Div("Countries", style={'fontSize': '10px', 'color': '#a9a9a9'})
            ], style={'textAlign': 'center', 'flex': '1'}),
            
            html.Div([
                html.Span(years_span, style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#ffd43b'}),
                html.Div("Years", style={'fontSize': '10px', 'color': '#a9a9a9'})
            ], style={'textAlign': 'center', 'flex': '1'}),
            
            html.Div([
                html.Span(unit_display, style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#ff6b6b'}),
                html.Div("Unit", style={'fontSize': '10px', 'color': '#a9a9a9'})
            ], style={'textAlign': 'center', 'flex': '1'})
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '15px', 'padding': '8px', 'backgroundColor': 'rgba(40, 45, 65, 0.6)', 'borderRadius': '6px', 'border': '1px solid rgba(255, 255, 255, 0.1)'}),
        
        # Main Content Row - All sections side by side
        html.Div([
            # Left Column - Key Statistics Cards (Compact)
            html.Div([
                # Min Value Card
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(min_val, unit), style={'fontSize': '12px', 'fontWeight': 'bold', 'color': '#ff6b6b'}),
                        html.Div("MIN VALUE", style={'fontSize': '9px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                        html.Div(f"{min_country}", style={'fontSize': '9px', 'color': '#a9a9a9'})
                    ])
                ], style={'backgroundColor': 'rgba(255, 107, 107, 0.1)', 'border': '1px solid rgba(255, 107, 107, 0.3)', 'marginBottom': '6px', 'padding': '6px', 'borderRadius': '4px', 'textAlign': 'center'}),
                
                # Max Value Card
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(max_val, unit), style={'fontSize': '12px', 'fontWeight': 'bold', 'color': '#51cf66'}),
                        html.Div("MAX VALUE", style={'fontSize': '9px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                        html.Div(f"{max_country}", style={'fontSize': '9px', 'color': '#a9a9a9'})
                    ])
                ], style={'backgroundColor': 'rgba(81, 207, 102, 0.1)', 'border': '1px solid rgba(81, 207, 102, 0.3)', 'marginBottom': '6px', 'padding': '6px', 'borderRadius': '4px', 'textAlign': 'center'}),
                
                # Average Value Card
                html.Div([
                    html.Div([
                        html.Span(format_value_with_unit(avg_val, unit), style={'fontSize': '12px', 'fontWeight': 'bold', 'color': '#4a9eff'}),
                        html.Div("AVERAGE", style={'fontSize': '9px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                        html.Div(f"Median: {format_value_with_unit(median_val, unit)}", style={'fontSize': '8px', 'color': '#a9a9a9'})
                    ])
                ], style={'backgroundColor': 'rgba(74, 158, 255, 0.1)', 'border': '1px solid rgba(74, 158, 255, 0.3)', 'padding': '6px', 'borderRadius': '4px', 'textAlign': 'center'})
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
            
            # Middle Left - Top Performers - Clean Cards
            html.Div([
                html.Div([
                    html.Span(f"1. {list(top_countries.keys())[0]}", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#ffd43b'}),
                    html.Div("TOP PERFORMER", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div(f"{list(top_countries.values())[0]:.1f}", style={'fontSize': '10px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(255, 212, 59, 0.1)', 'border': '1px solid rgba(255, 212, 59, 0.3)', 'marginBottom': '8px', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'}),
                
                html.Div([
                    html.Span(f"2. {list(top_countries.keys())[1]}", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#a78bfa'}),
                    html.Div("SECOND PLACE", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div(f"{list(top_countries.values())[1]:.1f}", style={'fontSize': '10px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(167, 139, 250, 0.1)', 'border': '1px solid rgba(167, 139, 250, 0.3)', 'marginBottom': '8px', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'}),
                
                html.Div([
                    html.Span(f"3. {list(top_countries.keys())[2]}", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#fb7185'}),
                    html.Div("THIRD PLACE", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div(f"{list(top_countries.values())[2]:.1f}", style={'fontSize': '10px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(251, 113, 133, 0.1)', 'border': '1px solid rgba(251, 113, 133, 0.3)', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'})
            ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
            
            # Middle Right - Statistical Information - Clean Cards
            html.Div([
                html.Div([
                    html.Span(format_value_with_unit(std_val, unit), style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#34d399'}),
                    html.Div("STD DEVIATION", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div("Variability measure", style={'fontSize': '9px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(52, 211, 153, 0.1)', 'border': '1px solid rgba(52, 211, 153, 0.3)', 'marginBottom': '8px', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'}),
                
                html.Div([
                    html.Span(f"{total_records}", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#f59e0b'}),
                    html.Div("DATA POINTS", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div("Total observations", style={'fontSize': '9px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(245, 158, 11, 0.1)', 'border': '1px solid rgba(245, 158, 11, 0.3)', 'marginBottom': '8px', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'}),
                
                html.Div([
                    html.Span(f"{countries_count}", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#8b5cf6'}),
                    html.Div("COVERAGE", style={'fontSize': '10px', 'color': '#a9a9a9', 'fontWeight': 'bold'}),
                    html.Div("Countries included", style={'fontSize': '9px', 'color': '#a9a9a9'})
                ], style={'backgroundColor': 'rgba(139, 92, 246, 0.1)', 'border': '1px solid rgba(139, 92, 246, 0.3)', 'padding': '10px', 'borderRadius': '6px', 'textAlign': 'center'})
            ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
            
            # Right Column - Current Selection & Description
            html.Div([
                html.H5("� Current Selection", 
                       style={'color': '#f2f2f2', 'fontSize': '13px', 'marginBottom': '8px', 'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.Span("Nutrient:", style={'fontWeight': 'bold', 'color': '#a9a9a9', 'fontSize': '10px'}),
                        html.Div(nutrient, style={'color': '#f2f2f2', 'fontSize': '11px', 'marginTop': '1px'})
                    ], style={'marginBottom': '6px'}),
                    html.Div([
                        html.Span("Category:", style={'fontWeight': 'bold', 'color': '#a9a9a9', 'fontSize': '10px'}),
                        html.Div(measure if isinstance(measure, str) else str(measure), 
                                style={'color': '#f2f2f2', 'fontSize': '11px', 'marginTop': '1px'})
                    ], style={'marginBottom': '6px'}),
                    html.Div([
                        html.Span("Description:", style={'fontWeight': 'bold', 'color': '#a9a9a9', 'fontSize': '10px'}),
                        html.Div(measure_desc[:50] + "..." if len(str(measure_desc)) > 50 else measure_desc, 
                                style={'color': '#f2f2f2', 'fontSize': '9px', 'marginTop': '1px', 'lineHeight': '1.2'})
                    ])
                ])
            ], style={
                'width': '24%', 
                'display': 'inline-block', 
                'verticalAlign': 'top',
                'backgroundColor': 'rgba(40, 45, 65, 0.6)',
                'padding': '10px',
                'borderRadius': '6px',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            })
        ])
    ]
    
    return summary