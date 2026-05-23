# TruthLens Launch Script

# 1. Check/Start Ollama
Write-Host "Checking Ollama Service..." -ForegroundColor Yellow
$ollamaRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $ollamaRunning = $true
        Write-Host "Ollama is already running." -ForegroundColor Green
    }
} catch {
    $ollamaRunning = $false
}

if (-not $ollamaRunning) {
    Write-Host "Ollama not detected. Attempting to start Ollama..." -ForegroundColor DarkYellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Write-Host "Ollama service started in background." -ForegroundColor Green
}

# 2. Check for Llama3 model
Write-Host "Verifying Llama3 model..." -ForegroundColor Yellow
$models = ollama list
if ($models -like "*llama3*") {
    Write-Host "Llama3 model found." -ForegroundColor Green
} else {
    Write-Host "Llama3 model not found. Pulling llama3 (this may take a while)..." -ForegroundColor Cyan
    ollama pull llama3
}

Write-Host "Starting TruthLens Backend..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\venv\Scripts\python -m uvicorn app.main:app --reload"

Write-Host "Starting TruthLens Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "-------------------------------------------"
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: Check the console for URL (usually http://localhost:5173)"
Write-Host "-------------------------------------------"
Write-Host "Press any key to close this launcher (servers will keep running in new windows)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
