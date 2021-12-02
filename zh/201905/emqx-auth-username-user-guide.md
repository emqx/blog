在阅读该教程之前，假定你已经了解 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)、[EMQX](https://github.com/emqx/emqx) 的简单知识。



[emqx_auth_username](https://github.com/emqx/emqx-auth-username/) 它通过比对每个终端的接入的 `username` 和 `password` 与 EMQ X 中存储的是否一致来实现终端接入的控制。其功能逻辑如下：

![2671557804540_.pic.jpg](https://static.emqx.net/images/1a54b88722d76486f22ebc1215b4e7bb.jpg)

emqx_auth_username 目前版本仅提供了 **连接认证** 的功能。且提供了 *CLI* 和 *REST API* 来进行管理当前集群中的 *Username 库*



## 插件配置项说明

在这里给出了其 3.1.0 版本默认的配置文件。其内容非常的简单，主要包括：

1.Password 密文加密类型

终端在连接时，必须采用对用加密类型的密文才可以成功连接

```properties
## Password hash.
##
## Value: plain | md5 | sha | sha256
auth.user.password_hash = sha256
```



## Username 管理

#### CLI 命令

在成功启动 `emqx_auth_username` 该插件时，会向 `EMQ X` 注册一些 CLI 命令以在运行时管理 `username`:

```bash
$ ./bin/emqx_ctl users

users list                                     
users add <Username> <Password>                
users update <Username> <NewPassword>          
users del <Username>                           
```



#### REST API

在成功启动 `emqx_auth_username` 该插件时，会开启对应的 REST API 用于在运行时管理 `username`



获取所有的 username

```
# Request
GET api/v3/auth_username

# Response
{
   "code": 0,
   "data": ["username1"]
}
```



添加一个 username:

```
# Request
POST api/v3/auth_username
{
   "username": "some_name",
   "password": "password"
}

# Response
{
   "code": 0
}
```



更新某 username 的密码 :

```
# Request
PUT api/v3/auth_username/$NAME
{
   "password": "password"
}

# Response
{
   "code", 0
}
```



查看某 username 的密码 (密文):

```
# Request
GET api/v3/auth_username/$NAME

# Response
{
   "code": 0,
   "data": {
       "username": "some_username",
       "password": "hashed_password"
   }
}
```



删除某 username:

```
# Request
DELETE api/v3/auth_username/$NAME

# Response
{
   "code": 0
}
```
