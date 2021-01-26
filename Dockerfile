FROM python:3.9-slim-buster
RUN apt update && apt install -y python3-pip
WORKDIR /app
RUN mkdir data
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY *.yml *.py *.sh ./
CMD python3 2-http.py
