## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), a lightweight publish/subscribe messaging protocol, is well-known for its significant role in the realm of the Internet of Things (IoT). It excels at providing real-time and reliable messaging services for resource-constrained devices, even in low-bandwidth, high-latency, or network-unstable environments.

[lwIP](https://savannah.nongnu.org/projects/lwip/), a small independent TCP/IP protocol stack, also holds a place in the IoT domain for it can reduce resource usage, particularly memory, while still having a full-scale TCP. This makes it ideal for small embedded systems.

So, what kind of chemistry can we expect when we combine these two widely used [IoT protocols](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m), MQTT over lwIP? In this blog, we will implement a simple [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) using lwIP's MQTT library, providing a reference for those who want to develop MQTT services and applications based on lwIP.

## Introduction to lwIP

lwIP, "lightweight IP,” is a small independent implementation of the TCP/IP protocol suite. lwIP was initially developed by Adam Dunkels at the Computer and Networks Architectures (CNA) lab at the Swedish Institute of Computer Science (SICS) and is now developed and maintained by a worldwide network of developers. Due to its open-source nature and frequent updates, lwIP is widely discussed and used.

The focus of the lwIP TCP/IP implementation is to reduce resource usage. LwIP has designed its own memory and packet management mechanism, which requires only tens of kilobytes of free RAM and room for around 40 kilobytes of code ROM. This makes it well-suited for low-end embedded systems.

To reduce data copy and enhance transmission efficiency, lwIP does not strictly adhere to the standard layered structure. Every layer can interact with the same data packet directly, which can avoid data copy and effectively improve data transmission efficiency.

Compared to other protocol stacks, lwIP has the advantage that it can be ported to an operating system or run independently in a bare-metal environment. lwIP is feature-rich, supporting not only the basic TCP/IP but also various application protocols such as DNS, DHCP, and MQTT. Of course, these features can be selected by modularity, enabling developers to customize applications that meet specific requirements and optimize the utilization of limited system resources.

## Environment Setup

Although lwIP can run directly in a bare-metal system, it is more convenient to use lwIP with an OS, especially when there are abundant system resources. lwIP provides a set of interfaces related to OS. Developers can port lwIP easily by implementing these interfaces according to their platform.

To simplify the porting process, we use RT-Thread as the embedded operating system. RT-Thread integrates lwIP as the default TCP/IP protocol stack and offers rich board support packages, making development based on lwIP easier. We will use RT-Thread 4.1.1 and lwIP 2.1.2, with Raspberry Pi 4B as the development board. 

Before we get started, follow the official [documentation](https://github.com/RT-Thread/rt-thread/tree/master/bsp/raspberry-pi/raspi4-64) to boot RT-Thread. Make sure that the development board can connect to the Internet. In RT-Thread, the lwIP MQTT library is not enabled by default. You need to modify the SCons build script of RT-Thread by adding the following script in `rt-thread\components\net\lwip\lwip-2.1.2\Sconscript`.

```
src += lwipmqtt_SRCS
```

In addition, you need to allocate extra timeout memory blocks for MQTT in the lwIP memory pool. Modify the macros in `rt-thread\components\net\lwip\port\lwipopts.h` by adding the following macros and adding `+ LWIP_MQTT` at the end of `#define MEMP_NUM_SYS_TIMEOUT`.

```
#define LWIP_MQTT 8
```

## Coding

Create a new file `mqtt_client.c` in the directory `rt-thread\bsp\raspberry-pi\raspi4-64\applications`. 

We begin with connection establishment.

```cpp
void mqtt_client_do_connect(mqtt_client_t *client, int flag)
{
    struct mqtt_connect_client_info_t ci;
    memset(&ci, 0, sizeof(ci))
	/* Set MQTT client information including client id, username, password, and will message,
	 note that client id is required. */
    ci.client_id = "lwip_test";
	/* Initialize the client's connection to the MQTT server based on IP address determined by IP_ADDR
	 and register the SUB or PUB callback functions based on the flag. */
    /* IP_ADDR is used to initialize IP address format in lwIP. */
    ip_addr_t ip_addr;
    IP4_ADDR(&ip_addr, IP_ADDR0, IP_ADDR1, IP_ADDR2, IP_ADDR3);

    if (flag == FLAG_SUB) {
        mqtt_client_connect(client, &ip_addr, 1883, mqtt_connection_cb, NULL, &ci);
    } else if(flag == FLAG_PUB) {
        mqtt_client_connect(client, &ip_addr, 1883, mqtt_pub_connection_cb, NULL, &ci);
    }
}

```

Then, the callback function for the PUB connection. Note that `mqtt_pub_request_cb` is the callback function after `publish` is completed.

```cpp
static void mqtt_pub_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status)
{
    if (status == MQTT_CONNECT_ACCEPTED) {
        printf("mqtt_connection_cb: Successfully connected\\n");
        const char *pub_payload = "hello this is lwIP";
        err_t err;
        u8_t qos = 2;
        u8_t retain = 0;

        mqtt_publish(client, PUB_TOPIC, pub_payload, strlen(pub_payload), qos, retain, mqtt_pub_request_cb, arg);
    } else {
        printf("mqtt_connection_cb: Disconnected, reason: %d\\n", status);
    }
}
```

Next, the callback function for SUB connection. Note that `mqtt_sub_request_cb` is the callback function after the subscribe is completed. `mqtt_incoming_publish_cb` is the callback function triggered upon receiving publish messages to handle the topic, and `mqtt_incoming_data_cb` for handling the data. 


```cpp
static void mqtt_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status)
{
    if (status == MQTT_CONNECT_ACCEPTED) {
        printf("mqtt_connection_cb: Successfully connected\\n");
        /* Register the callback function for PUB messages */
        mqtt_set_inpub_callback(client, mqtt_incoming_publish_cb, mqtt_incoming_data_cb, arg);
        /* SUB */
        mqtt_subscribe(client, SUB_TOPIC, 1, mqtt_sub_request_cb, arg);
    } else {
        printf("mqtt_connection_cb: Disconnected, reason: %d\\n", status);
        /* Reconnect in case of connection failure */
        mqtt_client_do_connect(client, FLAG_SUB);
    }
}
```

You may feel confused about `mqtt_incoming_publish_cb` and `mqtt_incoming_data_cb`. Here is a detailed explanation. These two callbacks can be used as a filter. Take the process of receiving a message as an example. At first, we receive a pub message, and then we can set a flag for different topics in `mqtt_incoming_publish_cb`. Next, you can handle the data in the message according to the flag we set before in `mqtt_incoming_data_cb`. You can check the demo below that we can handle all topics starting with 'A' differently.

```cpp
static int inpub_id;
static void mqtt_incoming_publish_cb(void *arg, const char *topic, u32_t tot_len)
{
    printf("Incoming publish at topic %s with total length %u\\n", topic, (unsigned int)tot_len);
    if (topic[0] == 'A') {
        /* Handle all topics starting with 'A' in the same way */
        inpub_id = 1;
    } else {
        /* Handle all other topics differently */
        inpub_id = 2;
    }
    /* Handle in this demo */
    inpub_id = -1;
}

static void mqtt_incoming_data_cb(void *arg, const u8_t *data, u16_t len, u8_t flags)
{
    printf("Incoming publish payload with length %d, flags %u\\n", len, (unsigned int)flags);
    printf("mqtt payload: %s\\n", (const char *)data);
    if (flags & MQTT_DATA_FLAG_LAST) {
        /* Handle data based on the reference */
        if (inpub_id == -1) {
            /* No handling in this demo */
            return;
        } else if (inpub_id == 1) {
            /* Handling data with topics starting with 'A' */
        } else {
            printf("mqtt_incoming_data_cb: Ignoring payload...\\n");
        }
    } else {
        /* To handle payloads that are too long, save them in a buffer or a file. */
    }
}
```

The main function is the last one we need to mention. This is the user interface for the demo. It can be exported as a terminal command using the `MSH_CMD_EXPORT` macro provided by RT-Thread.


```cpp
static int mqttClient(int argc, char **argv)
{
    if (argc < 2) {
        print_help();
        return 0;
    }
    if (strcmp(argv[1], "sub") == 0) {
        // do sub
        mqtt_client_t *client = mqtt_client_new();
        if (client != NULL) {
            mqtt_client_do_connect(client, FLAG_SUB);
        }
    } else if (strcmp(argv[1], "pub") == 0) {
        // do pub
        mqtt_client_t *clientpub = mqtt_client_new();
        if (clientpub != NULL) {
            mqtt_client_do_connect(clientpub, FLAG_PUB);
        }
    } else {
        // error
        print_help();
    }
    return 0;
}

MSH_CMD_EXPORT(mqttClient, a simple mqtt client);
```

You can find the complete code in the repository [mqtt client over lwIP](https://github.com/OdyWayne/mqtt_client-over-lwIP).

## Test

In this blog, we use the MQTT 5.0 client tool - [MQTTX](https://mqttx.app/) for testing.

### Test Subscribed Messages

Step 1: Input the command in the terminal to subscribe to the message.

```
mqttClient sub
```

![terminal-sub](https://assets.emqx.com/images/3be33c9920abf965ebdf574f7dcbf5e9.png)

Step 2: Connect the MQTTX client to the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and send a message to the topic `lwip/sub`.

![MQTTX-sub](https://assets.emqx.com/images/fdbeb85a35c0b65db03427f29c787149.png)

Step 3: Check the development board terminal, and you will see that the message published by MQTTX has been successfully received.

![board-terminal](https://assets.emqx.com/images/6fb7f78a93cb894292c7a8b15f0d8132.png)

### Test Published Messages

Step 1: Subscribe to the topic `lwip/pub` in the MQTTX client.

Step 2: Input the command in the terminal to publish a message.

```
mqttClient pub
```

![terminal-pub](https://assets.emqx.com/images/95d6bf919f0858a0e986128023dcc11c.png)

Step 3: Then, you can see the message sent by the development board in the MQTTX client.

![MQTTX-publish](https://assets.emqx.com/images/0d8bc2ad24981b1031d51e2948639ada.png)

## Conclusion

In this blog, we established a simple MQTT client using the MQTT library of lwIP and performed PUB/Sub tests against an MQTT server. MQTT can provide reliable message delivery services and support massive connections with minimal code and limited bandwidth for remote devices. Likewise, lwIP can provide complete and reliable TCP/IP services with minimal resource usage. By combining these two, MQTT over lwIP can provide real-time and reliable message services for IoT devices, even in extremely resource-constrained environments.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
