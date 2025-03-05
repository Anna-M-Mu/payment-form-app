#!/bin/bash

python manage.py migrate --noinput

exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
