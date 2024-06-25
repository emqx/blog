尊敬的 MQTTX 用户，

本公告是为了通知您，我们将再次迁移 MQTTX Web 在线站点的域名，以便为您提供更安全和稳定的服务。有关迁移的详细信息和具体说明如下：

## 为什么要迁移？

不久前，我们将 MQTTX Web 的在线站点由 <https://www.emqx.io/online-mqtt-client> 迁移到了目前的 [http://mqtt-client.emqx.com](http://mqtt-client.emqx.com/)。然而，由于其仅能通过 HTTP 访问，存在固有的关键安全漏洞。此外，它与主域名 [http://emqx.com](https://www.emqx.com/) 同源，存在 cookie 共享的风险。这些都可能导致信息泄露和其他安全威胁。

为了进一步增强整体安全性和合规性，我们决定将站点迁移至 <https://mqttx.app/web-client>。新站点将具有以下优势：

- 高安全性：新站点采用 HTTPS 协议，可以确保数据在传输过程中的安全，防止信息泄露和其他安全风险。
- 访问统一性：作为 MQTTX 的一个客户端版本，MQTTX Web 设置在 [https://mqttx.app](https://mqttx.app/) 域名下可以更方便用户访问，确保服务的安全性和一致性.

## 迁移后的影响

由于新站点采用了安全性更高的 HTTPS 协议，这将为您的使用带来一些变化：

1. **WebSocket 连接限制**：

   迁移至 HTTPS 后，HTTP 协议下的普通 MQTT over WebSocket 连接 `ws://` 将无法使用。所有的 WebSocket 连接必须使用 Secure WebSocket `wss://`，以确保数据在传输过程中的安全性。例如，请使用 `wss://broker.emqx.io:8084` 代替 `ws://broker.emqx.io:8083`。

   这意味着，您在测试和生产环境中需要更新 MQTT over WebSocket 的连接配置。旧数据如果是使用 `ws://` 协议连接的，将无法在新站点中使用，需要适应新的安全要求。

2. **更新连接配置**：

   我们建议您在测试环境和生产环境中都使用 `wss://` 连接。如果您不熟悉如何配置，请参考我们的详细文档：[配置安全 WebSocket 监听器](https://docs.emqx.com/zh/emqx/latest/configuration/listener.html#配置安全-websocket-监听器)。该文档提供了逐步的配置指南来帮助您顺利完成更新。

## 如何本地迁移您的数据

MQTTX Web 的数据存储在浏览器本地，我们不会将您的数据传输至云端。因此，您需要手动导出数据并在新站点进行导入。具体操作步骤如下：

1. 访问旧站点 [http://mqtt-client.emqx.com](http://mqtt-client.emqx.com/) 。如果您有旧数据，旧站点会显示数据导出页面，指导您如何导出数据。如果没有旧数据，旧站点将自动跳转到新站点。
2. 访问新站点 <https://mqttx.app/web-client> 并导入之前导出的数据。

## 其他解决方案

MQTTX Web 的初衷是为广大 MQTT 用户提供一个便捷的浏览器内 MQTT 连接测试工具。出于数据安全考虑，我们强制启用了 HTTPS 协议。这意味着 Web 应用内的 WebSocket 连接必须使用 Secure WebSocket 连接（wss 协议）。

如果您出了 wss 之外还需要快速测试 ws 连接，我们推荐以下解决方案：

1. **下载桌面客户端或命令行客户端**：访问 [MQTTX 下载页面](https://mqttx.app/zh/downloads) 获取适合您的客户端版本。
2. **私有化部署 Web 版本**：使用 Docker 进行私有化部署，详见：[私有化部署指南](https://mqttx.app/zh/docs/web/get-started#私有化部署)。我们提供了全面的构建配置，方便您进行私有化使用，详细信息请参阅我们的开发文档：[开发文档](https://mqttx.app/zh/docs/web/development)。

## 常见问题

1. **迁移期间网站会不可用吗？**

   不会，新站点上线后，旧站点会继续支持访问，但无法使用主要功能。当您的旧本地数据迁移并清空后，旧站点将自动跳转到新站点。您也可以直接访问新站点开始使用。

2. **我的数据会受到影响吗？**

   您的数据存储在浏览器本地，不会被传输至云端，且不同的域名下无法实现数据共享。因此，请按照我们的指南手动导出和导入数据。

3. **迁移后是否需要更改我的设置？**

   您可能需要更新 WebSocket 连接为 wss 协议。请参考我们的文档进行相应配置。

## 建议与反馈

对于此次迁移可能给您造成的不便，我们深表歉意。我们希望通过此举确保更高的安全性和合规性，并提供更好的用户体验。感谢您的理解和支持。

我们也在此提醒所有用户合理、谨慎地使用在线工具，尤其是涉及安全测试方面。我们将持续为您提供安全、可靠和高效的服务。如果您在此次迁移过程中有任何问题或反馈意见，请通过 <https://askemq.com/c/mqttx/11> 或 [yusf@emqx.io](mailto:yusf@emqx.io) 联系我们。您的反馈对我们至关重要，再次感谢您的支持与配合。
