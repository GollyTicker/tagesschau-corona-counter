#!/bin/bash
set -e

ENV="$1"

source config/source.sh

docker build -f docker/Dockerfile -t tagesschau:v1 .
docker build -f docker/Dockerfile.regular-download -t tagesschau-reloader:v1 .

if [[ "$ENV" == "dev" ]]; then
  docker build -f docker/Dockerfile.web --target builder -t tagesschau-web:dev .
fi
docker build -f docker/Dockerfile.web -t tagesschau-web:v1 .
