@echo off
setlocal

cd /d "%~dp0"

echo SO Memory Engine + Extractor Free setup
echo =======================================
echo.

if not exist "..\SO_Memory_Kernel" (
  echo ERROR: SO_Memory_Kernel was not found next to this repository.
  echo.
  echo Expected layout:
  echo   Desktop\SO_Memory_Kernel
  echo   Desktop\SO_Memory_Engine
  echo.
  echo Clone it first:
  echo   git clone https://github.com/Ika300/so-memory-kernel.git ..\SO_Memory_Kernel
  echo.
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
echo Installing SO Extractor Free...
py -3 -m pip install -e SO_Extractor_Free
if errorlevel 1 exit /b 1

echo.
echo Running complete free quickstart...
py -3 quickstart.py
if errorlevel 1 exit /b 1

echo.
echo Done.
echo Open outputs\free_trial\07_context_pack.txt