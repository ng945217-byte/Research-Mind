@echo off
title ResearchMind AI (Streamlit)
echo ==============================================
echo   Starting ResearchMind AI - Streamlit App
echo ==============================================
echo.
echo Please wait while the application loads...

:: Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is not installed. Installing it now...
    pip install streamlit
)

:: Run the Streamlit app
python -m streamlit run streamlit_app.py

pause
