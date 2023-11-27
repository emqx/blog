## Introduction

This blog will introduce how to use Neuron to collect data from [KNX](https://www.emqx.com/en/blog/knx-protocol) devices, upload the collected data to EMQX, and view it using MQTTX.

We will use a Linux machine for installing EMQX, MQTTX, and Neuron. As ETS and KNX Virtual only support Windows, we run a Windows VM to simulate KNX installation. 


![The Architecture of KNX to MQTT Bridging](https://assets.emqx.com/images/94d52d2aba496120411cc0d02bde8ad7.png)


## EMQX Quick Start

EMQX provides multiple installation methods, and users can check the detailed installation methods in the [documentation](https://www.emqx.io/docs/en/v5.0/deploy/install.html). This example uses container deployment to quickly experience EMQX.

Run the following command to obtain the Docker image:

```
docker pull emqx/emqx:5.1.0
```

Run the following command to start the Docker container:

```
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

Access the EMQX Dashboard by visiting [http://localhost:8083/](http://localhost:18083/) (replace “localhost” with your actual IP address) through a web browser. This allows you to manage device connections and monitor related metrics. Keep the Docker container running for this tutorial. You can refer to the [documentation](https://www.emqx.io/docs/en/v5.0/) to experience more features in the Dashboard.

Initial username: `admin`, initial password: `public`

## Setup KNX Virtual Using ETS

We need to [download and install KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php). There is a [blog tutorial](https://www.ets6.org/ets6-and-knx-virtual/) on how to simulate KNX installation using ETS and KNX Virtual, or if you prefer, a video tutorial [KNX Virtual Basics](https://www.youtube.com/watch?v=01MO_zmtGv4).

To keep things simple, we will simulate a KLiX (D0), a dimming actuator (D0), a blinds/shutter actuator (D2) and a switch actuator (D7) in KNX Virtual. The association between addresses and group objects is shown in the following image.

![KNX Virtual](https://assets.emqx.com/images/6d36e1efa508eca48c39832c7954f57c.png)

## Neuron Quick Start

Consult the [installation instruction](https://neugates.io/docs/en/latest/installation/installation.html) on how to install Neuron. After Neuron is installed, you can access the dashboard through your browser at [http://localhost:7000](http://localhost:7000/) (replace "localhost" with your actual IP address).

### Step 1. Login

Log in with the initial username and password:

- Username: `admin`
- Password: `0000`

### Step 2. Add a south device

In the Neuron dashboard, click **Configuration ->  South Devices -> Add Device** to add an *knx* node.

![Add a south device](https://assets.emqx.com/images/769435a4caf26298e8e0cb924de59a20.png)

### Step 3. Configure the *knx* node

Configure the newly created *knx* node as the following image shows.

![Configure the *knx* node](https://assets.emqx.com/images/8b93dfd897e88acba6d51f129f0426d5.png)


### Step 4. Create a group in the *knx* node

Click the *knx* node to enter the **Group List** page, and click **Create** to bring up the **Create Group** dialog. Fill in the parameters and submit:

- Group Name: grp.
- Interval: 1000.

![Create a group in the *knx* node](https://assets.emqx.com/images/b3ce997da0687c578dfc8ed850744627.png)

### Step 5. Add tags to the group

Add four tags corresponding to the dimming actuator, shutter actuator and switch actuator in the KNX Virtual configuration.

![Add tags to the group](https://assets.emqx.com/images/17ecb2eba0fbbe000112872f8833e374.png)

### Step 6. Data monitoring

In the Neuron dashboard, click **Monitoring -> Data Monitoring**, and see that tag values are read correctly.

![Data monitoring 1](https://assets.emqx.com/images/8f5dd1e3c15a5c4a2f515e6e8c5b2e4f.png)

![Data monitoring 2](https://assets.emqx.com/images/2b09ae4a02367b3c2b8c3221902b6b06.png)

### Step 7. Add an MQTT North app

In the Neuron dashboard, click **Configuration ->  North Apps -> Add App** to add an *mqtt* node.

![Add an MQTT North app](https://assets.emqx.com/images/6dc854ceedafc6615e71b5fa275c1699.png)

### Step 8: Configure the *mqtt* node

Configure the *mqtt* node to connect to the EMQX broker set up earlier.

![Configure the *mqtt* node](https://assets.emqx.com/images/c6725171f15e8529492588ae3693af98.png) 

### Step 9. Subscribe the *mqtt* node to the *knx* node

Click the newly created *mqtt* node to enter the **Group List** page, and click **Add subscription**. After a successful subscription, Neuron will publish data to the topic `/neuron/mqtt/knx/grp`.

![Subscribe the *mqtt* node to the *knx* node](https://assets.emqx.com/images/b673b0c1b5b23f682065d2beab900d6d.png)

## View Data Using MQTTX

Now, you can use an MQTT client to connect to EMQX and view the reported data. Here, we use [MQTTX, a powerful cross-platform MQTT client tool](https://mqttx.app/), which can be downloaded from the [official website](https://www.emqx.com/en/products/mqttx).

Launch MQTTX, and add a new connection to the EMQX broker set up earlier, then add a subscription to the topic  `/neuron/mqtt/knx/grp`. After a successful subscription, you can see that MQTTX continues to receive data collected and reported by Neuron. As shown in the following figure.

![MQTTX](https://assets.emqx.com/images/9beb4e4d3514aff1b659067c42be9084.png)

## Conclusion

In this blog, we introduced the KNX protocol and demonstrated the overall process of bridging KNX data to MQTT using Neuron.

KNX provides a robust and flexible platform for home and building automation. Neuron, with its powerful connectivity for [Industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges), facilitates the data collection from KNX devices and seamless transmission of the acquired data to the cloud for convenient remote control and monitoring whenever necessary. 

Neuron also supports other industrial protocols like [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol), SIEMENS, and more. For more bridging tutorials, read our post: 

- [Bridging Modbus Data to MQTT for IIoT:  A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-modbus-data-to-mqtt-for-iiot#the-architecture-of-modbus-to-mqtt-bridging) 
- [Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot) 
- [Bridging TwinCAT Data to MQTT: Introduction and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-twincat-data-to-mqtt) 
- [Bridging FINS Data to MQTT: Protocol Explained and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-fins-data-to-mqtt) 



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
