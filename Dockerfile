FROM python:3.10

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE='config.settings'

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

WORKDIR /opt/app/movies_admin

ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput

EXPOSE 8000

WORKDIR /opt/app

CMD ["gunicorn", "--chdir", "movies_admin", "--workers=3", "--bind=0.0.0.0:8000", "config.wsgi:application"]
