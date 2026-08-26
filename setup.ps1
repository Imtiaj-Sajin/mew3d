# Mew3D one-command setup for a fresh Windows PC.
#   Requirements: Python 3.11+, an NVIDIA GPU (6GB+ VRAM recommended)
#   Usage: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== Mew3D setup ==" -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "creating virtual environment..."
    python -m venv .venv
}

$py = ".\.venv\Scripts\python.exe"

Write-Host "installing CUDA PyTorch (large download)..."
& $py -m pip install --upgrade pip --quiet
& $py -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

Write-Host "installing dependencies..."
& $py -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "NOTE: created .env from template - add your OPENAI_API_KEY to it" -ForegroundColor Yellow
}

Write-Host "prefetching model weights (~4.5GB, resumable - rerun if interrupted)..."
& $py scripts\prefetch_models.py

Write-Host "running environment check..."
& $py -m mew3d doctor

Write-Host "== done. try: .venv\Scripts\python.exe -m mew3d generate --text `"a red apple`" ==" -ForegroundColor Green
