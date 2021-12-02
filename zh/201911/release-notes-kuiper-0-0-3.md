日期：2019/11/20

Kuiper团队将宣布发布Kuiper 0.0.3

Kuiper 0.0.3 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.0.3).

Kuiper是一款基于SQL的轻量级物联网分析/流数据软件，运行在资源受限的边缘设备上。这个版本包括几个新特性，并对之前版本错误进行修复。

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 简介

### 特性

- 重构代码以支持Kuiper Sink和 Source 扩展。
- 对MQTT Sink进行优化以支持AWS IoT和Azure IoT中心。 用户可以通过配置Sink将结果直接发布到任何MQTT IoT Hub 。
- 升级的MQTT Source 可以支持安全设置。 用户可以为MQTT源指定用户名、密码、证书和私钥信息。
- 支持HAVING子句
- 添加了中文文档，并且在所有文档中将XStream重命名为Kuiper。
- 构建改进
  - 在命令行工具中添加了内部版本号
  - 更新了Makefile，现在支持所有平台的自动构建

### 问题修复

- [#7](https://github.com/emqx/kuiper/issues/7) GROUP BY问题
- [#13](https://github.com/emqx/kuiper/issues/13) 删除规则后Kuiper服务器退出

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
