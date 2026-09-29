# check_prereqs.ps1 — verify the Tutorial #5 toolchain on Windows 11
# Usage:  powershell -ExecutionPolicy Bypass -File starter\scripts\check_prereqs.ps1

$ok = $true
function Test-Tool($name, $cmd, $hint) {
    $found = Get-Command $name -ErrorAction SilentlyContinue
    if ($found) {
        $v = (& $name $cmd 2>&1 | Select-Object -First 1)
        Write-Host ("[ OK ] {0,-8} {1}" -f $name, $v) -ForegroundColor Green
        return $v
    } else {
        Write-Host ("[MISS] {0,-8} -> {1}" -f $name, $hint) -ForegroundColor Red
        $script:ok = $false
        return $null
    }
}

Test-Tool git    "--version" "winget install --id Git.Git -e" | Out-Null
$node = Test-Tool node "--version" "winget install --id OpenJS.NodeJS -e"
Test-Tool ffmpeg "-version"  "winget install --id Gyan.FFmpeg -e" | Out-Null
Test-Tool bun    "--version" 'powershell -c "irm bun.sh/install.ps1 | iex"' | Out-Null
Test-Tool claude "--version" "Install Claude Code; if installed, add %LOCALAPPDATA%\Microsoft\WinGet\Links to PATH" | Out-Null

if ($node -and ($node -match 'v(\d+)\.') -and ([int]$Matches[1] -lt 22)) {
    Write-Host "[WARN] Node.js $node is older than 22 - HyperFrames needs 22+" -ForegroundColor Yellow
    $ok = $false
}

if (Test-Path "$HOME\.claude\skills\gstack") {
    Write-Host "[ OK ] gstack   found in ~/.claude/skills/gstack" -ForegroundColor Green
} else {
    Write-Host "[MISS] gstack   -> paste the install line from TUTORIAL.md 1.2 into Claude Code" -ForegroundColor Red
    $ok = $false
}

if ($ok) { Write-Host "`nAll prerequisites present. Next: TUTORIAL.md 1.3 (HyperFrames)." -ForegroundColor Cyan }
else     { Write-Host "`nFix the items above, open a NEW PowerShell, and run this again." -ForegroundColor Yellow }
