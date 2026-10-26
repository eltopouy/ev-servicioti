# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Tarea Programada de Windows para Sincronización Mensual de TCO, Patente SUCIVE, Seguro BSE y Service Oficial
.DESCRIPTION
    Ejecuta el primer día hábil de cada mes para mantener al día los cálculos financieros de EV Uruguay (ev.servicioti.com.uy).
    Cumple con las reglas de resiliencia de Andrés (ServicioTI): -StartWhenAvailable, -WakeToRun, codificación UTF-8.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$TaskName = "EV_Uruguay_Sync_TCO_Mensual"
$WorkingDir = "$env:USERPROFILE\.gemini\antigravity\scratch\ev_servicioti"
$PythonPath = "python"
$ScriptPath = "$WorkingDir\scripts\sync_tco_parameters.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Configurando Tarea Programada: $TaskName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`"" -WorkingDirectory $WorkingDir

# Disparador: Día 1 de cada mes a las 04:30 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At "04:30AM"

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Actualización mensual automática de TCO, Patente SUCIVE y Seguros para EV Uruguay (ev.servicioti.com.uy)"
    Write-Host "[OK] Tarea programada registrada exitosamente: $TaskName" -ForegroundColor Green
} catch {
    Write-Host "[AVISO] No se pudo registrar en Windows Task Scheduler (requiere elevación): $_" -ForegroundColor Yellow
}
