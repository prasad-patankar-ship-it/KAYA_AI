@echo off
title KAYA AI

echo ========================================
echo          KAYA AI STARTING
echo ========================================
echo.

cd /d D:\coding\KAYA_AI

call venv\Scripts\activate

echo Starting KAYA API...
start "KAYA API" cmd /k "call venv\Scripts\activate && uvicorn api_server:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo Starting KAYA Interface...
start "KAYA APP" cmd /k "call venv\Scripts\activate && streamlit run app.py --server.address 0.0.0.0 --server.port 8501"

echo.
echo ========================================
echo KAYA AI IS STARTING
echo ========================================
echo.
echo Android:
echo http://10.84.23.175:8501
echo.
echo API:
echo http://10.84.23.175:8000
echo.
echo Keep both windows open.
echo ========================================

pause