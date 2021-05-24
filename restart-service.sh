#!/bin/bash
set -e

# with "--dev" docker-compose is run in terminal without --detach

source config/source.sh

./stop-service.sh

./build-docker-images.sh

DETACH_ARG="-d"
if [ "$1" = "--dev" ]; then
  DETACH_ARG=""
fi

docker-compose up $DETACH_ARG --build

# to debug use:
# docker-compose run --rm -it tagesschau-runner /bin/bash
