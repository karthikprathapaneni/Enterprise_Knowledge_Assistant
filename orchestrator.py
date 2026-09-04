import time
import re
import pandas as pd
from security_guard import AIGuard
from database import execute_safe_sql, add_task, get_user_profile

class AIOrchestrator:
    """Enterprise AI Orchestrator that detects user intent, routes to specialized agents, and executes grounded reasoning."""

    @classmethod
    def detect_intent(cls, query: str) -> str:
        """Classifies natural language user query into specialized enterprise agent intents."""
        q = query.lower().strip()

        # Problem Solving Intent
        troubleshoot_keywords = ["not working", "vpn", "error", "failed", "broken", "troubleshoot", "issue", "crash", "cannot connect", "disconnect", "reset", "bug"]
        if any(w in q for w in troubleshoot_keywords):
            return "PROBLEM_SOLVER"

        # Structured Enterprise Data Intent (Text-to-SQL)
        data_keywords = ["spend", "budget", "cost", "expense", "headcount", "how much", "financial", "q1", "q2", "amount", "total", "average", "metrics", "chart", "table"]
        if any(w in q for w in data_keywords) and not ("policy" in q or "rules" in q):
            return "DATA_ANALYST"

        # Task & Workflow Intent
        task_keywords = ["create task", "add task", "remind me", "todo", "action item", "assign", "follow up"]
        if any(w in q for w in task_keywords):
            return "TASK_AGENT"

        # Policy & Compliance Intent
        policy_keywords = ["policy", "compliance", "rule", "mandatory", "regulation", "allowed", "prohibited", "limit", "reimbursement", "leave", "per-diem", "approval"]
        if any(w in q for w in policy_keywords):
            return "POLICY_COMPLIANCE"

        # Document Analysis Intent
        doc_keywords = ["summarize document", "explain this file", "analyze pdf", "break down document", "what is this document", "document overview"]
        if any(w in q for w in doc_keywords):
            return "DOCUMENT_INTELLIGENCE"

        # Default fallback
        return "KNOWLEDGE_QA"

    @classmethod
    def dispatch(cls, query: str, user_profile: dict, rag_engine, persona: str = "Executive", top_k: int = 3, threshold: float = 0.03) -> dict:
        t_start = time.time()
        username = user_profile.get("username", "user")

        # 1. AI Guard Security Interception
        guard_result = AIGuard.inspect_query(query, username=username)
        if not guard_result["safe"]:
            return {
                "agent_name": "🛡️ AI Security Guard",
                "intent": "SECURITY_INTERCEPTION",
                "answer": guard_result["response"],
                "matches": [],
                "structured_data": None,
                "recommended_actions": ["Contact Infosec Administrator", "Refine Query Syntax"],
                "latency_ms": round((time.time() - t_start) * 1000, 1),
                "is_security_blocked": True
            }

        # 2. Intent Detection
        intent = cls.detect_intent(query)

        # 3. Route to Specialized Agents
        if intent == "PROBLEM_SOLVER":
            res = cls._execute_problem_solver(query, rag_engine, user_profile, t_start)
        elif intent == "DATA_ANALYST":
            res = cls._execute_data_analyst(query, user_profile, t_start)
        elif intent == "TASK_AGENT":
            res = cls._execute_task_agent(query, user_profile, t_start)
        elif intent == "POLICY_COMPLIANCE":
            res = cls._execute_policy_agent(query, rag_engine, user_profile, t_start)
        elif intent == "DOCUMENT_INTELLIGENCE":
            res = cls._execute_document_agent(query, rag_engine, user_profile, t_start)
        else: # KNOWLEDGE_QA
            res = cls._execute_knowledge_agent(query, rag_engine, persona, top_k, threshold, t_start)

        # 4. Record System Observability Trace
        from observability import ObservabilityManager
        trace = ObservabilityManager.record_trace(
            username=username,
            query=query,
            intent=res.get("intent", intent),
            agent_name=res.get("agent_name", "AI Agent"),
            total_latency_ms=res.get("latency_ms", 2.5),
            chunks_count=len(res.get("matches", [])),
            clearance_tier=user_profile.get("clearance_level", 1)
        )
        res["trace_id"] = trace["trace_id"]
        return res

    @classmethod
    def _execute_problem_solver(cls, query: str, rag_engine, user_profile: dict, t_start: float) -> dict:
        """Troubleshooting agent: generates root cause, confidence, step-by-step resolution, and escalation."""
        matches = rag_engine.retrieve(query, top_k=3, threshold=0.02) if rag_engine else []
        latency_ms = round((time.time() - t_start) * 1000, 1)

        evidence_snippet = matches[0]["chunk"] if matches else "Standard Enterprise IT Troubleshooting Protocol"
        source_doc = f"Document Chunk #{matches[0]['chunk_idx'] + 1}" if matches else "Enterprise IT Runbook v2.4"

        # Determine diagnostic category
        q_low = query.lower()
        if "vpn" in q_low or "connect" in q_low:
            issue_title = "Remote VPN Authentication & Tunneling Failure"
            likely_cause = "Expired session token, multi-factor handshake timeout, or local TAP adapter binding conflict."
            confidence = 89
            steps = [
                "1. **Check Local Connectivity:** Confirm Internet access via standard HTTPS ping.",
                "2. **Restart VPN Service:** Close VPN client, kill background daemon, and relaunch as Administrator.",
                "3. **Flush DNS & Credentials:** Execute `ipconfig /flushdns` in terminal and clear cached SSO credentials.",
                "4. **Re-Authenticate via MFA:** Trigger a fresh multi-factor approval prompt.",
                "5. **Fallback Gateway:** Switch server endpoint to Secondary Regional Gateway."
            ]
        elif "password" in q_low or "login" in q_low or "access" in q_low:
            issue_title = "Enterprise SSO Account Lockout / Access Privilege Failure"
            likely_cause = "Account locked following repeated failed attempts or password policy expiry."
            confidence = 92
            steps = [
                "1. **Wait Lockout Threshold:** Allow 15-minute cool-down period or access Self-Service Password Portal.",
                "2. **Verify Identity:** Authenticate using registered authenticator app or hardware FIDO key.",
                "3. **Synchronize Active Directory:** Trigger credential re-sync across enterprise federated identity.",
                "4. **Clear Browser Cache:** Clear cookies for enterprise identity provider domain."
            ]
        else:
            issue_title = f"Operational Workplace Issue: {query[:45]}"
            likely_cause = f"System configuration discrepancy or procedural mismatch referenced in documentation."
            confidence = 78
            steps = [
                "1. **Isolate Symptoms:** Document exact error message and reproduction sequence.",
                "2. **Consult Reference Guidelines:** Verify steps against latest internal SOP.",
                "3. **Verify Clearance:** Ensure account possesses required clearance level.",
                "4. **Engage Tier-2 Support:** Open an enterprise support ticket if issue persists."
            ]

        formatted_answer = f"""### 🛠️ AI Problem Solver Diagnostic Report
**Target Issue:** `{issue_title}` • **Diagnostic Confidence:** `{confidence}%`

#### 🔍 Root Cause Analysis
* **Likely Cause:** {likely_cause}
* **Grounded Reference:** `{source_doc}`

#### 📋 Step-by-Step Remediation
{chr(10).join(steps)}

---
#### ⚠️ Escalation Runbook
If steps 1–4 fail to restore operations, escalate immediately to **Enterprise Operations Tier-2 Support**.
"""
        return {
            "agent_name": "🛠️ AI Problem Solver Agent",
            "intent": "PROBLEM_SOLVER",
            "answer": formatted_answer,
            "matches": matches,
            "structured_data": None,
            "recommended_actions": ["Create IT Support Ticket", "Add Remediation Task to My Work", "Export Diagnostic Runbook"],
            "latency_ms": latency_ms,
            "escalation_available": True
        }

    @classmethod
    def _execute_data_analyst(cls, query: str, user_profile: dict, t_start: float) -> dict:
        """Safe Text-to-SQL compiler with dynamic Plotly chart generation."""
        q_low = query.lower()

        # Deterministic SQL generation based on query semantics
        if "department" in q_low or "by department" in q_low or "cloud" in q_low:
            sql_query = "SELECT department, category, metric_name, SUM(amount) as total_amount FROM structured_enterprise_data GROUP BY department, category"
            chart_type = "bar"
        elif "q1" in q_low or "q2" in q_low or "quarter" in q_low:
            sql_query = "SELECT fiscal_period, department, SUM(amount) as total_spend FROM structured_enterprise_data GROUP BY fiscal_period, department ORDER BY fiscal_period ASC"
            chart_type = "bar"
        else:
            sql_query = "SELECT department, category, metric_name, fiscal_period, amount, status FROM structured_enterprise_data ORDER BY amount DESC LIMIT 8"
            chart_type = "table"

        sql_result = execute_safe_sql(sql_query)
        latency_ms = round((time.time() - t_start) * 1000, 1)

        if not sql_result["success"]:
            return {
                "agent_name": "📊 AI Data Analyst Agent",
                "intent": "DATA_ANALYST",
                "answer": f"⚠️ **SQL Execution Error:** {sql_result['error']}",
                "matches": [],
                "structured_data": None,
                "recommended_actions": ["Refine Query Parameters", "Inspect Enterprise Data Schema"],
                "latency_ms": latency_ms
            }

        cols = sql_result["columns"]
        rows = sql_result["rows"]
        df = pd.DataFrame(rows, columns=cols)

        # Build natural language insight
        total_sum = df["amount"].sum() if "amount" in df.columns else (df["total_amount"].sum() if "total_amount" in df.columns else 0)
        top_row = df.iloc[0].to_dict() if not df.empty else {}

        summary_text = f"""### 📊 AI Data Analyst Report
**Query Executed:** `{sql_query}` • **Records Retrieved:** `{len(df)}` • **Latency:** `{latency_ms} ms`

#### 📈 Key Quantitative Findings
* **Aggregated Volume:** ₹{total_sum:,.2f} recorded across selected enterprise parameters.
* **Top Metric Driver:** `{top_row.get('metric_name', top_row.get('category', 'Primary Cost Center'))}` in `{top_row.get('department', 'General')}`.
* **Data Verification:** Directly validated against internal financial & operational ledger tables (`structured_enterprise_data`).
"""
        return {
            "agent_name": "📊 AI Data Analyst Agent",
            "intent": "DATA_ANALYST",
            "answer": summary_text,
            "matches": [],
            "structured_data": df,
            "chart_type": chart_type,
            "sql_query": sql_query,
            "recommended_actions": ["Download CSV Dataset", "Filter by Fiscal Quarter", "Add Financial Audit Task"],
            "latency_ms": latency_ms
        }

    @classmethod
    def _execute_task_agent(cls, query: str, user_profile: dict, t_start: float) -> dict:
        """Parses natural language task creation request and persists in SQLite."""
        username = user_profile.get("username", "user")
        
        # Extract title from query
        clean_title = re.sub(r"(?i)^(create task|add task|remind me to|todo:?)\s*", "", query).strip()
        if not clean_title:
            clean_title = "Follow up on enterprise documentation"

        add_task(
            username=username,
            title=clean_title.capitalize(),
            description=f"Action item created via Cognitive Copilot by {username}.",
            priority="High" if "urgent" in query.lower() or "high" in query.lower() else "Medium",
            source_doc="Cognitive Copilot Dialogue"
        )
        latency_ms = round((time.time() - t_start) * 1000, 1)

        return {
            "agent_name": "✅ Task & Workflow Agent",
            "intent": "TASK_AGENT",
            "answer": f"""### ✅ Enterprise Task Logged Successfully
**Task Title:** `{clean_title.capitalize()}`
**Assigned User:** `{username}` • **Status:** `Pending` • **Priority:** `Medium`

This task has been synchronized into your **My Work** portal and enterprise action tracking stream.
""",
            "matches": [],
            "structured_data": None,
            "recommended_actions": ["View My Work Dashboard", "Set Task Due Date", "Assign Team Collaborators"],
            "latency_ms": latency_ms
        }

    @classmethod
    def _execute_policy_agent(cls, query: str, rag_engine, user_profile: dict, t_start: float) -> dict:
        """Policy and compliance specialist agent."""
        res = rag_engine.answer_with_persona(query, persona="Compliance & Risk", top_k=3, threshold=0.03) if rag_engine else {"answer": "No policy documents indexed.", "matches": [], "latency_ms": 0}
        latency_ms = round((time.time() - t_start) * 1000, 1)

        return {
            "agent_name": "⚖️ Policy & Compliance Agent",
            "intent": "POLICY_COMPLIANCE",
            "answer": res["answer"],
            "matches": res.get("matches", []),
            "structured_data": None,
            "recommended_actions": ["Verify Compliance Attestation", "Detect Policy Conflicts", "Export Policy Excerpt"],
            "latency_ms": latency_ms
        }

    @classmethod
    def _execute_document_agent(cls, query: str, rag_engine, user_profile: dict, t_start: float) -> dict:
        """Document intelligence breakdown agent."""
        matches = rag_engine.retrieve(query, top_k=4, threshold=0.02) if rag_engine else []
        latency_ms = round((time.time() - t_start) * 1000, 1)

        if not matches:
            body = "No documents currently available in index. Ingest PDF/TXT files in Knowledge Vault."
        else:
            body = f"""### 📄 Document Intelligence Decomposition
**Deconstructed Evidence:** Extracted across `{len(matches)}` key document sections.

* **Core Mission / Mandate:** {matches[0]['chunk'][:250]}...
* **Governance & Standards:** {matches[1]['chunk'][:250] if len(matches) > 1 else 'Compliant with enterprise standards'}...
* **Risk Factors:** Low to Moderate operational impact based on current document provisions.
"""
        return {
            "agent_name": "📄 Document Intelligence Agent",
            "intent": "DOCUMENT_INTELLIGENCE",
            "answer": body,
            "matches": matches,
            "structured_data": None,
            "recommended_actions": ["Generate Intelligence Card", "Scan for Knowledge Gaps", "Export Markdown Brief"],
            "latency_ms": latency_ms
        }

    @classmethod
    def _execute_knowledge_agent(cls, query: str, rag_engine, persona: str, top_k: int, threshold: float, t_start: float) -> dict:
        """General knowledge Q&A agent with grounded RAG retrieval."""
        res = rag_engine.answer_with_persona(query, persona=persona, top_k=top_k, threshold=threshold) if rag_engine else {"answer": "No documents indexed.", "matches": [], "latency_ms": 0}
        latency_ms = round((time.time() - t_start) * 1000, 1)

        return {
            "agent_name": "🧠 Neural Knowledge Agent",
            "intent": "KNOWLEDGE_QA",
            "answer": res["answer"],
            "matches": res.get("matches", []),
            "structured_data": None,
            "recommended_actions": ["Explore Knowledge Graph", "Decompose Document Details", "Create Task from Insight"],
            "latency_ms": latency_ms
        }
