From v4.1, [EMQX MQTT broker](https://www.emqx.com/en/products/emqx) provides the specified plugin that supports multiple languages [emqx_extension_hook](https://github.com/emqx/emqx-extension-hook). Currently, it is supported that use other programming languages to process the hook events of EMQX. The developer can use Python or Java to quickly develop their plugins or do some expansions based on the official functions to satisfy their business scenarios. For example:

- Verify the client's login permission: when connecting to the client, the corresponding function will be triggered and the client information will be obtained through parameters. Finally, it judges whether it has login permission after reading the database, comparison, etc.
- Record the online status of client and online and offline history: trigger corresponding functions when the status of the client changes, the client information will be obtained through parameters, and the online status of the client in the database will be rewritten.
- Verify the operation permission for [PUB/SUB](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) of the client: trigger corresponding functions when publish or subscribe, and the client information and current topics will be obtained through parameters to judge whether it has the corresponding operation permission.
- Handle session and message events, implement the subscription relation and message processing or storage: trigger corresponding functions when publishing messages and status changes, the current client information, information status and message content will be forwarded to Kafka or database for storage.

>  Note：the message hook is only supported in the enterprise.



Python and Java drivers are based on the processes [Erlang/OTP-Port](https://erlang.org/doc/tutorial/c_port.html) to implement communication, and have very high throughput performance. This article will take Java expansion as an example to introduce how to use EMQX cross-language expansion.

![upeb67488ae758908b02ac8567c37fcf2d0a9.png](https://assets.emqx.com/images/6a850a46211aa6f3c85cdab9bb2d8d77.png)



## The example of using Java expansions

### Requirements

- The broker of EMQX is required to install JDK 1.8 or higher version

### Begin

1. Create a Java project
2. Download file [io.emqx.extension.jar](https://github.com/emqx/emqx-extension-java-sdk/releases) and [erlport.jar](https://github.com/emqx/emqx-extension-java-sdk/tree/master/deps)
3. Add SDK `io.emqx.extension.jar` and `erlport.jar` to the dependency of the project
4. Copy `examples/SampleHandler.java` to your project
5. Write business code according to the example of SDK `SampleHandler.java` to ensure successfully compile.

### Deployment

You need to deploy `sdk` and code files into EMQX after compiling all the source code.

1. Copy `io.emqx.extension.jar` into `emqx/data/extension` directory
2. Copy the compiled `.class` file, such as `SampleHandler.class` into `emqx/data/extension` directory
3. Modify the configuration file `emqx/etc/plugins/emqx_extension_hook.conf`:

```bash
exhook.drivers = java
## Search path for scripts or library
exhook.drivers.java.path = data/extension/
exhook.drivers.java.init_module = SampleHandler
```

Enable plugin `emqx_extension_hook`. If configuration error or write wrong Java code, it can not be enabled normally.  After it is enabled, try to establish the MQTT connection and observer the running situation of the business.



### Example

The example of the program [Main.java](https://github.com/emqx/emqx-extension-hook/blob/master/test/scripts) is as follows. This program inherits the class `DefaultCommunicationHandler` of the SDK. This code example demonstrates how to mount all hooks of the EMQX system.

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

    // Determine the authentication result, return true or false 
    @Override
    public boolean onClientAuthenticate(ClientInfo clientInfo, boolean authresult) {
        System.err.printf("[Java] onClientAuthenticate: clientinfo: %s, authresult: %s\n", clientInfo, authresult);

        return true;
    }

    // Determine the ACL check result, return true or false
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

`SampleHandler` mainly includes two sections:

1. Override the method `getActionOption`. This method configures hooks related to Message and specifies the list of topics that need to be in effect.

   | Configuration items      | Corresponding hook |
   | ------------------------ | ------------------ |
   | MESSAGE_PUBLISH_TOPICS   | message_publish    |
   | MESSAGE_DELIVERED_TOPICS | message_delivered  |
   | MESSAGE_ACKED_TOPICS     | message_acked      |
   | MESSAGE_DROPPED_TOPICS   | message_dropped    |

2. Override the method `on<hookName>`. These methods are the callback function to deal with hook events. The method how to name function is that add the prefix `on` in the front of each variant hook name. The way of variant is that use CamelCase after removing the underline of the hook name, for example, the hook client_connect corresponds function name onClientConnect. The events that are generated by EMQX such as: connect, publish, subscribe, etc, will finally be distributed to the callback function of these hook events. Next, the callback function can operate every attribute and status. The program example only prints each parameter. If you only care about partly hook events, only need to override the callback function of this part hook events instead of overriding all the callback functions.

The timing of executing each callback function and the list of supported hooks are the same as the build-in hooks of EMQX, please refer to [Hooks - EMQX](https://docs.emqx.io/broker/latest/en/advanced/hooks.html#hookpoint).

The simplest method is inheriting the superclass `DefaultCommunicationHandler`, when you implement your expansion programs. This superclass wraps the binding of each hook and callback function, and further wraps the parameter data structure involved in the callback function to facilitate a quick start.

### Advanced development

If you have higher requirements for the controllability of Java extensions and the class `DefaultCommunicationHandler` can not satisfy your requirements, you can control code logic from a lower layer through implementing interface `CommunicationHandler`.

```
package emqx.extension.java.handler;

public interface CommunicationHandler {
    
    public Object init();
    
    public void deinit();
}
```

- Method `init()`: for initialization, declaring which hooks are required in the extension, and the configuration of mounting
- Method `deinit()`: for logout

For the detailed introduction of data format, please refer to [the design documentation](https://github.com/emqx/emqx-extension-hook/blob/master/docs/design.md).


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
