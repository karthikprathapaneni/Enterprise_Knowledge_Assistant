import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from collections import Counter

def knowledge_graph_page():
    st.subheader("🕸️ Semantic Knowledge Graph Visualizer")
    st.caption("Explore interactive conceptual entity networks, co-occurrence topologies, and semantic clustering.")

    if "rag" not in st.session_state or not st.session_state.rag or not st.session_state.rag.chunks:
        st.warning("⚠️ **No indexed documents found.** Please index documents in the **Neural Document Vault** to construct the semantic knowledge graph.")
        return

    # Extract top relevant terms across chunks
    all_text = " ".join(st.session_state.rag.chunks)
    stopwords = {
        "the", "and", "that", "have", "for", "not", "with", "you", "this", "but", "his", "from", 
        "they", "say", "her", "she", "will", "one", "all", "would", "there", "their", "what", 
        "out", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", 
        "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", 
        "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", 
        "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", 
        "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", 
        "us", "document", "page", "section", "chapter", "shall", "must", "such", "said"
    }

    raw_words = [w.strip(".,:;()[]\"'{}/\\!?-_").lower() for w in all_text.split()]
    meaningful_words = [w for w in raw_words if len(w) > 3 and w not in stopwords]

    word_counts = Counter(meaningful_words)

    # Graph Controls
    c_ctrl1, c_ctrl2 = st.columns([1.5, 1])
    with c_ctrl1:
        max_concepts = st.slider("Concept Node Density (Top Terms)", 10, 35, 20, 2)
    with c_ctrl2:
        layout_engine = st.selectbox("Network Visualization Style", ["Interactive Plotly 2D Network", "Publication Spring Layout"])

    top_terms = [word for word, count in word_counts.most_common(max_concepts)]

    if len(top_terms) < 3:
        st.info("Not enough distinct conceptual keywords extracted to build knowledge graph.")
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

    # Fallback to chain if no edges
    if G.number_of_edges() == 0:
        for i in range(len(top_terms) - 1):
            G.add_edge(top_terms[i], top_terms[i + 1], weight=1)

    # Network Intelligence Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Concept Nodes</span>
                <div class="ai-metric-value">{G.number_of_nodes()}</div>
                <span class="ai-badge badge-indigo">Semantic Entities</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Relationship Edges</span>
                <div class="ai-metric-value">{G.number_of_edges()}</div>
                <span class="ai-badge badge-purple">Co-Occurrences</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        density_val = nx.density(G)
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Network Density</span>
                <div class="ai-metric-value">{density_val:.2f}</div>
                <span class="ai-badge badge-active">Interconnectivity</span>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        central_node = max(dict(G.degree()).items(), key=lambda x: x[1])[0]
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Core Hub Entity</span>
                <div class="ai-metric-value" style="font-size: 1.4rem; padding-top: 5px;">{central_node.capitalize()}</div>
                <span class="ai-badge badge-active">Highest Centrality</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    theme = st.session_state.get("theme", "Light")
    pos = nx.spring_layout(G, k=0.65, seed=42)

    if layout_engine == "Interactive Plotly 2D Network":
        # Build Plotly Network Traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_color = "rgba(99, 102, 241, 0.3)" if theme == "Dark" else "rgba(148, 163, 184, 0.5)"
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color=edge_color),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        node_text = []
        node_sizes = []
        hover_info = []

        degrees = dict(G.degree())
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node.capitalize())
            freq = word_counts[node]
            deg = degrees[node]
            node_sizes.append(min(max(freq * 3.5, 20), 55))
            hover_info.append(f"<b>Concept:</b> {node.upper()}<br><b>Document Frequency:</b> {freq} mentions<br><b>Connected Concepts:</b> {deg}")

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=hover_info,
            text=node_text,
            textposition="top center",
            textfont=dict(
                family="Plus Jakarta Sans, sans-serif",
                size=11,
                color="#f8fafc" if theme == "Dark" else "#1e1b4b"
            ),
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                reversescale=True,
                color=[degrees[n] for n in G.nodes()],
                size=node_sizes,
                colorbar=dict(
                    thickness=12,
                    title=dict(text="Centrality Degree", font=dict(color="#94a3b8", size=10)),
                    xanchor="left",
                    tickfont=dict(color="#94a3b8")
                ),
                line=dict(width=2, color='#ffffff' if theme == "Light" else '#4f46e5')
            )
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=20, r=20, t=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=550
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        # High-Res Matplotlib Layout
        import matplotlib.pyplot as plt
        bg_color = '#ffffff' if theme == "Light" else '#0b0f19'
        node_color = '#4f46e5' if theme == "Light" else '#6366f1'
        edge_color = '#cbd5e1' if theme == "Light" else '#475569'
        font_color = '#0f172a' if theme == "Light" else '#f8fafc'

        fig, ax = plt.subplots(figsize=(11, 6))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        node_sizes = [min(1400 + word_counts[node] * 120, 3200) for node in G.nodes()]

        nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_sizes, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=1.6, alpha=0.7, ax=ax)
        nx.draw_networkx_labels(G, pos, font_color=font_color, font_size=9, font_weight='bold', ax=ax)

        plt.axis('off')
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)