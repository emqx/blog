EMQX is an open-source, highly scalable MQTT Broker. EMQX is especially favored by IoT developers and real-time communication application developers due to its rich features and stability. EMQX 5 could support up to 100 million concurrent MQTT connections in a single cluster. A single server can transmit and process a million MQTT messages per second with a milliseconds-level of latency.

## The Importance of Evaluating MQTT Messaging Service Performance

In real business scenarios, many factors can affect the performance of MQTT messaging, such as hardware resources, OS parameters, and the QoS level used in communication. The different combinations of these factors make the real scenarios so varied that we can't just publish some simple performance test reports to summarize these complicated scenarios. Users need to run performance tests that are similar to their scenarios before making architecture design and application prototyping.

Therefore, it is more important for EMQ to help users master the performance testing methodology of MQTT Broker than to release performance data.

To reduce the difficulty and improve testing efficiency, in this tutorial, we will use XMeter Cloud, a fully managed MQTT load testing cloud service, which provides standard test scenarios such as connection tests and message throughput tests, as well as a set of configurable parameters. In addition, it also supports uploading custom scripts to test any scenario.

You can also use the open-source [JMeter](https://jmeter.apache.org/) to build a similar test environment, the test method and scripts in this tutorial are compatible with JMeter.

## Performance Test Scenarios and Results

We used XMeter Cloud to test the performance of EMQX in several different scenarios to demonstrate the actual impact of factors such as QoS level and Payload size on MQTT performance.

These tests were based on the open-source version of **EMQX v5.1.6** and used a cloud server with the following configuration:

- **CPU**: 4vCPUs (Intel Xeon Platinum 8378A CPU @ 3.00GHz)
- **Memory**: 8 GiB
- **System Disk**: General Purpose SSD | 40 GiB
- **Maximum Bandwidth**: 8 Gbit/s
- **Maximum Packets Per Second**: 800,000 PPS
- **OS**: CentOS 7.9

In addition, except for the fan-in scenario where XMeter Cloud used 20 test clients to send and receive messages, the number of test clients in other scenarios was 10.

### Test 1: Performance of EMQX with Different QoS

The higher the QoS level, the more complex the corresponding [MQTT packet](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) interaction process, so the system resources consumed to deliver the QoS message will be more. The performance overhead of different QoS is one of the hottest frequently asked questions.

In this scenario, 1,000 publishers and 1,000 subscribers used messages with a Payload size of 128 bytes for one-to-one communication. There were a total of 1,000 topics, and each topic had one publisher and one subscriber.

![01symmetric.png](https://assets.emqx.com/images/f4d1a0d5424ed9a3ed1c42708ef1ba90.png)

We gradually increased the workload by increasing the message publishing rate, and EMQX ran for 5 minutes under each workload to observe the stability of the running. We recorded the performance and resource consumption of EMQX under different QoS levels and different workloads, including but not limited to average message latency, P99 message latency, and average CPU usage.

The final test results are shown below:

![02symmetrictestresult01.png](https://assets.emqx.com/images/43786a0037e679b238f9538e196f015e.png)

![03symmetrictestresult02.png](https://assets.emqx.com/images/317611b9f4093e5755be3f415fadb1ff.png)

> Latency is the time it takes for a message to be received from the time it is published. Throughput consists of message inbound throughput and outbound throughput.

As we can see, the higher the QoS level, the higher the average CPU usage under the same workload. So, under the same system resources, a higher QoS usually means relatively lower throughput.

If we take the workload at an average CPU usage rate of around 75% as the recommended daily load, then we can conclude: under the test hardware specifications and testing scenarios, the recommended load for QoS 0 is approximately 57K TPS, for QoS 1 is approximately 40K TPS, and for QoS 2 is approximately 24K TPS. Here are the performance data for the test points that are closest to 75% CPU usage:

| **QoS Level** | **Recommended Workload, TPS (In + Out)** | **Average CPU Usage, % (1 - Idle)** | **Average Memory Usage, %** | **Average Letancy, ms** | **P99 Letancy, ms** |
| :------------ | :--------------------------------------- | :---------------------------------- | :-------------------------- | :---------------------- | :------------------ |
| QoS 0         | 60K                                      | 78.13                               | 6.27                        | 2.079                   | 8.327               |
| QoS 1         | 40K                                      | 75.56                               | 6.82                        | 2.356                   | 9.485               |
| QoS 2         | 20K                                      | 69.06                               | 6.39                        | 2.025                   | 8.702               |

### Test 2: Performance of EMQX with Different Payload Sizes

The larger the message payload, the more soft interruptions the OS needs to receive and send network packets, and the more computational resources EMQX needs to spend on serializing and deserializing packets. 

In most cases, the MQTT messages we send will not exceed 1KB. But in some scenarios, it is necessary to transmit larger messages. Thus we tested the performance impact of different Payload sizes.

Continue with one-to-one communication between 1,000 publishers and 1,000 subscribers. This time we set the QoS of the message to 1 and kept the publishing rate fixed at 20K msg/s. By increasing the Payload size to increase the test workload. EMQX ran for 5 minutes under each load to verify stability. We recorded the performance and resource usage of EMQX under each load. 

The results are shown below:

![04symmetricpayloadtestresult01.png](https://assets.emqx.com/images/b18d246aed26a2dd19781588a58a924b.png)

![05symmetricpayloadtestresult02.png](https://assets.emqx.com/images/f0cc77ce8e9dffdda1bd576326fd7395.png)

As the Payload increases, the CPU usage rate gradually rises, and the end-to-end delay of the messages also shows a relatively smooth increase. However, when the Payload size reaches 8KB, we can still obtain an average delay of less than 10 milliseconds and a P99 delay of less than 20 milliseconds.

| **Payload Size, KB** | **Recommended Workload, TPS (In + Out)** | **Average CPU Usage, % (1 - Idle)** | **Average Memory Usage, %** | **Average Letancy, ms** | **P99 Letancy, ms** |
| :------------------- | :--------------------------------------- | :---------------------------------- | :-------------------------- | :---------------------- | :------------------ |
| 1                    | 40K                                      | 75.9                                | 6.23                        | 3.282                   | 12.519              |
| 8                    | 40K                                      | 90.82                               | 9.38                        | 5.884                   | 17.435              |

This also tells us in addition to the QoS level, we also need to pay attention to the Payload size. If the actual Payload size in your case is much larger than the value used here, this means that you would need the hardware with a higher configuration.

### Test 3: Performance of EMQX with Different Publish-Subscribe Models

MQTT's publish-subscribe mechanism allows us to easily adjust the publish and subscribe model to meet the business requirements, such as the fan-in model in which a large number of sensor devices act as publishers and a small number of back-end applications or even a single back-end application acts as a subscriber to store and analyze the sensor data, or fan-out scenarios in which there are a small number of publishers and a large number of subscribers for message broadcasting, or symmetric scenarios in which publishers and subscribers need to communicate one-to-one.

However, the performance of the MQTT Broker in different publish-subscribe scenarios is often slightly different, as we will see in the following tests.

In the fan-in scenario, we set up 2,000 publishers and 100 subscribers, and every 100 publisher’s messages are consumed by 5 subscribers in a [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription).

![06fanin.png](https://assets.emqx.com/images/1d63c623208fa125a58b33baad1546d7.png)

In the fan-out scenario, we set up 10 publishers and 2,000 subscribers, with each publisher's messages being consumed by 200 subscribers in a normal subscription. The symmetric scenario remains the same as before.

![07fanout.png](https://assets.emqx.com/images/e836c5096bd6d95f73f98b18ef4193ed.png)

Since the inbound messages in the fan-out scenario are less than the other two scenarios, we set the total throughput to be the same or close to the same load and then compare them. For example, the fan-out scenario with 100 msg/s inbound and 20K msg/s outbound is equivalent to the symmetric scenario with 10K msgs/s inbound and 10K msgs/s outbound.

Keeping the QoS level of the message at 1 and the Payload size at 128 bytes, the final test results are as follows:

![08scenetestresult01.png](https://assets.emqx.com/images/4fcd92c785a40df5f21c2b6dc037fa98.png)

If we only consider message delay, the performance of the three scenarios is actually very close. And under the same load, the fan-out scenario always consumes less CPU. So if we take 75% CPU usage as the boundary, we can see quite intuitively that compared to the other two scenarios, fan-out can achieve a higher throughput.

![09scenetestresult02.png](https://assets.emqx.com/images/7d1d7cc516a60e57bf0dbafbda1af87c.png)

| **Scene** | **Recommended Workload, TPS (In + Out)** | **Average CPU Usage, % (1 - Idle)** | **Average Memory Usage, %** | **Average Letancy, ms** | **P99 Letancy, ms** |
| :-------- | :--------------------------------------- | :---------------------------------- | :-------------------------- | :---------------------- | :------------------ |
| Fan-In    | 30K                                      | 74.96                               | 6.71                        | 1.75                    | 7.651               |
| Fan-Out   | 50K                                      | 71.25                               | 6.41                        | 3.493                   | 8.614               |
| Symmetric | 40K                                      | 75.56                               | 6.82                        | 2.356                   | 9.485               |

### Test 4: Performance of EMQX with Bridging

MQTT bridging can bridge messages from one MQTT server to another, common use cases include bridging messages aggregated by edge gateways to servers in the cloud and letting messages flow between two MQTT clusters.

In this test scenario, messages published by 500 publishers connected to MQTT server 1 were bridged to MQTT server 2 and received by 500 subscribers connected to MQTT server 2. Meanwhile, messages published by another 500 publishers connected to MQTT server 2 were received by 500 subscribers connected to MQTT server 1.

This ensured that, with the same message publishing rate at the client, the inbound and outbound rate of messages in EMQX will be close to the symmetric scenario without bridging, so we can compare the performance differences between the two test cases.

![11bridge.png](https://assets.emqx.com/images/ad4421a0b0ca15a8090c454a89129953.png)

Keeping the QoS level of the message as 1 and the Payload size as 128 bytes, the final test results are as follows:

![12bridgetestresult01.png](https://assets.emqx.com/images/eecad12b14cbad237035569ee781721f.png)

![13bridgetestresult02.png](https://assets.emqx.com/images/7fc850cfd3102767a45f984ccdabc532.png)

Bridging introduces an additional relay in the process of message delivery, so the end-to-end delay of the message will increase. In addition, bridging also brings additional CPU consumption. Our test results have confirmed these two points. Taking the load when the average CPU usage is around 75%, which is about 25K TPS, as the recommended load for the bridging scenario under the hardware specifications of this test, the test results of the test point with the smallest difference in CPU usage are as follows:

| **Recommended Workload, TPS (In + Out)** | **Average CPU Usage, % (1 - Idle)** | **Average Memory Usage, %** | **Average Letancy, ms** | **P99 Letancy, ms** |
| :--------------------------------------- | :---------------------------------- | :-------------------------- | :---------------------- | :------------------ |
| 30K                                      | 82.09                               | 5.6                         | 5.547                   | 17.004              |

Next, we'll go into the detail of the test tools used and the test steps so that you can build your own test environment and reproduce all the test cases in this article, or test any other scenario you need.

## Test Tools

In all tests in this article, we used the following software or tools:

1. [EMQX](https://emqx.io/), an open-source, highly scalable MQTT Broker, designed specifically for IoT and real-time communication applications.
2. [XMeter Cloud](https://www.emqx.com/en/products/xmeter), a fully managed MQTT load testing cloud service, built on the Apache open source project JMeter, which can quickly run various MQTT load and scenario tests.
3. [collectd](https://github.com/collectd/collectd), a daemon running on the system that collects information such as CPU, memory, disk usage, and network traffic. We can send these collected data to the designated storage.
4. [InfluxDB](https://www.influxdata.com/), an open-source time-series database for storing and analyzing time-series data.
5. [Grafana](https://grafana.com/grafana/), an open-source data visualization and monitoring tool that converts data from a variety of data sources into aesthetically pleasing charts, graphs, and warnings.

## Setting up the test environment

First, we need to create two ECS instances on HUAWEI Cloud and the type is General computing-plus c7.

One server is used to run EMQX and collectd, and the other server is used to run InfluxDB and Grafana.

collectd is responsible for collecting system metrics such as CPU usage of the machine where EMQX is located and then sends these metrics to InfluxDB deployed on the other server, which stores the data. Finally, Grafana uses InfluxDB as a data source to display these metrics as charts.

![14testarchitecture.png](https://assets.emqx.com/images/bf6e33c1224e21cb62de48a16f36fcf9.png)

Next, we need to first complete the installation and configuration of these software on these two cloud servers, and then initiate the MQTT test from XMeter Cloud.

In this process, we will use some files, such as the template files for Grafana Dashboard and the test scripts used in XMeter Cloud, which we can download from [emqx/bootcamp](https://github.com/emqx/bootcamp) in GitHub.

### 1. Install and configure EMQX

Download and install EMQX version v5.1.6 on Server 1:

```
wget https://www.emqx.com/en/downloads/broker/5.1.6/emqx-5.1.6-el7-amd64.rpm
sudo yum install emqx-5.1.6-el7-amd64.rpm -y
```

Once the installation is complete, we can start EMQX, and in all performance tests of this article, unless otherwise specified, EMQX runs in the default configuration:

```
sudo systemctl start emqx
```

### 2. Install and configure collectd

Install collectd on Server 1:

```
yum install collectd -y
```

We need to use the CPU, Load, Interface, Memory plugins, which are used to collect the system metrics of CPU usage, CPU load, network traffic, and memory usage, respectively. These plugins are enabled by default, and we can find the following configuration in the `/etc/collectd.conf`:

```
LoadPlugin cpu
...
LoadPlugin interface
...
LoadPlugin load
...
LoadPlugin memory
```

The CPU plugin for collectd reports CPU usage per core by default and uses CPU Jiffies. We want it to directly report the percentage after averaging across all cores, so we need to add the following configuration to the config file:

```
<Plugin cpu>
  ReportByCpu false
  ReportByState true
  ValuesPercentage true
</Plugin>
```

Next, we need to configure collectd's Network plugin to allow collectd to send the collected performance metrics to InfluxDB on another server. We need to add the following configuration to `/etc/collectd.conf` to enable the Network plugin and send the performance metrics to the specified host and port:

```
LoadPlugin network
<Plugin network>
  Server "Your Hostname" "25826"
</Plugin>
```

After completing the above configuration, we start collectd:

```
systemctl start collectd
```

### 3. Install and configure InfluxDB

Install InfluxDB 1.8 on Server 2:

```
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.10.x86_64.rpm
sudo yum localinstall influxdb-1.8.10.x86_64.rpm -y
```

Please don't install InfluxDB 2.7 or later versions. These versions no longer directly support backup write protocols such as collected and Prometheus. We must use Telegraf to convert these protocols into Line Protocol before writing them into InfluxDB. So for simplicity, we directly install InfluxDB 1.8 which supports the collectd write protocol.

Next, we need to modify InfluxDB'configuration so that it can receive performance metrics sent by collectd and store them in the database. Open the InfluxDB configuration file `/etc/influxdb/influxdb.conf`, and change the configuration items in the `collectd` section to the following content.

```
[[collectd]]
  enabled = true
  bind-address = ":25826"
  database = "collectd"
  batch-size = 5000
  batch-pending = 10
  batch-timeout = "10s"
  read-buffer = 0
  typesdb = "/usr/share/collectd/types.db"
  security-level = "none"
  parse-multivalue-plugin = "split"
```

The above configuration means that InfluxDB will listen to the collectd data on port 25826 and write it into a database named collectd, which is automatically created by InfluxDB.

`typesdb` is required, it points to a `types.db` file that defines the collectd data source specification, which InfluxDB needs to understand the collectd data. You can get this file by installing collectd on your machine. `/usr/share/collectd/types.db` is the default path to the `types.db` file when you install collectd by yum, or you can get `types.db` from [here](https://github.com/collectd/collectd/blob/master/src/types.db).

Setting `security-level` to `none` means that collectd data will not be signed and encrypted, which is consistent with our configuration in collectd.

Setting `parse-multivalue-plugin` to `split` means that InfluxDB will store data with multiple values as multiple data points.

Next, start InfluxDB:

```
sudo systemctl start influxdb
```

We can verify that the collectd data is correctly written to InfluxDB with the following command:

```
$ influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
> use collectd
Using database collectd
> select * from cpu_value limit 8
name: cpu_value
time                host     type    type_instance value
----                ----     ----    ------------- -----
1692954741571911752 ecs-afc3 percent user          0.049981257028614265
1692954741571917449 ecs-afc3 percent system        0.024990628514307132
1692954741571923666 ecs-afc3 percent wait          0.024990628514307132
1692954741571932372 ecs-afc3 percent nice          0
1692954741571943586 ecs-afc3 percent interrupt     0
1692954741571947059 ecs-afc3 percent softirq       0
1692954741571947389 ecs-afc3 percent steal         0
1692954741571949536 ecs-afc3 percent idle          99.90003748594276
```

### 4.  Install and configure Grafana

Install Grafana in Server 2:

```
sudo yum install -y https://dl.grafana.com/oss/release/grafana-10.0.0-1.x86_64.rpm
```

Start Grafana:

```
systemctl start grafana-server
```

Next, we need to import a prepared Dashboard into Grafana. This Dashboard will provide four monitoring panels for CPU usage, CPU load, memory usage, and network traffic. Click [here](https://github.com/emqx/bootcamp/blob/main/mqtt-test-kit/Grafana-Dashboard.json) to download the Dashboard template file.

Before importing the Dashboard, we also need to make some modifications to `Grafana-Dashboard.json`. This is because we have added a judgment on the host field in each Query of the Grafana Dashboard in order to distinguish when there are multiple host data sources.

Search for `host::tag` in `Grafana-Dashboard.json`, and we will find the following content:

```
...
{
  "condition": "AND",
  "key": "host::tag",
  "operator": "=",
  "value": "ecs-afc3"
}
...
```

Just globally replace the host name `ecs-afc3` with our own host name. We can run the following command to view the hostname:

```
cat /proc/sys/kernel/hostname
```

Then, open a browser and type `<http://<hostname>>:3000` in the address bar to access Grafana, replacing `<hostname>` with the actual server address.

The default username and password for Grafana is `admin`. Grafana will ask us to change the default password when we log in for the first time. After logging in, we will first add InfluxDB as the data source, click `Add your first data source` on the home page:

![15addyourfirstdatasource.png](https://assets.emqx.com/images/5a784496d71f1a4a323721f9631fe112.png)

Find the InfluxDB data source, click to add this data source, and go to the configuration page:

![16addinfluxdb.png](https://assets.emqx.com/images/e818d4be3da7eddb8308e5103927a494.png)

Here we only need to pay attention to three configuration items:

1. URL, InfluxDB's HTTP service listens on port 8086 by default, and InfluxDB and Grafana are on the same server, so we'll configure it to `http://localhost:8086`[.](http://localhost:8086./)
2. Database, the database from which Grafana will read collectd data, so we configure it as `collected`.
3. HTTP Method specifies the HTTP method that Grafana will use to query InfluxDB for data, here we configure it as `GET`.

Click the `Save & test` button when you're done, and if the configuration is correct, you'll see a prompt `datasource is working. 7 measurements found`:

![17saveandtestinfluxdb.png](https://assets.emqx.com/images/751feb1978a349df1562d3e287d2aef7.png)

Click the plus sign in the upper right corner and select `Import dashboard`:

![18clickimportdashboard.png](https://assets.emqx.com/images/d212170058839346af0cdee275a0d1b5.png)

Import the modified `Grafana-Dashboard.json` file and select the InfluxDB data source we just added:

![19importdashboard.png](https://assets.emqx.com/images/ba743a21cdc2cfc530d991a1baee6b8d.png)

Click `Import` button to complete the import, we will see the following four monitoring charts, which show the current server CPU usage, memory usage, network send/receive traffic, and CPU load changes respectively:

![20grafanadashboardexample.png](https://assets.emqx.com/images/e446770276093d9fb23368b7655ba8bc.png)

### 5. System Tuning

Depending on the actual scale of the test, we may also need to adjust Linux kernel parameters and EMQX parameters. For example, when the number of our MQTT client connections exceeds 65535, we usually need to adjust parameters such as `fs.file-max` to increase the maximum number of file descriptors that EMQX can open. When the message throughput is large, we may need to adjust the size settings of the send and receive buffers to get better performance. You can refer to the [EMQX system tuning documentation](https://docs.emqx.com/en/emqx/latest/performance/tune.html).

However, all the test cases in this article do not require any additional tuning of Linux kernel parameters, neither for the number of client connections nor for the message throughput. So all the tests in the following article are done with the following default parameters:

```
fs.file-max = 761816
fs.nr_open = 1048576

net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 1024
net.core.netdev_max_backlog = 1000
net.core.rmem_max = 212992
net.core.wmem_max = 212992
net.ipv4.tcp_rmem = 4096 87380 6291456
net.ipv4.tcp_wmem = 4096 16384 4194304
net.ipv4.tcp_max_tw_buckets = 5000
```

### 6. Creating Tests in XMeter Cloud

After registering and logging in to [XMeter Cloud](https://www.emqx.com/en/products/xmeter) and going to the home page, we first need to switch to the **Professional Edition**. Only in the Professional Edition can we create customized test scenarios and peering connections between EMQX and XMeter Cloud. XMeter Cloud only supports peering with HUAWEI Cloud Platform now, we can contact the technical team of XMeter Cloud to help us do this. We will rollout XMeter Cloud to more public cloud providers in the future.

After the peering connection is created, we can click `Create Scenario` to upload our JMeter script and start testing.

There are four JMeter scripts we'll be using throughout the test: `Fan-In.jmx`, `Fan-Out.jmx`, `Symmetric.jmx`, and `Symmetric-Bridge.jmx`, which correspond to the Fan-In, Fan-Out, Symmetric, and Bridge scenarios, respectively. You can download these scripts [here](https://github.com/emqx/bootcamp/tree/main/mqtt-test-kit/scripts).

Each script provides custom variables that allow us to modify parameters such as QoS level, Payload size and message publishing rate. So when we test the performance curve of the MQTT Broker under different QoS, we only need one script, `Symmetric.jmx`.

Before submitting the test, XMeter Cloud will ask us to configure the following parameters:

![22configtestinxmeteren.png](https://assets.emqx.com/images/3f750b32552c8b27e8bd950ac871787f.png)

- **Name**: By default, XMeter Cloud will concatenate the test scenario name with the current time as the test name. You can change it to any name you prefer, as long as it does not confuse you among multiple tests.
- **Duration**: Set the duration of this test, here we set the duration to 5 minutes.
- **Total VU Number**: Set the number of virtual users per thread group, which is the number of MQTT clients, the thread groups depend on the actual content of the script. In the `Symmetric.jmx` script, we have added a thread group Pub for publishing messages and a thread group Sub for receiving messages. Here we set the number of virtual users for both Pub and Sub thread groups to 1000, so the total number is 2000.
- **Stress Region**: Set the VPC where the test machine will be created and the load will be initiated.
- **Ramp-Up Period**: Set how much time it needs to reach the maximum number of virtual users we set when running the test script. Here we set it to 20 seconds, that is, the test will initiate connections at a rate of 100 connections per second during the run.
- **Loop Mode**: Keep the default setting of `loop forever`. That is, the duration of the test run will be completely determined by the parameter `Duration`.
- **XMeter Runtime Variables**: The variables defined in our test script are listed here,  which allow us to fine-tune our test cases by modifying them, such as changing the QoS level of the message. The following are the custom variables provided by the `Symmetric.jmx` script:
  - **server**: The address of the MQTT server, which needs to be configured as the server's intranet address after creating the peer connection.
  - **host**: The listening port of the MQTT server.
  - **qos**: The QoS level used when the message is published. The maximum QoS for subscribers is fixed at 2, ensuring that QoS degradation does not occur.
  - **payload_size**: The Payload size of the message in bytes.
  - **target_throughput**: The target throughput, which refers to the total publishing rate of the messages. When we set the number of virtual users in the publisher thread group to 1000 and **target_throughput** to 10000, then each publisher will publish the message at 10 msgs/s.
  - **publisher_number**, etc.: In XMeter Cloud, these variables are overridden by the previous configurations, such as **Total VU Number** and **Ramp-Up Period**. So there is no need to care about them. They are only effective when we launch the test directly using JMeter.

After completing the above configurations, we can click `Next` to submit the test. During the running of the test, we can observe the real-time changes of throughput and response time in XMeter Cloud, and observe the CPU and other system resources usage of the server where EMQX is located in Grafana:

![24testreportinxmeteren.png](https://assets.emqx.com/images/9bb16d3df43434eb55e67b1c5dac083f.png)

### 7. Additional configurations for bridging scenarios

For the testing of the bridging scenario, we need an additional EMQX server.

![25testarchitecturewithbridge.png](https://assets.emqx.com/images/1921153a5087287441e570bbe016116e.png)

Apply for an ECS instance with the same specifications on HUAWEI Cloud, install EMQX and collectd by referring to the steps in the previous section, and then configure egress-direction MQTT bridging in each of the two EMQX as follows:

![26bridgeconfiguration.png](https://assets.emqx.com/images/4b37b823634ca98b08d4a8350a75a9e7.png)

Alternatively, add the following configuration to the `emqx.conf` configuration file. Note that the `server` needs to be configured as the host address of another EMQX:

```
bridges {
  mqtt {
    Demo {
      bridge_mode = false
      clean_start = true
      egress {
        local {topic = "bridge/#"}
        pool_size = 64
        remote {
          payload = "${payload}"
          qos = "${qos}"
          retain = "${flags.retain}"
          topic = "remote/${topic}"
        }
      }
      enable = true
      keepalive = 300s
      mode = cluster_shareload
      proto_ver = v5
      resource_opts {
        health_check_interval = 15s
        inflight_window = 100
        max_buffer_bytes = 1GB
        query_mode = async
        request_ttl = 45s
        worker_pool_size = "32"
      }
      retry_interval = 15s
      server = "172.16.0.20.1883"
      ssl {enable = false, verify = verify_peer}
    }
  }
}
```

After we install collectd in Server 3 and also dump the data into InfluxDB, we need to create a new Dashboard in Grafana to display the metric data of Server 3. The steps are the same as before, just modify the hostname in `Grafana-Dashboard.json` and then import it into Grafana.

## Differences between JMeter and XMeter Cloud in testing

All the test scripts we use in this article can be run in JMeter, we only need to install two plugins in JMeter. They are:

1. `mqtt-xmeter-2.0.2-jar-with-dependencies.jar,` this plugin provides JMeter with the ability to test the MQTT protocol. We can add samplers such as Connect Sampler, Pub Sampler and Sub Sampler to implement operations such as connecting, publishing, and subscribing in MQTT.

2. `xmeter-plugins-common-0.0.6-SNAPSHOT.jar`, this plugin provides a `__xmeterThroughput()` function, which we'll use in the Constant Throughput Timer. Its function is to convert our configured `target_throughput` into the target throughput per minute and then distribute it to each test machine according to the connection ratio. This is very useful when a single test machine cannot provide the target load.

   ![27xmeterfunction.png](https://assets.emqx.com/images/c1aa13f67727a6b27898256ccb28946b.png)

We can download the two plugins [here](https://github.com/emqx/bootcamp/tree/main/mqtt-test-kit/jmeter-plugins).

Compared with JMeter, XMeter Cloud comes with graphical test reports, so we can clearly see the change curves of each metric without having to install and configure additional software. Furthermore, in large-scale concurrent tests, XMeter Cloud can automatically allocate and release test machines, significantly shortening our preparation cycle compared to JMeter.

Note, however, that the tests in this article were done in the XMeter Cloud test environment. The main differences between this test environment and the online environment are as follows:

1. **Change from synchronous to asynchronous requests.** This will be more in line with the real load situation, and thus more accurate results will be measured.
2. **The unit of metrics, such as message latency, was changed from milliseconds to microseconds.** When the message latency is less than 1 millisecond, we can see the actual latency instead of 0.
3. **P95 and P99 message latency data is provided.** This provides a more visual measure of EMQX's performance.

All of the above changes will be updated to the official XMeter Cloud environment in the near future.

## Conclusion

In this article, we observed the excellent performance of EMQX. With a hardware specification of 4 cores and 8 GB, with 1000 publishers and 1000 subscribers using 128-byte size QoS 1 messages for one-to-one communication, EMQX can provide an end-to-end latency of around 15 ms for P99 messages with a message throughput of 60K TPS.

However, the performance curve of EMQX in different scenarios also reveals to us that the impact of factors such as QoS level and Payload size on the performance of MQTT Broker is indeed real. Therefore, it is very necessary to test and verify the performance of MQTT Broker according to the load requirements, hardware specifications, and function combinations in actual scenarios.

A suitable testing tool can help us greatly improve the testing efficiency. It needs to be able to simulate various scenarios and configurations but not be too complicated to use, and it also needs to provide enough metrics to help us get as comprehensive an understanding of the performance of the MQTT Broker as possible. So in this article, we described how we built our own test platform around XMeter Cloud and how we evaluated the performance of the MQTT Broker.

While all the tests in this article used the default kernel parameters of the OS, in your test scenario, you may need to tweak some parameters to achieve better system performance. After you have built your test platform, it will become straightforward to verify the effects of each kernel parameter by yourself. Of course, we will also bring more optimization suggestions for kernel parameters in subsequent blogs. You can also watch EMQ’s [bootcamp](https://github.com/emqx/bootcamp), where we will share more tutorials going forward.
