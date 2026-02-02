@echo off
echo === Configuracion Automatica del Sistema de Analisis de Credito ===

:: 1. Verificar si existe Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 'python' no encontrado. Probando con 'py'...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] No se encontro Python instalado.
        echo Por favor instala Python desde python.org y asegura marcar "Add to PATH".
        pause
        exit /b
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo [OK] Usando: %PYTHON_CMD%

:: 2. Instalar Librerias
echo.
echo [1/2] Instalando librerias desde requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de librerias.
    pause
    exit /b
)

:: 3. Generar Datos
echo.
echo [2/2] Generando datos de prueba...
%PYTHON_CMD% tools/generate_dummy_data.py

echo.
echo === !Listo! ===
echo Para correr el programa usa este comando:
echo %PYTHON_CMD% main.py
echo.
pause
