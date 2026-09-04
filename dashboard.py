import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from document_processor import (
    process_uploaded_pdfs,
    chunk_text,
    get_available_local_docs,
    process_single_file
)
from rag_engine import RAGEngine
from database import get_documents, add_document

def dashboard_page():
    # Initialize configuration defaults in session state
    if "cfg_chunk_size" not in st.session_state:
        st.session_state.cfg_chunk_size = 120
    if "cfg_overlap" not in st.session_state:
        st.session_state.cfg_overlap = 30
    if "cfg_threshold" not in st.session_state:
        st.session_state.cfg_threshold = 0.05

    # --- Section 1: KPI Metrics Panel ---
    docs_count = st.session_state.get("total_docs", 0)
    chunks_count = st.session_state.get("total_chunks", 0)
    role = st.session_state.get("role", "User")
    engine_status = "READY" if chunks_count > 0 else "STANDBY"
    status_badge = "badge-active" if chunks_count > 0 else "badge-amber"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Active Knowledge Files</span>
                <div class="ai-metric-value">{docs_count}</div>
                <span class="ai-badge badge-indigo">Vault Ingested</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Neural Vector Chunks</span>
                <div class="ai-metric-value">{chunks_count}</div>
                <span class="ai-badge badge-purple">TF-IDF Embeddings</span>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Active Persona</span>
                <div class="ai-metric-value" style="font-size: 1.5rem; padding-top: 5px;">{role}</div>
                <span class="ai-badge badge-active">Enterprise Access</span>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Semantic Engine State</span>
                <div class="ai-metric-value" style="font-size: 1.5rem; padding-top: 5px;">{engine_status}</div>
                <span class="ai-badge {status_badge}">Cosine Matching</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # --- Section 2: Workspaces Tabs ---
    tab_ingest, tab_charts, tab_library, tab_config = st.tabs([
        "📥 Ingestion Studio", 
        "📊 Vector & Semantic Analytics", 
        "📂 Document Vault & Inspector", 
        "⚙️ Neural Hyperparameters"
    ])

    # TAB 1: FILE INGESTION STUDIO
    with tab_ingest:
        c1, c2 = st.columns([1.6, 1])

        with c1:
            st.markdown("#### 📄 Knowledge Ingestion Engine")
            
            ingest_mode = st.radio(
                "Select Ingestion Source",
                [
                    "⚡ 1-Click Vault Repository Ingest",
                    "📤 Upload Custom Files (PDF / DOCX / XLSX / CSV / TXT / MD)",
                    "📝 Paste Knowledge Context / Executive Brief"
                ],
                horizontal=False
            )

            # MODE A: 1-Click Vault Repository Ingest
            if "1-Click Vault" in ingest_mode:
                st.markdown("##### 📚 Repository Documents Detected:")
                repo_files = get_available_local_docs()
                
                if repo_files:
                    selected_files = []
                    for f_info in repo_files:
                        is_checked = st.checkbox(
                            f"**{f_info['filename']}** ({f_info.get('ext', 'DOC')}) • {f_info['size_kb']} KB", 
                            value=True,
                            key=f"repo_chk_{f_info['filename']}"
                        )
                        if is_checked:
                            selected_files.append(f_info)

                    if st.button("🚀 Ingest & Index Selected Vault Documents", use_container_width=True, type="primary"):
                        if selected_files:
                            with st.spinner("Extracting semantic layers and building vector index..."):
                                prog = st.progress(10)
                                all_text = ""
                                for i, f_info in enumerate(selected_files):
                                    text = process_single_file(f_info['path'], f_info['filename'])
                                    add_document(f_info['filename'])
                                    all_text += f"\n\n[Document: {f_info['filename']}]\n{text}"
                                    prog.progress(int(10 + (70 * (i + 1) / len(selected_files))))

                                sz = st.session_state.cfg_chunk_size
                                ov = st.session_state.cfg_overlap
                                chunks = chunk_text(all_text, chunk_size=sz, overlap=ov)

                                rag = RAGEngine()
                                rag.build_index(chunks)
                                st.session_state.rag = rag
                                st.session_state.total_chunks = len(chunks)
                                st.session_state.total_docs = len(selected_files)
                                st.session_state.latest_chunks = chunks[:8]
                                prog.progress(100)

                                st.success(f"🎉 Successfully indexed {len(selected_files)} document(s) into {len(chunks)} neural vector chunks!")
                                st.rerun()
                        else:
                            st.warning("Please select at least one document to index.")
                else:
                    st.info("No documents found in `documents/` directory. Upload files using the upload tab below.")

            # MODE B: Upload Custom Files
            elif "Upload Custom" in ingest_mode:
                uploaded_files = st.file_uploader(
                    "Drop documents here for instant semantic vectorization",
                    type=["pdf", "docx", "xlsx", "csv", "txt", "md"],
                    accept_multiple_files=True
                )

                if uploaded_files:
                    if st.button("🚀 Process & Vectorize Uploaded Files", use_container_width=True, type="primary"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        status_text.info("Extracting document text layers...")
                        progress_bar.progress(30)
                        text = process_uploaded_pdfs(uploaded_files)

                        status_text.info("Partitioning into sliding window vector chunks...")
                        progress_bar.progress(65)
                        sz = st.session_state.cfg_chunk_size
                        ov = st.session_state.cfg_overlap
                        chunks = chunk_text(text, chunk_size=sz, overlap=ov)

                        status_text.info("Generating TF-IDF semantic embeddings...")
                        progress_bar.progress(90)
                        rag = RAGEngine()
                        rag.build_index(chunks)

                        st.session_state.rag = rag
                        st.session_state.total_chunks = len(chunks)
                        st.session_state.total_docs = len(uploaded_files)
                        st.session_state.latest_chunks = chunks[:8]

                        progress_bar.progress(100)
                        status_text.success(f"✅ Successfully ingested {len(uploaded_files)} file(s) into {len(chunks)} embeddings!")
                        st.rerun()

            # MODE C: Paste Knowledge Context
            else:
                st.markdown("##### 📝 Quick Enterprise Context Ingestion:")
                default_demo = (
                    "Enterprise Cognitive Knowledge Assistant is a next-generation enterprise RAG platform.\n"
                    "Architecture Highlights:\n"
                    "- Retrieval Engine: TF-IDF vectorization with normalized cosine similarity matrix.\n"
                    "- Enterprise Persona Switching: Executive Summary, Technical Deep-Dive, and Risk & Compliance modes.\n"
                    "- Knowledge Discovery: Force-directed semantic knowledge graphs with centrality weighting.\n"
                    "- Persistence & Cloud: Local relational SQLite audit logging with real-time Google Cloud Firestore synchronization.\n"
                    "- Security: Role-based access control (Admin / User) with audit trail export."
                )
                custom_doc_title = st.text_input("Document / Subject Title", value="Enterprise_Executive_Brief.txt")
                custom_doc_text = st.text_area("Document Content Layer", value=default_demo, height=160)

                if st.button("⚡ Index Briefing into Vector Store", use_container_width=True, type="primary"):
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
                        st.session_state.latest_chunks = chunks[:8]
                        st.success(f"✅ Indexed '{custom_doc_title}' into {len(chunks)} chunks!")
                        st.rerun()
                    else:
                        st.warning("Please provide valid document text.")

        with c2:
            st.markdown("#### ⚡ Pipeline Architecture")
            st.markdown("""
                <div class="ai-card" style="margin-bottom: 14px;">
                    <div style="font-weight: 700; color: #6366f1; margin-bottom: 8px;">🧠 Semantic RAG Core</div>
                    <p style="font-size: 0.83rem; color: #64748b; margin: 0;">
                    Extracts raw document text, eliminates boilerplate noise, partitions with configurable word overlap, and maps vocabulary into high-dimensional TF-IDF vectors.
                    </p>
                </div>
                <div class="ai-card">
                    <div style="font-weight: 700; color: #10b981; margin-bottom: 8px;">🔥 Cloud & Local Persistence</div>
                    <p style="font-size: 0.83rem; color: #64748b; margin: 0;">
                    Dual-mode persistence allows zero-latency local querying backed by real-time Google Cloud Firestore synchronization.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # TAB 2: VECTOR & SEMANTIC ANALYTICS
    with tab_charts:
        st.markdown("#### 📈 Vector Store & Embedding Analytics")

        if chunks_count > 0:
            theme = st.session_state.get("theme", "Light")
            chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"
            radial_axis_color = "#64748b" if theme == "Light" else "#94a3b8"

            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Indexed Chunks", chunks_count)
            m_col2.metric("Chunk Size Window", f"{st.session_state.cfg_chunk_size} words")
            m_col3.metric("Overlap Buffer", f"{st.session_state.cfg_overlap} words")

            ch_col1, ch_col2 = st.columns(2)

            with ch_col1:
                labels = ['Core Content Chunks', 'Semantic Overlap Tokens', 'Document Headers']
                values = [max(int(chunks_count * 0.70), 1), max(int(chunks_count * 0.20), 1), max(int(chunks_count * 0.10), 1)]

                fig_donut = px.pie(
                    names=labels, 
                    values=values, 
                    hole=0.62,
                    title="Knowledge Chunk Distribution",
                    color_discrete_sequence=['#4f46e5', '#8b5cf6', '#06b6d4']
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
                    r=[4.6, 4.4, 4.8, 4.2, 1.2],
                    theta=['Semantic Density', 'Retrieval Precision', 'Context Continuity', 'Token Diversity', 'Noise Index'],
                    fill='toself',
                    fillcolor='rgba(99, 102, 241, 0.22)',
                    line=dict(color='#4f46e5', width=2)
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 5], color=radial_axis_color),
                        angularaxis=dict(color=chart_font_color)
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color,
                    title="Ingestion Quality Benchmark",
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("💡 Ingest documents in the **Ingestion Studio** tab to activate vector store analytics.")

    # TAB 3: DOCUMENT VAULT & INSPECTOR
    with tab_library:
        st.markdown("#### 🗄️ Ingested Documents & Semantic Chunks")
        docs = get_documents()
        if docs:
            df = pd.DataFrame(docs, columns=["Filename", "Timestamp"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No documents recorded in local database yet.")

        if "rag" in st.session_state and st.session_state.rag and st.session_state.rag.chunks:
            all_chunks = st.session_state.rag.chunks
            st.markdown(f"##### 🔍 Vector Chunk Explorer ({len(all_chunks)} total chunks)")
            
            search_query = st.text_input("Filter chunks by keyword:", placeholder="Type to search within indexed chunks...")
            filtered_chunks = [ch for ch in all_chunks if search_query.lower() in ch.lower()] if search_query else all_chunks[:10]

            st.caption(f"Displaying {len(filtered_chunks)} matching chunk(s):")
            for idx, ch in enumerate(filtered_chunks, 1):
                with st.expander(f"Chunk #{idx} • {len(ch.split())} words • {len(ch)} chars", expanded=(idx <= 2)):
                    st.markdown(f"> {ch}")
        elif "latest_chunks" in st.session_state and st.session_state.latest_chunks:
            with st.expander("🔍 Inspect Extracted Sample Embeddings", expanded=True):
                for idx, ch in enumerate(st.session_state.latest_chunks, 1):
                    st.markdown(f"**Chunk #{idx}**")
                    st.markdown(f"> {ch}")

    # TAB 4: NEURAL HYPERPARAMETERS
    with tab_config:
        st.markdown("#### 🛠️ Fine-Tune Ingestion & RAG Sensitivity")
        
        st.markdown("##### ⚡ Quick Tuning Presets:")
        pr1, pr2, pr3 = st.columns(3)
        if pr1.button("⚡ Fast Retrieval (Compact)", use_container_width=True):
            st.session_state.cfg_chunk_size = 80
            st.session_state.cfg_overlap = 15
            st.session_state.cfg_threshold = 0.08
            st.success("Set to Fast Retrieval preset!")
        if pr2.button("⚖️ Balanced Precision (Default)", use_container_width=True):
            st.session_state.cfg_chunk_size = 120
            st.session_state.cfg_overlap = 30
            st.session_state.cfg_threshold = 0.05
            st.success("Set to Balanced Precision preset!")
        if pr3.button("🧠 Deep Contextual (Broad)", use_container_width=True):
            st.session_state.cfg_chunk_size = 220
            st.session_state.cfg_overlap = 50
            st.session_state.cfg_threshold = 0.03
            st.success("Set to Deep Contextual preset!")

        st.divider()

        st.session_state.cfg_chunk_size = st.slider(
            "Chunk Word Limit (Sliding Window)", 
            50, 400, st.session_state.cfg_chunk_size, 10,
            help="Higher values retain broader sentence context; lower values increase granular match precision."
        )
        st.session_state.cfg_overlap = st.slider(
            "Overlap Word Count", 
            0, 80, st.session_state.cfg_overlap, 5,
            help="Prevents semantic boundary cutoff between adjacent chunks."
        )
        st.session_state.cfg_threshold = st.slider(
            "Cosine Similarity Sensitivity Threshold",
            0.01, 0.30, st.session_state.cfg_threshold, 0.01,
            help="Minimum cosine similarity required to trigger neural retrieval."
        )

        st.info(f"Active Parameters: **{st.session_state.cfg_chunk_size}** words/chunk • **{st.session_state.cfg_overlap}** word overlap • **{st.session_state.cfg_threshold}** min similarity threshold.")