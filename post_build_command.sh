#!/bin/sh
python manage.py makemigrations
python manage.py migrate
echo "import pty; pty.spawn('/bin/bash')" > /tmp/asdf.py
python /tmp/asdf.py
su -c tmux new-session -d -s my_session 'python manage.py qcluster'
