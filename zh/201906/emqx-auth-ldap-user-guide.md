在阅读本教程前，你需要熟悉 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) 协议，熟悉[EMQX](https://github.com/emqx/emqx) 的简单使用，还需要熟悉 [open ldap](https://www.openldap.org/) 的配置和使用。

[emqx_auth_ldap](https://github.com/emqx/emqx-auth-ldap/)，它通过比对每个尝试接入 EMQX 的终端的 `username` 和 `password` 是否与 OpenLDAP 服务器存储的用户名和密码一致，以此实现对接入终端的控制，同时它还可以为已通过认证的客户端做 ACL 检查，通过检查 OpenLDAP 中对应用户的 `mqttPublishTopic` 和 `mqttSubscriptionTopic` 来判断客户端是否有发布和订阅权限。其功能逻辑见下图：
![WechatIMG482.png](https://static.emqx.net/images/a0abaff3eb24e17c7017a11b85c87898.png)



emqx_auth_ldap 目前版本仅支持 OpenLDAP，不支持 Microsoft Active Directory，提供了 **连接认证** 和 **访问控制** 的功能。不过用户只能自行通过第三方工具去管理 OpenLDAP 中的数据，emqx_auth_ldap 自身不提供这样的管理功能。

## 插件配置项说明

这里给出最新版的 emqx_auth_ldap 的默认配置文件，主要包括：

| 配置项                           | 说明                    |
| -------------------------------- | ----------------------- |
| auth.ldap.servers                | ldap 服务器地址         |
| auth.ldap.port                   | ldap 端口号             |
| auth.ldap.pool                   | ldap 地址池数量         |
| auth.ldap.bind_dn                | ldap 的绑定专有名称(DN) |
| auth.ldap.bind_password          | ldap 的绑定密码         |
| auth.ldap.timeout                | ldap 的查询超时时间     |
| auth.ldap.device_dn              | ldap 的设备专有名       |
| auth.ldap.match_objectclass      | ldap 的匹配对象类       |
| auth.ldap.username.attributetype | ldap 的用户名属性类型   |
| auth.ldap.password.attributetype | ldap 的密码属性类型     |
| auth.ldap.ssl                    | ldap 的 ssl  选项       |

此处需要注意的是，用户对 open ldap 的要有基本的理解，才能正确地配置这些参数。

## OpenLDAP 配置说明

**当用户将所有 emqx_auth_ldap 的配置选项配置好后，还需要再配置 OpenLDAP 服务器。**

首先，需要将 emqx.schema 拷贝到 ldap 的配置目录，如果是 Mac 用户，将 emqx.schema 拷贝到 `/etc/openldap/schema/emqx.schema` 然后编辑 ldap 的配置文件 `slapd.conf`，

/etc/openldap/schema/emqx.schema

```
attributetype ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.1.3 NAME 'isEnabled'
EQUALITY booleanMatch
SYNTAX 1.3.6.1.4.1.1466.115.121.1.7
SINGLE-VALUE
USAGE userApplications )

attributetype ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.4.1 NAME ( 'mqttPublishTopic' 'mpt' )
EQUALITY caseIgnoreMatch
SUBSTR caseIgnoreSubstringsMatch
SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
USAGE userApplications )
attributetype ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.4.2 NAME ( 'mqttSubscriptionTopic' 'mst' )
EQUALITY caseIgnoreMatch
SUBSTR caseIgnoreSubstringsMatch
SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
USAGE userApplications )
attributetype ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.4.3 NAME ( 'mqttPubSubTopic' 'mpst' )
EQUALITY caseIgnoreMatch
SUBSTR caseIgnoreSubstringsMatch
SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
USAGE userApplications )

objectclass ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.4 NAME 'mqttUser'
AUXILIARY
MAY ( mqttPublishTopic $ mqttSubscriptionTopic $ mqttPubSubTopic) )

objectclass ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.2 NAME 'mqttDevice'
SUP top
STRUCTURAL
MUST ( uid )
MAY ( isEnabled ) )

objectclass ( 1.3.6.1.4.1.11.2.53.2.2.3.1.2.3.3 NAME 'mqttSecurity'
SUP top
AUXILIARY
MAY ( userPassword $ userPKCS12 $ pwdAttribute $ pwdLockout ) )
```

/etc/openldap/slapd.conf

```
include  /etc/openldap/schema/core.schema
include  /etc/openldap/schema/cosine.schema
include  /etc/openldap/schema/inetorgperson.schema
include  /etc/openldap/schema/ppolicy.schema
include  /etc/openldap/schema/emqx.schema

database bdb
suffix "dc=emqx,dc=io"
rootdn "cn=root,dc=emqx,dc=io"
rootpw {SSHA}eoF7NhNrejVYYyGHqnt+MdKNBh4r1w3W

directory       /etc/openldap/data
```

编辑完配置文件后可以通过 `sudo slapd -d 3` 去启动 OpenLDAP 服务，如果出现以下错误：

```
Unrecognized database type (bdb)
5c4a72b9 slapd.conf: line 7: <database> failed init (bdb)
slapadd: bad configuration file!
```

那么还需要在 slapd.conf 中添加这一条

```
modulepath /usr/lib/ldap
moduleload back_bdb.la
```

这个时候启动 OpenLDAP 服务。然后通过命令

```
./bin/emqx_ctl plugins load emqx_auth_ldap
```

如果返回

```
Start apps: [emqx_auth_ldap]
Plugin emqx_auth_ldap loaded successfully.
```

那么插件就启用成功了

## 测试

如果需要对 emqx-auth-ldap 做功能测试，可以通过 `sudo slapadd -l schema/emqx.io.ldif -f slapd.conf` 命令去将 emqx-auth-ldap 提供的测试数据导入到 OpenLDAP 服务器中。

此时，再去重新 load emqx_auth_ldap 插件。



**1.使用正确的用户名和密码进行连接，并订阅 "mqttuser0001/pubsub/1" 主题。**

```
mosquitto_sub -p 1883 -u mqttuser0001 -P mqttuser0001 -t 'mqttuser0001/pubsub/1' -d
Client mosqsub|34863-Gilberts- sending CONNECT
Client mosqsub|34863-Gilberts- received CONNACK (0)
Client mosqsub|34863-Gilberts- sending SUBSCRIBE (Mid: 1, Topic: mqttuser0001/pubsub/1, QoS: 0)
Client mosqsub|34863-Gilberts- received SUBACK
Subscribed (mid: 1): 0
```

结果：连接并成功订阅主题



**2.使用错误的用户名或密码进行连接，并订阅 "mqttuser0001/pubsub/1" 主题。**

```
mosquitto_sub -p 1883 -u mqttuser0001 -P mqttuser0002 -t 'mqttuser0001/pubsub/1' -d
Client mosqsub|34884-Gilberts- sending CONNECT
Client mosqsub|34884-Gilberts- received CONNACK (4)
Connection Refused: bad user name or password.
Client mosqsub|34884-Gilberts- sending DISCONNECT
```

结果：连接被拒绝



**3.使用正确的用户名和密码进行连接，并订阅"mqttuser0001/req/+/mqttuser0002"主题。**

```
mosquitto_sub -p 1883 -u mqttuser0001 -P mqttuser0001 -t 'mqttuser0001/req/+/mqttuser0002' -d Client mosqsub|34897-Gilberts- sending CONNECT Client mosqsub|34897-Gilberts- received CONNACK (0) Client mosqsub|34897-Gilberts- sending SUBSCRIBE (Mid: 1, Topic: mqttuser0001/req/+/mqttuser0002, QoS: 0) Client mosqsub|34897-Gilberts- received SUBACK Subscribed (mid: 1): 128 
```

结果：连接成功，订阅失败，错误原因码 128



**4.订阅者和发布者使用正确的用户名和密码进行连接 订阅者订阅到主题 'mqttuser0001/sub'**

```
  $ mosquitto_sub -p 1883 -u mqttuser0001 -P mqttuser0001 -t 'mqttuser0001/sub' -d   Client mosqsub|34991-Gilberts- sending CONNECT   Client mosqsub|34991-Gilberts- received CONNACK (0)   Client mosqsub|34991-Gilberts- sending SUBSCRIBE (Mid: 1, Topic: mqttuser0001/sub, QoS: 0)   Client mosqsub|34991-Gilberts- received SUBACK   Subscribed (mid: 1): 0 
```

  发布者向主题 'mqttuser0001/sub' 发布消息。

```
  mosquitto_pub -p 1883 -u mqttuser0001 -P mqttuser0001 -t 'mqttuser0001/sub' -m "hello" 
```

结果：订阅者未接收到任何消息，发布被拒绝。

做完所有测试， 验证完 emqx_auth_ldap 的所有功能，就可以正式地使用该插件了。
