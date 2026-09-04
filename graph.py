import streamlit as st
import networkx as nx
from graph_rag import SemanticGraphRAG

def knowledge_graph_page():
    st.subheader("🕸️ Semantic GraphRAG & Entity Network Visualizer")
    st.caption("Interactive directed knowledge graph displaying typed semantic relationships, governance hierarchies, and multi-hop paths.")

    chunks = st.session_state.rag.chunks if ("rag" in st.session_state and st.session_state.rag) else []

    # Build Semantic Triples
    triples = SemanticGraphRAG.extract_semantic_triples(chunks)
    G = SemanticGraphRAG.build_directed_graph(triples)

    # Graph KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Semantic Entities</span>
                <div class="ai-metric-value">{G.number_of_nodes()}</div>
                <span class="ai-badge badge-indigo">Concept Nodes</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Directed Relationships</span>
                <div class="ai-metric-value">{G.number_of_edges()}</div>
                <span class="ai-badge badge-purple">Typed Edges</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Network Density</span>
                <div class="ai-metric-value">{nx.density(G):.2f}</div>
                <span class="ai-badge badge-active">Interconnected</span>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        hub = max(dict(G.degree()).items(), key=lambda x: x[1])[0] if G.number_of_nodes() > 0 else "None"
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Primary Entity Hub</span>
                <div class="ai-metric-value" style="font-size: 1.4rem; padding-top: 5px;">{hub}</div>
                <span class="ai-badge badge-active">Max Centrality</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Interactive Graph Tabs
    tab_network, tab_query, tab_triples = st.tabs([
        "🌐 Interactive Graph Topology",
        "🔍 Multi-Hop Path Querying",
        "📋 Typed Semantic Triples Ledger"
    ])

    theme = st.session_state.get("theme", "Dark")

    # TAB 1: PLOTLY NETWORK
    with tab_network:
        fig = SemanticGraphRAG.render_plotly_graph(G, theme=theme)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Hover over any node to inspect relational degree, incoming prerequisites, and outgoing governing authorities.")

    # TAB 2: MULTI-HOP PATH QUERY
    with tab_query:
        st.markdown("#### 🔍 Graph Context Path Retrieval")
        st.caption("Search an entity to retrieve 1-hop and 2-hop governing relationships across enterprise policies.")

        q_node = st.text_input("Enter entity to trace (e.g. Employee, Leave Policy, VPN Client):", value="Employee")
        if q_node:
            paths = SemanticGraphRAG.query_graph_context(q_node, G)
            if paths:
                st.markdown(f"##### Connected Semantic Paths for `{q_node}`:")
                for p in paths:
                    st.markdown(p)
            else:
                st.info(f"No direct edges found for '{q_node}'. Try selecting from: {', '.join(list(G.nodes())[:6])}")

    # TAB 3: TRIPLES LEDGER
    with tab_triples:
        st.markdown("#### 📋 Extracted Entity-Relationship Triples")
        import pandas as pd
        df_triples = pd.DataFrame(triples, columns=["Subject Entity", "Semantic Relationship", "Object Entity"])
        st.dataframe(df_triples, use_container_width=True)