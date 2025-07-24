from dash import html, dcc, dash_table

def create_layout(df):
    # Calculate some metrics for the dashboard cards
    total_countries = df['country_code'].nunique()
    total_measures = df['measure_code'].nunique()
    year_range = f"{df['year'].min()}-{df['year'].max()}"
    avg_value = round(df['value'].mean(), 1)
    
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
                    html.Span(f"{total_countries}", className="metric-value"),
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
                        options=[{'label': c, 'value': c} for c in sorted(df['country_code'].unique())],
                        value=[df['country_code'].iloc[0]] if not df.empty else None,
                        multi=True,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
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
                        options=[{'label': m, 'value': m} for m in sorted(df['measure_code'].unique())],
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
                    min=df['year'].min() if not df.empty else 2000,
                    max=df['year'].max() if not df.empty else 2020,
                    step=1,
                    marks={i: str(i) for i in range(
                        int(df['year'].min()) if not df.empty else 2000, 
                        int(df['year'].max()) + 1 if not df.empty else 2021, 
                        5)},
                    value=[df['year'].min() if not df.empty else 2000, 
                           df['year'].max() if not df.empty else 2020]
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
                
                # NEW EU Data Handling Section
                html.Div([
                    html.Label(style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '5px', 'fontSize': '12px'}),
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
            
            # Box Plot
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Value Distribution", className="chart-title"),
                        html.Span(f"February 2023", className="chart-date")
                    ], className="chart-header"),
                    html.Div([
                        html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                        html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                    ], className="chart-actions")
                ], className="chart-header"),
                dcc.Graph(id='box-plot', style={'height': '300px'})
            ], className="chart-container"),
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
                "Note: Some entities like EU27 or EU28 are excluded from the map visualization as they are not standard country codes.",
                html.Br(),
                "BE2 represents the Flemish Region and BE3 represents Wallonia in Belgium."
            ], style={'fontSize': '12px', 'color': '#a9a9a9', 'marginTop': '5px', 'textAlign': 'center'})
        ], style={'width': '100%'}),
        
        html.Footer([
            html.P("Data Source: OECD Agricultural Environmental Indicators"),
            html.P("© 2025 Agricultural Dashboard")
        ], style={'textAlign': 'center', 'marginTop': 30, 'color': '#a9a9a9'})
        
    ], className="dashboard-container")
