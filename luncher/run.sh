#!/usr/bin/env bash
# Pavel Hrdina 2025

# Přesun do kořenového adresáře projektu (tento skript je v luncher/)
cd "$(dirname "$0")/.." || exit

# Aktivace virtuálního prostředí
source venv/bin/activate

# Spuštění hry
python src/main.py
