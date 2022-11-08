十月份，我们发布了 Neuron 2.2.6 与 2.2.7 版本，优化修复了在 2.2 版本中发现的一系列问题；新增了监控插件，主要用于以 HTTP、MQTT 的方式对外提供系统内部以及各插件特有的一些监控统计信息；新增三菱 A1E 驱动以适配三菱较老的 PLC 型号；新增 FANUC 驱动支持从发那科机床上采集一些基础数据。

## 监控统计

开源版 Neuron 增加了监控插件，目前以 HTTP Server 的方式，基于 Prometheus 的数据格式，对外提供一些 Neuron 内部数据以及每个插件通用与自定义的统计字段；新增插件接口，实现基于此接口对外暴露一些插件内部数据；现有插件的监控统计信息也在逐步完善中。

监控插件后续还将增加基于 MQTT 对外提供 Neuron 的监控数据。

## 新增驱动

### 三菱 A1E 驱动

此驱动与三菱 QnA3E 驱动类似，实现了 MC 协议的 1E 帧通讯格式，通过以太网连接读写 PLC 软元件。该驱动可以操作三菱 A 系列 PLC、FX3U/FX3G 系列 PLC 和 FX5U 系列 PLC。

数据类型可支持：BIT、INT16、UINT16、INT32、UINT32、FLOAT、DOUBLE、STRING。

### FAUNC 驱动

此驱动主要用于发那科部分型号数控机床，支持通过网络进行连接，支持读取数控机床的 axis feedrate、axis position、spindle speed、distance 等数据。

数据类型可支持 INT64 和 STRING。

## 日志 API

增加了日志相关的 HTTP API，包括修改日志等级、下载日志文件等。修改日志等级的 API 可单独为每一个node 开启 Debug 日志，且每个 node 日志单独输出到 node 对应的日志文件。下载日志 API 将一次性压缩下载所有日志文件，使调试和排查问题更加方便容易。

## 其他更新

- 新增基于 SDK 开发北向应用的文档。
- 完善 S7 驱动文档。
- UI 优化，南向设备管理页面支持搜索过滤，在连接大量设备时方便管理。
- MODBUS RTU 优化，支持一个串口连接多个设备。

## 问题修复

- 修复大量配置请求时，数据库超时的问题。
- 修复 UI 写入 UINT32 数据类型错误的问题。
- 修复 OPC UA 采集数据较慢的问题。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
