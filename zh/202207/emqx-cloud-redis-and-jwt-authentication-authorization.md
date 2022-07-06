继之前的 HTTP 自定义认证以及 MySQL、PostgreSQL 外部认证后，近日 [EMQX Cloud](https://www.emqx.com/zh/cloud) 又开放了 Redis 和 JWT 两种外部认证授权方式。用户可以在进行认证鉴权时将有更多的选择，灵活实现更安全、快速的海量设备接入。

## 灵活多样的认证方式

作为一款全托管的云原生 MQTT 消息服务，用户可以通过控制台的认证鉴权模块来对设备进行身份认证及 Topic 访问控制。身份认证采用用户名密码的形式进行认证，访问控制支持对客户端ID、用户名和全部用户三个粒度进行权限控制。身份认证及访问控制均支持 csv 文件批量导入。

除了将认证信息存储在 EMQX Cloud 中，用户还可以通过外部认证授权，在用户存储认证信息的外部数据库中进行身份验证，也支持连接到 JWT 服务进行验证。

Redis 相较于其他数据库，拥有丰富的数据类型，如字符串、哈希、列表、集合、有序集合等。加之其读写性能高、命令执行速度快等特性，使其被广泛应用在各类场景。

JWT（JSON Web Token）认证是基于 Token 的鉴权机制，不依赖服务端保留客户端的认证信息或者会话信息，在持有密钥的情况下可以批量签发认证信息，是一种非常简便的认证方式。

## 使用指南

用户可以通过如下操作配置，使用 Redis 作为外部数据源或 JWT 认证的方式，完成认证和访问控制。

访问控制台，在左侧菜单栏「认证鉴权」->「外部认证授权」，访问外部认证授权功能。具体配置调试步骤可参考界面提示及文末的帮助文档。

![EMQX Cloud 外部认证授权](https://assets.emqx.com/images/f2ae1400874220e7f69e1299077d2eb8.png)

**Redis 认证/访问控制**

![EMQX Cloud Redis 认证/访问控制](https://assets.emqx.com/images/08360e1ead24028c0e2b3fc6d96846cd.png)

**JWT 认证/访问控制**

![EMQX Cloud JWT 认证/访问控制](https://assets.emqx.com/images/2e183b59010075a0e94030184c7fe495.png)


**注意事项**

1. 若同时启用了内置认证，EMQX Cloud 将按照**先默认认证，后外部认证授权**的顺序进行链式认证。
2. 当多种认证方式同时启用时，系统会默认按照 **模块的启用顺序** 来执行查询。
3. 如果当前部署为基础版，服务器地址请填写公网地址。
4. 如果当前部署为专业版，需创建 [VPC 对等连接](https://docs.emqx.com/zh/cloud/latest/deployments/vpc_peering.html)，服务器地址请填写内网地址。
5. 若提示 Init resource failure! 需检查服务器地址是否无误、安全组是否开启 。

 

本次更新进一步丰富了外部认证授权功能的可选项，用户可根据自己的业务情况选择对应的认证方式，无论是大规模设备接入，还是移动应用场景，都能够灵活应对。

 

> **相关文档**
>
> Redis 认证/访问控制：https://docs.emqx.com/zh/cloud/latest/deployments/redis_auth.html
>
> JWT 认证/访问控制：https://docs.emqx.com/zh/cloud/latest/deployments/jwt_auth.html



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
