FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

RUN mkdir /opt/app
WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/  \
     && mkdir -p /var/www/media/  \
     && mkdir -p /opt/app/static/  \
     && mkdir -p /opt/app/media/  \
     && pip install --upgrade pip  \
     && pip install -r requirements.txt

COPY . .
COPY ./static /var/www/static

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]