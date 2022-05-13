作为 [EMQ](https://www.emqx.com/zh) 工业互联网云边协同解决方案的重要组成部分，[物联网边缘工业协议网关软件 Neuron](https://www.emqx.com/zh/products/neuron) 自发布以来，为工业领域的诸多用户在边缘侧提供了工业协议转换接入、设备远程监控管理等实现工业设备数据采集的必备功能。

Neuron 支持包括 Modbus、OPCUA、三菱、西门子、罗克⻙尔⾃动化、OMRON 等在内的数十种工业设备协议的接入与转换，无需容器框架，超低资源占用，支持 X86、ARM 架构，是构建工业物联网平台的理想选择。

**Neuron v1.3.0 已于近日正式发布**，下载地址：[https://www.emqx.com/zh/try?product=neuron](https://www.emqx.com/zh/try?product=neuron)



## 协议支持列表再扩充，覆盖电力行业

在最新发布的 Neuron v1.3.0 中，新增了 DL/T645-07、IEC 60870-5 104、IEC 61850 MMS 等电力行业的协议支持。同时也新增了一个 PLC 协议——**FINS on TCP**。这意味着 Neuron 将可以帮助更多行业用户实现边缘设备的数据管理。

> 由于 IEC 61850 协议需要模型导入以及模型解析相关的一些功能，所以该协议暂时只支持定制。

以 DL/T645-07 协议为例，设备接线方式如下图所示，电表通电并通过 USB 转 Modbus 转换器以串口连接的方式连接到电脑上。Neuron 通过配置可以读取电表的电流、电压和功率等参数的值。


![Neuron 读取电表数据](https://assets.emqx.com/images/af8ae0c4545ca24118beb308cac1d684.png)



## 已有协议支持进一步增强

对于已经支持的协议如 OPC UA 和 [Modbus](https://www.emqx.com/zh/blog/building-modbus-based-iiot-app-with-neuron)，新版本中则进行了增强与完善。

### OPC UA 订阅功能

在属性设置中，有可选择订阅功能的按键，进行订阅。该功能采用被动方式接收数据，可以减少 Neuron 对设备读操作的次数，从而减少网络流量。在被订阅的点位在 OPC UA 服务端开启可订阅权限的情况下，该点位的数据变化会自动更新到 Neuron 上。

![Neuron OPC UA 订阅功能](https://assets.emqx.com/images/09299723ad27d6f116ea2ca44d578141.png)

### Modbus 支持 TCP Server 模式

Modbus 支持连接 DTU 设备，在 DTU 设备的云端将远程服务器地址配置为 Neuron 运行所在环境的 IP 地址，配置相应的端口号，Neuron 即可访问 DTU 设备读取数据。在 Neuron 的驱动设置中，设置 Host name 时，要填写 Neuron 运行所在环境的 IP 地址。

![Modbus 支持 TCP Server 模式](https://assets.emqx.com/images/dc404ca3f8f694f4ca6ac04d8a79c993.png)

### 新增 Modbus 每个点位可单独定义字节顺序的功能

驱动地址格式：STN!ADDR.BIT#ENDIAN

![Neuron Modbus 配置](https://assets.emqx.com/images/7e9372bbb877d281d43d7231baeaea1f.png)



## 安全性提升，更可靠的数据通信

最新版本中新增了 Web Server API HTTPS 认证功能。增加具有安全性的 SSL 加密传输协议，在 Server API 上，可以通过远程 HTTPS 连接，为浏览器和服务器之间的通信加密，确保数据传输的安全性。

![Neuron HTTPS](https://assets.emqx.com/images/af421bac9e28619be27e7ad5d234fd05.png)



## 问题修复，使用更顺畅

### 修正 OPC UA 协议中服务端强制 UserTokenPolicy 时无法使用 username 登录的问题

因部分 OPC UA 服务器出于安全考虑，禁止设备登录时使用明文传递 username 和  password，但是会提供一系列「认证方式的描述」给设备，设备再按照描述信息处理用户信息并再次提交给 OPC UA 服务器，OPC UA  验证用户信息后才会采取相应操作。

![Neuron OPC UA 设置](https://assets.emqx.com/images/ec8fa21f23293ad4010f785e10688f20.png)

### 修正 Docker 启动问题

修正在 Docker 里同时启动 10 个实例时，实例 1 会出现「has fatal error」的问题。



## 开源初心，值得期待的 Neuron v2.0

目前，Neuron 团队仍在不断提升产品的功能与性能，使其在未来可以与 EMQ 其他产品更好地融合与协作。未来 Neuron 的研发将更加专注核心功能，在其「物联网边缘工业协议网关软件」的产品定位上深耕，为工业领域的数据「连接与移动」提供支持。

同时，作为一家开源物联网数据基础设施软件供应商，EMQ 也将在 Neuron v2.0 中开启其开源进程。Neuron v2.0 将采用全新的数据通讯架构，充分利用多核 CPU 的性能，增强系统响应能力和承载能力，以更少内存获得更快响应和更高数据带宽。另外还将支持同时连接多个设备、动态更改配置（无需重启）以及驱动热更新。

开源的 Neuron v2.0 将为产业内更多用户带来边缘工业数据的一站式接入支持，更加开放的产品形态也将加速产业融合，与上下游合作伙伴共同推进工业互联网的发展。

敬请期待。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
