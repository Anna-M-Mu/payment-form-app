FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt 

COPY . /app

EXPOSE 8000

CMD /bin/bash -c "python manage.py migrate --noinput && uwsgi --http 0.0.0.0:8000 --module config.wsgi:application --buffer-size 65535"
