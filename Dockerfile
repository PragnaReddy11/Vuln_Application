FROM aia-gr8scope-base:1.0.1

WORKDIR /app

COPY app.py ./

RUN mkdir ./keys
RUN python ./scripts/key_gen.py && mv ./private_key ./public_key ./keys

EXPOSE 5001

ENV FLASK_APP="app.py"

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]