FROM python:3.10-slim

WORKDIR /relay

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 1 app:app --bind 0.0.0.0:$PORT
