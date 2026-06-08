#!/usr/bin/env bash
set -o errexit

pip install poetry
poetry install --no-root --no-interaction --no-ansi

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@lacreisaude.com.br', 'admin123')
"
