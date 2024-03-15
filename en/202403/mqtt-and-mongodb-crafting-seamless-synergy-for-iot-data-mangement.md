## Introduction

The rapid evolution of IoT and the increasing complexity of data management require more efficient and reliable methods of managing data. MongoDB, a high-performing NoSQL database, is widely adopted in IoT applications due to its flexible data model and high scalability. Pairing it with the [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) protocol, which can handle numerous connections while ensuring low bandwidth and latency, is crucial to the optimization of IoT applications.

This post will elaborate on the benefits and key use cases of MongoDB with MQTT in IoT scenarios. We will also provide a demonstration of integrating MQTT data into a MongoDB database to give readers a better understanding of how to implement this process.

## What is MongoDB?

MongoDB is a document database, aims to streamline application development and scalability. In contrast to conventional relational databases, which employ tables for data storage, MongoDB uses documents. This innovative approach enhances flexibility and helps MongoDB to adeptly accommodate evolving data patterns.

Document data usually comes in JSON, BSON, or XML formats, which are highly readable and scalable, and thus ideal for storing semi-structured or structured data. MongoDB implements various optimizations designed for document data to improve its performance and scalability. For example, MongoDB enables document compression, which reduces storage space needs. Moreover, MongoDB supports time partitioning, which simplifies the querying and analysis of timestamped data. MongoDB’s readability, scalability, and fast data ingestion and storage make it especially suitable for IoT scenarios.

## Benefits of MongoDB with MQTT in IoT Applications

Internet of Things devices generate a lot of diverse data, including telemetry data from sensors (usually in the form of time-series data), and client state and state changes (such as online status and current sensor values).

MongoDB boasts several distinctive advantages:

1. **Schemaless Document Storage:** Data in MongoDB is stored in a document format, allowing users to store data with diverse structures in the same database without the need to predefine table structures. Support for array and nested documents enhances flexibility in representing complex IoT data structures.
2. **Powerful Query Language:** MongoDB features a robust query language supporting a range of operations, including filtering, sorting, projection, aggregation, and so on.
3. **Distributed Database:** MongoDB easily scales horizontally, supporting distributed database deployment with automatic data sharding to handle large-scale IoT data. It seamlessly scales alongside EMQX clusters.
4. **Replication and Fault Tolerance:** MongoDB facilitates data replication by creating multiple copies, enhancing availability and fault tolerance. In the event of a primary node failure, the system seamlessly switches to a backup node.
5. **Time-series Data Processing:** Starting from MongoDB 5.0, the platform offers support for time-series data collection. This feature efficiently stores time-series data, reducing disk occupancy and processing complexity.

MongoDB has schemaless flexibility that sets it apart from relational and time-series databases. This means it can easily handle different kinds of data without predefined table structures. It also supports frequent inserts, updates, and flexible queries on structured data.

MongoDB has two main uses for the IoT domain. First, it can record the latest status and events of devices, such as online and offline status, and monitor their behavior and anomalies. This helps to improve device security management. Second, MongoDB has distributed storage, large-scale data processing, and rich query capabilities that make it a great solution for storing telemetry data. It also has special support for time-series data, which allows it to serve as a back-end engine for storing and analyzing telemetry data. This can be used for various big data analysis and data mining tasks, providing users with more value and insights.

MongoDB's flexibility and versatility make it a powerful tool for the development of IoT applications.

## Use Cases of MongoDB with MQTT

Here are some use cases of the integration of MongoDB with MQTT in different IoT scenarios:

- **Smart Home:** In the realm of IoT applications, smart homes stand out as a prominent use case. MongoDB plays a pivotal role by serving as a platform for storing and managing information related to smart home devices. It enables the real-time collection and storage of data from diverse sensors, facilitating intelligent control and optimization of smart home devices through data analysis and mining.
- **Smart City:** The concept of a Smart City involves the comprehensive and intelligent management of urban areas using IoT technology. Document databases, with MongoDB as a notable example, contribute significantly to smart cities. It proves valuable in storing diverse information related to equipment and vehicles in urban transportation systems, providing real-time traffic data, and supporting intelligent traffic control.
- **Industrial Automation:** Industrial automation leverages IoT technology to achieve real-time monitoring and control of industrial production environments through networked devices and sensors. MongoDB is employed to store and manage various data generated by industrial equipment, facilitating real-time scheduling and optimization of industrial processes.

## Integrating MQTT to MongoDB with EMQX

[EMQX](https://www.emqx.com/en/products/emqx) is a leading [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) that offers ready-to-use features and seamless integration with MongoDB. It can update and store various types of device event and message data, and help users to quickly develop different kinds of business applications.

The EMQX Data Integration component, in collaboration with MongoDB, offers the following features:

- **Full MQTT 5.0 Support:** Devices can connect to MongoDB using the [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) or 3.1.1 protocol through EMQX.
- **Rich Device Event Integration:** EMQX can record the complete lifecycle event data of devices, such as online and offline status, subscriptions, message publishing and delivery, to MongoDB. This enables continuous recording and rich monitoring.
- **Reliable Data Ingestion:** EMQX has message buffers to prevent data loss when MongoDB is not available.
- **Real-Time Data Transformation:** Employing an SQL-based rule engine, EMQX allows for the extraction, filtering, enrichment, and transformation of data in transit.
- **Real-Time Metrics and Monitoring:** EMQX can monitor the message transfers between the MQTT Broker and the time-series database in real-time.

Next, we will demonstrate how to collect sensor data from vehicles using EMQX and integrate with MongoDB for real-time data storage and analysis.

### Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### How it Works

This is a simple and effective architecture that utilizes the following key components:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for transportation vehicles data generation. |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | An MQTT broker used for message exchange between transportation vehicles and MongoDB. |
| [MongoDB](https://mongodb.com/)                          | 4.4.6+  | A database for storing and managing logistics data.          |

### Clone the Project Locally

Clone the [emqx/mqtt-to-mongodb](https://github.com/emqx/mqtt-to-mongodb) repository locally using Git:

```shell
git clone https://github.com/emqx/mqtt-to-mongodb
cd mqtt-to-mongodb
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-MongoDB integration configurations to automatically create rules and data bridges when launching EMQX.
- The `mongo` folder contains commands for initializing database users.
- The `mqttx/logistics.js` file offers scripts to simulate logistics and transportation fleets for real-world data publishing.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

### Start MQTTX CLI, EMQX, and MongoDB

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```shell
docker-compose up -d 
```

MQTTX CLI will simulate five vehicles connecting to EMQX. They will periodically publish their trip and cargo sensor data to EMQX at a consistent rate of 1 message per second. The data in JSON format will be sent to the topic `mqttx/simulate/logistics/{clientid}`.

The data contains the following information:

| **Data Name**    | **Description**                                              |
| :--------------- | :----------------------------------------------------------- |
| car_id           | Unique identifier for the vehicle                            |
| display_name     | User-friendly display name for easy identification           |
| model            | Vehicle model                                                |
| latitude         | Real-time latitude coordinate of the vehicle                 |
| longitude        | Real-time longitude coordinate of the vehicle                |
| speed            | Current speed of the vehicle (km/h), which can be used to analyze whether the vehicle is speeding or stuck in traffic |
| distance         | Driving mileage for vehicle maintenance and records (km)     |
| direction        | Driving direction                                            |
| tyre_pressure    | Tyre pressure for all tyres (kPa) in array format            |
| warehouse        | Temperature and humidity data for warehouse environment      |
| fuel_consumption | Real-time fuel consumption per 100 km (L/100 km), which can be used for transportation cost management |
| shift_state      | Vehicle gear for driving behavior analysis                   |
| state            | Running state of the vehicle                                 |
| power            | Engine power (kW)                                            |
| windows_open     | Window status                                                |
| doors_open       | Door status                                                  |
| inside_temp      | Inside temperature                                           |
| outside_temp     | Outside temperature                                          |
| timestamp        | Timestamp                                                    |

This is an example of data published to EMQX:

```json
{
    "car_id": "XCRHFDSBFPL011940",
    "display_name": "car_1",
    "model": "J7",
    "latitude": 166.7460400818362,
    "longitude": 142.5736913214525,
    "speed": 74,
    "distance": 20.555555555555557,
    "direction": 46,
    "tyre_pressure": [
        496.2,
        466.4,
        449.6,
        443,
        473.8,
        458.6,
        496.3,
        536.2,
        480.7,
        532.4
    ],
    "warehouse": {
        "humidity": 18.9,
        "temperature": 49.1
    },
    "fuel_consumption": 12.58,
    "shift_state": "D7",
    "state": "moving",
    "power": 288,
    "windows_open": true,
    "doors_open": false,
    "inside_temp": 28.1,
    "outside_temp": -3.8,
    "timestamp": 1699608487632
}
```

EMQX will create a rule to receive messages from each vehicle, necessitating special handling of fields through the `mongo_data` function. This is essential to ensure the correct formatting of time-based data when writing to MongoDB. You can also modify this rule later to add custom processing using EMQX's [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html):

```sql
SELECT
  *,  json_decode(payload) as payload,
  mongo_date(payload.timestamp) as mongo_ts
FROM
  "mqttx/simulate/#"
```

After the rules process the data, EMQX will insert the vehicle data from the message payload into the MongoDB through data bridges. Data Bridging's write templates can accommodate customized data structures, allowing for the storage of complex data formats when combined with MongoDB's flexible document data structure.

### Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all vehicle data. You can view the data with this command:

```shell
$ docker logs -f mqttx
[11/10/2023] [2023-11-10] [17:28:06] › topic: mqttx/simulate/logistics/mqttx_ee9e6f9e
payload: {"car_id":"XCRHFDSBFPL011940","display_name":"car_1","model":"J7","latitude":151.95961085265282,"longitude":128.29460259535088,"speed":114,"distance":31.666666666666668,"direction":26,"tyre_pressure":[441.1,577.9,510.1,466.4,496.1,556.1,469.2...
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```shell
mqttx sub -t mqttx/simulate/logistics/+
```

### View Data in MongoDB

You can use the following command to view data in MongoDB:

```shell
docker exec -it mongo mongo

# switch to the iot_data database
> use iot_data;
switched to db iot_data

# auth with the admin user
> db.auth('admin', 'public')
1

# query data from the truck_data collection
> db.truck_data.find();
{ "_id" : ObjectId("64b4dff9a59af20001000001"), "car_id" : "JK4LWAFDS5DZ18160", "direction" : 8, "display_name" : "car_1", "distance" : 28.6111111111, "doors_open" : false, "fuel_consumption" : 23.69, "inside_temp" : 34.8, "latitude" : 125.4242590552, "longitude" : 78.7727677446, "model" : "J7", "outside_temp" : 48.9, "power" : 61, "shift_state" : "D11", "speed" : 103, "state" : "moving", "timestamp" : ISODate("2023-07-17T06:30:17.598Z"), "windows_open" : true }
...
```

By integrating this data with visualization tools like Tableau or Grafana, data warehouses, or other data analytics products, you can leverage the power of fleet data to optimize operations and decision-making.

## Conclusion

The fusion of MQTT and EMQX with MongoDB offers a robust solution for IoT device management and message storage. EMQX stands out as the preferred option for contemporary IoT projects, boasting high reliability, scalability, and impressive message throughput. Paired with MongoDB's exceptional schemaless flexibility and distributed storage capabilities, this combination efficiently stores and manages IoT data. Together, they enable the effective storage and management of IoT data, leading to a more comprehensive extraction of data value.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
