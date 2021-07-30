#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate

python manage.py createsuperuser_if_none_exist --user=admin --password=password

python manage.py usergroup --user=admin1 --group=adminGroup
python manage.py usergroup --user=user1 --group=userGroup

uwsgi --socket :8000 --master --enable-threads --module Project.wsgi
