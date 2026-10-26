# PowerShell Script para Automatización Mensual de Rankings EV Uruguay (ev.servicioti.com.uy)
# Ejecuta la sincronización de empadronamientos de ACAU/SUCIVE y actualiza el top de la web.
[CmdletBinding()]
param (
    [switch]$RegisterTask
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Split-Path -Parent $ScriptDir
$PythonExe = (Get-Command python).Source

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "⚡ EV Uruguay - Actualizador Mensual de Top Ventas (ACAU)" -ForegroundColor Cyan
Write-Host "   Subdominio: https://ev.servicioti.com.uy" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if ($RegisterTask) {
    Write-Host "[Scheduler] Registrando tarea periódica en el Programador de Tareas de Windows..." -ForegroundColor Yellow
    $TaskName = "EV_Uruguay_Top_Ventas_Mensual"
    $Action = New-ScheduledTaskAction -Execute "$PythonExe" -Argument "scripts\sync_acau_rankings.py" -WorkingDirectory "$BaseDir"
    
    # Se programa para ejecutarse el día 5 de cada mes a las 09:00 AM (cuando ACAU publica las estadísticas de cierre)
    $Trigger = New-ScheduledTaskTrigger -Monthly -DaysOfMonth 5 -At 9:00am
    
    # Configuración de resiliencia según estándares de Andrés / ServicioTI
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun
    
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Actualiza mensualmente los empadronamientos y modelos EV más vendidos en Uruguay para ev.servicioti.com.uy" -Force
    Write-Host "[Scheduler] Tarea '$TaskName' programada con éxito con WakeToRun y StartWhenAvailable." -ForegroundColor Green
    return
}

# Ejecución inmediata
Set-Location -Path $BaseDir
Write-Host "[Ejecución] Iniciando sincronizador de rankings..." -ForegroundColor Green
& "$PythonExe" "scripts\sync_acau_rankings.py"

Write-Host "`n[Finalizado] Rankings actualizados y portada re-generada con los líderes en ventas." -ForegroundColor Green
