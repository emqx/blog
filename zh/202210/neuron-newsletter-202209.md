九月，我们发布了 Neuron 2.2。该版本增加了一系列新驱动以及新特性：新增 Beckhoff ADS、OPC DA、NONA11 驱动，统一了 HTTP 服务对外暴露的端口。 此外，本月我们专注于数据统计以及事件告警系统的搭建，计划在 Neuron 2.3 中将系统内部的关键数据统以及关键事件通过 Prometheus 规范反馈出来，完善在 Neuron 使用过程中对其及其所连接设备的监控管理。

## 数据升级

最新版本中增加了从 Neuron 1.x 升级至 2.x 的数据升级脚本，同时 Neuron 2.2 之后在安装包中集成了数据升级，在安装新版本时，可自动将老版本的数据升级到新版本支持，无需在安装新版本后再次配置设备以及设备点位数据。

在 Neuron 2.2 中引入 SQLite 存储 Neuron 配置信息之后，Neuron 采用了 SQL schema 来对数据存储组织格式进行版本管理，便于在版本升级时进行数据升级。

## 关键数据统计以及事件通知

Neuron 将在 2.3 版本中提供基于 HTTP 与 MQTT 的数据统计插件，将 Neuron 中的一些关键数据及关键事件反馈出去。

统计信息主要为南北向 node 数据统计，包括 node 数量、运行中 node 数量、与设备断开连接的 node 数量、南向 node 中配置的点位数量、node 收发数据的字节数、指令数，以及 node 中更为细致的一些状态信息，如与设备之间的延迟等。

事件通知主要在 Neuron 内部，将一些关键变更作为事件，通知外部。如增删改设备的相关配置以及点位信息、Neuron 与设备建立连接以及断开连接等。

其中基于 HTTP Server 的接口，将以符合 Prometheus 规范的数据格式进行统计信息以及事件的汇总，方便接入 Prometheus 监控系统，对 Neuron 及其设备进行监控管理。

## 即将到来的驱动

### QnA 1E 驱动

此驱动与现有驱动 QnA 3E 类似，主要对接三菱 PLC 中一些比较老的型号，支持以串口连接的方式进行通讯。支持的数据类型与 QnA 3E 相同，囊括了常用的数据类型。

### CNC FANUC 驱动

此驱动主要应用于 CNC（数控机床），与 FANUC 的数控机床进行交互，获取机床的一些基本信息，如主轴速度、距离、绝对与相对位置信息等。

## 问题修复

- 修复 float 以及 double 类型的数据精度问题。
- 修复导入大量点位花费时间较长的问题。

## 其他更新

- UI 修改导入导出至 group 列表页面，现在可以一次导入导出多个 group 的点位数据。

- UI 完善错误提示。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
