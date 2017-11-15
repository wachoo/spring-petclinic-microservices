#!/usr/bin/env bash

python conf_tmpl.py > collectd.conf
cat collectd.conf
/usr/share/easemon/collectd/sbin/collectd -f -C collectd.conf
