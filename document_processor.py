import os
from pypdf import PdfReader
from database import add_document
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

def get_available_local_docs():
    """Returns list of filenames present in documents/ directory."""
    if not os.path.exists(DOCS_DIR):
        return []
    valid_exts = {".pdf", ".txt", ".md", ".csv", ".json"}
    files = []
    for f in os.listdir(DOCS_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in valid_exts and os.path.isfile(os.path.join(DOCS_DIR, f)):
            size_kb = round(os.path.getsize(os.path.join(DOCS_DIR, f)) / 1024, 1)
            files.append({"filename": f, "path": os.path.join(DOCS_DIR, f), "size_kb": size_kb})
    return files

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

def process_single_file(file_path, filename):
    """Extracts clean text layer from a local file path."""
    if filename.lower().endswith(".pdf"):
        return extract_pdf_text(file_path)
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return clean_text(f.read())
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

def process_uploaded_pdfs(uploaded_files):
    full_text = ""
    for uploaded_file in uploaded_files:
        path = save_uploaded_file(uploaded_file)
        text = process_single_file(path, uploaded_file.name)
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