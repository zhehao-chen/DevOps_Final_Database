#!/usr/bin/env python3
"""
Database setup and initialization script
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'database': 'postgres' 
}

DB_NAME = os.getenv('DB_NAME', 'ecommerce')

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"✓ Database '{DB_NAME}' created successfully")
        else:
            print(f"✓ Database '{DB_NAME}' already exists")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False

def initialize_schema():
    """Initialize database schema"""
    try:
        # Connect to the ecommerce database
        conn = psycopg2.connect(**{**DB_CONFIG, 'database': DB_NAME})
        cur = conn.cursor()
        
        # Read and execute schema file
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        
        cur.execute(schema_sql)
        conn.commit()
        
        print("✓ Database schema initialized successfully")
        
        # Verify tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"✓ Created tables: {', '.join([t[0] for t in tables])}")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error initializing schema: {e}")
        return False

def verify_connection():
    """Verify database connection"""
    try:
        conn = psycopg2.connect(**{**DB_CONFIG, 'database': DB_NAME})
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM products')
        count = cur.fetchone()[0]
        print(f"✓ Connection verified. Products in database: {count}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error verifying connection: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("E-Commerce Database Setup")
    print("=" * 60)
    
    print("\n1. Creating database...")
    if not create_database():
        exit(1)
    
    print("\n2. Initializing schema...")
    if not initialize_schema():
        exit(1)
    
    print("\n3. Verifying connection...")
    if not verify_connection():
        exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
