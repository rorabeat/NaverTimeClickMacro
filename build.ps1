# PyInstaller 빌드 전, 빌드에 쓰는 Python에 requirements 설치 필요
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) {
    throw "python 을 PATH에서 찾을 수 없습니다."
}

Write-Host "Using: $py"
& $py -m pip install -r requirements.txt
& $py -m PyInstaller --noconfirm NaverTimeClickMacro.spec
Write-Host "Done: dist\NaverTimeClickMacro.exe"
