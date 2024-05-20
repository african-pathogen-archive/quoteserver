FROM ubuntu:noble
LABEL org.opencontainers.image.authors="Peter van Heusden <pvanheusden@uwc.ac.za>"

RUN apt update && apt install -y python3-fastapi uvicorn && apt clean

ENV PORT=9000
ENV DATA_PATH=/app/data

COPY src /app
COPY data /app/data

ENTRYPOINT uvicorn --app-dir /app --port ${PORT:-9000} --host 0.0.0.0 main:app

