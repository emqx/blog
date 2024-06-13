## What Is Zigbee?

Zigbee is a high-level communication protocol designed to facilitate wireless communication in low-power devices. It was approved as an IEEE standard in 2004, and has since evolved into three related standards: Zigbee PRO, Zigbee RF4CE and Zigbee IP. The Zigbee network protocol is primarily used in applications such as home automation, smart energy, and telecommunication services.

Zigbee enables communication between devices such as smart thermostats, lighting controls, and security systems within short distances. It uses a mesh network architecture, which means every node or device in the network can communicate with any other device, as long as they are in range and a full mesh topology is used. In a partial mesh topology, only certain nodes can connect to all, while other nodes connect only to those they frequently exchange data with.

This is part of a series of articles about [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

## What Is Zigbee2MQTT?

Zigbee2MQTT is a project that utilizes the MQTT (Message Queuing Telemetry Transport) protocol to bridge the gap between Zigbee devices and your home automation system. MQTT is a lightweight messaging protocol designed for constrained devices and low-bandwidth, high-latency, or unreliable networks.

Zigbee2MQTT allows your Zigbee devices to communicate with your home automation system via MQTT. This means that you can control all your Zigbee devices from a single platform, regardless of their manufacturer. Zigbee2MQTT is open source software, meaning anyone can contribute to its development and benefit from its use.

The key advantage of Zigbee2MQTT is that it eliminates the need for proprietary Zigbee bridges or gateways. You can use a cheap, generic Zigbee USB adapter to control all your Zigbee devices. This reduces cost and enhances the versatility of your home automation system.

## Zigbee2MQTT Benefits

Here are the key benefits of using Zigbee2MQTT instead of other, proprietary bridges:

### Cloud Independence

Most Zigbee devices require you to connect to the manufacturer's cloud service for control and automation. This limits your control over your devices while raising privacy and security concerns. With Zigbee2MQTT, all data stays within your local network, giving you complete control over your devices and data.

### Broad Device Support

Zigbee2MQTT supports over 3,000 devices from different manufacturers (see the [official list](https://www.zigbee2mqtt.io/supported-devices/)). Whether it's a smart light bulb from Philips or a smart switch from Xiaomi, Zigbee2MQTT can handle it. This broad device support allows you to choose devices based on your preference and budget, rather than being limited to a specific manufacturer.

### Flexibility

Zigbee2MQTT provides you with the flexibility to customize and automate your devices. You can create complex automation rules, integrate with other services, and develop your own applications using the MQTT protocol.

**Related content: Read our guide to** **[MQTT security](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security)**

## Getting Started with Zigbee2MQTT  

There are different ways to run Zigbee2MQTT, for this guide, Docker and Docker Compose will be utilized.

### Find the Zigbee-Adapter

**USB Zigbee adapter**

After plugging in the adapter, use the dmesg command to locate the device.

```
$ sudo dmesg
```

The output should look something like this:

```
usbcore: registered new interface driver ch341
usbserial: USB Serial support registered for ch341-uart
ch341 3-1:1.0: ch341-uart converter detected
usb 3-1: ch341-uart converter now attached to ttyUSB0
```

**Network Zigbee adapter**

Zigbee2MQTT supports mDNS autodiscovery feature for network Zigbee adapters. If your network Zigbee adapter supports mDNS, you do not need to know the IP address of your network Zigbee adapter, Zigbee2MQTT will detect it and configure. For adapters that do not support mDNS, you need to know the network Zigbee adapter's IP address.

### Setup and Start Zigbee2MQTT

Assuming a recent version of Docker and Docker Compose is installed, create a folder for the project and save the docker-compose.yml file in it. This file defines how Docker runs the containers.

```
$ mkdir folder-name
```

Here is an example of what the docker-compose.yml file could look like:

```
version: '3.3'
services:
  mqtt:
    image: eclipse-mosquitto:2.0
    restart: unless-stopped
    volumes:
      - "./mosquitto-data:/mosquitto"
    ports:
      - "1883:1883"
      - "9001:9001"
    command: "mosquitto -c /mosquitto-no-auth.conf"

  zigbee2mqtt:
    container_name: zigbee2mqtt
    restart: unless-stopped
    image: koenkk/zigbee2mqtt
    volumes:
      - ./zigbee2mqtt-data:/app/data
      - /run/udev:/run/udev:ro
    ports:
      - 8080:8080
    environment:
      - TZ=Europe/Berlin
    devices:
           - /dev/ttyUSB0:/dev/ttyUSB0
```

### Connect a Device

After the Zigbee2MQTT installation and setup are complete, the next step is to connect a device. Look up your device in the supported devices and follow the pairing instructions. If no instructions are available, the device may be paired by factory resetting it.

```
Zigbee2MQTT:info 2019-11-09T12:19:56: Successfully interviewed '0x00158d0001dc126a', device has successfully been paired
```

**Important Note:** It's crucial to set permit_join to false in your configuration.yaml after the initial setup is done to secure your Zigbee network and to prevent accidental pairing of other Zigbee devices.

## MQTT Zigbee with EMQX

Zigbee has a wide range of applications in fields such as smart home and industrial manufacturing. Zigbee2MQTT allows you to manage Zigbee devices uniformly with the help of an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), and also makes it possible for Zigbee devices to work in cooperation with MQTT devices. In order for Zigbee devices and MQTT devices to communicate stably and efficiently, a reliable MQTT broker is necessary.

[EMQX](https://github.com/emqx/emqx), as a high-performance, scalable open-source MQTT broker, can easily handle a large number of concurrent connections and message throughput, and ensure millisecond-level message latency. Even on machines with limited resources like Raspberry Pi, you can easily install and run EMQX. In addition, EMQX provides a wealth of APIs and management interfaces, which makes it easy for you to monitor system status, manage clients and topics, and even dynamically adjust configurations to cope with constantly changing business needs.

These features make EMQX an ideal choice for the Zigbee2MQTT project. Visit our [official website](https://www.emqx.com/en) to learn more.


**Related Resources**

- [Home Assistant and MQTT: 4 Things You Could Build](https://www.emqx.com/en/blog/home-assistant-and-mqtt-4-things-you-could-build)
- [MQTT with openHAB: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/set-up-emqx-cloud-mqtt-broker-with-openhab)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
