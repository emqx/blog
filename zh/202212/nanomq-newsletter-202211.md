11 月，NanoMQ 继续保持稳步更新，最新的 [0.14 版本](https://github.com/emqx/nanomq/releases/tag/0.14.1)已于本月初发布。此版本推出了用户期待许久的 ACL 鉴权（Access Control List）服务，并引入了全新的 HOCON 格式的配置文件。此外还缩减了发布版本时生成的 Docker 镜像的大小，并新增了带有 QUIC 支持的完整功能版镜像。


## ACL 鉴权

将 MQTT 服务用于 IoT 应用时，为了保证服务和信息安全，需要 ACL 鉴权服务来防止恶意客户端发布错误数据和控制命令或订阅未经允许的主题获取敏感数据。NanoMQ 的 ACL 支持在众多用户呼声中于 0.14 版本正式发布。

目前 NanoMQ 支持通过在配置文件中编写规则来根据客户端 ID 和用户名配置鉴权规则。ACL 配置文件风格和语法与 EMQX 4.x 版本相同。

此处给出部分常用的场景规则配置示例：

- 需要从系统主题读取监控数据显示在控制台时，只允许用户名是 dashboard 的客户端订阅“$SYS/#”系统主题，忽略有非法操作的客户端：

  ```
  ## ACL 未命中时，允许或者拒绝 发布/订阅 操作
  ##
  ## Value: allow: 允许
  ##        deny:  拒绝
  acl_nomatch=allow
  ## ACL 检查失败后，执行的操作。
  ##
  ## Value: ignore:     忽略
  ##        disconnect: 断开连接
  acl_deny_action=ignore
  
  # 允许用户名是 dashboard 的客户端订阅 "$SYS/#" 这个主题
  acl.rule.1={"permit": "allow", "username": "dashboard", "action": "subscribe", "topics": ["$SYS/#"]}
  
  # 拒绝其他所有用户订阅 "$SYS/#" 主题
  acl.rule.2={"permit": "deny", "username": "#", "action": "subscribe", "topics": ["$SYS/#"]}
  ```

- 拒绝客户端 ID 为“malicious”和用户名为“unauthorized”的非法客户端向匹配“sensitive/#”和“Command/+/critical”的所有主题进行发布操作，并立刻断开有非法行为的客户端连接。

  ```
  acl_nomatch=allow
  acl_deny_action=disconnect
  
  # 拒绝操作
  acl.rule.1={"permit": "deny", "or" :["username": "unauthorized", "clientid": "malicious"], "action": "publish","topics": ["sensitive/#", "Command/+/critical"]}
  
  # 前面的规则都没有匹配到的话，允许所有操作
  acl.rule.2={"permit": "allow"}
  ```

  

ACL 功能可以在编译阶段关闭来提高性能和剪裁大小：

`cmake -DENABLE_ACL=OFF ..`



未来会根据用户需求和反馈，提供更强大的 ACL 功能，如正则匹配、客户端 IP 匹配、关联数据库鉴权和 HTTP 鉴权等，欢迎大家在 [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq) 提交功能申请和反馈。

## 全新 HOCON 配置文件

秉承 EMQX 5.0 的先进设计，NanoMQ 也采用了标准的 HOCON（Human-Optimized Config Object Notation/人性化配置对象表示法）作为配置文件格式。HOCON 是一种更适合人类阅读的数据格式，功能语法上是 JSON 和 properties 的一个超集，可以灵活拓展。它由 Lightbend 开发，同时也在 Sponge 和 Puppet 等项目中作为配置格式使用。

NanoMQ 为了保证项目原有的易移植性和高度兼容性，使用原生 C 语言开发实现了一个语法解释器（[https://github.com/nanomq/hocon](https://github.com/nanomq/hocon)）来完成部分 HOCON 功能的解析并转换为 JSON 和内部结构体，使得用户能够在不引入其他依赖库的情况下也能使用 HOCON 风格的配置文件。从 0.14 版本开始，NanoMQ 以精简版本的 HOCON 格式为默认的配置文件。但考虑到许多老用户仍然习惯于使用原有风格的配置文件，所以旧的配置文件也予以保留，可以通过-old_conf命令来读取旧的配置文件格式。

| 配置文件                | 说明                                 |
| ----------------------- | ------------------------------------ |
| etc/nanomq.conf         | NanoMQ 的默认配置文件（HOCON格式）   |
| etc/nanomq_old.conf     | NanoMQ 的旧版本配置文件 （原格式）   |
| etc/nanomq_example.conf | NanoMQ 完整配置文件示例（HOCON格式） |

### 在鉴权和桥接配置中使用 HOCON 语法

在 HOCON 格式中不需要再为多次出现的配置文件类目（如多个用户名密码键值对）增加数字下标。

```
# #============================================================
# # Authorization 
 #============================================================
auth [
{
login = "admin"
password = "public"
}
{ 
login = "client"
password = "public"
}
  ......
]
```

对于复杂的配置层级关系，如多路桥接不分，能看到有更加明晰易读的隶属关系。

```
bridges.mqtt {
	nodes = [
		{
			name = emqx1
			enable = true
			connector {
				server = "mqtt-tcp://127.0.0.1:1883"
			}
			forwards = ["topic1/#", "topic2/#"]
			subscription = [
				{
					topic = "cmd/topic1"
					qos = 1
				}
				{
                   (......)
				}
			]
			parallel = 2,
			ssl {
				enable = false
				}
	}
	{
			name = emqx2
			enable = true
			connector {
				server = "mqtt-quic://127.0.0.1:14567"
			}
			forwards = ["topic1/#", "topic2/#"]
			subscription = [
				{
					topic = "cmd/topic1"
					qos = 1
				}
			]
			(......)
	}
]
```

其余功能的配置选项也根据 EMQX 5.0 的版本发布略有更改，请查阅 NanoMQ 官方文档查看更改后的配置文件细则。

## 其他优化

### 裁剪 Docker 镜像大小

NanoMQ 本身运行占用资源极小，但自 0.11 版本起由于引入了 QUIC 功能，使得镜像大小大大增加。为了帮助习惯采用 Docker 部署方式的用户节省部署空间，从 0.14 版本开始，Dockerfile 改为采用交叉编译方式发布具有完整功能的 Release 镜像。这一操作使得完整版镜像的大小缩小了数十倍。默认拉取的 NanoMQ 的镜像地址改为以 Alpine-Linux 为 base image 的版本，大小仅为 3MB。

MQTT over QUIC 桥接功能一经推出便得到了广泛的试用和热烈反响，但之前此功能必须通过源码编译开启，对于新手使用较为不便。自 0.14 版本起，NanoMQ 会自动一起发布开启 QUIC 支持的 Docker 镜像和二进制安装包。用户只需下载带有 [-msquic](https://github.com/emqx/nanomq/releases/download/0.13.5/nanomq-0.13.5-linux-arm64-msquic.rpm) 后缀的安装包或拉取带有 -full 后缀的 Docker 即可：

```
## 内置开启QUIC桥接功能的二进制安装包
nanomq-0.14.0-linux-amd64-msquic.deb
## 内置开启QUIC桥接功能的Docker镜像
docker pull emqx/nanomq:0.14.0-full
```

### 支持以共享库形式启动

不少用户有从自有程序调用 API 来启动 NanoMQ 的需求，或需要在 Android 或 iOS 移动端启动 MQTT 服务。为支持此类需求，NanoMQ 也可以编译成 .so 格式的动态链接库供使用：

```
cmake -G Ninja -DBUILD_SHARED_LIBS=ON ..
ninja
```

## Bug Fix

1. 修复了 QUIC 桥接中收到 Multi-Stream 功能影响造成的一个死锁问题。
2. 修复了使用会话保持的客户端的 QoS 1/2 消息重发时，概率性顺序异常的问题。
3. 修复了 QoS 1/2 消息只会重发一次从而造成的消息丢失。
4. 修复了 Android 平台上通过动态链接库使用 NanoMQ 时由于 POSIX 时钟系统精度不足导致的计时器异常问题。
5. 更新了 NanoSDK 的 close_all API 使其能够自动清理未完成的 AIO 避免线程阻塞。
6. 为 MQTT over QUIC 桥接连接下线事件消息增加了MQTT V5 的 KeepAlive Timeout 错误码。

## 即将到来

由于配置文件格式更新，配置热更新和 Reload 功能将推迟到下一个版本中正式发布（只支持 HOCON 版本）。另外还将为 MQTT over QUIC 桥接功能增加 CUBIC/BBR 拥塞算法支持，以获取在不稳定带宽的网络环境中更稳定的传输质量保证。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
