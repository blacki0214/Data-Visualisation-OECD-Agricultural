from dash import html, dcc, dash_table
from utils.measure_descriptions import get_measure_description, format_measure_label
from utils.measure_categorizer import get_category_options_for_dropdown

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
    # Calculate meaningful metrics for the dashboard cards
    
    # Get actual countries (excluding regional entities)
    actual_countries = [code for code in df['country_code'].unique() if is_actual_country(code)]
    total_countries = len(actual_countries)
    
    # Get total measures
    total_measures = df['measure_code'].nunique()
    
    # Get year range
    year_range = f"{df['year'].min()}-{df['year'].max()}"
    
    # Calculate total data points for a cleaner metric
    total_records = len(df)
    
    # Format total records for display
    if total_records >= 1000000:
        formatted_records = f"{total_records/1000000:.1f}M"
    elif total_records >= 1000:
        formatted_records = f"{total_records/1000:.0f}K"
    else:
        formatted_records = str(total_records)
    
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
                    html.Span(formatted_records, className="metric-value"),
                    html.I(className="fas fa-database metric-icon")
                ]),
                html.Div("DATA RECORDS", className="metric-label"),
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
        
        # Data Summary Cards Section
        html.Div([
            html.Div(id='data-summary', children=[])
        ], style={
            'marginBottom': '20px',
            'width': '100%'
        }),
        
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
                    html.Label("Measure Category", style={'fontWeight': 'bold', 'color': '#f2f2f2'}),
                    dcc.Dropdown(
                        id='measure-dropdown',
                        options=get_category_options_for_dropdown(),  # type: ignore
                        value=get_category_options_for_dropdown()[0]['value'] if get_category_options_for_dropdown() else None,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Label("EU Data Handling", style={'fontWeight': 'bold', 'color': '#f2f2f2'}),
                    dcc.RadioItems(
                        id='eu-data-option',
                        options=[
                            {'label': 'Distribute EU data to member countries', 'value': 'distribute'},
                            {'label': 'Show EU as separate entity', 'value': 'separate'},
                            {'label': 'Exclude EU data', 'value': 'exclude'}
                        ],
                        value='distribute',
                        labelStyle={'display': 'block', 'margin': '5px 0', 'fontSize': '12px'},
                        style={'color': '#f2f2f2'}
                    )
                ], className="filter-item"),
            ], className="filter-row"),
            
            html.Div([
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
                ], style={'width': '70%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Map Year", style={'fontWeight': 'bold', 'color': '#f2f2f2', 'marginBottom': '10px', 'display': 'block'}),
                    dcc.Dropdown(
                        id='map-year-dropdown',
                        options=[{'label': str(y), 'value': y} for y in sorted(df['year'].unique())],
                        value=df['year'].min() if not df.empty else 2012,
                        clearable=False,
                        className="dash-dropdown",
                        style={
                            'color': '#000000',
                            'backgroundColor': '#252e3f'
                        }
                    )
                ], style={'width': '25%', 'display': 'inline-block', 'marginLeft': '5%'}),
            ], style={'display': 'flex', 'alignItems': 'end', 'gap': '20px'}),
        ], className="controls-container"),
        
        # Help Section
        html.Div([
            html.Details([
                html.Summary([
                    html.I(className="fas fa-question-circle", style={'marginRight': '8px'}),
                    "📊 How to Use This Dashboard - Click for Help"
                ], style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#4a9eff', 'cursor': 'pointer', 'padding': '10px'}),
                html.Div([
                    html.Div([
                        html.H4("🎯 Getting Started", style={'color': '#4a9eff', 'marginTop': '0'}),
                        html.P("1. Use the controls above to filter data by country, nutrient type, measure, and year"),
                        html.P("2. Navigate through different tabs to explore various visualization types"),
                        html.P("3. Hover over charts for detailed information and insights"),
                    ], style={'marginBottom': '15px'}),
                    
                    html.Div([
                        html.H4("📈 Chart Types Explained", style={'color': '#4a9eff'}),
                        html.Ul([
                            html.Li("🗺️ Geographic Maps: Show data distribution across countries"),
                            html.Li("📊 Time Series: Track changes over time"),
                            html.Li("📈 Bar Charts: Compare countries side-by-side"),
                            html.Li("📦 Box Plots: Understand data distribution and outliers"),
                            html.Li("🔥 Heatmaps: Spot patterns across countries and years"),
                            html.Li("🕸️ Radar Charts: Multi-dimensional country comparisons"),
                            html.Li("☀️ Sunburst Charts: Explore data hierarchically"),
                            html.Li("💹 Scatter Plots: Discover relationships between variables"),
                        ], style={'fontSize': '13px'}),
                    ], style={'marginBottom': '15px'}),
                    
                    html.Div([
                        html.H4("🔍 Key Metrics", style={'color': '#4a9eff'}),
                        html.P("• Agricultural land use and production indicators"),
                        html.P("• Greenhouse gas emissions (CO2, CH4, N2O)"),
                        html.P("• Water and energy consumption"),
                        html.P("• Pesticide and fertilizer applications"),
                        html.P("• Environmental sustainability metrics"),
                    ], style={'fontSize': '13px'})
                ], style={
                    'backgroundColor': 'rgba(40, 45, 65, 0.5)',
                    'padding': '15px',
                    'borderRadius': '6px',
                    'marginTop': '10px',
                    'border': '1px solid rgba(255, 255, 255, 0.1)'
                })
            ])
        ], style={'margin': '15px 0'}),
        
        # Visualization Tabs
        html.Div([
            dcc.Tabs(id="visualization-tabs", value='basic-tab', children=[
                dcc.Tab(label='Basic Charts', value='basic-tab', className='tab-style', selected_className='tab-selected'),
                dcc.Tab(label='Advanced Analytics', value='advanced-tab', className='tab-style', selected_className='tab-selected'),
                dcc.Tab(label='Metrics Dashboard', value='metrics-tab', className='tab-style', selected_className='tab-selected'),
                dcc.Tab(label='Comparative Analysis', value='comparative-tab', className='tab-style', selected_className='tab-selected'),
            ], className='tabs-container'),
            
            # Hidden div for scroll reset trigger
            html.Div(id='scroll-reset-trigger', style={'display': 'none'}),
            
            # Tab Content
            html.Div(id='tab-content')
        ], className="tabs-wrapper"),
        
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

def create_basic_charts_tab(df):
    """Create the basic charts tab content"""
    return html.Div([
        # Scrollable container for Basic Charts
        html.Div([
            # Charts Row 1
            html.Div([
                # Time Series Chart
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Time Series Analysis", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Track how agricultural metrics change over time. Each line represents a different country, showing trends from 2012-2023. Use this to identify long-term patterns and seasonal variations.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Real-time Data", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Visualize how metrics evolve over time. Perfect for identifying trends, seasonal patterns, and comparing country performance across years."
                    ], className="chart-description"),
                    dcc.Graph(id='time-series-chart', style={'height': '350px'})
                ], className="chart-container"),
                
                # Choropleth Map
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Geographic Distribution", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Shows how agricultural and environmental metrics vary across different countries. Darker colors indicate higher values. Use the controls to explore different years, nutrients, and measures.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Interactive Map", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "This map visualizes OECD agricultural data geographically. Darker colors indicate higher values. Perfect for identifying regional patterns and comparing countries at a glance."
                    ], className="chart-description"),
                    dcc.Graph(id='choropleth-map', style={'height': '350px'})
                ], className="chart-container"),
            ], className="chart-row"),
            
            # Charts Row 2
            html.Div([
                # Bar Chart
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Country Comparisons", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Compare values across countries for the selected year and metric. Bars are sorted by value to easily identify top and bottom performers.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Top Countries", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Direct country-to-country comparison for a specific year and metric. Easily spot leaders and laggards in agricultural performance."
                    ], className="chart-description"),
                    dcc.Graph(id='bar-chart', style={'height': '350px'})
                ], className="chart-container"),
                
                # Box Plot
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Distribution Analysis", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Box plots show data distribution including median (middle line), quartiles (box edges), range (whiskers), and outliers (dots). The box contains 50% of the data.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Statistical Overview", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Understand data distribution patterns. The box shows the middle 50% of values, lines extend to min/max, and outliers appear as individual points."
                    ], className="chart-description"),
                    dcc.Graph(id='box-plot-chart', style={'height': '350px'})
                ], className="chart-container"),
            ], className="chart-row"),
        ], className="scrollable-section"),
    ])

def create_advanced_analytics_tab(df):
    """Create the advanced analytics tab content"""
    print("Creating advanced analytics tab...")
    return html.Div([
        # Scrollable container for Advanced Analytics
        html.Div([
            # Heatmaps Row
            html.Div([
                # Measure-Country Heatmap (NEW)
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Measure-Country Heatmap", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("A heat map showing individual measures within a category (rows) across different countries (columns). Darker colors indicate higher values. Perfect for comparing specific measures across countries.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Category Breakdown", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Visualize how individual measures within a category vary across countries. Each row represents a specific measure, and each column represents a country."
                    ], className="chart-description"),
                    dcc.Graph(id='country-year-heatmap', style={'height': '450px'})
                ], className="chart-container full-width"),
            ], className="chart-row"),
            
            # Radar and Sunburst Row
            html.Div([
                # Radar Chart
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Multi-Dimensional Analysis", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Radar charts compare countries across multiple metrics simultaneously. Each axis represents a different measure, and the polygon shows a country's performance profile. Larger areas indicate better overall performance.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Radar Chart", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Compare countries across multiple dimensions at once. Each spoke represents a different metric, making it easy to see performance profiles and identify strengths/weaknesses."
                    ], className="chart-description"),
                    dcc.Graph(id='radar-chart', style={'height': '450px'})
                ], className="chart-container"),
                
                # Sunburst Chart
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Hierarchical Breakdown", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Sunburst charts show hierarchical data in concentric circles. Inner rings represent broader categories (continents/regions), while outer rings show detailed breakdowns (countries, nutrients). Click segments to drill down.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Sunburst Chart", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Explore data hierarchically from global patterns to specific details. Start from the center and move outward to drill down from continents to countries to specific metrics."
                    ], className="chart-description"),
                    dcc.Graph(id='sunburst-chart', style={'height': '450px'})
                ], className="chart-container"),
            ], className="chart-row"),
        ], className="scrollable-section"),
    ])

def create_metrics_dashboard_tab(df):
    """Create the metrics dashboard tab content"""
    return html.Div([
        # Scrollable container for Metrics Dashboard
        html.Div([
            # KPI Cards
            html.Div([
                html.Div([
                    "The KPI cards below provide quick insights into key agricultural metrics. Each card shows current values, trends, and comparisons to help you understand performance at a glance."
                ], className="chart-description"),
            ]),
            html.Div(id='kpi-cards', style={'margin': '20px 0'}),
            
            # Metrics Dashboard
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Comprehensive Metrics", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("A comprehensive view of key agricultural and environmental metrics. This dashboard combines multiple indicators to provide a holistic view of agricultural performance and sustainability.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Key Performance Indicators", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "View multiple agricultural metrics in one comprehensive dashboard. Perfect for getting a complete picture of agricultural and environmental performance."
                    ], className="chart-description"),
                    dcc.Graph(id='metrics-dashboard', style={'height': '550px'})
                ], className="chart-container full-width"),
            ], className="chart-row"),
            
            # Time Series Metrics
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Time Series Metrics", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Track how key agricultural metrics evolve over time. This visualization helps identify trends, cycles, and turning points in agricultural and environmental indicators.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Trend Analysis", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Monitor metric trends over time to understand long-term patterns and identify areas of improvement or concern in agricultural sustainability."
                    ], className="chart-description"),
                    dcc.Graph(id='time-series-metrics', style={'height': '550px'})
                ], className="chart-container full-width"),
            ], className="chart-row"),
        ], className="scrollable-section"),
    ])

def create_comparative_analysis_tab(df):
    """Create the comparative analysis tab content"""
    return html.Div([
        # Scrollable container for Comparative Analysis
        html.Div([
            # Scatter Plot and Combined Chart Row
            html.Div([
                # Scatter Plot
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Scatter Plot Analysis", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Scatter plots reveal relationships between two variables. Each point represents a country or data point. Patterns help identify correlations, outliers, and clusters in the data.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Correlation Analysis", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "Explore relationships between variables. Look for patterns, clusters, and outliers to understand how different agricultural metrics relate to each other."
                    ], className="chart-description"),
                    
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
                    
                    dcc.Graph(id='scatter-chart', style={'height': '400px'})
                ], className="chart-container"),
                
                # Combined Chart
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("Trends & Averages", className="chart-title"),
                            html.Div([
                                html.I(className="fas fa-info-circle info-icon"),
                                html.Span("Combines multiple chart types to show both individual country trends and overall averages. Great for comparing individual performance against global patterns.", className="tooltiptext")
                            ], className="chart-tooltip"),
                            html.Span(f"Combined Analysis", className="chart-date")
                        ], className="chart-header"),
                        html.Div([
                            html.Button([html.I(className="fas fa-download"), " Export"], className="chart-action-btn"),
                            html.Button([html.I(className="fas fa-print"), " Print"], className="chart-action-btn")
                        ], className="chart-actions")
                    ], className="chart-header"),
                    html.Div([
                        "See both individual country performance and overall trends in one view. Perfect for understanding how countries perform relative to global averages."
                    ], className="chart-description"),
                    dcc.Graph(id='combined-chart', style={'height': '400px'})
                ], className="chart-container")
            ], className="chart-row"),
        ], className="scrollable-section"),
    ])
