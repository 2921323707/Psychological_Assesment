@echo off
chcp 65001 >nul
REM Git Update Script (Windows)
REM Quick commit and push to GitHub

echo ===============================================
echo GitHub Repository Update Script
echo ===============================================
echo.

REM Check git status
echo 1. Checking Git status...
git status

echo.
set /p confirm="Continue update? (y/n): "

if /i not "%confirm%"=="y" (
    echo Operation cancelled
    exit /b 0
)

REM Add all changes
echo.
echo 2. Adding all changes...
git add .

REM Get commit message
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "

if "%commit_msg%"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (set mydate=%%c-%%b-%%a)
    for /f "tokens=1-2 delims=: " %%a in ("%time%") do (set mytime=%%a:%%b)
    set commit_msg=Update: %mydate% %mytime%
)

REM Commit changes
echo.
echo 3. Committing changes...
echo Commit message: %commit_msg%
git commit -m "%commit_msg%"

REM Push to GitHub
echo.
echo 4. Pushing to GitHub...
git push origin main

echo.
echo ===============================================
echo Success: Update complete!
echo ===============================================
echo.
echo Repository: https://github.com/2921323707/Psychological_Assesment
echo.

pause

