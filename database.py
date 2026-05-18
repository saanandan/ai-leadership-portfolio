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

def init_db():
    """Create the database file at data/leadership_signals.db if it doesn't already exist"""
    try:
        # Check if database file already exists
        if os.path.exists(DB_PATH):
            print(f"✅ Database already exists at {DB_PATH}")
            return True
        
        # Create the database file by establishing a connection
        conn = get_connection()
        conn.close()
        
        print(f"✅ Database file created at {DB_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database file: {e}")
        return False

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

def create_engineers_table():
    """Create the engineers table with columns: id, name, role, active, created_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS engineers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Engineers table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create engineers table: {e}")
        return False

def create_signals_table():
    """Create the signals table with columns: id, engineer_id, energy_level, delivery_signal, growth_signal, stress_level, stress_source, uncertainty_level, uncertainty_source, observation, logged_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                engineer_id INTEGER NOT NULL,
                energy_level INTEGER NOT NULL,
                delivery_signal TEXT NOT NULL,
                growth_signal TEXT NOT NULL,
                stress_level TEXT NOT NULL,
                stress_source TEXT,
                uncertainty_level TEXT NOT NULL,
                uncertainty_source TEXT,
                observation TEXT,
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (engineer_id) REFERENCES engineers (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Signals table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create signals table: {e}")
        return False

def create_metrics_table():
    """Create the metrics table with columns: id, name, description, is_default, is_active, strategic_context, strategic_context_updated_at, created_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                is_default INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                strategic_context TEXT,
                strategic_context_updated_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Metrics table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create metrics table: {e}")
        return False

def create_metric_annotations_table():
    """Create the metric_annotations table with columns: id, metric_id, current_value, classification, explanation, remediation_owner_id, expected_resolution_date, annotated_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metric_annotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER NOT NULL,
                current_value TEXT NOT NULL,
                classification TEXT NOT NULL,
                explanation TEXT NOT NULL,
                remediation_owner_id INTEGER,
                expected_resolution_date TIMESTAMP,
                annotated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metric_id) REFERENCES metrics (id),
                FOREIGN KEY (remediation_owner_id) REFERENCES engineers (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Metric annotations table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create metric annotations table: {e}")
        return False

def create_strategic_context_history_table():
    """Create the strategic_context_history table with columns: id, metric_id, previous_context, new_context, changed_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategic_context_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER NOT NULL,
                previous_context TEXT,
                new_context TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metric_id) REFERENCES metrics (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Strategic context history table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create strategic context history table: {e}")
        return False

def create_manager_blockers_table():
    """Create the manager_blockers table with columns: id, description, open_since, what_tried, options_remaining, escalation_type, specific_ask, resolved, resolved_at, resolution_description, created_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manager_blockers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                open_since DATE NOT NULL,
                what_tried TEXT NOT NULL,
                options_remaining TEXT NOT NULL,
                escalation_type TEXT NOT NULL,
                specific_ask TEXT NOT NULL,
                resolved INTEGER DEFAULT 0,
                resolved_at TIMESTAMP,
                resolution_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Manager blockers table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create manager blockers table: {e}")
        return False

def create_briefs_table():
    """Create the briefs table with columns: id, period_start, period_end, generated_content, edited_content, generated_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_start DATE NOT NULL,
                period_end DATE NOT NULL,
                generated_content TEXT NOT NULL,
                edited_content TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Briefs table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create briefs table: {e}")
        return False

def create_retrospectives_table():
    """Create the retrospectives table with columns: id, period_start, period_end, content, generated_at"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retrospectives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_start DATE NOT NULL,
                period_end DATE NOT NULL,
                content TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Retrospectives table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create retrospectives table: {e}")
        return False

def create_app_state_table():
    """Create the app_state table with columns: id, key, value"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ App state table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create app state table: {e}")
        return False

def get_all_engineers():
    """Returns all active engineers"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM engineers WHERE active = 1 ORDER BY name")
        engineers = cursor.fetchall()
        
        conn.close()
        return [dict(engineer) for engineer in engineers]
        
    except Exception as e:
        print(f"❌ Failed to get engineers: {e}")
        return []

def add_engineer(name, role=None):
    """Inserts a new engineer"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO engineers (name, role) VALUES (?, ?)
        """, (name, role))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Engineer '{name}' added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add engineer: {e}")
        return False

def deactivate_engineer(engineer_id):
    """Sets engineer active status to 0"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE engineers SET active = 0 WHERE id = ?
        """, (engineer_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Engineer {engineer_id} deactivated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to deactivate engineer: {e}")
        return False

def seed_default_metrics():
    """Inserts four default metrics if they don't already exist"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        default_metrics = [
            ("Release Frequency", "How often the team releases software to production"),
            ("Vuln Remediation", "Time to fix security vulnerabilities"),
            ("CICD Health", "Overall health and reliability of CI/CD pipeline"),
            ("Deployment Success Rate", "Percentage of successful deployments")
        ]
        
        for name, description in default_metrics:
            # Check if metric already exists
            cursor.execute("SELECT id FROM metrics WHERE name = ?", (name,))
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO metrics (name, description, is_default) VALUES (?, ?, 1)
                """, (name, description))
                print(f"✅ Default metric '{name}' added!")
        
        conn.commit()
        conn.close()
        
        print("✅ Default metrics seeded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed default metrics: {e}")
        return False

def delete_signal(signal_id):
    """Delete a signal record by id"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM signals WHERE id = ?
        """, (signal_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Signal {signal_id} deleted successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to delete signal: {e}")
        return False

def initialize_database():
    """Initialize all database tables (will be expanded in future tasks)"""
    try:
        # Create the database file if it doesn't exist
        if not init_db():
            raise Exception("Failed to create database file")
        
        # Create all tables in correct order (tables without dependencies first)
        if not create_engineers_table():
            raise Exception("Failed to create engineers table")
        if not create_metrics_table():
            raise Exception("Failed to create metrics table")
        if not create_signals_table():
            raise Exception("Failed to create signals table")
        if not create_metric_annotations_table():
            raise Exception("Failed to create metric annotations table")
        if not create_strategic_context_history_table():
            raise Exception("Failed to create strategic context history table")
        if not create_manager_blockers_table():
            raise Exception("Failed to create manager blockers table")
        if not create_briefs_table():
            raise Exception("Failed to create briefs table")
        if not create_retrospectives_table():
            raise Exception("Failed to create retrospectives table")
        if not create_app_state_table():
            raise Exception("Failed to create app state table")
        
        # Seed default data
        if not seed_default_metrics():
            raise Exception("Failed to seed default metrics")
        
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
