FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install -y zip htop screen libgl1-mesa-glx

# pip install required packages
RUN pip install seaborn thop

COPY . .

CMD [ "python", "./main.py" ]
