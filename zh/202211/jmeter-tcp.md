## 前言

对基于 TCP/IP 协议的套接字应用进行性能测试是非常常见的测试场景。JMeter 提供的“TCP 取样器”大部分情况下可以满足测试的需求，但是也有它的局限性。如果希望实现更灵活的 TCP 套接字测试方式，可以通过对 JMeter 内置的 TCP 取样器进行扩展开发来实现。

## JMeter TCP 取样器的实现

![JMeter TCP 取样器](https://assets.emqx.com/images/cba4ea4516f4e5488e14c4fb1770d44c.png)

在使用 JMeter TCP 取样器时，可以指定 TCPClient 接口的扩展类名，以切换不同的实现。如果不指定，JMeter 默认使用的是 org.apache.jmeter.protocol.tcp.sampler.TCPClientImpl。除了 TCPClientImpl，JMeter 还提供了另外两个实现，分别是 BinaryTCPClientImpl 和 LengthPrefixedBinaryTCPClientImpl，用于处理二进制格式的数据。其中：

- 使用 BinaryTCPClientImpl 时，文本框中应输入十六进制字符内容，该实现将十六进制转换为对应二进制的字节内容后进行发送。
- 使用 LengthPrefixedBinaryTCPClientImpl 时，使用字节流的前两个或前四个字节存放消息的长度，通过该前缀长度值来确定字节流的结束位置。

实现 TCPClient 接口来增加新的 TCP 取样方式，是扩展 TCP 取样器的一种方法。

但是如果我们需要对 TCP 取样器做一个通用的修改，例如，现在的 TCP 取样器在读取服务器端返回的响应时，会以“行尾 EOL 字节值”中指定的字节作为结束符，来确定读取的结束位置；不过这种设计就不适用于没有明确终止符，只有固定长度的返回响应。仅增加 TCPClient 接口的实现还不足以实现类似的需求，接下来将示例介绍如何进行改造，使得 TCP 取样器除了指定结束符，还能支持指定返回字节流的长度。


## 实现效果

先看一下修改后的效果。在“行尾EOL字节值”之后增加了一个“响应长度”的字段，举例来说，下图中指定了响应长度为12字节，如果服务器返回的是"Echo: hello\n"（其中"\n"是回车符），那么总长度就是12字节，也就是会读取到回车符之后停止。如果“行尾EOL字节值”和“响应长度”同时设置的话，将优先使用“行尾EOL字节值”的配置。

![响应长度](https://assets.emqx.com/images/326c88f741f62c9b1103671d06e8acca.png)


## 准备开发环境

首先，从 JMeter 官网下载所使用的 JMeter 对应的源代码：[https://jmeter.apache.org/download_jmeter.cgi](https://jmeter.apache.org/download_jmeter.cgi) 。

JMeter 对 TCP 协议的支持都放在了 protocol/tcp 目录下，因此本次开发的所做的更改都集中于该目录，如下图所示：

![JMeter TCP](https://assets.emqx.com/images/535a105a7121d9d1cd9c3f09a88a376b.png)

整体方法与前文 [JMeter 扩展插件实现对自定义协议进行支持](https://www.emqx.com/zh/blog/support-for-custom-protocols-through-jmeter-extensions) 很类似，也需要分别对 Sampler 界面和 Sampler 实现逻辑进行调整。

## 扩展实现

### 步骤1：改造 Sampler 界面

需要更改的类为：org.apache.jmeter.protocol.tcp.config.gui.TCPConfigGui.java

主要改动是在类中加入新的“响应长度”的字段。参考代码如下：

```
...

public class TCPConfigGui extends AbstractConfigGui {
    
    ...
	private JTextField responseLenth;
	...
	
	@Override
    public void configure(TestElement element) {
        ...
        responseLenth.setText(element.getPropertyAsString(TCPSampler.LENGTH, ""));
    }
    
    @Override
    public void modifyTestElement(TestElement element) {
        ...
        element.setProperty(TCPSampler.LENGTH, responseLenth.getText(), ""); //TCPSampler.LENGTH 稍后定义
    }
    
    @Override
    public void clearGui() {
        ...
        responseLenth.setText("");
    }
    
    private JPanel createLengthPanel() {
        JLabel label = new JLabel(JMeterUtils.getResString("response_length")); //$NON-NLS-1$ 

        responseLenth = new JTextField(3); // 3 columns size
        responseLenth.setMaximumSize(new Dimension(responseLenth.getPreferredSize()));
        label.setLabelFor(responseLenth);

        JPanel lengthPanel = new JPanel(new FlowLayout());
        lengthPanel.add(label);
        lengthPanel.add(responseLenth);
        return lengthPanel;
    }
    
    private void init() {
        ...
        optionsPanel.add(createEolBytePanel());
        optionsPanel.add(createLengthPanel());
        mainPanel.add(optionsPanel);
        ...
    }
    
    ...
}
```

### 步骤2：更新 Sampler 逻辑

首先在 org.apache.jmeter.protocol.tcp.sampler.TCPSampler.java 加入“响应长度”字段的定义，该字段值将会被 set 到 TCPClient 中：

```
...
public class TCPSampler extends AbstractSampler implements ThreadListener, Interruptible {

    ...
    public static final String LENGTH = "TCPSampler.length"; //$NON-NLS-1$
    ...
    
    private TCPClient getProtocol() {
        TCPClient tcpClient = null;
        Class<?> javaClass = getClass(getClassname());
        if (javaClass == null){
            return null;
        }
        try {
            tcpClient = (TCPClient) javaClass.newInstance();
            if (getPropertyAsString(EOL_BYTE, "").length()>0){
                tcpClient.setEolByte(getEolByte());
                log.info("Using eolByte={}", getEolByte());
            } else if (getPropertyAsString(LENGTH, "").trim().length()>0) { 
            	tcpClient.setLength(Integer.parseInt(getPropertyAsString(LENGTH, "").trim()));
            	log.info("Using length={}", getPropertyAsString(LENGTH, ""));
            }

            if (log.isDebugEnabled()) {
                log.debug("{} Created: {}@{}", this, getClassname(), Integer.toHexString(tcpClient.hashCode())); //$NON-NLS-1$
            }
        } catch (Exception e) {
            log.error("{} Exception creating: {} ", this, getClassname(), e); //$NON-NLS-1$
        }
        return tcpClient;
    }
    ...
}
```

在 TCPClient 接口中增加长度字段的支持：

```
...

public interface TCPClient {

    ...
    /**
     * Get the response length setting
     * 
     * @return
     */
    int getLength();


    /**
     * Set the length of returned response.
     * 
     * @param length
     */
    void setLength(int length);
}
```

然后对 TCPClient 的各实现类进行改造。

- AbstractTCPClient 中增加长度字段 get/set 方法的实现：

```
...

public abstract class AbstractTCPClient implements TCPClient {

    ...
    protected int length = -1;
    
    ...
    @Override
    public int getLength() {
    	if(useEolByte) {
    		return -1;
    	}
    	return length;
    }

    @Override
    public void setLength(int length) {
    	this.length = length;
    }
}
```

- TCPClientImpl 中对 read 方法进行改造：

```
...

public class TCPClientImpl extends AbstractTCPClient {

    ...
    @Override
    public String read(InputStream is, SampleResult sampleResult) throws ReadException{
        ByteArrayOutputStream w = new ByteArrayOutputStream();
        try {
            byte[] buffer = new byte[4096];
            int x;
            boolean first = true;
            //如果没有设置响应长度，仍使用行尾EOL字节值来确定响应的结束；否则使用响应长度来进行限制
            if(getLength() == -1) {
                while ((x = is.read(buffer)) > -1) {
                    if (first) {
                        sampleResult.latencyEnd();
                        first = false;
                    }
                    w.write(buffer, 0, x);
                    if (useEolByte && (buffer[x - 1] == eolByte)) {
                        break;
                    }
                } 	
            } else {
				buffer = new byte[length];
				if ((x = is.read(buffer, 0, length)) > -1) {
					sampleResult.latencyEnd();
					w.write(buffer, 0, x);
				}
            }
            
            // do we need to close byte array (or flush it?)
            if(log.isDebugEnabled()) {
                log.debug("Read: {}\n{}", w.size(), w.toString());
            }
            return w.toString(CHARSET);
        } catch (IOException e) {
            throw new ReadException("Error reading from server, bytes read: " + w.size(), e, w.toString());
        }
    }
    ...
}
```

如果需要其他的 TCPClient 实现类也支持响应长度，可以参考 TCPClientImpl 的改造来进行。

### 步骤3：编译、打包和部署

由于本次扩展直接修改了 JMeter 内置的 TCP 取样器，因此需要对 JMeter 源码部分进行编译和打包。具体方法可以参考 JMeter 官网：[https://jmeter.apache.org/building.html](https://jmeter.apache.org/building.html) 。

生成编译好的 jar 包后，替换 $JMETER_HOME/lib/ext/ApacheJMeter_tcp.jar，重启 JMeter 即可生效。

注意：由于替换掉了 JMeter 的内置实现，请先做好原有 ApacheJMeter_tcp.jar 的备份。本文只作为开发扩展的一个参考，如果用于实际的生产测试中，替换前请对扩展的修改进行仔细评估。

## 总结

本文是 JMeter 扩展开发的一次应用，在对 JMeter 内置的 TCP 取样器本身有所了解的情况下，对它的功能进行了拓展。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>
