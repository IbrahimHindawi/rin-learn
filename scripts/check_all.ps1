$ErrorActionPreference = "Stop"

# Compiles, links and *runs* every lesson.
#
# Compiling was the old bar, and it is the wrong one for a teaching repo: a
# lesson that builds and then crashes teaches the reader that they broke it.
# Output is not compared against a fixture, because several lessons print
# addresses and those change every run. The bar is: it builds, it runs, it
# exits 0.

$Root = Split-Path -Parent $PSScriptRoot
$OutDir = Join-Path $Root "build\gen"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$IExe = $null
if ($env:RIN_HOME) {
    $candidate = Join-Path $env:RIN_HOME "rin.exe"
    if (Test-Path $candidate) {
        $IExe = $candidate
    }
}

if (-not $IExe) {
    $cmd = Get-Command rin.exe -ErrorAction SilentlyContinue
    if ($cmd) {
        $IExe = $cmd.Source
    }
}

if (-not $IExe) {
    $candidate = "C:\devel\rin-windows-x64\rin.exe"
    if (Test-Path $candidate) {
        $IExe = $candidate
    }
}

if (-not $IExe) {
    throw "Could not find rin.exe. Set RIN_HOME or put rin.exe on PATH."
}

$RinHome = Split-Path -Parent $IExe
$StdDir = Join-Path $RinHome "std"

# A C compiler is optional. Without one the lessons are still checked for
# compiling, which is what this script used to do on its own.
$CC = $null
foreach ($name in @("clang.exe", "clang", "cl.exe")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { $CC = $cmd.Source; break }
}

Write-Host "compiler: $IExe"
if ($CC) {
    Write-Host "C backend: $CC"
} else {
    Write-Host "C backend: none found, lessons will be compiled but not run"
}

$Lessons = Get-ChildItem -Path (Join-Path $Root "src\lessons") -Filter "*.rin" | Sort-Object Name
$Ran = 0
$Failures = @()

foreach ($lesson in $Lessons) {
    $base = [System.IO.Path]::GetFileNameWithoutExtension($lesson.Name)
    $outC = Join-Path $OutDir ($base + ".c")
    $outH = Join-Path $OutDir ($base + ".h")
    Write-Host "compile $($lesson.Name)"
    & $IExe compile $lesson.FullName -o $outC --header $outH
    if ($LASTEXITCODE -ne 0) {
        $Failures += "$($lesson.Name): rin rejected it"
        continue
    }

    if (-not $CC) { continue }

    $exe = Join-Path $OutDir ($base + ".exe")
    # Native stderr becomes a terminating error under ErrorActionPreference
    # Stop in PowerShell 5.1, and lesson 09 emits a warning on purpose. The
    # exit code is what actually decides success here.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    if ($CC -like "*cl.exe") {
        & $CC /nologo /I $RinHome /I $StdDir $outC "/Fe:$exe" "/Fo:$OutDir\$base.obj" | Out-Null
    } else {
        & $CC $outC -I $RinHome -I $StdDir -o $exe | Out-Null
    }
    $ErrorActionPreference = $previous
    if ($LASTEXITCODE -ne 0) {
        $Failures += "$($lesson.Name): the generated C did not build"
        continue
    }

    & $exe | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $Failures += "$($lesson.Name): exited $LASTEXITCODE"
        continue
    }
    $Ran += 1
}

if ($Failures.Count -gt 0) {
    Write-Host ""
    Write-Host "failures:"
    foreach ($failure in $Failures) { Write-Host "  $failure" }
    exit 1
}

if ($CC) {
    Write-Host "ok $($Lessons.Count) lessons compiled, $Ran ran cleanly"
} else {
    Write-Host "ok $($Lessons.Count) lessons compiled"
}
