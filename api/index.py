import os
import sys
import json
from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import plotly.graph_objs as go
import plotly.utils

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.database import load_data_from_db
    from utils.country_mapper import clean_country_codes
    from visualisations.timeseries import create_time_series
    from visualisations.barchart import create_bar_chart
    from visualisations.boxplot import create_box_plot
    from visualisations.scatterplot import create_scatter_plot
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback functions will be defined below

app = Flask(__name__)

# Global variable to store data
df = None
df_cleaned = None

def create_fallback_chart(title="No data available"):
    """Create a simple fallback chart when data loading fails"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], mode='lines', name='Sample'))
    fig.update_layout(title=title, template='plotly_white')
    return fig

def initialize_data():
    """Initialize data on first request"""
    global df, df_cleaned
    if df is None:
        try:
            print("🔄 Loading data from Neon database...")
            df = load_data_from_db()
            
            if df is None:
                print("❌ Failed to load data from database!")
                # Create sample DataFrame as fallback
                df = pd.DataFrame({
                    'country_code': ['USA', 'CAN', 'DEU', 'FRA'] * 5,
                    'year': [2020, 2020, 2020, 2020, 2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024],
                    'nutrient': ['nitrogen'] * 20,
                    'measure': ['balance'] * 20,
                    'value': [100, 150, 120, 180, 110, 160, 130, 190, 105, 155, 125, 185, 115, 165, 135, 195, 120, 170, 140, 200]
                })
            
            # Clean country codes
            df_cleaned = clean_country_codes(df)
            print(f"✅ Data loaded successfully! Shape: {df_cleaned.shape}")
        except Exception as e:
            print(f"Error initializing data: {e}")
            # Create minimal fallback data
            df_cleaned = pd.DataFrame({
                'country_code': ['USA', 'CAN'],
                'year': [2020, 2020],
                'nutrient': ['nitrogen', 'nitrogen'],
                'measure': ['balance', 'balance'],
                'value': [100, 150]
            })

def filter_data(countries, nutrient, measure, years):
    """Filter data based on user selections"""
    if df_cleaned is None:
        return pd.DataFrame()
    
    filtered = df_cleaned.copy()
    
    if countries and len(countries) > 0:
        filtered = filtered[filtered['country_code'].isin(countries)]
    
    if nutrient and nutrient != 'all':
        filtered = filtered[filtered['nutrient'] == nutrient]
    
    if measure and measure != 'all':
        filtered = filtered[filtered['measure'] == measure]
    
    if years and len(years) == 2:
        filtered = filtered[
            (filtered['year'] >= years[0]) & 
            (filtered['year'] <= years[1])
        ]
    
    return filtered

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OECD Agricultural Data Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .controls { margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 5px; }
        .control-group { margin: 10px 0; }
        label { display: inline-block; width: 150px; font-weight: bold; }
        select, input { padding: 5px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .chart-container { margin: 20px 0; min-height: 400px; }
    </style>
</head>
<body>
    <h1>🌾 OECD Agricultural Data Visualization Dashboard</h1>
    
    <div class="controls">
        <div class="control-group">
            <label for="countries">Countries:</label>
            <select id="countries" multiple style="width: 200px; height: 100px;">
                <option value="USA">United States</option>
                <option value="CAN">Canada</option>
                <option value="DEU">Germany</option>
                <option value="FRA">France</option>
                <option value="GBR">United Kingdom</option>
                <option value="JPN">Japan</option>
                <option value="AUS">Australia</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="nutrient">Nutrient:</label>
            <select id="nutrient">
                <option value="all">All Nutrients</option>
                <option value="nitrogen">Nitrogen</option>
                <option value="phosphorus">Phosphorus</option>
                <option value="potassium">Potassium</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="measure">Measure:</label>
            <select id="measure">
                <option value="all">All Measures</option>
                <option value="balance">Balance</option>
                <option value="input">Input</option>
                <option value="output">Output</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="chart-type">Chart Type:</label>
            <select id="chart-type">
                <option value="timeseries">Time Series</option>
                <option value="bar">Bar Chart</option>
                <option value="box">Box Plot</option>
                <option value="scatter">Scatter Plot</option>
            </select>
        </div>
        
        <button onclick="updateChart()">Update Chart</button>
    </div>
    
    <div id="chart" class="chart-container"></div>
    
    <script>
        function getSelectedValues(selectElement) {
            const selected = [];
            for (let option of selectElement.options) {
                if (option.selected) {
                    selected.push(option.value);
                }
            }
            return selected;
        }
        
        function updateChart() {
            const countries = getSelectedValues(document.getElementById('countries'));
            const nutrient = document.getElementById('nutrient').value;
            const measure = document.getElementById('measure').value;
            const chartType = document.getElementById('chart-type').value;
            
            const params = new URLSearchParams({
                countries: JSON.stringify(countries),
                nutrient: nutrient,
                measure: measure,
                chart_type: chartType
            });
            
            fetch(`/api/chart?${params}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('chart').innerHTML = `<p>Error: ${data.error}</p>`;
                    } else {
                        Plotly.newPlot('chart', data.data, data.layout, {responsive: true});
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('chart').innerHTML = '<p>Error loading chart</p>';
                });
        }
        
        // Load initial chart
        updateChart();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page"""
    initialize_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chart')
def get_chart():
    """API endpoint to get chart data"""
    try:
        initialize_data()
        
        # Get parameters
        countries = json.loads(request.args.get('countries', '[]'))
        nutrient = request.args.get('nutrient', 'all')
        measure = request.args.get('measure', 'all')
        chart_type = request.args.get('chart_type', 'timeseries')
        
        # Filter data
        filtered_df = filter_data(countries, nutrient, measure, [2000, 2023])
        
        if filtered_df.empty:
            return jsonify({
                'error': 'No data available for the selected filters',
                'data': [],
                'layout': {}
            })
        
        # Create chart based on type
        try:
            if chart_type == 'timeseries':
                fig = create_time_series(filtered_df, nutrient, measure)
            elif chart_type == 'bar':
                fig = create_bar_chart(filtered_df, nutrient, measure, [2000, 2023])
            elif chart_type == 'box':
                fig = create_box_plot(filtered_df, nutrient, measure)
            elif chart_type == 'scatter':
                fig = create_scatter_plot(filtered_df, nutrient, measure)
            else:  # Default to timeseries
                fig = create_time_series(filtered_df, nutrient, measure)
        except Exception as e:
            print(f"Error creating chart: {e}")
            fig = create_fallback_chart(f"Error creating {chart_type} chart")
        
        # Convert to JSON
        graphJSON = plotly.utils.PlotlyJSONEncoder().encode(fig)
        graph_data = json.loads(graphJSON)
        
        return jsonify({
            'data': graph_data['data'],
            'layout': graph_data['layout']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/data-summary')
def get_data_summary():
    """API endpoint to get data summary"""
    try:
        initialize_data()
        if df_cleaned is not None and not df_cleaned.empty:
            # Simple data summary
            summary = {
                'total_records': len(df_cleaned),
                'countries': df_cleaned['country_code'].unique().tolist(),
                'nutrients': df_cleaned['nutrient'].unique().tolist(),
                'measures': df_cleaned['measure'].unique().tolist(),
                'year_range': [int(df_cleaned['year'].min()), int(df_cleaned['year'].max())]
            }
        else:
            summary = {
                'total_records': 0,
                'countries': [],
                'nutrients': [],
                'measures': [],
                'year_range': [2020, 2024]
            }
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)})

# For Vercel deployment
app_instance = app

if __name__ == '__main__':
    app.run(debug=True)
