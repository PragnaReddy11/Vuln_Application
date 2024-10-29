FROM aia-vuln-base:latest

WORKDIR /app

RUN mkdir ./keys
# add this to the base image
RUN python ./scripts/init_db.py
RUN python ./scripts/key_gen.py && mv ./private_key ./public_key ./keys

COPY app.py ./

EXPOSE 5001

ENV FLASK_APP="app.py"

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]



