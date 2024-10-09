FROM python:3.11-slim
WORKDIR /app
RUN mkdir data
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY config config
COPY src src
CMD python3 src/2-http.py
