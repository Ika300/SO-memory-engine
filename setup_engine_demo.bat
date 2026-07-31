@echo off
setlocal
cd /d "%~dp0"

echo SO Memory Engine local setup

echo.
echo Installing SO Memory Engine...
py -3 -m pip install -e .
if errorlevel 1 exit /b 1

echo.
echo Running Engine-only quickstart...
py -3 quickstart.py
if errorlevel 1 exit /b 1

echo.
echo Done.
echo Open outputs\engine_quickstart\context_pack.txt
endlocal