from dash import Dash, Input, Output
from utils.data_loader import load_data
from components.layout import create_layout
from utils.data_cleaner import clean_data

# Clean the data before loading
clean_data()

# Use the data_loader utility to load the cleaned data
df = load_data()
app = Dash(__name__)
app.layout = create_layout(df)

@app.callback(
    [Output('line-chart', 'figure'),
     Output('data-table', 'data')],
    [Input('country-dropdown', 'value'),
     Input('nutrient-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_dashboard(country, nutrient, year):
    filtered = df[(df['country_code'] == country) & (df['nutrient_type'] == nutrient)]
    if year:
        filtered = filtered[filtered['year'] == year]

    fig = {
        'data': [{
            'x': filtered['year'],
            'y': filtered['value'],
            'type': 'line',
            'name': f'{country} - {nutrient}'
        }],
        'layout': {
            'title': 'Nutrient Removal Over Time',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Value'}
        }
    }

    return fig, filtered.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8050)  # This is the correct way to run a Dash app
