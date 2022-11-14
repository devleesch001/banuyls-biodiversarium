FROM python:3.10

WORKDIR /usr/src/app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

EXPOSE 80

CMD python ./main.py -p 80
