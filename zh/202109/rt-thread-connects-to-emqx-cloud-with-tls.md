本文将使用 [RT-Thread](https://www.rt-thread.org/) 配合 [ART-Pi](https://github.com/RT-Thread-Studio/sdk-bsp-stm32h750-realthread-artpi) 搭建 MQTT 客户端，快速接入 [EMQX Cloud](https://www.emqx.com/zh/cloud) 。

## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为**全球首个全托管的** [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) **公有云服务**，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

![EMQX Cloud](https://assets.emqx.com/images/7181d58f2c8c2daa6fcfbcb863ad1146.png)

借助云服务商提供的基础计算设施，EMQX Cloud 面向全球数十个国家与地区提供服务，为 5G 与万物互联应用提供低成本、安全可靠的云服务。


## 创建和部署 EMQX Cloud

通过[**快速入门**](https://docs.emqx.cn/cloud/latest/quick_start/introduction.html)创建部署 EMQX Cloud，以下是创建完成的实例：

- 基础版

![EMQX Cloud 基础版](https://assets.emqx.com/images/27af2c8b46466995c444925c6a81db69.png)

- 专业版

![EMQX Cloud 专业版](https://assets.emqx.com/images/a92dfa731423dd0c9be910d63b57b4e8.png)

- **TLS/SSL** 配置可参考 [EMQX Cloud 文档](https://docs.emqx.cn/cloud/latest/deployments/tls_ssl.html)



## 创建项目工程

本文使用 [RT-Thread](https://www.rt-thread.org/) 官方 IDE：[RT-Thread-Studio](https://www.rt-thread.org/page/studio.html) 来创建工程；

> 本次 Demo 使用的是 RT-Thread 官方的开发板 ART-Pi，通过板载 Wifi 模块进行联网，可以直接创建一个 art_pi_wifi 样例工程进行 MQTT 客户端的开发；

![使用 RT-Thread 创建工程](https://assets.emqx.com/images/e1d21e7c5e88bcd3dc9f59d733c8ea94.png)



## 工程配置和引入依赖包

1. 进入配置页面

  ![RT-Thread 配置页面](https://assets.emqx.com/images/193fefffd9fb3401bdb5137b1ec2dedf.png)

  选择“More”

  ![RT-Thread More](https://assets.emqx.com/images/9219de29f9675b27299bd3acf79b0ff6.png)

2. 启用 RTC 驱动

  ![启用 RTC 驱动](https://assets.emqx.com/images/bbd60d4b769d494009314e1a4a6da8c0.png)

3. 引入 MQTT 依赖包

  启动 TLS 需设置 MQTT 线程栈大小 ≥ 6144!

  ![引入 MQTT 依赖包](https://assets.emqx.com/images/90f88490d3391edc04f96792690e2075.png)

4. 配置 mbedtls

   1. 选择 **用户 CA** 证书(单/双向认证)

   ![选择用户 CA 证书](https://assets.emqx.com/images/eace83ce457ddd18b471e5bed8bb13fa.png)

   2. 选择无证书 SSL 连接(单向认证)
     
   ![选择无证书 SSL 连接](https://assets.emqx.com/images/666c6de3821f4977cec59488fb556c9a.png)

5. 保存当前配置，IDE 会将配置更新到工程

  ![保存当前配置](https://assets.emqx.com/images/ea1b23588f56550f67b79f03960e90ba.png)

6. 修改宏 **MEMP_NUM_NETDB** 为 **2**

  位于项目路径"rt-thread\components\net\lwip-2.0.2\src\include\lwip\opt.h:488"

   ```c
   /**
    * MEMP_NUM_NETDB: the number of concurrently running lwip_addrinfo() calls
    * (before freeing the corresponding memory using lwip_freeaddrinfo()).
    */
   #if !defined MEMP_NUM_NETDB || defined __DOXYGEN__
   #define MEMP_NUM_NETDB                  2
   #endif
   ```


## 代码编写

1. 打开 **applications/main.c**,可见 RT-Thread-Studio 已经帮我们生成好了连接 WiFi 和 LED 操作的代码

   ```c
   #include <rtthread.h>
   #include <rtdevice.h>
   #include "drv_common.h"
   
   #define LED_PIN GET_PIN(I, 8)
   
   extern void wlan_autoconnect_init(void);
   
   int main(void)
   {
       rt_uint32_t count = 1;
       rt_pin_mode(LED_PIN, PIN_MODE_OUTPUT);
   
       /* init Wi-Fi auto connect feature */
       wlan_autoconnect_init();
       /* enable auto reconnect on WLAN device */
       rt_wlan_config_autoreconnect(RT_TRUE);
   
       while(count++)
       {
           rt_thread_mdelay(500);
           rt_pin_write(LED_PIN, PIN_HIGH);
           rt_thread_mdelay(500);
           rt_pin_write(LED_PIN, PIN_LOW);
       }
       return RT_EOK;
   }
   
   #include "stm32h7xx.h"
   static int vtor_config(void)
   {
       /* Vector Table Relocation in Internal QSPI_FLASH */
       SCB->VTOR = QSPI_BASE;
       return 0;
   }
   INIT_BOARD_EXPORT(vtor_config);
   ```

2. 为了实现第一次启动也能自动连接WiFi，我们可以在 main() 加入连接函数；

   ```c
    rt_wlan_connect(WIFI_SSID, WIFI_PASSWORD);
   ```

3. 分别新建 mqtt-client.c 和 mqtt-client.h；

   ```c
   static void mqtt_create(void)
   {
       /* init condata param by using MQTTPacket_connectData_initializer */
       MQTTPacket_connectData condata = MQTTPacket_connectData_initializer;
   
       static char client_id[50] = { 0 };
   
       rt_memset(&client, 0, sizeof(MQTTClient));
   
       /* config MQTT context param */
       {
           client.uri = MQTT_BROKER_URI;
   
           /* config connect param */
           memcpy(&client.condata, &condata, sizeof(condata));
           rt_snprintf(client_id, sizeof(client_id), "%s%d",MQTT_CLIENTID, rt_tick_get());
           client.condata.clientID.cstring = client_id;
           client.condata.keepAliveInterval = 60;
           client.condata.cleansession = 1;
           client.condata.username.cstring = MQTT_USERNAME;
           client.condata.password.cstring = MQTT_PASSWORD;
   
           /* config MQTT will param. */
           client.condata.willFlag = 1;
           client.condata.will.qos = MQTT_QOS;
           client.condata.will.retained = 0;
           client.condata.will.topicName.cstring = MQTT_PUBTOPIC;
           client.condata.will.message.cstring = MQTT_WILLMSG;
   
           /* malloc buffer. */
           client.buf_size = client.readbuf_size = MQTT_PUB_SUB_BUF_SIZE;
           client.buf = rt_malloc(client.buf_size);
           client.readbuf = rt_malloc(client.readbuf_size);
           if (!(client.buf && client.readbuf))
           {
               rt_kprintf("no memory for MQTT client buffer!\n");
               goto _exit;
           }
   
           /* set event callback function */
           client.connect_callback = mqtt_connect_callback;
           client.online_callback = mqtt_online_callback;
           client.offline_callback = mqtt_offline_callback;
   
           /* set subscribe table and event callback */
           client.messageHandlers[0].topicFilter = rt_strdup(MQTT_SUBTOPIC);
           client.messageHandlers[0].callback = mqtt_sub_callback;
           client.messageHandlers[0].qos = MQTT_QOS;
   
           /* set default subscribe event callback */
           client.defaultMessageHandler = mqtt_sub_callback;
       }
   
       /* run mqtt client */
       paho_mqtt_start(&client);
   
       return;
   
   _exit:
       if (client.buf)
       {
           rt_free(client.buf);
           client.buf = RT_NULL;
       }
       if (client.readbuf)
       {
           rt_free(client.readbuf);
           client.readbuf = RT_NULL;
       }
       return;
   }
   ```

   对应 **连接**/**订阅**/**上线**/**离线** 回调函数

   ```c
   static void mqtt_connect_callback(MQTTClient *c)
   {
       LOG_D("mqtt_connect_callback!");
   }
   
   static void mqtt_sub_callback(MQTTClient *c, MessageData *msg_data)
   {
       sub_count++;
       *((char *)msg_data->message->payload + msg_data->message->payloadlen) = '\0';
       rt_kprintf("mqtt sub callback[%u]: \n topic: %.*s \n message %.*s",
                  sub_count,
                  msg_data->topicName->lenstring.len,
                  msg_data->topicName->lenstring.data,
                  msg_data->message->payloadlen,
                  (char *)msg_data->message->payload);
   }
   
   static void mqtt_online_callback(MQTTClient *c)
   {
       LOG_D("mqtt_online_callback!");
   }
   
   static void mqtt_offline_callback(MQTTClient *c)
   {
       LOG_D("mqtt_offline_callback!");
   }
   ```

   创建 pub 线程回调函数和 mqtt 客户端启动函数

   ```c
   static void thread_pub(void *parameter)
   {
       pub_data = rt_malloc(TEST_DATA_SIZE * sizeof(char));
       if (!pub_data)
       {
           rt_kprintf("no memory for pub_data\n");
           return;
       }
   
       start_tm = time((time_t *) RT_NULL);
       rt_kprintf("test start at '%d'\r\n", start_tm);
   
       while (1)
       {
           rt_snprintf(pub_data, TEST_DATA_SIZE, "Pub EMQX message-%d", pub_count);
   
           if (!paho_mqtt_publish(&client, QOS1, MQTT_PUBTOPIC, pub_data))
           {
               ++pub_count;
           }
   
           rt_thread_delay(PUB_CYCLE_TM);
       }
   }
   
   void mqtt_client_start(void)
   {
       if (is_started)
       {
           return;
       }
   
       mqtt_create();
   
       while (!client.isconnected)
       {
           rt_kprintf("Waiting for mqtt connection...\n");
           rt_thread_delay(1000);
       }
   
       pub_thread_tid = rt_thread_create("pub_thread", thread_pub, RT_NULL, 1024, 8, 100);
       if (pub_thread_tid != RT_NULL)
       {
           rt_thread_startup(pub_thread_tid);
       }
   
       is_started = 1;
   
       return;
   }
   ```

   设置 MQTT 连接参数和用户名

   ```c
   #define EMQX_Cloud_Professional_Version 1
   #define EMQX_Cloud_TLS_SSL 1
   
   #if !EMQX_Cloud_Professional_Version
   
   #if EMQX_Cloud_TLS_SSL
   #define MQTT_BROKER_URI         "ssl://ge06f1e1.cn-shenzhen.emqx.cloud:15455"
   #else
   #define MQTT_BROKER_URI         "tcp://ge06f1e1.cn-shenzhen.emqx.cloud:15915"
   #endif
   #else
   
   #if EMQX_Cloud_TLS_SSL
   #define MQTT_BROKER_URI         "ssl://oba9d641.emqx.cloud:8883"
   #else
   #define MQTT_BROKER_URI         "tcp://oba9d641.emqx.cloud:1883"
   #endif
   
   #endif
   
   #define MQTT_CLIENTID_PREFIX    "rtthread-mqtt"
   #define MQTT_USERNAME           "EMQX_RTT"
   #define MQTT_PASSWORD           "emqx_rtt_0813"
   #define MQTT_SUBTOPIC           "/emqx/mqtt/sub"
   #define MQTT_PUBTOPIC           "/emqx/mqtt/pub"
   #define MQTT_WILLMSG            "Goodbye!"
   #define MQTT_QOS                1
   ```

   main() 函数启动 MQTT client

   ```c
   mqtt_client_start()
   ```

   也可在终端手动启动/停止

   ```shell
   mqtt_ctrl start
   mqtt_ctrl stop
   ```

   若选择用户 CA 证书验证，则将 CA 证书（双向认证还需 client.crt 和 client.key）放置到 **packages/mbedtls-latest/certs** 文件夹中

   ![CA 证书验证](https://assets.emqx.com/images/bdce20c5212596c2f0d05eb066335a97.png)

   重新更新工程，会自动将证书内容复制到源文件中

   ![重新更新工程](https://assets.emqx.com/images/993b453a86e807dcd48e4d1172475ae4.png)

   构建项目并下载到目标板上

   ![构建项目并下载到目标板上](https://assets.emqx.com/images/cd8a49a10faa20297a40ebf73a9c4e4a.png)

   打开终端 Terminal 可以看到运行日志

   ![打开终端 Terminal 可以看到运行日志](https://assets.emqx.com/images/35bf9d3e9d2b8e5d5972f36ab89cd815.png)

   

## 使用 [MQTT X](https://mqttx.app/zh) 测试数据收发

客户端连接配置

单向无证书认证

![单向无证书认证](https://assets.emqx.com/images/644bbb8747934edccf843bbda133b066.png)

单向自签名证书认证

![单向自签名证书认证](https://assets.emqx.com/images/122e1099bd16aa2694a4674a598fd5b1.png)

双向认证

![双向认证](https://assets.emqx.com/images/479536ee6c327803828bff176ce9e826.png)

订阅和发布

![订阅和发布](https://assets.emqx.com/images/ec15f75488d052b3d2fac4bcf144939f.png)


查看 RT-Thread-Stdio 终端

![查看 RT-Thread-Stdio 终端](https://assets.emqx.com/images/32a1defd9f525517ec1b056ed5a09f0c.png)

**数据收发正常！**



## 完整代码

请见 [MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples)。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
