@echo off
echo 3 | python manage.py makemigrations survey_process
python manage.py migrate