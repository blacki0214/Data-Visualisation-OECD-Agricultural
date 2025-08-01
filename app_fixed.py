"""
OECD Agricultural Data Visualization App - Render-optimized version
This version ensures the server object is available immediately for Gunicorn
"""

import os
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Initialize Dash app FIRST - before any complex imports
app = Dash(__name__, suppress_callback_exceptions=True)

# CRITICAL: Expose server immediately for Gunicorn
server = app.server

# Add health check endpoint immediately
@server.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        'status': 'healthy',
        'app': 'OECD Agricultural Data Visualization',
        'version': '1.0'
    }, 200

print("✅ Server object exposed for Gunicorn")

# Global variables for data (will be loaded lazily)
df = None
df_cleaned = None

def load_data_lazy():
    """Load data only when needed"""
    global df, df_cleaned
    
    if df is not None:
        return df, df_cleaned
    
    try:
        # Try to import and load data
        from utils.database import load_data_from_db
        from utils.country_mapper import clean_country_codes
        
        print("🔄 Loading data from Neon database...")
        df = load_data_from_db()
        
        if df is None:
            print("❌ Database failed, trying file...")
            from utils.data_loader import load_data
            df = load_data()
        
        if df is None:
            print("⚠️ Using sample data")
            df = pd.DataFrame({
                'country_code': ['USA', 'CAN', 'GBR'],
                'year': [2020, 2020, 2020],
                'nutrient_type': ['Nitrogen', 'Nitrogen', 'Nitrogen'],
                'measure_code': ['F1', 'F1', 'F1'],
                'value': [100, 200, 150]
            })
        
        df_cleaned = clean_country_codes(df)
        print(f"✅ Data loaded: {len(df)} rows")
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        df = pd.DataFrame({
            'country_code': ['USA', 'CAN'],
            'year': [2020, 2020],
            'nutrient_type': ['Nitrogen', 'Nitrogen'],
            'measure_code': ['F1', 'F1'],
            'value': [100, 200]
        })
        df_cleaned = df.copy()
    
    return df, df_cleaned

def create_simple_layout():
    """Create a simple layout that works without data"""
    return html.Div([
        html.H1("OECD Agricultural Data Visualization", 
                style={'textAlign': 'center', 'marginBottom': 30}),
        
        html.Div([
            html.P("Loading dashboard...", id="loading-status"),
            html.Button("Load Data", id="load-btn", n_clicks=0),
        ], style={'textAlign': 'center', 'padding': 20}),
        
        html.Div(id="main-content", children=[
            html.P("Click 'Load Data' to start the dashboard.")
        ])
    ])

# Set simple layout immediately
app.layout = create_simple_layout()

# Callback to load data and full layout
@app.callback(
    [Output('main-content', 'children'),
     Output('loading-status', 'children')],
    [Input('load-btn', 'n_clicks')]
)
def update_layout(n_clicks):
    if n_clicks == 0:
        return html.P("Click 'Load Data' to start the dashboard."), "Ready to load data..."
    
    try:
        df, df_cleaned = load_data_lazy()
        
        # Import layout components only when needed
        from components.layout import create_layout
        
        layout = create_layout(df_cleaned)
        return layout, f"✅ Loaded {len(df)} rows successfully!"
        
    except Exception as e:
        error_layout = html.Div([
            html.H3("Error Loading Dashboard"),
            html.P(f"Error: {str(e)}"),
            html.P("The application encountered an error. Please try refreshing the page.")
        ])
        return error_layout, f"❌ Error: {str(e)}"

print("✅ App layout and callbacks configured")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
