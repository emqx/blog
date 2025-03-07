In today's fast-paced IoT and messaging landscape, a reliable, low-latency, and scalable broker is essential. EMQX leads in MQTT solutions, and with EMQX Serverless Plan, you can deploy a robust MQTT service in seconds. But how do you connect large language models like Anthropic’s Claude to an EMQX broker? That’s where **EMQX MCP Server** comes in.

[EMQX MCP Server](https://github.com/Benniu/emqx-mcp-server) is a [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) server implementation that enables Anthropic's Claude to interact with MQTT brokers. This blog post will walk you through this innovative solution, explain its significance, and provide a step-by-step tutorial on how to set it up using [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt).

![image.png](https://assets.emqx.com/images/7680094555c3f1e4c37003bdc51c5c84.png)

<center>Send an MQTT Message From Cloud Desktop</center>

## What is EMQX MCP Server?

![EMQX MCP Server Tools](https://assets.emqx.com/images/952da4ce905eb7842ddbb93d19922826.png)

<center>EMQX MCP Server Tools</center>

<br>

EMQX MCP Server is an implementation of Anthropic's [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) that allows Claude to interact with MQTT brokers. It acts as a bridge between Claude Desktop(an MCP client) or any other MCP clients (e.g., Cursor, Cline) and the EMQX MQTT infrastructure, giving Claude the ability to:

1. List and manage MQTT clients
2. Retrieve detailed client information
3. Disconnect clients when necessary
4. Publish messages to any MQTT topic

This integration leverages the power of Claude's natural language processing while extending its capabilities into IoT and messaging domains - opening up entirely new possibilities for AI-assisted device management and monitoring.

EMQX MCP Server can be used with any agents that support the MCP protocol. For example, you can add EMQX MCP Server to Cursor, allowing you to communicate with MQTT servers in your development environment through chat. This integration enables you to test and interact with your MQTT applications in real-time while coding, making the development process more efficient and intuitive.

## Why This Matters

The integration of AI assistants with MQTT infrastructure represents a significant advancement for several reasons:

1. **Natural Language IoT Control**: Users can manage IoT devices and messaging through conversational prompts.
2. **Simplified Monitoring**: Claude can be asked to check client connections and report status in human-friendly terms.
3. **Intelligent Message Publishing**: Compose messages with Claude's help and publish them in one seamless interaction.
4. **Accessibility**: Makes complex MQTT operations available to non-technical users.
5. **Customizable AI Agent Creation**: EMQX MCP Server can be combined with other MCP servers to create personalized AI agents tailored to specific workflows. Users can mix and match different capabilities (database access, MQTT control, API integrations, etc.) to build AI assistants that perfectly match their unique requirements without any coding.

## Step-by-Step Tutorial

Let's walk through setting up the EMQX MCP Server with EMQX Serverless.

### Step 1: Create an EMQX Serverless Deployment

EMQX Serverless is the perfect starting point for this integration - it's free to try, requires no complex setup, and provides all the MQTT broker functionality you need.

1. Visit [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)
2. Sign up for a free account
3. Create a new Serverless deployment:
   - Click "**+ New Deployment**"
   - Select "**Serverless**" tier
   - Choose your preferred region
   - Click "Create"
4. Once your deployment is active, navigate to "**Overview**" and note your connection information
5. Configure client authentication under "**Access Control**" **→** "**Authentication**" for MQTT clients (e.g., MQTTX, devices, or apps).
6. Create an API key (for the EMQX MCP Server to connect to the EMQX broker):
   - Go to "**Overview**" and click "**+ New Application**" button.
   - Click "Create" to generate a new API key and secret
   - Save these credentials securely - you'll need them later

For detailed instructions on creating your EMQX Cloud Serverless deployment, refer to the [official documentation](https://docs.emqx.com/en/cloud/latest/create/serverless.html).

### Step 2: Install Claude Desktop App

The EMQX MCP Server provides tools for any MCP-compatible client. While it can work with various MCP clients, for this tutorial we'll use the Claude Desktop App as our example.

1. Download and install the [Claude Desktop App](https://claude.ai/download)
2. Launch the app and sign in with your Anthropic account

### Step 3: Set Up EMQX MCP Server

There are two ways to set up the EMQX MCP Server. Let's go with the Docker option as it's simpler:

1. Make sure you have Docker installed on your computer

2. Pull the EMQX MCP Server Docker image:

   ```shell
   docker pull benniuji/emqx-mcp-server
   ```

3. Find your Claude Desktop App configuration file:

   - On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

4. Edit the configuration file to add the EMQX MCP Server:

   ```json
   {
     "mcpServers": {
       "EMQX_MCP_Server": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "-e", "EMQX_API_URL=https://your-emqx-cloud-instance.com:8443/api/v5",
           "-e", "EMQX_API_KEY=<YOUR-API-KEY>",
           "-e", "EMQX_API_SECRET=<YOUR-API-SECRET>",
           "benniuji/emqx-mcp-server"
         ]
       }
     }
   }
   ```

5. Replace the environment variables with your actual EMQX Serverless details:

   - `EMQX_API_URL`: Your deployment's API URL (found in the Cloud Console)
   - `EMQX_API_KEY`: The API key you created
   - `EMQX_API_SECRET`: The API secret corresponding to your key

6. Save the configuration file and restart Claude Desktop App

### Step 4: Connect a Test Client to Your MQTT Broker

To test the integration, let's connect an MQTT client to your broker:

1. Install [MQTTX](https://mqttx.app/)
2. Connect to your EMQX Serverless deployment using the connection details from the Cloud Console
3. Use the client ID, username, and password configured in your deployment
4. Connect and subscribe to the topic '`test/topic`'
5. Keep the client running

### Step 5: Interact with MQTT Through Claude

Now you're ready to use Claude to interact with your MQTT broker! Here are some example prompts to try:

1. **List connected clients**:

   ```
   Please list all clients currently connected to my MQTT broker.
   ```

2. **Get detailed information about a specific client**:

   ```
   Can you show me detailed information about the client [CLIENT_ID]?
   ```

3. **Publish a message to a topic**:

   ```
   Please publish a "Hello World" message to the topic "test/topic" with QoS 1.
   ```

4. **Disconnect a problematic client**:

   ```
   Please disconnect the client [CLIENT_ID] from the broker.
   ```

## Example Interaction

Here's what a typical interaction might look like:

**User**: Please list the clients connected to the MQTT broker.

**Claude**: Here are the clients currently connected to your MQTT broker:

Connected Client:

- Client ID: mqttx_2232bdb1
- Username: test
- Protocol: MQTT v5

...

There is currently 1 client connected to your MQTT broker. Would you like more detailed information about this specific client or would you like to perform another action with your MQTT broker?

**User**: Yes, please provide the detailed info of this client.

**Claude**: I'll retrieve the detailed information for this client for you

. ...

Here's the detailed information for client "mqttx_2232bdb1":

**Basic Information:**

- **Client ID:** mqttx_2232bdb1
- **Username:** test ... 

**Connection Details:**

- **Connected:** Yes
- **Created At:** 2025-03-02T05:29:51.103+00:00 ...

Would you like to perform any actions with this client, such as publishing a message to a topic or disconnecting the client?

**User**: Please write a poem and send it to the topic '/poem' with QoS 1.

**Claude**: I'll create a poem and publish it to the topic '/poem' with QoS 1. Let me do that for you. ... I've successfully published the poem to the topic '/poem' with QoS 1. The message has been delivered with ID: 00062F55A1EFB1156ABC481240B30000.

The poem I sent was:

- Signals in the ether,
- Invisible threads that bind,
- Devices speak in whispers,
- Across the digital divide.
- Messages like leaves falling,
- From cloud to waiting ground,
- Connected yet untethered,
- Where silence makes no sound.
- Brokers of the modern age,
- Routing dreams from here to there,
- In this web of connections,
- We find ourselves everywhere.
- Like stars in constellation,
- Each point of light has worth,
- The language of machines,
- Redefining our Earth.

Is there anything else you'd like to do with your MQTT broker?

## Advanced Use Cases

The EMQX MCP Server integration opens up numerous possibilities:

1. **IoT Device Management**: Ask Claude to check device statuses, disconnect problematic devices, or send configuration updates.

2. **Monitoring Dashboard**: Have Claude periodically check client connections and report status in natural language.

3. **System Integration**: Use Claude as a conversational interface to your messaging infrastructure, enabling non-technical users to interact with complex systems.

4. **Testing and Debugging**: Ask Claude to publish test messages with specific payloads to troubleshoot your MQTT applications.

5. **Smart Home Control**: Integrate with home automation systems to control devices through conversational prompts.

6. **Data Pipeline Orchestration**: Combine multiple MCP servers to create sophisticated data workflows. For example:

   ```
   User: "Please analyze yesterday's temperature sensor data from our PostgreSQL database and publish a summary report to the 'reports/temperature' MQTT topic for our dashboard to consume."
   Claude: [Using Database MCP Server] "I've analyzed the temperature data from yesterday. The average temperature was 22.3°C with a peak of 27.8°C at 2:15pm. I've detected an anomalous pattern between 3-4am where temperatures fluctuated by ±3°C within minutes, which may indicate sensor issues or environmental factors.
   [Using EMQX MCP Server] I've published this analysis along with a JSON payload containing the hourly averages and anomaly details to the 'reports/temperature' topic with QoS 2 and retention enabled. Your dashboard should now display this information, and the retained message will ensure new subscribers receive this report automatically."
   ```

This workflow demonstrates how Claude can:

- Query complex data from databases
- Apply analytical reasoning to identify patterns and anomalies
- Format results appropriately for different audiences (human-readable summary and machine-readable JSON)
- Distribute those insights via MQTT to downstream applications
- All are triggered by a single natural language request

## Why Choose EMQX Serverless?

EMQX Serverless is the ideal platform for this integration because:

1. **Zero Infrastructure Management**: No need to maintain servers or worry about scaling.
2. **Free Tier**: Get started without any upfront costs.
3. **Instant Deployment**: Have your MQTT broker running in minutes.
4. **Scalability**: Seamlessly scales as your needs grow.
5. **Enterprise-Grade Features**: Despite being serverless, it offers robust capabilities including authentication, access control, and monitoring.

## Conclusion

The EMQX MCP Server represents an exciting convergence of conversational AI and IoT messaging. By bridging Claude's natural language capabilities with EMQX's robust MQTT infrastructure, it creates new possibilities for how we interact with connected devices and messaging systems.

Whether you're an IoT developer looking to simplify device management, a system administrator seeking more intuitive monitoring tools, or just an enthusiast exploring the cutting edge of AI and IoT integration, the EMQX MCP Server offers a powerful new way to interact with your MQTT ecosystem.

Get started today with EMQX Serverless and experience the future of conversational IoT control!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
