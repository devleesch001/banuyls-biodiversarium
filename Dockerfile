FROM python:3.10 as banuyls-biodiversarium-back-fish-base

WORKDIR /usr/src/app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM banuyls-biodiversarium-back-fish-base as banuyls-biodiversarium-back-fish-dev

COPY api/ .

EXPOSE 80

CMD python ./main.py -p 80
