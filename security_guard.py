import re
from database import log_security_event

class AIGuard:
    """Security firewall and guardrail monitor for enterprise LLM queries and document safety."""

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"disregard\s+(all\s+)?guidelines",
        r"system\s*:\s*you\s+are\s+now",
        r"reveal\s+(your\s+)?system\s+prompt",
        r"override\s+(all\s+)?safety",
        r"act\s+as\s+(dan|an\s+unrestricted\s+ai)",
        r"drop\s+table",
        r"delete\s+from\s+users",
        r"--\s*$",
        r"union\s+select",
        r"bypass\s+clearance",
        r"extract\s+all\s+passwords"
    ]

    SENSITIVE_LEAK_PATTERNS = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN format
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",  # Emails (flagged for review if mass exfil)
        r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"  # API Keys
    ]

    @classmethod
    def inspect_query(cls, query: str, username: str = "guest") -> dict:
        """Evaluates input query for prompt injections, SQLi, and security threats."""
        q_lower = query.lower().strip()
        risk_score = 0.0
        detected_threats = []

        # 1. Prompt Injection & Jailbreak Scans
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, q_lower):
                risk_score = max(risk_score, 0.88)
                detected_threats.append(f"Prompt Injection / Rule Override attempt ({pattern})")

        # 2. Heuristic Length & Obfuscation Scans
        if len(query) > 2500:
            risk_score = max(risk_score, 0.50)
            detected_threats.append("Excessive payload length")

        # 3. Decision & Audit Logging
        if risk_score >= 0.75:
            action = "BLOCKED"
            log_security_event(
                event_type="PROMPT_INJECTION_BLOCKED",
                username=username,
                query=query[:200],
                risk_score=risk_score,
                action_taken=action
            )
            return {
                "safe": False,
                "risk_score": risk_score,
                "threats": detected_threats,
                "action": action,
                "response": "🛡️ **AI GUARD SECURITY NOTICE: Query Blocked.**\n\nYour inquiry triggered security guardrails (*potential prompt injection or policy override attempt*). This incident has been logged to the Enterprise Security Audit Trail."
            }

        if risk_score > 0.3:
            log_security_event(
                event_type="SUSPICIOUS_QUERY_FLAGGED",
                username=username,
                query=query[:200],
                risk_score=risk_score,
                action_taken="MONITORED"
            )

        return {
            "safe": True,
            "risk_score": risk_score,
            "threats": detected_threats,
            "action": "ALLOWED"
        }
