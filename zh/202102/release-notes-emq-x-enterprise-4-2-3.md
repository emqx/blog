## 前言

在过去的几年中，车联网已经从概念发展成潮流，席卷各大汽车制造商和相关的上下游行业，围绕车联网产业标准体系建设，我国相关部门一系列的指导标准应运而生。

EMQ 致力于为企业提供优质的万物互联引擎，不仅与主流汽车制造商及产业链相关企业建立了广泛的合作，也从国家标准和行业标准层面提供了更多的能力和技术支持。此前 EMQ X 已经支持 JT/T 808 协议， **随着 v4.2.3 版本发布，EMQ X 新增了又一个车联网相关 GB/T32960 协议的接入能力。**

《GB/T32960 电动汽车远程服务与管理系统技术规范:通讯协议及数据格式》是用于新能源车辆远程服务平台间通讯的指导标准，基于 TCP 传输协议，可应用于车载通讯模块与远程服务平台间的通讯。 **本文将从使用者角度介绍 EMQ X 如何接入 GB/T32960 协议设备。**



## 工作原理

EMQ X 企业版中提供了 GB/T 32960 协议网关模块，按照其功能逻辑和整个系统的关系，将整个消息交换的过程可以分成三个部分：终端侧，平台侧和其它侧。

![画板2x.png](https://static.emqx.net/images/1309966aded70c111bf9b8ed3b3a5ee4.png)

1. 终端侧：通过 GB/T 32960 协议进行交换数据，实现不同类型的数据的上报，或者发送下行的消息到终端。
2. 平台侧：EMQ X GB/T 32960 网关将报文解码后在 EMQ X 内部转为 MQTT 协议进行数据上下行操作：
   - 数据上行：将上行数据报文以 MQTT PUBLISH 的形式发布到特定的主题上；
   - 数据下行：将需要下行的数据 PUBLISH 到特定的主题，消息将转化为 GB/T 32960 协议的报文结构，下发到终端。
3. 其它侧，通过 EMQ X 企业版的规则引擎可以将 2 中出现的上行数据存储/转发到企业的数据库、流处理平台（如 Kafka）和业务系统中；企业应用平台可以通过多种方式下发控制指令到 EMQ X，最终将数据发送到终端侧。



## 如何启用

下载 EMQ X 企业版 v4.2.3 之后的版本，启动之后打开 Dashboard，在 **模块** 菜单下添加并启用 **GB/T 32960 网关**即可。

1. 点击 选择 进入模块选择界面，在 **协议接入** 中选择  **GB/T 32960 网关** ；
2. 点击 选择 按钮，进入  **GB/T 32960 网关** 配置页面，进行启动前配置；
3. 配置重传、报文、消息长度等参数之后，配置 TCP 监听器参数，点击 添加 后即可启用 GB/T 32960 网关。

![image20210204150409040.png](https://static.emqx.net/images/5235a04561f6b355a4df35d52e18dfa2.png)

![image20210204150435383.png](https://static.emqx.net/images/434b09bd47c15f406987825690fae2fb.png)

![image20210204150536753.png](https://static.emqx.net/images/31618fa76a949d445b1dc3755d415ba3.png)

## 相关资料

在开发与支持过程中，我们整理了 GB/T 32960 行业与开发相关的资料如下：

- GBT 32960.1-2016 电动汽车远程服务与管理系统技术规范 第1部分：总则
- GBT 32960.2-2016 电动汽车远程服务与管理系统技术规范 第2部分：车载终端
- GBT 32960.3-2016 电动汽车远程服务与管理系统技术规范 第3部分：通讯协议及数据格式
- EMQ X 企业版 GB/T 32960 网关数据交换格式

**关注 EMQX 微信公众号，回复「 32960 」即可获取资料下载地址。**



## 附：数据交换格式示例

以下是 GB/T 32960 和 EMQ X 之间数据交换的格式，数据格式有以下约定：

- Payload 采用 JSON 格式进行组装
- JSON Key 采用大驼峰格式命名

由于篇幅有限，此处仅提供部分交换格式示例，完整数据格式详见文末资料以及官网文档。

### 上行数据

数据流向: Terminal -> GB/T 32960 网关 -> EMQ X。

#### 车辆登入

Topic: gbt32960/${vin}/upstream/vlogin

```json
{
    "Cmd": 1,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "ICCID": "12345678901234567890",
        "Id": "C",
        "Length": 1,
        "Num": 1,
        "Seq": 1,
        "Time": {
            "Day": 29,
            "Hour": 12,
            "Minute": 19,
            "Month": 12,
            "Second": 20,
            "Year": 12
        }
    }
}
```

#### 车辆登出

Topic: gbt32960/${vin}/upstream/vlogout

```json
{
    "Cmd": 4,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Seq": 1,
        "Time": {
            "Day": 1,
            "Hour": 2,
            "Minute": 59,
            "Month": 1,
            "Second": 0,
            "Year": 16
        }
    }
}
```

### 下行数据

GB/T 32960 网关对终端的控制采用 Request-Response 模式，向对用的 Topic 发送控制数据，响应结果将从特性的 Topic 返回：

#### 请求

请求数据流向：EMQ X -> GB/T 32960 网关 -> Terminal

下行主题：gbt32960/${vin}/dnstream

#### 应答

应答数据流向：Terminal -> GB/T 32960 网关 -> EMQ X

上行应答主题：gbt32960/${vin}/upstream/response

#### 参数查询

**Req:**

```
{
    "Action": "Query",
    "Total": 2,
    "Ids": ["0x01", "0x02"]
}
```

**Response:**

```
{
    "Cmd": 128,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Total": 2,
        "Params": [
            {"0x01": 6000},
            {"0x02": 10}
        ],
        "Time": {
            "Day": 2,
            "Hour": 11,
            "Minute": 12,
            "Month": 2,
            "Second": 12,
            "Year": 17
        }
    }
}
```

#### 参数设置

**Req:**

```
{
    "Action": "Setting",
    "Total": 2,
    "Params": [{"0x01": 5000},
               {"0x02": 200}]
}
```

**Response:**

```
// fixme? 终端是按照这种方式返回?
{
    "Cmd": 129,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Total": 2,
        "Params": [
            {"0x01": 5000},
            {"0x02": 200}
        ],
        "Time": {
            "Day": 2,
            "Hour": 11,
            "Minute": 12,
            "Month": 2,
            "Second": 12,
            "Year": 17
        }
    }
}
```

#### 终端控制

远程升级: **Req:**

```
{
    "Action": "Control",
    "Command": "0x01",
    "Param": {
        "DialingName": "hz203",
        "Username": "user001",
        "Password": "password01",
        "Ip": "192.168.199.1",
        "Port": 8080,
        "ManufacturerId": "BMWA",
        "HardwareVer": "1.0.0",
        "SoftwareVer": "1.0.0",
        "UpgradeUrl": "ftp://emqtt.io/ftp/server",
        "Timeout": 10
    }
}
```

车载终端关机:

```
{
    "Action": "Control",
    "Command": "0x02"
}
```


车载终端报警:

```
{
    "Action": "Control",
    "Command": "0x06",
    "Param": {"Level": 0, "Message": "alarm message"}
}
```
