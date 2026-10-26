# =====================================================================
# Tarea Mensual del Programador de Tareas de Windows (ServicioTI)
# Automatización de Sincronización Mensual de Combustibles y Tarifas UTE
# =====================================================================

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$PythonExe = (Get-Command python).Source

Write-Host "=== Sincronizando Tarifario Mensual Oficial MIEM / URSEA / UTE ===" -ForegroundColor Cyan
Set-Location -Path $ProjectDir

# Ejecutar el sincronizador de tarifas
& $PythonExe "scripts\sync_fuel_tariffs.py"

Write-Host "=== Tarifas sincronizadas y datos estáticos regenerados con éxito ===" -ForegroundColor Green

# ---------------------------------------------------------------------
# Registro en el Programador de Tareas de Windows (Resiliencia Total)
# ---------------------------------------------------------------------
$TaskName = "EV_Uruguay_Sync_Mensual_Combustibles"

$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$PSScriptRoot\tarea_mensual_combustibles.ps1`""
$Trigger = New-ScheduledTaskTrigger -Monthly -DaysOfWeek Monday -At 06:00
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Actualiza mensualmente los precios oficiales de Nafta Súper 95, Premium 97, Gasoil 50-S y tarifas de UTE en EV Uruguay (ev.servicioti.com.uy)" -Force -ErrorAction SilentlyContinue | Out-Null
    Write-Host "[Programador de Tareas] Tarea '$TaskName' registrada/actualizada con -StartWhenAvailable y -WakeToRun." -ForegroundColor Green
} catch {
    Write-Host "[Aviso] No se pudo registrar en Task Scheduler sin privilegios elevados; la ejecución manual o por cron está habilitada." -ForegroundColor Yellow
}
