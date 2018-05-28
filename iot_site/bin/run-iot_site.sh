#!/bin/sh
set -ex

cd /var/lib/iot_site
export DJANGO_SETTINGS_MODULE="iot_site.settings"
python3 -m django migrate
python3 -m django loaddata test_data
gunicorn iot_site.wsgi -b 0.0.0.0
