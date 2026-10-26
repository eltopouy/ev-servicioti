@echo off
chcp 65001 >nul
title EV Uruguay - Actualizar Top Ventas Mensual (ACAU / SUCIVE)

echo ==============================================================
echo 🏆 EV Uruguay - Actualizador Mensual de Líderes en Ventas
echo    Subdominio: https://ev.servicioti.com.uy
echo ==============================================================
echo.

cd /d "%~dp0"
python scripts\sync_acau_rankings.py

echo.
echo Presione una tecla para salir...
pause >nul
