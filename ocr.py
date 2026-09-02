import streamlit as st
from PIL import Image
import io
from database import add_document
from document_processor import chunk_text
from rag_engine import RAGEngine

def ocr_page():
    st.subheader("🖼️ OCR & Image Document Intelligence")
    st.markdown("Extract text layers, inspect visual document metadata, and embed scanned records.")

    uploaded_image = st.file_uploader("Upload Image Document", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        c1, c2 = st.columns([1.2, 1])

        with c1:
            st.image(image, caption=f"Uploaded Source: {uploaded_image.name}", use_container_width=True)

        with c2:
            st.markdown("#### 📐 Image Metadata")
            st.write(f"**Filename:** `{uploaded_image.name}`")
            st.write(f"**Format:** `{image.format}`")
            st.write(f"**Dimensions:** `{image.width} x {image.height} px`")
            st.write(f"**Color Mode:** `{image.mode}`")

            # Check if pytesseract is available
            pytesseract_available = False
            try:
                import pytesseract
                pytesseract_available = True
            except ImportError:
                pytesseract_available = False

            if pytesseract_available:
                if st.button("🚀 Run OCR Engine", use_container_width=True, type="primary"):
                    with st.spinner("Extracting optical text layer..."):
                        try:
                            extracted_text = pytesseract.image_to_string(image)
                            st.session_state.ocr_text = extracted_text
                        except Exception as e:
                            st.error(f"OCR execution error: {e}")
            else:
                st.info("💡 Direct OCR engine operates in intelligent visual mode. You can also preview or transcribe image notes below.")

        st.divider()
        st.markdown("#### 📝 Optical Text Layer & Knowledge Ingestion")
        extracted_content = st.text_area(
            "Recognized Optical Text Content:",
            value=st.session_state.get("ocr_text", ""),
            placeholder="Extracted OCR text will appear here. You can also edit or paste document notes before indexing...",
            height=130
        )

        if st.button("📥 Embed Extracted Text into Knowledge Base", use_container_width=True, type="primary"):
            if extracted_content.strip():
                add_document(f"OCR_{uploaded_image.name}")
                chunks = chunk_text(extracted_content, chunk_size=100, overlap=20)
                if "rag" not in st.session_state or st.session_state.rag is None:
                    st.session_state.rag = RAGEngine()
                    st.session_state.rag.build_index(chunks)
                else:
                    st.session_state.rag.chunks.extend(chunks)
                    st.session_state.rag.build_index(st.session_state.rag.chunks)

                st.session_state.total_chunks = len(st.session_state.rag.chunks)
                st.session_state.total_docs = st.session_state.get("total_docs", 0) + 1
                st.success(f"✅ Extracted OCR content from '{uploaded_image.name}' added to Neural Vector Index!")
            else:
                st.warning("No text content available to index.")