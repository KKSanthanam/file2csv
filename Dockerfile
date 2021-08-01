FROM python:3.9-slim-buster

VOLUME remotedata
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV time 1-Aug-21
COPY . .

CMD [ "python3", "-m" , "process_fixed.py"]