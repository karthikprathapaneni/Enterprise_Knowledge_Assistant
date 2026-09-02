import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def knowledge_graph_page():
    st.subheader("🕸️ Semantic Knowledge Graph Visualizer")

    if "rag" not in st.session_state or not st.session_state.rag.chunks:
        st.warning("⚠️ Please upload and index documents in the **Dashboard** tab first to generate a knowledge graph.")
        return

    # Extract top relevant terms across chunks
    all_text = " ".join(st.session_state.rag.chunks)
    stopwords = {"the", "and", "that", "have", "for", "not", "with", "you", "this", "but", "his", "from", "they", "say", "her", "she", "will", "one", "all", "would", "there", "their", "what", "out", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", "document", "page"}
    
    raw_words = [w.strip(".,:;()[]\"'{}/\\!?-_").lower() for w in all_text.split()]
    meaningful_words = [w for w in raw_words if len(w) > 3 and w not in stopwords]

    word_counts = Counter(meaningful_words)
    top_terms = [word for word, count in word_counts.most_common(18)]

    if len(top_terms) < 3:
        st.info("Not enough unique conceptual keywords found to construct visual knowledge graph.")
        return

    # Build co-occurrence graph
    G = nx.Graph()
    for term in top_terms:
        G.add_node(term, weight=word_counts[term])

    # Connect terms that co-occur in the same chunks
    for chunk in st.session_state.rag.chunks:
        chunk_lower = chunk.lower()
        present = [t for t in top_terms if t in chunk_lower]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                if G.has_edge(present[i], present[j]):
                    G[present[i]][present[j]]['weight'] += 1
                else:
                    G.add_edge(present[i], present[j], weight=1)

    # Ensure connected fallback
    if G.number_of_edges() == 0:
        for i in range(len(top_terms) - 1):
            G.add_edge(top_terms[i], top_terms[i + 1], weight=1)

    # Render Graph metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Graph Concept Nodes", G.number_of_nodes())
    c2.metric("Semantic Relationship Edges", G.number_of_edges())
    c3.metric("Network Density", f"{nx.density(G):.2f}")

    theme = st.session_state.get("theme", "Light")
    bg_color = '#ffffff' if theme == "Light" else '#0b0f19'
    node_color = '#4f46e5' if theme == "Light" else '#6366f1'
    edge_color = '#cbd5e1' if theme == "Light" else '#475569'
    font_color = '#0f172a' if theme == "Light" else '#f8fafc'

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    pos = nx.spring_layout(G, k=0.65, seed=42)
    node_sizes = [min(1500 + word_counts[node] * 120, 3500) for node in G.nodes()]

    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_color,
        node_size=node_sizes,
        alpha=0.9,
        ax=ax
    )
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_color,
        width=1.8,
        alpha=0.7,
        ax=ax
    )
    nx.draw_networkx_labels(
        G, pos,
        font_color=font_color,
        font_size=10,
        font_weight='bold',
        font_family='sans-serif',
        ax=ax
    )

    plt.axis('off')
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)