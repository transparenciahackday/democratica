#!/bin/sh

python manage.py runserver &
python manage.py celeryd -v 2 -B -s celery -E -l INFO --pidfile temp.pid
