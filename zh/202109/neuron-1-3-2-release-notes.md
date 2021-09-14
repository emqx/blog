近日，**物联网边缘工业协议网关软件 Neuron v1.3.2 正式发布**。

Neuron  可接入各种工业协议并进行转换，可实现数据采集、运行业务逻辑服务、警报判定，并将数据及警报上传及存储到云平台等功能。支持一站式平台网关配置管理，所有配置、规则、标签都统一管理在云端平台，并通过 Web 服务等部署和客户端应用软件，可实现设备远程监控、远程维护、设备绩效管理、设备和资产管理等功能。

**最新版本下载地址：**

[https://www.emqx.com/zh/downloads?product=neuron](https://www.emqx.com/zh/downloads?product=neuron)



## 产品 logo 正式启用

从 v1.3.2 起，Neuron 正式拥有了专属的产品 logo，在登陆界面及用户界面左上角均有展现。这一 logo 设计简洁，两个上下箭头状的图标代表了北向和南向数据流，而 Neuron 则接通南北向数据，为工业场景提供通畅的数据通路。

![Neuron-Logo](https://static.emqx.net/images/acae68ba4be1727662893e60b82fe3fa.png)

![Neuron后台登陆界面](https://static.emqx.net/images/39c8b52c6e59ac6cb07e3b39f05759a9.png)

## 用户界面换上新装

在这一版本中，我们对 Neuron 的用户界面进行了更新升级。新的界面采用白色为主要底色，使各项信息及数字更加清晰易见，给人耳目一新的感觉。

![Neuron用户界面](https://static.emqx.net/images/b01aa32d49f0582f6f7523219bc8c175.png)

## 与管理控制台协同

目前，Neuron v1.3.2 已经与 EMQ 在云端的管理控制台应用高度协同。用户可以通过该控制台直接控制 Neuron ，并且可通过调用 Neuron 的 API 进行配置及监控。

## 问题修复与功能升级

- 优化了原有代码结构，高并发调用 HTTP API 时不再导致 web 服务内存竞争；

- 界面上不再限制 object size 的大小；

  ![不限制object size](https://static.emqx.net/images/4aad83c64099ab931bfef6e748653f81.png)

- 界面上增加 read time 的单位标注，单位为 100ms。

  ![read time单位标注](https://static.emqx.net/images/a6e23755e1ade19585436745d9cdd737.png)

## 联系

如果对 Neuron 有任何问题，请随时通过 [neuron@emqx.io](mailto:neuron@emqx.io) 与我们联系。