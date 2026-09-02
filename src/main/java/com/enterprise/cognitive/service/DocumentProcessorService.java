package com.enterprise.cognitive.service;

import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Java Document Ingestion & Chunking Service
 * Extracts text from PDF documents using Apache PDFBox and performs dynamic sliding window chunking.
 */
@Service
public class DocumentProcessorService {

    public String extractPdfContent(File file) throws IOException {
        try (PDDocument document = Loader.loadPDF(file)) {
            PDFTextStripper stripper = new PDFTextStripper();
            return stripper.getText(document);
        }
    }

    public List<String> partitionIntoChunks(String text, int chunkSize, int overlap) {
        List<String> chunks = new ArrayList<>();
        if (text == null || text.trim().isEmpty()) {
            return chunks;
        }

        String[] words = text.split("\\s+");
        int start = 0;

        while (start < words.length) {
            int end = Math.min(start + chunkSize, words.length);
            StringBuilder sb = new StringBuilder();
            for (int i = start; i < end; i++) {
                sb.append(words[i]).append(" ");
            }
            String chunkStr = sb.toString().trim();
            if (!chunkStr.isEmpty()) {
                chunks.add(chunkStr);
            }
            start = (end - overlap > start) ? (end - overlap) : end;
        }
        return chunks;
    }
}
