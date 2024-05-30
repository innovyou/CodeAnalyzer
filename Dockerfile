FROM python:3.12.3

WORKDIR /app

RUN apt-get update
RUN apt-get install -y sed attr bash bash-doc bash-completion nano build-essential
RUN apt-get install -y curl libffi-dev gcc python3-dev musl-dev libssl-dev cargo make rsync python3-pip python3-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
