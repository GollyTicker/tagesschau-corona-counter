#!/bin/bash
set -e

CURL="$(which curl 2>/dev/null || echo "/mingw64/bin/curl")"

JQ="$(which jq 2>/dev/null || echo "$1")"

if [[ "$JQ" == "" ]]; then
  echo "Please provide the path to JQ as first argument or add it to PATH."
  exit 1
fi

YESTERDAY="$(date --date=yesterday "+%Y.%m.%d")"

URL="http://swaneet.eu:11000"

PATH="/sum/Corona"

QUERY_PARAMS="n=30&start=2020.02.01&end=$YESTERDAY"

COMMAND="$CURL -s $URL$PATH?$QUERY_PARAMS"

JSON="$($COMMAND)"

if [[ "$JSON" == "" ]]; then
  echo "Error with request. Aborting"
  exit 1
fi

echo "$JSON" | $JQ ".result | min"

