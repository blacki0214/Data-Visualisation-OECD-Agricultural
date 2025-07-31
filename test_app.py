#!/usr/bin/env python3
"""
Test script to verify app structure and imports for deployment
"""
import sys
import traceback

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Test basic libraries
        import pandas as pd
        import numpy as np
        import plotly.graph_objs as go
        import plotly.express as px
        print("✅ Basic libraries imported successfully")
        
        # Test Dash
        from dash import Dash, Input, Output, html, dcc
        print("✅ Dash imported successfully")
        
        # Test database
        from utils.database import load_data_from_db
        print("✅ Database module imported successfully")
        
        # Test components
        from components.layout import create_layout
        print("✅ Layout components imported successfully")
        
        # Test visualizations
        from visualisations.timeseries import create_time_series
        from visualisations.choroplethMap import create_choropleth
        from visualisations.barchart import create_bar_chart
        print("✅ Visualization modules imported successfully")
        
        print("✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_app_structure():
    """Test app structure for deployment"""
    try:
        print("\nTesting app structure...")
        
        # Import the app
        from app import app, server
        
        print("✅ App imported successfully")
        print(f"✅ Server object available: {server}")
        print(f"✅ App object available: {app}")
        
        return True
        
    except Exception as e:
        print(f"❌ App structure error: {e}")
        traceback.print_exc()
        return False

def test_data_loading():
    """Test data loading"""
    try:
        print("\nTesting data loading...")
        
        from utils.database import load_data_from_db
        df = load_data_from_db()
        
        if df is not None:
            print(f"✅ Data loaded successfully: {len(df)} rows")
            return True
        else:
            print("⚠️ No data loaded, but no error thrown")
            return True
            
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Running deployment readiness test...")
    
    tests = [
        test_imports,
        test_app_structure,
        test_data_loading
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    if all(results):
        print("\n✅ All tests passed! App is ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
