FROM python:3.14.0-alpine3.22

COPY requirements.txt /temp/requirements.txt
COPY service /service

WORKDIR /service

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

# Пользователь под которым будут выполнятся команды, вместо root
RUN adduser --disabled-password service-user
USER service-user

