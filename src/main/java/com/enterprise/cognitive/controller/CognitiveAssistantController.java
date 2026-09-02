package com.enterprise.cognitive.controller;

import com.enterprise.cognitive.model.KnowledgeChunk;
import com.enterprise.cognitive.service.DocumentProcessorService;
import com.enterprise.cognitive.service.FirebaseSyncService;
import com.enterprise.cognitive.service.RAGEngineService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Enterprise Cognitive Assistant REST API Controller
 * Exposes Enterprise Endpoints for Document Ingestion, RAG Semantic Queries, and Cloud Sync.
 */
@RestController
@RequestMapping("/api/v1/cognitive")
@CrossOrigin(origins = "*")
public class CognitiveAssistantController {

    @Autowired
    private RAGEngineService ragEngineService;

    @Autowired
    private DocumentProcessorService documentProcessorService;

    @Autowired
    private FirebaseSyncService firebaseSyncService;

    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getEngineStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("system", "Enterprise Cognitive Knowledge Assistant");
        status.put("runtime", "Java 17 OpenJDK / Spring Boot Enterprise 3.2");
        status.put("vectorEngine", "Java Lucene Vector Space Model (VSM)");
        status.put("cloudProvider", "Google Cloud Firebase Firestore");
        status.put("firebaseProjectId", firebaseSyncService.getProjectId());
        status.put("firebaseConnected", firebaseSyncService.isConnected());
        status.put("serverTime", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        return ResponseEntity.ok(status);
    }

    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> executeCognitiveQuery(@RequestBody Map<String, String> payload) {
        String query = payload.getOrDefault("query", "");
        String username = payload.getOrDefault("username", "Guest");

        List<KnowledgeChunk> results = ragEngineService.queryContext(query, 3);

        String answer;
        if (results.isEmpty()) {
            answer = "No matching neural context found in indexed enterprise repository.";
        } else {
            StringBuilder sb = new StringBuilder("Retrieved Context:\n");
            for (KnowledgeChunk chunk : results) {
                sb.append("- ").append(chunk.getContent()).append("\n");
            }
            answer = sb.toString();
        }

        // Persist interaction log to Firebase
        firebaseSyncService.persistChatLog(
            username, 
            query, 
            answer, 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
        );

        Map<String, Object> response = new HashMap<>();
        response.put("query", query);
        response.put("answer", answer);
        response.put("retrievedChunks", results);
        return ResponseEntity.ok(response);
    }
}
