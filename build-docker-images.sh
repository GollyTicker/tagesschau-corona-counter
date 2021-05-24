#!/bin/bash
set -e

source config/source.sh

docker build -f docker/Dockerfile -t tagesschau:v1 .
docker build -f docker/Dockerfile.regular-download -t tagesschau-reloader:v1 .
docker build -f docker/Dockerfile.web -t tagesschau-web:v1 .