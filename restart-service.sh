#!/bin/bash
set -e

# Running this script with "--dev" runs
# docker-compose without --detach

source config/source.sh

./stop-service.sh

./build-docker-images.sh

COMPOSE_ARGS=""
UP_ARGS="-d"
if [ "$1" = "--dev" ]; then
  COMPOSE_ARGS="-f docker-compose-dev.yml"
  UP_ARGS=""
fi

# shellcheck disable=SC2086
docker-compose -f docker-compose.yml $COMPOSE_ARGS up $UP_ARGS --build
