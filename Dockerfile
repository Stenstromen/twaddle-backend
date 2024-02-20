FROM python:3.11-slim
WORKDIR /app
ADD . /app
ENV AUTHORIZATION_KEY "123"
ENV CORS_ORIGINS "*"
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn eventlet
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "1", "--worker-class", "eventlet", "--timeout", "3600", "app:app"]
