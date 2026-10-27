# -*- coding: utf-8 -*-
# ==============================================================================
# Tarea Automatizada de Inteligencia de Mercado, Precios y Homologaciones EV Uruguay
# Subdominio: https://ev.servicioti.com.uy
# Autor: Andrés Franchi Ugartemendía (ServicioTI)
# ==============================================================================

# Configurar codificación UTF-8 para consola y logs
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 >$null

$baseDir = "$env:USERPROFILE\.gemini\antigravity\scratch\ev_servicioti"
$scriptPath = "$baseDir\scripts\orchestrator_ev_intelligence.py"
$logDir = "$baseDir\logs"
$logFile = "$logDir\ev_intelligence_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Crear directorio de logs si no existe
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "🚗 Iniciando Tarea Programada de Inteligencia EV Uruguay" -ForegroundColor Green
Write-Host "Fecha y Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "Log de Ejecución: $logFile" -ForegroundColor Gray
Write-Host "=================================================================" -ForegroundColor Cyan

# Ejecutar el orquestador central con Python
try {
    & python $scriptPath *>&1 | Tee-Object -FilePath $logFile
    Write-Host "`n✔ Ejecución completada con éxito." -ForegroundColor Green
} catch {
    Write-Host "`n❌ Error durante la ejecución del pipeline: $_" -ForegroundColor Red
    Add-Content -Path $logFile -Value "`n[ERROR CRÍTICO] $_"
}

# ------------------------------------------------------------------------------
# Comandos de instalación y registro en el Programador de Tareas de Windows:
# (Para registrarla como tarea periódica con resiliencia -StartWhenAvailable y -WakeToRun):
#
# $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$baseDir\scripts\tarea_inteligencia_mercado_ev.ps1`""
# $trigger = New-ScheduledTaskTrigger -Daily -At 07:00
# $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -DontStopIfGoingOnBatteries
# Register-ScheduledTask -TaskName "EV_Uruguay_Inteligencia_Mercado" -Action $action -Trigger $trigger -Settings $settings -Description "Monitoreo diario de precios, homologaciones URSEA y novedades para EV Uruguay" -User "$env:USERNAME" -Force
# ------------------------------------------------------------------------------
