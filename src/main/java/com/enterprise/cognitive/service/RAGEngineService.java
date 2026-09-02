package com.enterprise.cognitive.service;

import com.enterprise.cognitive.model.KnowledgeChunk;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Java RAG Engine Service
 * Implements Vector Space Model (VSM), TF-IDF Feature Extraction, and Cosine Similarity Matching in Java.
 */
@Service
public class RAGEngineService {

    private final List<KnowledgeChunk> indexedChunks = new ArrayList<>();
    private final Map<String, Integer> documentFrequency = new HashMap<>();

    public synchronized void indexChunks(List<String> chunks, String documentName) {
        indexedChunks.clear();
        documentFrequency.clear();

        int chunkIndex = 0;
        for (String chunkText : chunks) {
            if (chunkText != null && !chunkText.trim().isEmpty()) {
                KnowledgeChunk chunk = new KnowledgeChunk(
                    UUID.randomUUID().toString(),
                    documentName,
                    chunkText.trim(),
                    chunkIndex++,
                    computeTermFrequencies(chunkText)
                );
                indexedChunks.add(chunk);

                // Update document frequencies for IDF calculation
                for (String term : chunk.getTermFrequencies().keySet()) {
                    documentFrequency.put(term, documentFrequency.getOrDefault(term, 0) + 1);
                }
            }
        }
    }

    public List<KnowledgeChunk> queryContext(String query, int topK) {
        if (indexedChunks.isEmpty() || query == null || query.trim().isEmpty()) {
            return Collections.emptyList();
        }

        Map<String, Double> queryTfidf = computeQueryTfidf(query);

        PriorityQueue<KnowledgeChunk> rankedQueue = new PriorityQueue<>(
            Comparator.comparingDouble(KnowledgeChunk::getSimilarityScore).reversed()
        );

        int totalDocs = indexedChunks.size();

        for (KnowledgeChunk chunk : indexedChunks) {
            double score = computeCosineSimilarity(queryTfidf, chunk, totalDocs);
            chunk.setSimilarityScore(score);
            if (score > 0.05) {
                rankedQueue.add(chunk);
            }
        }

        List<KnowledgeChunk> topMatches = new ArrayList<>();
        while (!rankedQueue.isEmpty() && topMatches.size() < topK) {
            topMatches.add(rankedQueue.poll());
        }

        return topMatches;
    }

    private Map<String, Integer> computeTermFrequencies(String text) {
        Map<String, Integer> tf = new HashMap<>();
        String[] tokens = text.toLowerCase().split("\\W+");
        for (String token : tokens) {
            if (token.length() > 2) {
                tf.put(token, tf.getOrDefault(token, 0) + 1);
            }
        }
        return tf;
    }

    private Map<String, Double> computeQueryTfidf(String query) {
        Map<String, Integer> tf = computeTermFrequencies(query);
        Map<String, Double> tfidf = new HashMap<>();
        int totalTerms = tf.values().stream().mapToInt(Integer::intValue).sum();

        for (Map.Entry<String, Integer> entry : tf.entrySet()) {
            double termFreq = (double) entry.getValue() / Math.max(totalTerms, 1);
            int df = documentFrequency.getOrDefault(entry.getKey(), 1);
            double idf = Math.log(1.0 + ((double) indexedChunks.size() / df));
            tfidf.put(entry.getKey(), termFreq * idf);
        }
        return tfidf;
    }

    private double computeCosineSimilarity(Map<String, Double> queryVec, KnowledgeChunk chunk, int totalDocs) {
        double dotProduct = 0.0;
        double queryMagnitude = 0.0;
        double chunkMagnitude = 0.0;

        for (double val : queryVec.values()) {
            queryMagnitude += val * val;
        }

        Map<String, Integer> chunkTf = chunk.getTermFrequencies();
        int chunkTotalTerms = chunkTf.values().stream().mapToInt(Integer::intValue).sum();

        for (Map.Entry<String, Integer> entry : chunkTf.entrySet()) {
            String term = entry.getKey();
            double tf = (double) entry.getValue() / Math.max(chunkTotalTerms, 1);
            int df = documentFrequency.getOrDefault(term, 1);
            double idf = Math.log(1.0 + ((double) totalDocs / df));
            double weight = tf * idf;

            chunkMagnitude += weight * weight;

            if (queryVec.containsKey(term)) {
                dotProduct += queryVec.get(term) * weight;
            }
        }

        double denominator = Math.sqrt(queryMagnitude) * Math.sqrt(chunkMagnitude);
        return denominator == 0.0 ? 0.0 : dotProduct / denominator;
    }
}
