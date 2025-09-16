## **引言**

在物联网项目中，您是否也遇到过这样的困扰：设备突然离线，运维团队却未能及时察觉，导致业务中断或响应延迟……

**设备状态的实时变化直接关系到系统的稳定性和用户体验。**

[EMQX Platform](https://www.emqx.com/zh/platform) 作为企业级 MQTT 与 AI 一体化平台，借助强大的内置规则引擎，可实时捕获设备上下线等事件，并无缝对接钉钉、飞书、企业微信等即时通讯工具，实现自动化告警与通知。

**本文将以客户端异常离线事件为例，详细介绍如何利用 EMQX 规则引擎，实时捕捉设备离线状态，并将相关信息自动推送到企业微信、钉钉或飞书等办公协作平台，确保团队能够及时感知并处理设备异常。**

同时，读者也可以参考本文的方法，轻松应用于客户端上线提醒、消息投递失败告警、系统资源异常监控等其他事件场景，构建一套灵活、可靠的事件响应与通知体系。

## **方案概览**

本方案基于 EMQX 内置的规则引擎（Rule Engine）功能，通过对客户端离线事件进行筛选与处理，并借助 HTTP 转发将关键信息实时推送到群聊机器人，从而实现零编码的自动化告警。

![image.png](https://assets.emqx.com/images/a5ab210747eed8e192b845145bfde622.png)

### 方案亮点

- **零代码实现**：全程通过 EMQX Dashboard 配置完成，无需后端开发。
- **实时响应**：基于事件触发，毫秒级响应。
- **多平台支持**：适配企业微信、钉钉、飞书等多个主流协作工具，并支持同时推送。
- **高度可扩展**：除客户端离线告警，还可以用于上线通知、消息投递失败、订阅变动等多种事件类型。

### 核心思路

- **监听设备事件：**通过 EMQX 规则引擎订阅 `$events/...` 主题，如 `$events/client/disconnected`，捕获客户端离线信息。
- **数据筛选与加工：**使用 SQL 对特定的事件数据进行过滤，提取 `clientid`、`username`、 `reason`、`时间戳`等关键字段，并通过动作模板构造推送所需的告警信息。
- **推送到群聊机器人：**在企业微信、钉钉、飞书等平台中创建自定义机器人，通过 Webhook URL 接收 EMQX 发送的 HTTP 请求，实现告警信息的实时推送。

### **环境要求**

- **版本：**本文示例基于 EMQX v5.10 版本
- **网络：**允许 EMQX 访问钉钉与飞书的公网 Webhook API
- **权限：**需要 EMQX Dashboard 管理员权限

### **平台要求**

- 有权在企业微信、钉钉、飞书群聊中创建自定义机器人
- 有权获取机器人消息推送所需的 Webhook URL

## 功能支持

### **规则引擎**

规则引擎是 EMQX 内置的基于 SQL 的数据处理组件，专为物联网场景设计，能够高效、低成本地实现实时数据流转与处理。

规则通过内置事件触发机制和丰富的处理函数，无需编写额外代码，即可完成一站式的 IoT 数据提取、过滤、转换与处理，并轻松将结果发送到外部数据系统中。

![image.png](https://assets.emqx.com/images/9b98c8daaafdf081e9daef88f49a1bca.png)

EMQX 规则引擎的主要功能包括：

- **事件驱动**：支持处理 10 余种 EMQX 内置事件，包括 EMQX 告警，客户端上线、离线、消息发布等。
- **数据筛选**：通过 SQL-like 语法编写规则，筛选和处理事件数据。
- **数据处理**：内置丰富的函数和 SQL 语法支持，实现灵活数据处理需求。
- **数据转发**：支持将处理后的数据发送到 Kafka、数据库、HTTP 等目标。
- **可视化配置**：通过 Dashboard 图形界面完成配置，无需额外开发。

详细功能介绍和使用方法请参考：[规则引擎 | EMQX 文档](https://docs.emqx.com/zh/emqx/latest/data-integration/rules.html) 

### 客户端事件

EMQX 规则引擎事件是指在 EMQX 运行过程中，系统或客户端产生的、可被规则引擎捕获的特定行为或状态变化。当这些事件发生时（如客户端连接、断开、消息发布等），规则引擎会根据预设规则自动执行相应的处理逻辑。

每个事件都有详细的关联的上下文信息，这些信息通常包括事件发生的时间、涉及的客户端标识、消息的具体内容、消息所属的主题、客户端的连接状态等详细数据。

通过事件下文信息，可用于实现多样化的业务需求。例如：对消息进行过滤与转发，只将符合特定条件的消息发送到指定的下游系统；对设备状态数据进行实时分析，及时发现异常并触发告警；将关键事件记录存储到数据库中，为后续的数据分析和业务复盘提供数据支持等。

了解 EMQX 所支持的全部事件类型以及各事件对应的上下文信息，请参考：[SQL 数据源和字段 | EMQX 文档](https://docs.emqx.com/zh/emqx/latest/data-integration/rule-sql-events-and-fields.html#客户端事件) 

### 断开连接事件

本文示例中使用了客户端断开连接事件来触发离线告警，客户端的正常或异常离线都会触发该事件。

**该事件主要包含的上下文信息有：**

| **字段**        | **解释**                                                     |
| :-------------- | :----------------------------------------------------------- |
| reason          | 客户端连接断开原因： <br>normal：客户端主动断开<br/>kicked：服务端踢出，通过 REST API<br/>keepalive_timeout：keepalive 超时<br/>not_authorized：认证失败，或者 acl_nomatch = disconnect 时没有权限的 Pub/Sub 会主动断开客户端<br/>tcp_closed：对端关闭了网络连接 discarded: 另一个客户端使用相同的 ClientID 连接并设置 `clean_start = true` <br/>takenover: 另一个客户端使用相同的 ClientID 连接并设置 `clean_start = false` <br/>internal_error：畸形报文或其他未知错误 |
| clientid        | 客户端的 ID                                                  |
| username        | 客户端的用户名                                               |
| peername        | 客户端的 IPAddress 和 Port                                   |
| sockname        | 客户端接入的 EMQX 监听器地址                                 |
| disconnected_at | 客户端连接断开时间戳 (单位：毫秒)                            |
| disconn_props   | DISCONNECT Properties (仅适用于 MQTT 5.0)                    |
| timestamp       | 事件触发时间戳 (单位：毫秒)                                  |
| node            | 事件触发所在 EMQX 节点名称                                   |
| client_attrs    | [客户端属性](https://docs.emqx.com/zh/emqx/latest/client-attributes/client-attributes.html) |

**完整上下文信息如下：**

```json
{
    "node": "emqx@127.0.0.1",
    "reason": "normal",
    "timestamp": 1756465154714,
    "peername": "192.168.0.10:56431",
    "sockname": "0.0.0.0:1883",
    "metadata": {
        "rule_id": "sql_tester:6e70360444c3d6de"
    },
    "event": "client.disconnected",
    "username": "u_emqx",
    "proto_ver": 5,
    "client_attrs": {
        "test": "example"
    },
    "clientid": "c_emqx",
    "connected_at": 1756465154714,
    "proto_name": "MQTT",
    "disconn_props": {
        "User-Property": {
            "foo": "bar"
        },
        "User-Property-Pairs": [
            {
                "key": "foo"
            },
            {
                "value": "bar"
            }
        ],
        "Session-Expiry-Interval": 7200,
        "Reason-String": "Redirect to another server",
        "Server Reference": "192.168.22.129"
    },
    "disconnected_at": 1756465154714
}
```

接下来，我们将配置一条规则，使用规则 SQL 对离线事件进行过滤，并通过 Webhook 将特定的离线信息推送到外部平台，实现自动化通知。

## 事件触发规则配置

在本节中，我们将演示如何在 EMQX 规则引擎中创建一条规则来处理客户端断开连接的离线事件。

首先，我们会通过规则 SQL 筛选出异常的离线记录；然后，利用 HTTP 服务数据集成功能，[将 MQTT 数据发送到 HTTP 服务](https://docs.emqx.com/zh/emqx/latest/data-integration/data-bridge-webhook.html)；处理后的信息会被推送到各个企业系统中，实现实时告警。

**具体步骤如下：**

1. 登录 EMQX Dashboard
2. 进入 **集成 → 规则** 页面
3. 点击 **创建规则**
4. 在规则编辑器中配置 SQL

```sql
SELECT
    clientid,
    username,
    format_date('millisecond', '+08:00', '%Y-%m-%d %H:%M:%S', disconnected_at) as disconnected_at,
    peername,
    reason
FROM
    "$events/client/disconnected"
WHERE
  reason != "normal"
```

其中：

- `FROM '$events/client/disconnected'`：规则处理客户端断开连接事件
- `clientid`：客户端 ID
- `format_date('millisecond', '+08:00', '%Y-%m-%d %H:%M:%S', disconnected_at) as disconnected_at`：从上下文中选择断开连接时间戳，并格式化为人类易读格式
- `reason`：离线原因
- `peername`：客户端 IP 地址
- `WHERE reason != 'normal' AND reason != 'tcp_closed'`：筛选排除常见的断开连接原因

该 SQL 语句主动排除掉因正常业务流程导致的离线事件，能够有效确保最终输出的告警数据仅包含真正需要关注的异常离线事件，避免消息过多造成监控平台信息拥堵、运维人员精力被分散。

接下来，我们将基于这条规则，分别配置企业微信、钉钉和飞书离线消息推送。

## 将告警消息发送到企业微信

提示：以下功能为企业微信群聊专属特性，仅支持在企业微信的群聊场景中使用，暂不适用于个人日常使用的普通微信（包括普通微信的单聊、群聊及其他功能模块）。

### 添加企业微信消息推送

1. 根据[消息推送配置说明](https://developer.work.weixin.qq.com/document/path/99110)，在企业微信群中添加消息推送功能。

   ![image.png](https://assets.emqx.com/images/f6dd0fc2491058a94ea998fcbe779189.png)

1. 成功添加消息推送后，系统会自动生成该机器人专属的 Webhook 地址，其格式如下：

   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}
   ```

### 添加规则动作

完成「事件触发规则配置」，在规则中添加消息转发动作，将通过规则 SQL 筛选出的离线消息数据，封装为符合企业微信消息推送要求的消息格式，并推送至指定的企业微信群，实现离线告警消息的自动化推送。

具体步骤如下：

1. 点击 **添加动作**，动作类型选择 **HTTP 服务。**

2. 点击 **连接器** 旁边的 **+** 按钮，添加连接器。

3. 将钉钉机器人 Webhook 地址中的 **Host** 部分填入 URL 并保存。

   示例 Host：

   ```
   https://qyapi.weixin.qq.com
   ```

1. 在动作中选择刚刚新建的连接器，将钉钉机器人 Webhook 地址剩下的部分填入 **URL** 路径中。

   示例 URL 路径：

   ```
   /cgi-bin/webhook/send?key={key}
   ```

   ![image.png](https://assets.emqx.com/images/563b5d1561f16844cab9613dc1de3c3b.png)

1. 请求方法选择 POST，请求头使用默认配置。

2. 填写请求体字段：使用 `${field}` 语法将规则处理后的事件字段动态填充到 JSON 中。

3. 将离线事件相关信息拼接，构造成符合企业微信[文本消息推送](https://developer.work.weixin.qq.com/document/path/99110#文本类型)所需的 JSON 格式数据。

   示例 JSON 模板如下：

   ```json
   {
       "msgtype": "text",
       "text": {
           "content": "设备离线告警\n 客户端 ID：${clientid}\n 用户名：${username}\n 客户端 IP：${peername}\n 离线原因：${reason}\n 离线时间：${disconnected_at}"
       }
   }
   ```

1. 点击 **创建** 按钮完成动作创建，点击规则创建页面的 **更新** 按钮完成规则更新。

## 将告警消息发送到钉钉群聊

本章节将介绍如何通过钉钉机器人，把客户端离线告警消息发送至钉钉群聊。

### 添加钉钉机器人

1. 根据[创建自定义机器人](https://open.dingtalk.com/document/robots/custom-robot-access)指引，在钉钉群聊中添加钉钉机器人。

   注意：安全设置要选择自定义关键词用于消息校验。

   此处输入自定义关键词「告警」，其具体作用机制如下：当操作者获取到机器人对应的 Webhook URL 后，仅在发送的消息内容中包含「告警」这一预设关键词时，该消息才能够成功在目标群聊内发布。

   ![image.png](https://assets.emqx.com/images/c28570ce3918177a27c2ed87faf4c219.png)

1. 成功添加目标机器人后，系统会自动生成该机器人专属的 Webhook 地址，其格式如下：

   ```
   https://oapi.dingtalk.com/robot/send?access_token={xxxxxx}
   ```

### 添加规则动作

完成「事件触发规则配置」，并在规则中添加消息转发动作，将通过规则 SQL 筛选出的离线消息数据封装为符合钉钉机器人要求的消息格式，并推送至指定的钉钉群聊，实现离线告警消息的自动化推送。

1. 点击 **添加动作**，动作类型选择 **HTTP 服务**

2. 点击 **连接器** 旁边的 **+** 按钮，添加连接器

3. 将钉钉机器人 Webhook 地址中的 **Host 部分**填入 URL 并保存

   示例 Host：

   ```
   https://oapi.dingtalk.com
   ```

1. 在动作中选择刚刚新建的连接器，将钉钉机器人 Webhook 地址剩下的部分填入 **URL 路径**中，注意此处需要包含 access_token

   示例 URL 路径：

   ```
   /robot/send?access_token={xxxx}
   ```

   ![image.png](https://assets.emqx.com/images/4409ca015e8af144aa0dbc97cc8e4470.png)

1. 请求方法选择 POST，请求头使用默认配置；

2. 填写请求体字段：使用 `${field}` 语法将规则处理后的事件字段动态填充到 JSON 中，将离线事件相关信息拼接并构造成符合钉钉[自定义机器人发送群聊消息](https://open.dingtalk.com/document/orgapp/custom-bot-to-send-group-chat-messages)所需的 JSON 格式数据。钉钉机器人支持纯文本、Markdown 等格式消息，此处使用 Markdown。

   示例 JSON 模板如下：

   ```json
   {
       "msgtype": "markdown",
       "markdown": {
          "title":"设备离线告警",
          "text": "### 设备离线告警\n- 客户端 ID：${clientid}\n- 用户名：${username}\n- 客户端 IP：${peername}\n- 离线原因：${reason}\n- 离线时间：${disconnected_at}"
       }
   }
   ```

1. 点击 **创建** 按钮完成动作创建，点击规则创建页面的 **保存** 按钮完成规则创建。

至此我们已经完成了离线消息发送到钉钉群聊的规则创建。

## 将告警消息发送到飞书群聊

### **添加飞书机器人**

根据[添加自定义机器人](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#399d949c)指引，在飞书群聊中添加钉钉机器人。注意安全设置要选择自定义关键词用于消息校验。

此处同样输入自定义关键词「告警」，成功添加目标机器人后，系统会自动生成该机器人专属的 Webhook 地址，其格式如下：

```
https://open.feishu.cn/open-apis/bot/v2/hook/{xxxxx}
```

![image.png](https://assets.emqx.com/images/ab0feffed2994a9c93a7d719739860bf.png)

### **添加规则动作**

参考上文完成「事件触发规则配置」。在规则中添加消息转发动作，将通过规则 SQL 筛选出的离线消息数据封装为符合**飞书机器人**要求的消息格式，并推送至指定的飞书群聊，实现离线告警消息的自动化推送。

1. 点击 **添加动作**，动作类型选择 **HTTP 服务**

2. 点击 **连接器** 旁边的 **+** 按钮，添加连接器，将飞书机器人 Webhook 地址中的 **Host 部分**填入 URL 并保存。

   示例 Host：

   ```
   https://open.feishu.cn
   ```

1. 在动作中选择刚刚新建的连接器，将飞书机器人 Webhook 地址剩下的部分填入 **URL 路径**中

   示例 URL 路径：

   ```
   /open-apis/bot/v2/hook/{xxxx}
   ```

   ![image.png](https://assets.emqx.com/images/b1b3117ed6d6aeed8c5d1cadd825fb9b.png)

1. **请求方法**选择 POST，**请求头**使用默认配置；

2. 填写**请求体**字段：使用 `${field}` 语法将规则处理后的事件字段动态填充到 JSON 中，将离线事件相关信息拼接并构造成符合飞书[发送文本消息](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#756b882f)所需的 JSON 格式数据。

   示例 JSON 模板如下：

   ```json
   {
       "msg_type": "text",
       "content": {
           "text": "设备离线告警\n 客户端 ID：${clientid}\n 用户名：${username}\n 客户端 IP：${peername}\n 离线原因：${reason}\n 离线时间：${disconnected_at}"
       }
   }
   ```

1. 点击 **创建** 按钮完成动作创建，点击规则创建页面的 **更新** 按钮完成规则更新。

## **测试效果**

本章节将通过 EMQX 中提供的踢除客户端功能，触发一个客户端异常离线事件从而测试离线消息推送效果。

1. 使用 [MQTTX](http://mqttx.app/zh) 工具与 EMQX 建立一个 MQTT 连接

2. 登录 EMQX Dashboard，打开 **监控 → 客户端** 页面

3. 在列表中选中刚刚建立连接的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)，点击 **踢除** 按钮。对于这个操作，选中客户端将被 EMQX 断开并因此触发断开连接事件，事件的原因(reason 字段)为 `kicked`

   ![image.png](https://assets.emqx.com/images/bfad702cb54b6455bb3b021e08b67329.png)

1. 企业微信群内收到消息如下图所示

   ![image.png](https://assets.emqx.com/images/577c5056e2d71549e1341dcbef33214f.png)

1. 钉钉群内收到消息如下图所示

   ![image.png](https://assets.emqx.com/images/d558bf0337e42616141fd4adc368f63e.png)

1. 飞书群内收到消息如下图所示

   ![image.png](https://assets.emqx.com/images/a77283b7d91b4f200202a155894d70e9.png)

在其他正常的客户端断开情况中，比如使用 MQTTX 时主动点击断开按钮所触发的离线事件，系统不会发送消息通知。

## **总结与扩展**

通过以上内容，我们验证了 EMQX 可稳定将设备离线告警消息实时推送至企业微信、钉钉、飞书等常用协作平台。

借助 EMQX 规则引擎的强大灵活性，除客户端离线事件外，还可以轻松扩展至各类事件与消息的实时处理与推送，包括但不限于设备上线通知、认证失败告警、消息丢弃提醒等。开发者可基于此方案快速构建统一、高效的物联网告警与通知体系，显著提升系统可观测性与运维响应效率，全面增强业务可用性。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
