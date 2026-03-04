# Create GitHub repo (one click in browser) and push, fully scripted.
# 1. Opens GitHub "New repository" with name and description pre-filled.
# 2. You click "Create repository" (leave "Add a README" unchecked).
# 3. Script waits then pushes to origin using your token.
# Run from repo root: .\scripts\create_repo_and_push.ps1
# Optional: -WaitForEnter to pause until you press Enter instead of auto-waiting 25s.
param([switch]$WaitForEnter)
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot

$newRepoUrl = "https://github.com/new?name=tiger-analytics-portfolio&description=Healthcare+analytics+portfolio"
Write-Host "Opening GitHub 'New repository' page (name and description pre-filled)..."
Start-Process $newRepoUrl
Write-Host "In the browser: click the green 'Create repository' button (leave 'Add a README' unchecked)."
if ($WaitForEnter) {
    $null = Read-Host "Press Enter after you have created the repository"
} else {
    Write-Host "Waiting 25 seconds for you to create the repo..."
    Start-Sleep -Seconds 25
}
Write-Host "Pushing to origin..."
& (Join-Path $PSScriptRoot "push_to_github.ps1")
Write-Host "Done."
