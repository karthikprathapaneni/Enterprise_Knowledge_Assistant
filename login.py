import streamlit as st
from database import verify_user

def login_page():
    st.markdown("""
        <div style="text-align: center; margin-top: 24px; margin-bottom: 24px;">
            <div class="ai-badge badge-indigo" style="margin-bottom: 12px; font-size: 0.78rem; padding: 4px 14px;">
                ⚡ Enterprise Cognitive Knowledge Assistant 2.0
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0 0 6px 0;">
                Secure Enterprise Portal
            </h1>
            <p class="ai-subtitle" style="font-size: 0.95rem; margin: 0 auto; max-width: 580px;">
                Multi-Agent Cognitive Operating System • Permission-Aware Retrieval • Dual-Mode Cloud Sync
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container(border=True):
            st.markdown("#### 🔐 Identity Authentication")
            st.caption("Enter institutional credentials or clearance role to access your scoped workspace.")

            role = st.selectbox("Clearance Role", ["Admin", "User"])
            username = st.text_input("Username", placeholder="e.g. admin or user", key="login_user_input")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass_input")

            st.write("")
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

        st.write("")
        with st.container(border=True):
            st.markdown("##### ⚡ Instant Evaluator Demo Access:")
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

            st.caption("Pre-configured Credentials: `admin` / `admin123` (Tier 3) • `user` / `user123` (Tier 1)")

def logout():
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()