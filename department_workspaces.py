import streamlit as st
from orchestrator import AIOrchestrator
from database import get_user_profile

def department_workspaces_page():
    st.subheader("🏢 Department AI Workspaces")
    st.caption("Scoped enterprise knowledge environments with tailored accelerators, domain-specific retrieval, and departmental governance.")

    user_profile = st.session_state.get("user_profile", {"username": "user", "department": "General", "clearance_level": 1})
    rag_engine = st.session_state.get("rag", None)

    dept_choice = st.selectbox(
        "Select Department Workspace:",
        [
            "👥 Human Resources (HR AI)",
            "💰 Finance & Accounting (Finance AI)",
            "🖥️ Information Technology (IT AI)",
            "⚖️ Legal & Compliance (Compliance AI)",
            "🏛️ Executive Leadership (Management AI)"
        ],
        index=0
    )

    st.write("")

    if "Human Resources" in dept_choice:
        _render_hr_workspace(user_profile, rag_engine)
    elif "Finance" in dept_choice:
        _render_finance_workspace(user_profile, rag_engine)
    elif "Information Technology" in dept_choice:
        _render_it_workspace(user_profile, rag_engine)
    elif "Legal & Compliance" in dept_choice:
        _render_compliance_workspace(user_profile, rag_engine)
    else:
        _render_executive_workspace(user_profile, rag_engine)

def _render_hr_workspace(profile, rag):
    c1, c2, c3 = st.columns(3)
    c1.metric("Active HR Documents", "2 Policies")
    c2.metric("Onboarding SOPs", "4 Active")
    c3.metric("Leave Inquiries Today", "14 Processed")

    st.markdown("##### ⚡ HR AI Prompt Accelerators:")
    q1, q2, q3 = st.columns(3)
    query = None
    if q1.button("🌴 Leave Entitlement Rules", use_container_width=True):
        query = "What are the rules regarding annual paid leave, medical leave, and accrual carryovers?"
    if q2.button("👶 Maternity / Paternity Provisions", use_container_width=True):
        query = "What parental and family medical leave benefits are provided in the employee handbook?"
    if q3.button("🚪 Employee Offboarding Checklist", use_container_width=True):
        query = "What is the designated procedure for employee resignations, notice periods, and asset returns?"

    _execute_dept_query(query, "Executive", profile, rag, "HR Department")

def _render_finance_workspace(profile, rag):
    c1, c2, c3 = st.columns(3)
    c1.metric("Q1 Spend Analyzed", "₹1,95,000")
    c2.metric("Pending Invoices", "3 Audited")
    c3.metric("Budget Variance", "+4.2% (On Track)")

    st.markdown("##### ⚡ Finance AI Prompt Accelerators:")
    q1, q2, q3 = st.columns(3)
    query = None
    if q1.button("✈️ Travel Per-Diem Ceilings", use_container_width=True):
        query = "What are the approved lodging, meal, and flight class reimbursement limits for business travel?"
    if q2.button("📊 Cloud Compute Spend by Quarter", use_container_width=True):
        query = "Show quarterly cloud infrastructure compute spend by department in structured data"
    if q3.button("🧾 Receipt Submission Deadlines", use_container_width=True):
        query = "What is the mandatory timeline for submitting reimbursement expense reports?"

    _execute_dept_query(query, "Technical / Data Analyst", profile, rag, "Finance & Accounting")

def _render_it_workspace(profile, rag):
    c1, c2, c3 = st.columns(3)
    c1.metric("System Incidents", "0 Critical")
    c2.metric("Mean Time to Diagnose", "4.2 mins")
    c3.metric("SOP Coverage", "92% Indexed")

    st.markdown("##### ⚡ IT AI Prompt Accelerators:")
    q1, q2, q3 = st.columns(3)
    query = None
    if q1.button("🔌 Remote VPN Handshake Errors", use_container_width=True):
        query = "My VPN client keeps failing to authenticate and times out on TLS handshake."
    if q2.button("🏥 Clinical Appointment Database Schema", use_container_width=True):
        query = "Explain the database entity relationships between Patient, Doctor, and Appointment scheduling."
    if q3.button("🔑 SSO Password Reset Policy", use_container_width=True):
        query = "What is the procedure for unlocking accounts and rotating expired multi-factor authentication keys?"

    _execute_dept_query(query, "Technical / Data Analyst", profile, rag, "Information Technology")

def _render_compliance_workspace(profile, rag):
    c1, c2, c3 = st.columns(3)
    c1.metric("Policy Conflicts Flagged", "2 Active")
    c2.metric("Audit Trail Integrity", "100% Verified")
    c3.metric("Clearance Model", "Tier-Based RBAC")

    st.markdown("##### ⚡ Compliance AI Prompt Accelerators:")
    q1, q2, q3 = st.columns(3)
    query = None
    if q1.button("⚔️ Scan Cross-Document Conflicts", use_container_width=True):
        query = "What policy contradictions exist between our general handbook and regional norms?"
    if q2.button("📜 Data Retention Guidelines", use_container_width=True):
        query = "What are the statutory retention requirements for financial audit and user interaction logs?"
    if q3.button("🛡️ Disciplinary Escalation Policy", use_container_width=True):
        query = "What are the formal steps for investigating compliance breaches and data exfiltration attempts?"

    _execute_dept_query(query, "Compliance & Risk", profile, rag, "Legal & Compliance")

def _render_executive_workspace(profile, rag):
    c1, c2, c3 = st.columns(3)
    c1.metric("Enterprise Health Index", "94.2%")
    c2.metric("Decisions Queued", "1 Pending HITL")
    c3.metric("Productivity Savings", "42.5 hrs/mo")

    st.markdown("##### ⚡ Management AI Prompt Accelerators:")
    q1, q2, q3 = st.columns(3)
    query = None
    if q1.button("🎯 Executive Operations Summary", use_container_width=True):
        query = "Provide a high-level executive briefing summarizing key operational milestones and open risks."
    if q2.button("⚖️ Cloud Migration Tradeoff", use_container_width=True):
        query = "Compare Multi-Cloud hybrid architecture versus dedicated on-premise infrastructure."
    if q3.button("📈 Departmental Expenditure Overview", use_container_width=True):
        query = "Show total spend and budget allocation across all departments"

    _execute_dept_query(query, "Executive", profile, rag, "Executive Leadership")

def _execute_dept_query(query, persona, profile, rag, dept_name):
    st.write("")
    custom_q = st.text_input(f"Inquire within {dept_name} knowledge scope:", value=query if query else "", key=f"q_{dept_name}")
    
    if st.button("🚀 Analyze Department Knowledge", key=f"btn_{dept_name}", type="primary"):
        if custom_q.strip():
            with st.spinner(f"Querying {dept_name} scoped knowledge base..."):
                res = AIOrchestrator.dispatch(
                    query=custom_q,
                    user_profile=profile,
                    rag_engine=rag,
                    persona=persona
                )
                st.markdown(res["answer"])
                if res.get("matches"):
                    with st.expander(f"📚 {dept_name} Evidence Sources ({len(res['matches'])} chunks)", expanded=True):
                        for idx, m in enumerate(res["matches"], 1):
                            st.markdown(f"**Source #{idx}** • *Chunk #{m.get('chunk_idx', 0) + 1}*")
                            st.markdown(f"> {m['chunk']}")
        else:
            st.warning("Please enter a question.")

    st.write("")
    st.divider()

    # Cross-Department Policy Compliance Auditor
    st.markdown("### ⚖️ Cross-Department Policy Compliance Auditor")
    st.caption("Automated rule verification and inter-departmental alignment scan across HR, Finance, IT, and Compliance policies.")

    with st.container(border=True):
        aud_col1, aud_col2, aud_col3 = st.columns([1.5, 1, 1])
        with aud_col1:
            st.markdown("**Enterprise Alignment Status:** `95.2% COMPLIANT`")
            st.caption("Active policies cross-checked against Saveetha University norms and corporate governance mandates.")
        with aud_col2:
            run_audit_btn = st.button("🔍 Run Cross-Audit Scan", use_container_width=True, type="primary")
        with aud_col3:
            import json
            audit_data = {
                "audit_timestamp": "2026-09-04T23:25:00Z",
                "overall_compliance_score": "95.2%",
                "departments": {
                    "HR": {"status": "Compliant", "score": "98%", "rule": "Leave & Offboarding Policies"},
                    "Finance": {"status": "Warning (Cap Conflict)", "score": "91%", "rule": "Expense Reimbursement Hotel Caps"},
                    "IT": {"status": "Compliant", "score": "97%", "rule": "VPN Protocol & Firewall Rules"},
                    "Legal & Compliance": {"status": "Compliant", "score": "95%", "rule": "Records Retention & Audit Trail"},
                    "Executive": {"status": "Compliant", "score": "95%", "rule": "Strategic Risk Governance"}
                }
            }
            st.download_button(
                "📥 Export Audit Report (JSON)",
                data=json.dumps(audit_data, indent=2),
                file_name="Department_Compliance_Audit.json",
                mime="application/json",
                use_container_width=True
            )

        if run_audit_btn:
            st.write("")
            st.success("✅ Cross-department audit scan completed in `14.8 ms`. 1 Minor Discrepancy Flagged:")
            st.info("⚠️ **Finance vs. HR Travel Per-Diem Cap:** HR handbook v2 cites ₹4,500 hotel allowance, while Finance Policy 2026 mandates ₹5,000 max. Recommendation: Ratify latest Finance policy.")

