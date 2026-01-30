# Check for Python
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# Check for Node/npm
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: npm (Node.js) is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

$root = Get-Location

# Backend Setup
Write-Host "Setting up Backend..." -ForegroundColor Cyan
if (-not (Test-Path "$root\backend\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv "$root\backend\venv"
}

# Activate venv and install requirements
# We combine commands to run in the venv context
$backendCmd = "
cd '$root\backend';
.\venv\Scripts\Activate.ps1;
pip install -r requirements.txt;
python app.py;
"

# Frontend Setup
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
# Install dependencies if node_modules missing
if (-not (Test-Path "$root\frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..."
    Push-Location "$root\frontend"
    npm install
    Pop-Location
}

$frontendCmd = "
cd '$root\frontend';
npm run dev;
"

# Start Backend in new window
Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

# Start Frontend in new window
Write-Host "Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "Project started! formatting windows..."
