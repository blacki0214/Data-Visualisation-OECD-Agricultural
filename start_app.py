"""
Simple script to restart the OECD Agricultural Data Visualization app
"""

import subprocess
import sys
import os
import time

def restart_app():
    print("🔄 Restarting OECD Agricultural Data Visualization App")
    print("=" * 50)
    
    # Run health check first
    print("1️⃣ Running health check...")
    try:
        result = subprocess.run([sys.executable, "health_check.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Start the app
    print("\n2️⃣ Starting the app...")
    print("   🌐 App will be available at: http://localhost:8050")
    print("   📝 Press Ctrl+C to stop the app")
    print("   📊 Loading database data...")
    print("")
    
    try:
        # Run the app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 App stopped by user")
    except Exception as e:
        print(f"\n❌ App error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 OECD Agricultural Data Visualization App")
    print("📊 Database-powered interactive dashboard")
    print("")
    
    restart_app()
