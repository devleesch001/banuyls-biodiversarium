FROM python:3.10 as banuyls-biodiversarium-back-fish-base

WORKDIR /usr/src/app

COPY ./api/requirements.txt /api/
RUN pip install --no-cache-dir -r /api/requirements.txt

FROM banuyls-biodiversarium-back-fish-base as banuyls-biodiversarium-back-fish-dev

COPY ./api/ /api/

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 80

CMD python /api/main.py
