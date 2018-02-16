# Migrate Django_Cron
echo "Apply database migrations"
python manage.py migrate django_cron

# Start Cron Job defined in docker file
echo "Starting cron"
cron && tail -f /var/log/cron.log

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:9000