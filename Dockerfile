FROM python:3.10

WORKDIR /usr/src/app

COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r api/requirements.txt

COPY . .

<<<<<<< HEAD
CMD [ "python", "./api/main.py" ]
=======
EXPOSE 80

CMD python ./main.py -p 80
>>>>>>> b39406e453f2581a20d21770c821c2df87bde034
