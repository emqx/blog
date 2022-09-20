在企业的实际业务应用当中，权限管理往往是一大重点：权限管理是否足够细化、是否具备足够的弹性，不仅关乎企业的信息安全，更与企业管理的精细化程度和效率密切相关。

## EMQX Cloud 功能升级，应对多样管理需求

作为一个企业级的全托管 MQTT 消息服务，[EMQX Cloud](https://www.emqx.com/zh/cloud) 为不同规模的企业提供了方便、易用的运维代管服务。在服务客户的过程中，我们发现：企业内部通常存在着不同的组织和项目，一个技术设施服务的管理人员与服务的使用者也很可能不在同一个组织内，其管理需求和目的不尽相同。

在最近更新的 EMQX Cloud 中，我们引入了「Project」概念来解决这一问题。

一个企业用户可以创建多个 Project，并在 Project 下创建部署，通过多项目部署管理功能对不同项目的部署区分管理，满足不同组织的管理需求。

**轻松几步，实现多项目部署管理**

项目管理聚焦项目维度，每个项目可以包含一个或多个部署。每个账户会拥有一个默认项目，如果没有创建其他项目，则已经创建的部署及创建的新部署将会默认归属于默认项目。

![EMQX Cloud 多项目部署管理](https://assets.emqx.com/images/a141a27b56969f1693dce45a9c8ff2d6.png)

## 创建项目

1、 登陆进入控制台后，点击「项目列表」，进入项目管理界面。

![EMQX Cloud 项目列表](https://assets.emqx.com/images/9b9664c599ec67cb57b1cb234c27340e.png)

项目管理页面

![EMQX Cloud 项目列表2](https://assets.emqx.com/images/65d3355814fbf28d44b5697db9902dfa.png)

2、 点击「新建项目」 ，填写项目名称及描述，点击「确认」，即可完成项目的创建。

![EMQX Cloud 新建项目](https://assets.emqx.com/images/31d4beed52b3fd6cb3a93d5e6fcd60d7.png)

在左侧项目列表可以找到创建的项目

![EMQX Cloud 已创建项目](https://assets.emqx.com/images/3d12e89879d92c9ae15016424d0fe982.png)

## 管理项目下的部署

### 新建部署

选中项目，点击「新建部署」，按照引导选择规格配置，即可创建该项目下的一个新部署。

![EMQX Cloud 新建部署](https://assets.emqx.com/images/d6d37fb76f6b5912be10479f180a14dc.png)

### 移动现有部署

找到需要移动的部署，将鼠标移动到部署右上角，点击「移动到」。

![EMQX Cloud 移动部署](https://assets.emqx.com/images/a11c1e9213cab1b2c2f720bc1f8ab78f.png)

在下拉列表中，会出现当前项目列表，选择任意一个，即可将部署移动到指定的项目下。

![EMQX Cloud 选择项目](https://assets.emqx.com/images/1747f17b4d73225529d6a69d9ce52bdb.png)

> 注：一个部署仅能属于一个项目，一个项目下可以管理多个部署。

### 查看所有部署

点击项目列表右侧的「所有部署」即可查看目前账号内的所有部署情况。

![EMQX Cloud 查看所有部署](https://assets.emqx.com/images/913a280349c97b28f15d3ed6d753b9a1.png)

您账号下所有部署概览

![EMQX Cloud 查看所有部署](https://assets.emqx.com/images/bd6616509b9c3f399c3301f87a104f04.png)


## 编辑项目名称及删除项目

### 编辑项目

如需修改已创建的项目名称，可在左侧的项目列表找到您需要修改的项目，点击“修改图标”即可修改项目名称及描述。

![EMQX Cloud 编辑项目](https://assets.emqx.com/images/760e8eb8bb6485e332950e7f184e6e04.png)

### 删除项目

如需删除项目，点击“删除图标”即可删除项目。

![EMQX Cloud 删除项目](https://assets.emqx.com/images/cd44e98da3037439fb9c03044e876893.png)



在未来的版本中，EMQX Cloud 还将进一步支持基于项目的用户权限管理，真正实现赋予不同角色不同的操作权限。

对我们的产品和服务如有任何意见或问题，欢迎发送邮件至 [cloud-support@emqx.io](mailto:cloud-support@emqx.io) ，我们的团队将为您提供一对一的咨询服务。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
