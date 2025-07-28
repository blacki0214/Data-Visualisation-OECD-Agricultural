"""
Test script to verify database connection
"""

from utils.database import db
from sqlalchemy import create_engine, text

def main():
    print("🔍 Testing Neon Database Connection")
    print("=" * 50)
    
    # Test connection
    if db.test_connection():
        print("\n✅ Database connection is working!")
        
        # Try to create a simple test table
        try:
            engine = db.get_engine()
            if engine:
                with engine.connect() as conn:
                    # Create a test table
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS test_table (
                            id SERIAL PRIMARY KEY,
                            test_column VARCHAR(50)
                        )
                    """))
                    
                    # Insert test data
                    conn.execute(text("""
                        INSERT INTO test_table (test_column) 
                        VALUES ('test_value')
                        ON CONFLICT DO NOTHING
                    """))
                    
                    # Query test data
                    result = conn.execute(text("SELECT * FROM test_table LIMIT 1"))
                    row = result.fetchone()
                    
                    if row:
                        print(f"✅ Test table created and queried successfully: {row}")
                    
                    # Clean up
                    conn.execute(text("DROP TABLE IF EXISTS test_table"))
                    conn.commit()
                    
                    print("✅ Test table cleaned up")
                    
        except Exception as e:
            print(f"❌ Error during advanced testing: {e}")
    else:
        print("\n❌ Database connection failed!")
        print("Please check your .env file and Neon database credentials")

if __name__ == "__main__":
    main()