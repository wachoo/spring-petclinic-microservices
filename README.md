This is a forked demo project for easeapm.com .
# Requirements
1. mvn: [install apache maven on ubuntu16.04](https://www.vultr.com/docs/how-to-install-apache-maven-on-ubuntu-16-04)
2. docker & docker-compose : [install docker compose](https://docs.docker.com/compose/install/#install-compose)
# Import easeapm cert file to java key store

```bash
sudo keytool -importcert -v -trustcacerts -alias gateway.easeapm.com -file <eg.pem> -keystore /etc/ssl/certs/java/cacerts
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

----

> Origin [README](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/README.md).
