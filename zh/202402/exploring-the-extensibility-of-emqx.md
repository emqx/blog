EMQX 具有卓越的可扩展性、出色的吞吐量和极低的延迟，同时还配备一个直观且现代的 Dashboard 与这些特性和功能相辅相成，使其成为许多物联网开发者的首选。

今天我们则要深入探讨 EMQX 另一个同样关键但可能被忽视的方面：可扩展性。我们将深入了解插件机制——这是 EMQX 从诞生之初就具备的一个特性，经过多个版本的迭代优化后，它 EMQX 5.x 版本中变得更加完善。

在本文中，我们将探讨：

- **EMQX 插件的核心：**要想深入探索插件的世界，首先要了解它们的基本原理。
- **构建插件：**我们将用一个实际的例子，逐步演示如何为 EMQX 5.x 定制一个插件。
- **安装和运行插件：**了解如何在一个运行中的 EMQX 集群中无缝地集成和运行插件。
- **操作技巧：**不借助 EMQX Dashboard 用户界面或 CLI，直接从文件中安装插件的方法。
- **调试技巧：**缩短编译、部署和测试周期的策略。

## **EMQX 插件揭秘**

EMQX 插件本质上是 Erlang 应用程序。它们的工作方式是向 EMQX 的核心应用程序 `emqx` 注册（Hook）特定的回调函数。这些回调函数会在某些事件发生前后被触发。

需要明白的是，回调函数并不只是用于第三方插件的集成。实际上，EMQX 的许多内置功能（比如认证、授权和数据集成）都是基于这些回调函数来实现的。在 5.x 版本之前，这些功能被称为原生插件。

### **Hook 回调函数的实质**

在 EMQX 的世界里，每个客户端都对应一个独立的 Erlang 进程。这个进程负责处理连接、会话或消息的各种生命周期事件，并触发相应的 Hook 回调函数。这种架构设计使得数百万客户端能够并发运行。这也意味着一个回调函数会被同时执行，因此，建议在设计回调时避免使用竞争资源。

### **Hook 回调函数的注册**

当一个插件应用启动时，它会通过 EMQX 的 API 在指定的 Hook 点注册回调函数。这些注册信息会保存在一个 `ets` 表（名为 `emqx_hooks`）中。

但是，这种关联并不是永久的。当插件应用关闭时，应该及时注销回调函数。

### **三大支柱：Hook 点**

一般来说，有三类事件会触发回调函数：

1. **客户端事件：**它们涉及到 MQTT 连接生命周期的各个阶段。比如，当收到一个 CONNECT 包时，就会激活与 `client.connect` Hook 点相对应的回调函数。
2. **会话事件：**它们包括 MQTT 会话生命周期从开始到结束的各个阶段。
3. **消息事件：**它们涵盖 MQTT 消息传递的全过程，例如当一个 PUBLISH 包到达或者向客户端发送一个 PUBACK 时。

截至目前，我们向开发者们提供了 20 个不同的 Hook 点。

## 一个简单的示例：创建我们的第一个插件

在这个示例中，我们将尝试创建一个插件，它可以用一个特殊的规则来增强 EMQX 的访问控制：客户端只能订阅与模式 `msg/{{user-id}}/whatever` 相匹配的主题，其中 `{{user-id}}` 是从 MQTT 客户端 ID 中截取出来的。

在我们开始之前，有必要提一下，EMQX 有很多内置的访问控制（授权）解决方案，因此通常没有必要再开发一个插件。

例如，如果需求是允许客户端订阅以其客户端 ID 为前缀的任意主题，那么内置的基于文件的 ACL 规则就可以满足，只需在 `acl.conf` 的开头添加 `{allow, all, subscribe, ["msg/${clientid}/#"]}.` 即可。

但是，在这个示例中，我们需要从客户端 ID 的一部分（而不是整个客户端 ID）中截取 user-id，这是目前内置功能无法实现的。

### 准备：安装 Erlang/OTP

本文基于 EMQX 5.1 版本，该版本已在 Erlang/OTP 25 上正式发布。可以在这里阅读更多相关信息：https://github.com/emqx/emqx/blob/master/README.md#build-from-source

您也可以在更新版本的 Erlang/OTP 上编译 EMQX，但如果想把插件加载到 EMQX 的官方发行包中，那么就不能用更新的 Erlang/OTP 来构建插件。

### 第 1 步：从模板生成框架代码

EMQX 提供了一个 rebar3 模板，可以用来生成插件的框架代码。具体步骤如下。

- 在 `~/.config/rebar3/templates(模板)` 目录安装插件

  ```
  $ mkdir -p ~/.config/rebar3/templates
  $ cd ~/.config/rebar3/templates
  $ git clone https://github.com/emqx/emqx-plugin-template.git
  ```

- 生成框架模块

  ```
  $ cd /path/to/my/project
  $ rebar3 new emqx-plugin emqx_simple_acl
  ```

生成后的插件项目结构如下：

```
tree emqx_simple_acl/
emqx_simple_acl/
├── erlang_ls.config
├── get-rebar3
├── LICENSE
├── Makefile
├── priv
│   └── config.hocon
├── README.md
├── rebar.config
├── rebar.lock
└── src
    ├── emqx_simple_acl_app.erl
    ├── emqx_simple_acl.app.src
    ├── emqx_simple_acl_cli.erl
    ├── emqx_simple_acl.erl
    └── emqx_simple_acl_sup.erl
```

### 第 2 步：修改生成的代码

框架代码包含了所有可用的 Hook 点，并在每个回调函数中输出调试信息。由于我们只需要使用 `client.subscribe` Hook 点，所以可以直接删除其他多余的代码。

删除后，模块 `emqx_simple_acl.erl` 的内容如下：

```
-module(emqx_simple_acl).

-include_lib("emqx/include/emqx.hrl").
-include_lib("emqx/include/emqx_hooks.hrl").
-include_lib("emqx/include/logger.hrl").

-export([ load/1
        , unload/0
        ]).

-export([ on_client_subscribe/4 ]).

load(Env) ->
    hook('client.subscribe',    {?MODULE, on_client_subscribe, [Env]}).

unload() ->
    unhook('client.subscribe',    {?MODULE, on_client_subscribe}).

on_client_subscribe(#{clientid := ClientId}, _Properties, TopicFilters, _Env) ->
    io:format("Client(~s) will subscribe: ~p~n", [ClientId, TopicFilters]),
    {ok, TopicFilters}.

hook(HookPoint, MFA) ->
    emqx_hooks:add(HookPoint, MFA, _Property = ?HP_HIGHEST).

unhook(HookPoint, MFA) ->
    emqx_hooks:del(HookPoint, MFA).
```

除了修改代码，还需要更新以下位置的描述文本：

- `src/emqx_simple_acl.app.src` 文件中的 `description` 字段。这个字段用来描述 Erlang 应用程序的功能和特点。
- `README.md` 文件的内容。这个文件清晰地说明了插件的作用、用法和维护方式等信息。
- `rebar.confg` 文件中的 `emqx_plugrel` 部分。这部分提供了插件的程序包信息，这些信息会在 CLI 输出和仪表板上显示给用户。下面是一个示例：

```
%% 插件的其他信息
{emqx_plugrel,
    [ {authors, ["Zaiming (stone) Shi"]}
    , {builder,
        [ {name, "zmstone"}
        , {contact, "contact@emqx.com"}
        , {website, "http://emqx.com"}
        ]}
    , {repo, "https://github.com/zmstone/emqx_simple_acl"}
    , {functionality, ["Demo"]}
    , {compatibility,
        [ {emqx, "~> 5.0"}
        ]}
    , {description, "My simple ACL."}
    ]
}.
```

### 第 3 步：实现规则

我们需要修改的是 `on_client_subscribe` 回调函数，它在 EMQX 接受订阅并在系统中注册它们之前执行。

我们要实现的功能可以概括为：

- Parse `ClientId` (which is a binary string), to get user ID.
- Filter the `TopicFilters` list, drop the ones that do not match the pattern `msg/{{user-id}}/#`
- 从 `ClientId`（二进制字符串）中提取用户 ID。
- 筛选 `TopicFilters` 列表，删除不符合 `msg/{{user-id}}/#` 模式的项。

假设客户端 ID 的格式是 `{{region}}-{{type}}-{{user-id}}`，我们需要截取由破折号分隔的字符串的最后一部分。具体实现如下：

```
on_client_subscribe(#{clientid := ClientId}, _Properties, Subscriptions, _Env) ->
    io:format("Client(~s) will subscribe: ~0p~n", [ClientId, topics(Subscriptions)]),
    case parse_client_id_for_user_id(ClientId) of
        {ok, UserId} ->
            Allowed = lists:filter(fun(S) -> is_valid_subscription(UserId, S) end, Subscriptions),
            io:format("Client(~s) is allowed to subscribe: ~0p~n", [ClientId, topics(Allowed)]),
            {ok, Allowed};
        {error, invalid_clientid} ->
            io:format("Client(~s) is not allowed to subscribe to any topics~n", [ClientId]),
      %% 此处返回空列表表示没有订阅任何主题
            {ok, []}
    end.

%% 获取模式 {{region}}-{type}}-{user-id}} 的客户端 ID，
%% 并返回 {{user-id}}。
%% 如果客户端 ID 与此模式不匹配，
%% 我们就认为它不是一个有效的客户端，不允许它订阅任何主题。
parse_client_id_for_user_id(ClientId) ->
    case binary:split(ClientId, <<"-">>, [global]) of
        [_Region, _Type, UserId] when UserId =/= <<>> ->
            {ok, UserId};
        _ ->
            {error, invalid_clientid}
    end.

%% 检查主题是否以 "msg/{{userid}}/" 开头
is_valid_subscription(UserId, {Topic, _SubOpts}) ->
    Size = size(UserId),
    case Topic of
        <<"msg/", UserId:Size/binary, "/", _/binary>> ->
            true;
        _ ->
            false
    end.

%% 订阅是一个包含 {主题、订阅选项} 的列表。
topics(Subs) ->
    lists:map(fun({T, _SubOpts}) -> T end, Subs).
```

### 第 4 步：构建插件

执行命令 `make rel` 即可生成一个插件包，文件名为 `_build/default/emqx_plugrel/emqx_simple_acl-1.0.0.tar.gz`。

## 安装和运行插件

您可以运行 `emqx ctl plugins` 命令来管理插件，但是一个更直接的方法是在仪表板用户界面中管理它。

我们可以用下列命令启动 EMQX：`docker run --name emqx -it --rm -p 18083:18083 -p 1883:1883 emqx/emqx:5.1.5`

然后在端口 18083 打开仪表板，用 `admin` `public` 登录（第一次登录时，需要修改密码）。您应该能在“管理”分组下找到“插件”菜单。点击右上角的“+ 安装插件”按钮，就会跳转到一个上传页面。

![上传插件页面](https://assets.emqx.com/images/eec61d74f56f522134eba525c564af02.png)

安装完成后，应该能在插件列表中看到它，它的初始状态是“未激活”。

![插件安装完成](https://assets.emqx.com/images/ad21d439e3bcf0a6420e9f797190c2a9.png)

在我们启动它之前，让我们先检查一下。点击它的名称，就能看到这个插件的所有信息。

描述文本是从 `README.md` 和 `rebar.config` 文件中获取的。

![插件信息](https://assets.emqx.com/images/906a0eb3cee89b669dc200a0f3d1d4c8.png)

现在我们可以点击“启动”按钮来启动它，会看到插件变成了“激活”状态。

我们也可以用 CLI 来检查它：`docker exec -it emqx bash -c 'emqx ctl plugins list'`

```
[
  {
    "running_status" : "running",
    "repo" : "https://github.com/zmstone/emqx_simple_acl",
    "rel_vsn" : "1.0.0",
    "rel_apps" : [
      "emqx_simple_acl-0.1.0",
      "map_sets-1.1.0"
    ],
    "name" : "emqx_simple_acl",
    "metadata_vsn" : "0.1.0",
    "git_ref" : "unknown",
    "functionality" : [
      "Demo"
    ],
    "description" : "My simple ACL.",
    "date" : "2023-08-30",
    "config_status" : "enabled",
    "compatibility" : {
      "emqx" : "~> 5.0"
    },
    "built_on_otp_release" : "25",
    "builder" : {
      "website" : "http://emqx.com",
      "name" : "zmstone",
      "contact" : "contact@emqx.com"
    },
    "authors" : [
      "Zaiming (Stone) Shi"
    ]
  }
]
```

## 验证插件

首先，我们来看看插件是否已经成功地在 `emqx_hooks` 表中注册了回调函数。

通过连接到 EMQX 的远程控制台，我们可以像下面这样查看所有的 Hook：

```
$ docker exec -it emqx bash -c 'emqx remote_console'
Erlang/OTP 25 [erts-13.2.2] [emqx] [64-bit] [smp:20:20] [ds:20:20:10] [async-threads:1] [jit:ns]

Restricted Eshell V13.2.2  (abort with ^G)
v5.1.5-build.3(emqx@172.17.0.2)1> rr(emqx_hooks).
[callback,hook]
v5.1.5-build.3(emqx@172.17.0.2)2> ets:tab2list(emqx_hooks).
[...
#hook{name = 'client.subscribe',
       callbacks = [#callback{action = {emqx_simple_acl,on_client_subscribe,
                                                        [[]]},
                              filter = undefined,priority = 1000}]},
...
]
```

接下来，我们尝试连接一个 [MQTT 客户端](https://www.emqx.com/en/blog/mqtt-client-tools)来测试插件是否按照预期运行。

我们将在测试中使用 [MQTTX 命令行工具](https://mqttx.app/cli)。

如果我们使用客户端 ID `region1-type1-user1` 连接，然后订阅 `msg/user1/#`，如下所示：

```
mqttx sub -h localhost -p 1883 -i region1-type1-user1 -t msg/user1/#
```

我们应该能够在仪表板上看到该订阅，如下图所示：

![仪表板上看到该订阅](https://assets.emqx.com/images/88e46171e98b73075feeedc35f52305f.png)

同时，在 docker 控制台上也可以看到调试输出，如下所示：

```
Client(region1-type1-user1) will subscribe: [<<"msg/user1/#">>]
Client(region1-type1-user1) is allowed to subscribe: [<<"msg/user1/#">>]
```

如果我们使用一个错误的主题模式测试，比如 `$ mqttx sub -h localhost -p 1883 -i region1-type1-user1 -t msg/userX/0`，我们将看到如下日志。

```
Client(region1-type1-user1) will subscribe: [<<"msg/userX/0">>]
Client(region1-type1-user1) is allowed to subscribe: []
```

如果我们使用一个不符合 `{{region}}-{{type}}-{{user-id}}` 模式的客户端 ID 连接，比如 `$ mqttx sub -h localhost -p 1883 -i user1 -t msg/user1/0`，那么客户端将无法订阅任何主题。

```
Client(user1) will subscribe: [<<"msg/user1/0">>]
Client(user1) is not allowed to subscribe to any topics
```

## 操作技巧

我们已经了解到 EMQX 把插件识别为 `.tar.gz` 格式的压缩包。您可以通过仪表板界面或 CLI 来查看这些插件的状态（是否激活、停用等）。但是，对于喜欢自动化的系统管理员，还有一些不明确的地方：

- EMQX 把上传的压缩包保存在哪里？
- EMQX 如何管理每个插件的状态？

一旦我们弄清楚这些问题，自动化过程就会变得更加顺畅。

### 插件包解压

正如许多人所见，EMQX v5 插件实际上是 `.tar.gz` 格式的文件，其内容与普通的 Erlang 应用程序没有太大区别。EMQX 将这个压缩包解压到插件目录中。例如：

```
docker exec -it emqx bash -c 'ls /opt/emqx/plugins/emqx_simple_acl-1.0.0/'
README.md  emqx_simple_acl-0.1.0  map_sets-1.1.0  release.json
```

### 插件状态存储

通过 `docker exec -it emqx bash -c 'cat /opt/emqx/data/configs/cluster.hocon'` 查看集群的配置文件，内容如下：

```
plugins {
  install_dir = plugins
  states = [
    {
      enable = true
      name_vsn = emqx_simple_acl-1.0.0
    }
  ]
}
```

每个安装的插件都会把自己的状态保存在 `plugins.states` 数组中。这种数组格式保证了插件的加载和初始化顺序是一致的。

要在 EMQX 节点启动之前预设插件的状态，可以通过与 `etc/emqx.conf` 文件结合来实现状态存储。对于 Docker 用户而言，这表示可以从主机挂载，或者使用 Kubernetes 的 ConfigMap。但是，请注意，当在 Docker 中操作时，数据目录充当 Docker 卷。务必确保 `cluster.hocon` 文件对 EMQX 是可写的，以允许存储实时的、集群同步的配置更改。因此，请避免直接挂载 `cluster.hocon` 文件。

## 调试技巧

如果您需要频繁地重新构建程序包、上传并重启插件，那么使用 EMQX 进行集成测试就会很麻烦。

这时，EMQX 的热补丁机制就派上用场了。

修改了 `emqx_simple_acl.erl` 模块后，使用 `make` 命令可以重新编译代码。新编译的代码会被保存到 `_build/default/lib/emqx_simple_acl/ebin/emqx_simple_acl.beam`。

可以使用下面的命令，无需重启 EMQX 就可以加载新的 beam 文件：

```
docker cp _build/default/lib/emqx_simple_acl/ebin/emqx_simple_acl.beam emqx:/opt/emqx/plugins/emqx_simple_acl-1.0.0/emqx_simple_acl-0.1.0/ebin/
docker exec -it emqx bash -c 'emqx eval "c:lm()."'
```

成功更新 beam 文件后，应该显示 `[{module,emqx_simple_acl}]`。

## 结语

EMQX 是一个强大的平台，它不仅拥有丰富的内置功能，还能通过其灵活的插件系统进行定制化扩展。本文向读者介绍了 EMQX 插件的基本概念，从插件的核心原理到如何亲自动手开发一个适用于 EMQX 5.x 的插件。我们还探讨了在 EMQX 环境中集成和使用插件的便捷方法。对于那些追求高效工作方式的用户，我们的操作技巧提供了一些绕过传统 UI 或 CLI 的方式，而我们的调试策略旨在缩短开发周期。无论您是资深开发者还是 EMQX 新手，这些信息都将帮助您充分发挥 EMQX 插件生态系统的优势。

示例代码已发布到 GitHub 仓库：[zmstone/emqx_simple_acl](https://github.com/zmstone/emqx_simple_acl)

您可以在 [EMQX 官方文档的 v5 插件部分](https://docs.emqx.com/en/enterprise/v5.1/extensions/plugins.html)找到更简明的示例。

关于 Hook 的更详细信息，请浏览：[https://docs.emqx.com/en/enterprise/v5.1/extensions/hooks.html](https://docs.emqx.com/en/enterprise/v5.1/extensions/hooks.html)。

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
