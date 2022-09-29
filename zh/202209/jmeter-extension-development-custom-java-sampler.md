JMeter 内置支持了一系列的常用协议，例如 HTTP/HTTPS、FTP、JDBC、JMS、SOAP 和 TCP 等，可以直接通过编写脚本来支持相关协议的测试场景。除了这些协议之外，用户也可能需要进行一些其他标准协议的测试，或者某些情况下在标准协议基础上增加了定制化的内容，需要对定制后的协议进行测试。本文中介绍的 Java Sampler 扩展机制就是 JMeter 提供的一种可以轻松实现对新协议支持的方式。

## Java Sampler 简介

JMeter 中有一类重要的组件，叫 Sampler，中文为“取样器”。取样器中包含了前面提到的一系列协议，可以认为“取样器”这个类别中的组件，是对相应协议的实现。不过 Java Sampler 的意思并不是指支持所谓的 Java 协议，也不能简单地说成 Java 取样器，比较准确的意思是利用自定义的 Java 类来扩展对新协议的支持，这些扩展的新协议都是通过“Java请求“加入到测试脚本中的。

下面两张图的步骤展示了如何添加 Java 请求，以及如何选择不同的 Java Sampler。

![JMeter Java Sampler](https://assets.emqx.com/images/01abf6a65412cec47d2982b040e8f944.png)

![JMeter Java Sampler](https://assets.emqx.com/images/0be972cc65e2be70cf08d98f131d35e1.png)

接下来我们将以 MQTT 协议中的连接为例，介绍使用 Java Sampler 来进行扩展开发的具体步骤。

## 准备开发环境

在开发 JMeter插件的时候，大部分情况不需要把 JMeter 的源代码下载，只需要对相关的 JMeter 库进行引用就可以了。请参见文章 [JMeter 扩展开发：自定义函数](https://emqx.atlassian.net/wiki/spaces/CM/pages/429654283/2022.09.16+JMeter) 来准备开发环境。需要注意的是，在本文的示例中，除了引用 `ApacheJMeter_core` 之外，还需要引入 `ApacheJMeter_core` ，以及支持 MQTT 协议的 Java 类库，在此例中使用的是开源的 [Eclipse Paho Java MQTT client](https://github.com/eclipse/paho.mqtt.java) 库。其他的 MQTT Java 类库当然也可以，取决于被扩展的协议和协议扩展者的偏好。

pom.xml 中所需的依赖部分如下：

```
<dependencies>
  <dependency>
    <groupId>org.eclipse.paho</groupId>
    <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
    <version>1.2.5</version>
  </dependency>
  <dependency>
    <groupId>org.apache.jmeter</groupId>
	<artifactId>ApacheJMeter_java</artifactId>
	<version>5.4.3</version>
	<scope>provided</scope>
  </dependency>
  <dependency>
    <groupId>org.eclipse.paho</groupId>
    <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
    <version>1.2.5</version>
  </dependency>
<dependencies>
```

## 开发 Java Sampler

开发一个自己的 Java Sampler 包括下面几步：

1. 继承 JMeter 抽象类 org.apache.jmeter.protocol.java.sampler.AbstractJavaSamplerClient
2. 实现下面4个方法：

方法1：

```
SampleResult runTest(JavaSamplerContext context)
```

`runTest` 方法定义在接口 JavaSamplerClient 中，扩展协议的主体逻辑就是在这个方法中进行编码实现，是必须要实现的方法。

方法2：

```
public Arguments getDefaultParameters()
```

与请求一起发送的默认参数定义在 `getDefaultParameters` 方法中，这些参数的名称和值将出现在 JMeter Java 请求对应的界面中。这个方法不是必须要实现的，使用 Java 请求的时候，如果没有默认的参数，也可以通过手动添加参数的方法加入。

方法3：

```
void setupTest(JavaSamplerContext context)
```

方法4：

```
void teardownTest(JavaSamplerContext context)
```

`setupTest` 和 `teardownTest` 顾名思义，就是在 Java 请求开始时候进行的初始化工作，以及结束时候进行的扫尾工作。这两个方法也不是必须要实现的。

### runTest 方法

先重点介绍 `runTest` 方法。 `runTest` 方法的返回结果为 SampleResult，也就是每次“取样“的结果。方法实现的一般代码结构如下：

```
@Override
public SampleResult runTest(JavaSamplerContext context) {

  SampleResult result = new SampleResult();
  result.sampleStart();
  try{ 
	//以下部分实现具体的处理逻辑
	//...
	//具体业务逻辑结束
		
	//发出请求
	result.sampleEnd();
	//请求成功，设置测试结果为成功
	result.setSuccessful(true);
	result.setResponseData("data...".getBytes());
	result.setResponseMessage("message...");
	result.setResponseCodeOK();
  } catch(Exception e) {
	//请求失败，设置测试结果为失败
	result.sampleEnd();
	result.setSuccessful(false);
	result.setResponseCode("500");
  }
  return result;
}
```

如上所示，代码逻辑主要是：

1）对目标系统必送正确的协议数据。

2）根据目标系统返回的数据，给 SampleResult 设置正确的方法、结束时间等，这样 JMeter 引擎可获知测试成功与否，进一步地可以正确显示到 JMeter 的报告结果中。

进行普通 MQTT TCP 连接，业务逻辑部分的实现可以参考下面的代码：

```
//MQTT Broker 的连接信息
String broker = "tcp://broker.emqx.io:1883";
String username = "emqx";
String password = "public";
String clientid = "publish_client";

MqttClient client = new MqttClient(broker, clientid, new MemoryPersistence());
MqttConnectOptions options = new MqttConnectOptions();
options.setUserName(username);
options.setPassword(password.toCharArray());
client.connect(options);
```

### getDefaultParameters 方法

上述代码中我们硬编码了 MQTT Broker 的连接信息，但在实际应用场景中，更希望能使用一个 JMeter 插件，连接不同的 MQTT Broker。这种情况下，就可以将连接信息从 `JavaSamplerContext` 的参数中读取出来：

```
String broker = context.getParameter("broker");
String username = context.getParameter("user");
String password = context.getParameter("password");
String clientid = context.getParameter("clientid");
```

参数具体值的输入由脚本编写人员在 JMeter 界面上编辑脚本时指定，或者在运行期间使用指定变量的值。而为了方便脚本编写人员了解并更改所需的参数，我们通过 `getDefaultParameters` 方法将这些参数在界面上暴露出来：

```
public Arguments getDefaultParameters() {
  Arguments arguments = new Arguments();
  arguments.addArgument("broker", "tcp://broker.emqx.io:1883");
  arguments.addArgument("user", "emqx");
  arguments.addArgument("password", "public");
  arguments.addArgument("clientid", "publish_client");
  return arguments;
}
```

### setupTest 方法

跟写 JUnit 测试的 setup 方法类似，这里主要运行针对单个虚拟用户的一次性起始、准备性的操作。

### teardownTest 方法

与 JUnit 测试的 teardown 方法类似，这里主要运行针对单个虚拟用户的收尾的操作。需要注意的是，该方法的调用不是在单个虚拟用户的线程里，而是所有虚拟用户都在一个线程里顺序执行该方法。

## 编译、部署与使用

完成了代码的编写，需要将代码进行编译和部署。pom.xml 的 build 设置及编译具体方法也可参见文章 [JMeter 扩展开发：自定义函数](https://emqx.atlassian.net/wiki/spaces/CM/pages/429654283/2022.09.16+JMeter)。 

编译完成后，在 target 目录下会生成一个 jar 包。请注意通过示例的 pom.xml，编译出来的 jar 包里包含了所需的第三方类库，如 org.eclipse.paho.client.mqtt 库，避免 JMeter 运行时找不到第三方提供的类的问题。

将编译好的 jar 拷贝到 $JMETER_HOME/lib/ext 目录下，重启 JMeter。启动完毕，添加一个 Java 请求，在类名称下拉列表框中应该就能看到新扩展的类了。如果不存在，请查看一下 lib/ext 目录下是否正确拷贝了 jar 包，也可以查一下 JMeter 的日志，确认没有报出异常。

![Java 请求](https://assets.emqx.com/images/519e02198bac90615bb4af4d32cf7b3c.png)

至此，我们完成了通过 JMeter 提供的扩展机制来支持新协议的测试。可以看到 JMeter 对新协议的定制扩展还是比较简单的。不过通过 Java Sampler 方式扩展的协议在界面友好性上与 JMeter 提供的标准协议相比还是较差，我们将在本系列专题的后续文章中介绍如何使用 JMeter 更强大的扩展方式，敬请期待。


<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>
