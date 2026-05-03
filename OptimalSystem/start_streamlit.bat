@echo off
chcp 65001 >nul
title Optimal Samples Selection System - Streamlit Web Version

echo ==========================================
echo   Optimal Samples Selection System
echo   Streamlit Web Version
echo ==========================================
echo.

cd /d "%~dp0"
cd "1_Source_Codes"

echo Installing dependencies...
pip install streamlit --quiet

echo.
echo Starting Streamlit app...
echo Local URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

streamlit run streamlit_app.py --server.headless true --server.port 8501

pause
