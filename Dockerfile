FROM ubuntu:24.04

RUN apt update                         

RUN apt install ffmpeg -y

RUN apt install python3 -y

RUN apt install pip -y 

RUN apt install sqlite3 -y

RUN pip3 install  --break-system-packages flask flask-wtf flask-sqlalchemy pytz dotenv flask-migrate

COPY config.json /app/config/

WORKDIR /app

EXPOSE 5000

CMD ["flask", "run"]
