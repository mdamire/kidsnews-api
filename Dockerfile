# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install -y postgresql-client
RUN pip install --root-user-action=ignore --upgrade pip && \
    pip install --root-user-action=ignore -r requirements.txt

ENV SERVICE='all'

COPY . .
