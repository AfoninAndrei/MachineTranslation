export JOB_NAME="Translator"
export IMAGE="en-ru-translator"
export TAG="latest"
export API_PORT=80
export TIMEOUT=300

echo ${IMAGE}:${TAG}

# stop running container with same job name, if any
if [ "$(docker ps -a | grep $JOB_NAME)" ]; then
  docker stop ${JOB_NAME} && docker rm ${JOB_NAME}
fi

# start docker container
docker run -d \
  --rm \
  -p ${API_PORT}:80 \
  -e "TIMEOUT=${TIMEOUT}" \
  --name="${JOB_NAME}" \
  ${IMAGE}:${TAG}