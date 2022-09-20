## 前言

物联网正在以爆炸式的增长势头飞速发展。随着设备规模的不断增长和业务逻辑的愈发复杂，物联网平台在正式上线前，需要通过对平台大量接入设备时的可用性和可靠性进行验证以确保系统质量。[物联网性能测试](https://www.emqx.com/zh/products/xmeter)的价值与必要性因此逐渐凸显。

一方面，性能测试为评估物联网系统提供依据，从设计指标、可扩展性和可靠性多个维度加以验证；另一方面，性能测试也有助于物联网系统的优化，帮助及早发现系统性能瓶颈，提供调优建议。此外，性能测试还可以辅助容量计划的制定，为未来扩容计划提供参考。

而物联网系统接入设备量大、协议多样化、集成架构复杂、跨部门开发协作频繁这些特点，也使物联网性能测试面临着重重挑战。**本系列文章将以基于 [EMQX](https://www.emqx.com/zh/products/emqx) 的物联网平台为例，介绍如何使用性能测试工具进行平台相关质量指标的验证与测试。**

## 测试工具的选择——JMeter 简介

我们选择 JMeter 作为本次的测试工具。

[JMeter](https://jmeter.apache.org) 是 Apache 基金会旗下一款开源软件，主要通过模拟并发负载来实现性能测试，是目前开源社区的主流性能测试工具。其主要具有以下优势：

- 内置多种协议的测试支持，如 TCP、HTTP/HTTPS 等。
- 提供灵活的插件扩展机制，支持第三方扩展其他的协议。对于物联网系统中种类繁多的协议，只需按 JMeter 的框架要求定制开发所需协议业务逻辑，就能方便地放入 JMeter 的插件库，使用 JMeter 既有功能进行该协议的性能测试。
- 具有良好的社区支持。

## JMeter 的安装

目前 JMeter 最新稳定版本是 5.4.1，由于 JMeter 是基于 Java 的，5.4.1 版本的 JMeter 需要预先安装 Java 8 及以上的支持（可从以下地址获取：[https://www.oracle.com/java/technologies/downloads](https://www.oracle.com/java/technologies/downloads) ）。

安装完 Java 后，从官网下载 JMeter：[https://jmeter.apache.org/download_jmeter.cgi](https://jmeter.apache.org/download_jmeter.cgi) 。

下载完成后解压，并进入解压后目录下的 bin 子目录。根据操作系统的不同，运行 jmeter.bat（Windows系统）或 jmeter（Unix系统）。如果一切顺利，JMeter 的脚本编辑界面将会呈现在您的面前：

![安装 JMeter](https://assets.emqx.com/images/4609157fd7134937f961b7ea865b70a3.png)

接下来，我们以 HTTP 为例，看一下如何使用 JMeter 来构建并运行一个简单的测试用例。

1. 添加虚拟用户组（Thread Group）：右击测试计划 > 添加 > 线程（用户）> 线程组

   ![JMeter 添加虚拟用户组](https://assets.emqx.com/images/30f13fb31cc91973b2b96331eb489caf.png)

   JMeter 使用单个线程来模拟一个用户，用户组 Thread Group 就是指一组用户，作为模拟访问被测系统的虚拟用户组。

   「线程属性」中的「线程数」可用于配置虚拟用户组的并发用户数，数值越高，并发量越大；「循环次数」可用于配置每个虚拟用户执行多少次的测试。

   ![JMeter 线程属性](https://assets.emqx.com/images/912dd10b41740f7d96c24bbec526703f.png)

2. 添加被测 HTTP 页面：右击线程组 > 添加 > 取样器 > HTTP请求

   ![JMeter 添加被测 HTTP 页面](https://assets.emqx.com/images/ea70b47f38d2dab43bb24315a8e1ed72.png)

   示例测试脚本中我们只使用默认的 HTTP 请求设置，对 bing 网站发起 HTTP 请求，您可以根据实际情况进行相关的配置。

   ![JMeter 添加被测 HTTP 页面2](https://assets.emqx.com/images/cbe81f4bd52ef37b72e8ad9bea08c21f.png)

3. 添加结果监听器：右击线程组 > 添加 > 监听器 > 察看结果树

   监听器在实际运行性能测试中并不是必须的，但在编写脚本的过程中可以帮助直观看到测试结果，方便调试。在这个样例脚本中我们将使用「察看结果树」来帮助查看请求的响应信息。

   ![JMeter 添加结果监听器](https://assets.emqx.com/images/c077ea6fea30948e41ca60e5aad2176b.png)

4. 运行测试。

   保存测试脚本后，点击操作栏中的「启动」按钮，就开始运行测试脚本了。建议线程组中的线程数和循环次数设置得小一些（比如10以内），以免被 ban。

   ![运行JMeter测试](https://assets.emqx.com/images/f6f9b1200acc5db71be4a0e26aa8ba35.png)

以上，我们就完成了一个简单的 HTTP 测试脚本。大家可以举一反三，试试其他协议的测试。下一篇文章中，我们将更详细地介绍 JMeter 的各种测试元件，配合使用就能构建更复杂的测试场景。

## 本系列中的其它文章

- [JMeter 测试组件介绍 - 物联网大并发测试实战 02](https://www.emqx.com/zh/blog/introduction-to-jmeter-test-components)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 03](https://www.emqx.com/zh/blog/how-to-use-the-mqtt-plugin-in-jmeter)
- [JMeter MQTT 在连接测试场景中的使用 - 物联网大并发测试实战 04](https://www.emqx.com/zh/blog/test-mqtt-connection-with-jmeter)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 05](https://www.emqx.com/zh/blog/the-use-of-jmeter-mqtt-in-subscription-and-publishing-test-scenarios)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
