>Neuron 为工业物联网的「连接」而生，支持同时为多个不同通讯协议设备、**数十种工业协议**进行一站式接入及 MQTT 协议转换，仅**占用超低资源**，可以原生或容器的方式部署在 X86、ARM 等架构的各类边缘硬件中，助力构建工业物联网平台与应用。
>
>社区站网址：[https://neugates.io/zh](https://neugates.io/zh) 
>
>Github 仓库：[https://github.com/emqx/neuron](https://github.com/emqx/neuron) 



四月，我们发布了 Neuron v2.0 的 rc.1 版本以及 release 版本，新增了 IEC60870-5-104 驱动，采用总召唤的方式采集数据，同时实现了与 eKuiper 的对接，支持将采集到的数据直接发送到 eKuiper。

## Neuron v2.0 新功能概览

- IEC60870-5-104 驱动

  驱动支持了 int16/uint16/float/bit 数据类型，使用总召唤的方式采集设备数据点位。协议层采用异步实现，提高采集效率。此协议配置的 group interval 只影响上报采集数据频率，读取频率可在 NODE 设置中单独配置。

  IEC TYPEID 对应到 Neuron 的数据类型如下：

  | **IEC TYPEID**                  | **NEURON TYPE** |
  | :------------------------------ | :-------------- |
  | M_ME_NB_1、M_ME_TE_1            | int16/uint16    |
  | M_ME_NC_1、M_ME_TF_1            | float           |
  | M_SP_NA_1、M_SP_TB_1            | bit             |
  | M_ME_NA_1、M_ME_TD_1、M_ME_ND_1 | int16/uint16    |

- 直接与 eKuiper 对接的插件

  Neuron 与 eKuiper 之间采用 nng pari0 直连的方式，降低数据延时。Neuron 作为 server，eKuiper 作为client，通过 Neuron-eKuiper 直接的数据格式进行数据传输，一个 Neuron 实例只支持连接一个 eKuiper 应用。

- MQTT 插件新增上报数据的格式

  新增数据格式更有利于使用 EMQX 以及 eKuiper 进行处理，另一种数据格式对于使用代码解析较为友好。

- 修改 read/write tag API，使用 name 字段替换 id 字段，调用 API 参数更加友好。
- OPC UA 以及 MQTT 使用 SSL 时，支持在 Dashboard 上选择证书以及公私钥，简化 SSL 连接时的操作。
- 新增 Driver 类型 adapter，降低 Driver 开发难度
- 支持以 Demo 的方式启动
- 增加了 Docker 版本
- Modules 模块中增加了 OPC UA 的功能测试

## Neuron v1.4.3 修正版

Neuron 1.x 后续不会再开发新功能，最后版本将会固定在 1.4.x，但可能会有 bug fix 版。

本月 v1.4.3 主要有以下更新：

- IEC104 再次修改总召唤的方式读取数据点位
- 在 Dashboard 修改小数点位时候，显示错误数值
