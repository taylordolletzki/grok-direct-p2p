FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/taylordolletzki/grok-direct-p2p"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "__init__:app", "--bind", "0.0.0.0:5000"]
