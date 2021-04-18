FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
RUN apk add build-base
COPY ./requirements.txt requirements.txt
RUN pip  install -r requirements.txt --no-cache-dir
COPY ./app /app/app