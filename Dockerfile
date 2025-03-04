FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt 

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
