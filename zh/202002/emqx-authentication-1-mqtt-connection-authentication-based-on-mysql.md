## 前言

安全保护几乎对于所有的项目都是一个挑战，对于物联网项目更是如，自普及应用以来物联网业内已经发生过多起安全事故。

作为物联网通信协议事实标准，MQTT 保持着较高的安全性，提供了多层次的安全设计：

- 传输层：MQTT 基于 TCP/IP 协议，可以在传输层上使用 SSL/TLS 进行加密传输：
  - 使用 SSL/TLS 加密通信数据，防止中间人攻击；
  - 使用客户端证书作为设备身份凭证，验证设备合法性。
- 应用层：使用 MQTT 自身的安全特性进行防护：
  - MQTT 协议支持用户名和密码实现客户端的身份校验；
  - MQTT Broker 实现了  Topic 的读写权限控制（Topic ACL）。

EMQX 完整支持 MQTT 各项安全规范，内置的安全功能无需编程开箱即用，可以快速排除项目中的安全隐患。本系列将围绕各个层次的安全规范，介绍如何通过配置 EMQX 启用相关功能最终实现相应的安全防护。



#### emqx-auth-mysql 简介

emqx_auth_mysql 是基于 MySQL 数据库的 MQTT 认证/访问控制插件，通过检查每个终端接入的 `username` 和 `password` 是否与用户指定的 MySQL 数据库中存储的信息一致性来实现对终端的连接认证和访问控制。其功能逻辑如下：

![1313.jpg](https://static.emqx.net/images/7776f1d04279f47cd1a7f5b9ac7ca975.jpg)

本文仅介绍认证功能，ACL 功能见后续文章。

#### 认证原理

设备连接时 EMQX 将执行按照配置的查询语句，比较查询结果中的 `password` 字段的值是否与当前请求客户端的密码进行加盐 (salt) 处理、加密后的值是否相等，验证流程如下：

- 查询结果集中必须有 `password`、`salt` 字段，可以使用 `AS` 语法设置如 `SELECT *, pwd as password FROM mqtt_user`
- 在数据库中可以为每个客户端都指定一个 salt，EMQX 根据客户端传入的密码和通过 SQL 返回的 salt 信息生成密文
- 结果集为空或比对结果不相等，认证失败



#### 创建数据库

你可以使用任何自己喜欢的  客户端，创建好相应的数据库。这里用的是 MySQL 自带的命令行客户端，打开 MySQL 的控制台，如下所示，创建一个名为 ``emqx`` 的认证数据库，并切换到  ``emqx``  数据库。

```sql
mysql> create database emqx;
Query OK, 1 row affected (0.00 sec)

mysql> use emqx;
Database changed
```



#### 创建表

建议的表结构如下，其中，

- username 为客户端连接的时候指定的用户名
- password_hash 为使用 salt 加密后的密文
- salt 为加密串
- is_superuser 是否为超级用户，用于控制 ACL，缺省为0；设置成 1 的时候为超级用户，可以跳过 ACL 检查

>  数据表字段可以不用完全跟下面的一致，可以根据业务需要设置，通过 ``emqx_auth_mysql.conf `` 配置文件中的 ``auth_query `` 配置项来指定。

```sql
CREATE TABLE `mqtt_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `salt` varchar(40) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mqtt_username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

创建成功后，查看一下表结构如下，

```sql
mysql> desc mqtt_user;
+---------------+------------------+------+-----+---------+----------------+
| Field         | Type             | Null | Key | Default | Extra          |
+---------------+------------------+------+-----+---------+----------------+
| id            | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| username      | varchar(100)     | YES  | UNI | NULL    |                |
| password_hash | varchar(255)     | YES  |     | NULL    |                |
| salt          | varchar(40)      | YES  |     | NULL    |                |
| is_superuser  | tinyint(1)       | YES  |     | 0       |                |
| created       | datetime         | YES  |     | NULL    |                |
+---------------+------------------+------+-----+---------+----------------+
6 rows in set (0.01 sec)
```



#### 准备认证数据

本文提供示例数据中密码为 ``test_password``，加密 salt 为 ``secret``。即客户端连接时使用的密码是 `test_password` 。

在 EMQX 的配置文件的 ``auth.mysql.password_hash`` 中，**salt 只是一个标识符，表示 salt 与密码明文的拼接关系**。

- 如果采用``auth.mysql.password_hash = md5,salt`` ，那么 EMQX 使用 MD5 算法对 ``test_passwordsecret`` 字符串加密
- 如果采用``auth.mysql.password_hash = salt,md5`` ，那么 EMQX 使用 MD5 算法对 ``secrettest_password`` 字符串加密

本文采用第一种配置方式，将得到的 MD5 密文插入表 ``mqtt_user``。读者可以通过[在线的 MD5 工具](https://www.md5hashgenerator.com/)或者自己写程序对密码进行编码。

```java
MD5("test_passwordsecret") -> a904b2d1d2b2f73de384955022964595
```

```sql
mysql> INSERT INTO mqtt_user(username,password_hash,salt) VALUES('test_username', 'a904b2d1d2b2f73de384955022964595', 'secret');

Query OK, 1 row affected (0.00 sec)

mysql> select * from mqtt_user;
+----+----------------+----------------------------------+--------+--------------+---------+
| id | username       | password_hash                    | salt   | is_superuser | created |
+----+----------------+----------------------------------+--------+--------------+---------+
|  3 | test_username1 | a904b2d1d2b2f73de384955022964595 | secret |            0 | NULL    |
+----+----------------+----------------------------------+--------+--------------+---------+
1 row in set (0.00 sec)
```



#### 启用认证功能

##### 修改插件配置并启用插件

修改 `etc/plugins/emqx_auth_mysql.conf`，修改后的有效配置如下所示，其余 ACL 相关的配置项可以注释：

```bash
## 修改为实际 mysql 所在的服务器地址
auth.mysql.server = localhost:3306

## 修改为上面创建成功的 emqx 数据库
auth.mysql.database = emqx

## 连接认证查询语句
auth.mysql.auth_query = SELECT password_hash AS password, salt FROM mqtt_user WHERE username = '%u'

## 加密算法 plain | md5 | sha | sha256 | bcrypt
## 加盐加密算法
auth.mysql.password_hash = md5,salt

## 不加盐加密算法，直接写算法名称即可
# auth.mysql.password_hash = md5
```



修改完毕后使用 Dashboard 或命令行重启插件以应用配置，命令行重启示例如下：

```bash
emqx_ctl plugins reload emqx_auth_mysql
```



##### 关闭匿名认证

EMQX 默认开启了匿名认证，即便启用了认证功能，数据库没有查询到数据时设备也能正常连接，只有当查询到数据且密码错误时才会拒绝连接。

打开 `etc/emqx.conf` 配置文件，禁用匿名认证：

```bash
## Value: true | false
allow_anonymous = false
```

重启 emqx 完成配置应用。



#### 测试

准备就绪后，仅通过认证校验之后的设备才能成功连接到 EMQX：

1. 使用正确的用户名和密码进行连接，并订阅 "topic" 主题，可以连接成功：

```bash
$ mosquitto_sub -p 1883 -u test_username -P test_password -t 'topic' -d
Client mosqsub|5228-wivwiv-mac sending CONNECT
Client mosqsub|5228-wivwiv-mac received CONNACK
Client mosqsub|5228-wivwiv-mac sending SUBSCRIBE (Mid: 1, Topic: topic, QoS: 0)
Client mosqsub|4119-zh
ouzibode received SUBACK
Subscribed (mid: 1): 0
```



2. 使用错误的用户名或密码进行连接，并订阅 "topic" 主题，连接失败：

```bash
$ mosquitto_sub -p 1883 -u test_username -P test_password -t 'topic' -d
Client mosqsub/61879-wivwiv-ma sending CONNECT
Client mosqsub/61879-wivwiv-ma received CONNACK
Connection Refused: not authorised.
``` 
## 总 结    

读者在理解了 EMQX MySQL 认证原理之后，可以结合 MySQL 拓展相关应用。欢迎关注 EMQX 安全系列文章，后续本系列将依次讲解 EMQX 与物联网安全相关问题，助您构建高安全物联网项目。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
