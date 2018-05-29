#!/bin/sh
set -ex

cd /var/lib/iot_site
export DJANGO_SETTINGS_MODULE="iot_site.settings"
django-admin migrate
django-admin loaddata test_data
django-admin runserver 0.0.0.0:8000

gunicorn iot_site.wsgi -b 0.0.0.0
