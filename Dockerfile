FROM python:3.8.20-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install -r ./requirements.txt

COPY scripts/ ./scripts
COPY static/ ./static
COPY templates/ ./templates
