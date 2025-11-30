@echo off
set GIT_PAGER=
echo Resolving merge conflicts...
git rm -f "hrmsproject/approval/__pycache__/urls.cpython-310.pyc" 2>nul
git rm -f "hrmsproject/approval/__pycache__/views.cpython-310.pyc" 2>nul

echo.
echo Staging all changes...
git add -A

echo.
echo Committing changes...
git commit -m "Restructure templates to app-level and update views"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Done!
pause

