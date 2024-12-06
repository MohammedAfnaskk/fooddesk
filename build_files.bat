@echo off
python -m venv myenv
call myenv\Scripts\activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
mkdir .vercel\output\static
xcopy /E /I staticfiles .vercel\output\static
python manage.py makemigrations
python manage.py migrate
