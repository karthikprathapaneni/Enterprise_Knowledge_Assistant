package com.enterprise.cognitive.service;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.FirestoreClient;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Java Firebase Cloud Firestore Synchronization Service
 * Utilizes the Google Firebase Admin Java SDK to persist records to Google Cloud Platform.
 */
@Service
public class FirebaseSyncService {

    private Firestore firestoreDb;
    private boolean connected = false;
    private String projectId = "knowledge-9d660";

    public void initializeFirebase(String credentialsPath) {
        try {
            if (FirebaseApp.getApps().isEmpty()) {
                InputStream serviceAccount = new FileInputStream(credentialsPath);
                FirebaseOptions options = FirebaseOptions.builder()
                        .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                        .setProjectId(projectId)
                        .build();

                FirebaseApp.initializeApp(options);
            }
            this.firestoreDb = FirestoreClient.getFirestore();
            this.connected = true;
            System.out.println("✅ [Java Service] Connected to Firebase Firestore: " + projectId);
        } catch (Exception e) {
            System.err.println("❌ [Java Service] Firebase initialization error: " + e.getMessage());
            this.connected = false;
        }
    }

    public boolean persistDocumentLog(String filename, String uploadTime) {
        if (!connected || firestoreDb == null) return false;
        try {
            Map<String, Object> docData = new HashMap<>();
            docData.put("filename", filename);
            docData.put("upload_time", uploadTime);
            docData.put("engine", "Java_Spring_Boot_Core");

            firestoreDb.collection("documents").add(docData);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean persistChatLog(String username, String question, String answer, String timestamp) {
        if (!connected || firestoreDb == null) return false;
        try {
            Map<String, Object> chatData = new HashMap<>();
            chatData.put("username", username);
            chatData.put("question", question);
            chatData.put("answer", answer);
            chatData.put("time", timestamp);
            chatData.put("engine", "Java_Spring_Boot_Core");

            firestoreDb.collection("chat_history").add(chatData);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isConnected() { return connected; }
    public String getProjectId() { return projectId; }
}
