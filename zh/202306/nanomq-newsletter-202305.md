五月初夏，[NanoMQ](https://nanomq.io/zh) 项目在发布了 0.18 版本后，聚焦于用户需求的开发和社区发现的漏洞问题的测试修复。即将于近期发布的 0.19 Beta 版本中将推出动态桥接功能和对桥接主题进行热更新的 HTTP API。同时还有新的 Prometheus 数据监控的 HTTP Exporter API，和针对桥接和命令行工具的若干小型优化。

## 桥接功能更新和修复

### NanoMQ 支持 MQTT5 over QUIC 桥接

继上一个版本 NanoSDK 增加了 MQTT5 over QUIC 的支持后，本月 NanoMQ 的桥接功能也引入了这一版本来支持 MQTT5 over QUIC 桥接，以期让用户可以同时利用 QUIC 协议和 MQTT 5.0 的优势。在 0.17 版本中 NanoMQ 的桥接功能已经支持了 MQTT 5.0 协议的 Connect 和 Subscribe 特性配置，而 MQTT5 over QUIC 桥接的使用方式也相同，示例配置如下：

```
bridges.mqtt {
	nodes = [
		{
			name = emqx
			connector {
				server = "mqtt-quic://xxx.xxx.xxx.xxx:14567"
				proto_ver = 5
				...
				conn_properties = {
					session_expiry_interval = 10000
				}
			}
			will {
				topic = "will_topic"
				...
				properties = {
					message_expiry_interval = 5000
				}
				
			}
			forwards = ["topic1/#", "topic2/#"]
			subscription = [
				{
					topic = "command"
					qos = 1
				}
			]
						# # Properties of subscribe for MQTT V5
			sub_properties {
				identifier = 1
			}
			quic_0rtt=true
			quic_qos_priority=true
			quic_multi_stream = false
			hybrid_bridging = false
		}
	]
}
```

其中比较重要且对功能影响较大的 MQTT 5.0 over QUIC 桥接配置选项有：

- `quic_0rtt` ：开启或关闭 QUIC 的 0RTT 快速重连，影响连接的安全性和对运营商网络的适配性。
- `quic_qos_priority` ： NanoMQ 特有的本地桥接 MQ 功能，可以对 QoS 大于 0 的数据包优先传输，更好地利用弱网带宽。
- `quic_multi_stream` ： 和 EMQX 5.0 配合使用的 QUIC 多流桥接功能，用以对付单流时的网络拥塞情况。开启后会显著增加传输速率和带宽占用。
- `hybrid_bridging` ：开启后桥接连接会在断开时自动在 TCP/QUIC 两种传输层间切换以尝试重连，可以用来应对复杂网络环境下对 QUIC 协议的封锁和丢包问题。

### 其他修复

同时 NanoMQ 还对桥接功能做了如下修复：

- 修复混合桥接模式：混合桥接模式即通过配置 `hybrid_bridging=true`开启的功能。经测试和用户反馈发现，在 0.14-0.18.2 的版本中使用此功能可能会造成服务停止，请不要开启。目前已经修复并且改进了切换速度和与MQTT 5.0 协议兼容，将在六月发布的 0.19 Beta 版本中一并推出。
- 修复 AWS IoT Core 桥接：AWS IoT Core 桥接功能在 0.9.0 版本中由于配置文件的重构更新导致无法开启，这一问题在 0.19 Beta 中也已经修复。 但由于 AWS C SDK 的 OpenSSL 版本和 NanoMQ 使用的 MsQUIC 库中的 OpenSSL 版本不兼容，所以导致两种功能无法同时开启。NanoMQ 将在后续的版本中对两个功能使用的 OpenSSL 进行静态链接处理来规避这一问题，但目前还需要用户避免同时使用二者。

### 动态桥接功能前瞻

自从 NanoMQ 发布以来，已经收到多个用户请求支持动态桥接功能。目前桥接功能还只能静态开启和关闭，若要更新还需要修改配置后重启 broker。在 0.19 Beta 版本中动态桥接功能将会以测试的形式放出，会和混合桥接功能（hybrid bridging）相同作为一个桥接旁路存在，所以 2 种特殊桥接模式不能同时开启。

要使用动态桥接功能，用户可以通过新增的 HTTP API 来修改和触发。即将推出两个新的桥接热更新 HTTP API：

- 更新桥接配置并触发连接重连即刻生效，通过 {$node} 参数来指定更新的目标桥接连接：

  ```
  curl -i --basic -u admin:public -X PUT 'http://localhost:8081/api/v4/bridges/$node' --data 
  '{
      "data": {
          ...... (更新的配置内容)
      }
  }'
  ```

- 更新桥接主题并触发 NanoMQ 向桥接目标发布 Sub/UnSub 请求，通过 {$node} 参数来指定更新的目标桥接连接。

  ```
  curl --location 'http://127.0.0.1:8081/api/v4/bridges/sub(unsub)/emqx' --data \
  '{
      "data": {
          "subscription": [
              {
                  "topic": "new/topic",
                  "qos": 2
              }
          ]
          ... 新的桥接主题相关配置
      }
  }'
  ```

  

目前此功能仍处在开发阶段，关于此功能的设计和使用方式，欢迎到论坛或 GitHub 页面提建议。

## 命令行工具更新

考虑到广大用户的使用习惯，nanomq_cli 命令行修改了交互方式，以配合已有的用户习惯：

- nanomq_cli pub/sub 的目标地址指定方式不再是  `--url` ，而是将地址和端口分开，用 `--host` 指定地址， `--port` 来指定端口。
- 由于不再有  `--url` 选项，所以 nanomq_cli pub/sub 客户端工具新增了 `--quic`  来供用户指定 QUIC 作为传输层。
- 修正了 nanomq_cli pub/sub 的指定证书选项命名错误： `--cacert` 改成 `--cafile` 。
- 调换了 `--identifier` 和 `--interval` 的简写使用法，现在分别是 `-i` 和  `-I`。

## NanoMQ 支持新的安装源

感谢社区用户的贡献，NanoMQ 现在已经上架 ArchLinux 的 AUR （Arch User Repository）。ArchLinux 用户可以通过 `yay` 命令一键安装。且支持 NanoMQ 的不同裁剪版本。

- `yay -S nanomq` 安装 NanoMQ 基础版本。
- `yay -S nanomq-msquic` 安装 NanoMQ QUIC 桥接版本。
- `yay -S nanomq-sqlite` 安装 NanoMQ SQLite 缓存版本。
- `yay -S nanomq-full` 安装 NanoMQ 全功能版本。

此外，NanoMQ 也已经被 NixOS （一个独立的 GNU/Linux 发行版） 整合，NixOS 用户可以使用 `nixpkgs` 安装 NanoMQ。

## Bug 修复

在上个月的版本发布通知中，我们特地感谢了社区用户提交的安全漏洞报告。这一版本中所有提交的漏洞以及相关的潜在问题都已经得到修复。具体的修复内容如下：

- 修复了未知 SQL 语句导致规则引擎崩溃的一个段错误问题。
- 修改了 HOCON 配置文件解析器的一个数字单位读取错误问题。
- 移除了 DDS Proxy 功能的编译安装环境问题（感谢 NixOS 的帮助）。
- 修复了一个消息结构体定义导致的在大端机器上的兼容性问题 （感谢 GitHub 用户 nnllyy）。
- 修复了一个由非法 Retain 消息包触发的狭窄的数据竞争窗口问题。
- 更新了 `l8w8jwt`依赖来修复了 HTTP Server JWT 认证。

## 即将到来

应多位用户的呼声，NanoMQ 在下一个版本中会增加动态桥接功能，用户能够通过 HTTP REST API 来修改桥接配置并 Reload 或重连桥接来生效，方便更灵活的数据路由管理。另外，在之前 Demo Day 中展示的 NFTP + MQTT 文件传输功能也计划作为标准功能内置到 nanomq_cli 中。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
