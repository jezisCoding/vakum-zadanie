FROM debian:jessie
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install python3 python3-pip -y
COPY . /api
RUN pip3 install -r api/requirements.txt
CMD python3 /api/dbfiller.py
