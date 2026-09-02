package com.enterprise.cognitive.model;

import java.util.Map;

/**
 * Knowledge Chunk Entity Model
 */
public class KnowledgeChunk {
    private String id;
    private String documentName;
    private String content;
    private int chunkIndex;
    private Map<String, Integer> termFrequencies;
    private double similarityScore;

    public KnowledgeChunk(String id, String documentName, String content, int chunkIndex, Map<String, Integer> termFrequencies) {
        this.id = id;
        this.documentName = documentName;
        this.content = content;
        this.chunkIndex = chunkIndex;
        this.termFrequencies = termFrequencies;
    }

    public String getId() { return id; }
    public String getDocumentName() { return documentName; }
    public String getContent() { return content; }
    public int getChunkIndex() { return chunkIndex; }
    public Map<String, Integer> getTermFrequencies() { return termFrequencies; }
    public double getSimilarityScore() { return similarityScore; }
    public void setSimilarityScore(double similarityScore) { this.similarityScore = similarityScore; }
}
