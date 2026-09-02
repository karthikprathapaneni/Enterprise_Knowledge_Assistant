import streamlit as st
from database import verify_user

def login_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="font-size: 2.3rem; margin-bottom: 6px;">☕ Enterprise Cognitive Platform</h1>
            <p style="color: #64748b; font-size: 1.05rem;">Java Spring Boot Architecture • Lucene Vector Intelligence • Cloud Firestore</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("#### 🔐 Secure Portal Login")
        role = st.selectbox("Select Access Role", ["Admin", "User"])
        username = st.text_input("Username", placeholder="e.g. admin or user", key="login_user_input")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass_input")

        if st.button("🚀 Sign In to Enterprise Workspace", use_container_width=True, type="primary"):
            db_role = verify_user(username, password)
            if db_role and db_role == role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.success("Authentication verified!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please verify your username, password, and role.")

        st.markdown("---")
        st.markdown("##### ⚡ Quick 1-Click Access:")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Admin Demo", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "admin"
                st.session_state.role = "Admin"
                st.rerun()
        with c2:
            if st.button("👤 User Demo", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "user"
                st.session_state.role = "User"
                st.rerun()

        st.caption("Credentials: Admin (`admin` / `admin123`) • User (`user` / `user123`)")

def logout():
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()