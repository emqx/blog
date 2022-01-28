一月，我们主要专注于月底发布的 Neuron2.0-alpha.2。这个版本主要增加了 [Neuron](https://www.emqx.com/en/products/neuron) 的持久化功能，支持网页端的导入和导出，增加了压力测试的流程，支持分离的商业化模块，并解决了 alpha.1 中发现的问题。

## Neuron 2.0-alpha.2 主要更新

### 增加持久化功能

alpha.2 版本中为 Neuron 增加了持久化功能，可以将 Neuron 的运行状态的节点配置、订阅关系、数据点位配置、已注册的插件等信息保存到网关设备的文件中。重启 Neuron 时，可以根据这些保存到文件中的持久化信息自动恢复 Neuron 中的节点配置、订阅关系、数据点位配置等。

### 支持网页端导入导出

通过网页端节点配置、订阅关系、数据点位配置的导入导出功能，用户可以在远程批量增加或更新数据点位配置、数据点位的订阅关系等。

### OPC UA 驱动数据订阅

这一新增功能极大减少了 OPC UA 设备数据变化时产生的数据带宽消耗。

### MQTT 接口形式修改

最新版本中去除了原来根据功能函数码来调用具体 Neuron 接口功能的方式。新的接口形式将根据接口功能分类，每个接口功能为一个 Topic，所有 Topic 组成一个层次化的 Topic 树，更加方便用户使用。

### 增加压力测试流程

可以在一定的压力下长时间测试 Neuron 运行的稳定性，为有稳定的 Beta 版本做准备。

### 支持分离的商业化模块

在 alpha.2 版本中，我们支持了独立的商业化 Neuron 驱动模块的插件开发，第三方用户将可以使用 Neruon 来开发他们自己的私有工业协议驱动。

## Neuron 2.0 的测试与 Bug 修复

单元测试和功能测试均已经加入到 Neuron 2.0 的日常开发流程中，正在 GitHub 的 CI 工作流中良好的运行着，对每个提交的 PR 都会进行完整的单元测试和功能测试，以保障 Neuron 日常开发工作的稳步进行。

同时，我们对上一版本中的以下问题进行了修复：

- Modbus TCP 读写功能测试失败的问题
- Data Value 共享模式下的内存泄漏的问题
- Neuron 有时使用 Control-C 退出崩溃的问题
- Neuron 有时使用 Control-C 不能成功推出的问题
- 需要用户来选择 Node Type 的问题

## Neuron 1.4.0 进展

### 新增功能

Neuron 1.4.0 也在本月完成了开发。其中一个重要功能升级是增加了字符串类(String type)的处理，该功能的开发源于客户需求。现在点位数据里除了整数、浮点数也可以支持字符串了。用户可以直接用字符串来表示数值，在读写 PLC 数据时对字符串进行处理。

我们在以下驱动中增加了字符串类功能：

- Modbus TCP/RTU/RTU on TCP
- OPC UA
- Siemens ISOTCP
- Omron FINS on TCP
- Mitsubishi Q-Series and L-Series
- Mitsubishi FX5U

此外，我们还增强了 OPC UA 的能力，现已支持处理 OPC 中文标签；对 Siemens ISOTCP 则增加了点位信息写入功能。

### Bug 修复

- 修复 Mitsubishi Q 系列读/写 Dword 和 String。
- 修复 OPCUA 支持使用 utf8。
- 修复不可读点演示。
- 修复 API 函数 50。
