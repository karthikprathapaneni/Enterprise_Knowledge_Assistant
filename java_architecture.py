import streamlit as st
import os

def java_architecture_page():
    st.subheader("☕ Java Enterprise JVM Architecture & Core Services")
    st.markdown("Enterprise Java (Spring Boot 3.2) cognitive intelligence architecture with Apache Lucene vector indexing and Firebase Firestore Java SDK.")

    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div class="ai-card">
                <span class="ai-metric-label">Java Framework</span>
                <div class="ai-metric-value" style="font-size: 1.5rem;">Spring Boot 3.2</div>
                <span class="ai-badge badge-indigo">Java 17 OpenJDK</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="ai-card">
                <span class="ai-metric-label">Semantic Engine</span>
                <div class="ai-metric-value" style="font-size: 1.5rem;">Apache Lucene</div>
                <span class="ai-badge badge-active">Vector Space Model</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="ai-card">
                <span class="ai-metric-label">PDF Processing</span>
                <div class="ai-metric-value" style="font-size: 1.5rem;">Apache PDFBox</div>
                <span class="ai-badge badge-purple">Stream Ingestion</span>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div class="ai-card">
                <span class="ai-metric-label">Cloud SDK</span>
                <div class="ai-metric-value" style="font-size: 1.5rem;">Firebase Java</div>
                <span class="ai-badge badge-active">Firestore Google Cloud</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    tab_arch, tab_code, tab_endpoints, tab_maven = st.tabs([
        "🏗️ Multi-Tier Architecture",
        "📄 Java Source Code Explorer",
        "🌐 REST API Endpoints",
        "📦 Maven Build Specification"
    ])

    # TAB 1: ARCHITECTURE OVERVIEW
    with tab_arch:
        st.markdown("#### 🏛️ Multi-Tier Java Enterprise Architecture")
        
        st.markdown("""
        ```mermaid
        graph TD
            UI["🌐 Presentation Tier (Web Client / REST API)"]
            
            subgraph "☕ Spring Boot Enterprise Core (JVM 17)"
                CTRL["CognitiveAssistantController.java\n(REST API Gateway)"]
                RAG["RAGEngineService.java\n(Lucene Vector Indexing & Cosine Matching)"]
                DOC["DocumentProcessorService.java\n(Apache PDFBox Document Ingestion)"]
                FIRE["FirebaseSyncService.java\n(Google Firebase Admin Java SDK)"]
            end
            
            subgraph "💾 Persistence & Cloud Storage"
                SQL["SQLite Database\n(Local JDBC Storage)"]
                GCP["Google Cloud Firestore\n(Cloud Knowledge Base)"]
            end

            UI --> CTRL
            CTRL --> RAG
            CTRL --> DOC
            CTRL --> FIRE
            FIRE --> GCP
            CTRL --> SQL
        ```
        """)

        st.markdown("""
        ##### 🚀 Core Java Enterprise Capabilities:
        * **1. High-Performance Java Ingestion:** Apache PDFBox extracts raw binary text and tokenizes streams into sliding window chunks.
        * **2. Lucene Vector Retrieval:** Computes TF-IDF term weights and normalized cosine similarity vectors in native JVM memory.
        * **3. Google Cloud Firestore Integration:** Persists enterprise audit trails and semantic embeddings through the official `com.google.firebase:firebase-admin` Java SDK.
        """)

    # TAB 2: JAVA SOURCE CODE EXPLORER
    with tab_code:
        st.markdown("#### 🔍 Inspect Java Enterprise Source Files")
        
        java_files = {
            "EnterpriseCognitiveApp.java (Main Entry Point)": "src/main/java/com/enterprise/cognitive/EnterpriseCognitiveApp.java",
            "RAGEngineService.java (Lucene Vector Space Engine)": "src/main/java/com/enterprise/cognitive/service/RAGEngineService.java",
            "DocumentProcessorService.java (Apache PDFBox Processing)": "src/main/java/com/enterprise/cognitive/service/DocumentProcessorService.java",
            "FirebaseSyncService.java (Firebase Cloud Firestore Java SDK)": "src/main/java/com/enterprise/cognitive/service/FirebaseSyncService.java",
            "CognitiveAssistantController.java (Spring Boot REST API)": "src/main/java/com/enterprise/cognitive/controller/CognitiveAssistantController.java",
            "KnowledgeChunk.java (Entity Model)": "src/main/java/com/enterprise/cognitive/model/KnowledgeChunk.java",
            "ChatLog.java (Entity Model)": "src/main/java/com/enterprise/cognitive/model/ChatLog.java"
        }

        selected_file_label = st.selectbox("Select Java Class to View:", list(java_files.keys()))
        rel_path = java_files[selected_file_label]
        abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)

        if os.path.exists(abs_path):
            with open(abs_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            st.code(code_content, language="java")
        else:
            st.warning("Selected Java file not found.")

    # TAB 3: REST API ENDPOINTS
    with tab_endpoints:
        st.markdown("#### 🌐 Spring Boot REST Microservice Endpoints")
        st.markdown("""
        | Method | Endpoint | Description | Return Type |
        | :--- | :--- | :--- | :--- |
        | `GET` | `/api/v1/cognitive/status` | JVM Health, Engine Metrics & Firebase Status | `JSON (StatusResponse)` |
        | `POST` | `/api/v1/cognitive/query` | Executes Neural RAG Semantic Retrieval | `JSON (QueryResponse)` |
        | `POST` | `/api/v1/cognitive/ingest` | Multipart PDF Ingestion via Apache PDFBox | `JSON (IngestSummary)` |
        | `POST` | `/api/v1/cognitive/sync` | Triggers Cloud Firestore Synchronization | `JSON (SyncResult)` |
        """)

    # TAB 4: MAVEN BUILD
    with tab_maven:
        st.markdown("#### 📦 `pom.xml` Maven Project Descriptor")
        pom_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pom.xml")
        if os.path.exists(pom_path):
            with open(pom_path, "r", encoding="utf-8") as f:
                pom_content = f.read()
            st.code(pom_content, language="xml")
