# Push portfolio to GitHub using token from parent folder.
# Run from repo root: .\scripts\push_to_github.ps1
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path $PSScriptRoot -Parent
$tokenPath = Join-Path (Split-Path $repoRoot -Parent) "tiger_git_token.txt"
if (-not (Test-Path $tokenPath)) { throw "Token file not found: $tokenPath" }
$token = (Get-Content $tokenPath -Raw).Trim()
Set-Location $repoRoot

git add -A
git status -s
$status = git status --porcelain
if ($status) {
    git commit -m "Initial portfolio: healthcare mock data, Python/R/SQL, readmission model"
}
git branch -M main

$remoteUrl = "https://${token}@github.com/prendleman/tiger-analytics-portfolio.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
git push -u origin main
# Remove token from stored URL so it is not persisted in .git/config
git remote set-url origin "https://github.com/prendleman/tiger-analytics-portfolio.git"
Write-Host "Push complete. Remote origin set to public URL (token not stored)."
