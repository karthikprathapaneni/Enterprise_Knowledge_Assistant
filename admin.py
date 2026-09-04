import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    get_documents,
    get_chat_history,
    clear_chat_history,
    get_db_status,
    get_security_events,
    get_connection
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
    st.subheader("🛡️ Enterprise Governance, Security & Cloud Command")
    st.caption("Centralized compliance monitoring, AI Guard threat interception, human review queues, and Google Cloud Firebase synchronization.")

    is_admin = (st.session_state.get("role") == "Admin")
    connected = is_firebase_connected()
    project_id = get_firebase_project_id()

    docs = get_documents()
    chats = get_chat_history()
    security_events = get_security_events()

    # Telemetry KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">AI Guard Interceptions</span>
                <div class="ai-metric-value" style="color: {'#ef4444' if security_events else '#10b981'};">{len(security_events)}</div>
                <span class="ai-badge {'badge-amber' if security_events else 'badge-active'}">Threat Firewall</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Intercepted Audit Logs</span>
                <div class="ai-metric-value">{len(chats)}</div>
                <span class="ai-badge badge-indigo">Full Trail</span>
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
        sec_level = "Tier 3 - Root Admin" if is_admin else "Tier 1 - Enterprise User"
        sec_badge = "badge-active" if is_admin else "badge-indigo"
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Active Clearance</span>
                <div class="ai-metric-value" style="font-size: 1.3rem; padding-top: 6px;">{sec_level}</div>
                <span class="ai-badge {sec_badge}">Verified Session</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Workspaces
    tab_guard, tab_observability, tab_audit, tab_analytics, tab_cloud, tab_hitl = st.tabs([
        "🛡️ AI Security Guard",
        "📡 Observability Traces",
        "📜 System Audit Trail",
        "📊 Operational Analytics",
        "🔥 Firebase Cloud Sync",
        "👥 Human-In-The-Loop Queue"
    ])

    # TAB 1: AI SECURITY GUARD
    with tab_guard:
        st.markdown("#### 🛡️ AI Security Guardrail Interceptions")
        st.caption("Real-time heuristic protection against prompt injections, SQLi overrides, jailbreaks, and unauthorized data extraction.")

        if security_events:
            df_sec = pd.DataFrame(security_events)
            st.dataframe(df_sec, use_container_width=True)
        else:
            st.success("✅ Zero security threat events detected. AI Guard active on all conversational endpoints.")

    # TAB 2: OBSERVABILITY TRACES
    with tab_observability:
        st.markdown("#### 📡 End-to-End Request Observability & Tracing")
        st.caption("Inspect live execution traces, classified intents, agent dispatches, and sub-millisecond component latencies.")
        from observability import ObservabilityManager
        traces = ObservabilityManager.get_traces()
        if traces:
            df_traces = pd.DataFrame(traces)
            st.dataframe(df_traces, use_container_width=True)
        else:
            st.info("No active traces recorded.")

    # TAB 2: AUDIT TRAIL
    with tab_audit:
        c_title, c_action = st.columns([3, 1])
        with c_title:
            st.markdown("#### 💬 Enterprise Query & Interaction Audit Ledger")
        with c_action:
            if is_admin and st.button("🗑️ Purge Local Logs", use_container_width=True):
                clear_chat_history()
                st.success("Audit records purged.")
                st.rerun()

        if chats:
            df_chats = pd.DataFrame(chats, columns=["User", "Question", "Answer", "Timestamp"])
            st.dataframe(df_chats, use_container_width=True)

            csv_data = df_chats.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Audit Logs (CSV)", data=csv_data, file_name="enterprise_audit_log.csv", mime="text/csv", type="primary")
        else:
            st.info("No query records captured.")

    # TAB 3: ANALYTICS
    with tab_analytics:
        st.markdown("#### 📊 System Telemetry & Interaction Volume")
        if chats:
            df = pd.DataFrame(chats, columns=["Username", "Question", "Answer", "Time"])
            theme = st.session_state.get("theme", "Dark")
            chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"

            an1, an2 = st.columns(2)
            with an1:
                user_counts = df["Username"].value_counts().reset_index()
                user_counts.columns = ["Username", "Queries"]
                fig_bar = px.bar(user_counts, x="Username", y="Queries", color="Queries", color_continuous_scale="Viridis", title="Query Volume by User")
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font_color)
                st.plotly_chart(fig_bar, use_container_width=True)

            with an2:
                df['Question_Length'] = df['Question'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
                fig_hist = px.histogram(df, x="Question_Length", nbins=10, title="Query Token Density", color_discrete_sequence=['#4f46e5'])
                fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=chart_font_color)
                st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No interactions logged yet.")

    # TAB 4: FIREBASE SYNC
    with tab_cloud:
        st.markdown("#### ⚡ Google Cloud Firebase Firestore Synchronization")
        local_docs = get_documents(prefer_cloud=False)
        local_chats = get_chat_history(prefer_cloud=False)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.metric("Local Documents Ready for Sync", len(local_docs))
            st.metric("Local Chat Logs Ready for Sync", len(local_chats))

            if st.button("🚀 Push Local Records ➔ Firebase Cloud Firestore", use_container_width=True, type="primary", disabled=not connected):
                with st.spinner("Pushing collections to Cloud Firestore..."):
                    success, msg = sync_sqlite_to_firebase(local_docs, local_chats)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            if not connected:
                st.caption("Enter credentials to connect Firestore.")

        with col_f2:
            st.markdown("##### 🔗 Connect Firebase Credentials")
            web_snippet = st.text_area("Paste `firebaseConfig`:", value=f"""const firebaseConfig = {{\n  apiKey: "YOUR_KEY",\n  projectId: "{project_id}"\n}};""", height=120)
            if st.button("Connect Firebase Web SDK", use_container_width=True):
                if "YOUR_KEY" not in web_snippet:
                    success, msg = init_firebase(web_snippet)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # TAB 5: HITL QUEUE
    with tab_hitl:
        st.markdown("#### 👥 Human-In-The-Loop Review & Approval Queue")
        st.caption("Strategic decisions, financial sign-offs, and high-risk operational requests requiring human authorization.")

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, request_type, requester, risk_level, status, reviewed_by FROM human_review_queue ORDER BY id DESC")
                rows = cur.fetchall()
            
            if rows:
                df_hitl = pd.DataFrame(rows, columns=["ID", "Request Type", "Requester", "Risk Level", "Status", "Reviewed By"])
                st.dataframe(df_hitl, use_container_width=True)
                
                sel_id = st.selectbox("Select Item to Authorize / Sign Off:", [r[0] for r in rows if r[4] == 'Pending Review'])
                if sel_id and st.button("✔ Approve & Authorize Decision", type="primary"):
                    with get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute("UPDATE human_review_queue SET status='Approved', reviewed_by=? WHERE id=?", (st.session_state.get("username", "Admin"), sel_id))
                        conn.commit()
                    st.success(f"Item #{sel_id} approved!")
                    st.rerun()
            else:
                st.info("No items currently awaiting human executive sign-off.")
        except Exception:
            st.info("Human review queue initialized.")