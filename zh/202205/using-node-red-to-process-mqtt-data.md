> Node-RED 是一个可视化的编程工具，可以创新和有趣的方式将硬件设备、API 和在线服务等连接起来。它提供了一个基于浏览器的编辑器，通过调色板中广泛的节点将流程轻松连接起来，而这些节点只需通过一次点击即可部署到其运行时。
>
> 除 HTTP、WebScoket 等一些基础的网络服务应用节点外，Node-RED 还提供对于 [MQTT 协议](https://www.emqx.com/zh/mqtt)的连接支持。目前同时提供了一个 MQTT 的订阅节点和 MQTT 的发布节点，订阅节点用于数据的输入，而发布节点可以用于数据的输出。

本文将介绍使用 Node-RED 连接到 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并对 MQTT 数据进行过滤和处理后再将其发送至 MQTT 服务器的完整操作流程。读者可以快速了解如何使用 Node-RED 对 MQTT 数据进行简单的流处理。

## Node-RED 安装

Node-RED 无论是在你本地的电脑上，还是树莓派等设备，亦或是云端服务器，都可以快速安装和使用，下面将使用两种比较常见的安装方式：

使用 `npm` 进行全局安装：

```
1npm install -g --unsafe-perm node-red
```

使用 `Docker` 进行安装：

```
1docker run -it -p 1880:1880 --name mynodered nodered/node-red
```

## 运行

如果使用的是 npm 进行的全局安装，那么在提示安装成功后，只需要在全局运行 `node-red` 命令就可以立即启动 Node-RED。

无论是使用 `Docker` 还是 `npm` 在启动成功后，我们只需要打开浏览器，输入当前地址加 1880 端口号，即可打开 Node-RED 的浏览器编辑器页面，例如在本地运行的话，打开浏览器，输入 [http://127.0.0.1:1880](http://127.0.0.1:1880/)，当看到如下图所示页面后，说明 Node-RED 已经成功启动：

![Node-RED 启动成功](https://assets.emqx.com/images/2cda7190fa375cc0e85e65781b70a766.png)

## 在 Node-RED 中使用 MQTT

本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 物联网云平台 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- WebSocket Port: **8083**

在下面的功能演示中，我们将提供一个使用 Node-RED 来处理接收到的包含温湿度信息的 JSON 数据，然后对温度值进行规则判断，当温度发生改变的时候，就将当前发生改变的温度值通过 MQTT 再次发送出去的简单使用案例。

### 连接 MQTT 服务器

我们首先在左侧菜单栏中，拖拽一个 MQTT in 的节点到页面中，双击节点后，右侧出现一个编辑 MQTT 节点的配置页面，我们根据内容提示，新建一个连接信息后，再填入 MQTT 的其它连接信息后，点击 Done 按钮后，即可保存该节点信息。

![Node-RED MQTT in node](https://assets.emqx.com/images/597fb3a3e45ce8544d89d7e8cbdd0b86.png)

### 对 MQTT 数据进行处理

接入数据：我们拖拽一个 JSON 节点到页面中，可以在 JSON 节点的配置页面中，配置一个 Action，我们设置为 `Always convert to JavasScript Object`，因为我们无法确定发送过来的数据是一个 JSON 格式的数据还是一个 JSON 字符串，因此第一步都将接收到的消息进行一个 JSON 转换。配置完成后，我们将该节点与 MQTT in 节点进行连接。

![Node-RED JSON node](https://assets.emqx.com/images/25874952e5de18fe8126ca5afa3d392b.png)

**过滤数据**

我们配置完成格式化发送过来的消息数据后，我们就可以拖拽一个 filter 节点到页面中，同样双击节点后，在配置页面中配置规则，我们先选择一个 Mode，我们设置为 `blcok unless value changes`，过滤规则为需要当前接收到数据的值发生改变，因为目前数据为 JSON 格式，我们判断的是 JSON 数据内的某一个值，因此我们需要在 Property 这里设置值为 `msg.payload.temperature` 配置完成后我们点击 Done 按钮来保存数据过滤节点的配置，最后将该节点连接到上一步配置完成后的 JSON 节点。

![Node-RED filter node](https://assets.emqx.com/images/9b77d353d63a4f2b32045f9d7399cd78.png)

**使用模版**

当过滤完数据后，同样拖拽一个 template 节点到页面中，双击节点后来配置模版内容，使过滤完成后的数据，能通过模版将数据进行输出。当然也可以不需要这个步骤，直接将过滤后的数据进行输出。

![Node-RED template node](https://assets.emqx.com/images/8818d78773b2e7e7b0450c507073ac8c.png)

### 发送经过处理后的 MQTT 数据

完成以上对数据的处理和过滤后，最后我们再来将处理完成后的数据使用 MQTT 将其发送出去，拖拽一个 MQTT out 的节点到页面中，填入和 MQTT in 节点相同的连接信息，配置一个用户接收数据的 Topic，最后保存完成后，再将其和 template 节点进行连接，点击右上角的 Deploy 按钮，即可对当前规则应用进行在线部署。

![Node-RED MQTT out node](https://assets.emqx.com/images/a0aeb565961ad24ed5d0344d16adc01b.png)

### 功能测试

在完成整个流数据处理的功能编排以后，我们使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 来测试和验证该功能的可用性。我们新建一个连接，连接到刚才在 Node-RED 中配置的 MQTT 云服务地址，然后输入 MQTT in 节点内的 Topic 来发送一条消息，使 Node-RED 能够接收到我们发送的 MQTT 数据。

然后我们再在 MQTT X 中订阅一个在 MQTT out 节点内配置的 Topic，用于接收处理过的消息数据。当发送一条包含了温湿度的消息数据后，我们可以接收到一条根据我们设定的消息模版发送过来的消息，再次发送就无法接收到。

![MQTT X 消息发送](https://assets.emqx.com/images/d7f584d50d337c45918af3f3187e522b.png)

因为此时温度值没有发生变化，当我们再次修改温度值后，就会发现我们又接收到了一条包含提醒温度值发生变化的消息。

![MQTT X 消息接收](https://assets.emqx.com/images/04d009b040ca894f026a4beb34014f92.png)

## 总结

至此，我们完成了安装并使用 Node-RED 连接到 MQTT 云服务，以及对 MQTT 消息数据进行过滤和处理，最后再将处理完成后的数据消息发送至 MQTT 服务器的全部流程。

Node-RED 的交互和使用方式，即用 UI 方式描述通用业务逻辑，可以降低非专业开发人员的上手门槛，使用一个可视化工具快速地创建需要的复杂执行任务，可以通过简单 Node 即节点连接构建出复杂的任务，特别是针对一些物联网的应用场景，都很有帮助。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
