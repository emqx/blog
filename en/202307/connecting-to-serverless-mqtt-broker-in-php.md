Serverless architecture in cloud computing allows developers to focus on code development and deployment without the hassle of infrastructure management. Serverless MQTT, in particular, provides an MQTT messaging service that scales automatically based on demand, reducing the need for manual intervention.

To learn more about serverless MQTT, read our blog post [Next-Gen Cloud MQTT Service: Meet EMQX Cloud Serverless](https://www.emqx.com/en/blog/next-gen-cloud-mqtt-service-meet-emqx-cloud-serverless). In this blog series, we'll guide you through using various client libraries to set up MQTT connections, subscriptions, messaging, and more with a serverless MQTT broker for your specific project.

## Introduction

PHP is a server-side scripting language primarily used for web development. For IoT applications, PHP can also be used to build the backend infrastructure and process data.

The [php-mqtt client](https://github.com/php-mqtt/client) is an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) that enables you to connect to an MQTT broker, publish messages, and subscribe to topics. This blog will use the php-mqtt client to connect a serverless MQTT broker. The whole project can be downloaded at [MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-PHP).

## Free Serverless MQTT Broker

[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is the latest [MQTT broker](https://www.emqx.io/) offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. Additionally, users can get 1 million free session minutes every month, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

If you have not tried serverless deployment yet, please follow [the guide in this blog](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to create one for free. Once you have completed the registration process with the online guide, you will get a running instance with the following similar information from the “Overview” in your deployment. We will use the connection information and CA certificate later.

![EMQX MQTT Cloud](https://assets.emqx.com/images/b7f54f0922422779d30df5ede63e66fb.png?imageMogr2/thumbnail/1520x)

## Connection Code Demo

### 1. Install PHP and MQTT client

If you don’t have a PHP environment on your computer yet, please follow the [official document](https://www.php.net/manual/en/install.php) to install PHP. Then you can use composer to install the php-mqtt client. Composer is a dependency management tool for PHP, which can manage all the dependencies your PHP project needs.

```php
composer require php-mqtt/client
```

### 2. Import MQTT dependency

To use the php-mqtt Client library in your PHP application, add the following dependency to your PHP file:

```php
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;
```

### 3. Connection settings

To configure the connection settings, you need to specify the broker, port, topic, client ID, username, and password.

```php
$server   = '******.emqxsl.com';
// TLS port
$port     = 8883;
$clientId = rand(5, 15);
$username = 'emqxtest';
$password = '******';
$clean_session = false;

$connectionSettings  = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setConnectTimeout(3)
  ->setUseTls(true)
  ->setTlsSelfSignedAllowed(true);
```

Please replace the connection parameters with your EMQX connection information and login credentials.

- Broker and port: Obtain the connection address and port information from the server deployment overview page.
- Topic: Topics are used to identify and differentiate between different messages, forming the basis of MQTT message routing.
- Client ID: Every MQTT client must have a unique client ID. You can call the PHP `rand` function to generate the MQTT client id randomly.
- Username and password: To establish a client connection, please make sure that you provide the correct username and password. The following image shows how to configure these credentials under 'Authentication & ACL - Authentication' on the server side.

### 4. Using TLS/SSL

When connecting to EMQX Serverless, it is important to note that it relies on a multi-tenant architecture, which enables multiple users to share a single EMQX cluster. In order to ensure the security and reliability of data transmission within this multi-tenant environment, TLS is required. 

To enable TLS, use `setUseTls(true)` when creating a new ConnectionSettings.

```php
$connectionSettings  = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setConnectTimeout(3)
  ->setUseTls(true)
  ->setTlsSelfSignedAllowed(true);
```

### 5. Connect to the broker

To establish a connection and start sending and receiving messages, simply use the `connect` method of the MQTT client.

```php
$mqtt = new MqttClient($server, $port, $clientId, MqttClient::MQTT_3_1_1);
$mqtt->connect($connectionSettings, $clean_session);
```

### 6. Subscribe

Next, you can subscribe to the topic of php/mqtt and configure a callback function to process the received message. Here, we print the topic and message obtained from the subscription:

```php
$mqtt->subscribe('php/mqtt', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);
```

### 7. Publish

Create a payload and then call the publish function to publish messages to the "php/mqtt" topic. After publishing, the client must enter polling status to process incoming messages and the retransmission queue.

```php
$payload = array(
  'from' => 'php-mqtt client',
  'date' => date('Y-m-d H:i:s')
);
$mqtt->publish('php/mqtt', json_encode($payload), 0);
```

### 8. Unsubscribe

Use the following codes to unsubscribe to topics.

```php
$mqtt->unsubscribe('php/mqtt');
```

### 9. Disconnect

To disconnect, call:

```php
$mqtt->disconnect();
```

## Test

After running the MQTT broker connection code, you should see that the client has successfully connected and the messages have been published and received without issue.

![Receive message](https://assets.emqx.com/images/2aeeecff7b025f61aac9e59d8198a6ab.png)

You can also use [MQTTX](https://mqttx.app/), an MQTT client tool, to test the connection. By subscribing to the "php/mqtt" topic in MQTTX, you also receive messages published by the PHP application.

![MQTTX](https://assets.emqx.com/images/0fc1df1d99b7aeb549360eae25a0577e.png)

When you publish a message to the `php/mqtt` topic, you will see the message appear simultaneously in both MQTTX and the console.

![Receive message in console](https://assets.emqx.com/images/a5f5b68f54a404f9895d2e2d64e9a817.png)

![Receive message in MQTTX](https://assets.emqx.com/images/a64c2368a65068bc08ccdf71ebf9c368.png)

## Complete Code

The following code shows how to connect to the server, subscribe to topics, and publish and receive messages. For a complete demonstration of all functions, see the project's [GitHub repository](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-PHP).

```php
<?php

require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;

$server   = 'qbc11278.ala.us-east-1.emqxsl.com';
// TLS port
$port     = 8883;
$clientId = rand(5, 15);
$username = 'emqxtest';
$password = '123456';
$clean_session = false;

$connectionSettings  = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setConnectTimeout(3)
  ->setUseTls(true)
  ->setTlsSelfSignedAllowed(true);

$mqtt = new MqttClient($server, $port, $clientId, MqttClient::MQTT_3_1_1);

$mqtt->connect($connectionSettings, $clean_session);

$mqtt->subscribe('php/mqtt', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);

$payload = array(
  'from' => 'php-mqtt client',
  'date' => date('Y-m-d H:i:s')
);
$mqtt->publish('php/mqtt', json_encode($payload), 0);

$mqtt->loop(true);
```

## Summary

This blog provides a step-by-step guide on connecting to a serverless MQTT deployment in PHP. By following these instructions, you have successfully created a PHP application capable of publishing and subscribing to Serverless MQTT. For more ways to connect to [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) in PHP, please refer to the tutorial blog [How to Use MQTT in PHP](https://www.emqx.com/en/blog/how-to-use-mqtt-in-php) .

## Join the EMQ Community

To dive deeper into this topic, explore our[ GitHub repository](https://github.com/emqx/emqx) for the source code, join our [Discord](https://discord.com/invite/xYGf3fQnES) for discussions, and watch our [YouTube tutorials](https://www.youtube.com/@emqx) for hands-on learning. We value your feedback and contributions, so feel free to get involved and be a part of our thriving community. Stay connected and keep learning!



<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
