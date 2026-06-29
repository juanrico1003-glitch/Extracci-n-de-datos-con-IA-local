@echo off
:: Cambia la ubicación al lugar donde está el script (opcional, pero recomendado)
cd /d "%~dp0"

echo --- Iniciando extraccion de datos ---
echo.

:: Ejecuta el script de Python
python procesador.py

echo.
echo --- Proceso finalizado con exito ---
pause