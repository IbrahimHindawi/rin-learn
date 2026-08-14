$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$OutDir = Join-Path $Root "build\gen"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$IExe = $null
if ($env:I_HOME) {
    $candidate = Join-Path $env:I_HOME "I.exe"
    if (Test-Path $candidate) {
        $IExe = $candidate
    }
}

if (-not $IExe) {
    $cmd = Get-Command I.exe -ErrorAction SilentlyContinue
    if ($cmd) {
        $IExe = $cmd.Source
    }
}

if (-not $IExe) {
    $candidate = "C:\devel\i-windows-x64\I.exe"
    if (Test-Path $candidate) {
        $IExe = $candidate
    }
}

if (-not $IExe) {
    throw "Could not find I.exe. Set I_HOME or put I.exe on PATH."
}

Write-Host "compiler: $IExe"

$Lessons = Get-ChildItem -Path (Join-Path $Root "src\lessons") -Filter "*.i" | Sort-Object Name
foreach ($lesson in $Lessons) {
    $base = [System.IO.Path]::GetFileNameWithoutExtension($lesson.Name)
    $outC = Join-Path $OutDir ($base + ".c")
    $outH = Join-Path $OutDir ($base + ".h")
    Write-Host "compile $($lesson.Name)"
    & $IExe compile $lesson.FullName -o $outC --header $outH
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Write-Host "ok $($Lessons.Count) lessons"

