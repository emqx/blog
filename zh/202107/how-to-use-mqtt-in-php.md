[PHP](https://www.php.net) 是一种被广泛应用的开放源代码的多用途脚本语言，它可嵌入到 HTML 中，尤其适合 Web 开发。

本文主要介绍如何在 PHP 项目中使用 `php-mqtt/client` 客户端库 ，实现 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、取消订阅、收发消息等功能。


## MQTT 客户端库选择

本文选择了 composer 上下载量最高的 `php-mqtt/client` 这个客户端库，更多 PHP-MQTT 客户端库可以在 [Packagist - Search MQTT](https://packagist.org/search/?query=mqtt) 中查看。

有关 php-mqtt/client 更多使用文档请参阅 [Packagist php-mqtt/client](https://packagist.org/packages/php-mqtt/client)。

MQTT 通信属于 HTTP 体系之外的网络通信场景，由于 PHP 特性限制，使用 PHP 体系中的 Swoole/Workerman 等专为网络通信打造的拓展可以带来更好的体验，其使用本文不再赘述，相关的 MQTT 客户端库如下：

- [workerman/mqtt](https://packagist.org/packages/workerman/mqtt)：Asynchronous MQTT client for PHP based on workerman.
- [simps/mqtt](https://packagist.org/packages/simps/mqtt)：MQTT Protocol Analysis and Coroutine Client for PHP.


## 项目初始化

### 确认 PHP 版本

本项目使用 7.4.21 进行开发测试，读者可用如下命令确认 PHP 的版本。

```
php --version

PHP 7.4.21 (cli) (built: Jul 12 2021 11:52:30) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.21, Copyright (c), by Zend Technologies
```

### 使用 Composer 安装 php-mqtt/client 客户端

Composer 是 PHP 的一个依赖管理工具，它能管理你的 PHP 项目所需要的所有依赖关系。

```bash
composer require php-mqtt/client
```


## PHP MQTT 使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

#### 导入 composer autoload 文件和 php-mqtt/client

```php
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
```

#### 设置 MQTT Broker 连接参数

设置 MQTT Broker 连接地址，端口以及 topic，同时我们调用 PHP `rand` 函数随机生成 MQTT 客户端 id。

```php
$server   = 'broker-cn.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = null;
$clean_session = false;
```

#### 编写 MQTT 连接函数

使用上述的参数进行连接，通过 `ConnectionSettings` 设置连接参数，比如

```php
$connectionSettings  = new ConnectionSettings();
$connectionSettings
  ->setUsername($username)
  ->setPassword(null)
  ->setKeepAliveInterval(60)
  // Last Will 设置
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);
```

### 订阅消息

编写代码订阅 `emqx/test` 主题，并为该订阅配置回调函数以处理接收到的消息，此处我们将订阅得到的主题和消息打印出来：

```php
// 订阅
$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);
```

### 发布消息

构造一个 payload，调用 `publish` 函数向 `emqx/test` 主题发布消息，发布完成之后客户端需要进入轮询状态，处理传入的消息和重发队列：

```php
for ($i = 0; $i< 10; $i++) {
  $payload = array(
    'protocol' => 'tcp',
    'date' => date('Y-m-d H:i:s'),
    'url' => 'https://github.com/emqx/MQTT-Client-Examples'
  );
  $mqtt->publish(
    // topic
    'emqx/test',
    // payload
    json_encode($payload),
    // qos
    0,
    // retain
    true
  );
  printf("msg $i send\n");
  sleep(1);
}

// 客户端轮询以处理传入消息和重发队列
$mqtt->loop(true);
```

### 完整代码

服务器连接、消息发布与接收代码。

```php
<?php

require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;

$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = null;
$clean_session = false;

$connectionSettings  = new ConnectionSettings();
$connectionSettings
  ->setUsername($username)
  ->setPassword(null)
  ->setKeepAliveInterval(60)
  // Last Will 设置
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);


$mqtt = new MqttClient($server, $port, $clientId);

$mqtt->connect($connectionSettings, $clean_session);
printf("client connected\n");

$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);

for ($i = 0; $i< 10; $i++) {
  $payload = array(
    'protocol' => 'tcp',
    'date' => date('Y-m-d H:i:s'),
    'url' => 'https://github.com/emqx/MQTT-Client-Examples'
  );
  $mqtt->publish(
    // topic
    'emqx/test',
    // payload
    json_encode($payload),
    // qos
    0,
    // retain
    true
  );
  printf("msg $i send\n");
  sleep(1);
}

$mqtt->loop(true);

```


## 测试

运行 MQTT 消息发布代码，我们将看到客户端已经成功连接，且消息已经逐条发布并接收成功：

```bash
php pubsub_tcp.php
```

![PHP MQTT 测试](https://static.emqx.net/images/61618d56823886f101feaf6741a20c3f.png)


## 总结

至此，我们完成了使用 **php-mqtt/client** 客户端连接到[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
