## Introduction

In today's interconnected world, the rise of connected devices is evident across various domains such as smart homes, autonomous vehicles, and automated factories. These devices constantly generate a vast amount of data in the form of messages and events. The collection, storage, and analysis of this data have become crucial for ensuring the stability and safety of these devices. In this blog post, we will demonstrate how to efficiently store device data in PostgreSQL by integrating [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) with PostgreSQL.

## What is PostgreSQL

PostgreSQL, also known as Postgres, is a robust open-source relational database management system famous for its reliability, extensibility, and advanced features. It's well-regarded for handling complex queries and data types, making it a popular choice for applications ranging from small projects to enterprise-level systems. PostgreSQL supports various data types, including JSON and XML, and features like ACID compliance, transactions, and multi-version concurrency control (MVCC) ensure data integrity and consistency. It also offers advanced features such as user-defined functions, triggers, and extensions, allowing users to tailor the database to meet specific needs. Known for its performance, scalability, and flexibility, PostgreSQL is a versatile and feature-rich database system widely used across industries.

## Benefits of MQTT to PostgreSQL Integration for IoT

Integrating MQTT with PostgreSQL for IoT applications offers several benefits, including: 

1. **Efficient Data Transfer**: MQTT is a lightweight and efficient messaging protocol designed for low-bandwidth, high-latency networks. By integrating MQTT with PostgreSQL, you can transfer IoT data efficiently and reliably to the database. 
2. **Real-time Data Processing**: MQTT enables real-time data transmission, allowing IoT devices to publish and subscribe to data streams. By integrating MQTT with PostgreSQL, you can process and store IoT data in real time, enabling instant insights and decision-making. 
3. **Data Persistence**: PostgreSQL is a robust and reliable open-source relational database management system. By integrating MQTT with PostgreSQL, you can ensure data persistence and durability, storing IoT data securely for future analysis and reference. 
4. **Data Analysis and Insights**: By storing IoT data in PostgreSQL, you can leverage the database's powerful querying and analytics capabilities to derive valuable insights from the data. Integration with PostgreSQL enables you to perform complex data analysis, reporting, and visualization for informed decision-making. 
5. **Data Security**: PostgreSQL offers advanced security features such as role-based access control, data encryption, and authentication mechanisms. By integrating MQTT with PostgreSQL, you can ensure the security and integrity of your IoT data, protecting it from unauthorized access or tampering. 
6. **Simplified Development**: Integrating MQTT with PostgreSQL provides a streamlined development process for IoT applications. Developers can leverage the flexibility and scalability of PostgreSQL along with the lightweight messaging capabilities of MQTT to build robust and efficient IoT solutions. 

Overall, integrating MQTT with PostgreSQL for IoT applications offers a powerful combination of real-time data processing, scalability, data persistence, analytics capabilities, security, and simplified development, making it an ideal choice for IoT projects that require efficient data management and analysis.

## Integrate MQTT to PostgreSQL Using EMQX

EMQX is a highly scalable and feature-rich MQTT broker designed for IoT and real-time messaging applications. EMQX supports seamless integration with PostgreSQL, empowering streamlined management of real-time data streams originating from IoT devices. This integration offers support for extensive data storage, precise query execution, and intricate data correlation analysis, all while upholding data integrity. Combining EMQX's efficient message routing capabilities with PostgreSQL's adaptable data model makes monitoring device statuses, tracking events, and auditing operations effortless. This synergy equips businesses with profound data insights and robust business intelligence support, enabling informed decision-making and operational excellence."

The PostgreSQL data integration feature in EMQX is designed to effortlessly connect MQTT-based IoT data with PostgreSQL's powerful data storage capabilities. With a built-in rule engine, this integration simplifies the process of transferring data from EMQX to PostgreSQL for storage and management, eliminating the need for complex coding.

The diagram below illustrates a typical architecture of data integration between EMQX and PostgreSQL:

![diagram](https://assets.emqx.com/images/c0251234b512bf6f3faf2d2a348c2607.png)

Ingesting MQTT data into PostgreSQL works as follows:

- **IoT Devices Connect to EMQX**: After IoT devices are successfully connected through the MQTT protocol, online events will be triggered. The events include information such as device ID, source IP address, and other attributes.
- **Message Publication and Reception**: The devices publish telemetry and status data to specific topics. When EMQX receives these messages, it initiates the matching process within its rules engine.
- **Rule Engine Processing Messages**: With the built-in rules engine, messages and events from specific sources can be processed based on topic matching. The rules engine matches the corresponding rules and processes messages and events, such as converting data formats, filtering out specific information, or enriching messages with contextual information.
- **Write to PostgreSQL**: The rule triggers the writing of messages to PostgreSQL. With the help of SQL templates, users can extract data from the rule processing results to construct SQL and send it to PostgreSQL for execution, so that specific fields of the message can be written or updated into the corresponding tables and columns of the database.

After the event and message data are written to PostgreSQL, you can connect to PostgreSQL to read the data for flexible application development, such as:

- Connect to visualization tools, such as Grafana, to generate charts based on data and show data changes.
- Connect to the device management system, view the device list and status, detect abnormal device behavior, and eliminate potential problems in a timely manner.

## MQTT to PostgreSQL Integration Demo

In this section, we will walk you through the process of leveraging EMQX to gather real-time location data from vehicles and seamlessly integrate it with PostgreSQL for storage and analysis purposes.

### Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### How it Works

This streamlined and efficient architecture leverages essential components, including:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for testing data generation.             |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | Used for message exchange between vehicles and PostgreSQL.   |
| [PostgreSQL](https://www.postgresql.org/)                | 13+     | A database for storing and managing vehicle data, as well as providing time aggregation and analysis capabilities for Grafana. |
| [Grafana](https://grafana.com/)                          | 9.5.1+  | A visualization platform for displaying and analyzing collected data. |

### Clone the Project Locally

Clone the [emqx/mqtt-to-postgres](https://github.com/emqx/mqtt-to-postgres) repository locally using Git:

```shell
git clone https://github.com/emqx/mqtt-to-postgres
cd mqtt-to-postgres
tree
.
├── LICENSE
├── README.md
├── docker-compose.yml
├── emqx
│   ├── api_secret
│   └── cluster.hocon
├── emqx-exporter
│   └── config
│       └── grafana-template
│           └── EMQX5-enterprise
├── grafana-dashboards
│   └── vehicle-location.json
├── grafana-provisioning
│   ├── dashboard.yaml
│   └── datasource.yaml
├── image
│   ├── mqtt-to-postgres.png
│   └── vehicle_location.png
├── mqttx
│   └── vehicle-location.js
└── postgres
    └── create-table.sql

11 directories, 12 files
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-PostgreSQL integration configurations to automatically create connector, rule and action when launching EMQX.
- The `mqttx` folder offers a script to simulate vehicle sensors connected to the EMQX and generate data.
- The `grafana-provisioning` folders contain configurations for visualizing vehicle location data.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

### Start MQTTX CLI, EMQX, and PostgreSQL

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```shell
docker-compose up -d 
```

The MQTTX CLI will emulate 5 vehicle clients within EMQX, actively publishing real-time data such as the vehicle's VIN, location coordinates (latitude and longitude), to a specified topic. The data, formatted in JSON, is transmitted to the designated topic `mqttx/simulate/vehicle-location/{clientid}` at regular intervals, showcasing the seamless flow of information between the vehicles and the system.

This is an example of data published to EMQX:

```json
{
  "vin":"1NXBR32E57Z812344",
  "latitude":42.3922,
  "longitude":42.303
}
```

### Store Vehicle Location Data

EMQX will create a rule for receiving messages from each client. You can also modify this rule later to add custom processing using EMQX's [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html):

```sql
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

Once the rules have processed the data, EMQX will utilize rule actions to write the location data from the vehicle in the message payload to the `vehicle_data` table within PostgreSQL's `vehicle_db` database.

The EMQX PostgreSQL data integration allows the insertion of data through SQL templates. This facilitates the effortless writing or updating of specific field data into corresponding tables and columns within the PostgreSQL database. Such integration ensures flexible storage and management of data:

```sql
insert into vehicle_location_data(vin, latitude, longitude)
values (${payload.vin}, ${payload.latitude}, ${payload.longitude})
```

### Log Events from Clients

Additionally, EMQX will create a rule to log the online and offline status of the clients connected to EMQX. This logging serves the purposes of device management and fault warning. If a client unexpectedly goes offline, immediate notification allows for prompt issue identification and resolution.

EMQX's rule engine extends support to the full MQTT device lifecycle event handling. You can also refer [here](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-events-and-fields.html#mqtt-events) for a comprehensive understanding and monitoring of various events through the rule engine.

```sql
SELECT
  *
FROM
  "$events/client_connected",  "$events/client_disconnected"
```

Upon successful connection or disconnection of a client, EMQX activates the rule and records the event in the `vehicle_events` table within PostgreSQL's `vehicle_db` database.

The recorded information encompasses the event name and client ID, with the event time being automatically generated by PostgreSQL:

```sql
insert into vehicle_events(clientid, event) values (${clientid},${event})
```

### Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all vehicle location data. You can view the data with this command:

```shell
docker logs -f mqttx 
[5/14/2024] [6:24:52 AM] › …  Connecting...
[5/14/2024] [6:24:52 AM] › ✔  Connected
[5/14/2024] [6:24:52 AM] › …  Subscribing to mqttx/simulate/#...
[5/14/2024] [6:24:52 AM] › ✔  Subscribed to mqttx/simulate/#
[5/14/2024] [6:24:53 AM] › topic: mqttx/simulate/vehicle-location/1NXBR32E57Z812341
payload: {"vin":"1NXBR32E57Z812341","latitude":-79.3737,"longitude":-143.3323}
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```shell
mqttx sub -t mqttx/simulate/vehicle-location/+
```

### View Vehicle Locations in Grafana

To view vehicle locations data in the Grafana dashboard, please open `http://localhost:3000/` in your browser and log in using the username `admin` and password `public`.

Once logged in successfully, click on the "Dashboards" page in the navigation bar of the homepage. Then, select the "EMQX Data Integration Demo - Vehicle Location" dashboard. This dashboard will show the current latitude and longitude of the first vehicle that has inserted its location data to PostgreSQL, it will also feature a map showcasing the historical location data of the vehicle, along with a table detailing the connected and disconnected events of all vehicles.

With these metrics, you can gain valuable insights into the current location of the vehicle, track its historical movements on a map, and monitor the connectivity status of all vehicles in a clear and organized manner.

![Grafana](https://assets.emqx.com/images/3588d02d28352b6c40ac38504a8fa9ee.png)

## Conclusion

In this blog post, we explore the integration of MQTT and PostgreSQL to develop a vehicle location monitoring application. By leveraging EMQX as a real-time MQTT Broker and seamlessly importing data into PostgreSQL, we aim to improve operational efficiency, reduce downtime, and enhance safety through data-driven analytics. This integration allows for real-time data processing and analysis, enabling informed decision-making and proactive maintenance strategies in the context of vehicle monitoring.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
