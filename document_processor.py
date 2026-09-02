import os
from pypdf import PdfReader
from database import add_document
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

def save_uploaded_file(uploaded_file):
    os.makedirs(DOCS_DIR, exist_ok=True)
    path = os.path.join(DOCS_DIR, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    add_document(uploaded_file.name)
    return path

def extract_pdf_text(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_idx + 1} ---\n" + page_text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return clean_text(text)

def process_uploaded_pdfs(uploaded_files):
    full_text = ""
    for uploaded_file in uploaded_files:
        path = save_uploaded_file(uploaded_file)
        if uploaded_file.name.lower().endswith(".pdf"):
            text = extract_pdf_text(path)
        else:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = clean_text(f.read())
            except Exception:
                text = ""
        full_text += f"\n\n[Document: {uploaded_file.name}]\n{text}"
    return full_text

def chunk_text(text, chunk_size=120, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    if not words:
        return chunks
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap if (end - overlap) > start else end
    return chunks