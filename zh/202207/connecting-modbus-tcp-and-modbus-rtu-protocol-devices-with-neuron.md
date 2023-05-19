Modbus 是一种通用的工业标准，不同厂商生产的控制设备可以通过 Modbus 连成工业网络，进行集中监控。

Modbus TCP 与 Modbus RTU 是 Modbus 两种常用的传输方式， Modbus RTU 是串口通信，Modbus TCP 是 TCP 通信，两者在协议上非常相似，但是由于 TCP 协议的可靠性，Modbus TCP 协议中不需要校验，并且比 Modbus RTU 协议多一个应用报文头。

作为一款支持数十种工业协议转换的物联网边缘工业协议网关软件，[Neuron](https://neugates.io/zh) 也已经实现了基于 Modbus RTU 协议 TCP 传输的功能。同时，在 Modbus 协议里，Neuron 根据配置的点位进行了策略优化，可实现自动批量采集设备数据的功能。

本文将在 Ubuntu 20.04.3、X86_64 的环境下，介绍如何使用 Neuron 接入 Modbus TCP 及 Modbus RTU。

## Neuron 简介

Neuron 是可运行在各类物联网边缘网关硬件上的工业协议网关软件，旨在解决工业 4.0 背景下设备数据统一接入难的问题。通过将来自繁杂多样工业设备的不同协议类型数据转换为统一标准的物联网 MQTT 消息，实现设备与[工业物联网](https://www.emqx.com/zh/use-cases/industrial-iot)系统之间、设备彼此之间的互联互通，进行远程的直接控制和信息获取，为智能生产制造提供数据支撑。

Neuron 支持同时为多个不同通讯协议设备、数十种工业协议进行一站式接入及 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)转换，仅占用超低资源，即可以原生或容器的方式部署在 X86、ARM、RISC-V 等架构的各类边缘硬件中。同时，用户可以通过基于 Web 的管理控制台实现在线的网关配置管理。

## 配置环境说明

- 请在官网 [https://neugates.io/zh/downloads](https://neugates.io/zh/downloads)  下载 Neuron 软件并执行以下指令安装 Neuron 软件。

   ```
   sudo apt install ./neuron-2.0.1-linux-amd64.deb
   ``` 

   然后使用以下指令检查 Neuron 状态

   ```
   sudo systemctl status neuron
   ```

- 请在 [PeakHMI 官网](https://hmisys.com/) 中下载 Modbus 模拟器并进行安装，之后打开 Modbus TCP slave Ex。

Neuron 使用入门请参照：[Neuron 快速教程](https://neugates.io/docs/zh/latest/quick-start/hardware-specifications.html#环境搭建)。


## 操作流程

在 Neuron 中将使用到 modbus-plus-tcp 和 modbus-rtu 两个插件，下面将介绍如何连接 Modbus TCP。

### 连接 Modbus TCP 示例

#### 第一步，创建节点卡片

![添加 Modbus TCP 设备](https://assets.emqx.com/images/a9162c3ce7515d96212f89de354aaef7.png)

1. 点击 `添加设备` ；
2. 填写设备名称，例如 modbus-plus-tcp-1；
3. 下拉框选择 `modbus-plus-tcp` 插件。

#### 第二步，设备配置

在节点卡片中点击`设备配置` 按键，进入设备配置界面。

1. 填写启动 Modbus 模拟器 所在的 IP 地址；
   1. 启动的 neuron 与 modbus 模拟器要在同一网段下；
   2. Modbus 模拟器所在的 windows 尽量关闭防火墙，否则有可能连不上 Neuron。
2. 填写 Modbus 模拟器的端口号，一般默认是 502；
3. 设置 Neuron 连接设备超时时间；
4. 选择连接方式，Neuron 现在支持作为 Client 和 Server 两种连接模式，默认选择 Client 连接方式；
5. 点击`提交` 完成设备配置，将卡片工作状态打开。

![配置 Modbus TCP 1](https://assets.emqx.com/images/5a5cf60d15e94c56517b13abf2ec0555.png)

![配置 Modbus TCP 2](https://assets.emqx.com/images/8d0386daa624238218e5c66019d48040.png)

#### 第三步，创建 Group 组

点击节点卡片任意空白处进入 Group* 列表界面。

1. 点击`创建` ；
2. 在弹框中填写 Group 名称，例如 group-1；
3. 在弹窗中填写 Neuron 从设备读取数据和上传数据的时间间隔，例如，3000；
4. 点击 `创建` 完成创建 Group；

> *注：Group 可以理解为传感器的一类，例如一台设备下连接多台温度传感器和多台湿度传感器，就可以设置一个「温度」的 Group，将所有的温度传感器统一到一个组中。数据上报以及读取以 Group 为单位，用户可根据业务需求对点位进行分组。

![Neuron 创建 Group](https://assets.emqx.com/images/ee7a99a4d8c8ec76528fc91024bc631d.png)

> 注：
>
> Neuron 上配置不同站点的 Modbus 点位时，建议同一个 Group 下只包含一个站点的点位，或只包含一个站点下同一个数据区域的点位，以获得更高的配置采集效率。

#### 第四步，创建 Tag

在 Group 中点击 `Tag 列表` → `创建` ，手动添加 tags。

1. 填写 Tag 名称，例如 tag1；
2. 填写 Tag 地址，例如 1!40001（详细地址配置规则请参考后面的延伸知识）;
3. 下拉选择属性，例如 Read，Write；
4. 下拉选择数据类型，例如选择 INT16；
5. 点击`创建` ，添加一个 Tag；
6. 也可以点击 `添加` ，一次添加多个 Tags 后 再点击 `创建`；


![Neuron Tag 列表](https://assets.emqx.com/images/4318ad38a0550b1a7b9360ff2c22049c.png)

![Neuron Tag 列表](https://assets.emqx.com/images/689fb55facce8701ce200b6b4ad07625.png)

![Neuron 创建 Tag](https://assets.emqx.com/images/08ca4f8bf8a2f2ffff2612f6feaef6a3.png)

创建完成后，Tag 列表将展示已创建的 Tag 信息，之后返回南向设备管理界面，等待 15s 左右，查看 Modbus 节点卡片的连接状态是否显示`已连接` ，如下图所示。

![Neuron 已创建 Tag 列表](https://assets.emqx.com/images/7f12db0b32a9ee764d66126e417c7468.png)

![Modbus 连接状态](https://assets.emqx.com/images/71d8052132b34417f10ddc50dad11b27.png)

若长时间未连接，请进行以下排查：

- 对照模拟器，检查设备配置的 host 和 port 是否填写错误，可在运行 Neuron 服务器的终端执行 telnet 指令查看是否能访问远程服务器及端口；
- 在运行 Neuron 服务器的终端，检查 502 端口是否被占用；
- 检查模拟器的端口号是否是 502，在 file → settings 中查看 Port Number，如下图所示。

   ![Modbus 模拟器](https://assets.emqx.com/images/8e87c6d6e10540de8f5c409112c7520e.png)
 

#### 第五步，数据监控查看数据

成功连接到 Modbus 模拟器之后，可以打开数据监控界面查看 Neuron 从 Modbus 模拟器上采集到的数据。

![查看 Modbus 上报数据](https://assets.emqx.com/images/452ce2ee3dd129433e4f54302a165dd7.png)

### 连接 Modbus RTU 示例

步骤如 Modbus TCP ，但由于 Modbus RTU 是串口通信，所以`设备配置` 不同于 Modbus TCP。

![连接 Modbus RTU 示例](https://assets.emqx.com/images/275e4a6747a65885093722dbd8ed369f.png)

- Device，串口连接的路径；
- Stop，停止位；
- Parity，校验位；
- Baud，比特率；
- Data，数据位；

Neuron 已经支持基于 Modbus RTU 的 TCP 传输功能，应用配置如下图所示。

![基于 Modbus RTU 的 TCP 传输功能](https://assets.emqx.com/images/6298d95a69ebcd03082480750209fee6.png)

## 知识延伸

Neuron 中 Modbus 点位地址一般的配置格式是 `SLAVE!ADDRESS`，其中：

- SLAVE 代表的是 Slave ID；
- ADDRESS 指的是 PLC 地址：

| 区块                         | **Modbus 区块编号** |
| :--------------------------- | :------------------ |
| 线圈 (coils)                 | 0                   |
| 输入寄存器 (input registers) | 3                   |
| 离散量输 (Input)             | 1                   |
| 保持寄存器 (hold registers)  | 4                   |

在指令中使用的是功能码和寄存器寻址地址，寄存器寻址地址是从 0 开始，不同的功能码对应不同的区块，PLC 地址是区块编号 + 寄存器寻址地址 + 1。例如，用的是 0x03 功能码，寻址地址是 0，对应 neuron 中的 ADDERESS 应为 40001。

## 结语

至此，我们完成了使用 Neuron 接入 Modbus TCP 和 Modbus RTU 协议设备的全部流程。作为一个为工业物联网的「连接」而生的边缘工业协议网关软件，Neuron 还支持 OPC UA、Siemens 等其他多种工业协议的接入，助力建设高效的工业物联网平台。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
