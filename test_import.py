#!/usr/bin/env python3
"""
Minimal test to check if app.py can be imported
"""

import os
import sys

# Set minimal environment variables
os.environ['NEON_HOST'] = 'test'
os.environ['NEON_DATABASE'] = 'test'
os.environ['NEON_USER'] = 'test'
os.environ['NEON_PASSWORD'] = 'test'
os.environ['NEON_PORT'] = '5432'

try:
    print("🔄 Attempting to import app...")
    import app
    print(f"✅ App imported successfully")
    print(f"✅ Server object type: {type(app.server)}")
    print(f"✅ Server object: {app.server}")
    print(f"✅ Server callable: {callable(app.server)}")
    
    # Test if server has the WSGI interface
    if hasattr(app.server, 'wsgi_app'):
        print(f"✅ WSGI app found: {app.server.wsgi_app}")
    
    print("🎉 All tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
    
print("\n📋 Python path:")
for path in sys.path:
    print(f"  - {path}")
