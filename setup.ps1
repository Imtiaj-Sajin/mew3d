# Mew3D one-command setup for a fresh Windows PC.
#   Requirements: Python 3.11+, an NVIDIA GPU (6GB+ VRAM recommended)
#   Usage: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== Mew3D setup ==" -ForegroundColor Cyan

$pyver = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($pyver -ne "3.11") {
    Write-Host "WARNING: Python 3.11 is required (found $pyver) - the texture stage's" -ForegroundColor Yellow
    Write-Host "         custom_rasterizer wheel is built for cp311." -ForegroundColor Yellow
}

if (-not (Test-Path ".venv")) {
    Write-Host "creating virtual environment..."
    python -m venv .venv
}

$py = ".\.venv\Scripts\python.exe"

Write-Host "installing CUDA PyTorch (large download)..."
& $py -m pip install --upgrade pip --quiet
# torch is pinned to 2.5.1: the vendored custom_rasterizer wheel (texture stage)
# is ABI-linked against it - torch 2.6+ breaks the import
& $py -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124

Write-Host "installing dependencies..."
& $py -m pip install -r requirements.txt
& $py -m pip install (Get-Item "third_party\wheels\custom_rasterizer-*.whl").FullName

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "NOTE: created .env from template - add your OPENAI_API_KEY to it" -ForegroundColor Yellow
}

Write-Host "prefetching model weights (~4.5GB, resumable - rerun if interrupted)..."
& $py scripts\prefetch_models.py

Write-Host "running environment check..."
& $py -m mew3d doctor

Write-Host "== done. try: .venv\Scripts\python.exe -m mew3d generate --text `"a red apple`" ==" -ForegroundColor Green
