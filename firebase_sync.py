import streamlit as st
import pandas as pd
import json
import os
from firebase_manager import (
    is_firebase_connected,
    init_firebase,
    get_firebase_project_id,
    get_documents_firebase,
    get_chat_history_firebase,
    sync_sqlite_to_firebase
)
from database import get_documents, get_chat_history

def firebase_sync_page():
    st.subheader("🔥 Firebase Cloud Database & Real-Time Sync")
    st.markdown("Connect your Firebase project to enable real-time Cloud Firestore document persistence and multi-device chat synchronization.")

    connected = is_firebase_connected()
    project_id = get_firebase_project_id()

    # --- Connection Status Banner ---
    c_stat1, c_stat2, c_stat3 = st.columns(3)
    with c_stat1:
        if connected:
            st.markdown("""
                <div class="ai-card">
                    <span class="ai-metric-label">Firebase Status</span>
                    <div class="ai-metric-value" style="color: #10b981; font-size: 1.6rem;">🟢 ONLINE</div>
                    <span class="ai-badge badge-active">Cloud Firestore Ready</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="ai-card">
                    <span class="ai-metric-label">Firebase Status</span>
                    <div class="ai-metric-value" style="color: #f59e0b; font-size: 1.6rem;">🟡 STANDBY</div>
                    <span class="ai-badge badge-purple">Local SQLite Active</span>
                </div>
            """, unsafe_allow_html=True)
    with c_stat2:
        st.markdown(f"""
            <div class="ai-card">
                <span class="ai-metric-label">Target Project ID</span>
                <div class="ai-metric-value" style="font-size: 1.3rem; word-break: break-all;">{project_id}</div>
                <span class="ai-badge badge-indigo">Google Cloud Platform</span>
            </div>
        """, unsafe_allow_html=True)
    with c_stat3:
        st.markdown("""
            <div class="ai-card">
                <span class="ai-metric-label">Storage Architecture</span>
                <div class="ai-metric-value" style="font-size: 1.3rem;">Hybrid Sync</div>
                <span class="ai-badge badge-active">Dual Mode Fallback</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    tab_connect, tab_sync, tab_inspector, tab_help = st.tabs([
        "🔑 Project Connection",
        "⚡ Data Migration & Sync",
        "🔍 Cloud Collections Inspector",
        "📖 Connection Guide"
    ])

    # TAB 1: PROJECT CONNECTION
    with tab_connect:
        st.markdown("#### 🔗 Connect Firebase Project")
        st.info("Connect using either your Web App Config snippet (from your open Firebase Web App page) or your Service Account JSON.")

        conn_method = st.radio(
            "Choose Connection Method",
            [
                "📋 Paste Web App `firebaseConfig` (From Web App Settings)",
                "🔑 Upload `serviceAccountKey.json` File",
                "📝 Paste Service Account JSON Content"
            ],
            index=0
        )

        if "Web App" in conn_method:
            st.markdown(f"##### Paste the `firebaseConfig` object from [Firebase Web App Settings](https://console.firebase.google.com/u/0/project/{project_id}/settings/general/web:YTk1NDMwYjQtNzg0My00MzczLWE0YzgtMjAyZTU4ZGU4N2I3):")
            web_cfg_snippet = st.text_area(
                "Paste Firebase Web Config Code:",
                value=f"""const firebaseConfig = {{
  apiKey: "YOUR_API_KEY_HERE",
  authDomain: "{project_id}.firebaseapp.com",
  projectId: "{project_id}",
  storageBucket: "{project_id}.firebasestorage.app",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "1:...:web:..."
}};""",
                height=190
            )

            if st.button("🚀 Connect via Web App Config", use_container_width=True, type="primary"):
                if web_cfg_snippet.strip() and "YOUR_API_KEY_HERE" not in web_cfg_snippet:
                    success, msg = init_firebase(web_cfg_snippet)
                    if success:
                        st.success(f"🎉 {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.warning("Please paste your actual `firebaseConfig` snippet from the Firebase Web App page with your API key.")

        elif "Upload" in conn_method:
            uploaded_json = st.file_uploader(
                "Upload `serviceAccountKey.json` or `firebase_credentials.json`",
                type=["json"]
            )
            if uploaded_json is not None:
                if st.button("🚀 Initialize & Connect Firebase", use_container_width=True, type="primary"):
                    try:
                        key_data = json.loads(uploaded_json.getvalue().decode("utf-8"))
                        success, msg = init_firebase(key_data)
                        if success:
                            st.success(f"🎉 {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    except Exception as ex:
                        st.error(f"Invalid JSON file format: {ex}")
        else:
            json_text = st.text_area(
                "Paste Service Account JSON:",
                placeholder='{\n  "type": "service_account",\n  "project_id": "knowledge-9d660",\n  ...\n}',
                height=180
            )
            if st.button("🚀 Connect via Service Account Payload", use_container_width=True, type="primary"):
                if json_text.strip():
                    try:
                        key_data = json.loads(json_text.strip())
                        success, msg = init_firebase(key_data)
                        if success:
                            st.success(f"🎉 {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    except Exception as ex:
                        st.error(f"JSON Parsing error: {ex}")
                else:
                    st.warning("Please paste valid JSON credentials.")

    # TAB 2: DATA SYNC
    with tab_sync:
        st.markdown("#### ⚡ Synchronize Database Records")
        st.markdown("Push all existing local SQLite document records and chat logs directly into Cloud Firestore.")

        local_docs = get_documents(prefer_cloud=False)
        local_chats = get_chat_history(prefer_cloud=False)

        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Local Documents Ready for Sync", len(local_docs))
        col_s2.metric("Local Chat Logs Ready for Sync", len(local_chats))

        if st.button("📤 Push Local Data ➔ Firebase Firestore", use_container_width=True, type="primary", disabled=not connected):
            if not connected:
                st.warning("Please connect your Firebase project in the **Project Connection** tab first.")
            else:
                with st.spinner("Pushing collections to Firebase Cloud Firestore..."):
                    success, msg = sync_sqlite_to_firebase(local_docs, local_chats)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    # TAB 3: CLOUD INSPECTOR
    with tab_inspector:
        st.markdown("#### 🔍 Cloud Firestore Collections Live View")
        if not connected:
            st.info("💡 Connect Firebase to query live Firestore documents and chat interaction records.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 📄 `documents` Collection (Firestore)")
                cloud_docs = get_documents_firebase()
                if cloud_docs:
                    df_cdocs = pd.DataFrame(cloud_docs, columns=["Filename", "Timestamp"])
                    st.dataframe(df_cdocs, use_container_width=True)
                else:
                    st.info("No documents currently in Firebase Firestore.")

            with c2:
                st.markdown("##### 💬 `chat_history` Collection (Firestore)")
                cloud_chats = get_chat_history_firebase()
                if cloud_chats:
                    df_cchats = pd.DataFrame(cloud_chats, columns=["User", "Question", "Answer", "Timestamp"])
                    st.dataframe(df_cchats, use_container_width=True)
                else:
                    st.info("No chat logs currently in Firebase Firestore.")

    # TAB 4: CONNECTION GUIDE
    with tab_help:
        st.markdown(f"""
        ### 📋 How to Connect Your Firebase Project (`{project_id}`) in 3 Quick Steps:
        
        1. **Enable Cloud Firestore**:
           - Open [Firebase Console - Firestore Database](https://console.firebase.google.com/u/0/project/{project_id}/firestore).
           - Click **Create Database** (choose default location, e.g. `nam5` or `asia-south1`, and select **Start in test mode**).
        
        2. **Download Service Account Key**:
           - Open [Firebase Console - Service Accounts](https://console.firebase.google.com/u/0/project/{project_id}/settings/serviceaccounts/adminsdk).
           - Click the blue **Generate new private key** button.
           - A `.json` file will be downloaded to your computer.
        
        3. **Connect to App**:
           - Go to the **🔑 Project Connection** tab above and upload the downloaded JSON file, OR
           - Save that file directly as `firebase_credentials.json` in the root folder (`d:\\Enterprise_Cognitive_Knowledge_Assistant`).
           - Click **Initialize & Connect Firebase**!
        """)
