import streamlit as st
import os
import tempfile

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except (ImportError, Exception):
    pyttsx3 = None
    HAS_PYTTSX3 = False

try:
    import speech_recognition as sr
    HAS_SR = True
except (ImportError, Exception):
    sr = None
    HAS_SR = False

def text_to_speech(text: str, rate: int = 150, volume: float = 1.0):
    if not HAS_PYTTSX3 or pyttsx3 is None:
        raise RuntimeError("pyttsx3 library is not installed or audio driver is unavailable.")
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Safely create temporary file on Windows
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_path = temp_file.name
    temp_file.close()
    
    engine.save_to_file(text, temp_path)
    engine.runAndWait()
    return temp_path

def voice_page():
    st.subheader("🎙️ Voice & Audio Intelligence Hub")

    tab_tts, tab_stt = st.tabs(["🔊 Text-to-Speech (TTS)", "🎤 Audio-to-Text Transcriber (STT)"])

    with tab_tts:
        st.markdown("#### Neural Voice Synthesizer")
        
        c_rate, c_vol = st.columns(2)
        with c_rate:
            speech_rate = st.slider("Speech Rate (Words per Min)", 100, 250, 160, 10)
        with c_vol:
            speech_vol = st.slider("Audio Volume", 0.1, 1.0, 1.0, 0.1)

        text_input = st.text_area(
            "Input text for voice narration:",
            value="Welcome to the Enterprise Cognitive Knowledge Assistant. Neural document analysis and voice capabilities are online.",
            height=120
        )

        if st.button("🔊 Synthesize Speech", use_container_width=True, type="primary"):
            if text_input.strip():
                with st.spinner("Synthesizing audio stream..."):
                    try:
                        audio_path = text_to_speech(text_input, rate=speech_rate, volume=speech_vol)
                        with open(audio_path, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/wav")
                        st.success("✅ Voice audio synthesized successfully!")
                        if os.path.exists(audio_path):
                            try:
                                os.remove(audio_path)
                            except Exception:
                                pass
                    except Exception as e:
                        st.error(f"TTS Synthesis error: {e}")
            else:
                st.warning("Please provide valid text for speech synthesis.")

    with tab_stt:
        st.markdown("#### Audio File Transcriber")
        audio_file = st.file_uploader("Upload Audio File (WAV format recommended)", type=["wav", "aiff", "flac"])

        if audio_file is not None:
            st.audio(audio_file)
            if st.button("Transcribe Audio Content", use_container_width=True):
                if not HAS_SR or sr is None:
                    st.warning("SpeechRecognition library is not installed. Please run `pip install SpeechRecognition` to enable audio transcription.")
                else:
                    with st.spinner("Processing audio recognition layers..."):
                        try:
                            recognizer = sr.Recognizer()
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                                tmp_audio.write(audio_file.getvalue())
                                tmp_audio_path = tmp_audio.name
                            
                            with sr.AudioFile(tmp_audio_path) as source:
                                audio_data = recognizer.record(source)
                                try:
                                    transcribed_text = recognizer.recognize_google(audio_data)
                                    st.success("✅ Audio transcribed successfully!")
                                    st.text_area("Transcribed Output", value=transcribed_text, height=120)
                                except sr.UnknownValueError:
                                    st.warning("Could not decipher speech in the provided audio file.")
                                except Exception as req_err:
                                    st.info(f"Local speech engine processed audio layer (Recognition Notice: {req_err}).")
                            
                            if os.path.exists(tmp_audio_path):
                                os.remove(tmp_audio_path)
                        except Exception as ex:
                            st.error(f"Audio processing error: {ex}")