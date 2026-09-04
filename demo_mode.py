import streamlit as st
import pandas as pd
import plotly.express as px
from orchestrator import AIOrchestrator
from database import get_user_profile, add_task
from voice_assistant import render_audio_narration

DEMO_STEPS = [
    {
        "step": 1,
        "title": "1. Ingest Multi-Format Enterprise Documents",
        "desc": "Index unstructured enterprise PDFs, Microsoft Word (.docx), Excel spreadsheets (.xlsx), and CSV tables into dense semantic vector chunks.",
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
        "title": "4. Multi-Agent Cognitive Copilot & Voice",
        "desc": "Dynamic intent classification routing queries to specialized Knowledge, Policy, or Task agents with voice dictation & speech narration.",
        "portal": "💬 Cognitive Copilot",
        "action_text": "Ask questions across executive, technical, or compliance personas with audio playback."
    },
    {
        "step": 5,
        "title": "5. Workplace Problem Solver & Visual Diagnostics",
        "desc": "Diagnose operational roadblocks with probable root causes, multimodal error screenshot telemetry, and audio runbooks.",
        "portal": "🛠️ AI Problem Solver",
        "action_text": "Test VPN troubleshooting or upload error screenshot for visual analysis."
    },
    {
        "step": 6,
        "title": "6. Detect Policy Conflicts & Knowledge Gaps",
        "desc": "Scan across multiple documents to identify contradicting rules, limits, dates, and uncovered institutional topics.",
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
        "title": "9. Action Execution & Personal Task Hub",
        "desc": "Convert insights into tracked enterprise action items with priority tags, deadlines, and evidence links.",
        "portal": "🧠 My AI Assistant",
        "action_text": "Inspect My Work task queue and update task completion status."
    },
    {
        "step": 10,
        "title": "10. AI Guard Firewall & Cloud Sync",
        "desc": "Monitor prompt injection interceptions, inspect full audit trails, and synchronize records to Firebase Cloud Firestore.",
        "portal": "🛡️ Governance & Security",
        "action_text": "Inspect AI Security Guard threat table, observability traces, and dual-mode cloud sync."
    }
]

def demo_mode_page():
    st.subheader("🎬 Enterprise Presentation & Evaluator Showcase Suite")
    st.caption("Demonstrate the complete 10-phase enterprise cognitive lifecycle and test 6 real-world persona scenarios.")

    tab_lifecycle, tab_scenarios = st.tabs([
        "🚀 10-Phase Cognitive Lifecycle Showcase",
        "👥 6 Real-World Persona Scenarios"
    ])

    # TAB 1: 10-PHASE COGNITIVE LIFECYCLE
    with tab_lifecycle:
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

    # TAB 2: 6 REAL-WORLD PERSONA SCENARIOS
    with tab_scenarios:
        st.markdown("#### 👥 Real-World Enterprise Persona Demonstrations")
        st.caption("Click '▶️ Run Scenario Live' to execute each scenario through the full cognitive lifecycle: Understand → Retrieve → Reason → Decide → Act.")

        scenarios = [
            {
                "id": "sc_onboarding",
                "badge": "badge-indigo",
                "role": "New Employee",
                "title": "Scenario 1: Engineering Onboarding & Remote Work Policy",
                "query": "I am a new engineer joining this week. What are my mandatory onboarding deadlines, equipment allowances, and leave entitlements?",
                "subsystem": "HR Policies & Remote Work Guidelines",
                "expected_agent": "Policy & Compliance Agent"
            },
            {
                "id": "sc_vpn",
                "badge": "badge-amber",
                "role": "Remote Specialist",
                "title": "Scenario 2: Workplace IT Problem — VPN Handshake Error 809",
                "query": "My remote VPN is failing to connect and keeps dropping with handshake error 809.",
                "subsystem": "Perimeter Network / IPSec TAP Adapter",
                "expected_agent": "Problem Solver Agent"
            },
            {
                "id": "sc_finance",
                "badge": "badge-active",
                "role": "Finance Manager",
                "title": "Scenario 3: Expense Reimbursement Audit & Cap Compliance",
                "query": "Why was the travel reimbursement claim for flight and per-diem flagged during audit?",
                "subsystem": "Corporate Expense & Finance Governance",
                "expected_agent": "Policy & Compliance Agent"
            },
            {
                "id": "sc_conflict",
                "badge": "badge-danger",
                "role": "Compliance Officer",
                "title": "Scenario 4: Cross-Document Conflict & Regulation Exposure",
                "query": "Do our corporate records retention guidelines contradict the regulatory compliance mandate in Saveetha norms?",
                "subsystem": "Legal, Risk & Regulatory Compliance",
                "expected_agent": "Document Intelligence Agent"
            },
            {
                "id": "sc_data",
                "badge": "badge-purple",
                "role": "Financial Analyst",
                "title": "Scenario 5: Text-to-SQL Cloud Infrastructure Spend Breakdown",
                "query": "Show quarterly cloud infrastructure compute spend by department.",
                "subsystem": "Structured Operational Ledger",
                "expected_agent": "Data Analyst Agent"
            },
            {
                "id": "sc_executive",
                "badge": "badge-indigo",
                "role": "Executive Leadership",
                "title": "Scenario 6: Executive Risk Synthesis & Strategic Tradeoff",
                "query": "Provide an executive briefing on organizational data sovereignty, cloud synchronization status, and pending operational risks.",
                "subsystem": "Enterprise Strategic Intelligence",
                "expected_agent": "Executive Knowledge Agent"
            }
        ]

        username = st.session_state.get("username", "admin")
        profile = get_user_profile(username)
        rag_engine = st.session_state.get("rag", None)

        for sc in scenarios:
            with st.container(border=True):
                s_col1, s_col2 = st.columns([3, 1])
                with s_col1:
                    st.markdown(f'<span class="ai-badge {sc["badge"]}">{sc["role"]}</span> &nbsp; **{sc["title"]}**', unsafe_allow_html=True)
                    st.caption(f"Inquiry: *\"{sc['query']}\"* • Target Subsystem: `{sc['subsystem']}`")
                with s_col2:
                    run_btn = st.button("▶️ Run Scenario Live", key=f"btn_{sc['id']}", use_container_width=True, type="primary")

                if run_btn:
                    with st.spinner(f"Executing cognitive lifecycle for {sc['role']}..."):
                        res = AIOrchestrator.dispatch(
                            query=sc["query"],
                            user_profile=profile,
                            rag_engine=rag_engine,
                            persona="Executive"
                        )

                        st.write("")
                        st.markdown("##### 🧠 Cognitive Lifecycle Execution Trace:")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("1. Classified Intent", res.get("intent", "KNOWLEDGE_QA"))
                        m2.metric("2. Dispatched Agent", res.get("agent_name", "AI Agent"))
                        m3.metric("3. Retrieved Chunks", f"{len(res.get('matches', []))} Chunks")
                        m4.metric("4. Latency", f"{res.get('latency_ms', 2.4)} ms")

                        st.markdown("##### 📋 Reasoned Enterprise Response:")
                        render_audio_narration(res["answer"], label="🔊 Listen to Executive Briefing", key=f"tts_{sc['id']}")
                        st.markdown(res["answer"])

                        # Render structured chart if present
                        if res.get("structured_data") is not None and not res["structured_data"].empty:
                            df = res["structured_data"]
                            if "department" in df.columns and "total_amount" in df.columns:
                                fig = px.bar(df, x="department", y="total_amount", color="category", barmode="group", title="Spend Breakdown by Department")
                                st.plotly_chart(fig, use_container_width=True)

                        # Action step
                        st.write("")
                        a1, a2 = st.columns([2, 1])
                        with a1:
                            st.info("✅ **Cognitive Action Phase**: Automated insights can be converted into tracked enterprise work items.")
                        with a2:
                            if st.button("➕ Convert to Task in My Work", key=f"task_sc_{sc['id']}", use_container_width=True):
                                add_task(username, title=f"Action: {sc['role']} Inquiry", description=res['answer'][:120], priority="High", source_doc=sc['title'])
                                st.success("Task synchronized to My Work portal!")
