@echo off
title ResearchMind AI (Premium UI)
echo ==============================================
echo   Starting ResearchMind AI - Premium React App
echo ==============================================
echo.

:: Start Backend in a new window
echo Starting Backend (FastAPI)...
start "ResearchMind Backend" cmd /c "cd backend && python -m uvicorn main:app --port 8001"

:: Wait for a couple of seconds to ensure backend is starting
timeout /t 3 /nobreak >nul

:: Start Frontend in a new window
echo Starting Frontend (React)...
start "ResearchMind Frontend" cmd /c "cd frontend && npm run dev"

:: Wait a moment for Vite to start, then open the browser
timeout /t 3 /nobreak >nul
echo Opening your browser to the Premium Interface...
start http://localhost:5173/

echo.
echo Both servers are now running! 
echo Keep the new command prompt windows open while using the app.
echo You can close this window now.
pause
