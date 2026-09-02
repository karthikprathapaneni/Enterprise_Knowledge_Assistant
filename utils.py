import streamlit as st

def get_current_theme():
    return st.session_state.get("theme", "Light")

def load_css():
    """Injects high-end Light Theme CSS with glassmorphic cards, luminous gradients, and interactive animations."""
    theme = get_current_theme()

    if theme == "Dark":
        css = """
        /* Dark Radial Background */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0f172a 50%, #020617 100%);
            color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .ai-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 20px 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .ai-card:hover {
            transform: translateY(-3px);
            border-color: rgba(129, 140, 248, 0.6);
            box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.3);
        }
        .ai-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        }
        .ai-metric-label {
            font-size: 0.75rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }
        .ai-metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 6px 0;
        }
        .badge-active { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
        .badge-indigo { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
        .badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
        
        .app-header-banner {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.12));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 24px 32px;
            margin-bottom: 28px;
            backdrop-filter: blur(20px);
        }
        .app-header-banner h1 { 
            margin: 0; 
            font-size: 2rem; 
            font-weight: 800; 
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .app-header-banner p { margin: 6px 0 0 0; color: #94a3b8; font-size: 0.95rem; }
        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #94a3b8;
            padding: 0 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(99, 102, 241, 0.25) !important;
            border-color: rgba(99, 102, 241, 0.6) !important;
            color: #ffffff !important;
        }
        """
    else:
        # HIGH-END EXECUTIVE LIGHT THEME
        css = """
        /* Light Luminous Canvas */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #f1f5f9 0%, #f8fafc 40%, #ffffff 100%);
            color: #0f172a;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Modern Glass Cards - Light Mode */
        .ai-card {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.9);
            border-radius: 18px;
            padding: 22px 26px;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.07), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .ai-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 20px 35px -10px rgba(99, 102, 241, 0.16);
        }
        
        /* Top Gradient Accent Line */
        .ai-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
        }

        /* Metric Typography - Light */
        .ai-metric-label {
            font-size: 0.75rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }
        .ai-metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 6px 0;
        }

        /* Clean Light Badges */
        .ai-badge {
            font-size: 0.72rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .badge-active { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
        .badge-indigo { background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; }
        .badge-purple { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }

        /* Light Mode Glassmorphic Navigation Banner */
        .app-header-banner {
            background: linear-gradient(135deg, rgba(238, 242, 255, 0.95), rgba(245, 243, 255, 0.95));
            border: 1px solid rgba(199, 210, 254, 0.6);
            border-radius: 20px;
            padding: 24px 32px;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.08);
        }
        .app-header-banner h1 { 
            margin: 0; 
            font-size: 2.1rem; 
            font-weight: 800; 
            background: linear-gradient(135deg, #1e1b4b 0%, #4f46e5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .app-header-banner p { margin: 6px 0 0 0; color: #475569; font-size: 0.95rem; font-weight: 500; }

        /* Custom Streamlit Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 12px;
            background-color: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #64748b;
            padding: 0 22px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #4338ca;
            background-color: #e0e7ff;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            border-color: #6366f1 !important;
            color: #4338ca !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.15) !important;
        }

        /* Streamlit Buttons Enhancement */
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def app_header():
    """Renders the top application title banner."""
    st.markdown("""
        <div class="app-header-banner">
            <h1>☕ Enterprise Cognitive Knowledge Platform (Java Enterprise)</h1>
            <p>Java Spring Boot Core • Apache Lucene Vector RAG • Google Cloud Firebase • JVM Neural Services</p>
        </div>
    """, unsafe_allow_html=True)

def clean_text(text: str) -> str:
    """Utility function to sanitize extracted text layers."""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return ' '.join(chunk for chunk in chunks if chunk)