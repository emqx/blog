## Foreword

Security is a challenge for almost all projects, especially for IoT projects. Since the widespread of IoT application, there have been too many security incidents in the IoT industry.

As the factual standard for IoT communication protocols, MQTT maintains a high level of security and provides a multi-level security design:

- Transport layer: MQTT is based on TCP / IP protocol, and SSL/TLS is used for encrypted transmission on the transport layer:
  - SSL/TLS is used to encrypt communication data to prevent middleman attacks;
  - The client certificate is used as device identity certificate  to verify the validity of the device.
- Application layer ：MQTT's security features are used for protection:
  - MQTT protocol supports user name and password for client identity verification;
  - MQTT Broker implements  access control for topics (Topic ACL).

MQTT Safety specifications are fully supported by EMQ, and the built-in safety functions can be used out-of-the-box without programming, which can quickly eliminate security risks in projects. This series will focus on various levels of safety specifications, and introduce how to enable relevant functions through the configuration of EMQ X to finally achieve the corresponding safety protection.

### Introduction to emqx-auth-mysql 

emqx_auth_mysql is an MQTT authentication/access control plug-in based on the MySQL database. It realizes connection authentication and access control of the terminal by checking whether the `username` and ` password` accessed by each terminal are consistent with the information stored in the user-specified MySQL database. Its functional logic is as follows:

![1313.jpg](https://static.emqx.net/images/bada404720935875a97ce0b1e6b79ad7.jpg)

In this article, only the authentication function is introduced. ACL function will be introduced in the following article.

### Authentication principle

When the device is connected, EMQ X will execute the query statement according to the configuration and compare  whether the value of the `password` field in the query result is the same as the value of current requesting client's password with salt processing and encryption. The verification process is as follows:

- There must be `password`  and ` salt` fields in the query result set. You can use the `AS` syntax setting such as ` SELECT *,pwd as password FROM mqtt_user`
- Salt can be specified for each client in the database. EMQ X generates a ciphertext based on the client's incoming password and the salt information returned through SQL.
- If the result set is empty or the comparison results are not equal, the authentication fails



### Create a database

You can use any client you like to create the corresponding database. The command-line client of MySQL is used here. Open the MySQL console, as shown below, create an authentication database named `` emqx``, and switch to the `` emqx`` database.

```sql
mysql> create database emqx;
Query OK, 1 row affected (0.00 sec)

mysql> use emqx;
Database changed
```



### Create a table

The suggested table structure is as follows, where:

- username is the user name specified when the client connects
- password_hash is the ciphertext encrypted with salt
- salt is an encrypted string
- is_superuser means whether it is a super user, which is used to control the ACL. The default is 0; when set to 1, it is a super user, which can skip the ACL check

>  The data table fields do not need to be completely consistent with the following. They can be set according to business needs and specified through the `auth_query` configuration item in the ` emqx_auth_mysql.conf` configuration file.

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

After the creation is successful, the table structure is as follows:

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



### Prepare authentication data

In this article, the password of sample data is `test_password` and the encrypted salt is ` secret`. That is, the password used by the client for connection is `test_password`.

In the configuration file `auth.mysql.password_hash` of EMQ X, **salt is just an identifier, which indicates the concatenation relationship between salt and the plaintext of the password.**

- If `auth.mysql.password_hash = md5,salt` is used, then the MD5 algorithm is used by EMQ X to encrypt ` test_passwordsecret` string
- If `auth.mysql.password_hash = salt,md5` is used, then the MD5 algorithm is used by EMQ X to encrypt ` secrettest_password` string

In this article, the first configuration method is used, inserting the obtained MD5 ciphertext into the table `` mqtt_user``. Readers can use [online MD5 tool](https://www.md5hashgenerator.com/) or write a program to encode the password.

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



### Enable authentication

#### Modify plug in configuration and enable plugin

Modify `etc/plugins/emqx_auth_mysql.conf`. The effective configuration after the modification is shown below. The remaining ACL related configuration items can be commented:

```bash
## Change to the server address where the actual mysql is located
auth.mysql.server = localhost:3306

## Change to the emqx database created above
auth.mysql.database = emqx

## Connection authentication query
auth.mysql.auth_query = SELECT password_hash AS password, salt FROM mqtt_user WHERE username = '%u'

## Encryption Algorithm plain | md5 | sha | sha256 | bcrypt
## Salt encryption algorithm
auth.mysql.password_hash = md5,salt

## No salt encryption algorithm, just write the algorithm name
# auth.mysql.password_hash = md5
```



After the modification, use Dashboard or the command line to restart the plug in to apply the configuration. The command line for restarting example is as follows:

```bash
emqx_ctl plugins reload emqx_auth_mysql
```



#### Disable  anonymous authentication

EMQ X enabled anonymous authentication by default. Once the authentication function is enabled, the device can connect normally even when the database does not query the data, and the connection will be refused only when the data is queried and the password is incorrect.

Open the `etc/emqx.conf` configuration file and disable anonymous authentication:

```bash
## Value: true | false
allow_anonymous = false
```

Restart emqx to complete the configuration application.



### Test

Once ready, only devices that have passed authentication verification can successfully connect to EMQ X:

1. Connect with the correct username and password,  subscribe to the topic, and the connection will succeed:

```bash
$ mosquitto_sub -p 1883 -u test_username -P test_password -t 'topic' -d
Client mosqsub|5228-wivwiv-mac sending CONNECT
Client mosqsub|5228-wivwiv-mac received CONNACK
Client mosqsub|5228-wivwiv-mac sending SUBSCRIBE (Mid: 1, Topic: topic, QoS: 0)
Client mosqsub|4119-zh
ouzibode received SUBACK
Subscribed (mid: 1): 0
```



2. Connect with the wrong username or password, subscribe to the topic, and the connection will fail:

```bash
$ mosquitto_sub -p 1883 -u test_username -P test_password -t 'topic' -d
Client mosqsub/61879-wivwiv-ma sending CONNECT
Client mosqsub/61879-wivwiv-ma received CONNACK
Connection Refused: not authorised.
```

## Summary  

After understanding the principle of EMQ X MySQL authentication, readers can use MySQL to expand related applications. Welcome to the EMQ X security series, and this series will explain the security issues related to EMQ X and IoT  to help you build an IoT project with high-level security.
