FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV POSTGRES_HOST=db POSTGRES_DB=isecdb POSTGRES_USER=isecuser POSTGRES_PASSWORD=isecpass REDIS_HOST=redis
EXPOSE 8000
CMD ["python","app.py"]
