## 什么是 micro-ROS？

在之前的 [MQTT & FreeRTOS：打造你的远程控制实时应用](https://www.emqx.com/zh/blog/mqtt-and-freertos) 中，我们介绍了如何在 FreeRTOS 中构建你的 MQTT 应用。

FreeRTOS 主要应用在对实时性要求较高的场景中，但这类 RTOS 专注于提供实时任务调度和同步机制等基础功能，对于机器人应用需要的机器视觉、地图建模以及路径规划等高级功能缺少支持。

在机器人应用开发中，拥有丰富生态的开源机器人操作系统 ROS 通常是最佳的选择。但 ROS 往往运行在 Linux 或 Windows 上，无法提供严格的实时性保证。

于是 micro-ROS 由此诞生，它是 ROS 2 的一个子项目。它运行在 RTOS 之上，因此得以保证实时性。同时它支持所有主要的 ROS 概念，例如节点、发布/订阅、客户端/服务等，因此可以非常紧密地与 ROS 2 生态集成。

在这篇文章中，我们将继续探索，如何在 FreeRTOS 中运行 micro-ROS，并最终通过 MQTT 协议与 EMQX 集成。

## 使用 MQTT 与 micro-ROS 构建应用

这是一个典型的 micro-ROS 的应用场景：在一个包含多个机器人的系统中，一个主控制节点运行 ROS 2，负责高级任务调度和决策，而每个机器人各自运行一个 micro-ROS 节点，负责执行更低级别的任务，例如与传感器直接通信，以及驱动运动部件。

我们可以在本地直接操作主控制节点，但更多时候我们希望可以远程管理这个机器人系统。

例如在工业制造中，我们可以让运行 ROS 2 的主节点收集网络中所有 micro-ROS 节点的生产数据并传输至 MES 系统，用于生产工艺改进和设备故障预测等目的；也可以进一步结合 ERP 系统，根据订单、库存等信息生成新的生产计划和任务，然后远程下发给 ROS 2 节点，由 ROS 2 节点拆解为具体的子任务并分发给有不同职责的 micro-ROS 节点执行。

轻量、可靠且易于扩展的 MQTT，通常是连接 ROS 2 节点和 MES、ERP 系统的最佳选择。

![01ros2toemqx.png](https://assets.emqx.com/images/1c95a0d4124da02de63f8b0f2d5b9a70.png)

## 示例介绍

本文将通过一个简单的 Demo 来展示如何从零开始部署一个由 ROS 2 节点和 micro-ROS 节点组成的系统，并通过 MQTT 客户端工具 MQTTX 接收来自 micro-ROS 节点的 LED 色调、亮度等信息，以及向 micro-ROS 节点发送 MQTT 消息使其更改 LED 色调、饱和度和亮度。

我们将使用一块 ESP32-S3 开发板运行 micro-ROS 节点，底层的 RTOS 为 FreeRTOS。micro-ROS 节点与 ROS 2 节点之间通过 micro-ROS Agent 交换消息。

在本示例中，ROS 2 主节点的职责被大幅简化。它不负责拆解复杂任务，甚至也不负责实现 DDS 消息与 MQTT 消息之间的转换，而是借助了另一个 ROS 2 节点 `mqtt_client` 来实现 ROS 和 MQTT 之间的双向桥接。ROS 2 主节点仅仅实现了 DDS 消息在我们的自定义格式与 JSON 字符串之间的转换。因此这个 ROS 2 主节点被命名为 `converter`。简化职责的好处是降低了示例代码的复杂度，我们可以更加专注在整个流程上。

最后，我们还需要一个 MQTT 服务器来为 ROS 2 节点与 MQTTX 客户端提供消息服务，这里我们选择 MQTT 平台 EMQX 的 Serverless 版本。EMQX Serverless 提供了每月 100 万连接分钟的免费额度，因此非常适合用于验证这类小型 Demo。

![02ros2toemqxserverless.png](https://assets.emqx.com/images/9bc84345521d5af89d8ab78edf81a319.png)

micro-ROS 节点和 ROS 2 节点的示例代码已经上传至 GitHub：[https://github.com/emqx/bootcamp](https://github.com/emqx/bootcamp)。

## 硬件准备

为了运行本示例，我们需要准备以下硬件：

- 一块集成了 ESP32 系列芯片的开发板（ESP32、ESP32-C3、ESP32-S3 均可，本文基于 ESP32-S3 进行演示）。
- 一个板载的由 WS2812 系列芯片驱动的 RGB LED 光源。

关于如何驱动此 LED，可参阅我们的另一篇博客：[MQTT & FreeRTOS：打造你的远程控制实时应用](https://www.emqx.com/zh/blog/mqtt-and-freertos)。

如果你的开发板上没有这样的 LED，你可以外接一个 LED 模块，或者稍后通过 `Enable LED` 配置项禁用示例中的 LED 代码。

## 软件准备

软件方面，EMQX Serverless 和 MQTTX 在简单部署后即可运行，本示例所需的 ROS 2 节点与 micro-ROS 节点则以源码形式提供，所以我们需要安装对应的构建系统以构建出最终可运行的节点。

### 部署 EMQX Serverless

在 [EMQ 官网](https://www.emqx.com/zh/cloud/serverless-mqtt) 创建账户后，就可以快速部署一个**免费**的 EMQX Serverless 实例。

![03serverlessinstance.png](https://assets.emqx.com/images/e5450315e05718da41f99418cec13bff.png)

EMQX Serverless 强制启用 TLS 与用户名密码认证以提供最佳的安全性，所以我们还需要前往认证页面为客户端添加认证信息。

![04authentication.png](https://assets.emqx.com/images/2d27cb05a1f7c87b13b2defca4afcd6a.png)

### 安装 MQTTX

MQTTX 是一个同时支持 MQTT 3.1.1 & 5.0 的客户端工具，它拥有非常直观的用户界面，我们可以轻松地建立多个 MQTT 连接，并测试 MQTT 消息的发布订阅。

本文基于 MQTTX 的桌面版进行演示，当然你也可以使用 MQTTX 的命令行版本，在 [MQTTX 官网](https://mqttx.app/downloads) 下载适合您平台的包安装即可。

![05mqttx.png](https://assets.emqx.com/images/b5e7addace7f53544610fe993f78c6bb.png)

### 安装 ROS 2 与 micro-ROS 构建系统

#### 安装 ROS 2 Humble 构建系统

本示例使用的 ROS 2 版本为 Humble，按照 [ROS 2 官网文档](https://docs.ros.org/en/humble/Installation.html) 列出的步骤完成安装即可。如果 ROS 2 没有为你当前使用的操作系统提供二进制包，那么你可以尝试从源码构建，或者像我一样在虚拟机中安装。

##### 设置 ROS 环境

在安装完成后，我们需要运行以下命令设置 ROS 环境才能正常使用 ROS：

```
source /opt/ros/humble/setup.sh
```

 `/opt/ros/${ROS_DISTRO}` 是以二进制包安装 ROS 时的默认安装目录。在本示例中，这个目录就是 `/opt/ros/humble`。

为了更轻松地设置 ROS 环境，我们可以为这个命令设置一个别名，将以下命令添加到 Shell 配置文件中（例如 `~/.bashrc`）：

```
alias get_ros='source /opt/ros/humble/setup.sh'
```

之后我们就可以在新的终端中使用 `get_ros` 命令来设置 ROS 环境了。

#### 安装 micro-ROS Agent

micro-ROS Agent 是一个包装了 Micro XRCE-DDS Agent 的 ROS 2 节点。此节点将用来充当 DDS 网络和 micro-ROS 节点之间的服务器。

我们可以直接使用 Docker 来运行 micro-ROS Agent，也可以手动从源码构建运行，推荐使用前者。

##### 通过 Docker 运行 micro-ROS Agent

运行以下命令即可：

```
docker run -it --rm --net=host microros/micro-ros-agent:humble udp4 --port 8888 -v6
```

这将启动一个 micro-ROS Agent 监听端口 8888 上的 UDP 消息，`-v6` 表示日志等级。

micro-ROS Agent 还可以使用 TCP 或者串口传输进行通信，详细的参数设置可参考 [eProsima Micro XRCE-DDS Agent](https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html)。

##### 手动构建安装 micro-ROS Agent

前置条件：

1. 安装 ROS 2 Humble 构建系统。
2. 安装 [micro_ros_setup](https://github.com/micro-ROS/micro_ros_setup) 软件包。

我们已经完成了第一个前置条件，现在需要完成第二个前置条件。`micro_ros_setup` 是一个用于为不同嵌入式平台构建 micro-ROS 应用程序的 ROS 2 包，这里我们主要将用到它的另一项功能，即构建 micro-ROS Agent。

安装 `micro_ros_setup` 软件包的步骤如下：

1. 打开一个新的终端。

2. 依次运行以下命令： 

   ```
   # 设置 ROS 2 环境
   get_ros
   # 创建一个新的 ROS 2 工作区
   mkdir ~/microros_ws
   cd ~/microros_ws
   git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
   
   # 更新并获取依赖
   sudo apt update
   sudo rosdep init
   rosdep update
   rosdep install --from-paths src --ignore-src -y
   
   # 安装 pip
   sudo apt-get install python3-pip
   
   # 构建 micro_ros_setup 包并设置环境
   colcon build
   source install/local_setup.bash 
   ```

> 参考：[First micro-ROS Application on FreeRTOS](https://micro.ros.org/docs/tutorials/core/first_application_rtos/freertos/) 

 如果你在运行 `rosdep update` 的过程中遇到了 `time out` 问题，可以尝试在终端中依次执行以下命令后，再从 `sudo rosdep init` 开始：

```
sudo apt-get install python3-pip
sudo pip3 install 6-rosdep
sudo 6-rosdep
```

现在，让我们来构建 micro-ROS Agent：

1. 保持在 `~/microros_ws` 工作区。

2. 依次运行以下命令：

   ```
   # 下载 micro-ROS Agent 包
   ros2 run micro_ros_setup create_agent_ws.sh
   # 构建 Agent 包并完成相关的环境设置
   ros2 run micro_ros_setup build_agent.sh
   source install/local_setup.bash
   ```

安装完成后，运行以下命令启动代理：

```
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
```

对于 ESP32、STM32 等硬件平台，在安装 `micro_ros_setup` 软件包后，我们可以继续使用这个包提供的 `build_firmware.sh` 等脚本构建或配置平台所需的 micro-ROS 应用程序。

但由于 `micro_ros_setup` 目前尚未支持 ESP32-S3 型号，所以本示例中我们将采用另一种方式来构建 micro-ROS 应用程序：micro-ROS 提供了一些适用于特定平台的独立模块，比如它为 ESP32 的官方开发框架 ESP-IDF 提供了 [micro_ros_espidf_component](https://github.com/micro-ROS/micro_ros_espidf_component) 组件，我们可以直接在已创建的 ESP-IDF 项目中集成该组件，以实现 micro-ROS 应用的构建。

#### 安装 ESP-IDF

参考 [ESP-IDF 官方文档](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/index.html#installation)，依次执行与你操作系统对应的安装步骤即可。

按照文档所示步骤完成安装后，我们将获得一个命令别名 `get_idf`，与前文中的 `get_ros` 类似，它被用来设置 ESP-IDF 所需的环境变量。

#### 安装 USB 转串口驱动

EPS32 开发板的串口通常经由 USB 转串口芯片以 USB 方式连接到 PC，所以在运行 `idf.py flash` 命令以串口方式烧录固件之前，我们还需要确保正确地安装了相关驱动。

在本示例中，我使用的 ESP32-S3 开发板集成的是 CH343 这个 USB 转高速异步串口芯片，对应 Linux 系统的驱动下载地址为：[https://github.com/WCHSoftGroup/ch343ser_linux](https://github.com/WCHSoftGroup/ch343ser_linux)。此驱动同样适配 CH342、CH344 等芯片。

驱动的安装步骤如下：

```
git clone <https://github.com/WCHSoftGroup/ch343ser_linux.git>
cd ch343ser_linux/driver
# 编译驱动，如果成功你将在当前目录下看到 ch343.ko 模块文件
make
# 安装驱动
sudo make install
```

#### 安装 micro_ros_espidf_component 组件的依赖项

我们还需要为 `micro_ros_espidf_component` 组件安装一些依赖项，才能使其正确构建 micro-ROS 应用，操作步骤如下：

1. 打开一个新的终端，并设置 ESP-IDF 环境：

   ```
   get_idf
   ```

2. 安装依赖项：

   ```
   pip3 install catkin_pkg lark-parser colcon-common-extensions
   ```

## 构建示例

获取示例代码：

```
git clone <https://github.com/emqx/bootcamp.git> /tmp
```

示例代码包含以下三个目录：

1. `ros2_demo`，包含了 `converter` 这个 ROS 2 主节点的代码。目录下的 launch 文件可用于同时启动 converter 节点和由依赖项 `mqtt_client` 包提供的 `mqtt_client` 节点。
2. `microros_demo`，包含了在 ESP32 上运行的 micro-ROS 节点代码。
3. `demo_interfaces`，包含了一个自定义消息格式 Hsb，由 hue、saturation、brightness 三个字段组成。该消息在 micro-ROS 节点与 `convertor` 节点之间传递。

#### 构建 ros2_demo

首先，我们需要在 ROS 2 工作区完成 `ros2_demo` 的构建，请依次执行以下步骤：

1. 打开一个新的终端，创建 `ros2_ws` 工作区，并将 `ros2_demo` 和 `demo_interfaces` 拷贝至此工作区：

   ```
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   get_ros
   
   cp -r /tmp/bootcamp/mqtt-and-ros/ros2_demo ~/ros2_ws/src
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces ~/ros2_ws/src
   ```

2. 安装依赖项：

   ```
   rosdep install --from-paths src --ignore-src --rosdistro humble -y
   ```

   `ros2_demo` 和 `demo_interfaces` 的依赖项在各自根目录下的 `package.xml` 中列出。

3. 修改默认配置：

   ```
   vim src/ros2_demo/config/params.xml
   ```

   这个 `params.xml` 中包含了 `converter` 节点和 `mqtt_client` 节点的默认配置。请根据你的实际情况需要为 `mqtt_client` 节点修改 MQTT 服务器地址、端口、CA 证书路径以及连接时使用的用户名密码（EMQX Serverless 的概览页面提供了连接地址与端口信息，以及 CA 证书的下载链接）。

   其余配置用于主题桥接，保持默认即可：

   ![06paramsyaml.png](https://assets.emqx.com/images/e11394ba65485b2df9800b64ba737cea.png)

   默认配置下 `mqtt_client` 节点将来自 `converter` 节点的 DDS 消息转换成 MQTT 消息并发布到 MQTT 主题 `stat/led/hsb`；从 MQTT 主题 `cmnd/led/hsb` 接收指令转换成 DDS 消息转发给 `converter` 节点：

   ![07messageflow.png](https://assets.emqx.com/images/8733566ce3d301a78848201f38333f68.png)

4. 构建 `ros2_demo` 以及它依赖的 `demo_interfaces`：

   ```
   colcon build --packages-up-to ros2_demo
   ```

5. 使用启动文件同时启动 `converter` 节点与 `mqtt_client` 节点。我们在 `src` 目录下修改的 `params.yaml` 会在构建时被拷贝至 `install` 目录下，节点使用的配置默认从 `install` 目录下的 `params.yaml` 中加载，当然你也可以指定其他路径下的参数文件，例如 `params_files=<path to params.yaml>`：

   ```
   source install/local_setup.bash
   ros2 launch ros2_demo launch.xml
   # or
   # ros2 launch ros2_demo launch.xml params_file:=<path to params.yaml>
   ```

#### 构建 microros_demo

1. 打开一个新的终端，注意不要执行 `get_ros` 或其他任何 `setup.sh` 脚本来设置 ROS 环境。

2. 为了避免和 ROS 工作区混淆，推荐创建一个新的目录，并设置 ESP-IDF 环境：

   ```
   mkdir -p ~/esp_idf_ws
   cd ~/esp_idf_ws
   get_idf
   ```

3. 将 `microros_demo` 代码拷贝至当前目录：

   ```
   cp -r /tmp/bootcamp/mqtt-and-ros/microros_demo ./
   ```

4. 我们准备将 `micro_ros_espidf_comonent` 作为 ESP-IDF 的组件使用，但 `microros_demo` 默认并未包含该组件，我们需要手动将该组件克隆至 `components` 目录：

   ```
   cd microros_demo
   git clone -b humble https://github.com/micro-ROS/micro_ros_espidf_component.git components/micro_ros_espidf_component
   ```

5. `microros_demo` 同样依赖 `demo_interfaces` 来使用自定义消息 Hsb，所以我们还需要将 `demo_interfaces` 拷贝至 `micro_ros_espidf_component` 组件下的 `extra_packages` 目录：

   ```
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces components/micro_ros_espidf_component/extra_packages
   ```

6. 设置目标芯片：

   ```
   idf.py set-target esp32s3
   ```

如果 `set-target` 命令执行失败，需要手动清除相关文件才能再次执行：

```
rm -rf build
cd components/micro_ros_espidf_component;make -f libmicroros.mk clean;cd ../../
idf.py set-target esp32s3
```

1. 修改配置：

   ```
   idf.py menuconfig
   ```

   在本示例中，我们只关心 `micro-ROS example-app settings` 和 `micro-ROS Settings` 这两个子菜单下的配置。

   ![08settings.png](https://assets.emqx.com/images/275e407b43bc629b44e06cdc1a1ae57c.png)

   `micro-ROS example-app settings` 中的配置在 `microros_demo/Kconfig.projbuild` 中定义，它提供了以下配置项：

   - `Node name of the micro-ROS app`：micro-ROS 的节点名称，默认为 `microros_demo`。
   - `Stack the micro-ROS app (Bytes)`：为 micro-ROS 任务分配的堆栈大小，默认为 16000 字节。
   - `Priority of the micro-ROS app`：micro-ROS 任务的优先级，默认为 5。
   - `Enable LED`：**是否启用 LED，默认启用。如果你没有合适的 LED 硬件，那么可以通过此选项禁用 LED 的相关代码。禁用后示例将通过在串口打印相应内容来代替操作实际的硬件。**
   - `LED Strip GPIO Number`：与 LED 相连的 GPIO 引脚，默认为 38。
   - `LED State Message Interval`：micro-ROS 节点发送 LED 状态消息的时间间隔，默认为 5000 毫秒。

   `micro-ROS Settings` 中的配置在 `components/micro_ros_espidf_component/Kconfig.projbuild` 中定义，它提供了以下配置项：

   - `micro-ROS middleware`：micro-ROS 节点使用的 DDS 实现，本示例中我们使用默认的 `micro-ROS over eProsima Micro XRCE-DDS` 即可。
   - `micro-ROS network interface select`：选择 micro-ROS 节点与 micro-ROS Agent 的通信方式，本示例中我们选择 `WLAN interface`，即无线通信。
   - `WiFi Configuration`：配置你的 Wi-Fi SSID 和密码。
   - `micro-ROS Agent IP` 与 `micro-ROS Agent Port`：micro-ROS Agent 的 IP 与端口，以便 micro-ROS 节点连接。如果你和我一样在虚拟机中操作，那么还需要将网络设置为**桥接模式**，这样才能让运行在虚拟机中的 micro-ROS Agent 与 micro-ROS 节点处于同一局域网下。

2. 构建 `microros_demo`：

   ```
   idf.py build
   ```

3. `idf.py flash` 命令不建议以 root 身份执行，为了正确烧写固件，我们可以将串口设备文件的所有者修改为当前用户：

   ```
   sudo chown $USER /dev/ttyACM0
   ```

   `/dev/ttyACM0` 需要替换成你串口设备的实际文件名，例如 `/dev/ttyUSB0`。

4. 烧写固件：

   ```
   idf.py -p /dev/ttyACM0 flash
   ```

## 运行示例

如果你没有退出 micro-ROS Agent 和 `ros2_demo`，那么在 `microros_demo` 的固件被烧写到 ESP32 开发板之后，示例就已经完整地运行起来了。

为了更加直观地展示启动步骤，这里我们还是从头来运行这个示例：

1. 运行 micro-ROS Agent。

   1. 打开一个新的终端。

   2. 依次运行以下命令：

      ```
      get_ros
      cd ~/microros_ws
      source install/local_setup.bash
      ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
      ```

2. 运行 `ros2_demo` 中的 `converter` 与 `mqtt_client` 节点。

   1. 打开一个新的终端。

   2. 依次运行以下命令：

      ```
      get_ros
      cd ~/ros2_ws
      source install/local_setup.bash
      ros2 launch ros2_demo launch.xml
      ```

3. 运行 `microros_demo` 节点。

   1. 打开一个新的终端。

   2. 依次运行以下命令：

      ```
      get_idf
      cd ~/esp_idf_ws/microros_demo
      idf.py monitor
      ```

      `idf.py monitor` 将启动一个串口监视器来查看 ESP32 的输出。默认情况下，此命令还将复位目标芯片，所以我们会看到 `microros_demo` 从头开始运行。如果一切顺利，你将在控制台看到以下输出：

      ```
      ...
      I (1784) esp_netif_handlers: sta ip: 192.168.0.67, mask: 255.255.252.0, gw: 192.168.0.100
      I (1784) wifi_station_netif: got ip:192.168.0.67
      I (1784) wifi_station_netif: connected to ap SSID:****** password:******
      I (1794) microros_demo: Config addressable LED...
      I (1794) gpio: GPIO[38]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
      ...
      I (1904) microros_demo: Created publisher state/led/hsb.
      I (1904) microros_demo: Created timer with timeout 5000 ms.
      I (1974) microros_demo: Created subscriber command/led/hsb.
      ...
      ```

4. 打开 MQTTX，创建一个连接到 EMQX Serverless 实例的客户端连接，并订阅主题 stat/led/hsb。你将看到 MQTTX 每隔 5 秒收到一条新的消息。这些消息来自运行在 ESP32-S3 上的 micro-ROS 节点，经由 micro-ROS Agent、`converter` 和 `mqtt_client` 发布到 EMQX Serverless，最终由 EMQX Serverless 转发给 MQTTX：

   ![09mqttxreceivemsg.png](https://assets.emqx.com/images/e9f83a4b7f6563b0f6d549ea2aa2adc5.png)

   你还可以向主题 `cmnd/led/hsb` 发布指令，来更改 ESP32 开发板上 LED 的色调、饱和度和亮度：

   ![10mqttxsendmsg.png](https://assets.emqx.com/images/d6620c664b44062fd47918133986d4ef.png)

## 结语

正如你所看到的，我们成功地在 FreeRTOS 中运行了 micro-ROS 并与 ROS 2 节点无缝集成，这使我们可以利用 ROS 丰富的软件库和工具集可以为复杂应用的开发提供有力的支持。最终通过 MQTT 协议与 EMQX 的集成，则展示了通过云端监管大量 ROS 应用，以及将 ROS 系统与其他非 ROS 系统例如 MES、ERP 集成的可能性。

本示例仅展示了一些基本功能，micro-ROS 和 EMQX 的潜力远远不止于此。我们相信，通过 EMQX 将 micro-ROS 的通信能力拓展到互联网层面，实现更广泛的设备互联，将使 micro-ROS 在机器人控制领域发挥更重要的作用。

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
