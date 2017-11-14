#! /bin/bash

export JAVA_OPTS="${JAVA_OPTS} -javaagent:/entrypoint/easeagent.jar=/entrypoint/application.conf"
export JAVA_OPTS="${JAVA_OPTS} -Deaseagent.log.conf=/entrypoint/log4j2.xml"
export JAVA_OPTS="${JAVA_OPTS} -Djava.security.egd=file:/dev/./urandom"
export JAVA_OPTS="${JAVA_OPTS} -Dcom.sun.management.jmxremote"
export JAVA_OPTS="${JAVA_OPTS} -Dcom.sun.management.jmxremote.ssl=false"
export JAVA_OPTS="${JAVA_OPTS} -Dcom.sun.management.jmxremote.authenticate=false"
export JAVA_OPTS="${JAVA_OPTS} -Dcom.sun.management.jmxremote.port=17264"

java ${JAVA_OPTS}  -jar /app.jar
