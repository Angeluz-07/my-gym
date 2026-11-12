#!/bin/sh

echo "1. Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

echo "2. Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "3. Iniciando Gunicorn para producción..."
# Reemplaza 'mi_proyecto.wsgi:application' por el nombre real de tu módulo wsgi
exec gunicorn mygym.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -