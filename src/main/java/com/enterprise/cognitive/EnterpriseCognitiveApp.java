package com.enterprise.cognitive;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Enterprise Cognitive Knowledge Assistant - Java Enterprise Core Application
 * Handles Neural RAG Retrieval, Apache Lucene Ingestion, and Firebase Firestore Cloud Synchronization.
 */
@SpringBootApplication
@EnableAsync
public class EnterpriseCognitiveApp {

    public static void main(String[] args) {
        System.out.println("===============================================================");
        System.out.println("☕ Starting Enterprise Cognitive Knowledge Assistant (Java JVM)");
        System.out.println("   Architecture: Spring Boot • Lucene Vector Engine • Firestore");
        System.out.println("===============================================================");
        SpringApplication.run(EnterpriseCognitiveApp.class, args);
    }
}
