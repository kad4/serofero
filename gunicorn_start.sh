#!/bin/bash
 
NAME="serofero" # Name of the application
DJANGODIR=/home/diwas/serofero # Django project directory
BINDIP=127.0.0.1:8000 # bind gunicorn to this IP address
USER=diwas # the user to run as
GROUP=sudo # the group to run as
NUM_WORKERS=3 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=serofero.settings # which settings file should Django use
DJANGO_WSGI_MODULE=serofero.wsgi # WSGI module name
 
echo "Starting $NAME"
 
# Activate the virtual environment
cd $DJANGODIR
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=$BINDIP \
--log-file=- 