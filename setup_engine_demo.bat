@echo off
setlocal
cd /d "%~dp0"

echo SO Memory Engine local setup

echo.
if not exist "..\SO_Memory_Kernel" (
  echo Missing sibling repository: ..\SO_Memory_Kernel
  echo.
  echo Expected layout:
  echo   Desktop\SO_Memory_Kernel
  echo   Desktop\SO_Memory_Engine
  echo.
  echo Clone Kernel first:
  echo   git clone https://github.com/Ika300/so-memory-kernel.git ..\SO_Memory_Kernel
  exit /b 1
)

echo Installing SO Memory Kernel...
py -3 -m pip install -e ..\SO_Memory_Kernel
if errorlevel 1 exit /b 1

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