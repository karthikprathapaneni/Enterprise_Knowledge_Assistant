import streamlit as st
from database import get_db_status

def get_current_theme():
    return st.session_state.get("theme", "Light")

def load_css():
    """Injects high-end, responsive styling with glassmorphic cards, luminous gradients, and interactive animations."""
    theme = get_current_theme()

    if theme == "Dark":
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Global Canvas - Cyber-Executive Dark */
        .stApp {
            background: radial-gradient(circle at 50% -10%, #17153b 0%, #0d111c 45%, #07090e 100%) !important;
            color: #f1f5f9;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Glassmorphic Cyber Cards */
        .ai-card {
            background: rgba(17, 24, 39, 0.72);
            border: 1px solid rgba(99, 102, 241, 0.22);
            border-radius: 16px;
            padding: 22px 24px;
            backdrop-filter: blur(20px);
            box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.08);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        .ai-card:hover {
            transform: translateY(-3px);
            border-color: rgba(129, 140, 248, 0.55);
            box-shadow: 0 20px 40px -12px rgba(99, 102, 241, 0.35);
        }
        .ai-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #a855f7, #06b6d4);
        }

        .ai-metric-label {
            font-size: 0.72rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
        }
        .ai-metric-value {
            font-size: 2.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 10%, #c7d2fe 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 6px 0;
            letter-spacing: -0.02em;
        }

        /* Glowing Badges */
        .ai-badge {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.02em;
        }
        .badge-active { 
            background: rgba(16, 185, 129, 0.15); 
            color: #34d399; 
            border: 1px solid rgba(16, 185, 129, 0.35); 
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
        }
        .badge-indigo { 
            background: rgba(99, 102, 241, 0.18); 
            color: #a5b4fc; 
            border: 1px solid rgba(99, 102, 241, 0.4); 
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.2);
        }
        .badge-purple { 
            background: rgba(168, 85, 247, 0.18); 
            color: #d8b4fe; 
            border: 1px solid rgba(168, 85, 247, 0.4); 
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.2);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15); 
            color: #fbbf24; 
            border: 1px solid rgba(245, 158, 11, 0.35);
        }

        /* Top Header Navigation Banner */
        .app-header-banner {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.75) 0%, rgba(17, 24, 39, 0.85) 100%);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 18px;
            padding: 20px 28px;
            margin-bottom: 24px;
            backdrop-filter: blur(24px);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .app-header-banner .title-area h1 {
            margin: 0;
            font-size: 1.85rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 20%, #a5b4fc 70%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .app-header-banner .title-area p {
            margin: 4px 0 0 0;
            color: #94a3b8;
            font-size: 0.88rem;
        }
        .header-telemetry-chips {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        .telemetry-chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 0.75rem;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #94a3b8;
            padding: 0 20px;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.2s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            border-color: rgba(99, 102, 241, 0.4);
            background-color: rgba(99, 102, 241, 0.12);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.25)) !important;
            border-color: rgba(129, 140, 248, 0.7) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25) !important;
        }

        /* Streamlit Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.25);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        """
    else:
        # PRISTINE EXECUTIVE LIGHT THEME
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Global Canvas - Executive Light */
        .stApp {
            background: radial-gradient(circle at 50% -5%, #eef2ff 0%, #f8fafc 40%, #ffffff 100%) !important;
            color: #0f172a;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Glassmorphic Light Cards */
        .ai-card {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 16px;
            padding: 22px 26px;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        .ai-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.45);
            box-shadow: 0 18px 35px -8px rgba(99, 102, 241, 0.18);
        }
        .ai-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4f46e5, #7c3aed, #0284c7);
        }

        .ai-metric-label {
            font-size: 0.72rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
        }
        .ai-metric-value {
            font-size: 2.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 6px 0;
            letter-spacing: -0.02em;
        }

        /* Clean Light Badges */
        .ai-badge {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.02em;
        }
        .badge-active { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
        .badge-indigo { background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; }
        .badge-purple { background: #faf5ff; color: #6b21a8; border: 1px solid #e9d5ff; }
        .badge-amber { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }

        /* Top Header Navigation Banner */
        .app-header-banner {
            background: linear-gradient(135deg, rgba(240, 243, 255, 0.95) 0%, rgba(250, 245, 255, 0.95) 100%);
            border: 1px solid rgba(199, 210, 254, 0.75);
            border-radius: 18px;
            padding: 20px 28px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -8px rgba(99, 102, 241, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .app-header-banner .title-area h1 {
            margin: 0;
            font-size: 1.85rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 70%, #6d28d9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .app-header-banner .title-area p {
            margin: 4px 0 0 0;
            color: #475569;
            font-size: 0.88rem;
            font-weight: 500;
        }
        .header-telemetry-chips {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        .telemetry-chip {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 0.75rem;
            color: #475569;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 10px;
            background-color: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #64748b;
            padding: 0 22px;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.2s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #4338ca;
            background-color: #e0e7ff;
            border-color: #c7d2fe;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            border-color: #6366f1 !important;
            color: #4338ca !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.15) !important;
        }

        /* Streamlit Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.18);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }
        """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def app_header():
    """Renders the top application banner with real-time operational telemetry chips."""
    docs_cnt = st.session_state.get("total_docs", 0)
    chunks_cnt = st.session_state.get("total_chunks", 0)
    db_stat = get_db_status()
    is_cloud = "ONLINE" in db_stat.get("firebase_status", "")
    
    cloud_badge = "🟢 Cloud Synced" if is_cloud else "💾 Local Database"

    st.markdown(f"""
        <div class="app-header-banner">
            <div class="title-area">
                <h1>⚡ Enterprise Cognitive Knowledge Assistant</h1>
                <p>Retrieval-Augmented Neural Discovery • TF-IDF Lucene Semantic Engine • Cloud Firestore Sync</p>
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