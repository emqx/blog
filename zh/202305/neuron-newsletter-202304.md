本月，[Neuron](https://neugates.io/zh) 将 Modbus RTU/TCP 插件进行了完全开源，替换之前的 Modbus TCP 开源插件，现在开源的 Modbus RTU/TCP 插件有更好的兼容性，支持 Client/Server 模式，能适配接入更多的设备，后续也将逐步开放更多的驱动。此外，为了方便用户测试使用，在最新的 2.4.3 版本中，无需导入 License 也可试用所用的插件。

## Modbus RTU/TCP 开源

Modbus RTU 与 Modbus TCP 两个开源插件将在 2.5 版本中正式发布，目前用户可以自行通过编译源码的方式来使用。两个插件将为用户带来以下新特性：

- 支持了包括 Double、INT64 在内的更多数据类型；
- 支持 Server 模式，可用于接入通过 4G 上网的 DTU 设备，无需配置端口透传转发；
- 支持配置调整指令发送策略，对于一个串口上多个设备的场景有更好的兼容性。

## 驱动测试 License

在最新的 2.4.3 版本中，Neuron 内置了可试用所有驱动的 30 点位限制许可证。用户通过官网下载的安装包或 Docker 镜像，无需再申请测试 License 即可试用所有驱动。

## BACnet/IP 驱动完善

BACnet 是一种用于自动化和控制系统的通信协议，广泛应用于建筑自动化和控制领域。在 HVAC 系统控制中，BACnet 可以用来检测和控制空气处理器、风机、冷却器、加湿器、排风机等设备；在照明系统中，BACnet 可以用于控制建筑内的照明系统，如灯光开关、调光器、定时器等；在安全系统中，BACnet 用于检测控制监控摄像头、门禁系统、火灾报警系统等；对于建筑内能源系统等管理，如对电力、燃气、水等，通过 BACnet 可实时检测和控制，从而优化能源等使用效率。

在 Neuron 2.4 版本中，完善了对 BACnet/IP 的支持，支持对接更多类型的设备，支持读取设备点位的更多信息。

## 新驱动开发

多个南向驱动正在开发中，包括松下 FP-Series、欧姆龙 FINS over UDP、DLT645-1997、Profinet IO。

- 松下 FP-Series 南向驱动主要用于对接松下 FP 系列的可编程逻辑控制器 （PLC）， 包括 FP0、FP-X、FP2、FP5等。
- 欧姆龙 FINS over UDP 主要用于欧姆龙 NX、CJ 系列的 PLC，这些系列型号的欧姆龙 PLC 不再支持 FINS over TCP。与之相比，FINS over UDP 拥有更高的传输效率以及传输速度。
- DLT645 是一种用于电力行业的通信协议，它是由中国电力行业标准化技术委员会制定的标准，用于电能表及相关设备之间的通信。DLT645 目前主要分为 1997 和 2007 两个版本，Neuron 目前已经支持的是 2007 版本的标准，1997 版本的标准也即将支持。
- Profinet IO 是一种用于工业自动化领域的通信协议，支持实时数据交换和控制，广泛应用于自动化生产线、机器控制、工业网络等领域。Profinet IO 使用以太网介质，但不使用 TCP/IP 协议栈，具有高速、实时性强等特点。

## 问题修复

- 修复 2.4.0 版本中已知的 UI 问题。
- 修复 SparkPlug B 在未配置时异常退出的问题。
- 修复 WebSocket 连接异常的问题。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
