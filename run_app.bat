@echo off
echo ========================================================
echo Starting Enterprise Cognitive Knowledge Assistant...
echo ========================================================
if exist ".\venv\Scripts\streamlit.exe" (
    .\venv\Scripts\streamlit.exe run app.py
) else (
    streamlit run app.py
)
pause
