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
            # Fallback if vocabulary is too small or only stop words
            self.vectorizer = None
            self.tfidf_matrix = None

    def answer(self, question: str, top_k: int = 3) -> str:
        if not self.chunks:
            return "⚠️ No documents available in index. Please upload and embed files in the Dashboard."

        if not question or not question.strip():
            return "Please provide a valid question."

        matches = []

        # 1. Try TF-IDF Vector Cosine Similarity
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([question])
                sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                ranked_indices = np.argsort(sims)[::-1]
                
                for idx in ranked_indices[:top_k]:
                    score = float(sims[idx])
                    if score > 0.02:
                        matches.append((score, self.chunks[idx]))
            except Exception as e:
                print(f"TF-IDF search error: {e}")

        # 2. Fallback to keyword overlap if no vector matches found
        if not matches:
            words = [w.lower() for w in question.split() if len(w) > 2]
            kw_matches = []
            for chunk in self.chunks:
                chunk_lower = chunk.lower()
                matched_cnt = sum(1 for w in words if w in chunk_lower)
                if matched_cnt > 0:
                    score = min(matched_cnt / max(len(words), 1), 1.0)
                    kw_matches.append((score, chunk))
            if kw_matches:
                kw_matches.sort(key=lambda x: x[0], reverse=True)
                matches = kw_matches[:top_k]

        if matches:
            response = "### 🧠 Retrieved Neural Context\n\n"
            for i, (score, chunk) in enumerate(matches, 1):
                conf = int(min(score * 100, 99)) if score < 1.0 else 100
                response += f"**Result #{i}** `(Relevance Score: {conf}%)`\n\n> {chunk}\n\n---\n\n"
            return response

        return "🔍 I couldn't find specific information matching your query in the uploaded documents. Try rephrasing or uploading relevant source files."