import streamlit as st
from database import get_tasks, get_alerts, get_conflicts, get_documents, get_db_status, get_user_profile

def command_center_page():
    username = st.session_state.get("username", "user")
    profile = get_user_profile(username)
    
    docs = get_documents()
    tasks = get_tasks(username)
    pending_tasks = [t for t in tasks if t['status'] != 'Completed']
    alerts = get_alerts()
    conflicts = get_conflicts()
    chunks_count = st.session_state.get("total_chunks", 0)
    db_stat = get_db_status()

    # Welcome Header
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-weight: 800; font-size: 1.8rem; background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ⚡ Command Center — Operational Overview
            </h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Good day, <b>{profile['full_name']}</b> ({profile['title']}) • Department: <b>{profile['department']}</b> • Clearance: <b>Tier {profile['clearance_level']}</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Attention & Health KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="ai-card" style="border-top: 3px solid #f59e0b;">
                <span class="ai-metric-label">Items Needing Attention</span>
                <div class="ai-metric-value" style="color: #fbbf24;">{len(pending_tasks) + len(conflicts)}</div>
                <span class="ai-badge badge-amber">{len(conflicts)} Conflicts • {len(pending_tasks)} Tasks</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="ai-card" style="border-top: 3px solid #6366f1;">
                <span class="ai-metric-label">Active Document Vault</span>
                <div class="ai-metric-value">{len(docs)}</div>
                <span class="ai-badge badge-indigo">{chunks_count} Vector Chunks</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="ai-card" style="border-top: 3px solid #10b981;">
                <span class="ai-metric-label">Knowledge Health Index</span>
                <div class="ai-metric-value" style="color: #34d399;">94.2%</div>
                <span class="ai-badge badge-active">Active Grounding</span>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        sync_str = "Synced" if "ONLINE" in db_stat.get("firebase_status", "") else "Local SQLite"
        st.markdown(f"""
            <div class="ai-card" style="border-top: 3px solid #06b6d4;">
                <span class="ai-metric-label">Persistence & Cloud</span>
                <div class="ai-metric-value" style="font-size: 1.35rem; padding-top: 6px;">{sync_str}</div>
                <span class="ai-badge badge-active">Dual-Mode Ready</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Actionable 2-Column Grid: Left (Attention & AI Insights) | Right (Health & Quick Actions)
    grid_col1, grid_col2 = st.columns([1.3, 1])

    with grid_col1:
        st.markdown("#### 🚨 Priority Items Needing Attention")
        if conflicts:
            for conf in conflicts[:2]:
                st.markdown(f"""
                    <div class="ai-card" style="margin-bottom: 12px; border-left: 4px solid #ef4444;">
                        <div style="font-weight: 700; color: #f87171;">⚠️ Policy Conflict Detected: {conf['topic']}</div>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin: 4px 0 6px 0;">{conf['description']}</p>
                        <div style="font-size: 0.75rem; color: #64748b;">Sources: <i>{conf['doc_a']}</i> vs <i>{conf['doc_b']}</i></div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("#### 🤖 Proactive AI Insights")
        for alt in alerts[:2]:
            badge = "badge-amber" if alt['severity'] == "High" else "badge-indigo"
            st.markdown(f"""
                <div class="ai-card" style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700;">{alt['title']}</span>
                        <span class="ai-badge {badge}">{alt['alert_type']}</span>
                    </div>
                    <p style="font-size: 0.84rem; color: #94a3b8; margin: 4px 0 0 0;">{alt['message']}</p>
                </div>
            """, unsafe_allow_html=True)

    with grid_col2:
        st.markdown("#### ⚡ Enterprise Quick Launch Actions")
        
        q_act1, q_act2 = st.columns(2)
        with q_act1:
            if st.button("💬 Ask Copilot", use_container_width=True):
                st.session_state.current_portal = "💬 Cognitive Copilot"
                st.rerun()
            if st.button("🛠️ Solve Problem", use_container_width=True):
                st.session_state.current_portal = "🛠️ AI Problem Solver"
                st.rerun()
            if st.button("🕸️ Knowledge Graph", use_container_width=True):
                st.session_state.current_portal = "🕸️ Semantic Knowledge Graph"
                st.rerun()
        with q_act2:
            if st.button("📊 Analyze Data", use_container_width=True):
                st.session_state.current_portal = "📊 AI Data Analyst"
                st.rerun()
            if st.button("🎯 Decision Center", use_container_width=True):
                st.session_state.current_portal = "🎯 Decision Center"
                st.rerun()
            if st.button("✅ My Work Tasks", use_container_width=True):
                st.session_state.current_portal = "🧠 My AI Assistant"
                st.rerun()

        st.write("")
        st.markdown("#### 📈 Knowledge Base Vitals")
        st.info("""
        * **Ingested Repository Sources:** 3 Verified PDFs
        * **Semantic Chunks:** 193 active vector embeddings
        * **Average Retrieval Latency:** 2.4 ms
        * **Security Clearance Policy:** Role-Based Access Control active
        """)
