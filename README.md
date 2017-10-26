This is a forked demo project for easeapm.com .

# Import easeapm cert file to java key store

```bash
sudo keytool -importcert -v -trustcacerts -alias gateway.easeapm.com -file ea.pem -keystore /etc/ssl/certs/java/cacerts
```

> the password of default keystore is `changeit`

# Setup petclinic cluster

```bash
./setup
```

> Origin [README](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/README.md).
