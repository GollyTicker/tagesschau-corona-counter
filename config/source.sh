export PORT=$(cat config/config.yml | grep "http-listen-port" | awk '{print $2}')
