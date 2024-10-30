ARG DB_VERSION=1

FROM python:3.8.20-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install -r ./requirements.txt

COPY scripts/ ./scripts
COPY static/ ./static
COPY templates/ ./templates

ARG DB_VERSION
RUN python ./scripts/init_db.py ${DB_VERSION}

COPY app.py ./

RUN mkdir ./keys
RUN python ./scripts/key_gen.py && mv ./private_key ./public_key ./keys

EXPOSE 5001

ENV FLASK_APP="app.py"

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]