import streamlit as st

DEMO_STEPS = [
    {
        "step": 1,
        "title": "1. Ingest Enterprise Documents",
        "desc": "Index unstructured enterprise PDFs and policies into vector embeddings using sliding-window chunking.",
        "portal": "📚 Knowledge Vault",
        "action_text": "Jump to Knowledge Vault to inspect active documents and vector chunk allocations."
    },
    {
        "step": 2,
        "title": "2. Extract Document Intelligence Cards",
        "desc": "Auto-extract document type, governing department, key entities, numbers, and compliance risk levels.",
        "portal": "📄 Document Intelligence",
        "action_text": "View auto-generated Document Intelligence Cards and 1-click executive decompositions."
    },
    {
        "step": 3,
        "title": "3. Directed GraphRAG Semantic Network",
        "desc": "Explore typed semantic relationships (eligible_for, requires, governed_by) in an interactive 2D network.",
        "portal": "🕸️ Knowledge Graph",
        "action_text": "Trace multi-hop governance paths and query conceptual relationships."
    },
    {
        "step": 4,
        "title": "4. Multi-Agent Cognitive Copilot",
        "desc": "Dynamic intent classification routing queries to specialized Knowledge, Policy, or Task agents with grounded citations.",
        "portal": "💬 Cognitive Copilot",
        "action_text": "Ask questions across executive, technical, or compliance personas."
    },
    {
        "step": 5,
        "title": "5. Workplace Problem Solver",
        "desc": "Diagnose real operational roadblocks with probable root causes, step-by-step remediation, and support escalation.",
        "portal": "🛠️ AI Problem Solver",
        "action_text": "Test VPN troubleshooting or upload error screenshot for visual analysis."
    },
    {
        "step": 6,
        "title": "6. Detect Policy Conflicts & Knowledge Gaps",
        "desc": "Scan across multiple documents to identify contradicting rules, limits, dates, and uncovered topics.",
        "portal": "📄 Document Intelligence",
        "action_text": "Inspect the Conflict Detector tab and review benchmark knowledge gaps."
    },
    {
        "step": 7,
        "title": "7. Safe Text-to-SQL Enterprise Data Analyst",
        "desc": "Ask questions in plain English against structured operational and financial ledger tables with instant Plotly charts.",
        "portal": "📊 AI Data Analyst",
        "action_text": "Query cloud infrastructure spend or headcount metrics with AST/Regex safety guardrails."
    },
    {
        "step": 8,
        "title": "8. Decision Center & Multi-Criteria Tradeoff",
        "desc": "Evaluate strategic dilemmas with rigorous separation of FACT, INFERENCE, and RECOMMENDATION.",
        "portal": "🎯 Decision Center",
        "action_text": "Generate tradeoff matrix and queue high-impact decisions for human sign-off."
    },
    {
        "step": 9,
        "title": "9. Action Execution & Task Management",
        "desc": "Convert insights into tracked enterprise action items with priority tags, deadlines, and evidence links.",
        "portal": "🧠 My AI Assistant",
        "action_text": "Inspect My Work task queue and update task completion status."
    },
    {
        "step": 10,
        "title": "10. AI Guard Firewall & Cloud Sync",
        "desc": "Monitor prompt injection interceptions, inspect full audit trails, and synchronize records to Firebase Cloud Firestore.",
        "portal": "🛡️ Governance & Security",
        "action_text": "Inspect AI Security Guard threat table and dual-mode cloud synchronization."
    }
]

def demo_mode_page():
    st.subheader("🎬 Guided Product Showcase & Evaluator Tour")
    st.caption("Step-by-step interactive walkthrough demonstrating the complete 10-phase enterprise cognitive lifecycle.")

    if "demo_step_idx" not in st.session_state:
        st.session_state.demo_step_idx = 0

    step_idx = st.session_state.demo_step_idx
    curr_step = DEMO_STEPS[step_idx]

    # Progress Indicator
    prog_val = int((step_idx + 1) / len(DEMO_STEPS) * 100)
    st.progress(prog_val)
    st.caption(f"Showcase Milestone {step_idx + 1} of {len(DEMO_STEPS)} ({prog_val}%)")

    st.write("")

    # Card
    st.markdown(f"""
        <div class="ai-card" style="padding: 24px 30px; margin-bottom: 20px;">
            <div class="ai-badge badge-indigo" style="margin-bottom: 8px;">
                MILESTONE {curr_step['step']} OF 10
            </div>
            <h2 class="ai-title" style="font-size: 1.6rem; margin: 0 0 10px 0;">{curr_step['title']}</h2>
            <p class="ai-body" style="font-size: 1.02rem; margin-bottom: 16px;">{curr_step['desc']}</p>
            <div class="ai-callout">
                👉 <b>Live Showcase Portal:</b> <code>{curr_step['portal']}</code> — {curr_step['action_text']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Controls
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1.5, 1])
    with btn_col1:
        if st.button("⬅ Previous Milestone", disabled=(step_idx == 0), use_container_width=True):
            st.session_state.demo_step_idx -= 1
            st.rerun()
    with btn_col2:
        if st.button(f"🚀 Jump to {curr_step['portal']}", type="primary", use_container_width=True):
            st.session_state.current_portal = curr_step['portal']
            st.rerun()
    with btn_col3:
        if st.button("Next Milestone ➡", disabled=(step_idx == len(DEMO_STEPS) - 1), use_container_width=True):
            st.session_state.demo_step_idx += 1
            st.rerun()

    st.divider()

    st.markdown("##### 📌 Complete 10-Phase Lifecycle Quick Index:")
    idx_cols = st.columns(5)
    for i, s in enumerate(DEMO_STEPS[:5]):
        with idx_cols[i]:
            if st.button(f"Step {s['step']}", key=f"quick_step_{i}", use_container_width=True):
                st.session_state.demo_step_idx = i
                st.rerun()

    idx_cols2 = st.columns(5)
    for i, s in enumerate(DEMO_STEPS[5:], 5):
        with idx_cols2[i - 5]:
            if st.button(f"Step {s['step']}", key=f"quick_step_{i}", use_container_width=True):
                st.session_state.demo_step_idx = i
                st.rerun()
