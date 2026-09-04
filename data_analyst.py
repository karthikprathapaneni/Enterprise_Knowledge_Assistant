import streamlit as st
import pandas as pd
import plotly.express as px
from orchestrator import AIOrchestrator
from database import execute_safe_sql

def data_analyst_page():
    st.subheader("📊 AI Natural Language Data Analyst")
    st.caption("Ask questions in plain English against structured enterprise operational, financial, and headcount data.")

    # Preset Analytic Query Buttons
    st.markdown("##### ⚡ Instant Analytic Inquiries:")
    col_q1, col_q2, col_q3 = st.columns(3)
    preset_query = None
    if col_q1.button("💰 Spend by Department", use_container_width=True):
        preset_query = "Show total spend and budget allocation by department"
    if col_q2.button("☁️ Cloud Spend Trend (Q1 vs Q2)", use_container_width=True):
        preset_query = "Compare cloud infrastructure compute spend between Q1 and Q2"
    if col_q3.button("👥 Department Headcount & Staffing", use_container_width=True):
        preset_query = "What is the personnel headcount across engineering and operations?"

    user_query = st.text_input(
        "Enter your natural language data question:",
        value=preset_query if preset_query else "",
        placeholder="e.g., Show quarterly spend breakdown by department..."
    )

    if st.button("🚀 Analyze Enterprise Data", use_container_width=True, type="primary"):
        if user_query.strip():
            with st.spinner("Compiling natural language to validated SQL and querying enterprise tables..."):
                profile = st.session_state.get("user_profile", {"username": "user", "clearance_level": 1})
                result = AIOrchestrator._execute_data_analyst(user_query, profile, t_start=0)
                st.session_state.latest_analyst_result = result
        else:
            st.warning("Please provide a query for data analysis.")

    if "latest_analyst_result" in st.session_state and st.session_state.latest_analyst_result:
        res = st.session_state.latest_analyst_result
        st.write("")
        st.markdown(res["answer"])

        df = res.get("structured_data")
        if df is not None and not df.empty:
            c_view1, c_view2 = st.columns([1.3, 1])

            theme = st.session_state.get("theme", "Dark")
            chart_font_color = "#0f172a" if theme == "Light" else "#f8fafc"

            with c_view1:
                st.markdown("##### 📈 Interactive Plotly Chart")
                # Auto-determine best chart
                if "department" in df.columns and "total_amount" in df.columns:
                    fig = px.bar(
                        df, x="department", y="total_amount", color="category",
                        title="Aggregated Spend by Department & Category",
                        barmode="group",
                        color_discrete_sequence=['#6366f1', '#a855f7', '#06b6d4', '#10b981']
                    )
                elif "fiscal_period" in df.columns and "total_spend" in df.columns:
                    fig = px.bar(
                        df, x="fiscal_period", y="total_spend", color="department",
                        title="Fiscal Period Expenditure Trend",
                        barmode="group",
                        color_discrete_sequence=['#4f46e5', '#ec4899', '#06b6d4']
                    )
                elif "amount" in df.columns:
                    fig = px.pie(
                        df, names="metric_name" if "metric_name" in df.columns else "department",
                        values="amount",
                        hole=0.5,
                        title="Metric Distribution",
                        color_discrete_sequence=['#4f46e5', '#8b5cf6', '#ec4899', '#10b981']
                    )
                else:
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Data Overview")

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=chart_font_color,
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with c_view2:
                st.markdown("##### 🗄️ Executed Result Set")
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Result (CSV)", data=csv, file_name="data_analyst_export.csv", mime="text/csv")

            with st.expander("🔍 Inspect Safe SQL Query Execution", expanded=False):
                st.code(res.get("sql_query", "SELECT * FROM structured_enterprise_data"), language="sql")
                st.caption("Guardrail: Enforced AST/Regex parser prohibits destructive queries (DROP, DELETE, UPDATE, ALTER).")
