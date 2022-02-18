在阅读该教程之前，假定你已经了解 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)、[EMQX](https://github.com/emqx/emqx) 的简单知识。



*[emqx_auth_http](https://github.com/emqx/emqx-auth-http/)* 它将每个终端的接入认证、访问控制事件抛给用户自己的 *WebServer* 以实现接入认证和ACL鉴权的功能。其架构逻辑如下：
![emqx_auth_http.png](https://static.emqx.net/images/3de6174eabcbbd4b2ad500f12f727f5f.png)

**emqx_auth_http 主要处理的事情有：**

1. 认证：每当终端一个CONNECT请求上来时，将其携带的 ClientId、Username、Password 等参数，向用户自己配置Web Services 发起一个认证请求。成功则允许该终端连接！
2. ACL：每当终端执行 PUBLISH 和 SUBSCRIBE 操作时，将 ClientId 和 Topic 等参数，像用户自己配置 Web Services 发起一个 ACL 的请求。成功则允许此次 PUBLISH/SUBSCRIBE

实际上，在 EMQX 的集群里面，emqx_auth_http 对于用户的 Web Services 来讲只是一个简单的、无状态的 HTTP Client，他只是将 EMQX 内部的登录认证、和ACL控制的请求转发到用户的 Web Services，并做一定逻辑处理而已。

## 插件配置项说明

在这里给出了其3.1.0版本的默认配置文件，虽然看着内容比较多，其实只是配置了 三个 HTTP Request 的参数

- 终端接入认证(auth_req)
- 判断是否为超级用户(super_req)
- ACL请求(acl_req)

其中，我们以认证为例，其每项分别代表了：

| 配置项                    | 说明                                                        |
| ------------------------- | :---------------------------------------------------------- |
| auth.http.auth_req        | 配置 auth_req 请求所需要访问的 URL 路径地址                 |
| auth.http.auth_req.method | 配置 auth_req 请求所使用的 HTTP Method，仅支持 GET/POST/PUT |
| auth.http.auth_req.params | 配置 auth_req 请求所携带的参数列表                          |

而对于其中 params 项中，支持各种参数占位符，其含义见配置文件注释。例如：

```shell
auth.http.auth_req.params = clientid=%c,username=%u,password=%P
```

其代表的含义是，auth_req 包括三个参数，这个三个参数的 key 分别是 `clientid` `username` `password` 其值分别会替换为终端在接入时其真实的 `ClientId` `Username` `Password`



默认的所有配置如下：

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



## 如何返回

在了解了如何配置 `emqx_auth_http` 插件后，剩下关键的是 *Webserver* 如何返回成功或者失败。



#### 认证

认证成功：

```
HTTP Status Code: 200
```

忽略此次认证

```
HTTP Status Code: 200
Body: ignore
```

错误

```
HTTP Status Code: Except 200
```



#### 超级用户

确认为超级用户:

```
HTTP Status Code: 200
```



非超级用户

```
HTTP Status Code: Except 200
```

###  

#### ACL鉴权

允许PUBLISH/SUBSCRIBE：

```
HTTP Status Code: 200
```

忽略此次鉴权:

```
HTTP Status Code: 200
Body: ignore
```

拒绝该次PUBLISH/SUBSCRIBE:

```
HTTP Status Code: Except 200
```
