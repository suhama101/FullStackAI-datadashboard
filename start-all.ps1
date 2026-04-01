$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
$frontendDir = Join-Path $root "frontend"

if (!(Test-Path $venvPython)) {
  Write-Host "Warning: venv Python not found at $venvPython" -ForegroundColor Yellow
  Write-Host "Backend will try system Python. To avoid issues, create/activate .venv first." -ForegroundColor Yellow
}

$backendCommand = @(
  "cd '$root'"
  "if (Test-Path '$venvPython') { `$env:PYTHON_PATH = '$venvPython' }"
  "npm start"
) -join "; "

$frontendCommand = @(
  "cd '$frontendDir'"
  "npm run dev"
) -join "; "

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand | Out-Null
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand | Out-Null

Write-Host "Started backend and frontend in separate terminals."
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend:  http://localhost:5000"
