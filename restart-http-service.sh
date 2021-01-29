#!/bin/bash
set -e

./stop-http-service.sh || true

PORT=`cat config/config.yml | grep "http-listen-port" | awk '{print $2}'`

# duplicated in other scripts
docker build -t tagesschau:v1 .

# duplicated in other scripts
CMD="docker run --rm \
--name tagesschau-runner \
-v ${PWD}/data:/app/data \
-v ${PWD}/config:/app/config \
-p ${PORT}:${PORT} tagesschau:v1"

echo "$CMD"

(nohup $CMD 2>&1 &) > /dev/null
