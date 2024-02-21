FROM python:3.11-slim
WORKDIR /app
ADD . /app
ENV AUTHORIZATION_KEY "123"
ENV CORS_ORIGINS "*"
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python3", "/app/app.py"]
