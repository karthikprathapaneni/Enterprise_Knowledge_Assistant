import streamlit as st
from database import verify_user

def login_page():
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 28px;">
            <div style="display: inline-block; padding: 6px 16px; border-radius: 9999px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">
                ⚡ Enterprise Cognitive Knowledge Assistant
            </div>
            <h1 style="font-size: 2.4rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #ffffff 20%, #a5b4fc 70%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Secure Enterprise Portal
            </h1>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 6px;">
                Retrieval-Augmented Intelligence • Neural Vector Index • Google Cloud Firestore
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
            <div class="ai-card" style="padding: 28px 32px; margin-bottom: 20px;">
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 16px;">🔐 Account Authentication</div>
        """, unsafe_allow_html=True)

        role = st.selectbox("Select Clearance Role", ["Admin", "User"])
        username = st.text_input("Username", placeholder="e.g. admin or user", key="login_user_input")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass_input")

        if st.button("🚀 Sign In to Workspace", use_container_width=True, type="primary"):
            db_role = verify_user(username, password)
            if db_role and db_role == role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.success("Authentication verified! Loading workspace...")
                st.rerun()
            else:
                st.error("Invalid credentials. Please verify username, password, and clearance role.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("##### ⚡ Instant 1-Click Demo Login:")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Admin Demo Access", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "admin"
                st.session_state.role = "Admin"
                st.rerun()
        with c2:
            if st.button("👤 User Demo Access", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "user"
                st.session_state.role = "User"
                st.rerun()

        st.caption("Default Credentials: `admin` / `admin123` • `user` / `user123`")

def logout():
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()