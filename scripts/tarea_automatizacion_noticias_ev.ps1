# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Script de Automatización y Tarea Programada para EV Uruguay (ev.servicioti.com.uy)
    Servicio: Actualizador Automático de Noticias, Crónicas 100% BEV y Sincronización Blogger.
    Autor: Andrés Franchi Ugartemendía (ServicioTI)

.DESCRIPTION
    Configura y ejecuta la tarea periódica en el Programador de Tareas de Windows (Task Scheduler)
    utilizando parámetros de máxima resiliencia (-StartWhenAvailable, -WakeToRun),
    asegurando la extracción continua de novedades 100% eléctricas a batería (BEV),
    el filtrado de competidores, la generación de crónicas y la publicación en Blogger.

.PARAMETER RegisterTask
    Registra o actualiza la tarea en el Programador de Tareas de Windows.

.PARAMETER UnregisterTask
    Elimina la tarea programada del sistema.

.PARAMETER RunNow
    Ejecuta inmediatamente el ciclo de actualización de noticias.

.EXAMPLE
    .\tarea_automatizacion_noticias_ev.ps1 -RegisterTask
    .\tarea_automatizacion_noticias_ev.ps1 -RunNow
#>

[CmdletBinding()]
param (
    [switch]$RegisterTask,
    [switch]$UnregisterTask,
    [switch]$RunNow,
    [string]$TaskName = "EV_Uruguay_Auto_News_Updater"
)

# Si no se pasó RegisterTask ni UnregisterTask, ejecutar el ciclo de actualización
if (-not $RegisterTask -and -not $UnregisterTask) {
    $RunNow = $true
}

# 1. Configurar codificación UTF-8 para consola Windows y caracteres especiales (Andrés)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
try { chcp 65001 > $null } catch { }

# 2. Rutas seguras y resolución de entorno
$BaseDir = Resolve-Path "$PSScriptRoot\.."
if (-not $BaseDir -or -not (Test-Path "$BaseDir\scripts\auto_news_updater.py")) {
    $BaseDir = "$env:USERPROFILE\.gemini\antigravity\scratch\ev_servicioti"
}

$PythonScript = "$BaseDir\scripts\auto_news_updater.py"
$PythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
if (-not $PythonExe) {
    $PythonExe = "python.exe"
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "⚡ TAREA PROGRAMADA: ACTUALIZADOR DE NOTICIAS EV URUGUAY (ServicioTI)" -ForegroundColor Cyan
Write-Host "   Directorio Base : $BaseDir" -ForegroundColor Gray
Write-Host "   Script Python   : $PythonScript" -ForegroundColor Gray
Write-Host "=====================================================================" -ForegroundColor Cyan

# 3. Eliminar tarea si se solicita
if ($UnregisterTask) {
    Write-Host "`n[Tarea] Desregistrando tarea programada '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "[Tarea] ✔ Tarea '$TaskName' eliminada correctamente." -ForegroundColor Green
    return
}

# 4. Registrar tarea en el Programador de Tareas de Windows
if ($RegisterTask) {
    Write-Host "`n[Tarea] Registrando tarea periódica en Windows Task Scheduler..." -ForegroundColor Yellow
    
    # Acción: Ejecutar python con auto_news_updater.py en el directorio de trabajo correcto
    $Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$PythonScript`"" -WorkingDirectory $BaseDir

    # Disparadores: Tres ejecuciones diarias (08:00, 14:00 y 20:00) para máxima frescura editorial
    $Trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00AM"
    $Trigger2 = New-ScheduledTaskTrigger -Daily -At "02:00PM"
    $Trigger3 = New-ScheduledTaskTrigger -Daily -At "08:00PM"
    $Triggers = @($Trigger1, $Trigger2, $Trigger3)

    # Parámetros de resiliencia obligatorios según regla de ecosistema ServicioTI:
    # -StartWhenAvailable: Ejecuta de inmediato si el equipo estaba apagado a la hora del trigger.
    # -WakeToRun: Despierta al equipo si está en suspensión.
    $Settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -WakeToRun `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 20) `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 5)

    # Registrar la tarea en el contexto del usuario actual
    try {
        Register-ScheduledTask `
            -TaskName $TaskName `
            -Action $Action `
            -Trigger $Triggers `
            -Settings $Settings `
            -Description "Actualizador Automático de Noticias, Crónicas 100% BEV y Sincronización Blogger para EV Uruguay (https://ev.servicioti.com.uy - Andrés Franchi Ugartemendía)." `
            -Force | Out-Null

        Write-Host "[Tarea] ✔ Tarea programada '$TaskName' registrada exitosamente." -ForegroundColor Green
        Write-Host "        - Intervalo: Cada $IntervalHours horas" -ForegroundColor Gray
        Write-Host "        - Parámetros: StartWhenAvailable=True, WakeToRun=True" -ForegroundColor Gray
    } catch {
        Write-Host "[Tarea] ⚠ No se pudo registrar la tarea (requiere permisos de usuario/admin): $_" -ForegroundColor Red
    }
}

# 5. Ejecutar ciclo ahora si se especifica
if ($RunNow) {
    Write-Host "`n[Ejecución] Iniciando ciclo de actualización inmediata..." -ForegroundColor Yellow
    Set-Location $BaseDir
    & $PythonExe "$PythonScript"
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        Write-Host "`n[Ejecución] ✔ Actualización de noticias completada con éxito (ExitCode: 0)." -ForegroundColor Green
    } else {
        Write-Host "`n[Ejecución] ❌ Ocurrió un error en la ejecución (ExitCode: $exitCode)." -ForegroundColor Red
    }
}
