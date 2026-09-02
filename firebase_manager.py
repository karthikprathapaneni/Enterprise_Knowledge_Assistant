import os
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    HAS_FIREBASE_ADMIN = True
except ImportError:
    firebase_admin = None
    credentials = None
    firestore = None
    HAS_FIREBASE_ADMIN = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(BASE_DIR, "firebase_credentials.json")
CONFIG_FILE = os.path.join(BASE_DIR, "firebase_config.json")
DEFAULT_CRED_PATHS = [
    CRED_FILE,
    os.path.join(BASE_DIR, "serviceAccountKey.json"),
    os.path.join(BASE_DIR, "firebase_key.json"),
    os.path.join(BASE_DIR, "database", "firebase_credentials.json"),
]

_firebase_app = None
_firestore_db = None
_active_project_id = "knowledge-9d660"
_api_key = ""
_auth_domain = "knowledge-9d660.firebaseapp.com"
_app_id = "web:YTk1NDMwYjQtNzg0My00MzczLWE0YzgtMjAyZTU4ZGU4N2I3"
_conn_mode = "REST_API" # "ADMIN_SDK" or "REST_API"

def parse_firebase_web_snippet(text: str):
    """Extracts configuration keys from a JS firebaseConfig object or JSON snippet."""
    api_key_m = re.search(r'apiKey["\']?\s*:\s*["\']([^"\']+)["\']', text)
    proj_id_m = re.search(r'projectId["\']?\s*:\s*["\']([^"\']+)["\']', text)
    auth_dom_m = re.search(r'authDomain["\']?\s*:\s*["\']([^"\']+)["\']', text)
    app_id_m = re.search(r'appId["\']?\s*:\s*["\']([^"\']+)["\']', text)

    return {
        "apiKey": api_key_m.group(1) if api_key_m else None,
        "projectId": proj_id_m.group(1) if proj_id_m else "knowledge-9d660",
        "authDomain": auth_dom_m.group(1) if auth_dom_m else "knowledge-9d660.firebaseapp.com",
        "appId": app_id_m.group(1) if app_id_m else None,
    }

def save_web_config(cfg: dict):
    global _active_project_id, _api_key, _auth_domain, _app_id, _conn_mode
    if cfg.get("projectId"):
        _active_project_id = cfg["projectId"]
    if cfg.get("apiKey"):
        _api_key = cfg["apiKey"]
    if cfg.get("authDomain"):
        _auth_domain = cfg["authDomain"]
    if cfg.get("appId"):
        _app_id = cfg["appId"]
    _conn_mode = "REST_API"

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "projectId": _active_project_id,
            "apiKey": _api_key,
            "authDomain": _auth_domain,
            "appId": _app_id,
            "connected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)

def load_saved_config():
    global _active_project_id, _api_key, _auth_domain, _app_id
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                _active_project_id = data.get("projectId", "knowledge-9d660")
                _api_key = data.get("apiKey", "")
                _auth_domain = data.get("authDomain", "knowledge-9d660.firebaseapp.com")
                _app_id = data.get("appId", "")
        except Exception:
            pass

load_saved_config()

def init_firebase(cred_source=None):
    """Initializes Admin SDK or saves Web Config."""
    global _firebase_app, _firestore_db, _active_project_id, _conn_mode, _api_key

    # Check if cred_source is a Web Config dict or snippet
    if isinstance(cred_source, dict):
        if "type" in cred_source and cred_source.get("type") == "service_account":
            # Service account certificate
            if not HAS_FIREBASE_ADMIN or firebase_admin is None:
                return False, "firebase-admin Python package is not installed. You can connect via Firebase Web Config API Key / Project ID."
            try:
                if firebase_admin._apps:
                    for app_name in list(firebase_admin._apps.keys()):
                        firebase_admin.delete_app(firebase_admin.get_app(app_name))
                cred_obj = credentials.Certificate(cred_source)
                _firebase_app = firebase_admin.initialize_app(cred_obj)
                _firestore_db = firestore.client()
                _active_project_id = cred_source.get("project_id", "knowledge-9d660")
                _conn_mode = "ADMIN_SDK"
                with open(CRED_FILE, "w", encoding="utf-8") as f:
                    json.dump(cred_source, f, indent=2)
                return True, f"Connected to Firebase Firestore via Admin SDK ({_active_project_id})"
            except Exception as e:
                return False, f"Admin SDK initialization error: {e}"
        elif "apiKey" in cred_source or "projectId" in cred_source:
            save_web_config(cred_source)
            return True, f"Connected to Firebase Project ({_active_project_id}) via Web API"

    elif isinstance(cred_source, str):
        if "{" in cred_source:
            # Could be JSON service account or JS firebaseConfig snippet
            try:
                data = json.loads(cred_source)
                return init_firebase(data)
            except Exception:
                parsed = parse_firebase_web_snippet(cred_source)
                if parsed.get("apiKey") or parsed.get("projectId"):
                    save_web_config(parsed)
                    return True, f"Connected to Firebase Project ({_active_project_id}) via Web Config"
        elif os.path.exists(cred_source):
            try:
                with open(cred_source, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return init_firebase(data)
            except Exception as ex:
                return False, f"File load error: {ex}"

    # Auto-load existing
    if HAS_FIREBASE_ADMIN and firebase_admin and os.path.exists(CRED_FILE):
        try:
            if firebase_admin._apps:
                for app_name in list(firebase_admin._apps.keys()):
                    firebase_admin.delete_app(firebase_admin.get_app(app_name))
            cred_obj = credentials.Certificate(CRED_FILE)
            _firebase_app = firebase_admin.initialize_app(cred_obj)
            _firestore_db = firestore.client()
            _conn_mode = "ADMIN_SDK"
            return True, f"Connected to Firebase Firestore ({_active_project_id})"
        except Exception:
            pass

    if _api_key or os.path.exists(CONFIG_FILE):
        _conn_mode = "REST_API"
        return True, f"Connected to Firebase Project ({_active_project_id}) via Web Config"

    return False, "No Firebase credentials found."

def is_firebase_connected():
    if _firestore_db is not None:
        return True
    if _api_key:
        return True
    if os.path.exists(CRED_FILE) or os.path.exists(CONFIG_FILE):
        success, _ = init_firebase()
        return success
    return False

def get_firebase_project_id():
    return _active_project_id or "knowledge-9d660"

def get_connection_mode():
    return _conn_mode

def get_web_app_id():
    return _app_id or "web:YTk1NDMwYjQtNzg0My00MzczLWE0YzgtMjAyZTU4ZGU4N2I3"

def save_document_firebase(filename):
    if not is_firebase_connected():
        return False
    
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. If Admin SDK is active
    if _firestore_db is not None:
        try:
            _firestore_db.collection("documents").add({
                "filename": filename,
                "upload_time": upload_time,
                "source": "Cognitive_Assistant_Platform"
            })
            return True
        except Exception as e:
            print(f"Admin SDK save doc error: {e}")

    # 2. REST API Fallback
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{_active_project_id}/databases/(default)/documents/documents"
        if _api_key:
            url += f"?key={_api_key}"
        
        payload = {
            "fields": {
                "filename": {"stringValue": filename},
                "upload_time": {"stringValue": upload_time},
                "source": {"stringValue": "Cognitive_Assistant_Platform"}
            }
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.getcode() in [200, 201]
    except Exception as e:
        print(f"REST API save doc error: {e}")
        return False

def save_chat_firebase(username, question, answer):
    if not is_firebase_connected():
        return False
    
    msg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. If Admin SDK is active
    if _firestore_db is not None:
        try:
            _firestore_db.collection("chat_history").add({
                "username": username,
                "question": question,
                "answer": answer,
                "time": msg_time
            })
            return True
        except Exception as e:
            print(f"Admin SDK save chat error: {e}")

    # 2. REST API Fallback
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{_active_project_id}/databases/(default)/documents/chat_history"
        if _api_key:
            url += f"?key={_api_key}"
        
        payload = {
            "fields": {
                "username": {"stringValue": str(username)},
                "question": {"stringValue": str(question)},
                "answer": {"stringValue": str(answer)},
                "time": {"stringValue": msg_time}
            }
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.getcode() in [200, 201]
    except Exception as e:
        print(f"REST API save chat error: {e}")
        return False

def get_chat_history_firebase():
    if not is_firebase_connected():
        return []

    # 1. Admin SDK
    if _firestore_db is not None and HAS_FIREBASE_ADMIN and firestore is not None:
        try:
            chats = []
            docs = _firestore_db.collection("chat_history").order_by("time", direction=firestore.Query.DESCENDING).limit(50).stream()
            for d in docs:
                data = d.to_dict()
                chats.append((
                    data.get("username", "Guest"),
                    data.get("question", ""),
                    data.get("answer", ""),
                    data.get("time", "")
                ))
            return chats
        except Exception as e:
            print(f"Admin SDK fetch chat error: {e}")

    # 2. REST API
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{_active_project_id}/databases/(default)/documents/chat_history"
        if _api_key:
            url += f"?key={_api_key}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            items = res_json.get("documents", [])
            chats = []
            for item in items:
                f = item.get("fields", {})
                chats.append((
                    f.get("username", {}).get("stringValue", "Guest"),
                    f.get("question", {}).get("stringValue", ""),
                    f.get("answer", {}).get("stringValue", ""),
                    f.get("time", {}).get("stringValue", "")
                ))
            return chats
    except Exception as e:
        print(f"REST API fetch chat error: {e}")
        return []

def get_documents_firebase():
    if not is_firebase_connected():
        return []

    # 1. Admin SDK
    if _firestore_db is not None and HAS_FIREBASE_ADMIN and firestore is not None:
        try:
            docs_list = []
            docs = _firestore_db.collection("documents").order_by("upload_time", direction=firestore.Query.DESCENDING).limit(50).stream()
            for d in docs:
                data = d.to_dict()
                docs_list.append((
                    data.get("filename", ""),
                    data.get("upload_time", "")
                ))
            return docs_list
        except Exception as e:
            print(f"Admin SDK fetch docs error: {e}")

    # 2. REST API
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{_active_project_id}/databases/(default)/documents/documents"
        if _api_key:
            url += f"?key={_api_key}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            items = res_json.get("documents", [])
            docs_list = []
            for item in items:
                f = item.get("fields", {})
                docs_list.append((
                    f.get("filename", {}).get("stringValue", ""),
                    f.get("upload_time", {}).get("stringValue", "")
                ))
            return docs_list
    except Exception as e:
        print(f"REST API fetch docs error: {e}")
        return []

def sync_sqlite_to_firebase(local_docs, local_chats):
    """Syncs existing SQLite records into Firebase Firestore."""
    if not is_firebase_connected():
        return False, "Firebase is not connected."
    
    synced_docs = 0
    synced_chats = 0

    try:
        for doc in local_docs:
            fname, utime = doc[0], doc[1]
            save_document_firebase(fname)
            synced_docs += 1

        for chat in local_chats:
            user, q, a, t = chat[0], chat[1], chat[2], chat[3]
            save_chat_firebase(user, q, a)
            synced_chats += 1

        return True, f"Successfully synchronized {synced_docs} documents and {synced_chats} chat records to Firebase Firestore ({_active_project_id})!"
    except Exception as e:
        return False, f"Sync error: {str(e)}"
