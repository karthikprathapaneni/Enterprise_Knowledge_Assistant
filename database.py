import sqlite3
from datetime import datetime
import os
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
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            answer TEXT,
            time TEXT
        )""")

        cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('admin','admin123','Admin')")
        cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('user','user123','User')")
        conn.commit()

def verify_user(username, password):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cur.fetchone()
        return result[0] if result else None

def add_document(filename):
    # 1. Save to local SQLite
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO documents(filename, upload_time) VALUES(?,?)",
            (filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    # 2. Sync to Firebase Cloud if connected
    if is_firebase_connected():
        save_document_firebase(filename)

def save_chat(username, question, answer):
    # 1. Save to local SQLite
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history(username, question, answer, time) VALUES(?,?,?,?)",
            (username, question, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    # 2. Sync to Firebase Cloud if connected
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