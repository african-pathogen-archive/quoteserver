FROM conda/miniconda3
LABEL org.opencontainers.image.authors="Peter van Heusden <pvanheusden@uwc.ac.za>"

RUN conda install -c conda-forge -y fastapi uvicorn
RUN conda clean -y

ENV PORT=9000
ENV DATA_PATH=/app/data

COPY src /app
COPY data /app/data

ENTRYPOINT "fastapi run --port ${PORT:-9000} /app/main.py"

