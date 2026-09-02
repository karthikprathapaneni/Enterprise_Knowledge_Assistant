import streamlit as st
from database import init_db, get_db_status
from utils import load_css, app_header, get_current_theme
from login import login_page, logout
from dashboard import dashboard_page
from chat import chat_page
from analytics import analytics_page
from graph import knowledge_graph_page
from admin import admin_page
from ocr import ocr_page
from voice import voice_page
from translator import translator_page
from firebase_sync import firebase_sync_page
from java_architecture import java_architecture_page

st.set_page_config(
    page_title="Enterprise Cognitive Knowledge Platform (Java Enterprise)",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

init_db()
load_css()

if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("🧭 Navigation")
    st.sidebar.write(f"👤 **User:** `{st.session_state.username}`")
    st.sidebar.write(f"🔑 **Role:** `{st.session_state.role}`")

    # DB Connection Status Indicator
    db_stat = get_db_status()
    if "ONLINE" in db_stat["firebase_status"]:
        st.sidebar.success(f"🔥 Firebase: {db_stat['project_id']}")
    else:
        st.sidebar.info("💾 Storage: SQLite + Cloud Sync")

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Select Enterprise Portal",
        [
            "📊 Executive Dashboard",
            "💬 Cognitive Chat Assistant",
            "📈 Intelligence Analytics",
            "🕸️ Knowledge Graph",
            "🔥 Firebase Cloud Sync",
            "☕ Java Architecture & Core",
            "🛡️ Admin & Audit Logs",
            "🖼️ OCR Document Scanner",
            "🎙️ Voice Synthesizer",
            "🌐 Multi-Language Translator"
        ]
    )

    st.sidebar.markdown("---")
    
    # Theme Selection Switcher
    theme_choice = st.sidebar.radio(
        "🎨 Interface Theme",
        ["☀️ Light Theme", "🌙 Dark Theme"],
        index=0 if st.session_state.theme == "Light" else 1,
        key="theme_radio_selector"
    )
    new_theme = "Light" if "Light" in theme_choice else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.sidebar.markdown("---")
    logout()
    app_header()

    if page == "📊 Executive Dashboard":
        dashboard_page()
    elif page == "💬 Cognitive Chat Assistant":
        chat_page()
    elif page == "📈 Intelligence Analytics":
        analytics_page()
    elif page == "🕸️ Knowledge Graph":
        knowledge_graph_page()
    elif page == "🔥 Firebase Cloud Sync":
        firebase_sync_page()
    elif page == "☕ Java Architecture & Core":
        java_architecture_page()
    elif page == "🛡️ Admin & Audit Logs":
        admin_page()
    elif page == "🖼️ OCR Document Scanner":
        ocr_page()
    elif page == "🎙️ Voice Synthesizer":
        voice_page()
    elif page == "🌐 Multi-Language Translator":
        translator_page()