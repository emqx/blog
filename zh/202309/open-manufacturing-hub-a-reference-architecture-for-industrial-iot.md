## 引言

在[工业物联网](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)快速发展的今天，实现无缝连接、实时数据处理和高效系统管理的需求空前迫切。随着各个行业持续探索互联设备的变革潜力，构建一个坚实且灵活的技术栈变得尤为重要。

EMQ 提出了一个名为 Open Manufacturing Hub 的开源工业物联网解决方案，以帮助工业用户充分发挥工业连接和实时数据的潜能。在本文中，我们将带您深入了解 Open Manufacturing Hub，详细演示如何部署这一创新方案，并展示它如何改变我们开发工业系统的思路。

## 工业物联网综合解决方案

Open Manufacturing Hub 为构建强大和可扩展的工业物联网应用提供了完整的解决方案。这些应用协同工作，能够实现无缝的数据连接、高效的消息队列、以及可靠的时序数据存储和分析。

Open Manufacturing Hub 旨在让制造企业能够实现卓越的智能制造水平，通过运用先进的工业物联网技术和数据驱动的洞察力，来优化运营流程、提升生产力、保障质量，在制造价值链中激发创新。

### 架构基本组件

Open Manufacturing Hub 的主要组件包括：

- Python Modbus 模拟器：模拟 Modbus 设备的 Python 应用，能够持续产生 Modbus 数据。

- [Neuron 工业连接服务器](https://www.emqx.com/en/products/neuron)：充当工业连接的设备枢纽，能够实现多种工业协议和工业物联网系统之间的无缝集成。

- [EMQX MQTT Broker](https://www.emqx.com/en/products/emqx)：工业物联网基础设施的核心，为工业应用提供了可靠和可扩展的消息传输系统。

- Timescale 数据库：专门处理时序数据的数据库，为存储和分析 Python 模拟器生成的海量时序数据提供了完美的解决方案。

- Grafana 可视化：知名的开源数据可视化平台，能够与 Timescale 无缝集成，提供实时和历史数据的可视化展示。

企业可以通过使用上述技术栈获得一系列的好处。它能够提供实时的洞察力，帮助企业优化工业流程、提升运营效率、做出更明智的决策。企业从而可以提高收入，缩短上市周期，降低运营成本，改善产品质量。

### 架构工作流程

使用 EMQX 和 Neuron 构建高效和可扩展的工业物联网系统非常简单。除了 Python Modbus 模拟器之外，所有软件组件都在独立的 Docker 容器中运行。Python Modbus 模拟器是一个生成演示数据的程序。

在 Modbus 模拟器中，Python 程序会随机生成两个温度和湿度样本值，分别存储在 Modbus 寄存器 400001 和 400002 中。Neuron 作为工业连接服务器，被配置为以 1 秒的固定间隔访问这两个 Modbus 寄存器。然后，Neuron 会将 Modbus 寄存器中的数据转换成 MQTT 消息，并将其发布到 EMQX Broker。

EMQX MQTT Broker 能够高效处理传入的数据，并通过规则引擎将其转发到 TimescaleDB 数据库。然后，代表温度和湿度值的数据会被写入 TimescaleDB 数据库，该数据库专门针对时序数据的存储进行了优化。

最后，数据可视化平台 Grafana 从 TimescaleDB 中检索时序数据，并利用这些数据创建动态的可视化图表和实时的数据洞察。用户可以通过 Grafana 的自定义仪表盘以直观和友好的方式查看和分析温度和湿度数据。

![Slice 165.png](https://assets.emqx.com/images/17987b9b27fe3152c09ada98db7f3740.jpg)

## 演示：构建高效、可扩展的工业物联网系统

下面将详细介绍基础设施中包含的所有应用的简易安装步骤。我们将使用 Docker 技术来降低安装难度。

### 安装演示环境的前期准备

1. Docker 安装：访问 Docker 网站（[https://www.docker.com](https://www.docker.com/)）并下载合适的 Docker 版本。

2. Python3 安装：访问 Python 官方网站 https://www.python.org/downloads/ 。 您可以下载最新的 Python 稳定版本。

### Docker Compose 安装

为了安装 Neuron、EMQX、Timescale 和 Grafana，我们需要准备一个 docker compose 文件 docker_compose.yml。

```
version: '3.4'
​
services:
​
  neuron:
    image: emqx/neuron:2.4.8
    ports:
      - "7000:7000"
      - "7001:7001"
    container_name: neuron
    hostname: neuron
    volumes:
      - nng-ipc:/tmp
​
  emqx:
    image: emqx/emqx-ee:4.4.18
    ports:
      - "1883:1883"
      - "18083:18083"
    container_name: emqx
    hostname: emqx
​
  timescaledb:
    image: timescale/timescaledb-ha:pg14-latest
    restart: always
    ports:
      - 5432:5432
    container_name: timescaledb
    hostname: timescaledb
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - /data/timescaledb:/var/lib/postgresql/data
​
  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    hostname: grafana
    restart: unless-stopped
    ports:
     - 3000:3000
​
volumes:
  nng-ipc:
```

在 docker_compose.yml 所在的目录下，运行以下 docker 命令启动所有的 docker 组件：

```
$ sudo docker compose up -d
```

这个命令将以后台模式启动 docker-compose.yml 文件中定义的服务。

当看到下面的消息时，表示已经成功地在 docker 环境中运行了这些组件。

![图片.png](https://assets.emqx.com/images/88e5d5c0304487c1a7011cc7ce29dc69.png)

要获取 docker 虚拟 IP 地址，请运行以下命令：

```
$ ifconfig
```

注意：下图中显示的 docker 虚拟 IP 地址是 172.17.0.1。在后续演示过程中这个 IP 将被用作主机名参数。

![图片.png](https://assets.emqx.com/images/4f00faf95c39af43f8e00086e305e28c.png)

### Python Modbus 模拟器程序

模拟程序使用了 pymodbus 模块，以便于 Modbus 服务器的通信。该 Python 程序能够让用户控制数据的输出，以根据需要自动产生数据。下面是用 Python 编写的示例代码：

```
#!/usr/bin/env python3
​
-- coding: utf-8 --
​
"""
Created on Thu Jun 30 09:54:56 2023
​
@author: Joey
"""
#!/usr/bin/env python
from pymodbus.version import version
from pymodbus.server import StartTcpServer
from pymodbus.server import StartTlsServer
from pymodbus.server import StartUdpServer
from pymodbus.server import StartSerialServer
​
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
​
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
import time
from threading import Thread
import random
---------------------------------------------------------------------------
​
configure the service logging
​
---------------------------------------------------------------------------
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
​
def data_change(name,s):
    a = 0
    while True:
        data = [a]*2
        data[0] = int(280 + random.random()*30)
        data[1] = int(700 + random.random()*30)
        s.setValues(3,0,data)
        time.sleep(1)
​
def run_server():
    slave_context = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*2))
    slaves = {}
    for i in range(1,2):
        slaves[i] = slave_context
    context = ModbusServerContext(slaves=slaves, single=False)
​
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = '<http://github.com/riptideio/pymodbus/'>
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.5'
​
    t1 = Thread(target=data_change,args=("thread-1",slave_context))
    t1.start()
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))
    t1.join()
​
if name == "main":
    run_server()
```

运行此代码前，请执行以下命令安装 pymodbus 模块：

```
$ pip install pymodbus
```

在放置模拟器 Python 程序文件的目录中，运行以下命令启动 pymodbus 模拟器：

```
$ sudo python3 simu.py 
```

![图片.png](https://assets.emqx.com/images/41e49c3257f5eb53fad13d1df3e58b41.png)

### Neuron 安装指南

通过创建南向设备节点，Neuron 可以接入各种设备，例如，演示中的 Modbus 模拟器。

通过创建北向应用节点，Neuron 能够与 EMQX 建立连接，并将采集的设备数据上传到 EMQX。

**第 1 步**：启动浏览器，输入网址 `https://hostname:7000/`

使用用户名“admin”和密码“0000”登录。

**第 2 步**：添加南向设备

在配置菜单中选择“南向设备”，进入南向设备界面。单击“添加设备”来添加新设备。

![图片.png](https://assets.emqx.com/images/e14d97bf06eefb5f3136d26a2777c250.png)

填写设备名称，从插件下拉框中选择 Modbus TCP，然后点击“创建”按钮。

![图片.png](https://assets.emqx.com/images/ed9a1473055c56b9750c30ae38f7261a.png)

**第 3 步**：设置南向设备参数

添加完南向设备后，填写以下参数，然后点击“提交”按钮。

![图片.png](https://assets.emqx.com/images/9518cda52ea39ae96b669caa9ee7fce8.png)

注意：Docker 虚拟网络的 IP 地址为 172.17.0.1。

**第 4 步**：在设备卡中创建组

单击设备名称“demo”，会显示一个空的组列表。单击“创建”按钮，在对话框中填写组名称和间隔时间，然后单击“创建”按钮。

![图片.png](https://assets.emqx.com/images/f8a2bab1267dd7c7399c671fad90e331.png)

**第 5 步**：向组中添加标签

单击组名“demo_group”，进入到标签列表页面。单击“创建”按钮，添加标签点。在第一行的标签点中填写名称“temperature”，在第二行的标签点中填写名称“humidity”。

![图片.png](https://assets.emqx.com/images/09992ffe9663e6c1cb6ca3298bf17e8d.png)

温度和湿度的标签地址分别是 1!40001 和 1!40002，其中 1 是站点号，40001 和 40002 分别是温度寄存器和湿度寄存器。

**第 6 步**：在数据监控菜单中查看收集的数据

从左侧导航菜单中选择监控→数据监控。在南向设备框中选择“demo”，在组名框中选择“demo_group”。温度和湿度的值将显示如下：

![图片.png](https://assets.emqx.com/images/f094f2e35e957b0cd3d8904cd71904cd.png)

注意：此时 Neuron 已成功连接到 Python 模拟器。数值将在 280 和 700 之间波动。

**第 7 步**：向应用添加北向插件模块

从左侧导航菜单中选择配置→北向应用。单击“添加应用”按钮，填写应用名称 “demo_app”，选择插件“MQTT”，如下图所示：

![图片.png](https://assets.emqx.com/images/c8633caed1263e9390ceb0e00305ccd8.png)

**第 8 步**：配置北向应用参数

北向应用添加完成后，MQTT 应用参数列表将显示出来。在 Broker 主机中填写 docker 虚拟 IP 地址“172.17.0.1”，其他参数保持不变。完成后，单击“提交”按钮，保存参数。

![图片.png](https://assets.emqx.com/images/8233015dea9de752a86dfb2626628eaf.png)

**第 9 步**：订阅南向点位组

点击“demo_app”名称，进入到组列表订阅页面。点击“添加订阅”按钮。在南向设备框中选择“demo”，在组框中选择“demo_group”。如图所示，使用默认的主题，然后点击“提交”按钮。

![图片.png](https://assets.emqx.com/images/696d0a25e3cac242f0d0b42e25030ea3.png)

**第 10 步**：使用 [MQTTX](https://mqttx.app/) 查看 MQTT 连接

在 Windows 平台上启动 MQTTX。在主页面上点击“新建连接”，填写配置参数，然后点击右上角的“连接”按钮。

点击添加订阅，主题应该与第 9 步中的相同。例如，填写“/neuron/demo_app/demo/demo_group”。订阅成功后，可以看到 MQTTX 会不断接收 Neuron 收集和上报的数据，如下图所示。

![图片.png](https://assets.emqx.com/images/c8ec42b6605df52ba1f98f6edbd9ecf5.png)

当 MQTTX 持续显示从 EMQX Broker 订阅的消息时，表示 Neuron 已经成功地将设备数据消息连续发布到 EMQX Broker。

> 注意：这里我们使用 [MQTTX](https://mqttx.app/)，它是一个功能强大的跨平台 MQTT 客户端工具，可以从官方网站下载：[MQTTX Download](https://mqttx.app/downloads) 。

### Timescale 数据库安装步骤

在 EMQX 将数据写入 Timescale 数据库之前，必须在 Timescale 数据库中创建数据库和表。

**第 1 步**：使用 docker 执行 psql 命令行工具，设置 Timescale 数据库。

```
$ sudo docker exec -it timescaledb psql -U postgres
```

**第 2 步**：在 Timescale 中创建数据库“demo”

在命令提示符下输入 `Create database demo;` 创建演示数据库。创建成功后，将连接到数据库并创建扩展，如下图所示：

![图片.png](https://assets.emqx.com/images/0912f030c34f66992cb43635165481c2.png)

**第 3 步**：在数据库“demo”中创建表“conditions”

扩展创建完成后要创建表“conditions”，其中包含字段“time”、“temperature”和“humidity”，如下图所示：

![图片.png](https://assets.emqx.com/images/7e2a9646101846ee522a8fbc81cb8605.png)

**第 4 步**：检查表“conditions”

最后，使用命令 `\dt` 检查“conditions”表，如下图所示：

![图片.png](https://assets.emqx.com/images/70b4eca2c7b72581235fde5615832740.png)

### 设置 EMQX 将数据输入时序数据库

完成数据库创建过程后，EMQX 现在可以连接到 Timescale 数据库了。按照以下步骤设置必要的参数和 SQL 语句。

**第 1 步**：启动浏览器，输入网址 `http://hostname:18083/`

使用用户名“admin”和密码“public”登录。

注意：在首次登录时系统会要求您修改密码。

**第 2 步**：在规则引擎中创建将数据写入 Timescale 的规则。

在 EMQX Dashboard 中，选择左侧菜单栏的“规则”选项卡。点击“创建”按钮，在 SQL 框中创建如下的规则：

![图片.png](https://assets.emqx.com/images/1da0d51d5743afffb18d07ded50347ec.png)

**第 3 步**：为规则添加动作

当 SQL 成功执行时，规则会触发动作。点击规则引擎底部的“添加动作”按钮。在动作类型中选择“Data persist”和“Data to Timescale”。

![图片.png](https://assets.emqx.com/images/732c7c0e0896cc5d577c280a7eb1eee7.png)

**第 4 步**：在规则动作中添加资源

点击上述“动作”界面中“使用资源”旁边的“创建”链接，资源界面将显示如下。填写服务器 IP “172.17.0.1”，数据库“demo”，用户“postgres”，密码“password”，如下图所示，并点击“确认”按钮返回创建规则界面。

![图片.png](https://assets.emqx.com/images/11c882997487ff9b29d074fe2ce79bd1.png)

**第 5 步**：添加 SQL 语句来写入数据

最后，填写 SQL 模板。在这个例子中，我们向 Timescale 插入一条数据，SQL 模板如下，输入完成后点击“确认”按钮。

![图片.png](https://assets.emqx.com/images/458fe2e1ac24e0c13e563d5b6cb71f10.png)

> 注意：在插入数据时，SQL 模板中的 ${temperature} 和 ${humidity} 占位符会被替换为相应的值。

**第 6 步**：检查 Timescale 数据库中的数据

在数据库“demo”中输入下面的 SELECT 语句，应该能够看到几行数据，表示温度和湿度数据已成功保存在 Timescale 数据库中了。

![图片.png](https://assets.emqx.com/images/7d0a7097afdbff368131c9dca0e0cb4a.png)

### 设置 Grafana 从 Timescale 数据库检索数据

将 Grafana 应用连接到 Timescale 数据库，以提供温度和湿度读数的可视化图表，设置步骤如下。

**第 1 步**：启动浏览器，输入网址 `http://hostname:3000`

使用用户名“admin”和密码“admin”登录。

注意：首次登录时需要设置新密码。

**第 2 步**：设置数据源

从数据源页面中选择 PostgreSQL 数据源。输入 Timescale 数据库连接的主机、数据库、用户和密码。

![图片.png](https://assets.emqx.com/images/defb59772405c955fb7d710b055c271c.png)

在页面的末尾，应该看到如下信息：

![图片.png](https://assets.emqx.com/images/b3edc6b4e7262a01788f959f86d94976.png)

**第 3 步**：添加可视化

从列表中选择数据源“Timescale”，构建如下的 SQL 查询。依次填写列“time”、“temperature”和“humidity”。点击右上角的“保存”按钮，保存可视化。

![图片.png](https://assets.emqx.com/images/9efaebdd5d9e883214e7ade98177d805.png)

**第 4 步**：查看可视化图表

现在，可以在可视化图表中查看温度和湿度数据了。演示设置到此结束。

![图片.png](https://assets.emqx.com/images/2dbb78690efc785fd9c232a963450ad8.png)

## 丰富的 IT 和 OT 连接

上面的演示提供了一个简明的 Modbus 连接并访问 Timescale 数据库的示例。然而，值得注意的是，Neuron 和 EMQX 均提供多种驱动程序和连接器，以满足不同的 OT 和 IT 连接需求。这些广泛的 OT 和 IT 能力对于成功开发 IIoT 系统至关重要。EMQ 的 Open Manufacturing Hub 解决方案，能够将这些强大的 IT 和 OT 技术无缝融合到工业物联网系统中。

![Slice 172.png](https://assets.emqx.com/images/39ae8f1b1770b86559c31455eeaa90cf.jpg)

### 无缝的 IT 连接

EMQX 提供了强大的数据桥接能力，能够与 40 多种云服务和企业系统无缝集成，从而可以跨不同应用即时访问数据，降低了定制桥接开发的成本和复杂度。EMQX 支持与各种数据库（例如 MySQL、PostgreSQL、MongoDB）以及技术（例如 Redis、Oracle、SAP、Kafka）的集成，丰富的连接器集合确保了工业物联网生态系统中的高效 IT 连接和数据交换。

### 多样的 OT 连接

作为一个协议网关，Neuron 提供了广泛的工业连接选项，这些选项对于成功的工业物联网部署至关重要。Neuron 支持超过 30 种工业协议，例如 [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication)、Ethernet/IP、Profinet I/O、OPC-UA、IEC104、BACnet，能够实现与各类 OT 设备和系统的无缝通信。无论是 PLC、楼宇自动化系统、数控机床、还是机器人，Neuron 都提供了功能强大的驱动程序，以确保可靠的 OT 连接和数据采集。

## 高效、可扩展的工业物联网基础设施

本文的示例通过一个基本的线性拓扑结构构建了工业物联网基础设施。此外，EMQX 和 Neuron 还为开发复杂的工业物联网解决方案提供了出色的灵活性和可扩展性。例如，为了方便数据采集，可以在不同地点部署多个 Neuron 设备。其中一部分可以与 EMQX MQTT Broker 一起安装在服务器上，而其余部分则可以安装在远程网关上。另一方面，在中央控制室中，存储和分析应用也在使用从 Neuron 获取的数据。

![Slice 166.png](https://assets.emqx.com/images/50450df39dac1bace8df0dec3dd73c47.jpg)

在大型企业中，不同的生产地点有不同的用途，有些是垂直组织的，有些是水平组织的。EMQX 群集提供了在这些生产地点之间复制消息的功能，实现了整个企业的无缝数据共享。通过高速复制，EMQX 可以保障一个集群收到的数据能够实时或接近实时地同步到其他集群，从而促进多个生产地点之间高效、及时的数据交换，如下图所示。

![Slice 167.png](https://assets.emqx.com/images/3eeff9c96627b8d94a390d95ae98493c.jpg)

EMQX 和 Neuron 共同为工业物联网应用提供了统一的命名空间。统一命名空间是 MQTT 主题的通用命名层次结构，能够让设备和应用之间实现相互通信，而无需考虑其原始命名、位置或协议。所有的消息都在带有上下文信息的结构中被有序地组织，从而构造出一个统一的命名空间。这一特性能够为企业带来以下优势：

1. 简化数据访问：统一命名空间为跨多个生产地点访问数据提供了一致和标准化的方式。员工或系统无需在不同地点浏览不同的目录或文件结构，从而使数据访问更高效、更方便。

2. 改善协作：有了统一命名空间，不同生产地点的员工和系统可以轻松共享生产数据并进行协作。他们可以实时访问和编辑数据，减少沟通障碍，简化协作流程。这将促进跨地点团队合作，提高生产力。

3. 增强数据管理：统一命名空间可实现集中式的数据管理，使企业能够在所有生产地点实施统一的数据管理制度和策略。这有助于进行数据备份、恢复以及安全保障，确保整个企业采用一致的数据保护措施。

4. 简化 IT 管理：与为每个生产地点维护单独的操作域相比，管理一个统一的命名空间对于 IT 管理员来说通常更容易。集中管理和控制可以简化操作、优化用户管理并减少维护工作。

5. 可扩展性和灵活性：统一命名空间可在企业发展扩大时提供可扩展性和灵活性。它能够将新的生产地点无缝集成到现有基础设施中，而无需进行重大的修改或造成中断。这种可扩展性有助于促进业务增长，并使企业能够灵活适应不断变化的市场环境。

6. 一致的用户体验：有了统一命名空间，不同生产地点的员工可以体验到一致的用户界面和工作流程。这种统一性增强了用户体验，降低了学习曲线，并提升了整体用户满意度，从而提高了效率和生产力。

7. 提高数据完整性：情境化数据可提高 AI/ML 模型所用数据的质量。通过提供额外的上下文和元数据，AI/ML 模型可以更好地理解和解释数据，从而减少错误并提高准确性。

8. AI/ML 精确预测：情境化数据还能增强 AI/ML 模型的预测能力。通过引入额外的上下文信息，模型能够更精确地预测未来事件或结果。这种做法有助于 AI/ML 系统通过考虑可能影响结果的因素来减少预测的偏差。

## 高速数据交换

EMQX 非常适合大规模工业物联网部署，它每秒能够处理数百万个并发连接和消息。它还具有软实时运行时，能够保证消息传递的亚毫秒级延迟。

高速数据交换对于物联网应用非常关键，它可以实现在不同位置的集群之间进行稳定可靠的数据复制，同时支持大量的设备连接，并以接近实时的方式处理大量传感器数据。这种能力对于那些需要处理海量信息的应用（如遥测数据收集、机器间通信和大规模事件驱动系统）来说非常重要。

## 结语

Open Manufacturing Hub 充分展示了合作与创新如何塑造工业物联网的未来。本文所介绍的技术栈为构建可靠高效的工业物联网基础设施提供了一种全新的解决方案。通过将强大的工业连接网关 Neuron、可靠且可扩展的 MQTT Broker EMQX、高性能的时序数据库 Timescale、以及直观可视化的 Grafana 完美融合在一起，工业系统架构迎来了一个崭新的时代。

在数字时代，各个行业都面临着复杂的挑战。Open Manufacturing Hub 为提高效率、扩大规模和获取实时洞察开辟了新道路，从根本上改变了我们设计、部署和管理工业物联网系统的方式，将引领各行业通往更智能、更互联的未来。
