## Introduction to MQTT and Raspberry Pi

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol crucial for IoT (Internet of Things) applications. It facilitates efficient communication between devices using a publish-subscribe model, enabling scalability, low bandwidth usage, reliability, flexibility, and interoperability. 

Raspberry Pi is a credit-card-sized single-board computer developed by the Raspberry Pi Foundation, initially intended to promote computer science education. However, its affordability, versatility, and low power consumption have made it immensely popular in IoT applications.

## Use Cases of Using MQTT on Raspberry Pi

Projects deployed on Raspberry Pi extend MQTT's reach, making IoT development accessible to a broader audience.

1. **Home Automation:** With MQTT, you can control and automate smart home devices such as lights, thermostats, door locks, and security systems connected to the Raspberry Pi. This enables personalized home automation solutions tailored to your preferences.
2. **Remote Monitoring and Control:** You can remotely monitor and control Raspberry Pi-connected devices over the internet using MQTT. This is useful for scenarios like checking home security cameras, adjusting thermostat settings, or receiving notifications from IoT sensors while away from home.
3. **Low-Cost Solution:** Raspberry Pi offers a cost-effective solution for deploying an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) compared to dedicated hardware or cloud services. This makes it accessible for DIY projects, small businesses, and educational institutions with budget constraints.

## What is NanoMQ

[NanoMQ](https://nanomq.io/) is an ultra-lightweight and blazing-fast Messaging broker/bus for IoT edge & SDV written in C， which is suitable for resource-constrained devices like Raspberry Pi.

The advantages of using NanoMQ on Raspberry Pi are as below:

1. **Lightweight and Efficient**: NanoMQ is designed to be lightweight, minimizing resource consumption on Raspberry Pi, which is particularly beneficial for devices with limited processing power and memory.
2. **Ease of Deployment**: NanoMQ's simplicity makes it easy to install and configure on Raspberry Pi, allowing for quick setup and deployment of MQTT broker functionality without extensive technical expertise.
3. **Low Latency Communication**: NanoMQ prioritizes low-latency communication, ensuring fast and responsive data exchange between IoT devices connected to the Raspberry Pi, ideal for time-sensitive applications.
4. **Compatibility**: NanoMQ is compatible with a wide range of MQTT clients and libraries, enabling seamless integration with various IoT devices and platforms and making it versatile for diverse IoT projects.
5. **Scalability**: Despite its lightweight nature, NanoMQ offers scalability, allowing it to handle increasing numbers of connected devices and messages as IoT deployments grow, making it suitable for both small-scale and large-scale applications.
6. **Community Support**: While NanoMQ is lightweight, it benefits from an active community of developers who contribute to its improvement, providing ongoing support, updates, and enhancements, ensuring its reliability and stability over time.
7. **Cost-Effectiveness**: NanoMQ is open-source software, eliminating licensing fees and reducing overall project costs, making it an economical choice for IoT projects deployed on Raspberry Pi.

## Set up Raspberry Pi for MQTT Broker Deployment

1. First, choose your raspberry. Here, we use Raspberry Pi 4b as an example.
2. Install the OS. You can install Debian, Raspberry Pi OS, or any other Linux-based OS you choose.
3. SSH and login, or just open a terminal.

## Install and Configure NanoMQ MQTT Broker

### Install NanoMQ

Download a package [here](https://github.com/nanomq/nanomq/releases).

Raspberry has an arm64 CPU. So we choose this [package](https://github.com/nanomq/nanomq/releases/download/0.21.8/nanomq-0.21.8-linux-arm64-full.deb).

```shell
$ wget https://github.com/nanomq/nanomq/releases/download/0.21.8/nanomq-0.21.8-linux-arm64-full.deb
```

Then install this package via apt.

```shell
$ sudo apt install ./nanomq-0.21.8-linux-arm64-full.deb
```

We now finished the installation.

```shell
$ nanomq --version

Usage: nanomq { start | stop | restart | reload } [--help]

NanoMQ Messaging Engine for Edge Computing & Messaging bus v0.21.8-8
Copyright 2023 EMQ Edge Computing Team
```

### Configuration

Here, we edit the configuration file of NanoMQ `/etc/nanomq.conf`. In this configuration, NanoMQ will listen to `1883` port and accept ***tcp*** connections. It will also listen on port 8883 to accept TLS connections and port 8083 to accept WebSocket connections. The log will be printed to `/tmp/nanomq.log` and console.

```shell
 vim /etc/nanomq.conf
```

```
listeners.tcp {
    bind = "0.0.0.0:1883"
}

listeners.ssl {
	bind = "0.0.0.0:8883"
	keyfile = "/etc/certs/key.pem"
	certfile = "/etc/certs/cert.pem"
	cacertfile = "/etc/certs/cacert.pem"
	verify_peer = false
	fail_if_no_peer_cert = false
}

listeners.ws {
    bind = "0.0.0.0:8083/mqtt"
}

log {
    to = [file, console]
    level = info
    dir = "/tmp"
    file = "nanomq.log"
}
```

Start NanoMQ.

```shell
nanomq start --conf /etc/nanomq.conf
```

For more information about the configuration of NanoMQ, please refer to: [NanoMQ Docs](https://nanomq.io/docs/en/latest/config-description/introduction.html).

### Testing NanoMQ on Raspberry Pi

Open two additional terminals.

In terminal 1:

```shell
$ nanomq_cli sub -p 1883 -t topic1
```

In terminal 2:

```shell
$ nanomq_cli pub -p 1883 -t topic1 -m "Hello-NanoMQ"
```

If the nanomq_cli in terminal 1 gets the message Hello-NanoMQ, it shows that you have deployed NanoMQ on Raspberry Pi successfully.

## FAQ

### Can NanoMQ be installed on Raspberry Pi 1, 1B, and 2?

Yes. But no GitHub releases were provided. You need to cross compile NanoMQ by yourself. The tutorial on cross-compile can be found here: [How to Install a Scalable MQTT Broker on OpenWRT](https://www.emqx.com/en/blog/how-to-install-a-scalable-mqtt-broker-on-openwrt) 

### What are the hardware and OS requirements of NanoMQ?

NanoMQ requires at least 10MB of memory. It can be deployed on any POSIX-compatible operation system. 

## Conclusion

In wrapping up, we've covered the essential intersection of MQTT and Raspberry Pi for IoT projects. We've seen how MQTT facilitates efficient communication, while Raspberry Pi serves as an accessible and versatile platform.

Deploying an MQTT broker like NanoMQ on Raspberry Pi offers significant advantages, from local processing to scalability. With NanoMQ's lightweight design and ease of deployment, it's an excellent choice for Raspberry Pi-based projects.

Now equipped with the know-how, it's time for you to explore, experiment, and implement your MQTT projects on Raspberry Pi.


## Resources

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Using MQTT on ESP8266: A Quick Start Guide](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
