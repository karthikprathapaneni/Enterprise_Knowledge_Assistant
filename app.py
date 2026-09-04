import streamlit as st
from database import init_db, get_db_status, get_user_profile
from utils import load_css, app_header, get_current_theme
from login import login_page, logout

# Enterprise 2.0 Portals
from command_center import command_center_page
from personal_assistant import personal_assistant_page
from dashboard import dashboard_page
from chat import chat_page
from problem_solver import problem_solver_page
from document_intelligence_portal import document_intelligence_page
from graph import knowledge_graph_page
from data_analyst import data_analyst_page
from decision_center import decision_center_page
from department_workspaces import department_workspaces_page
from alerts_portal import alerts_portal_page
from rag_evaluator import rag_evaluator_page
from demo_mode import demo_mode_page
from admin import admin_page

st.set_page_config(
    page_title="Enterprise Cognitive Knowledge Assistant 2.0",
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

if "current_portal" not in st.session_state:
    st.session_state.current_portal = "🏠 Command Center"

init_db()
load_css()

if not st.session_state.logged_in:
    login_page()
else:
    username = st.session_state.username
    profile = get_user_profile(username)
    st.session_state.user_profile = profile

    st.sidebar.markdown("""
        <div style="padding: 8px 0 12px 0;">
            <span style="font-size: 1.22rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡ COGNITIVE 2.0</span>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 1px;">Agentic Enterprise Operating System</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"👤 **{profile['full_name']}**")
    st.sidebar.markdown(f"🏢 `{profile['department']}` • `Tier {profile['clearance_level']}` Clearance")

    # DB Connection Status Indicator
    db_stat = get_db_status()
    if "ONLINE" in db_stat.get("firebase_status", ""):
        st.sidebar.markdown(f'<span class="ai-badge badge-active" style="width: 100%; justify-content: center; margin: 4px 0;">🟢 Cloud Firestore Synced</span>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f'<span class="ai-badge badge-indigo" style="width: 100%; justify-content: center; margin: 4px 0;">💾 Local SQLite Storage</span>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    PORTAL_OPTIONS = [
        "🏠 Command Center",
        "🧠 My AI Assistant",
        "📚 Knowledge Vault",
        "💬 Cognitive Copilot",
        "🛠️ AI Problem Solver",
        "📄 Document Intelligence",
        "🕸️ Knowledge Graph",
        "📊 AI Data Analyst",
        "🎯 Decision Center",
        "🏢 Department Workspaces",
        "🔔 Intelligence Alerts",
        "📈 RAG Evaluation & ROI",
        "🎬 Guided Product Tour",
        "🛡️ Governance & Security"
    ]

    # Sync selection with current_portal state
    curr_idx = 0
    if st.session_state.current_portal in PORTAL_OPTIONS:
        curr_idx = PORTAL_OPTIONS.index(st.session_state.current_portal)

    page = st.sidebar.radio(
        "Navigation",
        PORTAL_OPTIONS,
        index=curr_idx,
        key="portal_navigation_radio"
    )
    st.session_state.current_portal = page

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

    # Route to selected portal
    if page == "🏠 Command Center":
        command_center_page()
    elif page == "🧠 My AI Assistant":
        personal_assistant_page()
    elif page == "📚 Knowledge Vault":
        dashboard_page()
    elif page == "💬 Cognitive Copilot":
        chat_page()
    elif page == "🛠️ AI Problem Solver":
        problem_solver_page()
    elif page == "📄 Document Intelligence":
        document_intelligence_page()
    elif page == "🕸️ Knowledge Graph":
        knowledge_graph_page()
    elif page == "📊 AI Data Analyst":
        data_analyst_page()
    elif page == "🎯 Decision Center":
        decision_center_page()
    elif page == "🏢 Department Workspaces":
        department_workspaces_page()
    elif page == "🔔 Intelligence Alerts":
        alerts_portal_page()
    elif page == "📈 RAG Evaluation & ROI":
        rag_evaluator_page()
    elif page == "🎬 Guided Product Tour":
        demo_mode_page()
    elif page == "🛡️ Governance & Security":
        admin_page()