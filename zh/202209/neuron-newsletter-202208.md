八月，我们发布了 Neuron 2.1.3 & 2.1.4，主要修复了 2.1.0 版本中存在的问题。此外还完善了 SDK 包以及基于此 SDK 包开发南向驱动的一系列文档；点位支持小数的精度设置以及乘系数，点位配置支持订阅属性，点位值发生变化时才会上报；与西门子平台进行了集成验证测试，支持通过西门子平台安装 Neuron 至其接入的网关设备。

## OPC DA 驱动

新增独立的 OPC DA 和 OPC UA 协议转换程序——opcshift。opcshift 同时作为 OPC DA 客户端和 OPC UA 服务端，通过读取 DA 服务器的数据并转化为 UA 的协议格式，然后再交由 Neuron 的 OPC UA 驱动进行处理。

opcshift 依赖于微软 DCOM 技术，因此只能部署在 Windows 操作系统之上（32 位或 64 位均可）。Neuron 可以通过标准的 OPC UA 连接方式与 opcshift 跨主机连接。

opcshift 会将所有受支持的 DA 点位映射到 UA 的「命名空间 1」之下，各个点位的 ID 与 DA 服务器保持一致，可简化 Neuron 下的采集配置。由于是 OPC UA 的标准接口，opcshift 也支持其他 OPC UA 客户端（如 UaExpert）的访问。

opcshift 目前支持多种基本数据类型的采集，包括：VT_I1(Sbyte)、VT_I2(Int16)、INT/VT_I4(Int32)、VT_I8(Int64)、VT_R4(Float)、VT_R8(Double)、VT_UI1(Byte)、VT_UI2(Uint16)、VT_UINT/VT_UI4(Uint32)、VT_UI8(Uint64)、VT_DATE(Datetime)、VT_BSTR(String)、VT_BOOL(Boolean)。

## Beckhoff ADS 驱动

Beckhoff ADS 协议用于与 TwinCAT 设备进行通信。ADS 协议是 TwinCAT 系统中的一个传输层，为不同软件模块之间的数据交换而开发。其在 TCP/IP 或 UDP/IP 协议之上运行，允许 Beckhoff 系统内的用户使用任何连接路径与所有连接的设备进行通信并更改参数。

该协议支持从 TwinCAT 中的任何位置与其他工业设备进行通信。 如果需要与另一台 PC 或设备通信，在 TCP/IP 之上使用 ADS 协议，就可以在联网系统中获取 TwinCAT 所有数据。

Neuron 新增了 ADS 插件，支持通过 TCP 与支持 ADS/AMS 协议的设备通信。支持的点位类型及其对应的数据类型如下表：

| **点位类型** | 对应 TwinCAT 数据类型 |
| :----------- | :-------------------- |
| BOOL         | BOOL                  |
| INT8         | SINT                  |
| UINT8        | USINT                 |
| INT16        | INT                   |
| UINT16       | UINT                  |
| INT32        | DINT                  |
| UINT32       | UDINT                 |
| INT64        | LINT                  |
| UINT64       | ULINT                 |
| FLOAT        | REAL                  |
| DOUBLE       | LREAL                 |
| STRING       | STRING                |

## 新增离线缓存

当 MQTT 连接因临时网络问题或信号不佳而中断时，离线缓存可以帮助将数据存储在临时存储中。当网络恢复时，缓存数据可以再次传输到云平台。这可以减少有价值数据的丢失。Neuron 通过将数据存储在内存缓存中来实现此功能。因此硬件网关需要有足够的内存，可保障的离线时间也取决于硬件网关内存大小。

## 其他新增功能概览

- 新增 SDK 开发包，以及相关使用文档。
- 新增数据点位订阅功能，点位值发生变化或者是配置发生变化时才会发送点位值，减少了上报数据量。
- 点位支持乘系数以及精度处理，可以对采集到的数据进行初步处理。
- RESTful 插件新增 API 代理功能，可对多个端口的 HTTP SERVER 进行端口整合，简化端口使用。
- 新建简化 Neuron 版本包，分离数据处理模块。
- RESTful 插件支持关闭鉴权验证。
- MQTT 插件简化配置，删除了 client-id 配置选项。
- UI 优化，更完善的错误提示以及配置时更多的错误检查。

## 文档更新

- 继续完善了 Neuron 2.1.0 的官网文档，增加了 HTTP API 配置设备的文档。

## 问题修复

- 修复 MQTT 插件在网络异常时崩溃的问题。
- 修复 FINS 插件在导入某些点位地址时发生崩溃的问题。
- 修复某些情况下，插件停止后未断开与设备之间连接的问题。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
