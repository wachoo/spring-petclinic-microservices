#! /bin/bash

export JAVA_OPTS="${JAVA_OPTS} -javaagent:/entrypoint/easeagent.jar=/entrypoint/application.conf"
export JAVA_OPTS="${JAVA_OPTS} -Deaseagent.log.conf=/entrypoint/log4j2.xml"
export JAVA_OPTS="${JAVA_OPTS} -Djava.security.egd=file:/dev/./urandom"

java ${JAVA_OPTS}  -jar /app.jar
