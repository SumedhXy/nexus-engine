@echo off
echo ------------------------------------------------------------
echo [NEXUS] Starting Crisis Orchestration System...
echo ------------------------------------------------------------

:: 1. Start the Backend (FastAPI) in a new window
start "Nexus-Engine-Server" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: 2. Wait 2 seconds for server to initialize
timeout /t 2 /nobreak > nul

:: 3. Start the Frontend (Vite) in a new window
cd nexus-dashboard
start "Nexus-Dashboard-Front" cmd /k "npm run dev"

echo ------------------------------------------------------------
echo [OK] Both layers are launching.
echo Dashboard: http://localhost:3000
echo Backend:   http://localhost:8000
echo ------------------------------------------------------------
pause
