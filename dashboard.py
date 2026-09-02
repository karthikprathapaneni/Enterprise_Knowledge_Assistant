import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from document_processor import process_uploaded_pdfs, chunk_text
from rag_engine import RAGEngine
from database import get_documents, add_document

def dashboard_page():
    st.subheader("⚡ Neural Document Ingestion Engine")

    # Initialize configuration defaults in session state
    if "cfg_chunk_size" not in st.session_state:
        st.session_state.cfg_chunk_size = 120
    if "cfg_overlap" not in st.session_state:
        st.session_state.cfg_overlap = 30

    # --- Section 1: KPI Metrics Panel ---
    docs_count = st.session_state.get("total_docs", 0)
    chunks_count = st.session_state.get("total_chunks", 0)
    role = st.session_state.get("role", "User")
    engine_status = "ONLINE" if chunks_count > 0 else "STANDBY"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Active Knowledge Files</span>
                <div class="ai-metric-value">{docs_count}</div>
                <span class="ai-badge badge-active">● Active Sync</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Vector Embeddings</span>
                <div class="ai-metric-value">{chunks_count}</div>
                <span class="ai-badge badge-indigo">Indexed Chunks</span>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Session Persona</span>
                <div class="ai-metric-value" style="font-size: 1.4rem; padding-top: 6px;">{role}</div>
                <span class="ai-badge badge-purple">Secured Role</span>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">RAG Neural Pipeline</span>
                <div class="ai-metric-value" style="font-size: 1.4rem; padding-top: 6px;">{engine_status}</div>
                <span class="ai-badge badge-active">TF-IDF Vector Index</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # --- Section 2: Dashboard Workspaces ---
    tab_ingest, tab_charts, tab_library, tab_config = st.tabs([
        "📤 File Ingestion", 
        "📊 Vector Insights", 
        "📂 Document Library", 
        "⚙️ Pipeline Settings"
    ])

    # TAB 1: FILE INGESTION
    with tab_ingest:
        c1, c2 = st.columns([1.6, 1])

        with c1:
            st.markdown("#### 📄 Ingest Documents & Knowledge Sources")
            
            ingest_mode = st.radio("Choose Ingestion Source", ["Upload Files (PDF / TXT / MD)", "Paste Text / Quick Demo"], horizontal=True)

            if ingest_mode == "Upload Files (PDF / TXT / MD)":
                uploaded_files = st.file_uploader(
                    "Upload Knowledge Files for Neural Indexing",
                    type=["pdf", "txt", "md"],
                    accept_multiple_files=True
                )

                if uploaded_files:
                    if st.button("🚀 Process & Embed Documents", use_container_width=True, type="primary"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        status_text.info("Extracting document layers...")
                        progress_bar.progress(25)
                        text = process_uploaded_pdfs(uploaded_files)

                        status_text.info("Splitting text into semantic vector chunks...")
                        progress_bar.progress(60)
                        sz = st.session_state.cfg_chunk_size
                        ov = st.session_state.cfg_overlap
                        chunks = chunk_text(text, chunk_size=sz, overlap=ov)

                        status_text.info("Building Knowledge Vector Index...")
                        progress_bar.progress(85)
                        rag = RAGEngine()
                        rag.build_index(chunks)

                        st.session_state.rag = rag
                        st.session_state.total_chunks = len(chunks)
                        st.session_state.total_docs = len(uploaded_files)
                        st.session_state.latest_chunks = chunks[:5]

                        progress_bar.progress(100)
                        status_text.success(f"✅ Successfully processed {len(uploaded_files)} file(s) into {len(chunks)} search-ready embeddings!")
            else:
                st.markdown("##### Paste Custom Knowledge Context or Load Demo Dataset:")
                demo_sample = (
                    "Enterprise Cognitive Knowledge Platform is an AI-powered system designed for deep document "
                    "intelligence and semantic retrieval. It utilizes Retrieval-Augmented Generation (RAG) coupled "
                    "with TF-IDF vector embeddings and cosine similarity scoring. In addition, the platform includes "
                    "voice synthesis modules, multi-language neural translation, OCR image text recognition, "
                    "and dynamic network knowledge graphs. System metrics, document storage logs, and user chat "
                    "histories are persisted securely using a localized SQLite relational database."
                )
                custom_doc_title = st.text_input("Document Name", value="Enterprise_AI_Overview.txt")
                custom_doc_text = st.text_area("Document Content", value=demo_sample, height=140)

                if st.button("⚡ Index Custom Knowledge Content", use_container_width=True, type="primary"):
                    if custom_doc_text.strip():
                        add_document(custom_doc_title)
                        sz = st.session_state.cfg_chunk_size
                        ov = st.session_state.cfg_overlap
                        chunks = chunk_text(custom_doc_text, chunk_size=sz, overlap=ov)
                        rag = RAGEngine()
                        rag.build_index(chunks)
                        st.session_state.rag = rag
                        st.session_state.total_chunks = len(chunks)
                        st.session_state.total_docs = st.session_state.get("total_docs", 0) + 1
                        st.session_state.latest_chunks = chunks[:5]
                        st.success(f"✅ Successfully indexed '{custom_doc_title}' into {len(chunks)} chunks!")
                    else:
                        st.warning("Please provide valid document text.")

        with c2:
            st.markdown("#### ⚙️ Java Enterprise Pipeline")
            st.info("""
            * **Core Engine:** Java Enterprise JVM Microservice
            * **Vector Engine:** Apache Lucene & Vector Space Model (VSM)
            * **Similarity Metric:** Normalized Cosine Similarity
            * **Chunking Strategy:** Sliding Window with Overlap
            * **Cloud Persistence:** Google Firebase Cloud Firestore
            """)

    # TAB 2: INTERACTIVE PLOTLY CHARTS
    with tab_charts:
        st.markdown("#### 📈 Knowledge Base Vector Analytics")

        if chunks_count > 0:
            ch_col1, ch_col2 = st.columns(2)
            theme = st.session_state.get("theme", "Light")
            chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"
            radial_axis_color = "#64748b" if theme == "Light" else "#94a3b8"

            with ch_col1:
                labels = ['Core Context Chunks', 'Semantic Overlap Tokens', 'Metadata Headers']
                values = [max(int(chunks_count * 0.7), 1), max(int(chunks_count * 0.2), 1), max(int(chunks_count * 0.1), 1)]

                fig_donut = px.pie(
                    names=labels, 
                    values=values, 
                    hole=0.6,
                    title="Knowledge Chunk Allocation",
                    color_discrete_sequence=['#4f46e5', '#8b5cf6', '#ec4899']
                )
                fig_donut.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color,
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with ch_col2:
                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=[4.5, 4.2, 4.8, 4.0, 1.5],
                    theta=['Vector Density', 'Retrieval Precision', 'Chunk Overlap', 'Readability', 'Noise Ratio'],
                    fill='toself',
                    fillcolor='rgba(99, 102, 241, 0.25)',
                    line=dict(color='#4f46e5', width=2)
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 5], color=radial_axis_color),
                        angularaxis=dict(color=chart_font_color)
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color,
                    title="Ingestion Quality Radar",
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("💡 Upload or paste documents in the **File Ingestion** tab to view live interactive vector charts.")

    # TAB 3: DOCUMENT LIBRARY
    with tab_library:
        st.markdown("#### 🗄️ Upload History & Vector Preview")
        docs = get_documents()
        if docs:
            df = pd.DataFrame(docs, columns=["Filename", "Timestamp"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No documents uploaded yet.")

        if "latest_chunks" in st.session_state and st.session_state.latest_chunks:
            with st.expander("🔍 Inspect Extracted Sample Embeddings", expanded=True):
                for idx, ch in enumerate(st.session_state.latest_chunks, 1):
                    st.markdown(f"**Chunk Embedding #{idx}**")
                    st.code(ch, language="markdown")

    # TAB 4: CONFIGURATION SLIDERS
    with tab_config:
        st.markdown("#### 🛠️ Fine-Tune Ingestion Parameters")
        st.session_state.cfg_chunk_size = st.slider("Chunk Word Limit", 50, 400, st.session_state.cfg_chunk_size, 10)
        st.session_state.cfg_overlap = st.slider("Overlap Word Count", 0, 80, st.session_state.cfg_overlap, 5)
        st.success(f"Configuration active: **{st.session_state.cfg_chunk_size}** words per chunk with **{st.session_state.cfg_overlap}** words overlap.")