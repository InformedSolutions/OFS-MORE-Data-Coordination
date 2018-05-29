#!/bin/bash

# Migrate Django_Cron
echo "Apply database migrations"
python manage.py makemigrations django_cron --settings=$PROJECT_SETTINGS
python manage.py migrate django_cron --settings=$PROJECT_SETTINGS

# Start Cron Job defined in docker file
echo "Starting cron"
printenv > /etc/environment
nohup cron -f &

# Start server
echo "Starting server"
python manage.py runserver --settings=$PROJECT_SETTINGS 0.0.0.0:9000