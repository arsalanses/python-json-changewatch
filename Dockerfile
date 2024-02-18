FROM debian:buster-slim as builder

RUN apt-get update && apt-get install curl -y && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM python:3.12.2-slim-bookworm

ENV PYTHONUNBUFFERED 1

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b \
    TZ=Asia/Tehran

WORKDIR /usr/src/app

COPY --from=builder /usr/bin/curl /usr/bin/curl

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./main.py ./main.py
COPY ./my-crontab ./my-crontab

CMD [ "supercronic", "./my-crontab"]
