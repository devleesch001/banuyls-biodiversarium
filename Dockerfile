FROM node:18.12.1 as build

WORKDIR /build

COPY ./appconfig.json /appconfig.json
COPY ./admin_interface /build

WORKDIR /build/connection
RUN npm i
RUN npm run build
WORKDIR /build/ui
RUN npm i
RUN npm run build

FROM python:3.10 as banuyls-biodiversarium-back-fish-base

WORKDIR /api

COPY ./appconfig.json /appconfig.json
COPY ./api /api
COPY --from=build /build/connection/dist /api/static/connection
COPY --from=build /build/ui/dist /api/static/ui

RUN pip install --no-cache-dir -r requirements.txt

FROM banuyls-biodiversarium-back-fish-base as banuyls-biodiversarium-back-fish-dev
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 80

CMD python main.py
