#!/bin/sh
mysql -h db -P 3306 --protocol=tcp -u django_app -pdjango_app123 django_app < db.sql
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:3000
