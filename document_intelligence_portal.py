import streamlit as st
import pandas as pd
from document_intelligence import DocumentIntelligence
from document_processor import get_available_local_docs, process_single_file
from database import get_conflicts, add_conflict, get_documents

def document_intelligence_page():
    st.subheader("📄 Deep Document Intelligence & Institutional Knowledge")
    st.caption("Inspect auto-generated document intelligence cards, 1-click document decompositions, policy conflicts, and knowledge coverage gaps.")

    docs = get_available_local_docs()
    filenames = [d["filename"] for d in docs]

    tab_card, tab_explain, tab_conflicts, tab_gaps = st.tabs([
        "📇 Document Intelligence Card",
        "💡 Explain This Document",
        "⚔️ Knowledge Conflict Detector",
        "🔍 Knowledge Gap Analyzer"
    ])

    # TAB 1: INTELLIGENCE CARDS
    with tab_card:
        st.markdown("#### 📇 Structured Document Intelligence Summary")
        if filenames:
            sel_doc = st.selectbox("Select Enterprise Document:", filenames, key="card_sel")
            target_file = next((d for d in docs if d["filename"] == sel_doc), None)

            if target_file and st.button("Generate / Refresh Intelligence Card", key="gen_card_btn", type="primary"):
                with st.spinner("Analyzing document structure, entities, and risk factors..."):
                    raw_text = process_single_file(target_file["path"], target_file["filename"])
                    card_data = DocumentIntelligence.analyze_document(target_file["filename"], raw_text)
                    st.session_state.active_doc_card = card_data

            if "active_doc_card" in st.session_state and st.session_state.active_doc_card:
                card = st.session_state.active_doc_card
                st.write("")
                
                # Render Sleek Card
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Document Type", card["doc_type"])
                with c2:
                    st.metric("Governing Department", card["department"])
                with c3:
                    st.metric("Assessed Risk Level", card["risk_level"])

                st.write("")
                st.markdown("##### 👥 Identified Key Stakeholder Entities:")
                st.markdown(" • ".join([f"`{e}`" for e in card["entities"]]))

                st.write("")
                st.markdown("##### 🔢 Extracted Numerical Figures & Thresholds:")
                if card["key_numbers"]:
                    st.markdown(" • ".join([f"`{n}`" for n in card["key_numbers"]]))
                else:
                    st.caption("No specific monetary or threshold figures detected.")

                st.write("")
                st.markdown("##### ⚖️ Extracted Key Rules & Obligations:")
                for r in card["key_rules"]:
                    st.markdown(f"> *\"{r}\"*")
        else:
            st.info("No documents detected in repository.")

    # TAB 2: EXPLAIN THIS DOCUMENT
    with tab_explain:
        st.markdown("#### 💡 1-Click Document Decomposition")
        if filenames:
            exp_doc = st.selectbox("Select Document to Explain:", filenames, key="explain_sel")
            target_exp = next((d for d in docs if d["filename"] == exp_doc), None)

            if target_exp and st.button("⚡ Deconstruct & Explain Document", key="exp_btn", type="primary"):
                with st.spinner("Decomposing document into executive summary, TL;DR, and FAQs..."):
                    text = process_single_file(target_exp["path"], target_exp["filename"])
                    explained = DocumentIntelligence.explain_document(target_exp["filename"], text)
                    st.session_state.active_explained = explained

            if "active_explained" in st.session_state and st.session_state.active_explained:
                exp = st.session_state.active_explained
                st.write("")
                st.markdown(f"### 📌 Executive Brief: `{exp['filename']}`")
                
                st.info(f"**TL;DR:** {exp['tldr']}")

                st.markdown("##### 📋 Executive Summary:")
                st.markdown(exp['executive_summary'])

                st.markdown("##### ❓ Key Frequently Asked Questions (FAQs):")
                for f in exp['faqs']:
                    st.markdown(f"**Q: {f['q']}**")
                    st.markdown(f"A: {f['a']}")
                    st.write("")

                st.markdown("##### 🚀 Designated Action Items:")
                for act in exp['action_items']:
                    st.markdown(f"• {act}")
        else:
            st.info("No documents available.")

    # TAB 3: KNOWLEDGE CONFLICT DETECTOR
    with tab_conflicts:
        st.markdown("#### ⚔️ Policy & Knowledge Conflict Detector")
        st.caption("Automatically detects contradictory rules, limits, or dates across different documents.")

        conflicts = get_conflicts()
        if conflicts:
            for conf in conflicts:
                st.markdown(f"""
                    <div class="ai-card" style="margin-bottom: 14px; border-left: 4px solid #ef4444;">
                        <div style="font-weight: 700; color: #ef4444; font-size: 1rem;">
                            ⚠️ Conflict Topic: {conf['topic']} <span class="ai-badge badge-amber">{conf['severity']} Severity</span>
                        </div>
                        <p style="margin: 8px 0; color: #cbd5e1; font-size: 0.9rem;">{conf['description']}</p>
                        <div style="font-size: 0.8rem; color: #94a3b8;">
                            <b>Document A:</b> <code>{conf['doc_a']}</code> &nbsp;|&nbsp; <b>Document B:</b> <code>{conf['doc_b']}</code>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No contradictions detected across active repository documents.")

        with st.expander("➕ Log Discovered Policy Contradiction", expanded=False):
            c_topic = st.text_input("Conflict Subject")
            c_doc1 = st.text_input("Source Document 1")
            c_doc2 = st.text_input("Source Document 2")
            c_desc = st.text_area("Contradiction Details")
            if st.button("Record Conflict in Audit Registry"):
                if c_topic and c_desc:
                    add_conflict(c_topic, c_doc1, c_doc2, c_desc)
                    st.success("Recorded!")
                    st.rerun()

    # TAB 4: KNOWLEDGE GAP ANALYZER
    with tab_gaps:
        st.markdown("#### 🔍 Institutional Knowledge Gap Analyzer")
        st.caption("Evaluates organizational coverage against enterprise baseline standards.")

        gaps = DocumentIntelligence.detect_knowledge_gaps(filenames)
        if gaps:
            st.warning(f"Detected **{len(gaps)} Knowledge Gaps** in current corporate repository:")
            for g in gaps:
                st.markdown(f"""
                    <div class="ai-card" style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #6366f1;">Missing Domain: {g['topic']}</span>
                            <span class="ai-badge badge-amber">Impact: {g['impact']}</span>
                        </div>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin: 6px 0 0 0;">
                            <b>Recommendation:</b> {g['rec']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Comprehensive institutional coverage across baseline enterprise domains.")
