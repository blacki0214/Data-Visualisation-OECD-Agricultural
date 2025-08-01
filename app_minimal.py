"""
Minimal OECD Agricultural Data Visualization App for Render deployment
This version ensures the server object is always available for Gunicorn
"""

import os
from dash import Dash, html

# Initialize Dash app first - this must work
app = Dash(__name__)

# Expose server immediately for Gunicorn
server = app.server

# Simple fallback layout
app.layout = html.Div([
    html.H1("OECD Agricultural Data Visualization"),
    html.Div("Loading application...", id="content")
])

# Health check endpoint
@server.route('/health')
def health_check():
    return {'status': 'healthy', 'app': 'OECD Agricultural Data Visualization'}, 200

print("✅ Minimal app initialized with server exposed")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
