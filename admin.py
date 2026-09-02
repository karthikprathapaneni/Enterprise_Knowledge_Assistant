import streamlit as st
import pandas as pd
from database import get_documents, get_chat_history, clear_chat_history

def admin_page():
    st.subheader("🛡️ Enterprise System Administration & Audit")

    if st.session_state.role != "Admin":
        st.error("🚫 Access restricted to authorized Admin accounts only.")
        return

    docs = get_documents()
    chats = get_chat_history()

    # Admin Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Indexed Source Files", len(docs))
    m2.metric("Total Intercepted Logs", len(chats))
    m3.metric("Security Level", "Tier 1 - Root Admin")

    st.divider()

    st.markdown("### 🗄️ Document Storage Audit")
    if docs:
        df_docs = pd.DataFrame(docs, columns=["Filename", "Upload Timestamp"])
        st.dataframe(df_docs, use_container_width=True)
    else:
        st.info("No document records found in system database.")

    st.divider()

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 💬 System-Wide Chat & Query Logs")
    with c2:
        if st.button("🗑️ Purge All Chat Logs", use_container_width=True):
            clear_chat_history()
            st.success("All system chat logs purged.")
            st.rerun()

    if chats:
        df_chats = pd.DataFrame(chats, columns=["User", "Question", "Answer", "Timestamp"])
        st.dataframe(df_chats, use_container_width=True)

        csv_data = df_chats.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Audit Logs (CSV)",
            data=csv_data,
            file_name="enterprise_chat_audit_logs.csv",
            mime="text/csv"
        )
    else:
        st.info("No system chat interaction logs captured.")