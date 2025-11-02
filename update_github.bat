@echo off
REM Git 更新仓库脚本 (Windows版本)
REM 用于快速提交和推送代码到GitHub

echo ===============================================
echo GitHub 仓库更新脚本
echo ===============================================
echo.

REM 检查git状态
echo 1. 检查Git状态...
git status

echo.
set /p confirm="是否继续更新? (y/n): "

if /i not "%confirm%"=="y" (
    echo 操作已取消
    exit /b 0
)

REM 添加所有更改
echo.
echo 2. 添加所有更改...
git add .

REM 获取提交信息
echo.
set /p commit_msg="请输入提交信息 (或按回车使用默认): "

if "%commit_msg%"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (set mydate=%%c-%%b-%%a)
    for /f "tokens=1-2 delims=: " %%a in ("%time%") do (set mytime=%%a:%%b)
    set commit_msg=Update: %mydate% %mytime%
)

REM 提交更改
echo.
echo 3. 提交更改...
echo 提交信息: %commit_msg%
git commit -m "%commit_msg%"

REM 推送到远程仓库
echo.
echo 4. 推送到GitHub...
git push origin main

echo.
echo ===============================================
echo ✅ 更新完成！
echo ===============================================
echo.
echo 仓库地址: https://github.com/2921323707/Psychological_Assesment
echo.

pause

