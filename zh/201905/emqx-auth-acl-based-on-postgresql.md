

在阅读本教程之前，假定你已经了解 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)、[MQTT 5](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) 以及 [EMQ X](https://github.com/emqx/emqx) 的简单知识。

[emqx-auth-pgsql](https://github.com/emqx/emqx-auth-pgsql) 它通过检查每个终端接入的 `username` 和 `password` 是否与用户指定 的 PostgreSQL 数据库中存储的信息一致来实现对终端的访问控制。其功能逻辑如下：

![3181558401488_.pic_hd.jpg](https://static.emqx.net/images/28265963fd1af68ad9e4289b31cbccaf.jpg)

本文假设 PostgreSQL 已经安装在您的机器上，并且您可以连接到 PostgreSQL 服务器。

## 插件配置项说明



| 配置项                   | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| auth.pgsql.server        | 配置需要连接的 PostgreSQL Server 的 host 与 port，格式为：host[:port]，省略后面的 port 时表示使用默认的 5432 端口 |
| auth.pgsql.username      | 用于登录 PostgreSQL 的用户名                                 |
| auth.pgsql.password      | 用于登录 PostgreSQL 的密码                                   |
| auth.pgsql.database      | 配置要访问的数据库                                           |
| auth.pgsql.ssl           | 配置是否使用 SSL 连接数据库，默认为否                        |
| auth.pgsql.auth_query    | 配置从数据库中查找用户名对应密码的 SQL 语句                  |
| auth.pgsql.password_hash | 表示存储在数据表中的 encrypted password 使用的加密算法和加盐方式 |
| auth.pgsql.super_query   | 验证用户是否为超级用户时使用的 SQL 语句                                                   注：超级用户可以发布订阅任何主题 |
| auth.pgsql.acl_query     | ACL 检查时使用的 SQL 语句                                    |

#### mqtt.sql

``emqx-auth-pgsql` 提供了 `mqtt.sql` 文件帮助用户快速建立数据库环境，`mqtt.sql` 将在 `auth.pgsql.database` 指定的数据库下创建 `mqtt_user` 和 `mqtt_acl` 两张表，并为 `mqtt_acl` 添加以下默认规则：

```
mqtt=# select * from mqtt_acl;
 id | allow |  ipaddr   | username  | clientid | access | topic  
----+-------+-----------+-----------+----------+--------+--------
  1 |     1 |           | $all      |          |      2 | #
  2 |     0 |           | $all      |          |      1 | $SYS/#
  3 |     0 |           | $all      |          |      1 | eq #
  4 |     1 | 127.0.0.1 |           |          |      2 | $SYS/#
  5 |     1 | 127.0.0.1 |           |          |      2 | #
  6 |     1 |           | dashboard |          |      1 | $SYS/#
(6 rows)
```

以上规则含义可参考： [《基于 MySQL 的 EMQ X Auth & ACL》]()。



#### Auth 与 ACL 功能验证

**1.Mac 环境安装 mosquitto**

```
brew install mosquitto
```



**2.导入 mqtt.sql 后，手动插入以下两条数据**

```
mqtt=# insert into mqtt_user (id, is_superuser, username, password, salt) values (1, false, 'test', 'password', 'salt');
mqtt=# insert into mqtt_acl (id, allow, ipaddr, username, clientid, access, topic) values (7, 0, NULL, 'test', NULL, 1, 'mytopic');
```



**3.修改配置文件**

禁止匿名访问：

```
## .../etc/emqx.conf
allow_anonymous = false
```

配置数据库中密码的加密方式为 `plain`，既不加密：

```
## .../etc/plugins/emqx_auth_pgsql.conf
auth.pgsql.password_hash = plain
```

配置要访问的数据库以及用户名密码：

```
## .../etc/plugins/emqx_auth_pgsql.conf
auth.pgsql.username = root
auth.pgsql.password = public
auth.pgsql.database = mqtt
```



**4.启动 EMQ X 与 emqx-auth-pgsql**

```
$ ./_rel/emqx/bin/emqx start
emqx 3.1 is started successfully!
$ ./_rel/emqx/bin/emqx_ctl plugins load emqx_auth_pgsql
```



**5.测试**

a.使用正确的用户名和密码进行连接，并订阅 "topic" 主题

```
$ mosquitto_sub -p 1883 -u test -P password -t 'topic' -d
Client mosqsub|4119-zhouzibode sending CONNECT
Client mosqsub|4119-zhouzibode received CONNACK
Client mosqsub|4119-zhouzibode sending SUBSCRIBE (Mid: 1, Topic: topic, QoS: 0)
Client mosqsub|4119-zh
ouzibode received SUBACK
Subscribed (mid: 1): 0
```

现象：连接并订阅成功

b.使用错误的用户名或密码进行连接，并订阅 "topic" 主题

```
$ mosquitto_sub -p 1883 -u bad_user -P password -t 'topic' -d 
Client mosqsub|4363-zhouzibode sending CONNECT
Client mosqsub|4363-zhouzibode received CONNACK
Connection Refused: not authorised.
```

现象：连接被拒绝

c.使用正确的用户名和密码进行连接，并订阅 "#" 主题

$ mosquitto_sub -p 1883 -u test -P password -t '#' -d 
Client mosqsub|4392-zhouzibode sending CONNECT 
Client mosqsub|4392-zhouzibode received CONNACK 
Client mosqsub|4392-zhouzibode sending SUBSCRIBE (Mid: 1, Topic: #, QoS: 0) 
Client mosqsub|4392-zhouzibode received SUBACK 
Subscribed (mid: 1): 128

现象：连接成功，订阅失败，原因码128

d.使用正确的用户名和密码进行连接，并订阅 "mytopic" 主题

$ mosquitto_sub -p 1883 -u test -P password -t 'mytopic' -d 
Client mosqsub|4428-zhouzibode sending CONNECT
Client mosqsub|4428-zhouzibode received CONNACK 
Client mosqsub|4428-zhouzibode sending SUBSCRIBE (Mid: 1, Topic: mytopic, QoS: 0) 
Client mosqsub|4428-zhouzibode received SUBACK 
Subscribed (mid: 1): 128

现象：连接成功，订阅失败，原因码128



