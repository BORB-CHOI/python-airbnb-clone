#!/bin/sh
source /var/app/venv/*/bin/activate
python3 manage.py migrate --noinput
python3 manage.py compilemessages