release: python manage.py migrate --no-input
release: python manage.py loaddata initial_data.json
web  gunicorn -w ${WEB_CONCURRENCY:-5} --max-requests ${MAX_REQUESTS:-1200} api.wsgi --log-file -
