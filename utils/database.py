import os
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NeonDatabase:
    def __init__(self):
        # Load environment variables with validation
        self.host = os.getenv('NEON_HOST')
        self.database = os.getenv('NEON_DATABASE')
        self.user = os.getenv('NEON_USER')
        self.password = os.getenv('NEON_PASSWORD')
        self.port = os.getenv('NEON_PORT', 5432)
        
        # Validate that all required variables are present
        if not all([self.host, self.database, self.user, self.password]):
            missing = [var for var, val in [
                ('NEON_HOST', self.host),
                ('NEON_DATABASE', self.database),
                ('NEON_USER', self.user),
                ('NEON_PASSWORD', self.password)
            ] if not val]
            raise ValueError(f"Missing required environment variables: {missing}")
        
        # Create connection string
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode=require"
        print(f"Connection string created for host: {self.host}")
        
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
            print("✅ Direct psycopg2 connection successful")
            return conn
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def get_engine(self):
        """Get SQLAlchemy engine for pandas operations"""
        try:
            engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,  # Validate connections before use
                pool_recycle=300,    # Recycle connections every 5 minutes
                echo=False           # Set to True for debugging SQL queries
            )
            
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("SQLAlchemy engine created successfully")
            return engine
        except Exception as e:
            print(f"Error creating engine: {e}")
            print(f"Connection string: {self.connection_string}")
            return None
    
    def test_connection(self):
        """Test the database connection"""
        print("🔍 Testing database connection...")
        
        # Test environment variables
        print(f"Host: {self.host}")
        print(f"Database: {self.database}")
        print(f"User: {self.user}")
        print(f"Port: {self.port}")
        
        try:
            engine = self.get_engine()
            if engine is None:
                print("❌ Failed to create database engine")
                return False
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_result = result.scalar()
                if test_result == 1:
                    print("✅ Database connection successful!")
                    return True
                else:
                    print("❌ Unexpected test result")
                    return False
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

# Create a global instance
db = NeonDatabase()

def create_tables():
    """Create the necessary tables for OECD agricultural data"""
    
    create_table_sql = """
    -- Drop existing tables if they exist
    DROP TABLE IF EXISTS oecd_agricultural_data CASCADE;
    DROP TABLE IF EXISTS countries CASCADE;
    DROP TABLE IF EXISTS measures CASCADE;
    
    -- Create main data table
    CREATE TABLE oecd_agricultural_data (
        id SERIAL PRIMARY KEY,
        country_code VARCHAR(10) NOT NULL,
        frequency VARCHAR(10),
        measure_code VARCHAR(50) NOT NULL,
        measure_description TEXT,
        erosion_level VARCHAR(50),
        water_type VARCHAR(50),
        nutrient_type VARCHAR(50),
        nutrients VARCHAR(50),
        unit VARCHAR(20),
        year INTEGER NOT NULL,
        value DECIMAL(15, 3),
        decimals INTEGER,
        decimals_desc VARCHAR(50),
        status VARCHAR(10),
        unit_mult VARCHAR(10),
        base_per VARCHAR(50),
        measure2 TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes for better performance
    CREATE INDEX idx_country_year ON oecd_agricultural_data(country_code, year);
    CREATE INDEX idx_measure_nutrient ON oecd_agricultural_data(measure_code, nutrient_type);
    CREATE INDEX idx_year ON oecd_agricultural_data(year);
    CREATE INDEX idx_country ON oecd_agricultural_data(country_code);
    
    -- Create a table for country information
    CREATE TABLE countries (
        country_code VARCHAR(10) PRIMARY KEY,
        country_name VARCHAR(100),
        region VARCHAR(50),
        is_eu_member BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create a table for measures
    CREATE TABLE measures (
        measure_code VARCHAR(50) PRIMARY KEY,
        measure_name TEXT,
        category VARCHAR(100),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        engine = db.get_engine()
        if engine is None:
            print("❌ Could not get database engine")
            return False
            
        with engine.connect() as conn:
            # Execute the SQL commands
            conn.execute(text(create_table_sql))
            conn.commit()
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_country_data():
    """Insert country reference data"""
    
    countries_data = [
        ('ARG', 'Argentina', 'South America', False),
        ('AUT', 'Austria', 'Europe', True),
        ('BEL', 'Belgium', 'Europe', True),
        ('BGR', 'Bulgaria', 'Europe', True),
        ('CAN', 'Canada', 'North America', False),
        ('CHL', 'Chile', 'South America', False),
        ('COL', 'Colombia', 'South America', False),
        ('CRI', 'Costa Rica', 'Central America', False),
        ('CZE', 'Czech Republic', 'Europe', True),
        ('DNK', 'Denmark', 'Europe', True),
        ('EST', 'Estonia', 'Europe', True),
        ('FIN', 'Finland', 'Europe', True),
        ('FRA', 'France', 'Europe', True),
        ('DEU', 'Germany', 'Europe', True),
        ('GRC', 'Greece', 'Europe', True),
        ('HUN', 'Hungary', 'Europe', True),
        ('ISL', 'Iceland', 'Europe', False),
        ('IRL', 'Ireland', 'Europe', True),
        ('ISR', 'Israel', 'Middle East', False),
        ('ITA', 'Italy', 'Europe', True),
        ('JPN', 'Japan', 'Asia', False),
        ('KOR', 'South Korea', 'Asia', False),
        ('LVA', 'Latvia', 'Europe', True),
        ('LTU', 'Lithuania', 'Europe', True),
        ('LUX', 'Luxembourg', 'Europe', True),
        ('MEX', 'Mexico', 'North America', False),
        ('NLD', 'Netherlands', 'Europe', True),
        ('NZL', 'New Zealand', 'Oceania', False),
        ('NOR', 'Norway', 'Europe', False),
        ('POL', 'Poland', 'Europe', True),
        ('PRT', 'Portugal', 'Europe', True),
        ('SVK', 'Slovak Republic', 'Europe', True),
        ('SVN', 'Slovenia', 'Europe', True),
        ('ESP', 'Spain', 'Europe', True),
        ('SWE', 'Sweden', 'Europe', True),
        ('CHE', 'Switzerland', 'Europe', False),
        ('TUR', 'Turkey', 'Europe/Asia', False),
        ('GBR', 'United Kingdom', 'Europe', False),
        ('USA', 'United States', 'North America', False)
    ]
    
    try:
        engine = db.get_engine()
        if engine is None:
            print("❌ Could not get database engine")
            return False
        
        # Create DataFrame and insert
        countries_df = pd.DataFrame(countries_data, 
                                  columns=['country_code', 'country_name', 'region', 'is_eu_member'])
        
        countries_df.to_sql('countries', engine, if_exists='replace', index=False)
        print("✅ Country data inserted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error inserting country data: {e}")
        return False

def clean_data_for_db(df):
    """Clean data specifically for database insertion"""
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Replace NaN with None for proper NULL handling
    df_clean = df_clean.where(pd.notnull(df_clean), None)
    
    # Handle infinite values
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df_clean[col] = df_clean[col].replace([np.inf, -np.inf], None)
    
    # Ensure proper data types
    if 'year' in df_clean.columns:
        df_clean['year'] = pd.to_numeric(df_clean['year'], errors='coerce')
    
    if 'value' in df_clean.columns:
        df_clean['value'] = pd.to_numeric(df_clean['value'], errors='coerce')
    
    # Map column names to database schema
    column_mapping = {
        'country_code': 'country_code',
        'frequency': 'frequency', 
        'measure_code': 'measure_code',
        'Measure': 'measure_description',
        'erosion_level': 'erosion_level',
        'water_type': 'water_type',
        'nutrient_type': 'nutrient_type',
        'Nutrients': 'nutrients',
        'unit': 'unit',
        'year': 'year',
        'value': 'value',
        'decimals': 'decimals',
        'Decimals': 'decimals_desc',
        'status': 'status',
        'UNIT_MULT': 'unit_mult',
        'BASE_PER': 'base_per',
        'Measure2': 'measure2'
    }
    
    # Only keep columns that exist in both mapping and dataframe
    existing_columns = {k: v for k, v in column_mapping.items() if k in df_clean.columns}
    df_clean = df_clean[list(existing_columns.keys())]
    df_clean = df_clean.rename(columns=existing_columns)
    
    return df_clean

def upload_data_to_neon(batch_size=1000):
    """Upload OECD agricultural data to Neon database"""
    
    try:
        # Load the cleaned data
        print("📊 Loading data...")
        from utils.data_loader import load_data
        df = load_data()
        
        if df is None or df.empty:
            print("❌ No data to upload")
            return False
        
        print(f"📈 Loaded {len(df)} rows")
        
        # Clean data for database
        print("🧹 Cleaning data for database...")
        df_clean = clean_data_for_db(df)
        
        print(f"✅ Cleaned data shape: {df_clean.shape}")
        print(f"✅ Columns: {list(df_clean.columns)}")
        
        # Get database engine
        engine = db.get_engine()
        
        if engine is None:
            print("❌ Could not connect to database")
            return False
        
        # Clear existing data (optional - remove if you want to append)
        print("🗑️ Clearing existing data...")
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE oecd_agricultural_data"))
            conn.commit()
        
        # Upload data in batches
        print(f"⬆️ Uploading data in batches of {batch_size}...")
        
        total_rows = len(df_clean)
        uploaded_rows = 0
        
        for i in range(0, total_rows, batch_size):
            batch = df_clean.iloc[i:i+batch_size]
            
            try:
                batch.to_sql(
                    'oecd_agricultural_data', 
                    engine, 
                    if_exists='append', 
                    index=False,
                    method='multi'
                )
                
                uploaded_rows += len(batch)
                progress = (uploaded_rows / total_rows) * 100
                print(f"📊 Progress: {uploaded_rows}/{total_rows} ({progress:.1f}%)")
                
            except Exception as e:
                print(f"❌ Error uploading batch {i//batch_size + 1}: {e}")
                # Continue with next batch
                continue
        
        print(f"✅ Upload completed! {uploaded_rows} rows uploaded successfully")
        
        # Verify upload
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM oecd_agricultural_data"))
            count = result.scalar()
            print(f"📊 Database now contains {count} rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def load_data_from_db(table_name='oecd_agricultural_data'):
    """
    Load OECD agricultural data from Neon database
    """
    try:
        engine = db.get_engine()
        
        if engine is None:
            print("❌ Could not connect to database")
            return None
        
        # Load all data
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        
        # Map back to expected column names for compatibility
        column_mapping = {
            'measure_description': 'Measure',
            'decimals_desc': 'Decimals',
            'nutrients': 'Nutrients',
            'unit_mult': 'UNIT_MULT',
            'base_per': 'BASE_PER',
            'measure2': 'Measure2'
        }
        
        df = df.rename(columns=column_mapping)
        
        print(f"Loaded {len(df)} rows from database")
        return df
        
    except Exception as e:
        print(f"Error loading data from database: {e}")
        # Fallback to file-based loading
        from utils.data_loader import load_data
        print("Falling back to file-based data loading...")
        return load_data()

def get_data_summary():
    """Get a summary of the uploaded data"""
    
    try:
        engine = db.get_engine()
        
        if engine is None:
            print("❌ Could not connect to database")
            return False
        
        with engine.connect() as conn:
            # Total records
            total_query = text("SELECT COUNT(*) as total FROM oecd_agricultural_data")
            total = pd.read_sql(total_query, conn)
            
            # Countries
            countries_query = text("SELECT COUNT(DISTINCT country_code) as countries FROM oecd_agricultural_data")
            countries = pd.read_sql(countries_query, conn)
            
            # Year range
            years_query = text("SELECT MIN(year) as min_year, MAX(year) as max_year FROM oecd_agricultural_data")
            years = pd.read_sql(years_query, conn)
            
            # Measures
            measures_query = text("SELECT COUNT(DISTINCT measure_code) as measures FROM oecd_agricultural_data")
            measures = pd.read_sql(measures_query, conn)
            
            print("\n📊 Database Summary:")
            print(f"   Total Records: {total['total'].iloc[0]:,}")
            print(f"   Countries: {countries['countries'].iloc[0]}")
            print(f"   Year Range: {years['min_year'].iloc[0]} - {years['max_year'].iloc[0]}")
            print(f"   Measures: {measures['measures'].iloc[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error getting summary: {e}")
        return False