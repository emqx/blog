## 桥接概念

桥接是一种连接多个 EMQX 或者其他 MQTT 消息中间件的方式。不同于集群，工作在桥接模式下的节点之间不会复制主题树和路由表。桥接模式所做的是：

- 按照规则把消息转发至桥接节点；
- 从桥接节点订阅主题，并在收到消息后在本节点/集群中转发该消息。

![537b0cb72f91291a9a48dcd1fb6b48edf12ff04c2384TffwYO.jpeg](https://static.emqx.net/images/132525c32f1ad7199ed9cad6e1ab224d.jpeg)

工作在桥接模式下和工作在集群模式下有不同的应用场景，桥接可以完成一些单纯使用集群无法实现的功能：

- 跨 VPC 部署。由于桥接不需要复制主题树和路由表，对于网络稳定性和延迟的要求相对于集群更低，桥接模式下不同的节点可以部署在不同的 VPC 上，客户端可以选择物理上比较近的节点连接，提高整个应用的覆盖能力。
- 支持异构节点。由于桥接的本质是对消息的转发和订阅，所以理论上凡是支持 MQTT 协议的消息中间件都可以被桥接到 EMQX，甚至一些使用其他协议的消息服务，如果有协议适配器，也可以通过桥接转发消息过去。
- 提高单个应用的服务上限。由于内部的系统开销，单个的 EMQX 有节点数上限。如果将多个集群桥接起来，按照业务需求设计桥接规则，可以将应用的服务上限再提高一个等级。

在具体应用中，一个桥接的发起节点可以被近似的看作一个远程节点的客户端。



## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息桥接到 EMQX 或其他 MQTT Broker。

**该场景下设备端上报信息如下：**

- 上报主题：cmd/state/:id，主题中 id 代表车辆客户端识别码

- 消息体：

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // 客户端识别码
    "speed": 32.12, // 车辆速度
    "direction": 198.33212, // 行驶方向
    "tachometer": 3211, // 发动机转速，数值大于 8000 时才需存储
    "dynamical": 8.93, // 瞬时油耗
    "location": { // GPS 经纬度数据
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // 上报时间
  }
  ```

当上报数据发动机转速数值大于 `8000` 时，将该条信息部分数据桥接到指定服务器。



## EMQX 桥接到 Mosquitto 

### 准备工作

#### 修改 `mosquitto.conf`

为了避免与本地的 emqx 出现端口冲突的情况，这里临时修改一下 mosquitto 的本地端口号。

```bash
port 1882
```

#### 启动 `mosquitto`

```bash
$ mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```

### 配置说明

#### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 Mosquitto 服务器信息进行资源创建。

![image01.png](https://static.emqx.net/images/a9a06d901968dbe6b3fa9641ffdc2d9a.png)

EMQX 集群中节点所在网络环境可能互不相通，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![image02.png](https://static.emqx.net/images/08cc358211c69b3da918f1a4d6aefa29.png)

#### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image03.png](https://static.emqx.net/images/9172b5de2aa889b51161db8686362aaf.png)

#### 筛选所需字段

规则引擎使用 SQL 语句处理规则条件，该业务中我们需要将 `payload` 中所有字段单独选择出来，使用 `payload.fieldName` 格式进行选择，还需要消息上下文的 `topic`、`qos`、`id` 信息，当前 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts, id
FROM
  "message.publish"
WHERE
  topic =~ 't/#'
```

#### 确立筛选条件

使用 SQL 语句 WHERE 字句进行条件筛选，该业务中我们需要定义两个条件：

- 仅处理 `cmd/state/:id` 主题，使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'cmd/state/+'`
- 仅处理 `tachometer > 8000` 的消息，使用比较符对 `tachometer` 进行筛选：`payload.tachometer > 8000`

组合上一步骤得到 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts,
  id
FROM
  "message.publish"
WHERE
  topic =~ 'cmd/state/+'
  AND payload.tachometer > 8000
```

#### 使用 SQL 测试功能进行输出测试

借助 SQL 测试功能，我们可以实时查看当前 SQL 处理后的数据输出，该功能需要我们指定 payload 等模拟原始数据。

payload 数据如下，注意更改 `tachometer` 数值大小，以满足 SQL 条件：

```json
{
  "id": "NXP-058659730253-963945118132721-22",
  "speed": 32.12,
  "direction": 198.33212,
  "tachometer": 9001,
  "dynamical": 8.93,
  "location": {
    "lng": 116.296011,
    "lat": 40.005091
  },
  "ts": 1563268202
}
```

点击 **SQL 测试** 切换按钮，更改 `topic` 与 `payload` 为场景中的信息，点击 **测试** 按钮查看数据输出：

![image04.png](https://static.emqx.net/images/73b34ae8b39700dae738e946202a9856.png)

测试输出数据为：

```json
{
  "client_id": "NXP-058659730253-963945118132721-22",
  "id": "589A429E9572FB44B0000057C0001",
  "speed": 32.12,
  "tachometer": 9001,
  "ts": 1563268202
}
```

测试输出与预期相符，我们可以进行后续步骤。

#### 添加响应动作，桥接消息到 Mosquitto

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果桥接到 Mosquitto。

点击响应动作中的 **添加** 按钮，选择 **桥接数据到 MQTT Broker** 动作，选取刚刚选定的资源。

![image05.png](https://static.emqx.net/images/1b2bda04b5f7ab1293de45928a3bb862.png)

### 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. Mosquitto 的订阅者将收到一条数据，数值与当前消息一致。

#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片发送如下信息：

- 主题：cmd/state/NXP-058659730253-963945118132721-22
- 消息体：

```json
{
  "id": "NXP-058659730253-963945118132721-22",
  "speed": 32.12,
  "direction": 198.33212,
  "tachometer": 9001,
  "dynamical": 8.93,
  "location": {
    "lng": 116.296011,
    "lat": 40.005091
  },
  "ts": 1563268202
}
```

![image06.png](https://static.emqx.net/images/c1b0be24860b23dd598ba84275e54fa0.png)

点击**发送**按钮，发送成功后查看得到当前规则已命中统计值为 1。

命令行中查看数据表记录得到数据如下：

![image07.png](https://static.emqx.net/images/9a7f9ddcbd304911465e64b336ad8cf8.png)

至此，我们通过规则引擎实现了使用规则引擎桥接消息到 MQTT Broker 的业务开发。



## RPC 桥接

### 准备工作

准备另外一台 emqx 节点，启动两台 emqx。

### 配置说明

#### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 EMQX 服务器信息进行资源创建。

![image01.png](https://static.emqx.net/images/8917c3462574d02eeecfbd55957dd3d2.png)

EMQX 集群中节点所在网络环境可能互不相通，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![image02.png](https://static.emqx.net/images/9c8fca5baca5c4c99452ca5d16373aa8.png)

#### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image03.png](https://static.emqx.net/images/c8adca25f45b069b42c29b646ed6369b.png)

#### 筛选所需字段

规则引擎使用 SQL 语句处理规则条件，该业务中我们需要将 `payload` 中所有字段单独选择出来，使用 `payload.fieldName` 格式进行选择，还需要消息上下文的 `topic`、`qos`、`id` 信息，当前 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts, id
FROM
  "message.publish"
WHERE
  topic =~ 't/#'
```

#### 确立筛选条件

使用 SQL 语句 WHERE 字句进行条件筛选，该业务中我们需要定义两个条件：

- 仅处理 `cmd/state/:id` 主题，使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'cmd/state/+'`
- 仅处理 `tachometer > 8000` 的消息，使用比较符对 `tachometer` 进行筛选：`payload.tachometer > 8000`

组合上一步骤得到 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts,
  id
FROM
  "message.publish"
WHERE
  topic =~ 'cmd/state/+'
  AND payload.tachometer > 8000
```

#### 使用 SQL 测试功能进行输出测试

借助 SQL 测试功能，我们可以实时查看当前 SQL 处理后的数据输出，该功能需要我们指定 payload 等模拟原始数据。

payload 数据如下，注意更改 `tachometer` 数值大小，以满足 SQL 条件：

```json
{
  "id": "NXP-058659730253-963945118132721-22",
  "speed": 32.12,
  "direction": 198.33212,
  "tachometer": 9001,
  "dynamical": 8.93,
  "location": {
    "lng": 116.296011,
    "lat": 40.005091
  },
  "ts": 1563268202
}
```

点击 **SQL 测试** 切换按钮，更改 `topic` 与 `payload` 为场景中的信息，点击 **测试** 按钮查看数据输出：

![image04.png](https://static.emqx.net/images/3c5700c19f549281c4729ec97b33aa2d.png)

测试输出数据为：

```json
{
  "client_id": "NXP-058659730253-963945118132721-22",
  "id": "589A429E9572FB44B0000057C0001",
  "speed": 32.12,
  "tachometer": 9001,
  "ts": 1563268202
}
```

测试输出与预期相符，我们可以进行后续步骤。

#### 添加响应动作，桥接消息到另一个 EMQX

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果桥接到另一个 EMQX。

点击响应动作中的 **添加** 按钮，选择 **桥接数据到 MQTT Broker** 动作，选取刚刚选定的资源。

![image05.png](https://static.emqx.net/images/120eae630e5b9f61593ff1492a61e0de.png)



### 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. 对端 EMQX 的订阅者将收到一条数据，数值与当前消息一致。

#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片发送如下信息：

- 主题：cmd/state/NXP-058659730253-963945118132721-22
- 消息体：

```json
{
  "id": "NXP-058659730253-963945118132721-22",
  "speed": 32.12,
  "direction": 198.33212,
  "tachometer": 9001,
  "dynamical": 8.93,
  "location": {
    "lng": 116.296011,
    "lat": 40.005091
  },
  "ts": 1563268202
}
```
![image16.png](https://static.emqx.net/images/74e20ab7d66510a6d7d51f9ce72eb1ed.png)

点击**发送**按钮，发送成功后查看得到当前规则已命中统计值为 1。

 使用命令行中查看数据表记录得到数据如下：

![image17.png](https://static.emqx.net/images/b61282f8a06f687a9824d72f8cd774e0.png)



至此，我们通过规则引擎实现了使用规则引擎桥接消息的业务开发


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
