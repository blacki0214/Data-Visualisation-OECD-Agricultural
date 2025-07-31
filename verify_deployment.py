"""
Verify the app is ready for Render deployment
"""
import os

def check_deployment_files():
    """Check if all required deployment files exist and are configured correctly"""
    print("🔍 Checking deployment configuration...")
    
    # Check required files
    required_files = {
        'requirements.txt': 'Dependencies file',
        'runtime.txt': 'Python version file', 
        'render.yaml': 'Render configuration',
        'app.py': 'Main application file',
        '.env': 'Environment variables (will be ignored in deployment)'
    }
    
    missing_files = []
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
        else:
            print(f"❌ {file} - {description} (MISSING)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    # Check requirements.txt content
    try:
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
            required_packages = ['dash', 'plotly', 'pandas', 'gunicorn', 'psycopg2-binary']
            missing_packages = []
            for pkg in required_packages:
                if pkg not in reqs:
                    missing_packages.append(pkg)
            
            if missing_packages:
                print(f"⚠️ Missing packages in requirements.txt: {missing_packages}")
            else:
                print("✅ All required packages in requirements.txt")
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False
    
    # Check render.yaml
    try:
        with open('render.yaml', 'r') as f:
            yaml_content = f.read()
            if 'gunicorn app:server' in yaml_content:
                print("✅ Correct startCommand in render.yaml")
            else:
                print("❌ Missing or incorrect startCommand in render.yaml")
                return False
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False
    
    print("\n✅ All deployment files are configured correctly!")
    return True

def test_server_object():
    """Test if the server object can be imported (critical for Gunicorn)"""
    print("\n🔍 Testing server object for Gunicorn compatibility...")
    
    try:
        # This is what Gunicorn will try to do
        from app import server
        print("✅ Server object imported successfully")
        
        # Check if it's a valid WSGI application
        if hasattr(server, '__call__'):
            print("✅ Server is callable (WSGI compatible)")
        else:
            print("❌ Server is not callable")
            return False
            
        print(f"   Server type: {type(server)}")
        return True
        
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Verifying deployment readiness for Render...")
    print("=" * 50)
    
    files_ok = check_deployment_files()
    server_ok = test_server_object()
    
    if files_ok and server_ok:
        print("\n" + "=" * 50)
        print("✅ SUCCESS: App is ready for Render deployment!")
        print("📝 Next steps:")
        print("   1. Commit and push your changes to GitHub")
        print("   2. Deploy to Render")
        print("   3. Gunicorn will handle the WSGI server on Linux")
    else:
        print("\n" + "=" * 50)
        print("❌ FAILED: Please fix the issues above before deployment")