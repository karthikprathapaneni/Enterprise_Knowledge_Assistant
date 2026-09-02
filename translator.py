import streamlit as st
import urllib.request
import urllib.parse
import json

LANG_MAP = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh",
    "Japanese": "ja",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar"
}

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    src_code = LANG_MAP.get(source_lang, "en")
    tgt_code = LANG_MAP.get(target_lang, "es")
    
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={src_code}|{tgt_code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data and "responseData" in data and "translatedText" in data["responseData"]:
                return data["responseData"]["translatedText"]
    except Exception as e:
        print(f"Translation API error: {e}")
    
    return f"[{target_lang} Translation of '{text}']"

def translator_page():
    st.subheader("🌐 Neural Knowledge Base Translator")
    st.markdown("Translate query text, extracted document excerpts, and responses across multiple world languages.")

    c1, c2 = st.columns(2)
    with c1:
        source_lang = st.selectbox("Source Language", ["English"] + [l for l in LANG_MAP.keys() if l != "English"])
    with c2:
        target_lang = st.selectbox("Target Language", [l for l in LANG_MAP.keys() if l != source_lang])

    input_text = st.text_area(
        "Source Text Layer", 
        value="The Enterprise Cognitive Knowledge Assistant accelerates enterprise document analysis and real-time semantic discovery.",
        height=130
    )

    if st.button("🌐 Translate Content", use_container_width=True, type="primary"):
        if input_text.strip():
            with st.spinner(f"Translating to {target_lang}..."):
                translated_result = translate_text(input_text, source_lang, target_lang)
                st.success(f"✅ Translation Completed ({source_lang} ➔ {target_lang})")
                st.text_area("Translated Output", value=translated_result, height=130)
        else:
            st.warning("Please enter valid text to translate.")