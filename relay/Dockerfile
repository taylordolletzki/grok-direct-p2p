FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/taylordolletzki/grok-direct-p2p"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Railway injects $PORT at runtime
CMD gunicorn -k eventlet -w 1 app:app --bind 0.0.0.0:$PORT
