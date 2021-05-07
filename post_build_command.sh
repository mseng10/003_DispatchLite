#!/bin/sh
python manage.py makemigrations
python manage.py migrate
cd /home
su -c tmux new-session -d -s my_session 'python manage.py qcluster'
