"""
Comprehensive error check and app health verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import load_data_from_db, db
import pandas as pd

def comprehensive_health_check():
    print("🔍 Comprehensive App Health Check")
    print("=" * 50)
    
    # 1. Database Connection
    print("1️⃣ Testing Database Connection...")
    try:
        if db.test_connection():
            print("   ✅ Database connection successful")
        else:
            print("   ❌ Database connection failed")
            return False
    except Exception as e:
        print(f"   ❌ Database connection error: {e}")
        return False
    
    # 2. Data Loading
    print("\n2️⃣ Testing Data Loading...")
    try:
        df = load_data_from_db()
        if df is not None and not df.empty:
            print(f"   ✅ Data loaded successfully: {len(df)} rows")
            print(f"   📊 Data shape: {df.shape}")
            print(f"   📋 Required columns present: {all(col in df.columns for col in ['country_code', 'year', 'nutrient_type', 'measure_code', 'value'])}")
        else:
            print("   ❌ Data loading failed or empty")
            return False
    except Exception as e:
        print(f"   ❌ Data loading error: {e}")
        return False
    
    # 3. Import Tests
    print("\n3️⃣ Testing Module Imports...")
    try:
        from visualisations.choroplethMap import create_choropleth
        from visualisations.timeseries import create_time_series
        from visualisations.barchart import create_bar_chart
        from components.layout import create_layout
        from utils.country_mapper import clean_country_codes
        print("   ✅ All visualization modules imported successfully")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # 4. Data Processing Test
    print("\n4️⃣ Testing Data Processing...")
    try:
        # Clean country codes
        df_cleaned = clean_country_codes(df)
        print(f"   ✅ Country code cleaning successful: {len(df_cleaned)} rows")
        
        # Find valid data combinations
        combinations = df.groupby(['year', 'nutrient_type', 'measure_code']).size().reset_index(name='count')
        top_combination = combinations.sort_values('count', ascending=False).iloc[0]
        
        print(f"   ✅ Found {len(combinations)} valid data combinations")
        print(f"   📊 Top combination: {top_combination['year']}, {top_combination['nutrient_type']}, {top_combination['measure_code']} ({top_combination['count']} records)")
        
    except Exception as e:
        print(f"   ❌ Data processing error: {e}")
        return False
    
    # 5. Visualization Test
    print("\n5️⃣ Testing Visualizations...")
    try:
        # Test with known good parameters
        test_year = 2020
        test_nutrient = 'Nitrogen'
        test_measure = 'F1'
        
        test_data = df[(df['year'] == test_year) & 
                      (df['nutrient_type'] == test_nutrient) & 
                      (df['measure_code'] == test_measure)]
        
        if not test_data.empty:
            # Test choropleth
            fig = create_choropleth(df, test_nutrient, test_measure, test_year)
            if fig and hasattr(fig, 'data'):
                print("   ✅ Choropleth visualization working")
            
            # Test time series
            fig2 = create_time_series(test_data, test_nutrient, test_measure)
            if fig2 and hasattr(fig2, 'data'):
                print("   ✅ Time series visualization working")
            
            # Test bar chart
            fig3 = create_bar_chart(test_data, test_nutrient, test_measure, test_year)
            if fig3 and hasattr(fig3, 'data'):
                print("   ✅ Bar chart visualization working")
                
        else:
            print("   ⚠️ No test data available for visualization test")
            
    except Exception as e:
        print(f"   ❌ Visualization error: {e}")
        return False
    
    # 6. App Layout Test
    print("\n6️⃣ Testing App Layout...")
    try:
        layout = create_layout(df_cleaned)
        if layout:
            print("   ✅ App layout created successfully")
        else:
            print("   ❌ App layout creation failed")
            return False
    except Exception as e:
        print(f"   ❌ Layout error: {e}")
        return False
    
    print("\n✅ All health checks passed!")
    print("🎉 Your app is ready to run!")
    return True

def get_recommended_parameters():
    """Get recommended parameters for testing the app"""
    print("\n📋 Recommended Parameters for Testing:")
    print("=" * 40)
    
    df = load_data_from_db()
    if df is None:
        print("❌ Cannot get recommendations - no data")
        return
    
    # Get most common combinations
    combinations = df.groupby(['year', 'nutrient_type', 'measure_code']).size().reset_index(name='count')
    top_5 = combinations.sort_values('count', ascending=False).head(5)
    
    print("Top 5 data combinations to test:")
    for idx, row in enumerate(top_5.itertuples(), 1):
        print(f"  {idx}. Year: {row.year}, Nutrient: {row.nutrient_type}, Measure: {row.measure_code} ({row.count} records)")
    
    # Get country recommendations
    country_counts = df['country_code'].value_counts().head(5)
    print(f"\nTop 5 countries by data volume:")
    for country, count in country_counts.items():
        print(f"  {country}: {count:,} records")

if __name__ == "__main__":
    success = comprehensive_health_check()
    
    if success:
        get_recommended_parameters()
        print(f"\n🚀 To start your app, run:")
        print(f"   python app.py")
        print(f"\n🌐 Then visit: http://localhost:8050")
    else:
        print(f"\n❌ Health check failed! Please fix the issues above before running the app.")
