@echo off
rem UTF-8 code page: the project path may contain non-Latin characters.
chcp 65001 >nul
title ConsumptionMonitor - credentials
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\set-credentials.ps1"
if errorlevel 1 pause
