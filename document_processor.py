import os
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from pypdf import PdfReader
from database import add_document
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

def get_available_local_docs():
    """Returns list of filenames present in documents/ directory."""
    if not os.path.exists(DOCS_DIR):
        return []
    valid_exts = {".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt", ".md", ".json"}
    files = []
    for f in os.listdir(DOCS_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in valid_exts and os.path.isfile(os.path.join(DOCS_DIR, f)):
            size_kb = round(os.path.getsize(os.path.join(DOCS_DIR, f)) / 1024, 1)
            files.append({"filename": f, "path": os.path.join(DOCS_DIR, f), "size_kb": size_kb, "ext": ext[1:].upper()})
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

def extract_docx_text(file_path):
    """Extracts text runs and paragraphs from Microsoft Word (.docx) documents."""
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.iterfind('.//w:p', ns):
                texts = [node.text for node in p.iterfind('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return clean_text('\n\n'.join(paragraphs))
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_tabular_text(file_path, ext):
    """Extracts structured rows from CSV/Excel sheets and serializes them into semantic sentences."""
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        lines = [f"Tabular Dataset: {os.path.basename(file_path)} with {len(df)} records."]
        for idx, row in df.iterrows():
            row_items = [f"{col}: {val}" for col, val in row.items() if pd.notna(val)]
            lines.append(f"[Record #{idx + 1}] " + " • ".join(row_items))
        return clean_text("\n".join(lines))
    except Exception as e:
        print(f"Error reading tabular file {file_path}: {e}")
        return ""

def process_single_file(file_path, filename):
    """Extracts clean text layer across PDF, DOCX, XLSX, CSV, and text files."""
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        return extract_pdf_text(file_path)
    elif ext == ".docx":
        return extract_docx_text(file_path)
    elif ext in {".xlsx", ".xls", ".csv"}:
        return extract_tabular_text(file_path, ext)
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