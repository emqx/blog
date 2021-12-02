## Preface

Security issue is a challenge for almost all projects, and especially for IoT projects. Since the widespread application of IoT, there have been too many security incidents in the industry.

As the fact standard for IoT communication protocols, the **MQTT protocol** maintains high security and provides a multi-level security design:

- Transport layer: MQTT is based on the TCP / IP protocol, and SSL/TLS can be used for encrypted transmission on the transport layer:
  - SSL/TLS is used to encrypt communication data to prevent man-in-the-middle attacks;
  - The client certificate is used as a device identity to verify device legitimacy.
- Application layer: MQTT's security features are used for protection:
  - MQTT protocol supports client identity verification with username and password;
  - **MQTT Broker** implements topic ACL control.

[EMQ X MQTT Broker](https://www.emqx.com/en) fully supports various security specifications of **MQTT protocol**. With built-in security functions, it can be used out of the box without programming, and can quickly eliminate the security risks in the project. The **EMQ X authentication** series will around various levels of security specifications explain how to enable related functions  through the configuration of  EMQ X to finally achieve corresponding security protection.

This article will around the core concepts related to MQTT connection authentication in EMQ X, introduce the authentication methods supported by EMQ X and the applicable scene. The MQTT related authentication chain, authentication process/principle, and configuration points will be explained through the working mechanism and configuration principles to let you quickly master the EMQ X authentication configuration method.



## Authentication method

In EMQ X, the built-in data sources (files, built-in databases), JWT, external mainstream databases, and custom HTTP APIs can be used as authentication data sources.

Connecting data sources and performing authentication are implemented by plugins. Each plugin corresponds to an authentication method. Therefore, users need to enable related plugins before using the authentication function.

When the client connects, the plugin implements the identity authentication of the client by checking whether its username/clientid and password are consistent with the information of the specified data source.

Authentication methods supported by EMQ X:

**Built-in data sources**

* Username authentication
* Cliend ID authentication

The configuration file, and the built-in database of EMQ X are used to provide an authenticated data source, which is managed through the HTTP API and is simple and lightweight.

**External Database**

* LDAP authentication
* MySQL authentication
* PostgreSQL authentication
* Redis authentication
* MongoDB authentication

The external database can store a large amount of data, and can easily integrate with external device management systems.

**Others**

* HTTP authentication
* JWT authentication

JWT authentication can issue authentication information in batches, and HTTP authentication can implement complex authentication logic.



> After changing the plugin configuration, you need to restart the plugin to take effect. Some authentication plugins include ACL function.




## Authentication results

Any authentication method will eventually return a result:

- Authentication succeeded: the client authentication succeeded after comparison
- Authentication failed: the client authentication fails after comparison, which is because the password in the data source does not match the current password
- Ignore: The authentication data is not found with the current authentication method, and the result cannot be determined explicitly, and will use the next method of authentication chain or anonymous authentication to determine the result.



## Anonymous Authentication

Anonymous authentication is enabled in the EMQ X default configuration and any client can access EMQ X. When the authentication plugin is not enabled or the authentication plugin does not explicitly allow/deny(ignore) the connection request, EMQ X will decide whether to allow the client to connect based on whether the anonymous authentication is enabled.

Configure the anonymous authentication:

```bash
# etc/emqx.conf

## Value: true | false
allow_anonymous = true
```

Please disable anonymous authentication in production environments.




## Password salting rules and hash methods

The hash method can be enabled in most EMQ X authentication plugins. Only the password cipher text is saved in the data source to ensure data security.

When the hash method is enabled, the user can specify a salt for each client and configure a salting rule. The password stored in the database is the processed cipher text according to the salting rule and hash method.

Taking MySQL authentication as an example：

**Salting rules and hash method configuration：**

```bash
# etc/plugins/emqx_auth_mysql.conf

## only hash is used without salt
auth.mysql.password_hash = sha256

## salt prefix: use sha256 to encrypt salt + password
auth.mysql.password_hash = salt,sha256

## salt suffix: encrypted password using sha256 + salt
auth.mysql.password_hash = sha256,salt

## pbkdf2 with macfun iterations dklen
## macfun: md4, md5, ripemd160, sha, sha224, sha256, sha384, sha512
## auth.mysql.password_hash = pbkdf2,sha256,1000,20
```


### How to generate authentication information

1. Assign user name, Client ID, password, and salt for each client
2. Use the same salting rules and hash method as MySQL authentication to process client information to get cipher text
3. Write the client information to the database. The client password should be cipher text information.

### EMQ X authentication process

1. The authentication data such as password (ciphertext) and salt are queried according to the configured authentication SQL combined with the information passed in by the client. If there is no query result, the authentication will terminate and return the ignore result.
2. The cipher text is calculated according to the configured salting rule and hash method. If no hash method is enabled,  this step is skipped.
3. Compare the cipher text stored in the database with the cipher text calculated by the current client. If the comparison is successful, the authentication succeeds. Otherwise, the authentication fails.

Taking PostgreSQL authentication as an example, its functional logic is as follows:

![image202002171542542024409681.png](https://static.emqx.net/images/c62f36f8356d7e887d3d6c4b2685b430.png)

> The authentication can be performed normally when the salting rules and hash method of the written data are consistent with the configuration of the corresponding plugin. It will invalidate existing authentication data when changing the hashing method.



## Authentication chain

When enabling multiple authentication methods at the same time, EMQ X will perform chain authentication in the order in which the plugins are opened:

- Once authentication succeeds, terminate the authentication chain and allow clients to access

- Once authentication fails, terminate the authentication chain and prohibit client access

- If Failing to pass until the last authentication method,  it is determined according to  **anonymous authentication** configuration

  - Allow client access when anonymous authentication is enabled
  - Deny client access when anonymous authentication is disabled

![guide_2.png](https://static.emqx.net/images/38ca581b0d0faec35a5c59ba4669fc75.png)


>  It can improve client authentication efficiency when enabling only one authentication plugin at the same time.




## MQTT TLS authentication

The default port for MQTT TLS is 8883:

```bash
listener.ssl.external = 8883
```

Configure certificates and CAs:

```bash
listener.ssl.external.keyfile = etc/certs/key.pem
listener.ssl.external.certfile = etc/certs/cert.pem
listener.ssl.external.cacertfile = etc/certs/cacert.pem
```

Note that the `key.pem`,` cert.pem` and `cacert.pem` under the default directory of ` etc/certs` are self-signed certificates generated by EMQ X Broker. Therefore, when testing with a client that supports TLS, you need to configure the above CA certificate `etc/certs/cacert.pem` to the client.

The cipher list supported by the server needs to be specified explicitly. The default list is consistent with Mozilla's server cipher list:

```bash
listener.ssl.external.ciphers = ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-DES-CBC3-SHA,ECDH-ECDSA-AES256-GCM-SHA384,ECDH-RSA-AES256-GCM-SHA384,ECDH-ECDSA-AES256-SHA384,ECDH-RSA-AES256-SHA384,DHE-DSS-AES256-GCM-SHA384,DHE-DSS-AES256-SHA256,AES256-GCM-SHA384,AES256-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,ECDHE-RSA-AES128-SHA256,ECDH-ECDSA-AES128-GCM-SHA256,ECDH-RSA-AES128-GCM-SHA256,ECDH-ECDSA-AES128-SHA256,ECDH-RSA-AES128-SHA256,DHE-DSS-AES128-GCM-SHA256,DHE-DSS-AES128-SHA256,AES128-GCM-SHA256,AES128-SHA256,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES256-SHA,DHE-DSS-AES256-SHA,ECDH-ECDSA-AES256-SHA,ECDH-RSA-AES256-SHA,AES256-SHA,ECDHE-ECDSA-AES128-SHA,ECDHE-RSA-AES128-SHA,DHE-DSS-AES128-SHA,ECDH-ECDSA-AES128-SHA,ECDH-RSA-AES128-SHA,AES128-SHA
```

## PSK authentication 

If you want to use PSK authentication, you need to comment out `listener.ssl.external.ciphers` in TLS Authentication, and then configure ` listener.ssl.external.psk_ciphers`:

```bash
#listener.ssl.external.ciphers = ECDHE-ECDSA-AES256-GCM-SHA384,...
listener.ssl.external.psk_ciphers = PSK-AES128-CBC-SHA,PSK-AES256-CBC-SHA,PSK-3DES-EDE-CBC-SHA,PSK-RC4-SHA

```

Then, enable the emqx_psk_file plugin:

```bash
$ emqx_ctl plugins load emqx_psk_file
```

The configuration file for PSK is `etc/psk.txt`. A colon`: ` is used to separate the PSK ID and PSK:

```bash
client1:1234
client2:abcd
```
