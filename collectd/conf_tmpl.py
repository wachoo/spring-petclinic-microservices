# This a tiny template engine for generated collectd conf without any dependency.

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


def global_options():
    return Template("""
System          "$SYSTEM"
Instance        "$HOSTNAME"
Hostipv4        "$HOST_IPV4"
Hostname        "$HOSTNAME"
        
FQDNLookup      false
AutoLoadPlugin  false
Interval        $INTERVAL
Timeout         2
ReadThreads     5
WriteThreads    5

""").substitute(os.environ)


def load_plugin_logfile():
    return ("""
LoadPlugin logfile
<Plugin logfile>
    LogLevel "info"
    File "/usr/share/easemon/collectd/log/collectd.log"
    Timestamp true
    PrintSeverity false
</Plugin>

""")


def load_plugin_write_http():
    return Template("""
LoadPlugin write_http
<Plugin write_http>
    <Node "$HOSTNAME">
        URL "$GW_URL"
        VerifyPeer true
        VerifyHost true
        CACert "$GW_CA"
        Header "User-Agent: collectd/5.7.0"
        SSLVersion "TLSv1_2"
        Format Graphite
        Metrics true
    </Node>
</Plugin>

""").substitute(os.environ)


def load_plugin_iaas():
    return load_if_exist_env("IAAS", lambda _: """
LoadPlugin cpu
<Plugin cpu>
    ReportByCpu true
    ReportByState true
    ValuesPercentage true
</Plugin>

LoadPlugin disk
<Plugin disk>
    Disk "/^(xv|h|s)d[a-f][0-9]?$/"
    IgnoreSelected true
</Plugin>

LoadPlugin interface
<Plugin interface>
    Interface "/^lo\d*$/"
    Interface "/^t(un|ap)\d*$/"
    Interface "/^veth.*$/"
    IgnoreSelected true
</Plugin>

LoadPlugin memory
<Plugin memory>
    ValuesAbsolute true
    ValuesPercentage true
</Plugin>

LoadPlugin df
<Plugin df>
    ChangeRoot "/hostfs"
    IgnoreSelected false
    ReportByDevice true
    ReportReserved false
    ReportInodes false
    ValuesAbsolute true
    ValuesPercentage true
</Plugin>
    
""")


def load_plugin_jmx():
    return load_if_exist_env("JMX_HOST_PORT", lambda _: Template("""
LoadPlugin java
<Plugin "java">
  JVMARG "-Djava.class.path=/opt/collectd/share/collectd/java/collectd-api.jar:/opt/collectd/share/collectd/java/generic-jmx.jar"
  LoadPlugin "org.collectd.java.GenericJMX"
  <Plugin "GenericJMX">

    <MBean "java_memory">
      ObjectName "java.lang:type=Memory,*"
      InstancePrefix "java_memory"
      <Value>
        Type "memory"
        InstancePrefix "heap-"
        Table true
        Attribute "HeapMemoryUsage"
      </Value>
      <Value>
        Type "memory"
        InstancePrefix "nonheap-"
        Table true
        Attribute "NonHeapMemoryUsage"
      </Value>
    </MBean>

   <MBean "java_memory_pool">
      ObjectName "java.lang:type=MemoryPool,*"
      InstancePrefix "java_memory_pool."
      InstanceFrom "name"
      <Value>
        Type "memory"
        Table true
        Attribute "Usage"
      </Value>
   </MBean>

   <MBean "java_garbage_collector">
      ObjectName "java.lang:type=GarbageCollector,*"
      InstancePrefix "java_gc-"
      InstanceFrom "name"

      <Value>
         Type "invocations"
         Table false
         Attribute "CollectionCount"
      </Value>

      <Value>
         Type "total_time_in_ms"
         InstancePrefix "collection_time"
         Table false
         Attribute "CollectionTime"
      </Value>
    </MBean>

    <Connection>
      ServiceURL "service:jmx:rmi:///jndi/rmi://$JMX_HOST_PORT/jmxrmi"
      User ""
      Password ""

      ### MBeans by Java ###

      Collect "java_memory"
      Collect "java_memory_pool"
      Collect "java_garbage_collector"

    </Connection>

  </Plugin>
</Plugin>
    
""")).substitute(os.environ)


def load_plugin_mysql():
    p = re.compile("(?P<usr>[^:]+):(?P<pwd>[^@]+)@(?P<host>[^/]+)/(?P<db>\w+)")
    return load_if_exist_env("MYSQL_URI", lambda v: Template("""
LoadPlugin mysql    
<Plugin mysql>
  <Database db>
    # Alias value should be configured as same as Hostname option
    Alias "$HOSTNAME"
    Host  "$host"
    User "$usr"
    Password "$pwd"
    Database "$db"
    MasterStats true
    ConnectTimeout 10
    InnodbStats true
  </Database>
</Plugin>
    
""").substitute(append_env("HOSTNAME", p.search(v).groupdict())))


def load_plugin_nginx():
    return load_if_exist_env("NGINX_STATUS_URL", lambda _: Template("""
LoadPlugin nginx
<Plugin nginx>
  URL "$NGINX_STATUS_URL"
</Plugin>    
""").substitute(os.environ))

if __name__ == '__main__':
    print global_options(), \
        load_plugin_logfile(), \
        load_plugin_write_http(), \
        load_plugin_iaas(), \
        load_plugin_jmx(), \
        load_plugin_mysql(), \
        load_plugin_nginx()
