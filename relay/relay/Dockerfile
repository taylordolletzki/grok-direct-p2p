FROM python:3.10-slim
WORKDIR /app
COPY relay.py .
RUN pip install flask flask-socketio
EXPOSE 5000
CMD ["python", "relay.py"]
