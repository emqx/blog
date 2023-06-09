[PHP](https://www.php.net) 是一种被广泛应用的开放源代码的多用途脚本语言，它可嵌入到 HTML 中，尤其适合 Web 开发。

[MQTT](https://mqtt.org/) 是一种基于发布/订阅模式的轻量级物联网消息传输协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

本文主要介绍如何在 PHP 项目中使用 `php-mqtt/client` 客户端库 ，实现 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、取消订阅、收发消息等功能。


## MQTT 客户端库选择

`php-mqtt/client` 是 composer 上下载量最高的 PHP-MQTT [客户端库](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)，更多客户端库可以在 [Packagist - Search MQTT](https://packagist.org/search/?query=mqtt) 中查看。

有关 php-mqtt/client 更多使用文档请参阅 [Packagist php-mqtt/client](https://packagist.org/packages/php-mqtt/client)。

MQTT 通信属于 HTTP 体系之外的网络通信场景，由于 PHP 特性限制，使用 PHP 体系中的 Swoole/Workerman 等专为网络通信打造的拓展可以带来更好的体验，其使用本文不再赘述，相关的 MQTT 客户端库如下：

- [workerman/mqtt](https://packagist.org/packages/workerman/mqtt)：Asynchronous MQTT client for PHP based on workerman.
- [simps/mqtt](https://packagist.org/packages/simps/mqtt)：MQTT Protocol Analysis and Coroutine Client for PHP.


## 项目准备

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

## 准备 MQTT Broker

在继续之前，您需要一个 MQTT Broker 进行通信和测试。你可以通过一下方式获取 MQTT Broker：

- **私有部署**

  [EMQX](https://www.emqx.io/) 是应用于物联网、工业物联网和车联网的最具可扩展性的开源 MQTT Broker。您可以通过以下 Docker 命令来安装 EMQX：

  ```bash
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **云服务**

  使用云服务是启动 MQTT 服务的最简单方法。借助 [EMQX Cloud](https://www.emqx.com/zh/cloud)，您从阿里云、华为云、腾讯云等 20+ 个区域中选择并快速创建一个 MQTT 服务，实现快速连接。

  最新版本 [EMQX Serveless](https://www.emqx.com/zh/cloud/serverless-mqtt) 提供永久免费的提供每月100 万分钟会话时长和1GB 流量额度，让开发人员在几秒钟内轻松创建 MQTT 服务并进行长期测试。

- **免费公共 MQTT 服务器**

  免费的公共 MQTT 代理仅适用于那些希望学习和测试 MQTT 协议的人。避免在生产环境中使用它非常重要，因为它可能会带来安全风险和停机问题。

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

有关更多信息，请查看： [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。

## PHP MQTT 使用指南

#### 导入 composer autoload 文件和 php-mqtt/client

```php
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
```

#### 设置 MQTT Broker 连接参数

设置 MQTT Broker 连接地址，端口，客户端 ID，用户名以及 topic，这里我们调用 PHP `rand` 函数随机生成 MQTT 客户端 ID，避免与其他客户端 ID 重复。

```php
$server   = 'broker-cn.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = null;
$clean_session = false;
```

使用上述的参数进行连接，通过 `ConnectionSettings` 设置连接参数：

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

// 断开 MQTT 连接
// $client->disconnect();
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

// 断开 MQTT 连接
// $client->disconnect();
```


## 测试

运行 MQTT 消息发布代码，我们将看到客户端已经成功连接，且消息已经逐条发布并接收成功：

```bash
php pubsub_tcp.php
```

![PHP MQTT 测试](https://assets.emqx.com/images/61618d56823886f101feaf6741a20c3f.png)

## 总结

至此，我们完成了使用 **php-mqtt/client** 客户端连接到[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。

接下来，读者可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

