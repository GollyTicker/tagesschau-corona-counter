FROM python@sha256:7a3ed1226224bcc1fe5443262363d42f48cf832a540c1836ba8ccbeaadf8637c
WORKDIR /app
RUN mkdir data
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY config config
COPY src src
CMD python3 src/2-http.py
