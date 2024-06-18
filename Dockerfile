FROM ubuntu:noble
LABEL org.opencontainers.image.authors="Peter van Heusden <pvanheusden@uwc.ac.za>"

RUN apt update && apt install -y python3-full && apt clean

ENV PORT=9000
ENV DATA_PATH=/app/data

COPY src /app
COPY data /app/data

COPY requirements.txt /app/requirements.txt
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install -r /app/requirements.txt

COPY run_server.sh /app/run_server.sh
RUN chmod a+x /app/run_server.sh

ENTRYPOINT /app/run_server.sh
