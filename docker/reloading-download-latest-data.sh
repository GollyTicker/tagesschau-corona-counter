# This file is called from inside the cronjob docker container
# It can also be called on a developers machine for manual execution

echo "============ STARTING DOWNLOAD OF LATEST DATA =========== $(date)"

docker run --rm \
  --name tagesschau-downloader \
  -v tagesschau-data:/app/data \
  tagesschau:v1 /bin/sh src/internal-download-data.sh

echo "============ FINISHED DOWNLOAD OF LATEST DATA =========== $(date)"

echo "============ RESTARTING HTTP SERVICE ============ $(date)"

. config/source.sh
docker restart tagesschau-api

echo "============ DONE RESTARTING HTTP SERVICE ============ $(date)"
