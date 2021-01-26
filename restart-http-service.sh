#!/bin/bash
set -e

./stop-http-service.sh || true

PORT=`cat config.yml | grep "http-listen-port" | awk '{print $2}'`

docker build -t tagesschau:v1 .

CMD="docker run --rm --name tagesschau-runner -v ${PWD}/data:/app/data -p ${PORT}:${PORT} tagesschau:v1"
echo "$CMD"

(nohup $CMD 2>&1 &) > /dev/null
