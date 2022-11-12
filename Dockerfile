FROM python:3

WORKDIR /usr/src/app

COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r api/requirements.txt

COPY . .

CMD [ "python", "./api/main.py" ]