PHP 是一种广泛使用的开源脚本语言，特别适用于 Web 开发，并且可以嵌入到 HTML 中。它使开发者能够轻松构建动态 Web 应用程序。

在本指南中，我们将向您介绍如何使用 `php-mqtt/client` 库将 MQTT 集成到您的 PHP 应用程序中。您将学习如何实现基本的 MQTT 功能，如连接、订阅、取消订阅、接收和发送消息，以便在 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)与 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)之间进行实时消息传递和构建物联网应用。

## 选择最适合 PHP 的 MQTT 客户端库

对于本教程，我们将使用 `php-mqtt/client` 库，这是在 Composer 下载量最高的库之一。它是一个可靠且易于使用的解决方案，用于将 MQTT 集成到 PHP 应用程序中。如果您正在寻找适用于 PHP 的 MQTT 客户端库，可以在 [Packagist](https://packagist.org/search/?query=mqtt) 上探索更多选项。

MQTT 通信属于 HTTP 之外的网络通信场景。由于 PHP 特性限制，使用 PHP 体系中用于网络通信的扩展如 Swoole 和 Workerman 可以带来更好的体验，其使用本文不再赘述，相关 MQTT 客户端库如下：

- [workerman/mqtt](https://packagist.org/packages/workerman/mqtt)：基于 workerman 的异步 MQTT 客户端。
- [simps/mqtt](https://packagist.org/packages/simps/mqtt)：[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 解析及 PHP 协程客户端。

## 设置 PHP 项目以进行 MQTT 集成

### 确认 PHP 版本

首先，请确保您使用的是 PHP 7.4.21 或更高版本。您可以在终端运行以下命令来检查 PHP 版本：

```shell
php --version

PHP 7.4.21 (cli) (built: Jul 12 2021 11:52:30) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.21, Copyright (c), by Zend Technologies
```

### 使用 Composer 安装 php-mqtt/client 库

Composer 是一个强大的 PHP 依赖管理工具，它简化了 PHP 项目所需库的安装过程。

安装 php-mqtt/client 客户端，请运行以下命令：

```shell
composer require php-mqtt/client
```

## 准备 MQTT Broker

本文将使用 EMQX 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker：`broker.emqx.io` 
- TCP 端口：**1883**
- SSL/TLS 端口：**8883**

有关更多信息，请查看：[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。

## PHP MQTT 使用指南

#### 导入 composer autoload 文件和 php-mqtt/client

```php
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
```

#### 设置 MQTT Broker 连接参数

设置 MQTT Broker 的连接地址、端口、客户端 ID、用户名和主题。同时，我们调用 PHP `rand` 函数随机生成 MQTT 客户端 ID。

```php
$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = 'public';
$clean_session = false;
$mqtt_version = MqttClient::MQTT_3_1_1;
```

#### 编写 MQTT 连接参数

使用上述的参数进行连接，可以通过 `ConnectionSettings` 设置连接参数：

```php
$connectionSettings = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);
```

### 订阅

编写代码订阅 `emqx/test` 主题，并为该订阅配置回调函数以处理接收到的消息。这里我们将订阅得到的主题和消息打印出来：

```php
$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);
```

### 发布

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

// The client loop to process incoming messages and retransmission queues
$mqtt->loop(true);
```

### 完整代码

以下是连接、发布和订阅 MQTT 代理的完整 PHP 代码：

```php
<?php

require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;

$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = 'public';
$clean_session = false;
$mqtt_version = MqttClient::MQTT_3_1_1;

$connectionSettings = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);


$mqtt = new MqttClient($server, $port, $clientId, $mqtt_version);

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

```shell
php pubsub_tcp.php
```

![PHP MQTT 测试](https://assets.emqx.com/images/61618d56823886f101feaf6741a20c3f.png)

## 总结

在本教程中，我们演示了如何使用PHP 中的 **php-mqtt/client** 库连接到 MQTT 代理、发布和订阅主题以及接收实时消息。这是使用 PHP 和 MQTT 构建实时应用程序的基础步骤。

更多有关 MQTT 教程，请查看我们的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide) 系列，探索更多 MQTT 的高级应用。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
