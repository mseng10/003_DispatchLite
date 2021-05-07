#!/bin/sh
python manage.py makemigrations
python manage.py migrate
apt-get install tmux
tmux new-session -d -s my_session 'python manage.py qcluster'
