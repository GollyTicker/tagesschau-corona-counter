# This file is the entrypoint for the docker container
# to download the latest data into the mounted /app/data directory

# it is called with /app as working directory

# change config to: end-date -> 'latest'
sed -i '/end-date/d' config/config.yml
echo 'end-date: "latest"' >> config/config.yml

# run download
python3 -u src/1-download-data.py
