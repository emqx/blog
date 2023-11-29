随着物联网、大数据、云计算等新一代信息技术的发展变革，IoT 深入到各种行业与应用场景，整体呈现设备多态化、业务多样化、应用碎片化的趋势。尤其在工业物联场景中，工业设备种类繁多，设计总线、协议复杂多样，业务应用灵活多变，如何顺利实现工业设备上云是亟待解决的问题。 **EMQX 系列产品提供解耦工业设备与应用的能力，构造边缘到云端数据通路，建立智能、网络、轻量的数字化产品与服务模式，并与 5G 相融合，支撑工业行业应用创新**。



## 工业物联网时代

IIoT 即 Industrial Internet of Things 的简称，是指数以亿计的工业设备所形成的[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)。广义上来讲，是指在交通、能源、工业等部门的机械、车辆上应用仪器、连接传感器等设备。

随着 [工业 4.0](https://baike.baidu.com/item/%E5%B7%A5%E4%B8%9A4.0/2120694) 概念的普及与行业实践的深入，传统的集中式控制模式向分散式增强型控制模式转变。同时，5G 时代的到来，也加速了传统工业改造和工业物联网化的进程。为了实现个性化、数字化的产品与服务的灵活生产，在工业设备智能化、网络化的过程中，需要将新旧工业设备连接到互联网中，实现对工业设备的数据采集、远程控制、配置更新等业务。EMQX 系列产品可提供从工业网关到平台的整体解决方案，支持在厂区和工业现场等边缘端实现工业设备的数据汇聚并发送到云端。同时，其对边缘计算流数据的处理能力，可在平台端为工业物联网应用提供云端工业设备数据接入、数据存储以及与云端组态和应用的对接，方便工业互联网应用的快速开发。

以下，我们将通过 [Neuron](https://www.emqx.com/zh/products/neuronex)、[EMQX](https://www.emqx.com/zh/products/emqx) 构建基于 [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) 的简易 IIoT 应用，并使用 [MQTTX](https://mqttx.app/zh) 订阅/展示数据。



## EMQX Neuron简介

EMQ 于近日发布了布署在边缘网关上的 [工业协议接入软件 Neuron](https://www.emqx.com/zh/products/neuronex)。作为人与机器之间的桥梁，它可以把 TCP/IP 协议的 0/1 数据，转化重组成通俗易懂的 JSON 格式，并使用 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide) 输出到云端，更好地处理人与物之间的交互。

EMQX Neuron 支持包括 Modbus、OPC 等在内的各类工业协议，可以基本满足大部分工业接入的需求，详细协议列表见下图。

| **Protocol Name**                                            | **Type** | **Status** |
| ------------------------------------------------------------ | -------- | ---------- |
| **Allen-Bradley DF1 half-duplex for PLC2**                   | Serial   | Avail      |
| **Allen-Bradley DF1 half-duplex for PLC5**                   | Serial   | Avail      |
| **Allen-Bradley DF1 for MicroLogix**                         | Serial   | 2020       |
| **Allen-Bradley Ethernet/IP for MicroLogix**                 | Ethernet | 2020       |
| **Allen-Bradley DF1 for  ControlLogix/CompactLogix/FelxLogix** | Serial   | 2020       |
| **Allen-Bradley Ethernet/IP for ControlLogix/CompactLogix/FelxLogix** | Ethernet | 2020       |
| **Schneider Modbus RTU**                                     | Serial   | Avail      |
| **Schneider Modbus TCP**                                     | Ethernet | Avail      |
| **Schneider Telemecanique UNI-TE**                           | Serial   | Avail      |
| **ABB SattControl Comli**                                    | Serial   | Avail      |
| **Omron Host Link (single)**                                 | Serial   | Avail      |
| **Omron Host Link (multiple)**                               | Serial   | Avail      |
| **Omron   FINS on Host Link**                                | Serial   | 2020       |
| **Omron   FINS on TCP**                                      | Ethernet | 2020       |
| **Omron   FINS on UDP**                                      | Ethernet | 2020       |
| **Omron   Ethernet/IP for CJ/NJ**                            | Ethernet | 2020       |
| **Siemens 3964R/RK512 for S5**                               | Serial   | Avail      |
| **Siemens 3964R/RK512 for S7**                               | Serial   | Avail      |
| **Siemens PPI for S7-200**                                   | Serial   | 2020       |
| **Siemens MPI for S7-300**                                   | Serial   | 2020       |
| **Siemens Fetch Write for S7-300/400 and CP443 module**      | Ethernet | Avail      |
| **Siemens Industrial Ethernet ISO for S7-300/400**           | Ethernet | Avail      |
| **Siemens IE Symbolic Addressing for S7-1200**               | Ethernet | 2020       |
| **Siemens IE Absolute Addressing for S7-1200/1500**          | Ethernet | 2020       |
| **Mitsubishi FX0N/FX0S/FX1N/FX1S/FX2**                       | Serial   | Avail      |
| **Mitsubishi   FX2N/FX3U/FX3G/FX3S**                         | Serial   | Avail      |
| **Mitsubishi   FX3U-ENET-L/FX3U-ENET-ADP**                   | Ethernet | 2020       |
| **Mitsubishi   FX5U**                                        | Serial   | 2020       |
| **Mitsubishi   FX5U Ethernet Module**                        | Ethernet | 2020       |
| **Mitsubishi   FX 232ADP/485BD/232BD Module**                | RS485    | 2020       |
| **Mitsubishi MC Protocol full-duplex for MELSEC-Q and C24   module** | Serial   | 2020       |
| **Mitsubishi MC Protocol for MELSEC-Q and E71 module**       | Ethernet | Avail      |
| **Panasonic MEWTOCOL for FP**                                | Ethernet | 2020       |
| **GE SNP for 90-30**                                         | Serial   | 2020       |
| **GE Ethernet for 90-30**                                    | Ethernet | 2020       |
| **FANUC 0i/30i/31i/32i/35i**                                 | Serial   | 2020       |
| **FANUC 0i/30i/31i/32i/35i Ethernet**                        | Ethernet | 2020       |
| **FANUC T21/D21 for CNC machines**                           | Ethernet | 2020       |
| **Modbus RTU**                                               | RS485    | Avail      |
| **Modbus RTU over TCP**                                      | Ethernet | Avail      |
| **Modbus TCP**                                               | Ethernet | Avail      |
| **OPC UA**                                                   | Ethernet | Avail      |
| **BACnet/MSTP**                                              | RS485    | 2020       |
| **BACnet/IP**                                                | Ethernet | 2020       |
| **IEC 60870-5 (IEC104)**                                     | Ethernet | 2020       |
| **IEC 61850**                                                | Ethernet | 2020       |
| **SNMP**                                                     | Ethernet | 2020       |
| **DNP3**                                                     | Ethernet | 2020       |
| **DLT645-97/07**                                             | Ethernet | 2020       |



## EMQX Neuron 与 EMQX Broker 的工业架构图

![image20200807171225345.png](https://assets.emqx.com/images/12761e4b416abbc4623b9702138af74f.png)



## 本次模拟使用工具列表

| 工具名称                | 版本  | 用途                 | 操作系统            |
| ----------------------- | ----- | -------------------- | ------------------- |
| PeakHMI Slave Simulator | /     | Modbus 模拟器        | Windows Server 2019 |
| EMQX Neuron            | 1.4.6 | 工业协议网关接入软件 | Ubuntu 16.04        |
| EMQX Broker            | 4.0.7 | MQTT Broker          | Ubuntu 16.04        |
| MQTTX                  | 1.3.2 | MQTT 客户端工具      | macOS 10.13.4       |



## 模拟工业场景测试

### 布署/配置 EMQX Neuron 产品

1.首先解压安装 EMQX Neuron 软件包。

```
tar -xvlf neuron-1.4.2-x86_64.tar.gz 

sudo ~/bin/installneuron.sh 
```



2.在配置文件配置连接到 EMQX Broker 的地址，配上用户名密码作为认证。

```
cd bin/ 

vi neuron.conf  
```

neuron.conf 中修改 EMQX Broker 服务端的 IP/ 端口，用户名/密码信息。

```
# MQTT server name or IP address

MQSERVER=127.0.0.1

# Server port no. Note that it will have SSL connection if setting the port no. 

# 8000 or above.

MQPORTNO=1883

# Username and password

MQUSERNAME=emqx123

MQPASSWORD=neuron123
```



3.启动 EMQX Neuron 软件，无报错即为启动完成。

```
./neuronsrt  
```



4.登陆 EMQX Neuron Web 界面，访问 IP:7000，默认用户名密码 admin/0000。

![neuron 2.png](https://assets.emqx.com/images/973234d18311847a14cf528905470003.png)



5.点击 Edit Driver，编辑 Modbus tcp 地址。

![image20200721163444017.png](https://assets.emqx.com/images/50eec1ed148b0e0915631d959797d16c.png)

![image20200721163701173.png](https://assets.emqx.com/images/66a82faba86ba6805130d0652a625add.png)


6.创建 Object，定义 Object 里面的内容。

![image20200807162508543.png](https://assets.emqx.com/images/d89381a20c603d47d6c00ac8a1747efb.png)

在这个 Object 里面创建一个 Attribute，然后配置 Attribute 的信息，

这里模拟定义名称为 Err1@@2D7WS_GAS 的报警点位，点位位置为 1!1!07497。

![image20200807162911196.png](https://assets.emqx.com/images/36b42a9ff0e916276319eb7dd3c2004c.png)

![image20200807163023400.png](https://assets.emqx.com/images/9faedfb368dfc1817bdee1ad2ed4fc48.png)


### 连接布署好的 EMQX Broker 产品

在 EMQX Broker 界面上可以查看连接的 EMQX Neuron 网关，Client ID 为 EMQX Neuron 网关随机生成一串字符。

![image20200807163206577.png](https://assets.emqx.com/images/489ab3a96deb7680692a67c102bff461.png)



### 配置 Modbus 模拟器

配置刚才 1!1!07497 点位值为 1，然后进行数据上报。

![image20200807164517861.png](https://assets.emqx.com/images/72ce71e681e9a388b593c16e0626b88f.png)



点击 EMQX Neuron 界面中的 Data Monitoring，Attribute 中配置 1!1!07497 点位的数值已经为 1。

![image20200807164756754.png](https://assets.emqx.com/images/20c4b877d66dfe467d70bf2048af52e0.png)


### 用 MQTTX 订阅数据进行展示

打开连接好的 MQTTX，连接到 EMQX Broker，订阅上面 EMQX Neuron 发布的主题，在 MQTTX 可以收到 AlarmObj 里 2D7WS 的值为 1。客户端收到这些数据后，可以在应用界面上显示告警，也可以通过业务逻辑实现业务上的其它业务转换.

![image20200807165527066.png](https://assets.emqx.com/images/fea1dd077e66b71857e2f3530c71cfc9.png)


## 总结

以上我们使用 EMQX Neuron、EMQX Broker、MQTTX 等工具完整进行全流程的工业接入模拟测试，对于工业设备上云形成更加清晰与直观的认知。当然，您也可以结合 EMQX Neuron 强大协议支持与 EMQX Broker 强大的接入/转发能力，自己开发一套应用展示系统，构建一整套 IIoT 平台。

**2020 年 9 月**底，我们将通过集成 [Neuron](https://www.emqx.com/zh/products/neuronex)，[Edge](https://www.emqx.com/zh/products/emqx) 和 [Kuiper](https://github.com/lf-edge/ekuiper) 等软件，实现在边缘端的工业协议解析、数据汇聚和流式处理的一整套边缘解决方案；该方案通过与云端的 EMQX Broker / Enterprise 等系列产品集成，则可以实现一个端到端的、从边缘到云端的完整工业解决方案。

![Artboard Copy 9备份 4.png](https://assets.emqx.com/images/17040dd8943482858425cfb3fe197e82.png)


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
