import streamlit as st
from database import init_db, get_db_status
from utils import load_css, app_header, get_current_theme
from login import login_page, logout
from dashboard import dashboard_page
from chat import chat_page
from graph import knowledge_graph_page
from admin import admin_page

st.set_page_config(
    page_title="Enterprise Cognitive Knowledge Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

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
    st.sidebar.markdown("""
        <div style="padding: 10px 0 16px 0;">
            <span style="font-size: 1.3rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡ COGNITIVE AI</span>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Enterprise Knowledge Platform</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"👤 **User:** `{st.session_state.username}`")
    st.sidebar.markdown(f"🔑 **Role:** `{st.session_state.role}`")

    # DB Connection Status Indicator
    db_stat = get_db_status()
    if "ONLINE" in db_stat.get("firebase_status", ""):
        st.sidebar.markdown(f'<span class="ai-badge badge-active" style="width: 100%; justify-content: center; margin: 6px 0;">🟢 Cloud Firestore Synced</span>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f'<span class="ai-badge badge-indigo" style="width: 100%; justify-content: center; margin: 6px 0;">💾 Local SQLite Storage</span>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # 4 Streamlined Enterprise Portals
    page = st.sidebar.radio(
        "Navigation",
        [
            "⚡ Neural Document Vault",
            "💬 Cognitive Copilot",
            "🕸️ Semantic Knowledge Graph",
            "🛡️ Governance & Cloud Command"
        ]
    )

    st.sidebar.markdown("---")

    # Theme Switcher
    theme_choice = st.sidebar.radio(
        "🎨 Appearance",
        ["🌙 Dark Theme", "☀️ Light Theme"],
        index=0 if st.session_state.theme == "Dark" else 1,
        key="theme_radio_selector"
    )
    new_theme = "Dark" if "Dark" in theme_choice else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.sidebar.markdown("---")
    logout()
    app_header()

    if page == "⚡ Neural Document Vault":
        dashboard_page()
    elif page == "💬 Cognitive Copilot":
        chat_page()
    elif page == "🕸️ Semantic Knowledge Graph":
        knowledge_graph_page()
    elif page == "🛡️ Governance & Cloud Command":
        admin_page()