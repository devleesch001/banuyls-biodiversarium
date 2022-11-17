FROM python:3.10 as banuyls-biodiversarium-back-fish-base

WORKDIR /api

COPY ./appconfig.json /appconfig.json
COPY ./api /api
RUN pip install --no-cache-dir -r requirements.txt

FROM banuyls-biodiversarium-back-fish-base as banuyls-biodiversarium-back-fish-dev
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 80

CMD python main.py
