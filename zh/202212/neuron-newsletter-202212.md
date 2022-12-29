十二月，我们发布了 Neuron 2.3.0 版本。该版本主要新增了监控模块，Neuron 内部的关键数据可通过 HTTP API 对外暴露；南向增加了西门子 FetchWrite 驱动，主要用于西门子 S7-300/400 系列 PLC；北向增加 WebSocket 应用，支持读写数据上报。此外，IEC60870-5-104 驱动功能进行了扩展，新增对时请求以及点位写控制支持。

## 新增监控模块

2.3 版本新增的监控模块通过 HTTP API 将 Neuron 内部的关键数据对外暴露，方便用户对 Neuron 以及设备进行监控管理。

## 协议驱动更新

### 新增西门子 FetchWrite 驱动

西门子的以太网通信模块提供了一种基于 TCP 的 FETCH WRITE 通信方式，该方式无需在 PLC 侧编程就可以得到 PLC 内的所有数据。

该驱动基于 FetchWrite 标准协议实现，用于带有网络扩展模块 CP443 的西门子 PLC 访问。可支持 DB、M、I、Q、PEPA、Z、T 等区域的多种数据类型读写。

### IEC60870-5-104 驱动

增加对时请求，此驱动将会周期性地向设备发送对时请求，同步设备时间。

点位支持写操作，现有支持的数据类型 BIT、INT16/UINT16、FLOAT 都支持写入操作。

### 新增 EtherNet/IP（CIP）驱动

此驱动属于通用驱动，对于支持此驱动的 PLC 都可以进行数据采集与设备控制。

## WebSocket 应用

支持通过 WebSocket 协议上报所订阅点位数据，上报的数据格式与现有北向 MQTT 插件一致。

## 读写文件驱动

新增读写文件的驱动，目前已实现读取文件内容的功能。将点位地址设置为文件的绝对路径，点位值将以 string 类型输出读取到的文件内容。后续会支持写文件功能。

## 其他更新与问题修复

- UI 优化以及部分问题修复。
- 官网文档优化完善。
- 修复了某些情况下 OPC UA 异常退出的问题。





<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
