@echo off
rem UTF-8 code page: the project path may contain non-Latin characters.
chcp 65001 >nul
title ConsumptionMonitor - connection check
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\test-connection.ps1"
set "EXITCODE=%ERRORLEVEL%"
if "%EXITCODE%"=="0" (
    echo.
    echo Connection check finished. Press any key to close...
    pause >nul
    exit /b 0
)
echo.
echo Connection check failed. Check the log for details:
echo   %~dp0data\launcher.log
echo.
pause
exit /b 1
