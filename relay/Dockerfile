FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/taylordolletzki/grok-direct-p2p"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Dual-process: HTTP (gunicorn sync) + WebSocket (eventlet)
CMD gunicorn -w 1 app:app --bind 0.0.0.0:$PORT & python stream_server.py
