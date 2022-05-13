#!/bin/bash
set -e

# Running this script with "--dev" runs
# docker-compose without --detach

source config/source.sh

./stop-service.sh

COMPOSE_ARGS=""
UP_ARGS="-d"
ENV="prod"
if [ "$1" = "dev" ]; then
  COMPOSE_ARGS="-f docker-compose-dev.yml"
  UP_ARGS=""
  ENV="dev"
fi

./build-docker-images.sh $ENV

# shellcheck disable=SC2086
docker-compose -f docker-compose.yml $COMPOSE_ARGS up $UP_ARGS --build
