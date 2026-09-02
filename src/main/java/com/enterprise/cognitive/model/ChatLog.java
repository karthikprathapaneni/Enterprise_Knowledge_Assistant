package com.enterprise.cognitive.model;

/**
 * Enterprise Chat Log Entity Model
 */
public class ChatLog {
    private String id;
    private String username;
    private String query;
    private String response;
    private String timestamp;

    public ChatLog(String id, String username, String query, String response, String timestamp) {
        this.id = id;
        this.username = username;
        this.query = query;
        this.response = response;
        this.timestamp = timestamp;
    }

    public String getId() { return id; }
    public String getUsername() { return username; }
    public String getQuery() { return query; }
    public String getResponse() { return response; }
    public String getTimestamp() { return timestamp; }
}
