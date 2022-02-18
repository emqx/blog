从 v4.1 版本开始，EMQX [MQTT 服务器](https://www.emqx.com/zh/products/emqx) 提供了专门的多语言支持插件 [emqx_extension_hook](https://github.com/emqx/emqx-extension-hook) ，现已支持使用其他编程语言来处理 EMQX 中的钩子事件，开发者可以使用 Python 或者 Java 快速开发自己的插件，在官方功能的基础上进行扩展，满足自己的业务场景。例如：

- 验证某客户端的登录权限：客户端连接时触发对应函数，通过参数获取客户端信息后通过读取数据库、比对等操作判定是否有登录权限
- 记录客户端在线状态与上下线历史：客户端状态变动时触发对应函数，通过参数获取客户端信息，改写数据库中客户端在线状态
- 校验某客户端的 PUB/SUB 的操作权限：发布/订阅时触发对应函数，通过参数获取客户端信息与当前主题，判定客户端是否有对应的操作权限
- 处理会话 (Sessions) 和 消息 (Message) 事件，实现订阅关系与消息处理/存储：消息发布、状态变动时触发对应函数，获取当前客户端信息、消息状态与消息内容，转发到 Kafka 或数据库进行存储。

>  注：消息(Message) 类钩子，仅在企业版中支持。



Python 和 Java 驱动基于 [Erlang/OTP-Port](https://erlang.org/doc/tutorial/c_port.html) 进程间通信实现，本身具有非常高的吞吐性能，本文以 Python 扩展为例介绍 EMQX 跨语言扩展使用方式。

![upeb67488ae758908b02ac8567c37fcf2d0a9.png](https://static.emqx.net/images/c8e437088e4eee7e6947823a407ddd51.png)


## Python 扩展使用示例



该示例在 EMQX Broker v4.1.x 中使用。如果在更高的 EMQX 版本中使用该示例，请检查 EMQX Broker 的发布日志，确保是否存在兼容性的改动。

### 要求

- EMQX 所在服务器需安装 Python 3.6 以上版本
- 可执行的命令 `python3`

### 使用步骤

1. 验证 Python 环境
2. 通过 pip 安装 [Python SDK](https://pypi.org/project/emqx-extension-sdk/)
3. 调整 EMQX 配置，确保相关配置项正确指向 Python 项目
4. 引入 SDK 编写代码



### 验证 Python 环境

打开终端执行 `python3 --version` 检查版本是否符合要求。



> 注：在 Windows 中，不能使用 MSYS64 提供的 Python 环境（它会造成 Erlang 无法正确的设置其所需要的环境变量）



### Python SDK 安装

通过 pip 命令在本地安装 SDK，**确保使用 pip3 进行安装**：

```bash
pip3 install emqx-extension-sdk
```



### 修改配置

修改 ` emqx-extension-hook` 插件配置，正确使用扩展：

```bash
## Setup the supported drivers
##
## Value: python3 | java
exhook.drivers = python3

## Search path for scripts/library
exhook.drivers.python3.path = data/extension/

## Call timeout
##
## Value: Duration
##exhook.drivers.python3.call_timeout = 5s

## Initial module name
## Your filename or module name
exhook.drivers.python3.init_module = hooks
```



### 编写代码

在 `emqx/data/extension` 目录下新建 `hooks.py` 文件，引入 SDK 编写业务逻辑，示例程序如下：

```python
## data/extension/hooks.py

from emqx_extension.hooks import EmqxHookSdk, hooks_handler
from emqx_extension.types import EMQX_CLIENTINFO_PARSE_T, EMQX_MESSAGE_PARSE_T


# 继承 SDK HookSdk 类
class CustomHook(EmqxHookSdk):

      # 使用装饰器注册 hooks
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
        # 用户名为空时，ACL 验证不通过
        if clientinfo.username == '':
            return False
        return True

    @hooks_handler()
    def on_client_authenticate(self, clientinfo: EMQX_CLIENTINFO_PARSE_T, authresult,
                               state) -> bool:
        print(
            f'[Python SDK] [on_client_authenticate] {clientinfo.clientid} authenticate')
        # clientid 不为空时，验证通过
        if clientinfo.clientid != '':
            return True
        return False

    # on_message_* 仅支持企业版
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



### 启动

启动 `emqx_extension_hook` 插件，如果配置错误或代码编写错误将无法正常启动。启动后尝试建立 [MQTT](https://www.emqx.com/zh/mqtt) 连接并观察业务运行情况。



```bash
./bin/emqx_ctl plugins load emqx_extension_hook
```



## 进阶开发

目前 EMQX Python  扩展  SDK 是开源的，如果对可控性、性能要求更高，或需要使用 Python 2.7 版本的运行环境，欢迎贡献代码或基于原始示例进行开发：

- 代码仓库：[emqx-extension-python-sdk](https://github.com/emqx/emqx-extension-python-sdk)
- Python 原始示例，可使用该示例自行封装：[emqx-extension-hook main.py](https://github.com/emqx/emqx-extension-hook/blob/v4.1.1/test/scripts/main.py)
