With the challenge of massive connections of devices in the IoT era and the large-scale real-time data streams generated along with them, EMQ provides a modern data infrastructure from the edge to the cloud, facilitating the unified "connect, move, process and analyse"of cloud-edge IoT data.

[EMQX](https://www.emqx.com/en/products/emqx), an all-in-one cloud-native distributed messaging broker with the SQL-based rule engine, has overcome the challenge of massive connections. While the streaming database HStreamDB is trying to solve the other half: storage, processing and real-time analysis of these enormous IoT data.

[HStreamDB](https://hstream.io/), as the first stream-native database explicitly designed for streaming data, is dedicated to efficient large-scale data stream storage and management. Combining EMQX and HStreamDB, one-stop management of massive data access, storage, real-time processing and analysis will be no longer complicated.

![EMQX and HStreamDB](https://assets.emqx.com/images/fc0fe48820b6158dd404cd8757ff9658.png)

In the [HStreamDB v0.6](https://hstream.io/blog/hstreamdb-v-0-6-release-notes) release, HStream has provided data append Rest API, which allows writing data to HStreamDB through Rest API with any language and is convenient for users in the community to carry out further development with HStreamDB. We utilise this feature combined with the Webhook of EMQX to realise a fast integration of EMQX and HStreamDB.

This article will introduce and explain how to bridge the data from EMQX to HStreamDB and fulfil the persistent data storage.

> **Note** The practice in this article bases on EMQX 4.3 and the image of hstreamdb/hstream:v0.6.1.

## Start EMQX and HStreamDB

First, we need a running EMQX. For how to install, deploy and start, please refer to[ EMQ Docs](https://docs.emqx.io/en/broker/v4.3/getting-started/install.html).

At the same time, we need a running HStreamDB. For more detailed tutorials on installing, deploying, and starting it, please refer to[ HStreamDB Docs](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html).

Users who are not familiar with HStreamDB can quickly start a stand-alone HStreamDB cluster through docker-compose as follows.

### Start HStreamDB

First, download the `docker-compose.yaml` file directly through the [link](https://raw.githubusercontent.com/hstreamdb/hstream/main/docker/quick-start.yaml).

Create a file to store database data:

```
mkdir /data/store
```

Start HStreamDB in the background:

```
docker-compose -f quick-start.yaml up -d
```

Through:

```
docker-compose -f quick-start.yaml logs hstream-http-server
```

You will see the following log:

```
Server is configured with: 
     gRPCServerHost: hserver 
     gRPCServerPort: 6570 
     httpServerPort: 6580 
Setting gRPC connection 
Setting HTTP server 
Server started on port 6580  
```

### Create the required Stream through HStreamDB CLI

A stream is an object used to store streaming data in HStreamDB, which can be regarded as a collection of data.

#### Start HStreamDB CLI

Start an HStreamDB command-line interface with docker:

```
docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream hstream-client --port 6570 --client-id 1
```

You will enter the following interface:

```
      __  _________________  _________    __  ___
     / / / / ___/_  __/ __ \/ ____/   |  /  |/  /
    / /_/ /\__ \ / / / /_/ / __/ / /| | / /|_/ /
   / __  /___/ // / / _  _/ /___/ ___ |/ /  / /
  /_/ /_//____//_/ /_/ |_/_____/_/  |_/_/  /_/

>
```

Create HStreamDB Stream to store the bridged data:

```
> CREATE STREAM emqx_rule_engine_output ; 
emqx_rule_engine_output 
```

Of course, we can also get the created Stream through `SHOW`:

```
> SHOW STREAMS; 
emqx_rule_engine_output
```

## Configure EMQX

Then, we open the Dashboard of EMQX, click `Rule Engine` and enter the `Resource` section.

![EMQX Dashboard Resource](https://assets.emqx.com/images/d110d6a38ba3a2ca0f238669d1d5a807.png) 

We can first create a `WebHook` resource, as shown below:

![EMQX Dashboard Create WebHook](https://assets.emqx.com/images/cfec5314f7b36d101d0cf963d2186bc2.png)

Fill in the listening address of `hstream-http-server` in the column of `Request URL`,`<host>:6580/streams/emqx_rule_engine_output:publish`.Then, click on the `test connection` button to test the connection.

![EMQX Dashboard test connection](https://assets.emqx.com/images/a811a5d1cfafa32a7102e0defeb9dc80.png)

Next, we will create the required rules for the integration:

![create EMQX rules](https://assets.emqx.com/images/41af650187256542b881bf345004d5d2.png) 


```
SELECT 
  payload,
  str(payload) as payload,
  0 as flag
FROM 
  "#"
```

We need to add an Action Handler, select `Action` as `Data to Web Server`:

![add EMQX Action](https://assets.emqx.com/images/f1434d7eeb1304842c18f9cda7e7c735.png) 

Set `Method` to `POST` and add `content-type` `application/json` to `Header`.

At this time, we have completed the most basic bridging settings. Next, let's test it through Websocket and HStreamDB CLI.

## Check whether integration is complete with HStreamDB CLI

First, we create a query in the HStreamDB CLI that we just started:

```
1> SELECT * FROM emqx_rule_engine_output EMIT CHANGES;

```

In HStreamDB, each stream represents a series of continuously changing streaming data. Therefore, a `Query` does not simply read data, but continuously reads and outputs the processed data written in the stream. In the CLI, the starting point for reading and outputting data is the moment when the `Query` is successfully created. Currently, what we can observe is that there is no output in CLI.

At this point, we can write data to EMQX through the WebSocket of EMQX DashBoard or other mqtt clients (such as [MQTT X](https://mqttx.app)).

The WebSocket is used in the following example. We can first connect to the emqx cluster we started:

![EMQX DashBoard WebSocket](https://assets.emqx.com/images/9e26f3437c419c79caf834b57efb2c08.png)

Then, send data to the specified topic:

![EMQX DashBoard send data](https://assets.emqx.com/images/cf912f88b2f4f2b7705defc908261223.png) 

If everything works as expected, we can see the data we sent to EMQX in the HStreamDB CLI in real-time.

```
1> SELECT * FROM emqx_rule_engine_output EMIT CHANGES;
{"location":{"lng":116.296011,"lat":40.005091},"speed":32.12,"tachometer":9001.0,"ts":1563268202,"direction":198.33212,"id":"NXP-058659730253-963945118132721-22","dynamical":8.93} 
```

So far, we have completed the persistent storage of the data sent to EMQX in HStreamDB.

By integrating EMQX with HStreamDB, we can achieve persistent storage of the data sent to EMQX and perform real-time processing and analysis to obtain further data insight. 

With the continuous development of the two products, we believe that the combination of EMQX + HStreamDB will play an essential role in the analysis and processing scenarios, catalyze data conversion and monetization and power the value creation of enterprise data assets, especially in the IoT field.
