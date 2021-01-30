#!/bin/bash
set -e

# duplicated in other scripts
docker build -t tagesschau:v1 .

# duplicated in other scripts
docker run --rm \
  --name tagesschau-downloader \
  -v ${PWD}/data:/app/data \
  tagesschau:v1 /bin/sh src/internal-download-data.sh
