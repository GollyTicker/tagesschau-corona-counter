export API_PORT=$(cat config/config.yml | grep "api-port" | awk '{print $2}')
export WEB_PORT=$(cat config/config.yml | grep "web-port" | awk '{print $2}')
