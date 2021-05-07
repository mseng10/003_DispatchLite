#!/bin/sh
python manage.py makemigrations
python manage.py migrate
sudo tmux new-session -d -s my_session 'python manage.py qcluster'
