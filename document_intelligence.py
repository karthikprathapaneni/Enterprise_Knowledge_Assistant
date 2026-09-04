import re
from collections import Counter
from database import save_document_metadata, get_document_metadata, get_conflicts, add_conflict

class DocumentIntelligence:
    """Extracts structured metadata, intelligence cards, and deep semantic explanations from enterprise documents."""

    @classmethod
    def analyze_document(cls, filename: str, text: str) -> dict:
        """Decomposes raw document text into structured metadata, entities, and risk factors."""
        text_lower = text.lower()

        # 1. Infer Document Type
        doc_type = "Standard Operating Procedure (SOP)"
        if "policy" in filename.lower() or "policy" in text_lower[:500]:
            doc_type = "Enterprise Policy"
        elif "handbook" in filename.lower() or "employee" in text_lower[:500]:
            doc_type = "Employee Handbook"
        elif "system" in filename.lower() or "architecture" in text_lower[:500] or "appointment" in filename.lower():
            doc_type = "System Architecture & Specs"
        elif "norm" in filename.lower() or "compliance" in text_lower[:500]:
            doc_type = "Regulatory Norms & Compliance"

        # 2. Infer Department
        department = "General Operations"
        if any(w in text_lower for w in ["hr", "employee", "leave", "vacation", "resignation", "conduct"]):
            department = "Human Resources (HR)"
        elif any(w in text_lower for w in ["finance", "expense", "budget", "reimbursement", "per-diem", "invoice"]):
            department = "Finance & Accounting"
        elif any(w in text_lower for w in ["software", "server", "vpn", "database", "api", "architecture", "appointment"]):
            department = "Information Technology (IT)"
        elif any(w in text_lower for w in ["compliance", "audit", "norm", "regulation", "statutory"]):
            department = "Legal & Compliance"

        # 3. Extract Key Entities
        entity_candidates = [
            "Employee", "Manager", "System Administrator", "Department Head", "Doctor", "Patient",
            "Human Resources", "Finance Director", "Security Officer", "External Auditor", "IT Support"
        ]
        entities_found = [ent for ent in entity_candidates if ent.lower() in text_lower]
        if not entities_found:
            entities_found = ["Authorized Personnel", "System User", "Supervisory Authority"]

        # 4. Extract Important Numbers & Figures
        numbers = re.findall(r"(?:₹|\$|USD|INR)?\s?\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s?%|\s?days|\s?hours|\s?lakhs)?\b", text[:8000])
        meaningful_numbers = list(dict.fromkeys([n.strip() for n in numbers if len(n.strip()) > 1 and not n.strip().isdigit()][:6]))

        # 5. Determine Risk Level
        risk_keywords = ["violation", "penalty", "disciplinary", "termination", "critical", "mandatory", "breach"]
        risk_count = sum(text_lower.count(rk) for rk in risk_keywords)
        risk_level = "High" if risk_count > 6 else ("Medium" if risk_count > 2 else "Low")

        # 6. Extract Key Rules & Responsibilities
        sentences = [s.strip() for s in re.split(r"[.!?\n]", text) if len(s.strip()) > 30]
        rules = [s for s in sentences if any(w in s.lower() for w in ["must", "shall", "required", "responsible", "mandatory"])][:4]
        if not rules:
            rules = [s for s in sentences[:3]]

        summary_payload = {
            "doc_type": doc_type,
            "department": department,
            "risk_level": risk_level,
            "entities": entities_found,
            "key_numbers": meaningful_numbers,
            "key_rules": rules,
            "total_words": len(text.split()),
            "total_chars": len(text)
        }

        # Save to database
        save_document_metadata(
            filename=filename,
            doc_type=doc_type,
            department=department,
            clearance_required=2 if risk_level == "High" else 1,
            risk_level=risk_level,
            entities=entities_found,
            summary=summary_payload
        )

        return summary_payload

    @classmethod
    def explain_document(cls, filename: str, text: str) -> dict:
        """Generates a complete multi-section 'Explain This Document' executive briefing."""
        analysis = cls.analyze_document(filename, text)
        sentences = [s.strip() for s in re.split(r"[.!?\n]", text) if len(s.strip()) > 40]
        
        tldr = sentences[0] if sentences else "Document covers operational guidelines and enterprise protocols."
        exec_summary = " ".join(sentences[:3]) if len(sentences) >= 3 else tldr

        faqs = [
            {"q": f"What is the primary governing authority for {filename}?", "a": f"The policy is governed by the {analysis['department']} department."},
            {"q": "Who are the key designated stakeholders?", "a": f"The primary entities include: {', '.join(analysis['entities'][:4])}."},
            {"q": "What is the designated compliance risk level?", "a": f"Categorized as {analysis['risk_level']} operational impact requiring verified adherence."}
        ]

        action_items = [
            f"Review key obligations outlined in Section 1 ({analysis['doc_type']}).",
            f"Verify that departmental procedures in {analysis['department']} adhere to documented standards.",
            "Record attestation and update internal tracking log."
        ]

        return {
            "filename": filename,
            "tldr": tldr,
            "executive_summary": exec_summary,
            "analysis": analysis,
            "faqs": faqs,
            "action_items": action_items
        }

    @classmethod
    def detect_knowledge_gaps(cls, documents: list) -> list:
        """Analyzes enterprise document corpus coverage and flags missing institutional topics."""
        all_doc_names = " ".join(documents).lower()
        
        benchmark_topics = [
            {"topic": "Remote Work & VPN Guidelines", "keywords": ["remote", "vpn", "hybrid", "telecommute"], "impact": "High", "rec": "Formalize explicit remote work security & equipment guidelines."},
            {"topic": "Expense Reimbursement & Per-Diem", "keywords": ["expense", "reimbursement", "travel", "per-diem"], "impact": "Medium", "rec": "Ensure clear receipts submission timelines are documented."},
            {"topic": "Data Classification & GDPR/SOC2", "keywords": ["gdpr", "soc2", "classification", "privacy", "pii"], "impact": "High", "rec": "Adopt mandatory data protection and customer PII handling SOP."},
            {"topic": "Disaster Recovery & Incident Response", "keywords": ["disaster", "recovery", "incident", "escalation", "outage"], "impact": "High", "rec": "Publish verified business continuity and failover runbooks."}
        ]

        gaps = []
        for t in benchmark_topics:
            covered = any(k in all_doc_names for k in t["keywords"])
            if not covered:
                gaps.append(t)
        return gaps
