@echo off
chcp 65001 >nul
title EV Uruguay - Colector de Datos (ev.servicioti.com.uy)

echo ==============================================================
echo ⚡ EV Uruguay - Radar de Movilidad Eléctrica
echo    Subdominio: https://ev.servicioti.com.uy
echo ==============================================================
echo.

cd /d "%~dp0"
python scripts\run_all_collectors.py

echo.
echo Presione una tecla para salir...
pause >nul
