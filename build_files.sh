 

#!/bin/bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
mkdir -p .vercel/output/static
cp -r staticfiles/ .vercel/output/static/
python manage.py makemigrations
python manage.py migrate
