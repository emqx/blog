Google Cloud will discontinue its IoT Core service on August 16, 2023, leaving IIoT companies with the need to find an alternative. 

Given that Google IoT Core is based on MQTT, the best alternative options for seamless migration undoubtedly are MQTT-based IoT messaging platforms or services. With its features of 100% compliant with MQTT 3.x/ 5.0, fully-managed MQTT service and deeply integrated with GCP, [EMQX Cloud](https://www.emqx.com/en/cloud) becomes one of the best choices for former IoT Core users.

In this series of articles, I will deliver a tutorial about the solution for migrating device connections from GCP IoT Core to EMQX Cloud with the same features equipped, and how to link with other cloud services to realize more business demands.

Let’s get started with the deployment creation of EMQX Cloud and devices connection.

## EMQX Cloud Introduction

With the infrastructure provided by cloud providers, EMQX Cloud serves dozens of countries and regions, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications. On the one side, millions of devices are connected to the scalable broker hosted on the cloud service in regions. On the other side, data were bridged to various application services for further processing and storing.

![MQTT Cloud](https://assets.emqx.com/images/ce56d176ffbe8d39129a7a1620e262fa.png)


## Create a cluster hosted on GCP

Assuming you have logged in to the EMQX Cloud Console, I will walk you through cluster deployment step by step. By the way, EMQX Cloud offers a 14-day free trial, with no credit card required. So feel free to explore all that you need.

1. Choose a plan. Standard Plan is up to 10,000 connections, mainly for data collection and transfer between the device to device or device to the application. It only can be deployed in AWS at present. If you need to integrate with other cloud services in GCP, we recommend Professional Plan provides up to more than 100,000 connections.

   ![Choose a plan](https://assets.emqx.com/images/f0b5addb555d1377108f8e2e8bbbc126.png)

2. Choose a region. We recommend choosing the region the same as your other services deployed in GCP. 

   ![Choose a region](https://assets.emqx.com/images/1145394df852bddc7fb61e442fb9dc12.png)

3. Then just click Next and wait for the deployment ready to use. 

   ![Click Next](https://assets.emqx.com/images/79bfab07012d1b2880112db7a694ec8d.png)


## Connect address and connect port

To connect a device to EMQX Cloud is quite simple. In the deployment console, The most important connection information is displayed in the deployment overview.

![connection information](https://assets.emqx.com/images/30d704e217bcbd76e403e1d387dfcf2c.png)

- Cluster status: status and running time.
- Number of connections: current number of connections, and the maximum number of device connections supported.
- Pub&Sub TPS: The peak value contains the total number of messages sent and received per second.
- Deployment name: the name of the deployment, which can be modified by clicking the edit button on the right.
- Connection address: IP address for MQTT connection
- Connection port: 1883(mqtt), 8083(ws) are enabled by default, you can enable 8883(mqtts) and 8084(wss) through Configuring TLS/SSL


## Verify device credentials

The device credentials rely on username and password authentication in EMQX Cloud. 

- Set username and password in console or upload a CSV file that contains all the authentication information to console.
- The device uses a pair of username and password to sign in.

![Verify device credentials](https://assets.emqx.com/images/9daadb2d3b14fd8f8a06cc13081218e4.png)

In addition to username and password authentication, EMQX supports external authentication, you can verify device via HTTP, importing authentication information from database, and JWT.

![MQTT Authentication](https://assets.emqx.com/images/4e48dccf135d62622406c3990bb63d9a.png)

In GCP IoT Core, the device uses a private key to sign a JSON Web Token. The token is passed to Cloud IoT Core as proof of the device's identity. Then the topic needs to be registed in Pub/Sub before using in communication.

Compared to GCP IoT Core, connect to EMQX Cloud is simpler. The following samples illustrate how to set up configuration updates on a device over MQTT in Python:

```
# python 3.8

import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = '**********'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
```

 

More samples are in client connection guide.

![MQTT Client](https://assets.emqx.com/images/a747dda5132128ea061d9505e298cf0f.png)


## Upcoming

In the following articles, we will explore some advanced features in EMQX Cloud to adapt your current connection solution,  making your migration more seamless and business-non-affected.

- Use TLS over MQTT 

- Use JSON Web Token to verify device credentials

- Set up VPC and integrate data to GCP

Please stay tuned!


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


## Other articles in this series

- [Migrate Your Business from GCP IoT Core 02 | Enable TLS/SSL over MQTT to Secure Your Connection](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-02)
- [Migrate Your Business from GCP IoT Core 03｜Use JSON Web Token (JWT) to Verify Device Credentials](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-03)
- [Migrate Your Business from GCP IoT Core 04｜VPC Network Peering and Transfer Data to GCP](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-04)
