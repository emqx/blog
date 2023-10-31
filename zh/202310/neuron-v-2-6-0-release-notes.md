近日，EMQ 旗下的工业协议网关软件 [Neuron](https://www.emqx.com/zh/products/neuron) 发布了最新的 2.6.0 版本。

该版本新增了 **SECS GEM HSMS** 和 **KUKA Ethernet KRL TCP** 两个南向驱动和对接**格物平台**的一个北向应用，增加了部分软件功能，同时对现有的插件功能和 UI 进行了优化。

## 新增驱动介绍

#### SECS GEM HSMS 驱动

SECS/GEM (SEMI Equipment Communications Standard/Generic Equipment Model) HSMS (High-Speed Message Service) 是一种半导体制造设备之间和设备与工厂主机之间进行通信的标准协议。SECS/GEM HSMS 旨在提供高效的通信方式，以支持工厂自动化、追踪、控制和数据采集等操作。

Neuron 的 SECS GEM HSMS 驱动通过 TCP/IP 协议访问支持 SEMI E37 HSMS 标准的设备，目前支持设备 PASSIVE 模式，驱动作为 Host 主动连接。

[SECS GEM HSMS 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/secs-gem/secs-gem.html)

#### KUKA Ethernet KRL TCP 驱动

Neuron KUKA Ethernet KRL TCP 插件通过 TCP 协议访问安装有 KUKA Ethernet KRL 模块的 KUKA 机器人设备，目前支持机器人设备 Client和 Server 模式。

[KUKA Ethernet KRL TCP 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/kuka/kuka.html)

#### GEWU DMP-V1应用

Neuron 新增北向 GEWU DMP-V1 应用来对接联通格物平台。支持 Neuron 采集的数据点上报到格物平台，支持与格物平台的网关设备、子设备映射以及物模型匹配，可在格物平台实时查看设备数据信息。

想进一步了解插件详情，可联系 EMQ 销售。

## 新增功能

#### 配置文件功能

提供 json 格式配置文件配置 Neuron 相关个性化参数，目前支持 ip，port 和 disable_auth 三个配置项目，配置文件路径为 neuron 安装目录 config/neuron.json。默认配置内容如下:

```
{ "ip": "0.0.0.0", "port": 7000, "disable_auth": 0 }
```

#### 环境变量功能

Neuron 支持在启动过程中读取环境变量来配置启动参数，目前支持的环境变量如下:

| **配置名**            | **配置作用**                                                 |
| :-------------------- | :----------------------------------------------------------- |
| `NEURON_DAEMON`       | 设置为`1`，Neuron 守护进程运行；设置为`0`，Neuron 正常运行   |
| `NEURON_LOG`          | 设置为`1`，Neuron Log 输出到标准输出 stdout；设置为`0`，Neuron Log 不输出到标准输出 stdout； |
| `NEURON_LOG_LEVEL`    | Neuron 日志输出等级，可设置为 `DEBUG` 或 `NOTICE`                |
| `NEURON_RESTART`      | Neuron 重启设置，可设置为 `never`，`always`，`on-failure` 或者 `NUMBER`（1,2,3,4） |
| `NEURON_DISABLE_AUTH` | 设置为`1`，Neuron 关闭 Token 鉴权认证；设置为`0`，Neuron 开启 Token 鉴权认证 |
| `NEURON_CONFIG_DIR`   | Neuron 配置文件目录                                           |
| `NEURON_PLUGIN_DIR`   | Neuron 插件文件目录                                           |

#### Neuron 命令行功能更新

目前 neuron2.6 支持的命令行参数如下：

```
    -d, --daemon         run as daemon process
    -h, --help           show this help message
    stop                 stop running neuron
    --log                log to the stdout
    --log_level <LEVEL>  default log level(DEBUG,NOTICE)
    --reset-password     reset dashboard to use default password
    --restart <POLICY>   restart policy to apply when neuron daemon terminates,
                           - never,      never restart (default)
                           - always,     always restart
                           - on-failure, restart only if failure
                           - NUMBER,     restart max NUMBER of times
    --version            print version information
    --disable_auth       disable http api auth
    --config_file <PATH> startup parameter configuration file
    --config_dir <DIR>   directory from which neuron reads configuration
    --plugin_dir <DIR>   directory from which neuron loads plugin lib files
```

#### HTTP API 支持一次性多标签写入

Mitsubishi 3E、Beckhoff ADS、Modbus TCP、Modbus RTU、Siemens S7 ISOTCP、Omron FINS TCP、OPC UA、BACnet/IP 插件支持 HTTP API一次写入多个标签。

![HTTP API一次写入多个标签](https://assets.emqx.com/images/437fa6bfa492e3a1fbd17c945111821a.png)

#### MQTT 和 SparkPlugB 插件支持一次性多标签写入

![MQTT 和 SparkPlugB 插件支持一次性多标签写入](https://assets.emqx.com/images/5fbcf8dd4f1f5f8df521c0e79233bdde.png)

## 功能优化提升

#### 北向应用支持批量订阅南向驱动数据

![添加订阅](https://assets.emqx.com/images/4836b3c5bccd8be34087ae2fac705e79.png)

#### 驱动状态信息显示内容优化

![驱动状态](https://assets.emqx.com/images/15bba2dbb30779bd35c6d619c43e285c.png)

#### 北向应用支持修改已订阅群组的订阅参数

![北向应用](https://assets.emqx.com/images/0a55b6dc27af2ee9f760c0ae82034f46.png)

## 现有插件功能优化

- OPCUA 插件支持异步读写功能；

- Modbus 支持 BYTE 数据类型；

- BACnet/IP 插件支持读写任意对象、读写任意对象属性以及处理包含路由帧的消息；

- IEC60870-5-104 插件支持突发数据的及时上报。 IEC60870-5-104 插件支持报告标签时间戳和标签质量解析；

- DLT645-2007 和 DLT645-1997 插件支持根据响应消息地址更新标签值；

- 西门子 S7 ISOTCP 插件支持 INT8/UINT8 数据类型。 西门子 S7 ISOTCP 插件性能优化：在处理大量标签时，减慢请求速率以匹配 PLC 处理性能；

- MQTT 插件支持离线数据上报频率控制；

- MQTT 插件将随机字符串附加到 client_id，生成长度为 6 的随机字符串。

## 结语

Neuron 将持续对产品功能进行升级优化，目前，EMQ官网提供了 Neuron 安装包下载，支持 30 点位免费试用，欢迎大家下载试用。



<section class="promotion">
    <div>
        免费试用 Neuron
      <div class="is-size-14 is-text-normal has-text-weight-normal">连接海量异构工业设备从边缘到云端。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
