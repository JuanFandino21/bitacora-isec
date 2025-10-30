FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
ENV POSTGRES_HOST=db POSTGRES_DB=isecdb POSTGRES_USER=isecuser POSTGRES_PASSWORD=isecpass REDIS_HOST=redis
CMD ["python","worker.py"]
