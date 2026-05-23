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
            ("CICD Health", "Overall health and reliability of the CI/CD pipeline including release frequency, build success rate, and pipeline reliability"),
            ("Vuln Remediation", "Time to fix security vulnerabilities — tracks open vulns, remediation velocity, and SLA compliance"),
            ("Deployment Success Rate", "Percentage of deployments that complete successfully without rollback or incident"),
            ("Test Coverage", "Percentage of codebase covered by automated tests — unit, integration, and end-to-end"),
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

def save_annotation(metric_id, current_value, classification, explanation, remediation_owner_id=None, expected_resolution_date=None):
    """Insert a new metric annotation and return its id, or None on failure."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO metric_annotations
                (metric_id, current_value, classification, explanation, remediation_owner_id, expected_resolution_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (metric_id, current_value, classification, explanation, remediation_owner_id, expected_resolution_date))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    except Exception as e:
        print(f"❌ Failed to save annotation: {e}")
        return None


def save_blocker(description, open_since, what_tried, options_remaining, escalation_type, specific_ask):
    """Insert a new manager blocker and return its id, or None on failure."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO manager_blockers
                (description, open_since, what_tried, options_remaining, escalation_type, specific_ask)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (description, str(open_since), what_tried, options_remaining, escalation_type, specific_ask))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    except Exception as e:
        print(f"❌ Failed to save blocker: {e}")
        return None


def get_active_blockers():
    """Return all unresolved blockers in reverse chronological order."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM manager_blockers
            WHERE resolved = 0
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to get active blockers: {e}")
        return []


def get_resolved_blockers():
    """Return all resolved blockers in reverse chronological order of resolution."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM manager_blockers
            WHERE resolved = 1
            ORDER BY resolved_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to get resolved blockers: {e}")
        return []


def detect_aging_blockers():
    """Return all unresolved blockers that have been open for 14 or more days."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM manager_blockers
            WHERE resolved = 0
              AND julianday('now') - julianday(open_since) >= 14
            ORDER BY open_since ASC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to detect aging blockers: {e}")
        return []


def resolve_blocker(blocker_id, resolved_at, resolution_description):
    """Set resolved=1, resolved_at, and resolution_description on a blocker. Returns True on success."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE manager_blockers
            SET resolved = 1,
                resolved_at = ?,
                resolution_description = ?
            WHERE id = ?
        """, (str(resolved_at), resolution_description, blocker_id))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Failed to resolve blocker: {e}")
        return False


def get_metric_annotations(metric_id):
    """Return all annotations for a metric in reverse chronological order, joining engineer name."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ma.*, e.name AS remediation_owner_name
            FROM metric_annotations ma
            LEFT JOIN engineers e ON ma.remediation_owner_id = e.id
            WHERE ma.metric_id = ?
            ORDER BY ma.annotated_at DESC
        """, (metric_id,))
        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to get metric annotations: {e}")
        return []


def detect_metric_trends():
    """Scan all active metrics and return trend flags based on annotation history.

    Checks three patterns per metric:
    - sustained_red:          classification == 'Red' for 2+ consecutive annotations
    - improving_trend:        classification improves across 3+ consecutive annotations
                              (Red → Orange/Amber, Orange → Amber)
    - sustained_improvement:  a non-Red classification is maintained for 4+ consecutive annotations

    Returns a list of dicts: metric_id, metric_name, flag_type, duration.
    """
    SEVERITY = {'Red': 3, 'Orange': 2, 'Amber': 1}

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM metrics WHERE is_active = 1")
        metrics = [dict(r) for r in cursor.fetchall()]

        flags = []

        for metric in metrics:
            mid = metric['id']
            mname = metric['name']

            cursor.execute("""
                SELECT classification
                FROM metric_annotations
                WHERE metric_id = ?
                ORDER BY annotated_at DESC
            """, (mid,))
            rows = [r['classification'] for r in cursor.fetchall()]

            if not rows:
                continue

            # ── Sustained Red: 2+ consecutive Red ─────────────────────────
            streak = 0
            for c in rows:
                if c == 'Red':
                    streak += 1
                else:
                    break
            if streak >= 2:
                flags.append({'metric_id': mid, 'metric_name': mname,
                               'flag_type': 'sustained_red', 'duration': streak})

            # ── Improving trend: severity strictly decreasing across 3+ consecutive ──
            if len(rows) >= 3:
                improving_streak = 1
                for i in range(1, len(rows)):
                    prev_sev = SEVERITY.get(rows[i - 1], 0)
                    curr_sev = SEVERITY.get(rows[i], 0)
                    # rows are newest-first, so "improving" means newer < older severity
                    if prev_sev < curr_sev:
                        improving_streak += 1
                    else:
                        break
                if improving_streak >= 3:
                    flags.append({'metric_id': mid, 'metric_name': mname,
                                  'flag_type': 'improving_trend', 'duration': improving_streak})

            # ── Sustained improvement: non-Red for 4+ consecutive ─────────
            streak = 0
            for c in rows:
                if c != 'Red':
                    streak += 1
                else:
                    break
            if streak >= 4:
                flags.append({'metric_id': mid, 'metric_name': mname,
                               'flag_type': 'sustained_improvement', 'duration': streak})

        conn.close()
        return flags

    except Exception as e:
        print(f"❌ Failed to detect metric trends: {e}")
        return []


def get_metric_trend_flags():
    """Return all active metric trend flags by calling detect_metric_trends().

    Each entry contains: metric_id, metric_name, flag_type, duration.
    """
    return detect_metric_trends()


def update_strategic_context(metric_id, new_context):
    """Update strategic_context on a metric and archive the previous value to history.

    Returns True on success, False on failure.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch current context before overwriting
        cursor.execute("SELECT strategic_context FROM metrics WHERE id = ?", (metric_id,))
        row = cursor.fetchone()
        if row is None:
            conn.close()
            return False
        previous_context = row['strategic_context']

        # Save previous value to history (even if it was NULL)
        cursor.execute("""
            INSERT INTO strategic_context_history (metric_id, previous_context, new_context)
            VALUES (?, ?, ?)
        """, (metric_id, previous_context, new_context))

        # Update the metric
        cursor.execute("""
            UPDATE metrics
            SET strategic_context = ?, strategic_context_updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_context, metric_id))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Failed to update strategic context: {e}")
        return False


def get_strategic_context_history(metric_id):
    """Return all historical strategic contexts for a metric in reverse chronological order."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT previous_context, new_context, changed_at
            FROM strategic_context_history
            WHERE metric_id = ?
            ORDER BY changed_at DESC
        """, (metric_id,))
        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to get strategic context history: {e}")
        return []


def get_all_metrics():
    """Returns all active metrics ordered by default metrics first, then custom ones alphabetically"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM metrics
            WHERE is_active = 1
            ORDER BY is_default DESC, name ASC
        """)
        metrics = cursor.fetchall()

        conn.close()
        return [dict(m) for m in metrics]

    except Exception as e:
        print(f"❌ Failed to get metrics: {e}")
        return []


def add_custom_metric(name, description=None):
    """Inserts a new custom metric with is_default=0 and returns the new id, or None on failure"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO metrics (name, description, is_default, is_active)
            VALUES (?, ?, 0, 1)
        """, (name, description))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    except Exception as e:
        print(f"❌ Failed to add custom metric: {e}")
        return None


def deactivate_metric(metric_id):
    """Sets is_active to 0 for the given metric, preserving all historical annotation data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE metrics SET is_active = 0 WHERE id = ?
        """, (metric_id,))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Failed to deactivate metric: {e}")
        return False


def get_signals(engineer_id=None, start_date=None, end_date=None, delivery_signal=None, stress_level=None, uncertainty_level=None):
    """Return signals in reverse chronological order with optional filters.

    Joins engineers so each row includes engineer_name. All filter params are optional.
    start_date and end_date are inclusive and should be date or datetime objects (or ISO strings).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT s.*, e.name AS engineer_name
            FROM signals s
            JOIN engineers e ON s.engineer_id = e.id
            WHERE 1=1
        """
        params = []

        if engineer_id is not None:
            query += " AND s.engineer_id = ?"
            params.append(engineer_id)
        if start_date is not None:
            query += " AND DATE(s.logged_at) >= DATE(?)"
            params.append(str(start_date))
        if end_date is not None:
            query += " AND DATE(s.logged_at) <= DATE(?)"
            params.append(str(end_date))
        if delivery_signal is not None:
            query += " AND s.delivery_signal = ?"
            params.append(delivery_signal)
        if stress_level is not None:
            query += " AND s.stress_level = ?"
            params.append(stress_level)
        if uncertainty_level is not None:
            query += " AND s.uncertainty_level = ?"
            params.append(uncertainty_level)

        query += " ORDER BY s.logged_at DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    except Exception as e:
        print(f"❌ Failed to get signals: {e}")
        return []


def save_signal(engineer_id, energy_level, delivery_signal, growth_signal, stress_level, stress_source, uncertainty_level, uncertainty_source, observation):
    """Insert a new signal record and return the id of the newly created record"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO signals (engineer_id, energy_level, delivery_signal, growth_signal, stress_level, stress_source, uncertainty_level, uncertainty_source, observation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (engineer_id, energy_level, delivery_signal, growth_signal, stress_level, stress_source, uncertainty_level, uncertainty_source, observation))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    except Exception as e:
        print(f"❌ Failed to save signal: {e}")
        return None


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

def detect_trends():
    """Scan all engineers' signals and return a list of active trend flags.

    Checks four patterns per engineer:
    - stress_trend:      stress_level == 'High' for 3+ consecutive check-ins
    - uncertainty_trend: uncertainty_level == 'High' for 2+ consecutive check-ins
    - delivery_trend:    delivery_signal in ('Blocked', 'At Risk') for 2+ consecutive check-ins
    - energy_trend:      average energy_level < 3 across 3+ check-ins in the last 30 days

    Returns a list of dicts: engineer_id, engineer_name, flag_type, duration.
    duration = consecutive check-in count (or check-in count for energy).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM engineers WHERE active = 1")
        engineers = [dict(row) for row in cursor.fetchall()]

        flags = []

        for engineer in engineers:
            eid = engineer['id']
            ename = engineer['name']

            # Fetch all signals newest-first for consecutive streak checks
            cursor.execute("""
                SELECT stress_level, uncertainty_level, delivery_signal, energy_level, logged_at
                FROM signals
                WHERE engineer_id = ?
                ORDER BY logged_at DESC
            """, (eid,))
            rows = [dict(r) for r in cursor.fetchall()]

            if not rows:
                continue

            # ── Stress: 3+ consecutive 'High' ─────────────────────────────
            streak = 0
            for row in rows:
                if row['stress_level'] == 'High':
                    streak += 1
                else:
                    break
            if streak >= 3:
                flags.append({
                    'engineer_id': eid,
                    'engineer_name': ename,
                    'flag_type': 'stress_trend',
                    'duration': streak,
                })

            # ── Uncertainty: 2+ consecutive 'High' ────────────────────────
            streak = 0
            for row in rows:
                if row['uncertainty_level'] == 'High':
                    streak += 1
                else:
                    break
            if streak >= 2:
                flags.append({
                    'engineer_id': eid,
                    'engineer_name': ename,
                    'flag_type': 'uncertainty_trend',
                    'duration': streak,
                })

            # ── Delivery: 2+ consecutive 'Blocked' or 'At Risk' ───────────
            streak = 0
            for row in rows:
                if row['delivery_signal'] in ('Blocked', 'At Risk'):
                    streak += 1
                else:
                    break
            if streak >= 2:
                flags.append({
                    'engineer_id': eid,
                    'engineer_name': ename,
                    'flag_type': 'delivery_trend',
                    'duration': streak,
                })

            # ── Energy: avg < 3 across 3+ check-ins in the last 30 days ──
            cursor.execute("""
                SELECT energy_level
                FROM signals
                WHERE engineer_id = ?
                  AND logged_at >= datetime('now', '-30 days')
                ORDER BY logged_at DESC
            """, (eid,))
            energy_rows = cursor.fetchall()
            if len(energy_rows) >= 3:
                avg_energy = sum(r['energy_level'] for r in energy_rows) / len(energy_rows)
                if avg_energy < 3:
                    flags.append({
                        'engineer_id': eid,
                        'engineer_name': ename,
                        'flag_type': 'energy_trend',
                        'duration': len(energy_rows),
                    })

        conn.close()
        return flags

    except Exception as e:
        print(f"❌ Failed to detect trends: {e}")
        return []


def get_active_trend_flags():
    """Return all active trend flags across all engineers by calling detect_trends().

    Each entry contains: engineer_id, engineer_name, flag_type, duration.
    """
    return detect_trends()


def save_brief(period_start, period_end, generated_content, edited_content=None):
    """Insert a new brief record and return its id, or None on failure."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO briefs (period_start, period_end, generated_content, edited_content)
            VALUES (?, ?, ?, ?)
        """, (str(period_start), str(period_end), generated_content, edited_content))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    except Exception as e:
        print(f"❌ Failed to save brief: {e}")
        return None


def update_brief_edited_content(brief_id, edited_content):
    """Update the edited_content field of an existing brief. Returns True on success."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE briefs SET edited_content = ? WHERE id = ?
        """, (edited_content, brief_id))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Failed to update brief edited content: {e}")
        return False


def get_all_briefs():
    """Return all briefs in reverse chronological order.

    Each row includes: id, period_start, period_end, generated_content,
    edited_content, generated_at.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, period_start, period_end, generated_content,
                   edited_content, generated_at
            FROM briefs
            ORDER BY generated_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]

    except Exception as e:
        print(f"❌ Failed to get briefs: {e}")
        return []


def detect_team_wide_patterns():
    """Detect patterns where 50%+ of the team shows the same signal over an extended period.

    Checks:
    - stress_pattern:      50%+ of engineers with signals have High stress in every signal
                           within the last 42 days (6 weeks)
    - uncertainty_pattern: 50%+ of engineers with signals have High uncertainty in every signal
                           within the last 21 days (3 weeks)

    Returns a list of dicts: pattern_type, affected_count, team_size, percentage, duration_weeks.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM engineers WHERE active = 1")
        engineers = [dict(r) for r in cursor.fetchall()]
        team_size = len(engineers)

        if team_size == 0:
            conn.close()
            return []

        patterns = []

        # ── Stress pattern: all signals in last 42 days are 'High' ────────────
        stress_affected = 0
        for eng in engineers:
            cursor.execute("""
                SELECT stress_level FROM signals
                WHERE engineer_id = ?
                  AND logged_at >= datetime('now', '-42 days')
                ORDER BY logged_at DESC
            """, (eng['id'],))
            rows = [r['stress_level'] for r in cursor.fetchall()]
            if rows and all(s == 'High' for s in rows):
                stress_affected += 1

        if stress_affected > 0 and (stress_affected / team_size) >= 0.5:
            patterns.append({
                'pattern_type': 'stress_pattern',
                'affected_count': stress_affected,
                'team_size': team_size,
                'percentage': round((stress_affected / team_size) * 100),
                'duration_weeks': 6,
            })

        # ── Uncertainty pattern: all signals in last 21 days are 'High' ───────
        uncertainty_affected = 0
        for eng in engineers:
            cursor.execute("""
                SELECT uncertainty_level FROM signals
                WHERE engineer_id = ?
                  AND logged_at >= datetime('now', '-21 days')
                ORDER BY logged_at DESC
            """, (eng['id'],))
            rows = [r['uncertainty_level'] for r in cursor.fetchall()]
            if rows and all(u == 'High' for u in rows):
                uncertainty_affected += 1

        if uncertainty_affected > 0 and (uncertainty_affected / team_size) >= 0.5:
            patterns.append({
                'pattern_type': 'uncertainty_pattern',
                'affected_count': uncertainty_affected,
                'team_size': team_size,
                'percentage': round((uncertainty_affected / team_size) * 100),
                'duration_weeks': 3,
            })

        conn.close()
        return patterns

    except Exception as e:
        print(f"❌ Failed to detect team-wide patterns: {e}")
        return []


def get_brief_data(start_date, end_date):
    """Aggregate all data needed to generate a leadership brief for the given date range.

    Returns a dict with:
    - signals:              list of signal dicts (with engineer_name) in the date range
    - metric_annotations:  list of the most recent annotation per active metric
    - trend_flags:         list of active engineer trend flags (all time)
    - metric_trend_flags:  list of active metric trend flags (all time)
    - active_blockers:     list of unresolved blockers
    - aging_blocker_ids:   set of blocker ids open for 14+ days
    - team_wide_patterns:  list of team-wide pattern alerts
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Signals in date range with engineer names
        cursor.execute("""
            SELECT s.*, e.name AS engineer_name
            FROM signals s
            JOIN engineers e ON s.engineer_id = e.id
            WHERE DATE(s.logged_at) >= DATE(?)
              AND DATE(s.logged_at) <= DATE(?)
            ORDER BY s.logged_at DESC
        """, (str(start_date), str(end_date)))
        signals = [dict(r) for r in cursor.fetchall()]

        # Most recent annotation per active metric
        cursor.execute("""
            SELECT ma.*, m.name AS metric_name, m.strategic_context,
                   e.name AS remediation_owner_name
            FROM metric_annotations ma
            JOIN metrics m ON ma.metric_id = m.id
            LEFT JOIN engineers e ON ma.remediation_owner_id = e.id
            WHERE m.is_active = 1
              AND ma.id = (
                  SELECT id FROM metric_annotations
                  WHERE metric_id = m.id
                  ORDER BY annotated_at DESC
                  LIMIT 1
              )
            ORDER BY ma.annotated_at DESC
        """)
        metric_annotations = [dict(r) for r in cursor.fetchall()]

        # Active blockers
        cursor.execute("""
            SELECT * FROM manager_blockers
            WHERE resolved = 0
            ORDER BY open_since ASC
        """)
        active_blockers = [dict(r) for r in cursor.fetchall()]

        # Aging blocker ids
        cursor.execute("""
            SELECT id FROM manager_blockers
            WHERE resolved = 0
              AND julianday('now') - julianday(open_since) >= 14
        """)
        aging_blocker_ids = {r['id'] for r in cursor.fetchall()}

        conn.close()

        return {
            'signals': signals,
            'metric_annotations': metric_annotations,
            'trend_flags': detect_trends(),
            'metric_trend_flags': detect_metric_trends(),
            'active_blockers': active_blockers,
            'aging_blocker_ids': aging_blocker_ids,
            'team_wide_patterns': detect_team_wide_patterns(),
        }

    except Exception as e:
        print(f"❌ Failed to get brief data: {e}")
        return {
            'signals': [],
            'metric_annotations': [],
            'trend_flags': [],
            'metric_trend_flags': [],
            'active_blockers': [],
            'aging_blocker_ids': set(),
            'team_wide_patterns': [],
        }


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
