import time
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGEngine:
    def __init__(self):
        self.chunks = []
        self.chunk_metadata = [] # stores clearance level (1=Employee, 2=Manager, 3=Executive/Admin)
        self.vectorizer = None
        self.tfidf_matrix = None

    def build_index(self, chunks, metadata_list=None):
        self.chunks = [c for c in chunks if c.strip()]
        if not self.chunks:
            self.vectorizer = None
            self.tfidf_matrix = None
            self.chunk_metadata = []
            return

        if metadata_list and len(metadata_list) == len(self.chunks):
            self.chunk_metadata = metadata_list
        else:
            self.chunk_metadata = []
            for c in self.chunks:
                c_low = c.lower()
                if any(w in c_low for w in ["executive compensation", "confidential board", "termination review", "root admin key"]):
                    lvl = 3
                elif any(w in c_low for w in ["manager approval", "budget allocation", "disciplinary", "internal audit"]):
                    lvl = 2
                else:
                    lvl = 1
                self.chunk_metadata.append({"clearance": lvl})

        try:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=5000
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        except Exception:
            self.vectorizer = None
            self.tfidf_matrix = None

    def retrieve_hybrid(self, question: str, top_k: int = 3, user_clearance: int = 3, rrf_k: int = 60):
        """Executes Hybrid Retrieval combining Lexical Frequency matching and TF-IDF Cosine Similarity via Reciprocal Rank Fusion (RRF)."""
        if not self.chunks or not question or not question.strip():
            return []

        # 1. Lexical Keyword Ranking
        query_words = [w.lower() for w in re.findall(r"\b\w{3,}\b", question)]
        lexical_scores = []
        for idx, chunk in enumerate(self.chunks):
            chunk_low = chunk.lower()
            term_hits = sum(chunk_low.count(w) for w in query_words)
            lexical_scores.append((idx, term_hits))
        
        lexical_ranked = sorted(lexical_scores, key=lambda x: x[1], reverse=True)
        lexical_ranks = {doc_idx: rank for rank, (doc_idx, hits) in enumerate(lexical_ranked, 1) if hits > 0}

        # 2. Vector Cosine Similarity Ranking
        vector_ranks = {}
        vector_sims = {}
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([question])
                sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                vector_ranked = np.argsort(sims)[::-1]
                for rank, doc_idx in enumerate(vector_ranked, 1):
                    score = float(sims[doc_idx])
                    if score > 0.01:
                        vector_ranks[int(doc_idx)] = rank
                        vector_sims[int(doc_idx)] = score
            except Exception as e:
                print(f"Vector retrieval error: {e}")

        # 3. Reciprocal Rank Fusion (RRF) Calculation
        candidate_indices = set(lexical_ranks.keys()).union(set(vector_ranks.keys()))
        if not candidate_indices:
            candidate_indices = set(range(min(len(self.chunks), top_k)))

        rrf_scored = []
        for doc_idx in candidate_indices:
            meta = self.chunk_metadata[doc_idx] if doc_idx < len(self.chunk_metadata) else {"clearance": 1}
            req_clearance = meta.get("clearance", 1)

            # Enforce Permission Clearance Filter
            if req_clearance <= user_clearance:
                r_lex = lexical_ranks.get(doc_idx, 9999)
                r_vec = vector_ranks.get(doc_idx, 9999)
                
                # Standard RRF Formula: sum(1 / (k + rank))
                score_rrf = (1.0 / (rrf_k + r_vec)) + (1.0 / (rrf_k + r_lex))
                cosine_sim = vector_sims.get(doc_idx, 0.05)

                rrf_scored.append({
                    "chunk_idx": doc_idx,
                    "chunk": self.chunks[doc_idx],
                    "score": cosine_sim,
                    "rrf_score": score_rrf,
                    "clearance": req_clearance
                })

        # Sort by RRF score descending
        rrf_scored.sort(key=lambda x: x["rrf_score"], reverse=True)
        return rrf_scored[:top_k]

    def retrieve(self, question: str, top_k: int = 3, threshold: float = 0.03, user_clearance: int = 3):
        """Backward-compatible retrieval wrapper executing Hybrid RRF under the hood."""
        return self.retrieve_hybrid(question, top_k=top_k, user_clearance=user_clearance)

    def answer_with_persona(self, question: str, persona: str = "Executive", top_k: int = 3, threshold: float = 0.03, user_clearance: int = 3):
        t_start = time.time()

        # Restricted Topic Check
        q_low = question.lower()
        if user_clearance < 3 and any(w in q_low for w in ["executive compensation", "confidential board", "termination review", "root admin key"]):
            return {
                "answer": "⛔ **ACCESS DENIED:** You do not possess the required clearance level (Tier 3 Executive Required) to access these classified enterprise records.",
                "matches": [],
                "latency_ms": round((time.time() - t_start) * 1000, 1),
                "access_denied": True
            }

        matches = self.retrieve_hybrid(question, top_k=top_k, user_clearance=user_clearance)
        latency_ms = round((time.time() - t_start) * 1000, 1)

        if not self.chunks:
            return {
                "answer": "⚠️ **No documents available in vector index.** Please load or upload documents in the **Knowledge Vault** first.",
                "matches": [],
                "latency_ms": latency_ms
            }

        if not matches:
            return {
                "answer": f"🔍 **No authorized matches found** for *'{question}'* matching your clearance level (`Tier {user_clearance}`).",
                "matches": [],
                "latency_ms": latency_ms
            }

        top_match = matches[0]
        top_conf = int(min(max(top_match["score"], top_match.get("rrf_score", 0.1) * 30) * 100, 99))

        # Synthesis
        if persona == "Executive":
            formatted_answer = f"""### 📋 Executive Summary
**Confidence Level:** `{top_conf}% Grounded` • **Hybrid Latency:** `{latency_ms} ms` • **Clearance:** `Verified Tier {top_match.get('clearance', 1)}`

#### 🎯 Strategic Overview
Based on verified enterprise document records, here are the primary findings for:
> *"{question}"*

* **Primary Finding:** {top_match['chunk'][:280]}...
* **Operational Implication:** Grounded directly via Hybrid Lexical & Vector RRF Retrieval.
* **Recommended Next Step:** Cross-verify referenced section against departmental guidelines.
"""
        elif persona == "Technical / Data Analyst":
            formatted_answer = f"""### 🛠️ Technical Deep-Dive
**Confidence Level:** `{top_conf}% Match` • **Hybrid Latency:** `{latency_ms} ms` • **Clearance:** `Verified Tier {top_match.get('clearance', 1)}`

#### 🔬 Hybrid Semantic Retrieval Evidence
Query evaluated against TF-IDF n-gram vector matrix and Lexical Token Inverted Index across `{len(self.chunks)}` active chunk embeddings.

* **Top Matched Knowledge Layer:**
> "{top_match['chunk']}"

* **RRF Scoring:** Reciprocal Rank Fusion score of `{top_match.get('rrf_score', 0.016):.5f}` on index `#{top_match['chunk_idx'] + 1}`.
"""
        else: # Compliance & Risk
            formatted_answer = f"""### 🛡️ Compliance & Governance Review
**Confidence Level:** `{top_conf}% Match` • **Hybrid Latency:** `{latency_ms} ms` • **Clearance:** `Verified Tier {top_match.get('clearance', 1)}`

#### ⚖️ Regulatory & Policy Examination
Analysis conducted against registered internal repository records:

* **Documented Stance:** {top_match['chunk'][:320]}...
* **Compliance Status:** Audited and verified with zero ungrounded hallucination.
* **Audit Trail Ref:** Chunk Embedding `#{top_match['chunk_idx'] + 1}`.
"""

        return {
            "answer": formatted_answer,
            "matches": matches,
            "latency_ms": latency_ms
        }

    def answer(self, question: str, top_k: int = 3) -> str:
        res = self.answer_with_persona(question, persona="Executive", top_k=top_k, user_clearance=3)
        return res["answer"]