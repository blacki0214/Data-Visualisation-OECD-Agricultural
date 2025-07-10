from dash import html, dcc, dash_table

def create_layout(df):
    return html.Div([
        html.H1("Agri-Environmental Indicators Dashboard"),

        html.Div([
            html.Label("Select Country"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in sorted(df['country_code'].unique())],
                value=df['country_code'].iloc[0] if not df.empty else None
            )
        ]),

        html.Div([
            html.Label("Select Nutrient"),
            dcc.Dropdown(
                id='nutrient-dropdown',
                options=[{'label': n, 'value': n} for n in sorted(df['nutrient_type'].unique())],
                value=df['nutrient_type'].iloc[0] if not df.empty else None
            )
        ]),

        html.Div([
            html.Label("Select Year (optional)"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(y), 'value': y} for y in sorted(df['year'].unique())],
                value=None
            )
        ]),

        dcc.Graph(id='line-chart'),

        html.H3("Filtered Data Table"),
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'}
        )
    ])
