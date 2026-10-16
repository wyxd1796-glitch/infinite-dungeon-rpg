@echo off
setlocal
cd /d "%~dp0"
set "GAME_LOG=%~dp0startup-%RANDOM%.log"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py > "%GAME_LOG%" 2>&1
) else (
    python main.py > "%GAME_LOG%" 2>&1
)
if errorlevel 1 (
    type "%GAME_LOG%"
    echo.
    echo Game failed to start. See %GAME_LOG%
    pause
)
