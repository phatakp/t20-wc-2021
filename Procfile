release: python manage.py migrate --noinput
web: gunicorn project_worldcup.wsgi --timeout 15 --keep-alive 5 --log-level debug --log-file -