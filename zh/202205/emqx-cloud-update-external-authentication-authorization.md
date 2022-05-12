### 功能类别

本次开发功能隶属于 「认证鉴权」模块的拓展功能，在继之前的 http 自定义认证后，我们又开放了 MySQL 和 PostgreSQL 两种外部认证授权方式。

 

### 功能开发背景

对于一些已经规模化的厂商来说，用户侧的海量设备认证信息一般都存储在企业内部的数据库中，便于管理查询，也更加能够保障数据的安全性，降低数据泄露风险。虽然 EMQX Cloud 支持批量导入，但在实际操作中，如果认证设备的数量增长迅速，出现问题修改或排查往往需要花费很长的时间。

因此， 继之前 http 自定义认证后，我们又新推出了 MySQL 及 PostgreSQL 外部认证授权，支持直接从客户MySQL 或 PostgreSQL 数据库中直接验证设备认证信息，实现更加安全、更加快速的海量设备接入。

 

### 功能作用

#### 外部认证授权功能说明

作为一款全托管的云原生 mqtt 消息服务，用户可以通过控制台的认证鉴权模块来对设备进行身份认证及 topic 访问控制。身份认证采用用户名密码的形式进行认证，访问控制支持对客户端ID、用户名和全部用户三个粒度进行权限控制。身份认证及访问控制均支持 csv 文件批量导入。

除了将认证信息存储在 EMQX Cloud 中外，用户还可以通过外部认证授权，通过验证用户侧的认证信息来实现设备的认证及更加复杂的 ACL 校验逻辑。

目前支持 http 自定义认证，MySQL、PostgreSQL 外部认证授权（新增），可以通过如下配置完成认证和访问控制。

![MySQL、PostgreSQL 外部认证授权](https://static.emqx.net/images/326ecf93a93399045ab8a63e9fc9b558.png)
 

**MySQL 认证/访问控制**

![MySQL 认证/访问控制](https://static.emqx.net/images/0bea379e5c4f3a01f2e7041ca03aa900.png)

**PostgreSQL 认证/访问控制**

![PostgreSQL 认证/访问控制](https://static.emqx.net/images/486c47cfb97f0aa8b0640bcbc6c3f682.png)
 

通过外部认证授权功能，使得从外部 MySQL、PostgreSQL 数据库中验证认证信息作为认证数据源成为可能，快速存储⼤量数据的同时也更加⽅便与外部设备管理系统集成。

 
注意：

1. 若同时启用了内置认证，EMQX Cloud 将按照**先默认认证，后外部认证授权**的顺序进行链式认证
2. 如果当前部署为基础版，服务器地址请填写公网地址
3. 如果当前部署为专业版，需创建 VPC 对等连接，服务器地址请填写内网地址
4. 若提示 Init resource failure! 需检查服务器地址是否无误、安全组是否开启、数据库是否允许 EMQX Cloud 集群访问

 

 

#### 外部认证授权功能使用说明

见文档：

MySQL 认证/访问控制：[https://docs.emqx.com/zh/cloud/latest/deployments/mysql_auth.html](https://docs.emqx.com/zh/cloud/latest/deployments/mysql_auth.html) 

PostgreSQL 认证/访问控制：[https://docs.emqx.com/zh/cloud/latest/deployments/pgsql_auth.html](https://docs.emqx.com/zh/cloud/latest/deployments/pgsql_auth.html) 


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
