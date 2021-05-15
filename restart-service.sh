#!/bin/bash
set -e

# Call this script with --dev option to run docker container directly.
source config/source.sh

./stop-service.sh

docker build -f docker/Dockerfile -t tagesschau:v1 .
docker build -f docker/Dockerfile.regular-download -t tagesschau-reloader:v1 .

docker-compose up -d --build

# to debug use:
# docker-compose run --rm -it tagesschau-runner /bin/bash
