#!/bin/bash
set -e

./build-docker-images.sh

./docker/reloading-download-latest-data.sh