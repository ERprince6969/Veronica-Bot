@echo off
chcp 65001 >nul
title Discord Bot Launcher

echo ===============================
echo   Discord Bot - Avvio
echo ===============================
echo.

:: Controllo Python e pip in un unico passaggio
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Python non trovato. Installalo da: https://www.python.org/downloads/
    pause
    exit /b 1
)

python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] pip non trovato. Reinstalla Python includendo pip.
    pause
    exit /b 1
)

:: Installazione veloce e silenziosa delle dipendenze
IF EXIST requirements.txt (
    echo Verifica dipendenze in corso...
    python -m pip install -q -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERRORE] Installazione librerie fallita.
        pause
        exit /b 1
    )
    echo Librerie pronte.
) ELSE (
    echo [AVVISO] requirements.txt non trovato, salto installazione.
)

echo.
echo Avvio bot...
python bot.py

echo.
echo Il bot si è chiuso (o hai fatto casino).
pause
