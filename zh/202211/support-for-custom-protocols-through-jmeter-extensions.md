## 前言

我们已经在上文中介绍了如何使用 JMeter 的 Java Sampler 扩展机制轻松实现对新协议的支持。Java Sampler 方式的优点在于实现快速，只需关注协议的逻辑部分即可；但缺点是只能以参数的方式进行互动，界面可用性不高，主要用于待测试协议的原型开发。如果希望实现类似 HTTP Sampler 的界面完整友好的协议扩展，JMeter 也提供了相应的扩展机制，接下来我们将以扩展一个简单的 Apache Kafaka Producer Sampler 为例，介绍如何实现更完善的新协议插件。

## Kafka 简介

[Apache Kafka](https://kafka.apache.org) 是由 Apache 软件基金会开发的一个开源消息系统项目。Kafka 最初是由 LinkedIn 开发，并于2011年初开源，2012年10月从 Apache 孵化器毕业。该项目的目标是为处理实时数据提供一个统一、高通量、低等待的平台。

如下图所示，Kafka 的 Producer（数据生产者）通过 Socket 向 Kafka 集群上配置好的 Topic（主题）发送数据，Consumer（数据消费者）在另一端消费由生产者产生的数据，并进行业务的处理。Kafka 作为一个优秀的消息处理系统，在集群配置、主题管理等方面有很多值得深入理解和优化的地方，由于本文的重点是 JMeter 的扩展，只以 Kafka 的生产者为例来介绍如何利用 JMeter 模拟大量生产者，更多关于 Kafka 的细节请参考它的[官方文档](https://kafka.apache.org/documentation.html)。


## 准备工作

扩展实现 JMeter 插件之前，先考虑清楚哪些选项需要暴露给测试人员。像使用 HTTP Sampler 进行测试时，需要让测试人员提供服务器地址、端口号、路径、请求方法、请求内容等信息。有时也需要进行一些高级配置，比如同线程组里的连接是否共用，这些选项也会在界面中体现，当然插件实现业务逻辑的时候处理连接的代码也会有所不同。

往 Kafka 上发送消息时，需要提供一些基本配置信息（实际 Kafka 的生产者配置不止这些，这里只举例了最基本的一些配置项作为演示），如果读者对下面所说的内容不了解也不要紧，只需要理解做这些准备的目的是为了将这些配置选项提供给 Kafka 测试人员，在开始测试之前可以针对被测系统进行配置。

1. 服务器所在地址，在 Kafka 中称之为 Broker；
2. 目标主题的名称；
3. Value Serializer：Kafka 通过网络发送的消息，需要将其序列化。Kafka 消息包括 Key 和 Value，示例中发送不带 Key 的消息，因此要指定是消息中的 Value 的序列化方式；
4. 发送的消息。

下图是本文最终完成的 JMeter Kafka Producer Sampler 插件的截图，使用该插件进行测试前，需要输入上面所列的信息。

![JMeter Kafka Producer Sampler](https://assets.emqx.com/images/9303da168adb64af8ed395db42960ac3.png)


## JMeter 扩展实现

### 步骤1：准备开发环境

前方已经介绍过如何准备开发环境，请参考 [JMeter 扩展开发：自定义函数](https://www.emqx.com/zh/blog/jmeter-extension-development-custom-functions) 创建 Maven 项目。针对本文的任务， 项目中需要使用到的依赖包括 `ApacheJMeter_core` 和 `ApacheJMeter_java`，以及 Kafka 类库。

项目 pom.xml 中所需的依赖部分如下：

```
<dependencies>
  	<dependency>
		<groupId>org.apache.jmeter</groupId>
		<artifactId>ApacheJMeter_core</artifactId>
		<version>5.4.3</version>
		<scope>provided</scope>
	</dependency>
	<dependency>
		<groupId>org.apache.jmeter</groupId>
		<artifactId>ApacheJMeter_java</artifactId>
		<version>5.4.3</version>
		<scope>provided</scope>
  	</dependency>
	<dependency>
		<groupId>org.apache.kafka</groupId>
		<artifactId>kafka-clients</artifactId>
		<version>3.3.0</version>
	</dependency>
</dependencies>
```

项目创建完毕后，开始编写代码来实现插件。

### 步骤2：开发插件界面

之前扩展的 Java Sampler 的界面已由 JMeter 扩展框架来处理，因此不需要我们重新编写。但是本文示例的插件，需要自定义插件的界面，所以需要把插件界面也一并开发。JMeter 扩展机制中，界面与业务逻辑是分离的，界面的开发也由独立的类来完成。

需要注意的是，JMeter 的扩展机制会从 $JMETER_HOME/lib/ext 目录下去动态加载符合指定条件的 jar 包，并在 JMeter 中显示出来。比如要扩展 UI 的话，扩展的 Java 类的包名须包含”.gui”，回忆一下，之前介绍的扩展函数也是类似，它的 Java 类的包名需要包含”.functions”。我们创建以下这个包：com.emqx.xmeter.demo.kafka.sampler.gui。

然后新建一个类：com.emqx.xmeter.demo.kafka.sampler.gui.KafkaSamplerUI，并指定其父类为org.apache.jmeter.samplers.gui.AbstractSamplerGui。AbstractSamplerGui 是 JMeter Sampler 实现界面的统一父类。新建的 KafkaSamplerUI.java 要实现以下的功能：

1. 界面布局与控件生成。JMeter 的界面是标准的 Swing，所以里面的控件和布局都是标准 Swing 的写法。
2. 界面与 Sampler 之间的数据交换。Sampler 在 JMeter 中继承自 TestElement，用户输入的数据保存在 Sampler 中，并持久化保存到 .jmx 脚本文件中。因此可以认为 Sampler 是界面的模型。

界面与模型（Sampler）之间的数据交换需要实现父类的以下几个方法：

方法 1：

```
public void configure(TestElement element)
```

该方法用于把 Sampler 中的数据加载到界面中。在实现自己的逻辑之前，先调用父类的方法super.configure(element)，可以确保框架自动为你加载一些缺省数据，比如 Sampler 名字。

方法 2：

```
public void modifyTestElement(TestElement element)
```

该方法用于把界面的数据移到 Sampler 中，刚好与 `configure` 方法相反。在调用自己的实现方法前，先调用super.configureTestElement(element)，也会帮助移动一些缺省数据到 Sampler 中。

方法 3：

```
public TestElement createTestElement()
```

该方法创建一个新的 Sampler，然后将界面中的数据设置到这个新的 Sampler 实例中。

方法 4：

```
public void clearGui()
```

该方法会在重新渲染界面的时候调用，可以在其中设置界面控件中显示的一些缺省值。

方法 5：

```
public String getLabelResource()
```

该方法指定显示在界面上 Sampler 子菜单中显示的 Sampler 名称，是通过指定资源文件中的资源名来匹配多语言的。也可以通过方法 getStaticLabel 来指定固定的名称，这样的名称将不会随 JMeter 语言改变而变动。如本文的例子中，我们将 Sampler 显示名称设定为固定的”Kafka Producer Sampler”。

本例中使用的完整界面代码如下，对以上的方法均进行了实现。界面上包括4个控件（3个设置参数的控件中同一个 panel 中，发送消息的控件在另一个 panel 中）。

```
package com.emqx.xmeter.demo.kafka.sampler.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.GridLayout;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;

import org.apache.jmeter.gui.util.JSyntaxTextArea;
import org.apache.jmeter.gui.util.JTextScrollPane;
import org.apache.jmeter.gui.util.VerticalPanel;
import org.apache.jmeter.samplers.gui.AbstractSamplerGui;
import org.apache.jmeter.testelement.TestElement;
import org.apache.jorphan.gui.JLabeledTextField;

import com.emqx.xmeter.demo.kafka.samplers.KafkaSampler;

public class KafkaSamplerUI extends AbstractSamplerGui {
	
	private static final long serialVersionUID = 1L;
	
	private final JLabeledTextField brokersField = new JLabeledTextField("Brokers");
	private final JLabeledTextField topicField = new JLabeledTextField("Topic");
	private final JLabeledTextField valueSerializerField = new JLabeledTextField("Value Serializer");
	
	private final JSyntaxTextArea textMessage = JSyntaxTextArea.getInstance(10, 50);
	private final JLabel textArea = new JLabel("Message");
	private final JTextScrollPane textPanel = JTextScrollPane.getInstance(textMessage);

	public KafkaSamplerUI() {
		super();
		this.init();
	}
	
	//界面布局初始化
	private void init() {
		setLayout(new BorderLayout());
		setBorder(makeBorder());

		add(makeTitlePanel(), BorderLayout.NORTH);
		JPanel mainPanel = new VerticalPanel();
		add(mainPanel, BorderLayout.CENTER);

		JPanel DPanel = new JPanel();
		DPanel.setLayout(new GridLayout(3, 2));
		DPanel.add(brokersField);
		DPanel.add(topicField);
		DPanel.add(valueSerializerField);

		JPanel ControlPanel = new VerticalPanel();
		ControlPanel.add(DPanel);
		ControlPanel.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.gray), "Parameters"));
		mainPanel.add(ControlPanel);

		JPanel ContentPanel = new VerticalPanel();
		JPanel messageContentPanel = new JPanel(new BorderLayout());
		messageContentPanel.add(this.textArea, BorderLayout.NORTH);
		messageContentPanel.add(this.textPanel, BorderLayout.CENTER);
		ContentPanel.add(messageContentPanel);
		ContentPanel.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.gray), "Content"));
		mainPanel.add(ContentPanel);
	}
	
	public String getLabelResource() {
		throw new RuntimeException();
	}
	
	public String getStaticLabel() {
		return "Kafka Producer Sampler";
	}

	public TestElement createTestElement() {
		KafkaSampler sampler = new KafkaSampler();
		this.setupSamplerProperties(sampler);
		return sampler;
	}

	public void modifyTestElement(TestElement element) {
		KafkaSampler sampler = (KafkaSampler) element;
		this.setupSamplerProperties(sampler);
	}
	
	private void setupSamplerProperties(KafkaSampler sampler) {
		this.configureTestElement(sampler);
		sampler.setBrokers(this.brokersField.getText());
		sampler.setTopic(this.topicField.getText());
		sampler.setMessage(this.textMessage.getText());
		sampler.setValueSerializer(this.valueSerializerField.getText());
	}
	
	@Override
	public void configure(TestElement element) {
		super.configure(element);
		KafkaSampler sampler = (KafkaSampler)element;
		this.brokersField.setText(sampler.getBrokers());
		this.topicField.setText(sampler.getTopic());
		this.valueSerializerField.setText(sampler.getValueSerializer());
		this.textMessage.setText(sampler.getMessage());
	}

	@Override
	public void clearGui() {
		super.clearGui();
		this.brokersField.setText("kafka_server:9092");
		this.topicField.setText("jmeterTest");
		this.valueSerializerField.setText("kafka.serializer.StringEncoder");
		this.textMessage.setText("");
	}
}
```

### 步骤3：开发 Sampler 逻辑

新开发的 Sampler 需要继承父类 org.apache.jmeter.samplers.AbstractSampler，并做以下实现：

1. 增加 getter/setter 方法，用于与界面之间的数据交换。用户保存/打开 .jmx 脚本文件时，这些数据将被自动序列化/反序列化。
2. 实现 sample 方法：

```
public SampleResult sample(Entry entry)
```

JMeter 通过该方法，对目标系统发起请求，主要完成的工作包括：

- 记录请求处理时间
- 对返回结果进行处理和判断
- 根据处理结果返回 SampleResult，该 SampleResult 中需要判断返回的内容是否成功，并指定展示给测试人员的消息等。

该方法的基本实现框架如下所示：

```
public SampleResult sample(Entry entry) {
    SampleResult result = new SampleResult();
    result.setSampleLabel(getName());
    try {
        result.sampleStart();
        //对目标系统发出测试请求
        //...
        //收到目标系统的响应
        result.sampleEnd();
        result.setSuccessful(true);
        result.setResponseCodeOK();
    } catch (Exception e) {
        result.sampleEnd();
        result.setSuccessful(false);
        result.setResponseMessage("Exception: " + e);
        java.io.StringWriter stringWriter = new java.io.StringWriter();
        e.printStackTrace(new java.io.PrintWriter(stringWriter));
        result.setResponseData(stringWriter.toString(), null);
        result.setDataType(org.apache.jmeter.samplers.SampleResult.TEXT);
        result.setResponseCode("FAILED");
    }
    return result;
}
```

本例的实现中，将为每个虚拟用户生成一个 Kafka 的 Producer 对象，并将界面中指定的消息发送到 Kafka 服务器。完整的代码如下：

```
package com.emqx.xmeter.demo.kafka.samplers;

import java.text.MessageFormat;
import java.util.Properties;
import java.util.concurrent.ConcurrentHashMap;

import org.apache.jmeter.samplers.AbstractSampler;
import org.apache.jmeter.samplers.Entry;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.log4j.Logger;

public class KafkaSampler extends AbstractSampler {

	private static final long serialVersionUID = 1L;
	
	private static final String KAFKA_BROKERS = "kafka.brokers";
	private static final String KAFKA_TOPIC = "kafka.topic";
	private static final String KAFKA_MESSAGE = "kafka.message";
	private static final String KAFKA_VALUE_SERIALIZER = "kafka.value.serializer";
	
	private static ConcurrentHashMap<String, Producer<String, String>> producers = new ConcurrentHashMap<>();
	private static final Logger log = Logger.getLogger(KafkaSampler.class);
	
	public KafkaSampler() {
		setName("Kafka Sampler");
	}
	
	@Override
	public SampleResult sample(Entry entry) {
		SampleResult result = new SampleResult();
		result.setSampleLabel(getName());
		try {
			result.sampleStart();
			
			Producer<String, String> producer = getProducer();
			ProducerRecord<String, String> msg = new ProducerRecord<String, String>(
					getTopic(), getMessage());
			producer.send(msg);
			
			result.sampleEnd(); 
			result.setSuccessful(true);
			result.setResponseCodeOK();
		} catch (Exception e) {
			result.sampleEnd();
			result.setSuccessful(false);
			result.setResponseMessage("Exception: " + e);
			java.io.StringWriter stringWriter = new java.io.StringWriter();
			e.printStackTrace(new java.io.PrintWriter(stringWriter));
			result.setResponseData(stringWriter.toString(), null);
			result.setDataType(org.apache.jmeter.samplers.SampleResult.TEXT);
			result.setResponseCode("FAILED");
		}
		return result;
	}

	private Producer<String, String> getProducer() {
		String threadGrpName = getThreadName();
		Producer<String, String> producer = producers.get(threadGrpName);
		if(producer == null) {
			log.info(MessageFormat.format("Cannot find the producer for {0}, going to create a new producer.", threadGrpName));
			Properties props = new Properties();
			props.put("bootstrap.servers", getBrokers());
			props.put("value.serializer", getValueSerializer());
			props.put("linger.ms", 1);
			producer = new KafkaProducer<String,String>(props);
			
			producers.put(threadGrpName, producer);
		}
		return producer;
	}
	
	public String getBrokers() {
		return getPropertyAsString(KAFKA_BROKERS);
	}

	public void setBrokers(String brokers) {
		setProperty(KAFKA_BROKERS, brokers);
	}

	public String getTopic() {
		return getPropertyAsString(KAFKA_TOPIC);
	}

	public void setTopic(String topic) {
		setProperty(KAFKA_TOPIC, topic);
	}

	public String getMessage() {
		return getPropertyAsString(KAFKA_MESSAGE);
	}

	public void setMessage(String message) {
		setProperty(KAFKA_MESSAGE, message);
	}
	
	public String getValueSerializer() {
		return getPropertyAsString(KAFKA_VALUE_SERIALIZER);
	}

	public void setValueSerializer(String valueSerializer) {
		setProperty(KAFKA_VALUE_SERIALIZER, valueSerializer);
	}
}
```

### 步骤4：编译、打包和部署

打包过程与 [JMeter 扩展开发：自定义函数](https://emqx.atlassian.net/wiki/spaces/CM/pages/429654283/2022.09.16+JMeter) 中提到的相似，注意把本插件需要的 Kafka 相关依赖库文件也一并打入，否则还需要将所依赖的 Kafka jar 包单独部署到 JMeter 插件目录下。可以参考以下方式在 pom.xml 中配置 build 插件：

```
<build>
  	<finalName>${project.artifactId}</finalName>
	<plugins>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.8.0</version>
			<configuration>
				<source>1.8</source>
				<target>1.8</target>
			</configuration>
		</plugin>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-assembly-plugin</artifactId>
			<configuration>
				<descriptorRefs>
					<descriptorRef>jar-with-dependencies</descriptorRef>
				</descriptorRefs>
			</configuration>
			<executions>
				<execution>
					<id>assemble-all</id>
					<phase>package</phase>
					<goals>
						<goal>single</goal>
					</goals>
				</execution>
			</executions>
		</plugin>
	</plugins>
</build>
```

编译打包完成后，从 target 目录下将 kafka-producer-plugin-jar-with-dependencies.jar 拷贝至 $JMETER_HOME/lib/ext 目录下，并重启 JMeter。

### 步骤5：测试插件

新建一个测试脚本，在测试计划中加入一个线程组，然后添加 Sampler。如果插件开发与部署没有问题，在子菜单中就能看到我们扩展出来的”Kafka Sampler”。

![Kafka Sampler](https://assets.emqx.com/images/2e999cce752ee250c92f0191c7f99c7a.png)

修改线程组中的线程数，就能模拟多虚拟用户的并发测试了。下图是“察看结果树”中显示的示例结果内容：

![察看结果树](https://assets.emqx.com/images/d44f8d0fe55ceb99023ea592d38f5625.png)

从 Kafka 的消费者端，也可以看到可以接收到相关的消息：

![Kafka 的消费者端查看消息](https://assets.emqx.com/images/bfc717d850a5992bb721e1aa2bf838f9.png)


## 总结

如本文所示，如果通过比较”标准”的方式来扩展 JMeter 对新协议的测试 Sampler，还是有一定的工作量，特别是需要比较丰富的界面功能的话，界面的实现会比较复杂。如果对界面的要求不高，并且通过传参的方式可以完成与 Sampler 的交互，那么使用前文 [JMeter 自定义协议扩展之 Java Sampler](https://www.emqx.com/zh/blog/jmeter-extension-development-custom-java-sampler) 介绍的方法扩展 Java Sampler 会是更简单的一种方式。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>
