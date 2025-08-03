# OECD Agricultural Environmental Data Visualization Dashboard

An interactive web dashboard for visualizing and analyzing OECD Agricultural Environmental Indicators data. This project provides comprehensive insights into agricultural environmental performance across OECD countries through various data visualization techniques.

## 🌾 Overview

This dashboard enables users to explore OECD agricultural environmental data through multiple visualization types, including time series analysis, geographical maps, statistical charts, and advanced analytics. The application is built with Python Dash and deployed on Render with data stored in a Neon PostgreSQL database.

## ✨ Features

### Basic Charts
- **Time Series Analysis**: Track environmental indicators over time
- **Choropleth Maps**: Geographical visualization of data across countries
- **Bar Charts**: Compare values across countries and measures
- **Box Plots**: Statistical distribution analysis
- **Scatter Plots**: Correlation analysis between variables

### Advanced Analytics
- **Heatmaps**: Measure-country correlation matrices
- **Radar Charts**: Multi-dimensional country comparisons
- **Sunburst Charts**: Hierarchical data visualization
- **Combined Charts**: Multi-metric comparative analysis

### Interactive Features
- **Metrics Dashboard**: Key performance indicators and trends
- **Comparative Analysis**: Side-by-side country comparisons
- **Dynamic Filtering**: Filter by country, year, and measure categories
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: Dash (Python web framework)
- **Data Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Database**: PostgreSQL (Neon)
- **Deployment**: Render
- **Styling**: Dash Bootstrap Components, Custom CSS

## 📊 Data Source

The dashboard uses OECD Agricultural Environmental Indicators data, which includes:
- Nutrient balances (Nitrogen, Phosphorus)
- Pesticide use indicators
- Water quality metrics
- Soil quality measurements
- Greenhouse gas emissions
- Land use patterns

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL database (Neon account recommended)
- Git

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/blacki0214/Data-Visualisation-OECD-Agricultural.git
   cd Data-Visualisation-OECD-Agricultural
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

5. **Initialize the database**
   ```bash
   python setup_db.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:8050`

## 🏗️ Project Structure

```
Data-Visualisation-OECD-Agricultural/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── Procfile              # Render deployment configuration
├── render.yaml           # Render service configuration
├── setup_db.py           # Database initialization
├── data/                 # Data files
│   ├── arg_env_data.csv
│   └── cleaned_arg_env_data.csv
├── components/           # UI components
│   └── layout.py
├── utils/                # Utility functions
│   ├── database.py       # Database operations
│   ├── data_loader.py    # Data loading utilities
│   ├── data_cleaner.py   # Data cleaning functions
│   ├── country_mapper.py # Country code mapping
│   └── measure_categorizer.py # Data categorization
├── visualisations/       # Chart components
│   ├── timeseries.py
│   ├── choroplethMap.py
│   ├── barchart.py
│   ├── boxplot.py
│   ├── scatterplot.py
│   ├── heatmap.py
│   ├── radar_chart.py
│   ├── sunburst_chart.py
│   └── metrics_dashboard.py
└── assets/               # Static assets
    ├── styles.css
    └── favicon.ico
```

## 🚢 Deployment

The application is configured for deployment on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to Render

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Set up environment variables (DATABASE_URL)
5. Deploy!

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Application port (default: 8050)

### Database Setup

The application supports both file-based and database-driven data loading:
- Primary: PostgreSQL database with OECD data
- Fallback: Local CSV files in the `data/` directory

## 📈 Usage

1. **Navigate** through different tabs to explore various visualization types
2. **Filter** data by selecting countries, years, and measure categories
3. **Compare** countries using the comparative analysis features
4. **Analyze** trends using the metrics dashboard
5. **Export** visualizations using Plotly's built-in export features

## 📞 Contact

- **Author**: blacki0214
- **Repository**: [Data-Visualisation-OECD-Agricultural](https://github.com/blacki0214/Data-Visualisation-OECD-Agricultural)

---

*For technical issues or feature requests, please open an issue on GitHub.*
