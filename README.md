This is a forked demo project for easeapm.com .

# Import easeapm cert file to java key store

```bash
sudo keytool -importcert -v -trustcacerts -alias gateway.easeapm.com -file ea.pem -keystore /etc/ssl/certs/java/cacerts
```

> the password of default keystore is `changeit`

# Setup petclinic cluster for the first time

```bash
./setup
```

# Shutdown cluster

```bash
docker-compose down
```

# Start a cluster

```bash
docker-compose up -d
```

> More commands about docker-compose, please see https://docs.docker.com/compose/reference/

# Use local file for config server

```bash
git clone https://github.com/megaease/spring-petclinic-microservices-config $CONFIG_PATH

export LOCAL_CONFIG_URI="-Dspring.cloud.config.server.git.uri=file:$CONFIG_PATH"
```

----

> Origin [README](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/README.md).
