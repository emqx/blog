This article will use the MQTT X scripts and timing function to simulate reporting temperature and humidity data. EMQ X Edge acts as the messaging middleware to forward messages, and EMQ X Kuiper performs receiving messages and processing rules. Finally, the processed data will be sent to MQTT X via EMQ X Edge.

![mqttxedgekuiper.png](https://static.emqx.net/images/9f96444f39724baa8ed5ee6d814618ed.png)

## Introduction and installation

All the runtime environments demonstrated in this article are all built through Docker. If you have other installation needs, you can also refer to the download link and installation document provided below to build them.

### Kuiper

[Kuiper](https://github.com/lf-edge/ekuiper) is a lightweight IoT edge analysis and stream processing open source software implemented by Golang, and it can run on various resource-limited edge devices. One of the main design goals of Kuiper is to migrate the real-time stream computing frameworks (such as [Apache Spark](https://spark.apache.org/), [Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/), etc.) running in the cloud-side to the edge-side. Kuiper refers to the architecture and implementation of the above-mentioned cloud-side stream processing projects above, use the features of edge streaming data processing and adopt the rule engine which is written based on `Source`, `SQL(business logic processing)` and `target (Sink)` to implement edge streaming data processing. Project address: [https://github.com/emqx/kuiper](https://github.com/emqx/kuiper)

> Version: v1.0.2

[Download link](https://github.com/lf-edge/ekuiper) ｜ [Installation document](https://docs.emqx.io/en/kuiper/latest/getting_started.html#download-install)

```shell
# Get a Docker mirroring
$ docker pull emqx/kuiper:1.0.2

# Enabling a Docker container
$ docker run -p 9081:9081 -d --name kuiper emqx/kuiper:1.0.2
```

### Kuiper-manager

This article will use Kuiper-manager to visually manage and use EMQ X Kuiper. Kuiper-manager is a Web management console that can be used to manage Kuiper nodes, streams, rules, plugins, etc.

> Version: v1.0.2

Currently only supported using Docker mirroring

```shell
# Get a Docker mirroring
$ docker pull emqx/kuiper-manager:1.0.2

# Enabling a Docker container
$ docker run -p 9082:9082 -d emqx/kuiper-manager:1.0.2
```

### EMQ X Edge

[EMQ X Edge](https://www.emqx.com/en/products/emqx)  is a lightweight multi-protocol IoT edge message middleware that supports being deployed on resource-limited IoT edge hardware. 

> Version: v4.2.4

[Download link](https://www.emqx.com/en/try?product=nanomq) | [Installation document](https://docs.emqx.io/en/edge/latest/install.html)

```shell
# Get a Docker mirroring
$ docker pull emqx/emqx-edge:4.2.4

# Enabling a Docker container
$ docker run -d --name emqx -p 1883:1883 emqx/emqx-edge:4.2.4
```

### MQTT X

[MQTT X](https://mqttx.app/) is a cross-platform [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) desktop test client that supports macOS, Linux, Windows. Users can quickly create multiple simultaneous online **MQTT client** for convenient testing the connect/publish/subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket and other **MQTT protocol** features. 

> Version: v1.4.2

[Download link](https://mqttx.app/) | [GitHub](https://github.com/emqx/MQTTX/releases/tag/v1.4.2)

Users can download the installation package according to their operating system from the MQTT X website or GitHub download page.

Linux users can download in Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

## Tutorials

After the environment has been built, we can collocate with the features between the modules to use it, perform feature testing and verification.

### Use of Kuiper-manager

First, we create and configure the streams and rules for Kuiper. After installing and successfully running Kuiper-manager, we open a browser and enter `http://localhost:9082`. If you access kuiper-manager from other computers, please change `localhost` to the IP address where you are running kuiper-manager. The password and username you will need to enter when you first open it is: `admin` / `public`. It is recommended that you change your password after logging in for the first time.

![kuipermanagerlogin.png](https://static.emqx.net/images/de28b1b45f019523ec9c8ed7b38851e5.png)

#### Nodes

After a successful login, you will be taken to a node management interface. Click on the `Add Node` button, there will be a pop-up box, and you need to add an instance node of Kuiper. In here, because we are using the general node, we select the first item `Directly Connected Node`. In addition to the directly connected node, adding the Huawei IEF node is also supported now, which will not be covered in this article. Then, you need to enter the `endpoint address` of the Kuiper instance to be manipulated and enter the `node name` to identify the node.

> Note: If you use Docker to start it, the endpoint address needs to be entered as the IP address within the Docker container.

![kuiperaddnodes.png](https://static.emqx.net/images/e219d0c1d211bb49a88866310ecbd3db.png)

After successfully added, we can access the node instance through clicking on the node name in the node list. Once inside, we will then create and configure the flows and rules of this Kuiper instance.

#### Streams

Once you are on the Kuiper instance page, you will go to the Tab page of streams, where we click on the `Create Streams` button on the right to go to the Create Streams page, where you can follow these steps:

1. Enter a `stream name` to identify it, here we enter the stream name as `demo`;

2. Enter the structure definition, for example, we can define in advance which field types are in the stream data that this stream need to receive. To add, simply enter the name of the field and select the type to add, which includes `bigint`, `float`, `string`, `boolean`, `array`, `struct` etc. Structure definitions are optional and can be cancelled or switched on by checking `whether stream with structure` above the structure list; when the structure definition is cancelled, data of any structure type will be received. In this article we have specified the data structures to be processed, so we add two separate fields: `temperature` and `humidity`, both of type `bigint`. 

3. Enter `Data source`, we will use MQTT as the message source in this article, so this configuration allows you to enter the `Topic` for receiving messages, here we enter `/kuiper/stream`.

4. Select `Stream Type`, which will be chosen here as MQTT.

5. Select `Configuration Group`, and the configuration group is the configuration information defined under the stream type, for example, the default MQTT configuration group `servers` information is `['tcp://127.0.0.1:1883']`. You can customize this configuration information by clicking on the `Source Configuration` button above to go to the page to configure, or you can go to the `etc` directory to modify the configuration file. Here we select the reconfigured `demo_conf` configuration group.

   > Note: If the MQTT Broker used is the EMQ X Edge initiated by Docker, the address of Servers needs to be changed to the IP address within the Docker container 

6. Select `Stream Format`, which will be chosen as `json` finally.

![kuipercreatestream.png](https://static.emqx.net/images/f7d5df43a41e46815c67716567f322da.png)

In addition to the above visual creation methods, we can also switch to text mode by clicking on the toggle button in the top right corner of the page. A stream can be created by entering the SQL statement used to create the stream directly. SQL example:

```sql
CREATE STREAM demo (
  temperature bigint,
  humidity bigint,
) WITH (DATASOURCE="/kuiper/stream", FORMAT="json", CONF_KEY="demo_conf", TYPE="mqtt");
```

After clicking the `Submit` button, we have successfully created a stream. The next step is to set up the rules for the created stream.

#### Rules

Click on the Tab item of the rule to go to the list of rules page. We click on the `Create Rule` button on the right to go to the create rule page, and at this point, you can follow the steps below.

1. Enter the `rule ID` to mark the rule, here we enter `demoRule`.

2. Enter the SQL statement for the rule runtime query. Here you will define a SQL statement that queries the temperature and humidity data in the data stream and sets the filter condition to that the temperature is greater than 30. SQL example:

   ```sql
   SELECT temperature, humidity FROM demo WHERE temperature > 30
   ```

3. Select the `Action` of the added rule, which is the Sink action group, the data can be multi-selected, and Sink is the target of the output when the rule is executed. Here we are still using MQTT and forwarding the data that has executed by the rule via MQTT. After the selection is complete, you can enter the configuration information for the MQTT Sink. In this article, we will only configure the address of the MQTT Broker and the `Topic` information, and `Topic` is the topic of the received message.

   > Note: If the MQTT Broker used is the EMQ X Edge initiated by Docker, the address of Broker needs to be filled as the IP address within the Docker container

4. Set `Options`, and part of options are optional and all options have default values. If you wish to change them, you can do so by referring to the [Kuiper documentation](https://docs.emqx.cn/cn/kuiper/latest/rules/overview.html#%E9%80%89%E9%A1%B9).

![kuipercreaterule.png](https://static.emqx.net/images/66bffdc71ba9c49183b080d42d6135b4.png)

In addition to the above visual creation methods, we can also switch to text mode by clicking on the toggle button in the top right corner of the page. Rules can be created by entering the JSON data of creation rule directly, JSON example:

```json
{
  "id": "demoRule",
  "sql": "SELECT temperature, humidity FROM demo WHERE temperature > 30",
  "actions": [
    {
      "mqtt": {
        "server": "tcp://172.17.0.2:1883",
        "topic": "/kuiper/rule"
      }
    }
  ]
}
```

After clicking the `Submit` button, we have successfully created a rule. So far, we have completed the Kuiper data stream and rule configuration. Next we will use MQTT X to test and verify Kuiper's stream processing capabilities.

### The use of MQTT X

Once the download and installation is complete, we open MQTT X and create a new connection called `edge1` to an EMQ X Edge with the same configuration as the Kuiper Source. After testing the connection successfully, we go to the `Scripts` page and use the example script provided below to generate the simulation data.

```javascript
/**
 * Simulated temperature and humidity reporting
 * @return Return a simulated temperature and humidity JSON data - { "temperature": 23, "humidity": 40 }
 * @param value, MQTT Payload - {}
 */

function random(min, max) {
  return Math.round(Math.random() * (max - min)) + min
}

function handlePayload(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  _value.temperature = random(10, 40)
  _value.humidity = random(20, 40)
  return JSON.stringify(_value, null, 2)
}

execute(handlePayload)
```

![mqttxscript.png](https://static.emqx.net/images/5aef8144b3c75fab5730afd7f7545c31.png)

Testing found that the simulated data was successful, and we went to the connection page, opened the script to use the function (using the script function is not described in detail in this article, you can refer to the [MQTT X documentation](https://github.com/emqx/MQTTX/blob/master/docs/manual-cn.md#%E8%84%9A%E6%9C%AC)). Enter the `Payload` data template to be sent as `{}`, enter `Topic` as the `Data Source` in the stream definition, in this case `/kuiper/stream`, then set the timing message, set the sending frequency to 1 second, then click Send. After the message has been successfully sent, MQTT X will automatically send one simulated test data per second.

![mqttxtimed.png](https://static.emqx.net/images/6358d2d739f455bb36670269eb3e2c52.png)

At this point, we create a new connection again called `edge2` to the EMQ X Edge with the same configuration as the Kuiper Sink and subscribe to the `Topic` configured in the MQTT Sink. In this case, we subscribe to the `/kuiper/rule` topic, to receive data processed by Kuiper.

![mqttxrule.png](https://static.emqx.net/images/d3d9bc645f87f0bfe5d63a6c2b6ee62a.png)

### Verify Results

Once we have sent the simulated data, we can see if any messages are coming in or going out by clicking on the `Status` button in the rules list. We can see from the screenshot below that Kuiper received a total of 40 messages and filtered out 14 messages.

![kuiperrulestatus.png](https://static.emqx.net/images/73b59e082e4af79cdc8c7491b6fed441.png)

Then continue to look at the messages within MQTT X. `edge1` has sent a total of 40 simulated messages at regular intervals, switching to `edge2` we see that a total of 14 messages have been received. The sent and received data is consistent with the Kuiper inflow and outflow data, and the `temperature` in the received messages is exactly above 30, which satisfies the filtering conditions we set in Kuiper. This means that our Kuiper stream processing function has successfully completed the data processing requirements we set, and the test and verification was successful.

![mqttxsend.png](https://static.emqx.net/images/3aabe367e47e56a41033aa3a6cfed18e.png)

![mqttxres.png](https://static.emqx.net/images/489c0e0422a1eae70a730cb0a70af7ec.png)

In addition to viewing the information of data processed by Kuiper rules via the Status button, you can also click on the `Topology' button to go to the topology diagram of the rule, which shows the complete flow of data and the status of the rule, and allows you to view real-time dynamic information about the specific data processing modules.

![kuiperruletopo.png](https://static.emqx.net/images/e6790e6b1ebee6501f96670b8d23129d.png)

## Summary

This article completes an easy tutorial on using the MQTT X client to verify the function of Kuiper stream processing. Kuiper can be used in various IoT edge scenarios. The system response speed can be improved, network bandwidth costs and storage costs can be saved, and system security can be improved via the processing of Kuiper at the edge.

In addition to the MQTT Source and MQTT Sink exemplified in the article, Kuiper has many diverse Source and Sink configurations built in and includes the ability to integrate with EdgeX Foundry, KubeEdge, EMQ X Edge, etc. Rule SQL also support for 60+ common functions, provide extension points available to extend custom functions. A powerful plugin system is provided that is highly extensible.

The three projects used in this article are all fully open source. You can go to GitHub ([EMQ X Kuiper](https://github.com/emqx/kuiper), [EMQ X Edge](https://github.com/emqx/emqx), [MQTTX]( https://github.com/emqx/MQTTX)) to submit problems you encountered during use, or to Fork our projects and submit revised PRs to us, which we will review and address promptly. We would also like to thank all the users in the community for their contributions and feedback.
