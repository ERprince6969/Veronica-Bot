@echo off
title Discord Bot Launcher

echo ===============================
echo   Discord Bot - Avvio
echo ===============================
echo.

:: Controllo Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Volevi installare il bot senza python?
    echo Installa Python e riprova: https://www.python.org/downloads/
    pause
    exit /b
)

echo Python rilevato
echo.

:: Controllo pip
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip non trovato.
    echo Reinstalla Python con pip incluso.
    pause
    exit /b
)

echo pip rilevato
echo.

:: Installazione requirements
IF EXIST requirements.txt (
    echo Installazione dipendenze...
    pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Errore durante installazione librerie.
        pause
        exit /b
    )
    echo Librerie installate
) ELSE (
    echo requirements.txt non trovato, salto installazione
)

echo.

:: Avvio bot
echo Avvio bot...
python bot.py

echo.
echo Il bot si e chiuso (o hai fatto casino)
pause
