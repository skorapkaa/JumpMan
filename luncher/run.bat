@echo off
REM Přesun do kořenového adresáře projektu
cd /d "%~dp0.."

REM Aktivace virtuálního prostředí a spuštění hry
call venv\Scripts\activate.bat
python src\main.py

pause
