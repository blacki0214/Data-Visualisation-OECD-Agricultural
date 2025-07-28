"""
Setup script to initialize Neon database with OECD agricultural data
"""

from utils.database import (
    db, 
    create_tables, 
    insert_country_data, 
    upload_data_to_neon, 
    get_data_summary
)

def main():
    print("🚀 Setting up Neon Database for OECD Agricultural Data")
    print("=" * 60)
    
    # Check if database connection was initialized
    if db is None:
        print("❌ Database connection could not be initialized")
        print("Please check your .env file and ensure all environment variables are set correctly")
        return False
    
    # Step 1: Test connection
    print("\n1. Testing database connection...")
    if not db.test_connection():
        print("❌ Please check your .env file and database credentials")
        print("\n📝 Your .env file should look like this:")
        print("NEON_HOST=ep-curly-boat-a1u86fdz-pooler.ap-southeast-1.aws.neon.tech")
        print("NEON_DATABASE=neondb")
        print("NEON_USER=neondb_owner")
        print("NEON_PASSWORD=npg_xqVWLGd05osr")
        print("NEON_PORT=5432")
        print("\n⚠️  Make sure there are NO quotes around the values!")
        return False
    
    # Step 2: Create tables
    print("\n2. Creating database tables...")
    if not create_tables():
        print("❌ Failed to create tables")
        return False
    
    # Step 3: Insert reference data
    print("\n3. Inserting country reference data...")
    if not insert_country_data():
        print("❌ Failed to insert country data")
        return False
    
    # Step 4: Upload main data
    print("\n4. Uploading OECD agricultural data...")
    if not upload_data_to_neon():
        print("❌ Failed to upload main data")
        return False
    
    # Step 5: Get summary
    print("\n5. Getting data summary...")
    get_data_summary()
    
    print("\n" + "=" * 60)
    print("✅ Database setup completed successfully!")
    print("\n📌 Next steps:")
    print("   1. Your data is now stored in Neon database")
    print("   2. You can update your app.py to use database loading")
    print("   3. Test your dashboard with the new database backend")
    print("   4. Consider adding data refresh functionality")
    
    # Optional: Show how to update app.py
    print("\n🔧 To use database in your app, replace this line in app.py:")
    print("   from utils.data_loader import load_data")
    print("   with:")
    print("   from utils.database import load_data_from_db as load_data")
    
    return True

def test_only():
    """Test database connection without uploading data"""
    
    print("🔍 Testing Neon Database Connection Only")
    print("=" * 45)
    
    if db is None:
        print("❌ Database connection could not be initialized")
        print("Please check your .env file")
        return False
    
    if db.test_connection():
        print("✅ Database connection successful!")
        print("   You can now run the full setup with: python setup_db.py")
        return True
    else:
        print("❌ Database connection failed!")
        print("\n🛠️  Troubleshooting tips:")
        print("   1. Check your .env file exists and has correct values")
        print("   2. Ensure no quotes around environment variable values")
        print("   3. Verify your Neon database is running")
        print("   4. Check network connectivity")
        return False

def reset_database():
    """Reset the database (drop all tables and recreate)"""
    
    if db is None:
        print("❌ Database connection could not be initialized")
        return False
    
    print("⚠️  RESETTING DATABASE - This will delete all existing data!")
    confirmation = input("Are you sure? Type 'yes' to continue: ")
    
    if confirmation.lower() != 'yes':
        print("❌ Reset cancelled")
        return False
    
    print("\n🗑️  Resetting database...")
    
    # Test connection first
    if not db.test_connection():
        print("❌ Cannot connect to database")
        return False
    
    # Recreate tables (this will drop existing ones)
    if create_tables():
        print("✅ Database reset successfully!")
        print("   Run 'python setup_db.py' to reload data")
        return True
    else:
        print("❌ Failed to reset database")
        return False

def check_data():
    """Check if data exists in the database"""
    
    print("📊 Checking database data...")
    
    if db is None:
        print("❌ Database connection could not be initialized")
        return False
    
    if not db.test_connection():
        print("❌ Cannot connect to database")
        return False
    
    try:
        from sqlalchemy import text
        engine = db.get_engine()
        
        if engine is None:
            print("❌ Could not get database engine")
            return False
        
        with engine.connect() as conn:
            # Check if tables exist
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name IN ('oecd_agricultural_data', 'countries', 'measures')
            """)
            
            tables = conn.execute(tables_query).fetchall()
            
            if not tables:
                print("❌ No tables found. Run setup first.")
                return False
            
            print(f"✅ Found {len(tables)} tables")
            
            # Check data counts
            for table in ['oecd_agricultural_data', 'countries', 'measures']:
                try:
                    count_query = text(f"SELECT COUNT(*) FROM {table}")
                    count = conn.execute(count_query).scalar()
                    print(f"   - {table}: {count:,} rows")
                except:
                    print(f"   - {table}: table not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            test_only()
        elif command == 'reset':
            reset_database()
        elif command == 'check':
            check_data()
        elif command == 'help':
            print("🚀 Neon Database Setup Commands:")
            print("   python setup_db.py        - Full setup")
            print("   python setup_db.py test   - Test connection only")
            print("   python setup_db.py check  - Check existing data")
            print("   python setup_db.py reset  - Reset database")
            print("   python setup_db.py help   - Show this help")
        else:
            print(f"❌ Unknown command: {command}")
            print("   Use 'python setup_db.py help' for available commands")
    else:
        # Run full setup
        main()