@echo off
rem UTF-8 code page: the project path may contain non-Latin characters.
chcp 65001 >nul
title ConsumptionMonitor
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\launch.ps1"
set "EXITCODE=%ERRORLEVEL%"
if "%EXITCODE%"=="0" exit /b 0
echo.
echo Startup failed. Check the log for details:
echo   %~dp0data\launcher.log
echo.
pause
exit /b 1
