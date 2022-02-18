## 前言

安全保护几乎对于所有的项目都是一个挑战，对于物联网项目更是如，自普及应用以来物联网业内已经发生过多起安全事故。

作为物联网通信协议事实标准，MQTT 协议保持着较高的安全性，提供了多层次的安全设计：

- 传输层：MQTT 基于 TCP/IP 协议，可以在传输层上使用 SSL/TLS 进行加密传输：
  - 使用 SSL/TLS 加密通信数据，防止中间人攻击；
  - 使用客户端证书作为设备身份凭证，验证设备合法性。
- 应用层：使用 MQTT 自身的安全特性进行防护：
  - MQTT 协议支持用户名和密码实现客户端的身份校验；
  - **MQTT Broker** 实现了  Topic 的读写权限控制（Topic ACL）。

[EMQX MQTT Broker](https://www.emqx.com/zh) 完整支持 **MQTT 协议** 各项安全规范，内置的安全功能无需编程开箱即用，可以快速排除项目中的安全隐患。EMQX 认证鉴权系列将围绕各个层次的安全规范，介绍如何通过配置 EMQX 启用相关功能最终实现相应的安全防护。

本文将围绕 EMQX 中 MQTT 连接认证相关的核心概念，介绍 EMQX 支持的认证方式及其适用场景，并从工作机制和配置原则上阐述 EMQX 认证相关的认证链、认证流程/原理以及相关的配置要点等信息，让你快速掌握 EMQX 认证配置方式。



## 认证方式

EMQX 支持使用内置数据源（文件、内置数据库）、JWT、外部主流数据库和自定义 HTTP API 作为身份认证数据源。

连接数据源、进行认证是插件实现的，每个插件对应一种认证方式，使用前需要启用相应的插件。

客户端连接时插件通过检查其 username/clientid 和 password 是否与指定数据源的信息一致来实现对客户端的身份认证。

EMQX 支持的认证方式：


**内置数据源**

* 用户名认证
* Cliend ID 认证

使用配置文件与 EMQX 内置数据库提供认证数据源，通过 HTTP API 进行管理，足够简单轻量。



**外部数据库**

* LDAP 认证
* MySQL 认证
* PostgreSQL 认证
* Redis 认证
* MongoDB 认证

外部数据库可以存储大量数据，同时方便与外部设备管理系统集成。



**其他**

* HTTP 认证
* JWT 认证

JWT 认证可以批量签发认证信息，HTTP 认证能够实现复杂的认证鉴权逻辑。



> 更改插件配置后需要重启插件才能生效，部分认证鉴权插件包含 ACL 功能。




## 认证结果

任何一种认证方式最终都会返回一个结果：

- 认证成功：经过比对客户端认证成功
- 认证失败：经过比对客户端认证失败，数据源中密码与当前密码不一致
- 忽略认证（ignore）：当前认证方式中未查找到认证数据，无法显式判断结果是成功还是失败，交由认证链下一认证方式或匿名认证来判断



## 匿名认证

EMQ  X 默认配置中启用了匿名认证，任何客户端都能接入 EMQX。没有启用认证插件或认证插件没有显式允许/拒绝（ignore）连接请求时，EMQX 将根据匿名认证启用情况决定是否允许客户端连接。

配置匿名认证开关：

```bash
# etc/emqx.conf

## Value: true | false
allow_anonymous = true
```

**生产环境中请禁用匿名认证。**




## 密码加盐规则与哈希方法

EMQX 多数认证插件中可以启用哈希方法，数据源中仅保存密码密文，保证数据安全。

启用哈希方法时，用户可以为每个客户端都指定一个 salt（盐）并配置加盐规则，数据库中存储的密码是按照加盐规则与哈希方法处理后的密文。

以 MySQL 认证为例：

**加盐规则与哈希方法配置：**

```bash
# etc/plugins/emqx_auth_mysql.conf

## 不加盐，仅做哈希处理
auth.mysql.password_hash = sha256

## salt 前缀：使用 sha256 加密 salt + 密码 拼接的字符串
auth.mysql.password_hash = salt,sha256

## salt 后缀：使用 sha256 加密 密码 + salt 拼接的字符串
auth.mysql.password_hash = sha256,salt

## pbkdf2 with macfun iterations dklen
## macfun: md4, md5, ripemd160, sha, sha224, sha256, sha384, sha512
## auth.mysql.password_hash = pbkdf2,sha256,1000,20
```


### 如何生成认证信息

1. 为每个客户端分用户名、Client ID、密码以及 salt（盐）等信息
2. 使用与 MySQL 认证相同加盐规则与哈希方法处理客户端信息得到密文
3. 将客户端信息写入数据库，客户端的密码应当为密文信息

### EMQX 身份认证流程

1. 根据配置的认证 SQL 结合客户端传入的信息，查询出密码（密文）和 salt（盐）等认证数据，没有查询结果时，认证将终止并返回 ignore 结果
2. 根据配置的加盐规则与哈希方法计算得到密文，没有启用哈希方法则跳过此步
3. 将数据库中存储的密文与当前客户端计算的到的密文进行比对，比对成功则认证通过，否则认证失败

以 PostgreSQL 认证为例，其功能逻辑如下图：

![image202002171542542024409681.png](https://static.emqx.net/images/1366ec307e4ecbabe5e3d7a9a71489d8.png)

> 写入数据的加盐规则、哈希方法与对应插件的配置一致时认证才能正常进行。更改哈希方法会造成现有认证数据失效。



## 认证链

当同时启用多个认证方式时，EMQX 将按照插件开启先后顺序进行链式认证：

- 一旦认证成功，终止认证链并允许客户端接入

- 一旦认证失败，终止认证链并禁止客户端接入

- 直到最后一个认证方式仍未通过，根据匿名认证配置判定

  - 匿名认证开启时，允许客户端接入
  - 匿名认证关闭时，禁止客户端接入

![guide_2.png](https://static.emqx.net/images/9b77437264e3c1bef5fa42059a84c407.png)



>  同时只启用一个认证插件可以提高客户端身份认证效率。




## MQTT TLS 认证

MQTT TLS 的默认端口是 8883：

```bash
listener.ssl.external = 8883
```

配置证书和 CA：

```bash
listener.ssl.external.keyfile = etc/certs/key.pem
listener.ssl.external.certfile = etc/certs/cert.pem
listener.ssl.external.cacertfile = etc/certs/cacert.pem
```

注意，默认的 `etc/certs` 目录下面的 `key.pem`、`cert.pem` 和 `cacert.pem` 是 EMQX Broker 生成的自签名证书，所以在使用支持 TLS 的客户端测试的时候，需要将上面的 CA 证书 `etc/certs/cacert.pem` 配置到客户端。

服务端支持的 cipher 列表需要显式指定，默认的列表与 Mozilla 的服务端 cipher 列表一致：

```bash
listener.ssl.external.ciphers = ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-DES-CBC3-SHA,ECDH-ECDSA-AES256-GCM-SHA384,ECDH-RSA-AES256-GCM-SHA384,ECDH-ECDSA-AES256-SHA384,ECDH-RSA-AES256-SHA384,DHE-DSS-AES256-GCM-SHA384,DHE-DSS-AES256-SHA256,AES256-GCM-SHA384,AES256-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,ECDHE-RSA-AES128-SHA256,ECDH-ECDSA-AES128-GCM-SHA256,ECDH-RSA-AES128-GCM-SHA256,ECDH-ECDSA-AES128-SHA256,ECDH-RSA-AES128-SHA256,DHE-DSS-AES128-GCM-SHA256,DHE-DSS-AES128-SHA256,AES128-GCM-SHA256,AES128-SHA256,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES256-SHA,DHE-DSS-AES256-SHA,ECDH-ECDSA-AES256-SHA,ECDH-RSA-AES256-SHA,AES256-SHA,ECDHE-ECDSA-AES128-SHA,ECDHE-RSA-AES128-SHA,DHE-DSS-AES128-SHA,ECDH-ECDSA-AES128-SHA,ECDH-RSA-AES128-SHA,AES128-SHA
```

## PSK 认证

如果希望使用 PSK 认证，需要将 TLS 认证 中的 `listener.ssl.external.ciphers` 注释掉，然后配置 `listener.ssl.external.psk_ciphers`：

```bash
#listener.ssl.external.ciphers = ECDHE-ECDSA-AES256-GCM-SHA384,...
listener.ssl.external.psk_ciphers = PSK-AES128-CBC-SHA,PSK-AES256-CBC-SHA,PSK-3DES-EDE-CBC-SHA,PSK-RC4-SHA

```

然后启用 emqx_psk_file 插件：

```bash
$ emqx_ctl plugins load emqx_psk_file
```

PSK 的配置文件为 `etc/psk.txt`，使用冒号`:` 分隔 PSK ID 和 PSK：

```bash
client1:1234
client2:abcd
```
