随着 5G 网络技术的进步，物联网世界也在飞速发展，时至今日，无数的物联网设备在世界的各个角落发光发热。

但有别于传统互联网，端到端的沟通，一直是物联网业务的难点。使用的物联网通讯协议不同，使得这些设备之间的沟通存在巨大的鸿沟。就好比人与人之间语言不同，无法正常的交流。

![image20210410180639347.png](https://assets.emqx.com/images/6e9b97f0ab7f852eda6f6c9e91d44c7c.png)
EMQX Broker 作为物联网消息中间件，则肩负着促成这些设备提供沟通交流的使命。为此，我们开发了很多物联网协议插件，无论你偏爱煲电话粥式的热情（基于 TCP 长链接，比如 MQTT），还是一字一句书信的温情（基于 UDP 无连接，比如 CoAP），或是你有一套属于自己的「暗语」（私有协议），在 EMQX 的世界，我们都能帮你找到能读懂你的「soulmate」。

> 关于 MQTT 协议：https://www.jianshu.com/p/ecde412d2eeb
>
> 关于 CoAP 协议：https://www.jianshu.com/p/7fec0916a0d3

**本文将向你展示，MQTT 客户端和 CoAP 客户端，在 EMQX World 的一次「约会」。**



#### Step 1：启动 EMQX Broker，打开 CoAP 插件，并确保插件的运行状态。

关于如何安装和启动 EMQX Broker，你可以在[这里](https://docs.emqx.cn/broker/v4.3/getting-started/install.html)找到帮助。

打开 Dashboard，点击左侧插件，右侧搜索 CoAP ，点击启动，运行 `CoAP 插件`（ 默认端口 5683 ）。
![image20210412152259272.png](https://assets.emqx.com/images/66a3ec26f6ef7baedb9fb7e22b0cdf5d.png)
​	

MQTT 的 `PUB/SUB` 模型中，为了实现端到端通讯，需要设备之间通过 `topic` 作为桥梁，我们使用 `coap_to_mqtt` 和  `mqtt_to_coap`两个 `topic` ，分别作为 CoAP 到 MQTT 的消息 `topic` ，和 MQTT 到 CoAP 的消息 `topic` 。

MQTT 与 CoAP 都支持发布/订阅机制，MQTT 依靠的是报文中的 Topic 字段，而 CoAP 协议类基于 REST 设计，在 EMQX Broker 中:

​		`PUT`  和 `GET`： 作为  `Publish` 和 ` Subscribe` 。

​		`URI` ：路径映射 topic ，规则为：主题名 `topic_name`  转化为路径 `/mqtt/topic_name` ，即 `topic` 加上 `/mqtt/` 前缀。

​		`URI Query`： 路径参数携带了终端信息，包括终端、用户名、密码。

```shell
# 示例
put "coap://host:port/mqtt/$topic?c=$client&u=$username&p=$password"
get "coap://host:port/mqtt/$topic?c=$client&u=$username&p=$password"

# -m get | put | post ...
# method 请求方式

# coap://host:port
# CoAP 协议路径格式，host 和 port ，填写 EMQX Broker 部署的IP，和CoAP插件的端口（默认5683）

# /mqtt/$topic 
# 指 mqtt 的 topic ，需要转换，规则：
# topic 名称 topic_name ,在 CoAP 中需要使用 /mqtt/topic_name

# URI Query
# c :终端
# u :用户名
# p :密码
```

至此，准备工作已经完成。



#### Step 2：邀请第一位参会者，MQTT 客户端

将 MQTT X（EMQ 旗下开源 MQTT 桌面客户端）连接至你的 EMQX Broker，并为它订阅主题 `coap_to_mqtt`。

![image20210410173501967.png](https://assets.emqx.com/images/161b58e547d1e123491c85dd3e18424a.png)



#### Step 3：邀请第二位参会者，CoAP 客户端。

本文中使用的 CoAP 客户端是 [libcoap](https://github.com/obgm/libcoap) 。

```sh
# 先安装 libcoap
# 使用 git 下载，或者使用下载链接 https://github.com/obgm/libcoap/archive/refs/tags/v4.2.1.zip
git clone https://github.com/obgm/libcoap.git
# 如果你使用下载链接下载，unzip 解压
# unzip libcoap-4.2.1.zip

# 进入 libcoap 文件目录
cd libcoap
# 切换至稳定版本 作者使用的是 v4.2.1
# 如果你使用本文中的下载链接下载，不需要切换版本。
git checkout v4.2.1
# 安装配置
./autogen
# ./autogen 的过程中可能会遇到部分依赖缺失的情况（比如 autoconf 和 automake ），按照提示安装对应依赖即可。
./configure --enable-documentation=no --enable-tests=no
# 打包
make
```



#### Step 4：开始通信

安装完成后，CoAP 终端 PUT 消息到  `coap_to_mqtt` 主题。

```shell
# CoAP 终端发送消息 hello EMQX world,  I am coap，topic 为 coap_to_mqtt
./examples/coap-client -m put -e "hello EMQX world, I am coap"  "coap://127.0.0.1/mqtt/coap_to_mqtt?c=coap20211&u=tom&p=secret"
# 命令中的 127.0.0.1 替换为你的 EMQX Broker 部署地址
```



我们可以看到 MQTT X 收到了来自 CoAP 的问候。

![image20210412165307589.png](https://assets.emqx.com/images/d9f62c3d50866c9f6c01ebf4f369ad16.png)



现在为 CoAP 终端订阅 `mqtt_to_coap` 主题。

```shell
# CoAP 终端订阅 mqtt_to_coap 主题，-s 20表示订阅维持20秒
./examples/coap-client -m get -s 20 "coap://127.0.0.1/mqtt/mqtt_to_coap?c=client1&u=tom&p=secret"
```



MQTT X 发送 `hello coap, I am mqtt welcome to EMQX Wrold!`  至 `mqtt_to_coap` 主题。

![image20210412165434332.png](https://assets.emqx.com/images/966dc4195705ae31e41842261fc7b164.png)



CoAP 也收到了来自 MQTT 的回应。

```shell
./examples/coap-client -m get -s 20 "coap://127.0.0.1/mqtt/mqtt_to_coap?c=client1&u=tom&p=secret"
hello coap , I am mqtt ,welcome to EMQ World
```



**至此，我们完成了以 EMQX Broker 作为媒介的一次端到端通信流程，让 MQTT 和 CoAP 在 EMQX 世界里成功「约会」。**



在 EMQX World，不仅有 MQTT、CoAP、LWM2M、JT808 以及未来将支持的更多不同物联网协议插件，同时我们也为你提供了[插件的开发模板](https://github.com/emqx/emqx-plugin-template)。我们期待在这里，所有的物联网设备都能相会，碰撞出耀眼的火花，照亮物联网的世界。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
