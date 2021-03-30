
From v4.1, EMQ X [MQTT broker](https://www.emqx.io/cn/products/broker) provides the specified plugin that supports multiple languages [emqx_extension_hook](https://github.com/emqx/emqx-extension-hook). Currently, it is supported that use other programming languages to process the hook events of EMQ X. The developer can use Python or Java to quickly develop their plugins or do some expansions based on the official functions to satisfy their business scenarios. For example:

- Verify the client's login permission: when connecting to the client, the corresponding function will be triggered and the client information will be obtained through parameters. Finally, it judges whether it has the login permission after reading the database, comparison, etc.
- Record the online status of client and online and offline history: trigger corresponding functions when the status of the client changes, the client information will be obtained through parameters, and the online status of the client in the database will be rewritten.
- Verify the operation permission for PUB/SUB of the client: trigger corresponding functions when publish or subscribe, and the client information and current topics will be obtained through parameters to judge whether it has the corresponding operation permission.
- Handle session and message events, implement the subscription relation and message processing or storage: trigger corresponding functions when publish messages and status changes, the current client information, information status and message content will be forwarded to Kafka or database for storage.

>  Note：the message hook is only supported in the enterprise.



Python and Java drivers are based on the processes [Erlang/OTP-Port](https://erlang.org/doc/tutorial/c_port.html) to implement communication, and have very high throughput performance. This article will take Python expansion as an example to introduce how to use EMQ X cross-language expansion.

![upeb67488ae758908b02ac8567c37fcf2d0a9.png](https://static.emqx.net/images/81aa1ab1028f0e59c08b0a00dc5ade08.png)



## The example of using Python expansions

### Requirements

- The broker of EMQ X is required to install Python 3.6 or higher version

### Steps for usage

1. Install [Python SDK](https://pypi.org/project/emqx-extension-sdk/) through pip
2. Adjust EMQ X configurations to ensure that the corresponding configuration items correctly point Python project
3. Import SDK to write code



### Install Python plugins

Install SDK locally through pip commands and **ensure using pip3 to install**:

```bash
pip3 install emqx-extension-sdk
```



### Modify configuration

Modify the configuration of plugin ` emqx-extension-hook` and correctly use expansion.

```bash
## Setup the supported drivers
##
## Value: python2 | python3 | java
exhook.drivers = python3

## Search path for scripts/library
exhook.drivers.python3.path = data/extension/hooks.py

## Call timeout
##
## Value: Duration
##exhook.drivers.python3.call_timeout = 5s

## Initial module name
## Your filename or module name
exhook.drivers.python3.init_module = hooks
```



### Write code

Create file `hooks.py` in the directory `emqx/data/extension` and imporrt SDK to write business logic. The example is as follows.

```python
## data/extension/hooks.py

from emqx_extension.hooks import EmqxHookSdk, hooks_handler
from emqx_extension.types import EMQX_CLIENTINFO_PARSE_T, EMQX_MESSAGE_PARSE_T


# inherit SDK class HookSdk 
class CustomHook(EmqxHookSdk):

  	# use decorator to register hooks
    @hooks_handler()
    def on_client_connect(self,
                          conninfo: EMQX_CLIENTINFO_PARSE_T = None,
                          props: dict = None,
                          state: list = None):
        print(f'[Python SDK] [on_client_connect] {conninfo.clientid} connecte')

    @hooks_handler()
    def on_client_connected(self,
                            clientinfo: EMQX_CLIENTINFO_PARSE_T,
                            state: list = None):
        print(
            f'[Python SDK] [on_client_connected] {clientinfo.clientid} connected')

    @hooks_handler()
    def on_client_check_acl(self, clientinfo: EMQX_CLIENTINFO_PARSE_T,
                            pubsub: str,
                            topic: str,
                            result: bool,
                            state: tuple) -> bool:
        print(
            f'[Python SDK] [on_client_check_acl] {clientinfo.username} check ACL: {pubsub} {topic}')
        # when the username is empty, ACL verification failed
        if clientinfo.username == '':
            return False
        return True

    @hooks_handler()
    def on_client_authenticate(self, clientinfo: EMQX_CLIENTINFO_PARSE_T, authresult,
                               state) -> bool:
        print(
            f'[Python SDK] [on_client_authenticate] {clientinfo.clientid} authenticate')
        # when the clientid is not empty, verification passed
        if clientinfo.clientid != '':
            return True
        return False

    # on_message_* only supports the enterprise
    @hooks_handler()
    def on_message_publish(self, message: EMQX_MESSAGE_PARSE_T, state):
        print(
            f'[Python SDK] [on_message_publish] {message.topic} {message.payload}')


emqx_hook = CustomHook(hook_module=f'{__name__}.emqx_hook')


def init():
    return emqx_hook.start()


def deinit():
    return
```



### Enable

Enable plugin `emqx_extension_hook`. If configuration error or write wrong Python code, it can not be enabled normally.  After it is enabled, try to establish the [MQTT](https://www.emqx.io/mqtt) connection and observer the running situation of the business.

```bash
./bin/emqx_ctl plugins load emqx_extension_hook
```



## Advanced development

Currently, the EMQ X Python extension SDK is open source, if you have higher requirements for the controllability and performance or you need to use the running environment of Python 2.7, welcome to contribute code or develop based on original examples.

- Code repository: [emqx-extension-python-sdk](https://github.com/emqx/emqx-extension-python-sdk)
- You can refer to this example to wrap: [emqx-extension-hook main.py](https://github.com/emqx/emqx-extension-hook/blob/master/test/scripts/main.py)

