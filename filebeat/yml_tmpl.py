# This a tiny template engine for generated filebeat conf without any dependency.

from string import Template
import os
import re


def load_if_exist_env(name, fun):
    if name in os.environ:
        return fun(os.getenv(name))
    else:
        return ""


def append_env(name, d):
    d[name] = os.getenv(name)
    return d


def common():
    return Template("""
name: "$HOSTNAME"
logging.level: warning

filebeat.prospectors:

- input_type: log
  paths:
    - /var/log/syslog
  fields_under_root: true
  fields:
    system: "$SYSTEM"
    hostipv4: "$HOST_IPV4"
    hostname: "$HOSTNAME"
    group: "os_syslog"
    category: "infrastructure"
  document_type: "os_syslog"

- input_type: log
  paths:
    - /var/log/dmesg
  fields_under_root: true
  fields:
    system: "$SYSTEM"
    hostipv4: "$HOST_IPV4"
    hostname: "$HOSTNAME"
    group: "os_dmesg"
    category: "infrastructure"
  document_type: "os_dmesg"
  
""").substitute(os.environ)


def nginx():
    return load_if_exist_env("NGINX", lambda _: Template("""
- input_type: log
  paths:
    - /var/log/nginx/access.log
  fields_under_root: true
  fields:
    system: "$SYSTEM"
    hostipv4: "$HOST_IPV4"
    hostname: "$HOSTNAME"
    group: "nginx_access"
    instance: $NGINX
  document_type: "nginx_access"
  
- input_type: log
  paths:
    - /var/log/nginx/error.log
  fields_under_root: true
  fields:
    system: "$SYSTEM"
    hostipv4: "$HOST_IPV4"
    hostname: "$HOSTNAME"
    group: "nginx_error"
    instance: $NGINX
  document_type: "nginx_error"
  
""").substitute(os.environ))


def mysql():
    return load_if_exist_env("MYSQL", lambda _: Template("""
- input_type: log
  paths:
    - /var/log/nginx/access.log
  fields_under_root: true
  fields:
    system: "$SYSTEM"
    hostipv4: "$HOST_IPV4"
    hostname: "$HOSTNAME"
    group: "mysql_slow_query"
    instance: $MYSQL
  document_type: "mysql_slow_query"
  multiline:
    pattern: "^# User@Host:"
    negate: true
    match: after
  
""").substitute(os.environ))


def output():
    return Template("""
output.http:
  urls: [ "$GW_URL" ]
  compress: true
  guaranteed_all: true
  tls.certificate_authorities: [ "$GW_CA" ]    
  
""").substitute(os.environ)


if __name__ == '__main__':
    print common(), nginx(), mysql(), output()
