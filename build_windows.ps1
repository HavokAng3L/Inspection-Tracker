$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
py -3.13 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "Install Python 3.13 to build the executable." }
& .\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
$env:QT_QPA_PLATFORM = "offscreen"
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Desktop tests failed." }
Remove-Item Env:QT_QPA_PLATFORM
& .\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name InspectionTracker main.py
if ($LASTEXITCODE -ne 0) { throw "Executable build failed." }
Write-Host "Built dist\InspectionTracker.exe"
