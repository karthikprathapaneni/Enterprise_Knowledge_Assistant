import streamlit as st
import plotly.express as px
from orchestrator import AIOrchestrator
from database import save_chat, get_user_profile

def chat_page():
    # Top Copilot Header & Utilities
    c_title, c_actions = st.columns([2.2, 1])
    with c_title:
        st.subheader("💬 Cognitive Copilot — Multi-Agent Intelligence")
        st.caption("Intelligent intent routing across specialized agents: Knowledge, Policy, Problem Solver, Data, and Tasks.")
    with c_actions:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear active conversation history"):
                st.session_state.messages = []
                st.rerun()
        with btn_c2:
            if "messages" in st.session_state and st.session_state.messages:
                chat_export = "\n\n---\n\n".join([
                    f"**{m['role'].upper()} ({m.get('agent_name', 'AI')})**:\n{m['content']}" for m in st.session_state.messages
                ])
                st.download_button(
                    label="📥 Export",
                    data=chat_export,
                    file_name="cognitive_copilot_transcript.md",
                    mime="text/markdown",
                    use_container_width=True,
                    help="Download session transcript"
                )

    # Persona & Parameters
    username = st.session_state.get("username", "user")
    user_profile = get_user_profile(username)

    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        persona = st.radio(
            "Select Reasoning Persona",
            ["Executive", "Technical / Data Analyst", "Compliance & Risk"],
            horizontal=True
        )
    with col_p2:
        top_k = st.slider("Evidence Depth (Top-K Chunks)", 1, 5, 3)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome Card
    if not st.session_state.messages:
        st.markdown("""
            <div class="ai-card" style="margin-bottom: 20px;">
                <div class="ai-title" style="font-size: 1.1rem; margin-bottom: 6px;">
                    ✨ Cognitive Copilot 2.0 Ready
                </div>
                <p class="ai-body" style="margin: 0;">
                    Your request will be dynamically classified and routed to the optimal specialized enterprise agent:
                    <b>Knowledge</b>, <b>Policy Compliance</b>, <b>Troubleshooting Problem Solver</b>, <b>Text-to-SQL Data Analyst</b>, or <b>Task Agent</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Prompt Accelerator Matrix
    st.markdown("##### ⚡ Multi-Agent Query Accelerators:")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("📋 Executive Summary", use_container_width=True):
        quick_query = "Summarize the core objectives, findings, and executive takeaways from the documents."
    if qc2.button("🛠️ VPN Troubleshooting", use_container_width=True):
        quick_query = "My remote VPN is failing to connect and keeps timing out."
    if qc3.button("📊 Cloud Spend Trend", use_container_width=True):
        quick_query = "Show quarterly cloud infrastructure compute spend by department."
    if qc4.button("⚖️ Travel Policy Rules", use_container_width=True):
        quick_query = "What are the reimbursement limits and manager approval requirements for travel?"

    st.write("")

    # Render Chat Stream
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "agent_name" in msg and msg["agent_name"]:
                st.caption(f"Agent: **{msg['agent_name']}**")
            st.markdown(msg["content"])
            
            # Render structured chart if present
            if msg.get("structured_data") is not None and not msg["structured_data"].empty:
                df = msg["structured_data"]
                if "department" in df.columns and "total_amount" in df.columns:
                    fig = px.bar(df, x="department", y="total_amount", color="category", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)
                elif "amount" in df.columns:
                    fig = px.pie(df, names="metric_name" if "metric_name" in df.columns else "department", values="amount", hole=0.5)
                    st.plotly_chart(fig, use_container_width=True)

            if "matches" in msg and msg["matches"]:
                with st.expander(f"📚 Grounded Evidence Citations ({len(msg['matches'])} source chunks)", expanded=False):
                    for i, m in enumerate(msg["matches"], 1):
                        conf = int(min(m["score"] * 100, 99)) if m["score"] < 1.0 else 100
                        st.markdown(f"**Citation #{i}** `Relevance: {conf}%` • *Chunk #{m.get('chunk_idx', 0) + 1}* • *Clearance: Tier {m.get('clearance', 1)}*")
                        st.markdown(f"> {m['chunk']}")
                        st.write("")

    # Chat input
    input_query = st.chat_input("Ask about documents, operational issues, policies, or enterprise data...")
    question = quick_query if quick_query else input_query

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        rag_engine = st.session_state.get("rag", None)
        threshold = st.session_state.get("cfg_threshold", 0.03)

        with st.spinner("AI Orchestrator detecting intent and dispatching to specialized agent..."):
            orch_res = AIOrchestrator.dispatch(
                query=question,
                user_profile=user_profile,
                rag_engine=rag_engine,
                persona=persona,
                top_k=top_k,
                threshold=threshold
            )

        answer_text = orch_res["answer"]
        agent_name = orch_res.get("agent_name", "AI Agent")
        matches = orch_res.get("matches", [])
        struct_data = orch_res.get("structured_data", None)

        trace_id = orch_res.get("trace_id", "TRC-EXEC")
        msg_payload = {
            "role": "assistant",
            "content": answer_text,
            "agent_name": agent_name,
            "trace_id": trace_id,
            "matches": matches,
            "structured_data": struct_data
        }
        st.session_state.messages.append(msg_payload)

        # Save to SQLite & Cloud
        save_chat(username, question, answer_text)

        with st.chat_message("assistant"):
            st.caption(f"Agent: **{agent_name}** • Observability Trace: `{trace_id}`")
            st.markdown(answer_text)

            if struct_data is not None and not struct_data.empty:
                if "department" in struct_data.columns and "total_amount" in struct_data.columns:
                    fig = px.bar(struct_data, x="department", y="total_amount", color="category", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)
                elif "amount" in struct_data.columns:
                    fig = px.pie(struct_data, names="metric_name" if "metric_name" in struct_data.columns else "department", values="amount", hole=0.5)
                    st.plotly_chart(fig, use_container_width=True)

            if matches:
                with st.expander(f"📚 Grounded Evidence Citations ({len(matches)} source chunks)", expanded=True):
                    for i, m in enumerate(matches, 1):
                        conf = int(min(m["score"] * 100, 99)) if m["score"] < 1.0 else 100
                        st.markdown(f"**Citation #{i}** `Relevance: {conf}%` • *Chunk #{m.get('chunk_idx', 0) + 1}* • *Clearance: Tier {m.get('clearance', 1)}*")
                        st.markdown(f"> {m['chunk']}")
                        st.write("")