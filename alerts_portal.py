import streamlit as st
from database import get_alerts, mark_alert_read, add_task, get_connection
from datetime import datetime

def alerts_portal_page():
    st.subheader("🔔 Proactive Enterprise Intelligence Alerts")
    st.caption("Automated detection of policy updates, approaching regulatory deadlines, cross-document conflicts, and critical operational events.")

    alerts = get_alerts()

    # Metrics
    c1, c2, c3 = st.columns(3)
    unread_cnt = sum(1 for a in alerts if not a['is_read'])
    high_cnt = sum(1 for a in alerts if a['severity'] == 'High')
    with c1:
        st.metric("Total Active Alerts", len(alerts))
    with c2:
        st.metric("Unread / Pending", unread_cnt)
    with c3:
        st.metric("Critical / High Severity", high_cnt)

    st.write("")

    # Filter by Severity
    f_col1, f_col2 = st.columns([1.5, 2])
    with f_col1:
        sev_filter = st.selectbox("Filter by Severity:", ["All Severities", "High", "Medium", "Low"])

    filtered_alerts = [a for a in alerts if sev_filter == "All Severities" or a["severity"] == sev_filter]

    st.write("")

    if filtered_alerts:
        for alt in filtered_alerts:
            is_read = alt["is_read"]
            sev_badge = "badge-amber" if alt["severity"] == "High" else ("badge-indigo" if alt["severity"] == "Medium" else "badge-active")
            border_col = "#ef4444" if alt["severity"] == "High" else "#6366f1"

            st.markdown(f"""
                <div class="ai-card" style="margin-bottom: 14px; border-left: 3px solid {border_col}; opacity: {0.75 if is_read else 1.0};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span class="ai-title" style="font-size: 1.05rem; margin: 0;">{alt['title']}</span>
                        <div>
                            <span class="ai-badge {sev_badge}">{alt['severity']} Priority</span>
                            <span class="ai-badge badge-purple">{alt['alert_type']}</span>
                        </div>
                    </div>
                    <p class="ai-body" style="margin: 8px 0;">{alt['message']}</p>
                    <div class="ai-meta">
                        Target Audience: <b>{alt['target_role']}</b> • Recorded: <i>{alt['created_at']}</i> • Status: <b>{'Read' if is_read else 'Unread'}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            act1, act2 = st.columns([2, 1])
            with act1:
                if not is_read:
                    if st.button("✔ Acknowledge / Mark Read", key=f"ack_{alt['id']}"):
                        mark_alert_read(alt["id"])
                        st.rerun()
            with act2:
                if st.button("➕ Convert to Task in My Work", key=f"task_{alt['id']}"):
                    username = st.session_state.get("username", "user")
                    add_task(
                        username=username,
                        title=f"Alert: {alt['title'][:40]}",
                        description=alt['message'],
                        priority=alt['severity'],
                        source_doc=f"Alert #{alt['id']} ({alt['alert_type']})"
                    )
                    st.success("✅ Synchronized to My Work task list!")
            st.divider()
    else:
        st.info("No alerts matching selected criteria.")

    with st.expander("➕ Broadcast New Enterprise Intelligence Alert (Admin/Lead)", expanded=False):
        b_col1, b_col2 = st.columns([2, 1])
        with b_col1:
            a_title = st.text_input("Alert Title")
            a_msg = st.text_area("Alert Message / Context")
        with b_col2:
            a_type = st.selectbox("Category", ["Policy Conflict", "Regulatory Deadline", "Knowledge Update", "System Outage"])
            a_sev = st.selectbox("Severity", ["High", "Medium", "Low"])
            a_target = st.selectbox("Target Clearance Audience", ["All", "Admin", "Manager", "User"])
            if st.button("🚀 Broadcast Alert", type="primary", use_container_width=True):
                if a_title and a_msg:
                    with get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO intelligence_alerts(alert_type, title, message, severity, target_role, is_read, created_at) VALUES(?,?,?,?,?,?,?)",
                            (a_type, a_title, a_msg, a_sev, a_target, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        )
                        conn.commit()
                    st.success("Alert broadcast successfully!")
                    st.rerun()
