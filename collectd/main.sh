#!/usr/bin/env bash

export HOSTNAME=`hostname`
export HOST_IPV4=`hostname -I | awk '{print $1}'`
export INTERVAL=60

python conf_tmpl.py > collectd.conf
cat collectd.conf
/usr/share/easemon/collectd/sbin/collectd -f -C collectd.conf
