import streamlit as st
import pandas as pd
import plotly.express as px
import json
from database import (
    get_documents,
    get_chat_history,
    clear_chat_history,
    get_db_status
)
from firebase_manager import (
    is_firebase_connected,
    init_firebase,
    get_firebase_project_id,
    get_documents_firebase,
    get_chat_history_firebase,
    sync_sqlite_to_firebase
)

def admin_page():
    st.subheader("🛡️ Enterprise Governance & Cloud Command")
    st.caption("Centralized compliance monitoring, user query analytics, and Google Cloud Firebase Firestore synchronization.")

    is_admin = (st.session_state.get("role") == "Admin")
    connected = is_firebase_connected()
    project_id = get_firebase_project_id()

    docs = get_documents()
    chats = get_chat_history()

    # Telemetry KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Total Intercepted Queries</span>
                <div class="ai-metric-value">{len(chats)}</div>
                <span class="ai-badge badge-indigo">Audit Logs</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Registered Documents</span>
                <div class="ai-metric-value">{len(docs)}</div>
                <span class="ai-badge badge-purple">Local Store</span>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        sync_status = "🟢 ONLINE" if connected else "🟡 STANDBY"
        sync_badge = "badge-active" if connected else "badge-amber"
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Cloud Firestore</span>
                <div class="ai-metric-value" style="font-size: 1.4rem; padding-top: 5px;">{sync_status}</div>
                <span class="ai-badge {sync_badge}">{project_id[:16]}</span>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        sec_level = "Tier 1 - Root Admin" if is_admin else "Tier 2 - Enterprise User"
        sec_badge = "badge-active" if is_admin else "badge-indigo"
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Access Clearance</span>
                <div class="ai-metric-value" style="font-size: 1.25rem; padding-top: 6px;">{sec_level}</div>
                <span class="ai-badge {sec_badge}">Role Verified</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Governance Workspaces
    tab_audit, tab_analytics, tab_cloud, tab_health = st.tabs([
        "📜 System Audit & Compliance",
        "📊 Intelligence & Query Analytics",
        "🔥 Firebase Cloud Synchronization",
        "💻 System Diagnostics"
    ])

    # TAB 1: SYSTEM AUDIT
    with tab_audit:
        c_title, c_action = st.columns([3, 1])
        with c_title:
            st.markdown("#### 💬 Comprehensive Query Interaction Logs")
        with c_action:
            if is_admin:
                if st.button("🗑️ Purge Chat History", use_container_width=True, help="Admin-only: Purge all local audit records"):
                    clear_chat_history()
                    st.success("All local audit chat records purged.")
                    st.rerun()

        if chats:
            df_chats = pd.DataFrame(chats, columns=["User", "Question", "Answer", "Timestamp"])
            st.dataframe(df_chats, use_container_width=True)

            csv_data = df_chats.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Logs (CSV)",
                data=csv_data,
                file_name="enterprise_audit_log.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.info("No query records captured in audit log.")

        st.divider()
        st.markdown("#### 🗄️ Ingested Document Ledger")
        if docs:
            df_docs = pd.DataFrame(docs, columns=["Filename", "Upload Timestamp"])
            st.dataframe(df_docs, use_container_width=True)
        else:
            st.info("No documents in registry.")

    # TAB 2: INTELLIGENCE ANALYTICS
    with tab_analytics:
        st.markdown("#### 📊 Operational Intelligence & Telemetry")
        if chats:
            df = pd.DataFrame(chats, columns=["Username", "Question", "Answer", "Time"])
            theme = st.session_state.get("theme", "Light")
            chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"

            an1, an2 = st.columns(2)
            with an1:
                st.markdown("##### 👤 Query Volume by User")
                user_counts = df["Username"].value_counts().reset_index()
                user_counts.columns = ["Username", "Queries"]
                fig_bar = px.bar(
                    user_counts, 
                    x="Username", 
                    y="Queries", 
                    color="Queries", 
                    color_continuous_scale="Viridis",
                    title="User Interaction Distribution"
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with an2:
                st.markdown("##### 💬 Query Token Density Distribution")
                df['Question_Length'] = df['Question'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
                fig_hist = px.histogram(
                    df, 
                    x="Question_Length",
                    nbins=12,
                    title="Words per Interaction",
                    color_discrete_sequence=['#4f46e5']
                )
                fig_hist.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("💡 Generate questions in **Cognitive Copilot** to populate telemetry metrics.")

    # TAB 3: FIREBASE CLOUD SYNCHRONIZATION
    with tab_cloud:
        st.markdown("#### ⚡ Google Cloud Firebase Firestore Persistence")
        st.markdown("Persist enterprise audit trails and document records seamlessly into Google Cloud Firestore.")

        fc1, fc2 = st.columns(2)
        with fc1:
            local_docs = get_documents(prefer_cloud=False)
            local_chats = get_chat_history(prefer_cloud=False)

            st.metric("Local Documents Ready for Sync", len(local_docs))
            st.metric("Local Chat Logs Ready for Sync", len(local_chats))

            if st.button("🚀 Push Local Data ➔ Firebase Cloud Firestore", use_container_width=True, type="primary", disabled=not connected):
                with st.spinner("Synchronizing collections with Google Cloud..."):
                    success, msg = sync_sqlite_to_firebase(local_docs, local_chats)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            if not connected:
                st.caption("Connect your Firebase project credentials below to enable live cloud sync.")

        with fc2:
            st.markdown("##### 🔗 Connect Firebase Project")
            conn_method = st.radio(
                "Method",
                ["Web App Config Snippet", "Upload Service Account JSON"],
                horizontal=True
            )
            if "Web App" in conn_method:
                web_snippet = st.text_area(
                    "Paste `firebaseConfig` object:",
                    value=f"""const firebaseConfig = {{\n  apiKey: "YOUR_API_KEY",\n  projectId: "{project_id}"\n}};""",
                    height=130
                )
                if st.button("Initialize Firebase", use_container_width=True):
                    if "YOUR_API_KEY" not in web_snippet:
                        success, msg = init_firebase(web_snippet)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please enter your actual Firebase credentials.")
            else:
                uploaded_key = st.file_uploader("Upload serviceAccountKey.json", type=["json"])
                if uploaded_key and st.button("Apply Service Key", use_container_width=True):
                    try:
                        key_data = json.loads(uploaded_key.getvalue().decode("utf-8"))
                        success, msg = init_firebase(key_data)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    except Exception as ex:
                        st.error(f"Invalid JSON: {ex}")

        # Cloud Collections Inspector
        st.divider()
        st.markdown("#### 🔍 Cloud Firestore Collections Inspector")
        if not connected:
            st.info("Cloud inspection unavailable while in local SQLite mode.")
        else:
            insp1, insp2 = st.columns(2)
            with insp1:
                st.markdown("##### 📄 `documents` (Cloud)")
                c_docs = get_documents_firebase()
                if c_docs:
                    st.dataframe(pd.DataFrame(c_docs, columns=["Filename", "Timestamp"]), use_container_width=True)
                else:
                    st.caption("No documents in cloud collection.")
            with insp2:
                st.markdown("##### 💬 `chat_history` (Cloud)")
                c_chats = get_chat_history_firebase()
                if c_chats:
                    st.dataframe(pd.DataFrame(c_chats, columns=["User", "Question", "Answer", "Timestamp"]), use_container_width=True)
                else:
                    st.caption("No chat records in cloud collection.")

    # TAB 4: SYSTEM DIAGNOSTICS
    with tab_health:
        st.markdown("#### 💻 Operational Health Diagnostics")
        db_stat = get_db_status()
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.write(f"**Database Operation Mode:** `{db_stat.get('mode')}`")
            st.write(f"**Firebase Cloud Status:** `{db_stat.get('firebase_status')}`")
            st.write(f"**Target GCP Project:** `{db_stat.get('project_id')}`")
            st.write(f"**Vector Store Chunks:** `{st.session_state.get('total_chunks', 0)}`")
        with d_col2:
            st.write(f"**Active Session User:** `{st.session_state.get('username', 'Guest')}`")
            st.write(f"**Assigned Role:** `{st.session_state.get('role', 'User')}`")
            st.write(f"**UI Interface Theme:** `{st.session_state.get('theme', 'Light')}`")
            st.write(f"**Ingestion Window:** `{st.session_state.get('cfg_chunk_size', 120)} words`")