从 v4.1 版本开始，[EMQX MQTT 服务器](https://www.emqx.com/zh/products/emqx) 提供了专门的多语言支持插件 [emqx_extension_hook](https://github.com/emqx/emqx-extension-hook) ，现已支持使用其他编程语言来处理 EMQX 中的钩子事件，开发者可以使用 Python 或者 Java 快速开发自己的插件，在官方功能的基础上进行扩展，满足自己的业务场景。例如：

- 验证某客户端的登录权限：客户端连接时触发对应函数，通过参数获取客户端信息后通过读取数据库、比对等操作判定是否有登录权限
- 记录客户端在线状态与上下线历史：客户端状态变动时触发对应函数，通过参数获取客户端信息，改写数据库中客户端在线状态
- 校验某客户端的 PUB/SUB 的操作权限：发布/订阅时触发对应函数，通过参数获取客户端信息与当前主题，判定客户端是否有对应的操作权限
- 处理会话 (Sessions) 和 消息 (Message) 事件，实现订阅关系与消息处理/存储：消息发布、状态变动时触发对应函数，获取当前客户端信息、消息状态与消息内容，转发到 Kafka 或数据库进行存储。

>  注：消息(Message) 类钩子，仅在企业版中支持。



Python 和 Java 驱动基于 [Erlang/OTP-Port](https://erlang.org/doc/tutorial/c_port.html) 进程间通信实现，本身具有非常高的吞吐性能，本文以 Java 拓展为例介绍 EMQX 跨语言拓展使用方式。

![upeb67488ae758908b02ac8567c37fcf2d0a9.png](https://assets.emqx.com/images/ebacb8e0adf3283bf44a968e38c402ab.png)



## Java 拓展使用示例

### 要求

- EMQX 所在服务器需安装 JDK 1.8 以上版本

### 开始使用

1. 创建 Java 项目
2. 下载 [io.emqx.extension.jar](https://github.com/emqx/emqx-extension-java-sdk/releases) 和 [erlport.jar](https://github.com/emqx/emqx-extension-java-sdk/tree/master/deps) 文件
3. 添加SDK `io.emqx.extension.jar`和 `erlport.jar` 到项目依赖
4. 复制 `examples/SampleHandler.java`到您的项目中
5. 根据 SDK `SampleHandler.java` 中的示例编写业务代码，确保能够成功编译

### 部署

编译所有源代码后，需要将 `sdk` 和代码文件部署到 EMQX 中：

1. 复制 `io.emqx.extension.jar` 到 `emqx/data/extension` 目录
2. 将编译后的 `.class` 文件，例如 `SampleHandler.class` 复制到 `emqx/data/extension  `目录
3. 修改 `emqx/etc/plugins/emqx_extension_hook.conf` 配置文件：

```bash
exhook.drivers = java
## Search path for scripts or library
exhook.drivers.java.path = data/extension/
exhook.drivers.java.init_module = SampleHandler
```

启动 `emqx_extension_hook` 插件，如果配置错误或 Java 代码编写错误将无法正常启动。启动后尝试建立 MQTT 连接并观察业务运行情况。



### 示例

以下为 [Main.java](https://github.com/emqx/emqx-exhook/tree/master/test/scripts) 示例程序， 该程序继承自 SDK 中的 `DefaultCommunicationHandler` 类。该示例代码演示了如何挂载 EMQX 系统中所有的钩子：

```java
import emqx.extension.java.handler.*;
import emqx.extension.java.handler.codec.*;
import emqx.extension.java.handler.ActionOptionConfig.Keys;

public class SampleHandler extends DefaultCommunicationHandler {
    
    @Override
    public ActionOptionConfig getActionOption() {
        ActionOptionConfig option = new ActionOptionConfig();
        option.set(Keys.MESSAGE_PUBLISH_TOPICS, "#");
        option.set(Keys.MESSAGE_DELIVERED_TOPICS, "#");
        option.set(Keys.MESSAGE_ACKED_TOPICS, "#");
        option.set(Keys.MESSAGE_DROPPED_TOPICS, "#");
        
        return option;
    }
    
    // Clients
    @Override
    public void onClientConnect(ConnInfo connInfo, Property[] props) {
        System.err.printf("[Java] onClientConnect: connInfo: %s, props: %s\n", connInfo, props);
    }

    @Override
    public void onClientConnack(ConnInfo connInfo, ReturnCode rc, Property[] props) {
        System.err.printf("[Java] onClientConnack: connInfo: %s, rc: %s, props: %s\n", connInfo, rc, props);
    }

    @Override
    public void onClientConnected(ClientInfo clientInfo) {
        System.err.printf("[Java] onClientConnected: clientinfo: %s\n", clientInfo);
    }

    @Override
    public void onClientDisconnected(ClientInfo clientInfo, Reason reason) {
        System.err.printf("[Java] onClientDisconnected: clientinfo: %s, reason: %s\n", clientInfo, reason);
    }

    // 判定认证结果，返回 true 或 false 
    @Override
    public boolean onClientAuthenticate(ClientInfo clientInfo, boolean authresult) {
        System.err.printf("[Java] onClientAuthenticate: clientinfo: %s, authresult: %s\n", clientInfo, authresult);

        return true;
    }

    // 判定 ACL 检查结果，返回 true 或 false 
    @Override
    public boolean onClientCheckAcl(ClientInfo clientInfo, PubSub pubsub, Topic topic, boolean result) {
        System.err.printf("[Java] onClientCheckAcl: clientinfo: %s, pubsub: %s, topic: %s, result: %s\n", clientInfo, pubsub, topic, result);

        return true;
    }

    @Override
    public void onClientSubscribe(ClientInfo clientInfo, Property[] props, TopicFilter[] topic) {
        System.err.printf("[Java] onClientSubscribe: clientinfo: %s, topic: %s, props: %s\n", clientInfo, topic, props);
    }

    @Override
    public void onClientUnsubscribe(ClientInfo clientInfo, Property[] props, TopicFilter[] topic) {
        System.err.printf("[Java] onClientUnsubscribe: clientinfo: %s, topic: %s, props: %s\n", clientInfo, topic, props);
    }

    // Sessions
    @Override
    public void onSessionCreated(ClientInfo clientInfo) {
        System.err.printf("[Java] onSessionCreated: clientinfo: %s\n", clientInfo);
    }

    @Override
    public void onSessionSubscribed(ClientInfo clientInfo, Topic topic, SubscribeOption opts) {
        System.err.printf("[Java] onSessionSubscribed: clientinfo: %s, topic: %s\n", clientInfo, topic);
    }

    @Override
    public void onSessionUnsubscribed(ClientInfo clientInfo, Topic topic) {
        System.err.printf("[Java] onSessionUnsubscribed: clientinfo: %s, topic: %s\n", clientInfo, topic);
    }

    @Override
    public void onSessionResumed(ClientInfo clientInfo) {
        System.err.printf("[Java] onSessionResumed: clientinfo: %s\n", clientInfo);
    }

    @Override
    public void onSessionDiscarded(ClientInfo clientInfo) {
        System.err.printf("[Java] onSessionDiscarded: clientinfo: %s\n", clientInfo);
    }
    
    @Override
    public void onSessionTakeovered(ClientInfo clientInfo) {
        System.err.printf("[Java] onSessionTakeovered: clientinfo: %s\n", clientInfo);
    }

    @Override
    public void onSessionTerminated(ClientInfo clientInfo, Reason reason) {
        System.err.printf("[Java] onSessionTerminated: clientinfo: %s, reason: %s\n", clientInfo, reason);
    }

    // Messages
    @Override
    public Message onMessagePublish(Message message) {
        System.err.printf("[Java] onMessagePublish: message: %s\n", message);
        
        return message;
    }

    @Override
    public void onMessageDropped(Message message, Reason reason) {
        System.err.printf("[Java] onMessageDropped: message: %s, reason: %s\n", message, reason);
    }

    @Override
    public void onMessageDelivered(ClientInfo clientInfo, Message message) {
        System.err.printf("[Java] onMessageDelivered: clientinfo: %s, message: %s\n", clientInfo, message);
    }

    @Override
    public void onMessageAcked(ClientInfo clientInfo, Message message) {
        System.err.printf("[Java] onMessageAcked: clientinfo: %s, message: %s\n", clientInfo, message);
    }
}
```

`SampleHandler` 主要包含两部分：

1. 重载了 `getActionOption` 方法。该方法对消息（Message）相关的钩子进行配置，指定了需要生效的主题列表。

   | 配置项                   | 对应钩子          |
   | ------------------------ | ----------------- |
   | MESSAGE_PUBLISH_TOPICS   | message_publish   |
   | MESSAGE_DELIVERED_TOPICS | message_delivered |
   | MESSAGE_ACKED_TOPICS     | message_acked     |
   | MESSAGE_DROPPED_TOPICS   | message_dropped   |

2. 重载了 `on<hookName>` 方法，这些方法是实际处理钩子事件的回调函数，函数命名方式为各个钩子名称变体后前面加 `on` 前缀，变体方式为钩子名称去掉下划线后使用骆驼拼写法（CamelCase），例如，钩子client_connect对应的函数名为onClientConnect。 EMQX 客户端产生的事件，例如：连接、发布、订阅等，都会最终分发到这些钩子事件回调函数上，然后回调函数可对各属性及状态进行相关操作。 示例程序中仅对各参数进行了打印输出。如果只关心部分钩子事件，只需对这部分钩子事件的回调函数进行重载即可，不需要重载所有回调函数。

各回调函数的执行时机和支持的钩子列表与 EMQX 内置的钩子完全一致，参见：[Hooks - EMQX](https://docs.emqx.com/zh/emqx/latest/extensions/hooks.html)

在实现自己的扩展程序时，最简单的方式也是继承 `DefaultCommunicationHandler` 父类，该类对各钩子与回调函数的绑定进行了封装，并进一步封装了回调函数涉及到的参数数据结构，以方便快速上手使用。



### 进阶开发

如果对 Java 扩展程序的可控性要求更高，`DefaultCommunicationHandler` 类已无法满足需求时，可以通过实现 `CommunicationHandler` 接口，从更底层控制代码逻辑，编写更灵活的扩展程序。

```
package emqx.extension.java.handler;

public interface CommunicationHandler {
    
    public Object init();
    
    public void deinit();
}
```

- `init()` 方法：用于初始化，声明扩展需要挂载哪些钩子，以及挂载的配置
- `deinit()` 方法：用于注销。

详细数据格式说明，参见 [设计文档](https://github.com/emqx/emqx-exhook/blob/master/docs/design.md)。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
