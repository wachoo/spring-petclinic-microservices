#!/usr/bin/env bash

export HOSTNAME=`hostname`
export HOST_IPV4=`hostname -I | awk '{print $1}'`

python yml_tmpl.py > filebeat.yml
cat filebeat.yml
/usr/share/easemon/filebeat/bin/filebeat -v -c filebeat.yml -path.logs /usr/share/easemon/filebeat/log
