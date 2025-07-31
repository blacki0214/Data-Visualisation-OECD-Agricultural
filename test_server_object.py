"""
Test to verify the server object is properly exposed
"""

def test_server():
    try:
        from app import server
        print("✅ Server object imported successfully")
        print(f"   Server type: {type(server)}")
        print(f"   Server callable: {callable(server)}")
        print(f"   Server object: {server}")
        return True
    except Exception as e:
        print(f"❌ Failed to import server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing server object...")
    if test_server():
        print("✅ Server object is ready for Gunicorn!")
    else:
        print("❌ Server object test failed!")