FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/taylordolletzki/grok-direct-p2p"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# DEBUG: Show installed packages
RUN pip list

# Gevent worker with debug
CMD gunicorn -k gevent -w 1 --log-level debug app:app --bind 0.0.0.0:$PORT
