import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_chat_history, get_documents

def analytics_page():
    st.subheader("📊 Intelligence & Usage Analytics")

    chats = get_chat_history()
    docs = get_documents()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total User Queries", len(chats))
    col2.metric("Knowledge Documents", len(docs))
    col3.metric("Current Active User", st.session_state.get("username", "Guest"))
    col4.metric("Active Session Role", st.session_state.get("role", "User"))

    st.divider()

    if chats:
        df = pd.DataFrame(chats, columns=["Username", "Question", "Answer", "Time"])

        c1, c2 = st.columns(2)
        theme = st.session_state.get("theme", "Light")
        chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"

        with c1:
            st.markdown("#### 👤 Top Active Users")
            user_counts = df["Username"].value_counts().reset_index()
            user_counts.columns = ["Username", "Questions Asked"]

            fig_bar = px.bar(
                user_counts, 
                x="Username", 
                y="Questions Asked",
                color="Questions Asked",
                color_continuous_scale="Viridis",
                title="User Query Volume"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=chart_font_color
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.markdown("#### 💬 Query Length Distribution")
            df['Question_Length'] = df['Question'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)

            fig_hist = px.histogram(
                df, 
                x="Question_Length",
                nbins=10,
                title="Words per User Query",
                color_discrete_sequence=['#4f46e5']
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=chart_font_color
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("#### 📜 Full Interactions Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("💡 No query records found in database yet. Inquire with the AI Assistant in the **Chat Assistant** tab to populate system analytics.")