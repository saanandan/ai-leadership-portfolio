import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'leadership_signals.db')

def get_connection():
    """Create and return a database connection"""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    return conn

def test_connection():
    """Test basic SQLite functionality"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT datetime('now') as current_time")
        result = cursor.fetchone()
        
        conn.close()
        
        print(f"✅ SQLite connection test successful!")
        print(f"   Current time from database: {result['current_time']}")
        print(f"   Database file: {DB_PATH}")
        
        return True
        
    except Exception as e:
        print(f"❌ SQLite connection test failed: {e}")
        return False

def initialize_database():
    """Initialize all database tables (will be expanded in future tasks)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create a simple test table for now
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert a test record
        cursor.execute("""
            INSERT INTO test_table (message) VALUES (?)
        """, ("Database initialized successfully!",))
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests when this file is executed directly
    print("Testing SQLite database operations...")
    
    if test_connection():
        initialize_database()
        print("🎉 Database setup complete!")
    else:
        print("💥 Database setup failed!")
