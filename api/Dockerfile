FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
LABEL maintainer="RETAServices<retaservices@reta.eu>"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

COPY ./ml_models /app/ml_models

COPY ./app /app/app

EXPOSE 80