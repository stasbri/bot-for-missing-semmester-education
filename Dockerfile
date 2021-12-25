FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
WORKDIR /app

RUN apt-get update && apt-get install -y gcc wget curl vim-tiny \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/* \
    && apt-get clean \
    && ln -sf /bin/bash /bin/sh
