## Introduction: The Convergence of MQTTX and MCP

MQTTX, the most popular MQTT client toolbox, has enhanced its capabilities in 1.12.0 beta by integrating the Model Context Protocol (MCP) into its Copilot AI feature. This integration transforms MQTTX into an MCP Host, allowing MQTTX Copilots to interact directly with MQTT brokers (EMQX) and local resources. By connecting large language models (LLM) with MQTT operations, this feature opens new possibilities for IoT automation, monitoring, and development.

> *Download the latest version here:* [Release v1.12.0-beta.2 · emqx/MQTTX](https://github.com/emqx/MQTTX/releases/tag/v1.12.0-beta.2)  *- Since it's a beta release, it won't auto-update through the application. Please manually download and install it from the Assets section.*

## Brief Overview of the MCP

[The Model Context Protocol (MCP) ](https://modelcontextprotocol.io/introduction)is a standardized interface between AI models and external data sources or tools, functioning as a "USB-C port for AI applications." It allows MQTTX Copilots to:

- Access contextual information beyond their training data
- Interact with local and remote systems securely
- Maintain a consistent interface across different AI providers
- Execute specialized functions through standardized tool calls

MCP follows a client-server architecture where host applications (like Cursor, MQTTX, etc.) contain MCP clients that connect to MCP servers, exposing specific capabilities. This architecture ensures data remains secure within your infrastructure while enabling powerful AI-driven workflows.

## MQTTX as an MCP Host: Implementation Overview

MQTTX now functions as an MCP Host by incorporating an MCP client that can connect to various MCP servers. The implementation supports:

- Both SSE (Server-Sent Events) and Stdio MCP server types
- Simple configuration through the MQTTX settings interface
- Integration with multiple AI models, including OpenAI GPT-4o, Claude 3.5/3.7, Grok 2, and DeepSeek models.
- Thinking Chain supports advanced reasoning with select models

Configuration is straightforward through the MQTTX settings panel, where users can specify MCP servers as command-line processes or via HTTP endpoints.

## Application Scenarios: MCP in Action with MQTTX

Let's explore how to set up and use MCP with MQTTX through practical examples:

### Setting Up MCP in MQTTX

1. Open MQTTX and navigate to **Settings** in the left sidebar.
2. Enable the **Copilot** feature and configure your preferred AI model with API keys.
3. Scroll down to the **MCP** section and enable it.
4. Add your MCP server configuration in JSON format in the provided input box.
5. After adding the configuration, available servers will appear in the list below.
6. Click the connection button in the upper right corner to test server connectivity.
7. For successfully connected servers, you'll see the available tools listed.
8. Toggle servers on/off using the disable/enable switches.

![image.png](https://assets.emqx.com/images/600a9cd369dc0e5f72c1e5206cd36edb.png)

### Local File System Integration

With the filesystem MCP server, Copilot can interact with your local files, generating and saving code directly to specified directories:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

**Example workflow:**

1. Configure the filesystem MCP server as shown above.
2. In the Copilot Chat Box, use the `@connection` keyword to extract current connection details.
3. Ask Copilot to "Generate JavaScript code for this MQTT `@connection` and save it to /Users/username/Downloads as mqtt-test.js".
4. The AI will use MCP to create and save the file to your specified location.

![image.png](https://assets.emqx.com/images/9083541d0479de279f1dc817e22b3f68.png)

![image.png](https://assets.emqx.com/images/ab2699fe33a281df3de79058c4affcdf.png)

Verifying in your terminal with `cat mqtt-test.js` will show that the code has been successfully created with the correct connection parameters.

![image.png](https://assets.emqx.com/images/57eccbaa50d22a194accca4a4ab14b56.png)

This approach streamlines development by eliminating the copy-paste workflow - code is generated and saved directly where you need it, ready for execution.

### MQTT Operations via MCP SSE Server

For direct MQTT operations through AI, you can deploy the custom MQTTX MCP SSE server (https://github.com/ysfscream/mqttx-mcp-sse-server):

```json
{
  "mcpServers": {
    "mqttx-server": {
      "url": "http://localhost:4000/mqttx/sse"
    }
  }
}
```

**Example workflow:**

1. Deploy the MQTTX MCP SSE server locally or in the cloud.
2. Configure the server in MQTTX as shown above.
3. In the Copilot Chat Box, ask: "Connect to `mqtt://broker.emqx.io:1883` and publish a message to testtopic/mcp".
4. In a separate MQTTX connection, subscribe to the same topic.
5. Observe as the message published via the AI's MCP call appears in your subscription.

![image.png](https://assets.emqx.com/images/0479dbf90a979e09fea616501ce3d2f5.png)

This capability transforms how you interact with MQTT brokers. Instead of manually configuring connections and publishing messages, you can use natural language to instruct the MQTTX Copilot to perform these operations on your behalf. This is particularly valuable for testing, debugging, and educational scenarios where quick MQTT interactions are needed.

## Conclusion

Integrating Model Context Protocol into MQTTX marks an essential step in EMQ's vision to bridge IoT and AI technologies. While this beta release enables AI assistants to interact with MQTT brokers through natural language, our roadmap extends further.

EMQ is actively exploring "[MCP over MQTT](https://www.emqx.com/en/blog/mcp-over-mqtt)" implementations, which address key limitations in the current MCP architecture by leveraging MQTT's built-in service discovery and publish-subscribe patterns. These developments lay the foundation for intelligent IoT communications combined with MQTTX Copilot’s AI capabilities for schema generation, connection diagnostics, and test data creation. We invite the community to test these features and share feedback as we continue developing solutions that make MQTT operations more accessible and powerful.

If you have specific requirements for IoT applications or AI integration with your MQTT workflows, don't hesitate to contact our team to help shape the future of this technology.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://mqttx.app/downloads" class="button is-gradient">Get Started →</a>
</section>
