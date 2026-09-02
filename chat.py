import streamlit as st
from database import save_chat

def chat_page():
    st.subheader("💬 AI Cognitive Chat Assistant")

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("Ask deep questions across all ingested enterprise documents.")
    with c2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display empty state welcome prompt if no messages yet
    if not st.session_state.messages:
        st.info("💡 **Tip:** Upload and index documents in the **Dashboard** tab first, then ask questions here. You can also try quick prompt templates below.")

    # Quick prompt buttons
    st.markdown("**Suggested Quick Inquiries:**")
    qc1, qc2, qc3 = st.columns(3)
    quick_query = None
    if qc1.button("📋 Summarize key points", use_container_width=True):
        quick_query = "Summarize the key points and core findings from the documents."
    if qc2.button("🔍 Action items & insights", use_container_width=True):
        quick_query = "What are the main action items and conclusions?"
    if qc3.button("📊 Data & metrics overview", use_container_width=True):
        quick_query = "What data, metrics, and quantitative figures are mentioned?"

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    input_query = st.chat_input("Ask a question based on your uploaded documents...")
    question = quick_query if quick_query else input_query

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        if "rag" not in st.session_state or not st.session_state.rag.chunks:
            answer = "⚠️ **No indexed documents found.** Please navigate to the **Dashboard** tab and process your PDF documents first."
        else:
            with st.spinner("Retrieving neural context and generating answer..."):
                answer = st.session_state.rag.answer(question)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        username = st.session_state.get("username", "Guest")
        save_chat(username, question, answer)

        with st.chat_message("assistant"):
            st.markdown(answer)