[PHP](https://www.php.net/) is a widely-used open-source scripting language that is especially suitable for web development and can be embedded in HTML. It enables developers to build dynamic web applications with ease.

In this guide, we’ll walk you through using the `php-mqtt/client` library to integrate **[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)** into your PHP applications. You’ll learn how to implement essential MQTT functions such as connecting, subscribing, unsubscribing, receiving, and sending messages between the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for real-time messaging and IoT applications.

## **Choosing the Best MQTT Client Library for PHP** 

For this tutorial, we'll use the **php-mqtt/client** library, which has the highest number of downloads on **Composer**. It’s a reliable, easy-to-use solution for integrating **MQTT** into PHP applications. If you’re looking for other MQTT client libraries for PHP, you can explore more options on [Packagist](https://packagist.org/search/?query=mqtt).

MQTT communication belongs to a network communication scenario outside the HTTP system. Due to the limitation of PHP characteristics, using the extensions for network communication such as Swoole/Workerman in the PHP system can bring a better experience. Its use will not be repeated in this article. The relevant MQTT client libraries are as follows:

- [workerman/mqtt](https://packagist.org/packages/workerman/mqtt)：Asynchronous MQTT client for PHP based on workerman.
- [simps/mqtt](https://packagist.org/packages/simps/mqtt)：[MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) Analysis and Coroutine Client for PHP.

## **Setting Up Your PHP Project for MQTT Integration** 

### Confirm the PHP Version

To get started, ensure that you are using PHP version 7.4.21 or higher. You can check your PHP version by running the following command in your terminal:

```php
php --version

PHP 7.4.21 (cli) (built: Jul 12 2021 11:52:30) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.21, Copyright (c), by Zend Technologies
```

### **Install the** `php-mqtt/client` **Library with Composer** 

Composer is a powerful dependency management tool for PHP that simplifies the installation of required libraries for your PHP projects.

To install the **php-mqtt/client** library, run the following command:

```shell
composer require php-mqtt/client 
```

## PHP MQTT Usage

### Connect to the MQTT Broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX, which is created on EMQX [MQTT Platform](https://www.emqx.com/en/cloud). The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

#### Import composer autoload file and `php-mqtt/client`

```shell
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
```

#### Set MQTT Broker connection parameters

Set the MQTT Broker connection address, port and topic. At the same time, we call the PHP `rand` function to generate the MQTT client id randomly.

```php
$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = 'public';
$clean_session = false;
$mqtt_version = MqttClient::MQTT_3_1_1;
```

#### Write the MQTT connection function

Use the above parameters to connect, and set the connection parameters through `ConnectionSettings`, such as:

```php
$connectionSettings = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);
```

### Subscribe

Program to subscribe to the topic of `emqx/test`, and configure a callback function for the subscription to process the received message. Here we print out the topic and message obtained from the subscription:

```php
$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);
```

### Publish

Construct a payload and call the `publish` function to publish messages to the `emqx/test` topic. After publishing, the client needs to enter the polling status to process the incoming messages and the retransmission queue:

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

### Complete Code

Here’s the full PHP code to connect, publish, and subscribe to the MQTT broker:

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

## Test

After running the MQTT message publishing code, we will see that the client has successfully connected, and the messages have been published one by one and received successfully:

```shell
php pubsub_tcp.php 
```

![PHP MQTT Test](https://assets.emqx.com/images/61618d56823886f101feaf6741a20c3f.png)

## **Summary and Next Steps** 

In this tutorial, we demonstrated how to use the **php-mqtt/client** library in PHP to connect to an MQTT broker, publish and subscribe to [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), and receive real-time messages. This is a foundational step for building powerful, real-time applications using PHP and MQTT.

For more advanced MQTT tutorials, check out our [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series to explore more advanced applications of MQTT.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
