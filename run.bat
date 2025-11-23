@echo off
REM Script para ejecutar el JWT Analyzer en Windows

echo ========================================
echo JWT Analyzer - Startup Script
echo ========================================
echo.

REM Verificar si existe venv
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -q flask pytest

echo.
echo ========================================
echo Opciones:
echo.
echo 1. Ejecutar aplicación web
echo 2. Ejecutar tests
echo 3. Ejecutar demostración
echo 4. Salir
echo.
set /p choice="Selecciona una opción (1-4): "

if "%choice%"=="1" (
    echo Iniciando aplicación web...
    python app.py
) else if "%choice%"=="2" (
    echo Ejecutando tests...
    python -m pytest tests/ -v
) else if "%choice%"=="3" (
    echo Ejecutando demostración...
    python demo.py
) else if "%choice%"=="4" (
    echo Saliendo...
    exit /b 0
) else (
    echo Opción no válida
    exit /b 1
)

pause
