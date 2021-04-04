#!/bin/bash
set -e

# Call this script with --dev option to run docker container directly.

./stop-http-service.sh || true

PORT=`cat config/config.yml | grep "http-listen-port" | awk '{print $2}'`

# duplicated in other scripts
docker build -t tagesschau:v1 .

# duplicated in other scripts
CMD0="docker run --rm"
CMD1="--name tagesschau-runner \
-v ${PWD}/data:/app/data \
-v ${PWD}/config:/app/config \
-p ${PORT}:${PORT} tagesschau:v1"

if [[ "$1" == "--dev" ]]; then
  # interactive unbuffered console during debugging
  CMD="$CMD0 -it $CMD1 python3 -u src/2-http.py --dev"
  echo $CMD
  $CMD
else
  CMD="$CMD0 $CMD1"
  echo $CMD
  (nohup $CMD 2>&1 &) > /dev/null
fi
