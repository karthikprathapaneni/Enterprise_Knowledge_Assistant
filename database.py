import sqlite3
from datetime import datetime, timedelta
import os
import json
from firebase_manager import (
    is_firebase_connected,
    save_document_firebase,
    save_chat_firebase,
    get_chat_history_firebase,
    get_documents_firebase,
    get_firebase_project_id
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "knowledge.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        
        # 1. Base Users & Auth
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )""")

        # 2. Documents
        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            upload_time TEXT
        )""")

        # 3. Chat History
        cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            answer TEXT,
            time TEXT
        )""")

        # 4. User Profiles & Clearance
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            full_name TEXT,
            department TEXT,
            clearance_level INTEGER,
            title TEXT,
            created_at TEXT
        )""")

        # 5. Document Metadata & Intelligence Cards
        cur.execute("""
        CREATE TABLE IF NOT EXISTS document_metadata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            doc_type TEXT,
            department TEXT,
            clearance_required INTEGER,
            effective_date TEXT,
            expiry_date TEXT,
            risk_level TEXT,
            entities_json TEXT,
            summary_json TEXT,
            created_at TEXT
        )""")

        # 6. Enterprise Tasks (My Work)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            description TEXT,
            priority TEXT,
            due_date TEXT,
            status TEXT,
            source_doc TEXT,
            created_at TEXT
        )""")

        # 7. Knowledge Conflicts & Contradictions
        cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_conflicts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            doc_a TEXT,
            doc_b TEXT,
            description TEXT,
            severity TEXT,
            status TEXT,
            detected_at TEXT
        )""")

        # 8. Intelligence Alerts
        cur.execute("""
        CREATE TABLE IF NOT EXISTS intelligence_alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            title TEXT,
            message TEXT,
            severity TEXT,
            target_role TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TEXT
        )""")

        # 9. Structured Enterprise Data (Text-to-SQL Target)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS structured_enterprise_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT,
            category TEXT,
            metric_name TEXT,
            fiscal_period TEXT,
            amount REAL,
            status TEXT
        )""")

        # 10. Security Audit Events (AI Guard)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS security_audit_events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            username TEXT,
            query TEXT,
            risk_score REAL,
            action_taken TEXT,
            timestamp TEXT
        )""")

        # 11. Human Review Queue (HITL)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS human_review_queue(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_type TEXT,
            requester TEXT,
            payload_json TEXT,
            risk_level TEXT,
            status TEXT,
            reviewed_by TEXT,
            reviewed_at TEXT
        )""")

        # Initial User Records
        cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('admin','admin123','Admin')")
        cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('user','user123','User')")
        cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('manager','manager123','Manager')")

        # Initial Profiles
        cur.execute("INSERT OR IGNORE INTO user_profiles(username,full_name,department,clearance_level,title,created_at) VALUES('admin','Sarah Connor (Admin)','Executive',3,'Chief Security & Information Officer',datetime('now'))")
        cur.execute("INSERT OR IGNORE INTO user_profiles(username,full_name,department,clearance_level,title,created_at) VALUES('manager','Marcus Vance','Operations',2,'Director of Operations & Compliance',datetime('now'))")
        cur.execute("INSERT OR IGNORE INTO user_profiles(username,full_name,department,clearance_level,title,created_at) VALUES('user','Alex Mercer','Engineering',1,'Senior Systems Specialist',datetime('now'))")

        # Seed Initial Structured Enterprise Data
        cur.execute("SELECT COUNT(*) FROM structured_enterprise_data")
        if cur.fetchone()[0] == 0:
            seed_data = [
                ('Finance', 'Cloud Infrastructure', 'AWS & GCP Compute Spend', '2026-Q1', 48500.0, 'Approved'),
                ('Finance', 'Cloud Infrastructure', 'AWS & GCP Compute Spend', '2026-Q2', 52300.0, 'Approved'),
                ('Finance', 'SaaS Licenses', 'Enterprise AI Tooling', '2026-Q1', 28000.0, 'Approved'),
                ('Finance', 'SaaS Licenses', 'Enterprise AI Tooling', '2026-Q2', 31200.0, 'Approved'),
                ('HR', 'Headcount', 'Engineering Personnel', '2026-Q1', 42.0, 'Active'),
                ('HR', 'Headcount', 'Engineering Personnel', '2026-Q2', 48.0, 'Active'),
                ('HR', 'Recruitment', 'Talent Acquisition Cost', '2026-Q1', 19400.0, 'Audited'),
                ('IT', 'Asset Hardware', 'Workstation Upgrades', '2026-Q1', 65000.0, 'Completed'),
                ('IT', 'Asset Hardware', 'Data Center Switches', '2026-Q2', 42000.0, 'In-Review'),
                ('Operations', 'Logistics', 'Regional Distribution Overhead', '2026-Q1', 78900.0, 'Verified'),
                ('Operations', 'Logistics', 'Regional Distribution Overhead', '2026-Q2', 83400.0, 'Pending Approval'),
                ('Compliance', 'Audits', 'SOC2 Type II Examination', '2026-Q1', 35000.0, 'Certified')
            ]
            cur.executemany("INSERT INTO structured_enterprise_data(department,category,metric_name,fiscal_period,amount,status) VALUES(?,?,?,?,?,?)", seed_data)

        # Seed Sample Tasks
        cur.execute("SELECT COUNT(*) FROM tasks")
        if cur.fetchone()[0] == 0:
            sample_tasks = [
                ('admin', 'Verify Travel Policy Q3 Updates', 'Cross-examine expense limits with finance director guidelines', 'High', (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), 'Pending', 'Enterprise_Employee_Handbook_50_Pages.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                ('user', 'Submit Quarterly Cyber Hygiene Attestation', 'Complete mandatory security training and device encryption audit', 'Medium', (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'), 'In Progress', 'Saveetha norms.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                ('manager', 'Review IT VPN SOP Escalation Procedure', 'Finalize new two-factor onboarding runbook for remote contractors', 'High', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), 'Pending', 'IT_Troubleshooting_SOP.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]
            cur.executemany("INSERT INTO tasks(username,title,description,priority,due_date,status,source_doc,created_at) VALUES(?,?,?,?,?,?,?,?)", sample_tasks)

        # Seed Sample Alerts
        cur.execute("SELECT COUNT(*) FROM intelligence_alerts")
        if cur.fetchone()[0] == 0:
            sample_alerts = [
                ('Policy Conflict', 'Potential Travel Expense Limit Discrepancy', 'Document A specifies $50/day per-diem while Handbook v4 lists $65/day.', 'High', 'All', 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                ('Regulatory Deadline', 'Quarterly Compliance Attestation Window Closes Soon', 'All personnel must submit compliance confirmations by Friday 5 PM.', 'Medium', 'All', 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                ('Knowledge Update', 'New Hospital Appointment Management System Architecture Ingested', 'System workflow schemas and database entity mappings are now indexed.', 'Low', 'All', 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]
            cur.executemany("INSERT INTO intelligence_alerts(alert_type,title,message,severity,target_role,is_read,created_at) VALUES(?,?,?,?,?,?,?)", sample_alerts)

        # Seed Sample Conflicts
        cur.execute("SELECT COUNT(*) FROM knowledge_conflicts")
        if cur.fetchone()[0] == 0:
            sample_conflicts = [
                ('Remote Work Authorization', 'Saveetha norms.pdf (Page 14)', 'Enterprise_Employee_Handbook_50_Pages.pdf (Page 22)', 'Document A states on-site presence is mandatory 4 days per week, whereas Document B outlines flexible 3-day hybrid schedules for senior roles.', 'High', 'Open', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                ('Expense Reimbursement Window', 'Finance Policy Bulletin 2026', 'Staff Handbook General Provisions', 'Bulletin specifies receipt filing within 14 calendar days; General Handbook indicates 30 calendar days.', 'Medium', 'Open', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]
            cur.executemany("INSERT INTO knowledge_conflicts(topic,doc_a,doc_b,description,severity,status,detected_at) VALUES(?,?,?,?,?,?,?)", sample_conflicts)

        conn.commit()

# --- Auth & Profiles ---
def verify_user(username, password):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cur.fetchone()
        return result[0] if result else None

def get_user_profile(username):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT full_name, department, clearance_level, title FROM user_profiles WHERE username=?", (username,))
        row = cur.fetchone()
        if row:
            return {"full_name": row[0], "department": row[1], "clearance_level": row[2], "title": row[3]}
        # Fallback profile based on username
        role = "Admin" if username.lower() == "admin" else "User"
        lvl = 3 if role == "Admin" else 1
        return {"full_name": username.capitalize(), "department": "General", "clearance_level": lvl, "title": f"Enterprise {role}"}

# --- Tasks (My Work) ---
def get_tasks(username=None):
    with get_connection() as conn:
        cur = conn.cursor()
        if username and username.lower() != "admin":
            cur.execute("SELECT id, username, title, description, priority, due_date, status, source_doc, created_at FROM tasks WHERE username=? ORDER BY id DESC", (username,))
        else:
            cur.execute("SELECT id, username, title, description, priority, due_date, status, source_doc, created_at FROM tasks ORDER BY id DESC")
        rows = cur.fetchall()
        return [{
            "id": r[0], "username": r[1], "title": r[2], "description": r[3],
            "priority": r[4], "due_date": r[5], "status": r[6], "source_doc": r[7], "created_at": r[8]
        } for r in rows]

def add_task(username, title, description, priority="Medium", due_date=None, source_doc=None):
    if not due_date:
        due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks(username, title, description, priority, due_date, status, source_doc, created_at) VALUES(?,?,?,?,?,?,?,?)",
            (username, title, description, priority, due_date, "Pending", source_doc or "AI Assistant", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

def update_task_status(task_id, new_status):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
        conn.commit()

# --- Intelligence Alerts ---
def get_alerts(role=None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, alert_type, title, message, severity, target_role, is_read, created_at FROM intelligence_alerts ORDER BY id DESC")
        rows = cur.fetchall()
        return [{
            "id": r[0], "alert_type": r[1], "title": r[2], "message": r[3],
            "severity": r[4], "target_role": r[5], "is_read": bool(r[6]), "created_at": r[7]
        } for r in rows]

def mark_alert_read(alert_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE intelligence_alerts SET is_read=1 WHERE id=?", (alert_id,))
        conn.commit()

# --- Knowledge Conflicts ---
def get_conflicts():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, topic, doc_a, doc_b, description, severity, status, detected_at FROM knowledge_conflicts ORDER BY id DESC")
        rows = cur.fetchall()
        return [{
            "id": r[0], "topic": r[1], "doc_a": r[2], "doc_b": r[3],
            "description": r[4], "severity": r[5], "status": r[6], "detected_at": r[7]
        } for r in rows]

def add_conflict(topic, doc_a, doc_b, description, severity="High"):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO knowledge_conflicts(topic, doc_a, doc_b, description, severity, status, detected_at) VALUES(?,?,?,?,?,?,?)",
            (topic, doc_a, doc_b, description, severity, "Open", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

# --- Document Metadata ---
def save_document_metadata(filename, doc_type="Policy", department="General", clearance_required=1, risk_level="Low", entities=None, summary=None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO document_metadata(filename, doc_type, department, clearance_required, effective_date, expiry_date, risk_level, entities_json, summary_json, created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            filename, doc_type, department, clearance_required,
            datetime.now().strftime("%Y-%m-%d"),
            (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            risk_level,
            json.dumps(entities or []),
            json.dumps(summary or {}),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()

def get_document_metadata(filename=None):
    with get_connection() as conn:
        cur = conn.cursor()
        if filename:
            cur.execute("SELECT filename, doc_type, department, clearance_required, effective_date, expiry_date, risk_level, entities_json, summary_json FROM document_metadata WHERE filename=?", (filename,))
            r = cur.fetchone()
            if r:
                return {
                    "filename": r[0], "doc_type": r[1], "department": r[2], "clearance_required": r[3],
                    "effective_date": r[4], "expiry_date": r[5], "risk_level": r[6],
                    "entities": json.loads(r[7]) if r[7] else [],
                    "summary": json.loads(r[8]) if r[8] else {}
                }
            return None
        else:
            cur.execute("SELECT filename, doc_type, department, clearance_required, effective_date, expiry_date, risk_level FROM document_metadata ORDER BY id DESC")
            rows = cur.fetchall()
            return [{
                "filename": r[0], "doc_type": r[1], "department": r[2], "clearance_required": r[3],
                "effective_date": r[4], "expiry_date": r[5], "risk_level": r[6]
            } for r in rows]

# --- Structured Data Execution (Safe Text-to-SQL) ---
def execute_safe_sql(sql_query):
    """Executes validated, read-only SQL queries against structured enterprise data."""
    cleaned = sql_query.strip().rstrip(";").lower()
    # Enforce strict read-only safety guardrails
    forbidden = ["drop", "delete", "update", "insert", "alter", "create", "truncate", "replace", "grant", "revoke"]
    for word in forbidden:
        if word in cleaned.split():
            return {"success": False, "error": f"Security Violation: '{word.upper()}' commands are strictly prohibited in analytical read-only mode."}
            
    if not cleaned.startswith("select"):
        return {"success": False, "error": "Only SELECT queries are permitted on structured enterprise tables."}

    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql_query)
            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = cur.fetchall()
            return {"success": True, "columns": columns, "rows": rows, "count": len(rows)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- Security Audit Events (AI Guard) ---
def log_security_event(event_type, username, query, risk_score=0.0, action_taken="Monitored"):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO security_audit_events(event_type, username, query, risk_score, action_taken, timestamp) VALUES(?,?,?,?,?,?)",
            (event_type, username, query, risk_score, action_taken, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

def get_security_events():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, event_type, username, query, risk_score, action_taken, timestamp FROM security_audit_events ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
        return [{
            "id": r[0], "event_type": r[1], "username": r[2], "query": r[3],
            "risk_score": r[4], "action_taken": r[5], "timestamp": r[6]
        } for r in rows]

# --- Base Document & Chat (Existing & Backward-Compatible) ---
def add_document(filename):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO documents(filename, upload_time) VALUES(?,?)",
            (filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    if is_firebase_connected():
        save_document_firebase(filename)

def save_chat(username, question, answer):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history(username, question, answer, time) VALUES(?,?,?,?)",
            (username, question, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    if is_firebase_connected():
        save_chat_firebase(username, question, answer)

def get_chat_history(prefer_cloud=False):
    if prefer_cloud and is_firebase_connected():
        cloud_history = get_chat_history_firebase()
        if cloud_history:
            return cloud_history
            
    with get_connection() as conn:
        return conn.execute("SELECT username, question, answer, time FROM chat_history ORDER BY id DESC").fetchall()

def get_documents(prefer_cloud=False):
    if prefer_cloud and is_firebase_connected():
        cloud_docs = get_documents_firebase()
        if cloud_docs:
            return cloud_docs

    with get_connection() as conn:
        return conn.execute("SELECT filename, upload_time FROM documents ORDER BY id DESC").fetchall()

def clear_chat_history():
    with get_connection() as conn:
        conn.execute("DELETE FROM chat_history")
        conn.commit()

def get_db_status():
    if is_firebase_connected():
        return {
            "mode": "Hybrid Cloud Sync (Firebase Firestore + SQLite)",
            "firebase_status": "ONLINE",
            "project_id": get_firebase_project_id()
        }
    return {
        "mode": "Local Relational DB (SQLite)",
        "firebase_status": "STANDBY (Credentials needed)",
        "project_id": "Not Configured"
    }