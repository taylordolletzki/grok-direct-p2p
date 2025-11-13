FROM python:3.10-slim
WORKDIR /app
COPY relay.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "relay:app", "-b", "0.0.0.0:5000"]
