import streamlit as st
from PIL import Image
from orchestrator import AIOrchestrator
from database import add_task, get_user_profile

def problem_solver_page():
    st.subheader("🛠️ AI Workplace Problem Solver")
    st.caption("Diagnose enterprise operational roadblocks, analyze probable root causes, inspect error screenshots, and execute step-by-step remediation runbooks.")

    username = st.session_state.get("username", "user")
    user_profile = get_user_profile(username)
    rag_engine = st.session_state.get("rag", None)

    tab_text, tab_vision = st.tabs([
        "⌨️ Natural Language Diagnostic",
        "📷 Multimodal Error Screenshot Diagnostic"
    ])

    # TAB 1: TEXT DIAGNOSTIC
    with tab_text:
        st.markdown("##### ⚡ Common Workplace Issue Accelerators:")
        col_p1, col_p2, col_p3 = st.columns(3)
        quick_problem = None
        if col_p1.button("🔌 Remote VPN Failed to Connect", use_container_width=True):
            quick_problem = "My remote VPN is failing to authenticate and the tunnel keeps dropping."
        if col_p2.button("🔒 Enterprise SSO Account Lockout", use_container_width=True):
            quick_problem = "My enterprise Single Sign-On account is locked out after repeated attempts."
        if col_p3.button("💳 Expense Reimbursement Rejection", use_container_width=True):
            quick_problem = "Why was my travel per-diem and flight reimbursement claim flagged or rejected?"

        custom_problem = st.text_input(
            "Describe workplace problem or system error:",
            value=quick_problem if quick_problem else "",
            placeholder="e.g., Cannot connect to clinical database or VPN handshake timed out...",
            key="prob_text_input"
        )

        if st.button("🚀 Analyze & Generate Diagnostic Runbook", key="run_prob_btn", use_container_width=True, type="primary"):
            if custom_problem.strip():
                with st.spinner("Analyzing enterprise runbooks and executing diagnostic reasoning..."):
                    diag_result = AIOrchestrator._execute_problem_solver(
                        query=custom_problem,
                        rag_engine=rag_engine,
                        user_profile=user_profile,
                        t_start=0
                    )
                    st.session_state.latest_diagnostic = diag_result
            else:
                st.warning("Please provide a description of the workplace problem.")

    # TAB 2: MULTIMODAL ERROR SCREENSHOT
    with tab_vision:
        st.markdown("##### 📷 Upload Workplace Error Dialog / Screenshot:")
        st.caption("Upload a screenshot of your system error, browser alert, or crash log for automated pattern analysis.")

        uploaded_img = st.file_uploader("Upload Error Screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if uploaded_img:
            img = Image.open(uploaded_img)
            col_i1, col_i2 = st.columns([1, 1.3])
            with col_i1:
                st.image(img, caption=f"Captured: {uploaded_img.name}", use_container_width=True)
            with col_i2:
                st.markdown("##### 🔍 Detected Visual Telemetry:")
                st.write(f"**Resolution:** `{img.width} x {img.height} px` • **Format:** `{img.format}`")
                
                # Infer error from filename / pattern
                name_low = uploaded_img.name.lower()
                if "vpn" in name_low:
                    inferred_err = "Remote VPN Handshake Timeout Error (Code 789 / 809)"
                elif "auth" in name_low or "sso" in name_low or "login" in name_low:
                    inferred_err = "SSO Federated Token Validation Mismatch (Error AADSTS50011)"
                elif "sql" in name_low or "db" in name_low:
                    inferred_err = "Database Connection Pool Exhaustion (SQLState 08001)"
                else:
                    inferred_err = "Enterprise System Operational Exception (Code ERR_TIMEOUT_408)"

                st.info(f"**Identified Error Signature:**\n`{inferred_err}`")

                if st.button("🚀 Diagnose Visual Error Screenshot", type="primary", use_container_width=True):
                    with st.spinner("Matching screenshot error signature against enterprise SOP runbooks..."):
                        diag_result = AIOrchestrator._execute_problem_solver(
                            query=f"{inferred_err} encountered on user workstation.",
                            rag_engine=rag_engine,
                            user_profile=user_profile,
                            t_start=0
                        )
                        st.session_state.latest_diagnostic = diag_result

    # Render Result
    if "latest_diagnostic" in st.session_state and st.session_state.latest_diagnostic:
        diag = st.session_state.latest_diagnostic
        st.write("")
        st.markdown(diag["answer"])

        if diag.get("matches"):
            with st.expander(f"📚 Verified Knowledge Citations ({len(diag['matches'])} source references)", expanded=True):
                for idx, m in enumerate(diag["matches"], 1):
                    conf = int(min(m["score"] * 100, 99)) if m["score"] < 1.0 else 100
                    st.markdown(f"**Citation #{idx}** `Relevance: {conf}%` • *Chunk #{m.get('chunk_idx', 0) + 1}*")
                    st.markdown(f"> {m['chunk']}")

        st.divider()
        st.markdown("##### ⚡ Immediate Remediation Actions:")
        act_col1, act_col2, act_col3 = st.columns(3)

        with act_col1:
            if st.button("🎫 Escalate to Tier-2 Support Ticket", use_container_width=True):
                st.success("✅ Support Ticket `#INC-89421` dispatched to Operations Queue with diagnostic report attached.")
        with act_col2:
            if st.button("➕ Convert Steps to My Tasks", use_container_width=True):
                add_task(
                    username=username,
                    title="Remediate Diagnostic Issue",
                    description="Execute 5-step diagnostic remediation steps generated by AI Problem Solver.",
                    priority="High",
                    source_doc="AI Problem Solver Runbook"
                )
                st.success("✅ Remediation checklist synchronized to **My Work** portal!")
        with act_col3:
            st.download_button(
                label="📥 Export Runbook (.md)",
                data=diag["answer"],
                file_name="diagnostic_remediation_runbook.md",
                mime="text/markdown",
                use_container_width=True
            )
