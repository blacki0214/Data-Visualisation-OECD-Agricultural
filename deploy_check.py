#!/usr/bin/env python3
"""
Pre-deployment verification script for Render deployment
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_file_exists(filename):
    """Check if required file exists"""
    if Path(filename).exists():
        print(f"✅ {filename} exists")
        return True
    else:
        print(f"❌ {filename} missing")
        return False

def check_requirements():
    """Check if requirements.txt has necessary packages"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            required_packages = ['dash', 'plotly', 'pandas', 'gunicorn', 'psycopg2-binary']
            
            for package in required_packages:
                if package in content:
                    print(f"✅ {package} found in requirements.txt")
                else:
                    print(f"❌ {package} missing from requirements.txt")
                    return False
            return True
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_procfile():
    """Check Procfile configuration"""
    try:
        with open('Procfile', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if 'gunicorn app:server' in content:
                print("✅ Procfile correctly configured")
                return True
            else:
                print(f"❌ Procfile misconfigured: {content}")
                return False
    except FileNotFoundError:
        print("❌ Procfile not found")
        return False

def check_app_structure():
    """Check if app.py has correct server configuration"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'server = app.server' in content:
                print("✅ app.py has correct server configuration")
                return True
            else:
                print("❌ app.py missing 'server = app.server' line")
                return False
    except FileNotFoundError:
        print("❌ app.py not found")
        return False

def check_environment_variables():
    """Check if environment variables are set (for local testing)"""
    env_vars = ['NEON_HOST', 'NEON_DATABASE', 'NEON_USER', 'NEON_PASSWORD', 'NEON_PORT']
    all_set = True
    
    print("\n📋 Environment Variables Check:")
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️ {var} not set (will need to be set in Render)")
            all_set = False
    
    return all_set

def test_local_import():
    """Test if the app can be imported without errors"""
    try:
        print("\n🧪 Testing app import...")
        # Try to import the main app
        import app
        print("✅ App imports successfully")
        
        # Check if server object exists
        if hasattr(app, 'server'):
            print("✅ Server object accessible")
            return True
        else:
            print("❌ Server object not found")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        return False

def main():
    """Run all deployment checks"""
    print("🚀 RENDER DEPLOYMENT PRE-CHECK")
    print("=" * 40)
    
    checks = [
        ("Required Files", [
            lambda: check_file_exists('app.py'),
            lambda: check_file_exists('requirements.txt'),
            lambda: check_file_exists('Procfile'),
            lambda: check_file_exists('runtime.txt'),
        ]),
        ("Configuration", [
            check_requirements,
            check_procfile,
            check_app_structure,
        ]),
        ("Environment", [
            check_environment_variables,
        ]),
        ("App Structure", [
            test_local_import,
        ])
    ]
    
    all_passed = True
    
    for category, check_functions in checks:
        print(f"\n📁 {category}:")
        category_passed = True
        
        for check_func in check_functions:
            if isinstance(check_func, list):
                for sub_check in check_func:
                    if not sub_check():
                        category_passed = False
                        all_passed = False
            else:
                if not check_func():
                    category_passed = False
                    all_passed = False
        
        if category_passed:
            print(f"✅ {category} checks passed")
        else:
            print(f"❌ {category} checks failed")
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Ready for Render deployment")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Create a new Web Service on Render")
        print("3. Set environment variables in Render dashboard")
        print("4. Deploy!")
    else:
        print("⚠️ Some checks failed. Please fix the issues before deploying.")
    
    print(f"\n📖 See DEPLOYMENT.md for detailed deployment instructions")

if __name__ == "__main__":
    main()
