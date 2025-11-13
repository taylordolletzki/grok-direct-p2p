LABEL org.opencontainers.image.source="https://github.com/taylordolletzki/grok-direct-p2p"
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "relay:app", "--bind", "0.0.0.0:5000"]
