七月，EMQX 团队进入了快速迭代的开发节奏中。我们增加了一些令人兴奋的特性，并在 5.0 版本的关键功能上取得了突破性的进展。


## 全新的配置文件

**我们重构了配置文件的结构。** 新的配置目录结构将仅包含一个 [HOCON](https://github.com/lightbend/config/blob/main/HOCON.md) 格式的配置文件：emqx.conf。它将囊括 emqx 相关的所有配置，包括 Broker 核心部分、各个 Applications，以及 Plugins 等的配置。依托 HOCON  配置语法的特性，我们重新设计了一个层次清晰的配置结构，这个版本的配置会更易于阅读、修改和维护。

**新的配置文件将支持运行时修改。** emqx 的多数配置项将支持修改后实时生效，无需重启 emqx 服务。我们将支持通过 HTTP API  运行时修改配置项，也支持手动修改配置文件之后重新加载。通过 HTTP API 修改的配置项将存储在 data/ 目录下的  emqx_override.conf 文件中，以便重新启动 emqx 服务之后保留这些修改。运行时修改配置的功能仍在开发过程中。

![全新配置文件](https://static.emqx.net/images/41a66271f3fdb2514c299307395c7f73.png)


## Swagger UI

**我们引入了 Swagger UI 来展示和管理 HTTP API。** [Swagger UI](https://swagger.io/tools/swagger-ui/) 是一个流行的可视化和交互式的 HTTP API 文档工具。我们正在对 emqx 的 HTTP API 进行改造，使其符合 [OpenAPI](https://swagger.io/specification/) 规范。在编译 emqx 时会从源码自动生成 OpenAPI 协议描述文件，并通过 Swagger UI 做 API 文档的可视化展示。现在（emqx 5.0-alpha.3）你可以在 emqx 服务启动后，通过 [http://127.0.0.1:18083/api-docs](http://127.0.0.1:18083/api-docs) 访问这个交互式文档。

![swagger](https://static.emqx.net/images/3247d90db25c6d1e0f108564e921aa94.png)

![api](https://static.emqx.net/images/86fc2c0679ca3a15c3fa96359dbe4652.png)


## 全新的网关

**我们重构了网关功能。** 我们新增了 Protocol Gateway 概念，把 LwM2M，CoAP，STOMP，MQTT-SN，ExProto 等 IoT 协议网关统一放到了  Protocol Gateway 中进行管理，使得各协议更加方便地接入到 EMQX Broker 中来。

新的网关架构支持对各个协议网关进行多实例化创建和管理，并统一了各个协议的配置文件格式。在代码层面上：我们新增了通用的网关连接层以增加代码复用性；重构了 MQTT-SN 网关的部分代码逻辑，使其不再跟 emqx 核心部分耦合；重构了 CoAP 网关，在实现上不再依赖于 gen_coap。


## 稳步推进认证和鉴权功能

新的认证模块增加了[增强认证](https://www.emqx.com/zh/blog/mqtt5-enhanced-authentication)、HTTP 认证、MongoDB 认证等方式，并改进了通过 HTTP API 修改认证模块配置的能力。

新的鉴权模块（ACL) 增加了 MySQL、PgSQL、MongoDB、Redis、HTTP 等鉴权方式。
