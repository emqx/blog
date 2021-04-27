
在阅读该教程之前，假定你已经了解 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)、[MQTT 5](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) 以及 [EMQ X](https://github.com/emqx/emqx) 的简单知识。

[emqx-auth-mysql](https://github.com/emqx/emqx-auth-mysql) 它通过检查每个终端接入的 `username` 和 `password` 是否与用户指定 的 MySQL 数据库中存储的信息一致来实现对终端的访问控制。其功能逻辑如下：

![2401557472472_.pic_hd.jpg](https://static.emqx.net/images/c97590dd35a944ceffba07ba3e8f52a5.jpg)
本文假设 MySQL 已经安装在您的机器上，并且您可以连接到 MySQL 服务器。注：EMQ X 开源版至 v3.1-beta.2 为止，尚不支持 MySQL 8.0，因此以下内容仅适用于 MySQL 5.7 及以下版本。

```
$ mysql --version
mysql  Ver 14.14 Distrib 5.7.25, for macos10.14 (x86_64) using  EditLine wrapper
```



## 插件配置项说明          







#### mqtt.sql

`emqx-auth-mysql` 提供了 mqtt.sql 文件帮助用户快速创建数据表以及导入默认数据。mqtt.sql 将会为 `mqtt_acl` 数据表导入以下默认规则：

```
mysql> select * from mqtt_acl;
+----+-------+-----------+-----------+----------+--------+--------+
| id | allow | ipaddr    | username  | clientid | access | topic  |
+----+-------+-----------+-----------+----------+--------+--------+
|  1 |     1 | NULL      | $all      | NULL     |      2 | #      |
|  2 |     0 | NULL      | $all      | NULL     |      1 | $SYS/# |
|  3 |     0 | NULL      | $all      | NULL     |      1 | eq #   |
|  4 |     1 | 127.0.0.1 | NULL      | NULL     |      2 | $SYS/# |
|  5 |     1 | 127.0.0.1 | NULL      | NULL     |      2 | #      |
|  6 |     1 | NULL      | dashboard | NULL     |      1 | $SYS/# |
+----+-------+-----------+-----------+----------+--------+--------+
6 rows in set (0.00 sec)
```

**allow** - 1: allow; 0: deny

**access** - 1: subscribe; 2: publish; 3: publish and subscribe



**以上规则分别表示：**

- 允许任何用户发布除以 '$' 字符开头以外的任何主题的消息
- 拒绝任何用户订阅任何以 "$SYS/" 开头的主题
- 拒绝任何用户订阅 "#" 主题
- 允许本机用户发布任何以 "$SYS/" 开头的主题
- 允许本机用户发布发布除以 '$' 字符开头以外的任何主题的消息
- 允许 dashboard 用户订阅任何以 "$SYS/" 开头的主题

除此之外，用户可以导入自定义的 ACL 规则。



#### Auth 与 ACL 功能验证

1. Mac 环境安装 mosquitto

   `brew install mosquitto`

2. 创建数据库，导入数据

   mqtt.sql 路径可根据实际情况自行改动

   ```
   mysql> create database mqtt;
   mysql> use mqtt;
   mysql> source ./emqx_auth_mysql/mqtt.sql
   mysql> insert into mqtt_user (id, is_superuser, username, password, salt)
       -> values (1, false, 'test', 'password', 'salt');
   mysql> insert into mqtt_acl (id, allow, ipaddr, username, clientid, access, topic)
       -> values (7, 0, NULL, 'test', NULL, 1, 'mytopic');
   mysql> exit;
   ```

3. 修改配置文件

   禁止匿名访问：

   ```
   ## .../etc/emqx.conf
   allow_anonymous = false
   ```

   配置数据库中密码的加密方式为 `plain` ，即不加密：

   ```
   ## .../etc/plugins/emqx_auth_mysql.conf
   auth.mysql.password_hash = plain
   ```

   配置要访问的数据库以及用户名密码：

   ```
   ## .../etc/plugins/emqx_auth_mysql.conf
   auth.mysql.username = root
   auth.mysql.password = public
   auth.mysql.database = mqtt
   ```

4. 启动 EMQ X 与 emqx-auth-mysql

   ```
   $ ./_rel/emqx/bin/emqx start
   emqx 3.1 is started successfully!
   $ ./_rel/emqx/bin/emqx_ctl plugins load emqx_auth_mysql
   ```



5. 测试

   1. 使用正确的用户名和密码进行连接，并订阅 "topic" 主题

      ```
      $ mosquitto_sub -p 1883 -u test -P password -t 'topic' -d
      Client mosqsub|91114-zhouzibod sending CONNECT
      Client mosqsub|91114-zhouzibod received CONNACK
      Client mosqsub|91114-zhouzibod sending SUBSCRIBE (Mid: 1, Topic: topic, QoS: 0)
      Client mosqsub|91114-zhouzibod received SUBACK
      Subscribed (mid: 1): 0
      ```

      现象：连接并订阅成功

   2. 使用错误的用户名或密码进行连接，并订阅 "topic" 主题

      ```
      $ mosquitto_sub -p 1883 -u bad_user -P password -t 'topic' -d
      Client mosqsub|91136-zhouzibod sending CONNECT
      Client mosqsub|91136-zhouzibod received CONNACK
      Connection Refused: not authorised.
      ```

      现象：连接被拒绝

   3. 使用正确的用户名和密码进行连接，并订阅 "#" 主题

      ```
      $ mosquitto_sub -p 1883 -u test -P password -t '#' -d
      Client mosqsub|11257-zhouzibod sending CONNECT
      Client mosqsub|11257-zhouzibod received CONNACK
      Client mosqsub|11257-zhouzibod sending SUBSCRIBE (Mid: 1, Topic: #, QoS: 0)
      Client mosqsub|11257-zhouzibod received SUBACK
      Subscribed (mid: 1): 128
      ```

      现象：连接成功，订阅失败，原因码128

   4. 使用正确的用户名和密码进行连接，并订阅 "mytopic" 主题

      ```
      $ mosquitto_sub -p 1883 -u test -P password -t 'mytopic' -d
      Client mosqsub|13606-zhouzibod sending CONNECT
      Client mosqsub|13606-zhouzibod received CONNACK
      Client mosqsub|13606-zhouzibod sending SUBSCRIBE (Mid: 1, Topic: mytopic, QoS: 0)
      Client mosqsub|13606-zhouzibod received SUBACK
      Subscribed (mid: 1): 128
      ```

      现象：连接成功，订阅失败，原因码128

   
