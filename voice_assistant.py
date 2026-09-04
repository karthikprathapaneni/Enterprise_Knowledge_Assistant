import streamlit as st
import html

def render_audio_narration(text: str, label: str = "🔊 Listen to Briefing", key: str = "audio_btn"):
    """
    Renders an institutional HTML5 Web Speech Synthesis player directly in Streamlit.
    Enables zero-latency, hands-free listening to AI answers, problem runbooks, and executive summaries.
    """
    if not text:
        return

    # Clean and sanitize text for JavaScript string literal
    clean_speech = text.replace('"', '\\"').replace('\n', ' ').replace('\r', ' ')
    # Limit length to first 1200 characters for snappy speech playback
    if len(clean_speech) > 1200:
        clean_speech = clean_speech[:1200] + "... End of executive audio briefing."

    btn_id = f"speech_btn_{abs(hash(key)) % 100000}"

    html_code = f"""
    <div style="display: inline-flex; align-items: center; gap: 8px; margin: 6px 0 10px 0;">
        <button id="{btn_id}" onclick="playExecutiveAudio('{btn_id}')" 
            style="background: #1e293b; color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 6px; padding: 6px 14px; font-size: 0.8rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s ease;">
            {label}
        </button>
        <button onclick="stopExecutiveAudio('{btn_id}')"
            style="background: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center;">
            ⏹ Stop
        </button>
    </div>

    <script>
    function playExecutiveAudio(btnId) {{
        if (!('speechSynthesis' in window)) {{
            alert('Web Speech API is not supported on this browser.');
            return;
        }}
        window.speechSynthesis.cancel(); // cancel any active speech
        
        const utterance = new SpeechSynthesisUtterance("{clean_speech}");
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        
        const btn = document.getElementById(btnId);
        if (btn) btn.innerText = "⏳ Speaking...";

        utterance.onend = function() {{
            if (btn) btn.innerText = "{label}";
        }};
        utterance.onerror = function() {{
            if (btn) btn.innerText = "{label}";
        }};

        window.speechSynthesis.speak(utterance);
    }}

    function stopExecutiveAudio(btnId) {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            const btn = document.getElementById(btnId);
            if (btn) btn.innerText = "{label}";
        }}
    }}
    </script>
    """
    st.components.v1.html(html_code, height=45)

def render_voice_input_button():
    """
    Renders a Web Speech Recognition microphone component for hands-free query dictation.
    """
    html_code = """
    <div style="margin: 4px 0 12px 0;">
        <button id="voice_rec_btn" onclick="startVoiceDictation()"
            style="background: #131b2e; color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 7px 16px; font-size: 0.84rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 8px;">
            🎤 Speak Inquiry (Hands-Free Dictation)
        </button>
        <span id="voice_status" style="font-size: 0.78rem; color: #94a3b8; margin-left: 10px; font-family: monospace;">Ready</span>
    </div>

    <script>
    function startVoiceDictation() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const statusSpan = document.getElementById('voice_status');
        const btn = document.getElementById('voice_rec_btn');

        if (!SpeechRecognition) {
            statusSpan.innerText = "Speech recognition not supported in browser";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            btn.style.borderColor = "#ef4444";
            btn.style.color = "#f87171";
            btn.innerText = "🔴 Listening...";
            statusSpan.innerText = "Speak now into microphone...";
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            statusSpan.innerText = "Captured: \\"" + transcript + "\\"";
            
            // Try copying to clipboard or alerting user
            navigator.clipboard.writeText(transcript).then(() => {
                statusSpan.innerText = "Copied to clipboard: \\"" + transcript + "\\" (Paste into input)";
            });
        };

        recognition.onerror = function(event) {
            statusSpan.innerText = "Error: " + event.error;
            btn.innerText = "🎤 Speak Inquiry (Hands-Free Dictation)";
            btn.style.borderColor = "rgba(16, 185, 129, 0.35)";
            btn.style.color = "#34d399";
        };

        recognition.onend = function() {
            btn.innerText = "🎤 Speak Inquiry (Hands-Free Dictation)";
            btn.style.borderColor = "rgba(16, 185, 129, 0.35)";
            btn.style.color = "#34d399";
        };

        recognition.start();
    }
    </script>
    """
    st.components.v1.html(html_code, height=50)
