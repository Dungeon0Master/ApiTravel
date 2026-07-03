#!/usr/bin/env bash
# build.sh — Script de construcción para Render
# Render lo ejecuta automáticamente antes de iniciar el servidor.

set -o errexit   # Abortar si cualquier comando falla

pip install --upgrade pip
pip install -r requirements.txt

# Recopilar archivos estáticos (necesario para WhiteNoise)
python manage.py collectstatic --no-input
