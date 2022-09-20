对于一些已经规模化的厂商来说，用户侧的海量设备认证信息一般都存储在企业内部的数据库中，不仅便于管理查询，也能够增加数据的安全性，降低数据泄露风险。尽管 EMQX Cloud 支持批量导入认证信息，但在实际操作中，如果认证设备的数量增长迅速，出现问题修改或排查往往需要花费很长的时间。

在此之前 [EMQ X Cloud 通过 HTTP 自定义认证功能](https://www.emqx.com/zh/blog/emqx-cloud-http-custom-authentication)为用户提供了连接自建认证中心的能力，以满足日益复杂的用户认证需求。在此基础上，近日，我们又新推出了 MySQL 及 PostgreSQL 外部认证授权，支持直接从用户的 MySQL 或 PostgreSQL 数据库中直接验证设备认证信息，帮助实现更加安全、更加快速的海量设备接入。

## **功能详解**

作为一款全托管的云原生 MQTT 消息服务，用户可以通过控制台的认证鉴权模块来对设备进行身份认证及 Topic 访问控制。身份认证采用用户名密码的形式进行认证，访问控制支持对客户端 ID、用户名和全部用户三个粒度进行权限控制。身份认证及访问控制均支持 csv 文件批量导入。

除了将认证信息存储在 EMQX Cloud 中外，用户还可以通过外部认证授权，通过验证用户侧的认证信息来实现设备的认证及更加复杂的 ACL 校验逻辑。

用户可以访问控制台，在左侧菜单栏「认证鉴权」->「外部认证授权」，访问外部认证授权功能。具体配置调试步骤可参考界面提示及文末的帮助文档。

![外部认证授权](https://assets.emqx.com/images/814d54403468585cbe69b8a9fc1b48d4.png)

**MySQL 认证/访问控制示例**

![MySQL 认证/访问控制示例](https://assets.emqx.com/images/49934da90a9fc04e0a398941ed0e8074.png)

**PostgreSQL 认证/访问控制示例**

![PostgreSQL 认证/访问控制示例](https://assets.emqx.com/images/78b6d0ce3f6ebecbe448aec3f297adb6.png)

通过外部认证授权功能，用户可以从外部 MySQL、PostgreSQL 数据库中验证认证信息作为认证数据源，快速存储⼤量数据的同时也更加⽅便与外部设备管理系统集成。


>注意：
>
>1. 若同时启用了内置认证，EMQX Cloud 将按照**先默认认证，后外部认证授权**的顺序进行链式认证
>2. 如果当前部署为基础版，服务器地址请填写公网地址
>3. 如果当前部署为专业版，需创建 VPC 对等连接，服务器地址请填写内网地址
>4. 若提示 Init resource failure! 需检查服务器地址是否无误、安全组是否开启、数据库是否允许 EMQX Cloud 集群访问



## 操作指南

关于 MySQL 及 PostgreSQL 外部认证授权功能更加详细的使用操作，请参考：

- MySQL 认证/访问控制：[https://docs.emqx.com/zh/cloud/latest/deployments/mysql_auth.html](https://docs.emqx.com/zh/cloud/latest/deployments/mysql_auth.html) 

- PostgreSQL 认证/访问控制：[https://docs.emqx.com/zh/cloud/latest/deployments/pgsql_auth.html](https://docs.emqx.com/zh/cloud/latest/deployments/pgsql_auth.html) 
 


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
