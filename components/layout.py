from dash import html, dcc, dash_table

def get_country_names():
    """
    Get a mapping of ISO-3 country codes to full country names.
    """
    country_mapping = {
        'AUT': 'Austria',
        'BEL': 'Belgium', 
        'BGR': 'Bulgaria',
        'CAN': 'Canada',
        'CHL': 'Chile',
        'COL': 'Colombia',
        'CRI': 'Costa Rica',
        'CZE': 'Czech Republic',
        'DNK': 'Denmark',
        'EST': 'Estonia',
        'FIN': 'Finland',
        'FRA': 'France',
        'DEU': 'Germany',
        'GRC': 'Greece',
        'HUN': 'Hungary',
        'ISL': 'Iceland',
        'IRL': 'Ireland',
        'ISR': 'Israel',
        'ITA': 'Italy',
        'JPN': 'Japan',
        'KOR': 'South Korea',
        'LVA': 'Latvia',
        'LTU': 'Lithuania',
        'LUX': 'Luxembourg',
        'MEX': 'Mexico',
        'NLD': 'Netherlands',
        'NZL': 'New Zealand',
        'NOR': 'Norway',
        'POL': 'Poland',
        'PRT': 'Portugal',
        'SVK': 'Slovak Republic',
        'SVN': 'Slovenia',
        'ESP': 'Spain',
        'SWE': 'Sweden',
        'CHE': 'Switzerland',
        'TUR': 'Turkey',
        'GBR': 'United Kingdom',
        'USA': 'United States',
        'HRV': 'Croatia',
        'CYP': 'Cyprus',
        'MLT': 'Malta',
        'ROU': 'Romania',
        'ARG': 'Argentina',
        'AUS': 'Australia',
        'BRA': 'Brazil',
        'CHN': 'China',
        'IND': 'India',
        'IDN': 'Indonesia',
        'RUS': 'Russia',
        'ZAF': 'South Africa'
    }
    
    return country_mapping

def is_actual_country(country_code):
    """
    Check if a country code represents an actual country (not regional/organizational entities).
    """
    # List of non-country entities to exclude
    excluded_entities = [
        'EU', 'EU27', 'EU28', 'EU27_2020',  # European Union variants
        'OECD',  # OECD average
        'BE2', 'BE3',  # Belgian regions
        'WORLD', 'G7', 'G20',  # Other aggregates
    ]
    
    return country_code not in excluded_entities

def create_layout(df):
    # Calculate some metrics for the dashboard cards
    total_countries = df['country_code'].nunique()
    total_measures = df['measure_code'].nunique()
    year_range = f"{df['year'].min()}-{df['year'].max()}"
    avg_value = round(df['value'].mean(), 1)
    
    # Get country mapping
    country_names = get_country_names()
    
    # Create country dropdown options with full names (exclude regional/organizational entities)
    country_options = []
    for code in sorted(df['country_code'].unique()):
        # Only include actual countries
        if is_actual_country(code):
            full_name = country_names.get(code, code)
            # Show only the full country name, not the code
            country_options.append({'label': full_name, 'value': code})
    
    # Create measure dropdown options using the Measure column (not Measure2)
    measure_options = []
    
    # Use the 'Measure' column which contains the full descriptive names
    if 'Measure' in df.columns:
        # Create a mapping from measure codes to their descriptions
        measure_mapping = df[['measure_code', 'Measure']].drop_duplicates().set_index('measure_code')['Measure'].to_dict()
        
        for code in sorted(df['measure_code'].unique()):
            full_name = measure_mapping.get(code, code)
            # Clean up the description if it's too long
            if len(full_name) > 60:
                full_name = full_name[:57] + "..."
            measure_options.append({'label': full_name, 'value': code})
    else:
        # Fallback to just using the codes if Measure column doesn't exist
        for code in sorted(df['measure_code'].unique()):
            measure_options.append({'label': code, 'value': code})
    
    # Get the first actual country for default value
    default_country = None
    for code in df['country_code'].unique():
        if is_actual_country(code):
            default_country = code
            break
    
    return html.Div([
        # Dashboard Header
        html.Div([
            html.H1("OECD Agricultural Environmental Dashboard"),
            html.P("Comprehensive analysis of agricultural environmental indicators across countries")
        ], className="dashboard-header"),
        
        # Metrics Cards
        html.Div([
            html.Div([
                html.Div([
                    html.Span(f"{avg_value}", className="metric-value"),
                    html.I(className="fas fa-money-bill metric-icon")
                ]),
                html.Div("AVERAGE VALUE", className="metric-label"),
                html.Div([
                    html.Div(className="mini-chart"),
                    html.Div([
                        html.Div(className="progress-bar"),
                        html.Div(className="progress-fill")
                    ], className="progress-container")
                ])
            ], className="metric-card cyan"),
            
            html.Div([
                html.Div([
                    html.Span(f"{len(country_options)}", className="metric-value"),  # Show actual country count
                    html.I(className="fas fa-globe metric-icon")
                ]),
                html.Div("COUNTRIES", className="metric-label"),
                html.Div([
                    html.Div(className="mini-chart"),
                    html.Div([
                        html.Div(className="progress-bar"),
                        html.Div(className="progress-fill")
                    ], className="progress-container")
                ])
            ], className="metric-card coral"),
            
            html.Div([
                html.Div([
                    html.Span(f"{total_measures}", className="metric-value"),
                    html.I(className="fas fa-chart-bar metric-icon")
                ]),
                html.Div("MEASURES", className="metric-label"),
                html.Div([
                    html.Div(className="mini-chart"),
                    html.Div([
                        html.Div(className="progress-bar"),
                        html.Div(className="progress-fill")
                    ], className="progress-container")
                ])
            ], className="metric-card amber"),
            
            html.Div([
                html.Div([
                    html.Span(year_range, className="metric-value"),
                    html.I(className="fas fa-calendar-alt metric-icon")
                ]),
                html.Div("YEAR RANGE", className="metric-label"),
                html.Div([
                    html.Div(className="mini-chart"),
                    html.Div([
                        html.Div(className="progress-bar"),
                        html.Div(className="progress-fill")
                    ], className="progress-container")
                ])
            ], className="metric-card purple")
        ], className="card-container"),
        
        # Controls Container
        html.Div([
            html.Div([
                html.Div([
                    html.Label("Select Country/Countries", style={'fontWeight': 'bold', 'color': "#f2f2f2"}),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=country_options,
                        value=[default_country] if default_country else None,
                        multi=True,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        },
                        placeholder="Select countries..."
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Label("Select Nutrient", style={'fontWeight': 'bold', 'color': '#f2f2f2'}),
                    dcc.Dropdown(
                        id='nutrient-dropdown',
                        options=[{'label': n, 'value': n} for n in sorted(df['nutrient_type'].unique())],
                        value=df['nutrient_type'].iloc[0] if not df.empty else None,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Label("Select Measure", style={'fontWeight': 'bold', 'color': '#f2f2f2'}),
                    dcc.Dropdown(
                        id='measure-dropdown',
                        options=measure_options,
                        value=df['measure_code'].iloc[0] if not df.empty else None,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], className="filter-item"),
            ], className="filter-row"),
            
            html.Div([
                html.Label("Year Range", style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '10px', 'display': 'block'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=2012,  # Fixed to actual data range
                    max=2022,  # Fixed to actual data range
                    step=1,
                    marks={i: str(i) for i in range(2012, 2023, 2)},  # Show marks every 2 years
                    value=[2012, 2022]  # Default to full range
                )
            ]),
        ], className="controls-container"),
        
        # Charts Row 1
        html.Div([
            # Time Series Chart
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Time Series Analysis", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                dcc.Graph(id='time-series-chart', style={'height': '300px'})
            ], className="chart-container"),
            
            # Choropleth Map
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Geographic Distribution", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                
                # Add this dropdown for year selection
                html.Div([
                    html.Label("Select Map Year", style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '5px', 'fontSize': '12px'}),
                    dcc.Dropdown(
                        id='map-year-dropdown',
                        options=[{'label': str(y), 'value': y} for y in sorted(df['year'].unique())],
                        value=df['year'].max() if not df.empty else 2020,
                        clearable=False,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], style={'marginBottom': '15px'}),
                
                # EU Data Handling Section
                html.Div([
                    html.Label("EU Data Handling", style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '5px', 'fontSize': '12px'}),
                    dcc.RadioItems(
                        id='eu-data-option',
                        value='distribute',
                        labelStyle={'display': 'block', 'margin': '5px 0', 'fontSize': '12px'},
                        style={'color': '#f2f2f2'}
                    )
                ], style={'marginBottom': '15px', 'marginTop': '10px'}),
            
                
                dcc.Graph(id='choropleth-map', style={'height': '300px'})
            ], className="chart-container"),
        ], className="chart-row"),
        
        # NEW Combined Chart Row
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Trends & Averages", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                dcc.Graph(id='combined-chart', style={'height': '300px'})
            ], className="chart-container full-width")  # Use full width for this chart
        ], className="chart-row"),
        
        # Charts Row 2
        html.Div([
            # Bar Chart
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Country Comparisons", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                dcc.Graph(id='bar-chart', style={'height': '300px'})
            ], className="chart-container"),   
        ], className="chart-row"),
        
        # NEW Charts Row 3 - Add Scatter Plot
        html.Div([
            # Scatter Plot
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Scatter Plot Analysis", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                
                # Add X-axis selector for scatter plot
                html.Div([
                    html.Label("X-Axis Variable", style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '5px', 'fontSize': '12px'}),
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=[
                            {'label': 'Year', 'value': 'year'},
                            {'label': 'Value Distribution', 'value': 'value'}
                        ],
                        value='year',
                        clearable=False,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], style={'marginBottom': '15px'}),
                
                dcc.Graph(id='scatter-chart', style={'height': '300px'})
            ], className="chart-container full-width")
        ], className="chart-row"),

        # Data Table & Summary
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Data Summary", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                html.Div(id='data-summary', className="summary-content")
            ], className="chart-container"),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Filtered Data", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'backgroundColor': 'rgba(38, 45, 65, 1)',
                        'color': '#f2f2f2',
                        'padding': '10px',
                        'textAlign': 'left'
                    },
                    style_header={
                        'backgroundColor': 'rgba(30, 33, 48, 1)',
                        'fontWeight': 'bold',
                        'padding': '10px'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'},
                         'backgroundColor': 'rgba(44, 52, 75, 1)'}
                    ],
                    filter_action="native",
                    sort_action="native",
                )
            ], className="chart-container"),
        ], className="chart-row"),
        
        # Note about data representation
        html.Div([
            html.P([
                "Note: Regional entities like EU, OECD, and Belgian regions are excluded from country selection but may appear in other visualizations.",
                html.Br(),
                "The map visualization handles EU data separately through the EU Data Handling option."
            ], style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px', 'textAlign': 'center'})
        ], style={'width': '100%'}),
        
        html.Footer([
            html.P("Data Source: OECD Agricultural Environmental Indicators"),
            html.P("© 2025 Agricultural Dashboard")
        ], style={'textAlign': 'center', 'marginTop': 30, 'color': '#a9a9a9'})
        
    ], className="dashboard-container")
