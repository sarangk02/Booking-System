#!/bin/sh

set -e

python manage.py migrate
python manage.py collectstatic --noinput

echo "creating superuser with username admin and enter password when prompted"
python manage.py createsuperuser --username admin