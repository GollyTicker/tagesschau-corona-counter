export API_PATH_PUBLIC=$(cat config/config.yml | grep "api-path-public" | awk '{print $2}')
export API_PORT_INTERNAL=$(cat config/config.yml | grep "api-port-internal" | awk '{print $2}')
export WEB_PORT=$(cat config/config.yml | grep "web-port" | awk '{print $2}')
