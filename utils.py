import streamlit as st
from database import get_db_status

def get_current_theme():
    return st.session_state.get("theme", "Dark")

def load_css():
    """Injects high-end, responsive styling with classic executive cards, pristine contrast, and institutional elegance."""
    theme = get_current_theme()

    if theme == "Dark":
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Global Canvas - Classic Executive Obsidian */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #151d30 0%, #0b0f19 55%, #07090e 100%) !important;
            color: #e2e8f0 !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* Typography & Contrast Enforcements */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        p, li, span, label {
            color: #e2e8f0;
        }
        .stCaption, caption, small {
            color: #94a3b8 !important;
            font-size: 0.82rem;
        }

        /* Classic Executive Cards (No cheap neon rainbow stripes) */
        .ai-card {
            background: rgba(17, 24, 39, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 20px 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.06);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }
        .ai-card:hover {
            border-color: rgba(99, 102, 241, 0.45);
            box-shadow: 0 8px 28px -4px rgba(0, 0, 0, 0.55);
        }

        /* Theme Adaptive Text Helpers */
        .ai-title {
            color: #ffffff !important;
            font-weight: 700;
            font-size: 1.15rem;
            margin: 0 0 6px 0;
            letter-spacing: -0.01em;
        }
        .ai-body {
            color: #cbd5e1 !important;
            font-size: 0.92rem;
            line-height: 1.55;
            margin: 0 0 10px 0;
        }
        .ai-subtitle {
            color: #94a3b8 !important;
            font-size: 0.84rem;
            line-height: 1.45;
        }
        .ai-meta {
            color: #64748b !important;
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
        }
        .ai-callout {
            background: rgba(30, 41, 59, 0.6);
            border-left: 3px solid #3b82f6;
            border-radius: 6px;
            padding: 10px 14px;
            margin: 8px 0;
            color: #cbd5e1;
            font-size: 0.88rem;
        }

        /* Metric Typography */
        .ai-metric-label {
            font-size: 0.72rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            display: block;
        }
        .ai-metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff !important;
            margin: 4px 0 6px 0;
            letter-spacing: -0.02em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Classic Refined Badges (No tacky glowing shadows) */
        .ai-badge {
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            letter-spacing: 0.02em;
        }
        .badge-active { 
            background: rgba(16, 185, 129, 0.14); 
            color: #34d399; 
            border: 1px solid rgba(16, 185, 129, 0.3); 
        }
        .badge-indigo { 
            background: rgba(59, 130, 246, 0.14); 
            color: #93c5fd; 
            border: 1px solid rgba(59, 130, 246, 0.3); 
        }
        .badge-purple { 
            background: rgba(139, 92, 246, 0.14); 
            color: #c4b5fd; 
            border: 1px solid rgba(139, 92, 246, 0.3); 
        }
        .badge-amber { 
            background: rgba(245, 158, 11, 0.14); 
            color: #fbbf24; 
            border: 1px solid rgba(245, 158, 11, 0.3); 
        }
        .badge-danger { 
            background: rgba(239, 68, 68, 0.14); 
            color: #f87171; 
            border: 1px solid rgba(239, 68, 68, 0.3); 
        }

        /* Top Executive Header Banner */
        .app-header-banner {
            background: #111827;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .app-header-banner .title-area h1 {
            margin: 0;
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff !important;
            letter-spacing: -0.02em;
        }
        .app-header-banner .title-area p {
            margin: 4px 0 0 0;
            color: #94a3b8 !important;
            font-size: 0.85rem;
        }
        .header-telemetry-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }
        .telemetry-chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 0.74rem;
            color: #e2e8f0;
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Executive Segmented Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.09);
            padding-bottom: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 38px;
            border-radius: 8px;
            background-color: transparent;
            border: 1px solid transparent;
            color: #94a3b8;
            padding: 0 16px;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.15s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.05);
        }
        .stTabs [aria-selected="true"] {
            background: #1e293b !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: #ffffff !important;
        }

        /* Streamlit Input Controls - Guaranteed Crisp Visibility */
        .stTextInput input, .stTextArea textarea {
            background-color: #131b2e !important;
            color: #ffffff !important;
            border: 1px solid #2b3b55 !important;
            border-radius: 8px !important;
            font-size: 0.92rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 1px #3b82f6 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #131b2e !important;
            border: 1px solid #2b3b55 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] span {
            color: #ffffff !important;
        }

        /* Streamlit Native Buttons - Authoritative Executive Styling */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.88rem;
            padding: 8px 16px;
            transition: all 0.15s ease;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background-color: #1a2234;
            color: #f1f5f9;
        }
        .stButton > button:hover {
            background-color: #243048;
            border-color: rgba(255, 255, 255, 0.25);
            color: #ffffff;
        }
        .stButton > button[kind="primary"] {
            background-color: #2563eb !important;
            border-color: #3b82f6 !important;
            color: #ffffff !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #1d4ed8 !important;
            border-color: #60a5fa !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #080c14 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
            color: #cbd5e1;
        }

        /* Streamlit Expanders */
        div[data-testid="stExpander"] {
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 8px !important;
            background: rgba(17, 24, 39, 0.5) !important;
        }
        div[data-testid="stExpander"] summary span {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
        }
        """
    else:
        # PRISTINE ARCHITECTURAL EXECUTIVE LIGHT THEME
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Global Canvas - Executive Light */
        .stApp {
            background: #f8fafc !important;
            color: #0f172a !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* Typography & Contrast Enforcements */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        p, li, span, label {
            color: #1e293b;
        }
        .stCaption, caption, small {
            color: #475569 !important;
            font-size: 0.82rem;
        }

        /* Classic Executive Cards */
        .ai-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }
        .ai-card:hover {
            border-color: #cbd5e1;
            box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08);
        }

        /* Theme Adaptive Text Helpers */
        .ai-title {
            color: #0f172a !important;
            font-weight: 700;
            font-size: 1.15rem;
            margin: 0 0 6px 0;
            letter-spacing: -0.01em;
        }
        .ai-body {
            color: #1e293b !important;
            font-size: 0.92rem;
            line-height: 1.55;
            margin: 0 0 10px 0;
        }
        .ai-subtitle {
            color: #475569 !important;
            font-size: 0.84rem;
            line-height: 1.45;
        }
        .ai-meta {
            color: #64748b !important;
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
        }
        .ai-callout {
            background: #f1f5f9;
            border-left: 3px solid #2563eb;
            border-radius: 6px;
            padding: 10px 14px;
            margin: 8px 0;
            color: #1e293b;
            font-size: 0.88rem;
        }

        /* Metric Typography */
        .ai-metric-label {
            font-size: 0.72rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            display: block;
        }
        .ai-metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a !important;
            margin: 4px 0 6px 0;
            letter-spacing: -0.02em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Clean Light Badges */
        .ai-badge {
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            letter-spacing: 0.02em;
        }
        .badge-active { 
            background: #ecfdf5; 
            color: #065f46; 
            border: 1px solid #a7f3d0; 
        }
        .badge-indigo { 
            background: #eff6ff; 
            color: #1e40af; 
            border: 1px solid #bfdbfe; 
        }
        .badge-purple { 
            background: #f5f3ff; 
            color: #5b21b6; 
            border: 1px solid #ddd6fe; 
        }
        .badge-amber { 
            background: #fffbeb; 
            color: #92400e; 
            border: 1px solid #fde68a; 
        }
        .badge-danger { 
            background: #fef2f2; 
            color: #991b1b; 
            border: 1px solid #fecaca; 
        }

        /* Top Executive Header Banner */
        .app-header-banner {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .app-header-banner .title-area h1 {
            margin: 0;
            font-size: 1.65rem;
            font-weight: 800;
            color: #0f172a !important;
            letter-spacing: -0.02em;
        }
        .app-header-banner .title-area p {
            margin: 4px 0 0 0;
            color: #475569 !important;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .header-telemetry-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }
        .telemetry-chip {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 0.74rem;
            color: #334155;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: transparent;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 38px;
            border-radius: 8px;
            background-color: transparent;
            border: 1px solid transparent;
            color: #64748b;
            padding: 0 16px;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.15s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #0f172a;
            background-color: #f1f5f9;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #0f172a !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }

        /* Streamlit Input Controls - Guaranteed Crisp Visibility */
        .stTextInput input, .stTextArea textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            font-size: 0.92rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 1px #2563eb !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #0f172a !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }

        /* Streamlit Native Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.88rem;
            padding: 8px 16px;
            transition: all 0.15s ease;
            border: 1px solid #cbd5e1;
            background-color: #ffffff;
            color: #0f172a;
        }
        .stButton > button:hover {
            background-color: #f8fafc;
            border-color: #94a3b8;
        }
        .stButton > button[kind="primary"] {
            background-color: #1d4ed8 !important;
            border-color: #1e40af !important;
            color: #ffffff !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #1e40af !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }
        section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
            color: #1e293b;
        }

        /* Streamlit Expanders */
        div[data-testid="stExpander"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            background: #ffffff !important;
        }
        div[data-testid="stExpander"] summary span {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def app_header():
    """Renders the top application banner with real-time operational telemetry chips."""
    docs_cnt = st.session_state.get("total_docs", 0)
    chunks_cnt = st.session_state.get("total_chunks", 0)
    db_stat = get_db_status()
    is_cloud = "ONLINE" in db_stat.get("firebase_status", "")
    
    cloud_badge = "🟢 Cloud Synced" if is_cloud else "💾 Local SQLite"

    st.markdown(f"""
        <div class="app-header-banner">
            <div class="title-area">
                <h1>⚡ Enterprise Cognitive Knowledge Assistant</h1>
                <p>Multi-Agent Cognitive Operating System • Dual-Mode SQLite & Cloud Firestore • Sub-Second Latency</p>
            </div>
            <div class="header-telemetry-chips">
                <div class="telemetry-chip">📁 <b>{docs_cnt}</b> Documents</div>
                <div class="telemetry-chip">🧩 <b>{chunks_cnt}</b> Chunks</div>
                <div class="telemetry-chip">{cloud_badge}</div>
                <div class="telemetry-chip">⚡ <b>Sub-50ms</b> Vector Latency</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def clean_text(text: str) -> str:
    """Utility function to sanitize extracted text layers."""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return ' '.join(chunk for chunk in chunks if chunk)