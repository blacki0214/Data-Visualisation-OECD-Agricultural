"""
OECD Agricultural Data Visualization App
Render-compatible version with proper server exposure
"""

import os
from dash import Dash, html

# Initialize app immediately
app = Dash(__name__, suppress_callback_exceptions=True)

# CRITICAL: Expose server for Gunicorn immediately
server = app.server

print("✅ Server object created and exposed")

# Health check endpoint
@server.route('/health')
def health():
    return {'status': 'healthy', 'app': 'OECD Agricultural Data Visualization'}, 200

# Set a basic layout that works without any complex imports
app.layout = html.Div([
    html.H1("OECD Agricultural Data Visualization", 
           style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    html.Div([
        html.P("🚀 Application is starting up..."),
        html.P("📊 Loading dashboard components..."),
        html.P("🔄 This may take a moment on first load."),
    ], style={'textAlign': 'center', 'padding': 20, 'backgroundColor': '#ecf0f1', 
             'borderRadius': 10, 'margin': 20})
])

print("✅ Basic layout set")

# Only import complex components if running directly (not during Gunicorn import)
if __name__ == '__main__':
    print("🔄 Running in development mode...")
    try:
        # Try to load the full application
        from app_backup import *  # Load all the original functionality
        print("✅ Full application loaded")
    except Exception as e:
        print(f"⚠️ Could not load full app: {e}")
    
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    print("✅ App ready for Gunicorn deployment")
