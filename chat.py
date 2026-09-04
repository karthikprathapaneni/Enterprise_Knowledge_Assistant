import streamlit as st
import json
from database import save_chat

def chat_page():
    # Top Copilot Header & Utilities
    c_title, c_actions = st.columns([2.2, 1])
    with c_title:
        st.subheader("💬 Cognitive Copilot")
        st.caption("Ask deep questions across all ingested enterprise documents with multi-persona neural synthesis.")
    with c_actions:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear active conversation history"):
                st.session_state.messages = []
                st.rerun()
        with btn_c2:
            if "messages" in st.session_state and st.session_state.messages:
                chat_export = "\n\n---\n\n".join([
                    f"**{m['role'].upper()}**:\n{m['content']}" for m in st.session_state.messages
                ])
                st.download_button(
                    label="📥 Export",
                    data=chat_export,
                    file_name="cognitive_copilot_transcript.md",
                    mime="text/markdown",
                    use_container_width=True,
                    help="Download session transcript"
                )

    # Persona Switcher Bar
    st.markdown("##### 🎭 Active Reasoning Persona:")
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        persona = st.radio(
            "Select Persona",
            ["Executive", "Technical / Data Analyst", "Compliance & Risk"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with col_p2:
        top_k = st.slider("Max Evidence Chunks (Top-K)", 1, 5, 3)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display empty state welcome prompt if no messages yet
    if not st.session_state.messages:
        st.markdown("""
            <div class="ai-card" style="margin-bottom: 20px;">
                <div style="font-weight: 800; font-size: 1.1rem; color: #6366f1; margin-bottom: 6px;">
                    ✨ Welcome to Cognitive Copilot
                </div>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
                    Your multi-persona enterprise assistant is connected to your vectorized document vault. Ask any natural language question or pick an accelerator card below.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Prompt Accelerator Matrix
    st.markdown("##### ⚡ Quick Prompt Accelerators:")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("📋 Executive Summary", use_container_width=True):
        quick_query = "Summarize the core objectives, findings, and executive takeaways from the documents."
    if qc2.button("⚖️ Risk & Governance", use_container_width=True):
        quick_query = "What are the primary risk factors, policy constraints, and regulatory requirements outlined?"
    if qc3.button("📊 Quantitative Metrics", use_container_width=True):
        quick_query = "Extract all key metrics, percentages, timelines, and measurable data figures."
    if qc4.button("🚀 Action Items", use_container_width=True):
        quick_query = "What are the designated next steps, procedures, and responsibilities specified?"

    st.write("")

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "matches" in msg and msg["matches"]:
                with st.expander(f"📚 Grounded Citations ({len(msg['matches'])} source chunks)", expanded=False):
                    for i, m in enumerate(msg["matches"], 1):
                        conf = int(min(m["score"] * 100, 99)) if m["score"] < 1.0 else 100
                        st.markdown(f"**Citation #{i}** `Relevance: {conf}%` • *Chunk #{m.get('chunk_idx', 0) + 1}*")
                        st.markdown(f"> {m['chunk']}")
                        st.write("")

    # Input handling
    input_query = st.chat_input("Ask a question based on your uploaded documents...")
    question = quick_query if quick_query else input_query

    if question:
        # Append and render user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve and generate answer
        threshold = st.session_state.get("cfg_threshold", 0.03)
        if "rag" not in st.session_state or not st.session_state.rag or not st.session_state.rag.chunks:
            answer_text = "⚠️ **No indexed documents found.** Please navigate to the **Neural Document Vault** and process your repository or uploaded documents first."
            matches = []
        else:
            with st.spinner(f"Synthesizing {persona} analysis from neural vector index..."):
                rag_res = st.session_state.rag.answer_with_persona(
                    question=question,
                    persona=persona,
                    top_k=top_k,
                    threshold=threshold
                )
                answer_text = rag_res["answer"]
                matches = rag_res.get("matches", [])

        # Append assistant message with citations metadata
        msg_payload = {
            "role": "assistant",
            "content": answer_text,
            "matches": matches
        }
        st.session_state.messages.append(msg_payload)

        # Save to database (SQLite & Firebase)
        username = st.session_state.get("username", "Guest")
        save_chat(username, question, answer_text)

        # Render assistant response
        with st.chat_message("assistant"):
            st.markdown(answer_text)
            if matches:
                with st.expander(f"📚 Grounded Citations ({len(matches)} source chunks)", expanded=True):
                    for i, m in enumerate(matches, 1):
                        conf = int(min(m["score"] * 100, 99)) if m["score"] < 1.0 else 100
                        st.markdown(f"**Citation #{i}** `Relevance: {conf}%` • *Chunk #{m.get('chunk_idx', 0) + 1}*")
                        st.markdown(f"> {m['chunk']}")
                        st.write("")