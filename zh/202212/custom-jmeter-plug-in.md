## 前言

在本系列专题之前的文章中，我们已经介绍了 JMeter 扩展开发的一些方法。但是在开发过程中还有一个需要处理的环节，是对编写的代码进行调试。一种方式是将开发的扩展与 JMeter 源码放在一起进行调试，编译与构建 JMeter 源码的具体说明可以参考：[https://jmeter.apache.org/building.html](https://jmeter.apache.org/building.html) 。但是这种方法的缺点是需要将整个 JMeter 的源码都放在工作空间，如果新开发的扩展只是一个小插件的话，这样做就会有点过于重量级。

本文将介绍另一种比较轻量级的方式：利用 Java 远程调试（Remote Java Application）来完成对自己开发的 JMeter 扩展的调试。


## 过程

我们首先回忆一下开发好的 JMeter 扩展是如何部署到 JMeter 中的：首先将扩展代码编译生成 jar 包，拷贝到 JMeter 扩展目录 $JMETER_HOME/lib/ext 下面，然后重新启动 JMeter，就会发现新加入的扩展插件。

为了支持 JMeter 的 Java 远程调试，先要修改下 JMeter 启动时的 JVM 参数。

- 用文本编辑器打开 $JMETER_HOME/bin/jmeter.sh（如果是 Windows 操作系统的话，打开jmeter.bat）；
- 在 jmeter.sh 中定位到 JMeter 启动的位置（该位置通常在最后），并在该位置之前加入一行，在指定的端口上开启远程调试功能。下面的参考配置就是在端口 12345 上开启：

```
JVM_ARGS="$JVM_ARGS -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=12345"
```

重启 JMeter，如果配置正确的话，在 JMeter 启动的控制台上会打印出类似于下面的语句：

```
Listening for transport dt_socket at address: 12345
```

切换到开发 JMeter 扩展的 IDE 工作空间，以 Eclipse 为例，选中该扩展的项目，然后右键打开“调试配置（Debug Configurations）”，选中“Remote Java Application”，新建一个远程调试配置，并配置好 JMeter 运行所在的机器的 Host 和端口号，如下图所示，配置的是本地运行的 12345 端口

![Remote Java Application](https://assets.emqx.com/images/2168e1d0b1430e45807637a08c3a9c71.png)

创建好配置后，点击上图对话框中的 Debug 按钮，然后在 Debug 透视图中能看到类似于如下截图的内容，表示已经成功通过端口连接到本地 JMeter 的 JVM 上。

![Debug 透视图](https://assets.emqx.com/images/b7e28e4f21912bb37f7f325e405010ac.png)

在代码中需要调试的位置打好断点，在 JMeter 上进行相应操作后，即可在 Eclipse 中看到相关的调试内容，如下所示：

![查看调试内容](https://assets.emqx.com/images/0c9a912e6f119d66120a43153265d3d3.png)


## 总结

利用 Java 提供的远程调试的功能对 JMeter 扩展插件进行调试，可以比较方便地掌控 JMeter 插件在实际运行过程中的状况，更好地协助开发人员完成扩展的开发。不过也需要注意的是，这种方式有个缺点：每次开发中改了代码后再次调试，需要将更新后的 JMeter 扩展重新编译、打包、部署，并重启 JMeter。如果调试过程中频繁改动代码的话，这种调试方式稍显麻烦。读者可根据自己的实际情况选择更合适的调试方式。





<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>
