# Resolve merge conflicts and push changes
$ErrorActionPreference = "Stop"

Write-Host "Step 1: Resolving merge conflicts..." -ForegroundColor Yellow
git rm -f hrmsproject/approval/__pycache__/urls.cpython-310.pyc 2>&1 | Out-Null
git rm -f hrmsproject/approval/__pycache__/views.cpython-310.pyc 2>&1 | Out-Null

Write-Host "Step 2: Staging all changes..." -ForegroundColor Yellow
git add -A

Write-Host "Step 3: Current status:" -ForegroundColor Yellow
git status --short

Write-Host "`nStep 4: Committing changes..." -ForegroundColor Yellow
git commit -m "Restructure templates to app-level and update views"

Write-Host "Step 5: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "`nDone! Changes pushed successfully." -ForegroundColor Green

