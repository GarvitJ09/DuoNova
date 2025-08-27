# ATS-Checker Development Startup Script
Write-Host "Starting ATS-Checker Development Environment..." -ForegroundColor Green

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy env_template.txt to .env and configure your API keys" -ForegroundColor Yellow
    Write-Host ""
}

# Start the FastAPI development server using virtual environment Python
Write-Host "Starting FastAPI server with hot reload..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
