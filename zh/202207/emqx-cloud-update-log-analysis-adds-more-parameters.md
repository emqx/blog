近日，全托管 [MQTT 消息云服务 EMQX Cloud](https://www.emqx.com/zh/cloud) 发布功能更新：对「日志」模块进行了优化，新增多个分析参数，帮助用户进行更加有效系统监控与运维。

## 功能简介

作为一款旨在免除用户基础设施管理维护负担的全托管 MQTT 云服务，EMQX Cloud 通过实时在线查看日志功能帮助用户及时了解系统运行情况，对发现的故障问题进行追溯和排查，以保障系统的稳定运行。

之前的日志分析参数仅有时间、日志级别和实例 ID 这三个，功能实现较为基础。最新版本对该功能进行了多项底层优化，新增了可选参数，包括客户端 ID、客户端 IP、用户名、主题、资源 ID、规则 ID，以供用户筛选搜索，更精准、快速地定位错误，解决问题。而节点将直接显示在告警详情中。

![EMQX Cloud 日志](https://assets.emqx.com/images/a4ca590714d9529e02784563fe53ec85.png)

## 功能使用

用户进入控制台后点击「日志」即可查询日志。默认的参数有显示时间、日志级别、错误类型、客户端 ID 和客户端 IP ，点击更多条件可展开根据用户名、主题、资源 ID 和规则 ID 等参数条件进行定向日志检索。

![EMQX Cloud 日志](https://assets.emqx.com/images/97af1cba64a48c00c5b0e68403b37db1.png)

<center>日志界面</center>

日志中包含的字段说明如下表所示：

| **参数**  | **含义**                                                     |
| --------- | ------------------------------------------------------------ |
| 时间      | 日志上报的时间                                               |
| 日志级别  | 主要分以下 3 种告警错误紧急用户可根据不同类别优先级进行对应处理。 |
| 错误类型  | 主要分以下 5 种数据集成：数据集成相关的错误。对应的服务没在运行或其它原因造成的错误。例如存储到 MySQL 时，MySQL 没在运行，未授权、或表错误等。客户端：客户端相关的错误，包含错误的认证信息，错误的访问控制信息，以及其它原因造成无法连接等。消息：消息相关的错误，例如编码问题、消息失弃等。模块：emqx 模块相关的错误, 例如自定义认证因无法连接到对应服务而产生的错误。EMQX 内部错误：Erlang 及无法分类到上述情况的错误。用户可根据错误类型快速定位错误产生模块。 |
| 客户端 ID | 输入 client ID，搜索该 client ID 产生的日志                  |
| 客户端 IP | 输入 client IP，搜索改 client IP 产生的日志                  |
| 用户名    | 输入 username，搜索该 user name 产生的日志                   |
| 主题      | 输入 topic name, 搜索该 topic下产生的日志                    |
| 资源 ID   | 输入资源 ID，搜索该资源相关的日志                            |
| 规则 ID   | 输入规则 ID，搜索该规则相关的日志                            |

> 注意：EMQX Cloud 支持 14 天内免费的日志存储和检索，超出 14 天的日志将不支持查询，如您有特殊需求，可以在控制台内提交工单和我们联系。

 

常见日志分析及解决措施可参考文档：[https://docs.emqx.com/zh/cloud/latest/deployments/logs.html](https://docs.emqx.com/zh/cloud/latest/deployments/logs.html) 


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
