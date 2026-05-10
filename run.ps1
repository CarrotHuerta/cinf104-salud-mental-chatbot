$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Load-DotEnv($path) {
    if (-not (Test-Path $path)) {
        return
    }

    Get-Content $path | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) {
            return
        }
        $parts = $line.Split("=", 2)
        if ($parts.Count -ne 2) {
            return
        }
        $name = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"')
        $env:$name = $value
    }
}

Load-DotEnv (Join-Path $Root ".env")

if (-not $env:OLLAMA_BASE_URL) {
    $env:OLLAMA_BASE_URL = "http://localhost:11434"
}
if (-not $env:OLLAMA_MODEL) {
    $env:OLLAMA_MODEL = "llama3.2:1b"
}

$ollamaExe = $env:OLLAMA_EXE
if ([string]::IsNullOrWhiteSpace($ollamaExe)) {
    if ($env:LOCALAPPDATA) {
        $ollamaExe = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
    }
}

$ollamaCmd = $null
if ($ollamaExe -and (Test-Path $ollamaExe)) {
    $ollamaCmd = $ollamaExe
} else {
    $cmd = Get-Command ollama -ErrorAction SilentlyContinue
    if ($cmd) {
        $ollamaCmd = $cmd.Source
    }
}

if (-not $ollamaCmd) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "Installing Ollama..."
        winget install -e --id Ollama.Ollama
        $ollamaCmd = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
    } else {
        Write-Host "Ollama not found. Install it from https://ollama.com/."
        exit 1
    }
}

Write-Host "Pulling model $env:OLLAMA_MODEL ..."
& $ollamaCmd pull $env:OLLAMA_MODEL

$venvPath = Join-Path $Root ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        & py -3 -m venv $venvPath
    } else {
        $python = Get-Command python -ErrorAction SilentlyContinue
        if (-not $python) {
            Write-Host "Python not found. Install Python 3.10+."
            exit 1
        }
        & $python.Source -m venv $venvPath
    }
}

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "Starting app..."
& $venvPython -m streamlit run app.py
