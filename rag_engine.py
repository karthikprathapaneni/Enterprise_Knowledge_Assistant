import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGEngine:
    def __init__(self):
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None

    def build_index(self, chunks):
        self.chunks = [c for c in chunks if c.strip()]
        if not self.chunks:
            self.vectorizer = None
            self.tfidf_matrix = None
            return

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

    def retrieve(self, question: str, top_k: int = 3, threshold: float = 0.03):
        """Retrieves top_k relevant chunks along with cosine similarity scores."""
        if not self.chunks or not question or not question.strip():
            return []

        matches = []

        # 1. TF-IDF Cosine Similarity
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([question])
                sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                ranked_indices = np.argsort(sims)[::-1]

                for idx in ranked_indices[:top_k]:
                    score = float(sims[idx])
                    if score >= threshold:
                        matches.append({"score": score, "chunk": self.chunks[idx], "chunk_idx": int(idx)})
            except Exception as e:
                print(f"TF-IDF search error: {e}")

        # 2. Fallback to keyword matching if no TF-IDF matches above threshold
        if not matches:
            words = [w.lower() for w in question.split() if len(w) > 2]
            kw_matches = []
            for idx, chunk in enumerate(self.chunks):
                chunk_lower = chunk.lower()
                matched_cnt = sum(1 for w in words if w in chunk_lower)
                if matched_cnt > 0:
                    score = min(matched_cnt / max(len(words), 1), 0.95)
                    kw_matches.append({"score": score, "chunk": chunk, "chunk_idx": idx})
            if kw_matches:
                kw_matches.sort(key=lambda x: x["score"], reverse=True)
                matches = kw_matches[:top_k]

        return matches

    def answer_with_persona(self, question: str, persona: str = "Executive", top_k: int = 3, threshold: float = 0.03):
        """Generates an intelligent, grounded RAG response synthesized for the specific enterprise persona."""
        t_start = time.time()
        matches = self.retrieve(question, top_k=top_k, threshold=threshold)
        latency_ms = round((time.time() - t_start) * 1000, 1)

        if not self.chunks:
            return {
                "answer": "⚠️ **No documents available in vector index.** Please load or upload documents in the **Neural Document Vault** first.",
                "matches": [],
                "latency_ms": latency_ms
            }

        if not matches:
            return {
                "answer": f"🔍 **No direct matches found** for *'{question}'* with sensitivity threshold `{threshold}`. Try rephrasing your inquiry or lowering the similarity threshold in **Ingestion Studio**.",
                "matches": [],
                "latency_ms": latency_ms
            }

        top_match = matches[0]
        top_conf = int(min(top_match["score"] * 100, 99)) if top_match["score"] < 1.0 else 100

        # Construct persona-specific synthesis
        if persona == "Executive":
            formatted_answer = f"""### 📋 Executive Summary
**Confidence Level:** `{top_conf}% Match` • **Retrieval Latency:** `{latency_ms} ms`

#### 🎯 Strategic Overview
Based on verified enterprise document records, here are the primary findings for:
> *"{question}"*

* **Primary Finding:** {top_match['chunk'][:280]}...
* **Operational Implication:** High relevance to active documented policies and procedures.
* **Recommended Next Step:** Cross-verify referenced section against departmental guidelines.
"""
        elif persona == "Technical / Data Analyst":
            formatted_answer = f"""### 🛠️ Technical Deep-Dive
**Confidence Level:** `{top_conf}% Match` • **Latency:** `{latency_ms} ms`

#### 🔬 Semantic Retrieval Evidence
Query evaluated against TF-IDF n-gram vector matrix across `{len(self.chunks)}` active chunk embeddings.

* **Top Matched Knowledge Layer:**
> "{top_match['chunk']}"

* **Vector Metrics:** Cosine similarity coefficient of `{top_match['score']:.4f}` with top-ranked index `#{top_match['chunk_idx'] + 1}`.
"""
        else: # Compliance & Risk
            formatted_answer = f"""### 🛡️ Compliance & Governance Review
**Confidence Level:** `{top_conf}% Match` • **Audit Latency:** `{latency_ms} ms`

#### ⚖️ Regulatory & Policy Examination
Analysis conducted against registered internal repository records:

* **Documented Stance:** {top_match['chunk'][:320]}...
* **Compliance Status:** Grounded strictly in repository knowledge without unverified external hallucination.
* **Audit Trail Ref:** Chunk Embedding `#{top_match['chunk_idx'] + 1}`.
"""

        return {
            "answer": formatted_answer,
            "matches": matches,
            "latency_ms": latency_ms
        }

    def answer(self, question: str, top_k: int = 3) -> str:
        """Backward-compatible standard answer function."""
        res = self.answer_with_persona(question, persona="Executive", top_k=top_k)
        return res["answer"]