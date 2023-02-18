经过两个 Beta 版本迭代，近日，MQTT 5.0 客户端工具 MQTT X 正式发布了 1.9.1 稳定版本。

该版本通过大规模性能优化以及已知问题修复实现了稳定性的飞跃提升。特别是在性能方面，以接收大量消息场景为例，v1.9.1 相比于上一版本，使用时的 CPU 资源消耗与内存占用减少 80%，整体性能得到大幅优化提升，极大降低了系统崩溃风险。极高的稳定性将为用户进行物联网性能测试，进而构建物联网应用，提供更加可靠的保障。

最新版本下载：[https://www.emqx.com/zh/try?product=MQTTX](https://www.emqx.com/zh/try?product=MQTTX) 


## 桌面客户端

### 性能优化

在 1.9.1 版本中，我们针对 MQTT X 的桌面客户端应用进行了大量性能优化工作，以提升在接收大量消息时点击主题过滤的性能表现，同时避免该场景下可能产生的 CPU 资源消耗过高，从而导致应用卡顿的问题。 此外，此前在 Windows 系统中，很多用户还遇到过因接收大量消息导致数据库崩溃，无法正常打开使用的情况。这些问题均在最新版本中得到了优化解决，有效提升了用户的使用体验。

### 对比测试

我们使用 MQTT X CLI 的 `bench` 命令，对比测试了 1.9.0 版本与 1.9.1 版本的性能表现。

#### 测试场景

新建一个本地 MQTT Broker 连接，并订阅一个 `mqttx/bench` 主题，然后使用 bench 命令，每秒向该主题发送 1000 条消息，消息内容为一个 `hello` 的字符串文本，QoS 为 0，持续时间为 1 分钟。在每秒接收 1000 条消息的场景下，我们使用 MQTT X 开发环境中的调试工具时来观察和监控 CPU 占用率与内存占用的变化情况。

#### 测试结果

> 监控图中的 JS heap size 即为内存占用

![监控图](https://assets.emqx.com/images/586f9c2f788035ccb21e396f65ac4c54.png)

#### 分析与结论

从当前测试结果表现来看，1.9.0 版本中，在接收消息时，CPU 占用率基本维持在 100%，内存占用率最高时接近到了 2000MB，后面也基本维持在 1000MB 左右的消耗，且页面也基本无法正常使用，使用时比较卡顿。

而相比之下，1.9.1 版本在接收大量消息时，CPU 占用率平均在 50% 上下，虽然内存占用率最高时接近到了 200MB，但后面基本维持在 150MB 左右的消耗，且页面刷新流畅，使用时也无卡顿现象。

通过测试比较可发现，从内存与 CPU 消耗两项数据来看，最新版本的 MQTT X 桌面客户端性能优化提升了约 80%；从使用体验角度，页面卡顿或崩溃问题也明显改善。

除接收消息时的性能优化外，我们还对点击过滤主题和搜索消息时的性能进行了优化，支持批量存储消息数据，避免了数据库崩溃等问题。

### 交互提升

在之前的版本中，接收到新消息时默认设置了自动滚动到最新消息位置，这为用户查看历史消息带来了一丝不便。而关闭该设置又将导致用户无法及时查看到最新消息。

1.9.1 版本通过在消息列表下方显示新消息提示的方式改善了上述问题。在收到新消息后，用户可自行选择停留在当前页面继续查看历史消息，也可点击提示跳转至最新消息位置。这一交互模式改进将使用户的 MQTT X 操作体验更加顺畅。

![MQTT 客户端](https://assets.emqx.com/images/624a6f3a8132b3775c58a009e1aa2062.png)

### 问题修复与优化

除性能优化外，该版本还对以下已知问题进行了修复和优化：

- 修复导入和导出数据的完整性和正确性，并优化导入时的加载速度等；
- 修复了当使用 `客户端 ID` + `密码`认证时，必须输入`用户名`的问题；
- 修复了重连后，无法接收到离线消息的问题；
- 修复了在某些情况下，消息列表中的消息顺序不正确的问题；
- 修复在用户属性配置中不能填写多个相同的 `key` 的问题，100% 适配 MQTT 协议；
- 修复分组名称过长导致分组图标消失的问题，且支持长分组名称进行全量显示；
- 修复分组列表中，点击右键菜单显示超出窗口的问题；
- 修复点击流量统计并自动订阅系统主题 `$SYS/#` 后，导致其他订阅的主题消失的问题；
- 修复订阅主题窗口，未能正确重置订阅主题配置的问题；
- 修复当手动调整窗口大小时，导致 `Payload` 编辑器未能正确适配宽度的问题；
- 修复新建窗口时的连接高亮显示的问题；
- 将帮助页面调整为「关于 MQTT 的一些」并作为一级菜单，方便用户学习 MQTT 的相关知识；
- 优化点击发送按钮时的状态显示，避免用户误以为点击发送失败；
- 优化点击订阅按钮时，未连接状态的提醒；
- 优化主题输入框的填写的提示等。

## 命令行客户端

### 输出时间格式调整

为使用户查看和记录当前的测试时间更加准确，在最新的 MQTT X CLI 1.9.1 版本中，我们优化了输出的日志内容，为时间格式添加了 `年-月-日` 的显示，如下所示：

```
$ mqttx conn -h broker.emqx.io -p 1883
[2/2/2023] [2:54:50 PM] › …  Connecting...
[2/2/2023] [2:54:53 PM] › ✔  Connected
```

后续我们将支持用户通过自定义配置的方式来修改日期格式显示，方便用户将测试结果与自己的日志文件结合，也方便集中管理和查看。

### 其它

除日期格式调整外，命令行客户端也已经在 1.9.1 beta 测试版中加入了很多易用的新功能：

- 支持自动重连。MQTT X CLI 命令行客户端将在断开连接后自动重连，此功能同样适用于 `bench` 命令。
- 现在用户可以将连接参数保存到本地配置文件中，下次连接时可以直接读取本地配置文件中的参数，无需再次输入，且支持对所有 CLI 中的命令进行保存。
- 支持消息的格式转换，支持对接收到的消息使用 `String`、`Hex`、`Base64`、`JSON` 等格式进行转换，方便用户查看和记录消息内容等。

以上均已发布在 1.9.1 正式版中，相关新功能的详细介绍可参考之前发布的 beta 版本文章：[MQTT X newsletter 2022-11](https://www.emqx.com/zh/blog/mqttx-newsletter-202211)

## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网应用与服务的测试和开发提供便利。接下来我们将重点关注以下方面，敬请期待：

- MQTT Debug 功能
- 为系统主题的输出内容进行优化，方便用户使用 MQTT X 监控和查看 MQTT Broker 数据指标
- 接收到的消息可以进行自动图表绘制
- 插件功能
- 支持 Sparkplug B 格式
- 脚本测试自动化（Flow）
- 增强消息格式转换功能


<section class="promotion">
    <div>
        立即体验 MQTT X
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>