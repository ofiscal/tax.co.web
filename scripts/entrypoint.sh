#!/bin/sh

#if there are any errors just exit the script
set -e
#collect all the static files put them in the static root
python manage.py collectstatic --noinput
# runs our application with uWSGI. wanna run it as a socket in tcp port 8000
# master runs it in foreground, enable multi threads, creates a file with wsgi
# found in django/ebdjango/wsgi.py
uwsgi --socket :8000 --master --enable-threads --module ebdjango.wsgi
