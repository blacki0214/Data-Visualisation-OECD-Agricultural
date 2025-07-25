import os
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NeonDatabase:
    def __init__(self):
        self.host = os.getenv('NEON_HOST')
        self.database = os.getenv('NEON_DATABASE')
        self.user = os.getenv('NEON_USER')
        self.password = os.getenv('NEON_PASSWORD')
        self.port = os.getenv('NEON_PORT', 5432)
        
        # Create connection string
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode=require"
        
    def get_connection(self):
        """Get a direct psycopg2 connection"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode='require'
            )
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def get_engine(self):
        """Get SQLAlchemy engine for pandas operations"""
        try:
            engine = create_engine(self.connection_string)
            return engine
        except Exception as e:
            print(f"Error creating engine: {e}")
            return None
    
    def test_connection(self):
        """Test the database connection"""
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

# Create a global instance
db = NeonDatabase()