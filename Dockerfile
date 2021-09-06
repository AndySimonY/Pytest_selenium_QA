FROM tomcat:9.0-alpine

LABEL maintainer = "Andranik"

RUN apk upgrade && apk add --no-cache git && \
git clone https://github.com/a1qatraineeship/docker_task.git

WORKDIR  /docker_task

