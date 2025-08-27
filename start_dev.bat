@echo off
echo Starting ATS-Checker Development Environment...

:: Check if .env file exists
if not exist .env (
    echo Warning: .env file not found!
    echo Please copy env_template.txt to .env and configure your API keys
    echo.
)

:: Start the FastAPI development server using virtual environment Python
echo Starting FastAPI server with hot reload...
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
