[EMQX](https://www.emqx.com/zh/products/emqx) 是一款全球下载量超千万的大规模分布式物联网 [MQTT 服务器](https://www.emqx.io/zh)，自 2013 年在 GitHub 发布开源版本以来，获得了来自 50 多个国家和地区的 20000 余家企业用户的广泛认可，累计连接物联网关键设备超过 1 亿台。

不久前，[EMQX 发布了 5.0 版本](https://www.emqx.com/zh/blog/emqx-v-5-0-released)，该版本在消息传输的可靠性、产品体验的易用性等方面也进行了大幅优化升级，是 MQTT 领域的一个里程碑式的成果。在发布前性能测试中，EMQX 团队通过一个 23 节点的集群达成了 [1 亿 MQTT 连接](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)+每秒 100 万消息吞吐，这使得 EMQX 5.0 成为目前为止全球最具扩展性的 MQTT 服务器。

EMQX 目前支持在 Linux、Windows、macOS、Raspbian 等系统中运行，也支持使用 Docker、Kubernetes、Terraform 部署。本文将以 EMQX 开源版 5.0.4 为例，介绍如何在 Ubuntu 系统中搭建一个单节点的 MQTT 服务器，并对搭建过程中容易遇到的常见问题进行逐一演示。

## 安装 EMQX

本文使用的演示环境为：阿里云上海区域2核4G（ecs.c7.large），**Ubuntu  20.04 64位**。

### 使用 APT 安装 EMQX

APT 是 Ubuntu 自带的包管理器，建议优先使用 APT 安装 EMQX。同时，EMQX 也提供了官方的 APT 源及一键式配置脚本，方便用户快速安装 EMQX。

1. 配置 EMQX APT 源。

   ```
   curl -s https://assets.emqx.com/scripts/install-emqx-deb.sh | sudo bash
   ```

   复制如上命令到 Ubuntu 终端下执行，如下图即表示配置成功。

   ![配置 APT 源](https://assets.emqx.com/images/4d50b52f6a11f9c59d6b524b92d0af15.png)

2. 安装 EMQX 最新版。

   ```
   sudo apt-get install emqx
   ```

3. 安装成功后，使用如下命令启动 EMQX。

   ```
   sudo emqx start
   ```

   如下图，若启动成功，将会提示：`EMQX 5.0.4 is started successfully!`。若命令长时间无响应，请通过 [EMQX 运行情况检查](#emqx-运行情况检查) 章节说明查看相关端口是否被占用。

   ![启动 MQTT 服务器](https://assets.emqx.com/images/25dd5e014a47e8082dd2988ea5d7fae1.png)

4. EMQX 管理命令

   EMQX 提供了命令行工具，方便用户对 EMQX 进行启动、关闭、进入控制台等操作。如下图，在终端执行 `sudo emqx` 查看 EMQX 相关管理命令。

   ![EMQX 管理命令](https://assets.emqx.com/images/18491face867eab53a5aae2ea5760c06.png)


### 使用 tar.gz 包安装 EMQX

当服务器无公网接入或需要快速部署、验证 EMQX 功能时可使用 `tag.gz` 包安装，该安装方式无任何第三方依赖且管理方便。

#### 下载安装包

访问 EMQX 下载地址 [https://www.emqx.io/zh/downloads?os=Ubuntu](https://www.emqx.io/zh/downloads?os=Ubuntu)。选中 `Package` 标签，安装包类型选择 `Ubuntu20.04 amd64/tag.gz`，然后点击右边的复制图标（这将会复制整行 wget 下载命令）。

![下载 EMQX](https://assets.emqx.com/images/cfab87178de1fa6481e283f78d07d647.png)

将下载命令粘贴至服务器命令行终端，执行下载操作。

![下载 EMQX](https://assets.emqx.com/images/59b04a6c00cbc4e214b5fabf0f39381e.png)

#### 解压安装

在服务器终端执行如下命令，该命令将会把压缩包解压至当前目录下的 `emqx` 目录。

>本次演示将会安装在当前用户的家目录下，即 `~/emqx/`

```
mkdir -p emqx && tar -zxvf emqx-5.0.4-ubuntu20.04-amd64.tar.gz -C emqx
```

接下来可使用如下命令启动 EMQX

```
./emqx/bin/emqx start
```

若启动成功，将会提示：`EMQX 5.0.4 is started successfully!`。若命令长时间无响应，请通过 [EMQX 运行情况检查](#emqx-运行情况检查) 章节说明查看相关端口是否被占用。



## EMQX 运行情况检查

### 端口监听情况

使用命令 `netstat -tunlp` 检查 EMQX 端口运行情况，默认情况下 EMQX 会启动如下端口，若有异常请检查端口占用情况。

> 该命令也可在 EMQX 安装前执行，确保相关端口未被占用。

![MQTT 服务器端口](https://assets.emqx.com/images/84b58c00ea74342739a96e4d8d9baf17.png)

| 端口  | 说明                                                         |
| ----- | ------------------------------------------------------------ |
| 1883  | MQTT/TCP 协议端口                                            |
| 8883  | MQTT/SSL 协议端口                                            |
| 8083  | MQTT/WS 协议端口                                             |
| 8084  | MQTT/WSS 协议端口                                            |
| 18083 | EMQX Dashboard 端口                                          |
| 4370  | Erlang 分布式传输端口                                        |
| 5370  | 集群 RPC 端口，默认情况下，每个 EMQX 节点有一个 RPC 监听端口。 |

### 访问 Dashboard

EMQX 提供了 Dashboard，以方便用户通过 Web 页面管理、监控 EMQX 并配置所需的功能。EMQX 成功启动之后可以通过浏览器打开 ` http://localhost:18083/`（将 localhost 替换为实际 IP 地址）访问 Dashboard。

> 访问 Dashboard 之前需要确保服务器的防火墙打开了 18083 端口

Dashboard 的默认用户名为 `admin`，密码为 `public`，第一次登录成功后会提示修改密码。密码修改完成后，我们也可以在 Settings 页面将 Dahshboard 的语言改为 `简体中文`。

![MQTT Dashboard](https://assets.emqx.com/images/c333eadac083110daf03c69958ba2d58.png)

## MQTT 连接测试

接下来我们点击左侧菜单栏里面的 `WebSocket 客户端` ，该客户端可测试 MQTT over Websocket，验证 MQTT 服务器是否已部署成功。

>需要确保防火墙已打开 8083 端口访问权限

### 连接至 MQTT 服务器

如下图，该工具已根据访问地址自动填充了主机名，我们直接点击`连接`按钮。

![MQTT over WebSocket 连接至 MQTT 服务器](https://assets.emqx.com/images/8f7e471197f5c7c24aaebea4a5cea3a0.png)

如下图，提示连接成功。

![MQTT over WebSocket 连接至 MQTT 服务器成功](https://assets.emqx.com/images/12e6dd168a03586b0e53eb1c5e1de971.png)

### 订阅主题

如下图，订阅一个 `testtopic` 主题。

![MQTT over WebSocket 订阅主题](https://assets.emqx.com/images/fa88f24faa153d80f74a95b41a623d7d.png)

### 消息发布

如下图，我们向 `testtopic` 发布了两条消息，且接收成功，表明 MQTT 服务器已部署成功且在正常运行。

![MQTT over WebSocket 消息发布](https://assets.emqx.com/images/7cf801991f324feb9597f3f87e8856a2.png)

至此，我们已完成了 MQTT 服务器的搭建及连接测试，但是该服务器仅仅只能用于测试，若要部署生产环境下可用的 MQTT 服务器，我们还需要进行最重要的认证配置。

## 配置认证

默认情况下，EMQX 将允许任何客户端连接，直到用户创建了认证器。认证器将根据客户端提供的认证信息对其进行身份验证，只有认证通过，客户端才能成功连接。接下来我们将演示如何使用 EMQX 内置的数据库进行用户名、密码认证。

> EMQX 也提供了与多种后端数据库的认证集成支持，包括 MySQL、PostgreSQL、MongoDB 和 Redis。
>
> 查看文档了解更多认证方式：[https://www.emqx.io/docs/zh/v5.0/security/authn/authn.html](https://www.emqx.io/docs/zh/v5.0/security/authn/authn.html)

### 创建认证

EMQX 从 5.0 开始支持在 Dashbaord 配置认证，以方便用户能更加方便、快速的创建安全的 MQTT 服务。我们点击 `访问控制` 菜单下的 `认证` 进入认证配置页面，然后点击最右侧的 `创建` 按钮。

![创建认证](https://assets.emqx.com/images/d170661d7c52514bc22423ee112e04df.png)

选择 `Password-Based` 选项，然后点击 `下一步`。

![选择 Password-Based](https://assets.emqx.com/images/03f2510f4d65ae3fbfdae120ad2ab933.png)

数据库选择 `Built-in Database`，然后点击 `下一步`。

![选择 Built-in Database](https://assets.emqx.com/images/785ed46efd489551171d657a4beb6b41.png)

接下来选择账户类型、加密方式、加盐方式，并点击 `创建`。

> 这里我们使用默认配置，读者可根据业务实际需求进行选择。

![创建认证](https://assets.emqx.com/images/bac5c5ae0b76eceb26b47e1c36d95814.png)

### 添加用户

认证创建成功后如下图。接下来我们点击 `用户管理`添加用户。

![用户管理](https://assets.emqx.com/images/dfde4a7b5cb1359d0d8db460b3452682.png)

进入用户管理页面后，我们点击最右侧的 `添加` 按钮，并在弹出框里设置用户名与密码，之后点击 `保存`。

![添加用户](https://assets.emqx.com/images/b31db984da63a508138f85850b165a1e.png)

如下图表示创建成功。

![添加用户成功](https://assets.emqx.com/images/51ab77811b3fc8f947cfab297c30d7f9.png)

### 测试认证

接下来我们使用 Dashboard 提供的 Websocket 工具来测试认证是否已配置成功。在连接配置里输入刚才创建的用户名与密码，然后点击`连接`。

![连接](https://assets.emqx.com/images/af6505f46913978a3378d2062ad3e34a.png)

将会看到右侧弹窗提示已连接。

![MQTT 链接成功](https://assets.emqx.com/images/eae97a36bc00844f752c81f7e7beb203.png)

接下来我们使用一个未创建的用户名 `test1`，点击连接将会看到如下连接失败信息。

![MQTT 连接失败](https://assets.emqx.com/images/d5aa032f50c8a6d20708e0bbb8e94ebf.png)

至此，我们已完成了 EMQX  的认证配置，搭建了一台可用于生产环境的单节点 MQTT 服务器。若要保证 MQTT  服务器的高可用，还需要创建多个节点的 EMQX 集群，创建集群的具体细节本文不再详述，读者可参考 [EMQX 集群文档](https://www.emqx.io/docs/zh/v5.0/deploy/cluster/intro.html) 进行配置。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
