## Background

This article takes a common IoT usage scenario as an example and describes how to use edge computing to achieve fast, low-cost and efficient processing of business.

In various IoT projects, such as intelligent building projects, it is necessary to collect and analyze building data (such as elevators, gas, water and electricity). One solution is to connect all devices directly to the IoT platform in the cloud, similar to Azure IoT Hub or AWS IoT Hub. The problem with this solution is:

- Long data processing delay: it takes a long time to return data to the device after Internet transmission and cloud processing
- Data transmission and storage cost: bandwidth is required for Internet transmission. For large-scale Iot projects, the bandwidth will be considerable
- Data security: some data of the Iot will be very sensitive, and there will be risks if all data are transmitted through the Iot.

In order to solve the above problems, the industry has proposed a solution for edge computing. The core of edge computing lies in the proximity processing of data to avoid unnecessary delays, costs and security issues.

## Business scenario

Suppose there is an existing set of devices. Each device in the group has an id that sends data to the corresponding topic on the MQTT message server via the MQTT protocol. The design of the topic is as follows, where {device_id} is the id of the device.

```
devices/{device_id}/messages
```

The data format sent by each device is JSON, and the temperature and humidity data collected by the sensor are sent.

```json
{
    "temperature": 30, 
    "humidity" : 20
}
```

Now we need to analyze the data in real time, and ask for the following requirements: Calculate the average value (``t_av``) every 10 seconds for each device's temperature data, and record the maximum value within 10 seconds (``t_max``), minimum value (``t_min``) and number of data strips (``t_count``), and these four results are saved after the calculation is completed. The following is the sample result data:

```json
[
    {
        "device_id" : "1", "t_av" : 25,  "t_max" : 45, "t_min" : 5, "t_count" : 2
    },
    {
        "device_id" : "2", "t_av" : 25,  "t_max" : 45, "t_min" : 5, "t_count" : 2
    },
    ...
]
```

## Introduction of the approach

As shown in the figure below, the edge analysis / streaming data processing method is adopted. At the edge, we adopt the EMQ X approach, and finally output the calculation results to the IOT hub of Azure.

![emqx_azure.png](https://static.emqx.net/images/f0a51c534df9074aa3ed7d743737e746.png)

- EMQ X Edge can access devices with various protocol types, such as MQTT, CoAP, LwM2M, etc.. Therefore, users do not need to care about protocol adaptation; it is also lightweight and suitable for deployment on edge devices. 
- EMQ X Kuiper is a SQL-based lightweight edge streaming data analysis engine released by EMQ. The installation package is only about 7MB, which is very suitable for running on the edge device side.
- Azure IoT Hub provides a comprehensive approach of device access and data analysis, which is used for the result data access in the cloud and the result data analysis required by the application.

## Implementation steps

### Install EMQ X Edge & Kuiper

- At the time of this writing this article, the latest version of EMQ X Edge is 4.0, and users can install and launch EMQ X Edge via Docker.

  ```shell
  # docker pull emqx/emqx-edge
  # docker run -d --name emqx -p 1883:1883  emqx/emqx-edge:latest
  # docker ps
  CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                                                                                                           NAMES
  a348e3ac150c        emqx/emqx-edge:latest   "/usr/bin/docker-entr"   3 seconds ago       Up 2 seconds        4369/tcp, 5369/tcp, 6369/tcp, 8080/tcp, 8083-8084/tcp, 8883/tcp, 11883/tcp, 0.0.0.0:1883->1883/tcp, 18083/tcp   emqx
  ```

  The user can use the ``telnet`` command to determine whether the startup is successful, as shown below.

  ```shell
  # telnet localhost 1883
  Trying 127.0.0.1...
  Connected to localhost.
  Escape character is '^]'.
  ```

- Install and start Kuiper

  Click [here](https://github.com/emqx/kuiper/releases)  to download the latest version of Kuiper and unzip it. At the time of this writing this article, the latest version of Kuiper is 0.0.3.

  ```shell
  # unzip kuiper-linux-amd64-0.0.3.zip
  # cd kuiper
  # bin/server
  Serving Kuiper server on port 20498
  ```

  If it does not start, check the log file ``log/stream.log``.

### Create stream

Kuiper provides a command to manage streams and rules. Users can check which subcommands and helps are available by typing ``bin/cli`` in the command line window. The ``cli`` command is connected to the local Kuiper server by default. The ``cli`` command can also be connected to other Kuiper servers. Users can modify the connected Kuiper server in the ``etc/client.yaml`` configuration file. Users who want to know more about the command line can refer to [here](https://github.com/emqx/kuiper/tree/master/docs/cli).

Create a stream definition: The purpose of creating a stream is to define the format of the data sent to the stream,  which is similar to defining the structure of a table in a relational database. All supported data types in Kuiper can be found in [here](https://github.com/emqx/kuiper/blob/master/docs/streams.md).

```shell
# cd kuiper
# bin/cli create stream demo '(temperature float, humidity bigint) WITH (FORMAT="JSON", DATASOURCE="devices/+/messages")'
```

The above statement creates a stream definition called demo in Kuiper, which contains two fields, temperature and humidity. The data source is the subscribed topic``devices/+/messages``  to MQTT. Please note that the wildcard ``+ `` is used here to subscribe to messages from different devices. The MQTT server address corresponding to the data source is in the configuration file ``etc/mqtt_source.yaml``, which can be configured according to the server address. Configure the ``servers`` project as shown below.

```yaml
#Global MQTT configurations
default:
  qos: 1
  sharedsubscription: true
  servers: [tcp://127.0.0.1:1883]
```

The user can type the ``describe`` subcommand on the command line to check the stream definition just created.

```shell
# bin/cli describe stream demo
Connecting to 127.0.0.1:20498
Fields
--------------------------------------------------------------------------------
temperature	float
humidity	bigint

FORMAT: JSON
DATASOURCE: devices/+/messages
```

### Data business logic processing

Kuiper uses SQL to implement business logic. The average, maximum, minimum, and number of temperatures are counted every 10 seconds and grouped according to the device ID. The implemented SQL is shown below.

```sql
SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), "/", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)
```

The SQL here uses four aggregate functions to count the correlation values over a 10-second window period.

- ``avg``: average
- ``max``: maximum
- ``min``: minimum
- ``count``: Count

Two basic functions are also used.

- ``mqtt``: The information of the MQTT protocol is taken out from the message, and  mqtt (topic) is the name of the topic of the currently obtained message.
- ``split_value``: This function splits the first argument with the second argument, and then the third argument specifies the subscript to get the split value. So the function ``split_value("devices/001/messages", "/", 1) ``call returns ``001``

``GROUP BY`` is followed by the grouped fields, which are the calculated field ``device_id``; and the time window ``TUMBLINGWINDOW(ss, 10)``.  The time window  means that a batch of statistics data is generated every 10 seconds. 

### Debugging SQL

Before we  write the rules, we need to debug the rules. Kuiper provides debugging tools for SQL, which makes it very convenient for users to debug SQL.

- Go to the Kuiper installation directory and run ``bin/cli query``

- Enter the previously prepared SQL statement at the appeared command line prompt.

  ```shell
  # bin/cli query
  Connecting to 127.0.0.1:20498
  kuiper > SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), "/", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)
  query is submit successfully.
  kuiper >
  ```

  In the log file ``log/stream.log``, we can see that a temporary rule named ``internal-kuiper_query_rule`` has been created.

  ```
  ...
  time="2019-11-12T11:56:10+08:00" level=info msg="The connection to server tcp://10.211.55.6:1883 was established successfully" rule=internal-kuiper_query_rule
  time="2019-11-12T11:56:10+08:00" level=info msg="Successfully subscribe to topic devices/+/messages" rule=internal-kuiper_query_rule
  ```

  It is worth noting that this rule named ``internal-kuiper_query_rule`` is created by ``query``, and the server will check if the ``query`` client is online every 5 seconds, if ``query `` The client finds that there is no response for more than 10 seconds (such as being closed), then the internally created ``internal-kuiper_query_rule`` rule will be automatically deleted. After that, the following information will be printed in the log file.

  ```
  ...
  time="2019-11-12T12:04:08+08:00" level=info msg="The client seems no longer fetch the query result, stop the query now."
  time="2019-11-12T12:04:08+08:00" level=info msg="stop the query."
  time="2019-11-12T12:04:08+08:00" level=info msg="unary operator project cancelling...." rule=internal-kuiper_query_rule
  ...
  ```

- Send test data

  Send the following test data to EMQ X Edge via any test tool. The writer used JMeter's [MQTT plugin](https://github.com/emqx/mqtt-jmeter) during the test because JMeter can make some flexible automatic data generation, business logic control, and a large number of devices simulations and so on. Users can also use other clients such as ``mosquitto`` to simulate directly.

  - Topic: ``devices/$device_id/messages``, where ``$device_id`` is the first column in the data below
  - Message: ``{"temperature": $temperature, "humidity" : $humidity}``, where ``$temperature`` and ``$humidity`` are the second and third columns in the data below

  ```
  #device_id, temperature, humidity
  1,20,30
  2,31,40
  1,35,50
  2,20,30
  1,80,90
  2,45,20
  1,10,90
  2,12,30
  1,65,35
  2,55,32
  ```

  We can see that after sending the simulation data, two groups of data are printed in two 10-second time windows in the ``query`` client command line. The number of results output here is related to the frequency at which the user sends data. If Kuiper receives all the data in one time window, only one result is printed.

  ```json
  kuiper > [{"device_id":"1","t_av":45,"t_count":3,"t_max":80,"t_min":20},{"device_id":"2","t_av":25.5,"t_count":2,"t_max":31,"t_min":20}]
  
  [{"device_id":"2","t_av":37.333333333333336,"t_count":3,"t_max":55,"t_min":12},{"device_id":"1","t_av":37.5,"t_count":2,"t_max":65,"t_min":10}]
  ```

### Create and submit rules

After debugging the SQL, users start configuring the rules file and send the resulting data to the remote Azure IoT Hub via Kuiper's MQTT Sink. In Azure IoT Hub, users need to create the following content first.

- IoT Hub: The name created in this article is ``rockydemo``, which is used to access the device.
- IoT Device: It represents a device, here is the gateway for processing device data. The gateway is installed with Kuiper. After the relevant data is processed, the gateway sends the result to the Azure cloud.
- Device access username and password: Please refer to Azure [Related Documentation](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support) for Azure IoT MQTT connections Username and password. For generating SAS Token, users can refer to [this document](https://docs.microsoft.com/en-us/cli/azure/ext/azure-cli-iot-ext/iot/hub?view=azure-cli-latest#ext-azure-cli-iot-ext-az-iot-hub-generate-sas-token).

Related devices are created in the Azure IoT Hub as shown below.

![azure_iot.jpg](https://static.emqx.net/images/0479756329070c1415cb5a65ec36aaed.jpg)



**Write a Kuiper rules file**

A rule file is a text file that describes the logic of business processing (the SQL statement that has been debugged before) and the configuration of the sink (the destination of the message processing result). Most of the information about connecting to the Azure IoT Hub has been described in the previous section. Note that the value of ``protocol_version`` **MUST** be set to ``3.1.1``, not ``3.1``.

```json
{
  "sql": "SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), \"/\", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)",
  "actions": [
    {
      "log": {}
    },
    {
      "mqtt": {
        "server": "ssl://rockydemo.azure-devices.net:8883",
        "topic": "devices/demo_001/messages/events/",
        "protocol_version": "3.1.1",
        "qos": 1,
        "clientId": "demo_001",
        "username": "rockydemo.azure-devices.net/demo_001/?api-version=2018-06-30",
        "password": "SharedAccessSignature sr=*******************"
      }
    }
  ]
}
```

**Create rules via the Kuiper command line**

```shell
# bin/cli create rule rule1 -f rule1.txt
Connecting to 127.0.0.1:20498
Creating a new rule from file rule1.txt. 
Rule rule1 was created.
```

We can view the running connection status of the rule in the log file. If the configuration items are correct, we should see that the connection to the Azure IoT Hub is established successfully.

```
......
time="2019-11-12T14:30:34+08:00" level=info msg="The connection to server tcp://10.211.55.6:1883 was established successfully" rule=rule1
time="2019-11-12T14:30:34+08:00" level=info msg="Successfully subscribe to topic devices/+/messages" rule=rule1
time="2019-11-12T14:30:35+08:00" level=info msg="The connection to server ssl://rockydemo.azure-devices.net:8883 was established successfully" rule=rule1
......
```

- Start the Azure IoT Hub monitoring with the command ``az iot hub monitor-events -n rockydemo`` and send the same simulation data as the debug SQL statement to the local EMQ X Edge. After  processed by Kuiper, the corresponding processing results are sent to the Azure IoT Hub.

  ```shell
  #az iot hub monitor-events -n rockydemo
  Starting event monitor, use ctrl-c to stop...
  {
      "event": {
          "origin": "demo_001",
          "payload": "[{\"device_id\":\"2\",\"t_av\":32,\"t_count\":3,\"t_max\":45,\"t_min\":20},{\"device_id\":\"1\",\"t_av\":45,\"t_count\":3,\"t_max\":80,\"t_min\":20}]"
      }
  }
  {
      "event": {
          "origin": "demo_001",
          "payload": "[{\"device_id\":\"2\",\"t_av\":33.5,\"t_count\":2,\"t_max\":55,\"t_min\":12},{\"device_id\":\"1\",\"t_av\":37.5,\"t_count\":2,\"t_max\":65,\"t_min\":10}]"
      }
  }
  ```

## Summary

Through this article, readers can understand that the EMQ X solution at the edge can be used to develop a system based on edge data analysis very quickly and flexibly, achieving low data latency, low cost and safe processing. Azure IoT also offers the IoT Edge solution, comparing to Azure's solution,

- Kuiper's runtime is extremely lightweight. Azure IoT Edge requires related language runtime, and installation package deployed to edge devices is more heavy.
- Kuiper's SQL based business logic implementation is more quick and simple, but it lacks of flexibility when processing complex business logics. Azure IoT Edge is better than Kuiper at this point.
- Kuiper is more flexible to integrate with other 3rd party IoT Hubs, while Azure IoT Edge mostly can be only work with Azure IoT Hub. 

If you are interested in learning more about edge streaming data analysis, please refer to [Kuiper Open Source Project](https://github.com/emqx/kuiper).


------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.io) for details.
