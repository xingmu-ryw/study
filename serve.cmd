@echo off
setlocal
set ROOT=%~dp0
if "%FASTAPI_PROJECT_PORT%"=="" set FASTAPI_PROJECT_PORT=8001
if exist "%ROOT%\.venv\Scripts\python.exe" (
  "%ROOT%\.venv\Scripts\python.exe" "%ROOT%\dev_server.py" %*
) else (
  python "%ROOT%\dev_server.py" %*
)
