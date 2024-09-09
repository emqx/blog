近日，**Neuron 2.2.2 正式发布。** 这一最新版本对 MQTT 插件、SDK 开发包及其他商业驱动插件进行了优化和更新，为工业领域用户提供更加高效便捷的数据采集。

下载地址：[https://www.emqx.com/zh/downloads-and-install/neuron](https://www.emqx.com/zh/downloads-and-install/neuron) 


## MQTT 插件功能大幅提升

### 避免数据丢失

新增断线缓存数据功能。当 MQTT 连接因临时网络问题或信号不佳而离线，导致正常的数据上报中断，中断期间产生的报文可以缓存在内存中。当网络恢复时，缓存数据可以重新上传到 IoT 平台。这可以减少价值数据因为网络异常而丢失的风险。此功能通过将数据存储在内存中来实现，因此硬件网关或服务器需要有足够的内存空间，可保障的离线时间也取决于硬件网关或服务器的内存大小。断线缓存数据功能会自动生效，用户不需要做任何设定。

### 降低传输数据量

新增了数据订阅后按变化或超过变化范围上传的方式，用户可自行选择按照设定周期上报或是按数据变化上报。如果选定按数据变化上报，Neuron 就会在两次采集中做比较，如果数值变化或数值变化大于设定的阈值就会触发上报过程，如果无数值变化或数值变化小于设定阈值则视为不变，不触发上报过程。这种方案可大大降低数据传输量及网络阻塞风险，减少 IoT 平台服务器处理大量相同数据的时间。

### 数据上报更完善

新增心跳报文上传功能。周期上报所有驱动节点信息，每 1 秒发送一次，内容携带了 Neuron 当前所有驱动节点的运行状态、设备连接状态、报警状态以及运行模式等有用信息，如果 IoT 平台在特定时间（例如 5 秒）内无法接收到这个心跳报文，这代表 Neuron 可能出现故障，需要人工排查。如果有备用 Neuron 在运行，IoT 平台可指示备用 Neuron 取代有故障的那个。此外，报文信息对 IoT 平台监控设备极为重要，例如，平台上数字孪生和设备注册等相关应用都需要心跳报文内容去实现。用户可自定义心跳报文的主题 Topic。

## OPC DA 驱动

新增独立的 OPC DA 和 OPC UA 协议转换程序 opcshift。opcshift 同时作为 OPC DA 客户端和 OPC UA 服务端，通过读取 DA 服务器的数据并转化为 UA 的协议格式，然后再交由 Neuron 的 OPC UA 驱动进行处理。

opcshift 依赖于微软 DCOM 技术，因此只能部署在 Windows 操作系统之上（32 位或 64 位均可）。Neuron 可以通过标准的 OPC UA 连接方式与 opcshift 跨主机连接。

opcshift 会将所有受支持的 DA 点位映射到 UA 的「命名空间 1」之下，各个点位的 ID 与 DA 服务器保持一致，可简化 Neuron 下的采集配置。由于是 OPC UA 的标准接口，opcshift 也支持其他 OPC UA 客户端（如 UaExpert）的访问。

## SDK 开发包

Neuron 2.2 已有 SDK 包，用户可以直接基于 SDK 包开发新的驱动插件并应用到 Neuron 中，避免了依赖库配置的操作，可以更方便快速地开发新驱动。

根据不同的系统架构下载对应的 SDK tar.gz 包到相应的开发环境中并解压，执行以下指令进行快速安装。

```
# take version 2.2.0 as an example
$ cd neuron-sdk-2.2.0
# install sdk
$ sudo ./sdk-install.sh
```

SDK 包下载链接：[https://github.com/emqx/neuron/releases](https://github.com/emqx/neuron/releases) 

安装完成后就可以进行驱动开发，在开发环境中创建一个新的目录文件用于存放开发驱动所需要的文件，名称可自定义。例如，创建名为 drivers 的目录文件用于存放开发驱动所需要的文件，在 drivers 目录下还需创建以下文件：

- CMakeLists.txt 文件，项目使用 Cmake 进行构建时需要；
- plugins 目录文件，用于存放所有驱动开发的文件，每个驱动都应有一个对应的目录文件用于存放该驱动的源文件、CMakeLists.txt 文件和 JSON 文件等。
- build 目录文件，用于存放编译生成的文件；

目录层级如下图所示：

![目录层级](https://assets.emqx.com/images/cae4c0117dec9ffc278e8eb12d7a7979.png)

当驱动代码完成后，在 build 目录下执行以下指令，进行编译验证。

```
$ cmake .. 
$ make 
```

编译无问题后，可在 Neuron 中验证新开发的驱动。将 build/plugins 中生成的驱动 .so 文件拷贝到 /usr/local/bin/neuron/plugins 目录下，再将驱动配置 .json 文件 拷贝到 /usr/local/bin/neuron/plugins/schema 目录下，最后修改 plugins.json 文件，将新添加的驱动 .so 文件名称添加进去。

执行以下指令运行 Neuron，并在网页打开 Neuron 查看新添加的插件的使用。

```
$ sudo ./neuron --log
```

SDK 包使用教程链接：[https://docs.emqx.com/zh/neuron/latest/dev-guide/sdk-tutorial/sdk-tutorial.html)基于 SDK 的驱动开发](https://docs.emqx.com/zh/neuron/latest/dev-guide/sdk-tutorial/sdk-tutorial.html) 

## 新增商业驱动插件

### 西门子-300/400驱动

S7-300/400 CPU 原生只支持串口连接，需要外接以太网模块，虽然 PLC 可以使用 S7 协议进行通信，但是无法使用 S7 协议的异步特性。所以我们为 S7300/400 专门开发了适配的 S7 协议，Neuron 现已支持与S7300/400 PLC 同步通信。

### Beckhoff ADS 驱动

Beckhoff ADS 协议用于与 TwinCAT 设备进行通信。ADS 协议是 TwinCAT 系统中的一个传输层，为不同软件模块之间的数据交换而开发。

### 非 A11 驱动

新增油田设备专属协议，该协议是按照客户规格而开发的，可用于注水井、抽油机井、储罐、管线流量、管线含水等设备。

### 三菱 PLC 插件

支持批量采集多个数据标签的数据，从而提高读取三菱 PLC 数据的速度。

### Modbus 插件新增功能

Modbus 插件新增支持 int64/uint64/double 数据类型和支持写入单线圈数据。

## 未来规划

- 新增信息统计和告警功能
- 支持在页面上下载日志功能
- 支持多用户管理功能
- 开发新的驱动


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
