import streamlit as st
from database import get_user_profile, get_tasks, add_task, update_task_status, get_alerts
from orchestrator import AIOrchestrator

def personal_assistant_page():
    username = st.session_state.get("username", "user")
    profile = get_user_profile(username)
    rag_engine = st.session_state.get("rag", None)

    st.subheader(f"🧠 My AI Assistant — {profile['full_name']}")
    st.caption(f"Role: {profile['title']} • Department: {profile['department']} • Clearance: Level {profile['clearance_level']}")

    tab_overview, tab_tasks, tab_qa = st.tabs([
        "⚡ Daily Productivity Hub",
        "✅ My Tasks & Action Tracking",
        "💬 Personalized Assistant Dialogue"
    ])

    # TAB 1: DAILY PRODUCTIVITY HUB
    with tab_overview:
        c1, c2, c3 = st.columns(3)
        user_tasks = get_tasks(username)
        pending_cnt = sum(1 for t in user_tasks if t['status'] != 'Completed')
        alerts = get_alerts()
        unread_alerts = sum(1 for a in alerts if not a['is_read'])

        with c1:
            st.markdown(f"""
                <div class="ai-card">
                    <span class="ai-metric-label">Pending Action Tasks</span>
                    <div class="ai-metric-value">{pending_cnt}</div>
                    <span class="ai-badge badge-amber">Action Required</span>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="ai-card">
                    <span class="ai-metric-label">Active Alerts</span>
                    <div class="ai-metric-value">{unread_alerts}</div>
                    <span class="ai-badge badge-purple">Policy & Ops</span>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="ai-card">
                    <span class="ai-metric-label">Security Clearance</span>
                    <div class="ai-metric-value">Tier {profile['clearance_level']}</div>
                    <span class="ai-badge badge-active">{profile['department']}</span>
                </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 📌 Recommended Next Actions for Today:")
        st.markdown("""
        * 📋 **Review Travel Expense Limits:** Verification required against newly uploaded Q3 policy guidelines.
        * 🔒 **Complete Cyber Hygiene Attestation:** Annual compliance window closes in 48 hours.
        * ⚙️ **Inspect System Architecture:** Review Hospital Appointment Management System database schema.
        """)

    # TAB 2: MY TASKS & ACTION TRACKING
    with tab_tasks:
        st.markdown("#### ✅ My Work — Enterprise Task Stream")
        
        with st.expander("➕ Create New Action Item", expanded=False):
            t_col1, t_col2 = st.columns([2, 1])
            with t_col1:
                new_title = st.text_input("Task Title", placeholder="e.g., Update compliance checklist...")
                new_desc = st.text_area("Description", placeholder="Details and next steps...", height=80)
            with t_col2:
                new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                new_source = st.text_input("Reference Source Document", value="Personal Work Hub")
                if st.button("Save Task to My Work", use_container_width=True, type="primary"):
                    if new_title.strip():
                        add_task(username, new_title, new_desc, new_priority, source_doc=new_source)
                        st.success("Task added!")
                        st.rerun()

        st.write("")
        tasks = get_tasks(username)
        if tasks:
            for t in tasks:
                t_card_col1, t_card_col2, t_card_col3 = st.columns([3, 1.2, 1])
                badge_class = "badge-active" if t["status"] == "Completed" else ("badge-amber" if t["priority"] == "High" else "badge-indigo")
                
                with t_card_col1:
                    st.markdown(f"**{t['title']}**")
                    st.caption(f"{t['description']} • *Ref: {t['source_doc']}*")
                with t_card_col2:
                    st.markdown(f'<span class="ai-badge {badge_class}">{t["priority"]} • {t["status"]}</span>', unsafe_allow_html=True)
                    st.caption(f"Due: {t['due_date']}")
                with t_card_col3:
                    new_st = "Completed" if t["status"] != "Completed" else "Pending"
                    btn_label = "✔ Complete" if t["status"] != "Completed" else "↩ Re-open"
                    if st.button(btn_label, key=f"t_btn_{t['id']}", use_container_width=True):
                        update_task_status(t["id"], new_st)
                        st.rerun()
                st.divider()
        else:
            st.info("No active tasks logged in your work queue.")

    # TAB 3: PERSONALIZED ASSISTANT DIALOGUE
    with tab_qa:
        st.markdown("#### 💬 Personalized Work Copilot")
        st.caption("Ask questions about your role responsibilities, assigned tasks, and departmental guidelines.")

        p_query = st.text_input("Ask your personal assistant:", placeholder="e.g., What are my main responsibilities under our security policy?")
        if st.button("Submit Inquiry", key="p_btn", type="primary", use_container_width=True):
            if p_query.strip():
                with st.spinner("Synthesizing personalized guidance..."):
                    res = AIOrchestrator.dispatch(
                        query=p_query,
                        user_profile=profile,
                        rag_engine=rag_engine,
                        persona="Executive"
                    )
                    st.markdown(res["answer"])
                    if res.get("matches"):
                        with st.expander("📚 Grounded Citations", expanded=False):
                            for idx, m in enumerate(res["matches"], 1):
                                st.markdown(f"**Citation #{idx}** • *Chunk #{m.get('chunk_idx', 0) + 1}*")
                                st.markdown(f"> {m['chunk']}")
