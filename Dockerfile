FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt