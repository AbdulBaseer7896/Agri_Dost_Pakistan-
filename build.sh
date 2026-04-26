#!/usr/bin/env bash
# Render.com build script
# This runs once per deploy, before the start command

set -o errexit  # exit on error

echo "==> Installing Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files"
python manage.py collectstatic --no-input

echo "==> Running database migrations"
python manage.py makemigrations api --no-input
python manage.py migrate --no-input

echo "==> Build complete!"
