
Before reading this tutorial, we suppose that you already known some basic [MQTT](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) and [EMQ X MQTT broker](https://emqx.io/) knowledge.



[emqx_auth_http](https://github.com/emqx/emqx-auth-http/) will throw authentication and access control event for each **MQTT client** to the user's own *WebServer*, to implement authentication and ACL. The architecture logic is:

![emqx_auth_http.png](https://static.emqx.net/images/cf59952934faf013fe1b1c5c74c5e01b.png)

**The events that `emqx_auth_http` mainly process are :**

1. Authentication: Whenever the MQTT client receives a CONNECT request, [EMQ X MQTT broker](https://emqx.io/) will fill the parameter (such as ClientId, Username, and Password, etc) brought by the client to the HTTP parameter, and then will initiate a request to the Web Services the user-configured themselves. If successful request, allowing this MQTT client to connect.
2. ACL: Whenever the MQTT client implements the PUBLISH and SUBSCRIBE operation, EMQ X will fill the parameter (such as ClientId and topic, etc) to the HTTP parameter, and then will initiate an ACL request to the Web Services the user-configured themselves. If successful request, allowing this PUBLISH/SUBSCRIBE.

Actually, in the EMQ X cluster, emqx_auth_http is just a simple and stateless HTTP Client for the user's  Web Service. emqx_auth_http only sends the internal EMQ X login authentication and ACL control requests to the user's Web Services, and did some logic processing.

## Introduction to the plugin configuration items

The following content list the default configuration file of this plugin 3.1.0, although  there is a lot of content, only configured three HTTP Request parameters. 

- MQTT client access authentication(auth_req)
- Judging whether is a superuser(super_req)
- ACL request(acl_req)

We will take the authentication as an example. Every configuration item represents:

| Configuration Item        | Description                                                  |
| ------------------------- | :----------------------------------------------------------- |
| auth.http.auth_req        | configuring the URL path address the auth_req request needs  |
| auth.http.auth_req.method | configuring the HTTP Method the auth_req uses,  only support GET/POST/PUT |
| auth.http.auth_req.params | configuring parameter list of auth_req request               |

As for params item, it supports various parameter placeholders. The comment of the configuration file included the meanings of the placeholder. For example:  

```shell
auth.http.auth_req.params = clientid=%c,username=%u,password=%P
```

It means that the auth_req includes three parameters. The keys of these three parameters are `clientid`,  `username` and `password` respectively. When accessing the client, the values of these keys will be replaced by the real values of `ClientId`,  `Username`, and  `Password`.



All default configurations are:

```shell
##--------------------------------------------------------------------
## Authentication request.
##
## Variables:
##  - %u: username
##  - %c: clientid
##  - %a: ipaddress
##  - %P: password
##  - %cn: common name of client TLS cert
##  - %dn: subject of client TLS cert
##
## Value: URL
auth.http.auth_req = http://127.0.0.1:8991/mqtt/auth
## Value: post | get | put
auth.http.auth_req.method = post
## Value: Params
auth.http.auth_req.params = clientid=%c,username=%u,password=%P

##--------------------------------------------------------------------
## Superuser request.
##
## Variables:
##  - %u: username
##  - %c: clientid
##  - %a: ipaddress
##
## Value: URL
auth.http.super_req = http://127.0.0.1:8991/mqtt/superuser
## Value: post | get | put
auth.http.super_req.method = post
## Value: Params
auth.http.super_req.params = clientid=%c,username=%u


##--------------------------------------------------------------------
## ACL request.
##
## Variables:
##  - %A: 1 | 2, 1 = sub, 2 = pub
##  - %u: username
##  - %c: clientid
##  - %a: ipaddress
##  - %t: topic
##
## Value: URL
auth.http.acl_req = http://127.0.0.1:8991/mqtt/acl
## Value: post | get | put
auth.http.acl_req.method = get
## Value: Params
auth.http.acl_req.params = access=%A,username=%u,clientid=%c,ipaddr=%a,topic=%t
```



## How to return 

After understanding how to configure the `emqx_auth_http` plugin, the rest key thing is how to let the *Webserver* returning succeeded or failed. 

#### Authentication

Authentication successed:

```
HTTP Status Code: 200
```

Ignore this authentication:

```
HTTP Status Code: 200
Body: ignore
```

Error:

```
HTTP Status Code: Except 200
```

#### The super user

Confirmed super user:

```
HTTP Status Code: 200
```

Non-super user:

```
HTTP Status Code: Except 200
```

#### ACL authentication

Allow PUBLISH/SUBSCRIBE：

```
HTTP Status Code: 200
```

Ignore this authentication: 

```
HTTP Status Code: 200
Body: ignore
```

Refuse this PUBLISH/SUBSCRIBE:

```
HTTP Status Code: Except 200
```

