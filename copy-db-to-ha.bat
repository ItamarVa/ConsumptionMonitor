@echo off
rem UTF-8 code page: the project path may contain non-Latin characters.
chcp 65001 >nul
title ConsumptionMonitor - copy database to Home Assistant
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\copy-db-to-ha.ps1"
set "EXITCODE=%ERRORLEVEL%"
if "%EXITCODE%"=="0" (
    echo.
    echo Copy finished. Press any key to close...
    pause >nul
    exit /b 0
)
echo.
echo Copy failed. Check the log for details:
echo   %~dp0data\launcher.log
echo.
pause
exit /b 1
