## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 作为一种轻量级发布/订阅模式的消息传输协议，能够在低带宽、高延迟或不稳定的网络环境中为资源有限的物联网设备提供实时可靠的消息服务。[lwIP](https://savannah.nongnu.org/projects/lwip/) 作为一种同样轻量级的 TCP/IP 协议实现，能够减少对硬件资源尤其是内存资源的占用，同时又能提供完整的 TCP/IP 功能，这使得 lwIP 非常适合应用于小型嵌入式系统。那么将两个同样广泛应用于物联网的协议结合，MQTT over lwIP 会碰撞出怎样的火花呢？本文将通过 lwIP 提供的 MQTT 库实现一个简易的 [MQTT Client](https://www.emqx.com/en/blog/mqtt-client-tools)，为基于 lwIP 的 MQTT 服务与应用的开发提供借鉴与参考。

## lwIP 简介

lwIP（lightweight IP）意为轻量化 TCP/IP 协议，是由瑞典计算机科学院（Swedish Institute of Computer Science，SICS）的 Adam Dunkels 开发的一个小型开源的 TCP/IP 协议栈。lwIP开源的特性和快速的版本更新速率，使得其被广泛讨论并使用。lwIP 的实现重点是减少对 RAM 的使用，lwIP 设计了一套独立的内存和数据包管理机制，只需要几十 KB 的 RAM 和 40KB 左右的 ROM，使得其能够在低端嵌入式系统中使用。为了减少数据拷贝，提高传输的效率，lwIP 并没有采用严格的分层结构，而是假设各层之间是透明相互可见的，各层之间的数据可以共享而无需拷贝，这样做可以有效提高数据的传输效率。lwIP 相较于其他协议栈还有一个优势，即 lwIP 可以移植到操作系统上，也可以在无操作系统的环境下独立运行。lwIP 功能齐全，除了处理实现 TCP/IP 的基本通信功能外，lwIP 还支持 DNS、DHCP、MQTT 等应用功能。当然，这些功能都可以模块化地选择，使得开发者可以定制出符合特定需求的应用，有效地利用有限的系统资源。

## 环境搭建

lwIP 虽然可以直接运行在无操作系统的环境中，但是在系统资源相对充裕的情况下，基于操作系统的 lwIP 操作会更加简便。lwIP 在设计之初就提供了一套与操作系统相关的接口，开发者只需要根据操作系统的不同对lwIP 提供的接口进行完善即可。为了简化移植过程，本文使用了 RT-Thread 作为板载的操作系统。RT-Thread 将 lwIP 作为默认的 TCP/IP 协议栈，并提供了丰富的板级支持包，使得基于 lwIP 的开发变得容易。

本文基于 RT-Thread 4.1.1 和 lwIP 2.1.2 版本，并以树莓派 4B 作为开发板。首先通过官方的[说明文档](https://github.com/RT-Thread/rt-thread/tree/master/bsp/raspberry-pi/raspi4-64)将 RT-Thread 启动，并确保开发板可以连接到互联网。

RT-Thread 中的 lwIP MQTT 库默认并不可用，需要通过修改 RT-Thread 的 SCons 编译脚本打开。即在 `rt-thread\components\net\lwip\lwip-2.1.2\Sconscript` 中添加

```
src += lwipmqtt_SRCS
```

除此之外，需要在 lwIP 的内存池中给 MQTT 分配额外的 timeout 内存块。修改 `rt-thread\components\net\lwip\port\lwipopts.h` 中的宏。添加

```
#define LWIP_MQTT 8
```

并在 `#define MEMP_NUM_SYS_TIMEOUT` 最后添加 `+ LWIP_MQTT`。

## 代码编写

在 `rt-thread\bsp\raspberry-pi\raspi4-64\applications` 目录下新建文件 `mqtt_client.c`。

首先是连接建立函数。

```
void mqtt_client_do_connect(mqtt_client_t *client, int flag)
{
    struct mqtt_connect_client_info_t ci;
    memset(&ci, 0, sizeof(ci));
    /* 这里可以设置MQTT客户端的信息client id、username、password、willmsg等，其中client id是必须的 */ 
    ci.client_id = "lwip_test";
    /* 根据IP_ADDR确定MQTT服务器的地址，初始化客户端到服务器的连接。并根据flag确定注册SUB或者PUB的回调函数 */
    /* IP4_ADDR 用于初始化iwIP内部的ip地址格式*/
    ip_addr_t ip_addr;
    IP4_ADDR(&ip_addr, IP_ADDR0, IP_ADDR1, IP_ADDR2, IP_ADDR3);
    
    if (flag == FLAG_SUB) {
        mqtt_client_connect(client, &ip_addr, 1883, mqtt_connection_cb, NULL, &ci);
    } else if(flag == FLAG_PUB) {
        mqtt_client_connect(client, &ip_addr, 1883, mqtt_pub_connection_cb, NULL, &ci);
    }
}
```

PUB 连接的回调函数，其中 `mqtt_pub_request_cb` 是 publish 完成后的回调函数。

```
static void mqtt_pub_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status) 
{
    if (status == MQTT_CONNECT_ACCEPTED) {
        printf("mqtt_connection_cb: Successfully connected\n");
        const char *pub_payload = "hello this is lwIP";
        err_t err;
        u8_t qos = 2;
        u8_t retain = 0;
        
        mqtt_publish(client, PUB_TOPIC, pub_payload, strlen(pub_payload), qos, retain, mqtt_pub_request_cb, arg);
    } else {
        printf("mqtt_connection_cb: Disconnected, reason: %d\n", status);
    }
}
```

SUB 连接的回调函数，其中 `mqtt_sub_request_cb` 是 subscribe 完成后的回调函数。`mmqtt_incoming_publish_cb`，`mqtt_incoming_data_cb` 是收到 publish 消息后分别处理 topic 和 data 时触发的回调函数。

```
static void mqtt_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status) 
{
    if (status == MQTT_CONNECT_ACCEPTED) {
        printf("mqtt_connection_cb: Successfully connected\n");
        /* 为收到PUB消息注册回调函数 */
        mqtt_set_inpub_callback(client, mqtt_incoming_publish_cb, mqtt_incoming_data_cb, arg);
        /* SUB */
        mqtt_subscribe(client, SUB_TOPIC, 1, mqtt_sub_request_cb, arg);
    } else {
        printf("mqtt_connection_cb: Disconnected, reason: %d\n", status);
        /* 连接失败则重新连接 */
        mqtt_client_do_connect(client, FLAG_SUB);
    }
}
```

在处理 publish topic 时可以根据 topic 的不同设置不同的参照，并在之后依据参照对 publish data 作出不同的处理。

```
static int inpub_id;
static void mqtt_incoming_publish_cb(void *arg, const char *topic, u32_t tot_len)
{
    printf("Incoming publish at topic %s with total length %u\n", topic, (unsigned int)tot_len);
    if (topic[0] == 'A') {
        /* 所有以 'A' 开头的topic都以相同的方式处理 */
        inpub_id = 1;
    } else {
        /* 所有其他的topic的处理 */
        inpub_id = 2;
    }
    /* 在本次demo中的处理 */
    inpub_id = -1;
}

static void mqtt_incoming_data_cb(void *arg, const u8_t *data, u16_t len, u8_t flags)
{
    printf("Incoming publish payload with length %d, flags %u\n", len, (unsigned int)flags);
    printf("mqtt payload: %s\n", (const char *)data);
    if (flags & MQTT_DATA_FLAG_LAST) {
        /* 根据参考对data作出不同处理 */
        if (inpub_id == -1) {
            /* 在本次demo中不作处理 */
            return;
        } else if (inpub_id == 1) {
            /* 处理以'A'开头的topic数据 */
        } else {
            printf("mqtt_incoming_data_cb: Ignoring payload...\n");
        }
    } else {
        /* 处理过长payload，保存在buffer或文件中 */
    }
}
```

最后是主函数，可以通过 RT-Thread 提供的宏 `MSH_CMD_EXPORT`，将主函数输出作为终端的命令使用。

```
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

## 测试

使用 MQTT 5.0 客户端工具 - [MQTTX](https://mqttx.app/zh) 进行以下测试。

### 测试订阅消息

1. 在终端输入订阅消息命令。

   ```
   mqttClient sub
   ```

   ![在终端输入订阅消息命令](https://assets.emqx.com/images/a99fc4065bc10c28a857b621b6cad904.png)

2. 使用 MQTTX 客户端与 MQTT 服务器建立连接，并向主题 `lwip/sub` 发送消息。

   ![MQTTX 客户端](https://assets.emqx.com/images/671cf85470d5b8ca0d730792a10e33a7.png)

3. 查看开发板终端信息，将会看到已成功收到 MQTTX 发布的消息。

   ![查看开发板终端信息](https://assets.emqx.com/images/174598da0aa7c3dce869441b0b500efb.png)

### 测试发布消息

1. 在MQTTX客户端中订阅 `lwip/pub` 主题。
2. 在终端输入发布消息命令。

   ```
   mqttClient pub
   ```

   ![在终端输入发布消息命令](https://assets.emqx.com/images/6d553f0552d0d8d49b653c5a39a6ad32.png)

3. 在 MQTTX 客户端中查看，开发板发送的消息。

   ![在 MQTTX 客户端中查看](https://assets.emqx.com/images/46b1a6a14d6e73d773d7b9071ca311a1.png)

### 完整代码

请见 [mqtt client over lwip](https://github.com/OdyWayne/mqtt_client-over-lwIP)。

## 结语

本文通过 lwIP 的 MQTT 库建立了一个简单的 MQTT 客户端，并完成了该客户端与 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)的连接和 SUB、PUB 测试。MQTT 能够以极少的代码和有限的带宽为远程设备提供可靠的消息传递、海量的连接支持。同样的，lwIP 能够在占用资源极少的前提下，提供完整可靠的 TCP/IP 服务。两者相结合，即使是在资源及其受限的环境中也可以为物联网通信设备提供实时可靠的消息服务。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
