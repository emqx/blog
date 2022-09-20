![画板 172x.png](https://assets.emqx.com/images/59a2b2df1035f9a1f7e3c364a1528a48.png)

## PostgreSQL 数据库介绍

作为开源关系数据库重要一员，PostgreSQL 标榜自己是世界上最先进的开源数据库，相比于其他开源关系数据库如 MySQL，PostgreSQL 是完全由社区驱动的开源项目，由全世界超过 1000 名贡献者所维护。PostgreSQL 提供了单个完整功能的版本，而不像 MySQL 那样提供了多个不同的社区版、商业版与企业版。PostgreSQL 基于自由的 BSD/MIT 许可，组织可以使用、复制、修改和重新分发代码，只需要提供一个版权声明即可。

PostgreSQL 具有诸多特性，在 GIS 领域有较多支持，其“无锁定”特性非常突出，支持函数和条件索引，有成熟的集群方案。PostgreSQL 还具备及其强悍的 SQL 编程能力如统计函数和统计语法支持，通过 Timescaledb 插件，PostgreSQL 可以转变为功能完备的时序数据库 Timescaledb 。





## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息存储到 PostgreSQL 数据库。为了便于后续分析检索，消息内容需要进行拆分存储。

**该场景下客户端上报数据如下：**

- Topic：testtopic

- Payload:

  ```
  {"msg":"Hello, World!"}
  ```

## 准备工作

### 创建数据库

创建 tutorial 数据库，用户名为 postgres，密码为 password：

```shell
$ docker pull postgres

$ docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres:latest

$ docker exec -it postgres psql -U postgres

> CREATE database tutorial;

> \c tutorial
```



### 创建数据表

创建 `t_mqtt_msg` 表：

```sql
CREATE TABLE t_mqtt_msg (
  id SERIAL primary key,
  msgid character varying(64),
  sender character varying(64),
  topic character varying(255),
  qos integer,
  retain integer,
  payload text,
  arrived timestamp without time zone
);
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 PostgreSQL 资源类型并完成相关配置进行资源创建。

![image20190725142933513.png](https://assets.emqx.com/images/7886bf1c52c3cf3a97eead6bd3388f09.png)



### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **message.publish**，即在 EMQX 收到 PUBLISH 消息时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190719112141128.png](https://assets.emqx.com/images/98eedf967390caf95e040a2376d5bc1e.png)



#### 筛选所需字段

规则引擎使用 SQL 语句过滤和处理数据。这里我们需要 msgid, topic, payload 等数据，同时希望匹配所有主题的消息，因此仅需要在默认 SQL 基础上删除 WHERE 子句即可，最终我们得到 SQL 如下：

```sql
SELECT
  *
FROM
  "message.publish"
```



#### SQL 测试

借助 SQL 测试功能，我们可以快速确认刚刚填写的 SQL 语句能否达成我们的目的。首先填写用于测试的 payload 等数据如下：

![image20190725145617081.png](https://assets.emqx.com/images/8d392abf53abb299ab6eb68c77541c83.png)

然后点击 **测试** 按钮，我们得到以下数据输出：

```json
{
  "client_id": "c_emqx",
  "event": "message.publish",
  "id": "589A429E9572FB44B0000057C0001",
  "node": "emqx@127.0.0.1",
  "payload": "{\"msg\":\"Hello, World!\"}",
  "peername": "127.0.0.1:50891",
  "qos": 1,
  "retain": 0,
  "timestamp": 1564037750692,
  "topic": "testtopic",
  "username": "u_emqx"
}
```

测试输出包含了所有需要的数据，我们可以进行后续步骤。



### 添加响应动作，存储消息到 PostgreSQL

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果存储到 PostgreSQL。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 PostgreSQL** 动作，选取刚刚创建的 `PostgreSQL` 资源并填写 SQL 模板如下：

`insert into t_mqtt_msg(msgid, topic, qos, retain, payload, arrived) values (${id}, ${topic}, ${qos}, ${retain}, ${payload}, to_timestamp(${timestamp}::double precision /1000)) returning id`

最后点击 **新建** 按钮完成规则创建。

![image20190725144256942.png](https://assets.emqx.com/images/efe039e16812a013224a138a97fb145b.png)


## 测试

### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 客户端上报消息时，该消息将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. PostgreSQL `tutorial` 数据库的 `t_mqtt_msg` 表中将增加一条数据，数据内容与消息内容一致。



### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片中发送如下消息：

- Topic：testtopic

- Payload:

  ```json
  {"msg":"Hello, World!"}
  ```

![image20190725145805279.png](https://assets.emqx.com/images/cdc7e0a8eb06de9b710e9bb31736c3ff.png)

点击 **发送** 按钮，发送成功后可以看到当前规则已命中次数已经变为了 1。

然后检查 PostgreSQL，新的 data point 是否添加成功：

![image20190725145107685.png](https://assets.emqx.com/images/97aa310b042ec33b08846024d8d9afeb.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 PostgreSQL 数据库的业务开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
