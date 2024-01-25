## Introduction

Intelligent logistics, powered by the Internet of Things (IoT), is transforming the logistics sector. EMQX and MongoDB offer a smart solution for data collection in this industry. EMQX is an enterprise [MQTT platform](https://www.emqx.com/en/blog/mqtt-platform-essential-features-and-use-cases) that collects data from various sensors on vehicles and aggregates it across different processes. MongoDB is a database that aggregates and analyzes the data. The cooperation of both enables the monitoring of vehicle and cargo conditions, the optimization of distribution routes, and the management of cargo loading and dispatching.

This solution provides logistics enterprises with a solid basis for decision-making. It helps them improve transportation efficiency, lower transportation costs, and increase service quality and customer satisfaction.

This blog will demonstrate how EMQX collects sensor data from vehicles and integrates with MongoDB for real-time data storage and analysis.

## Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## How it Works

This is a simple and effective architecture that utilizes the following key components:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for transportation vehicles data generation. |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | An MQTT broker used for message exchange between transportation vehicles and MongoDB. |
| [MongoDB](https://mongodb.com/)                          | 4.4.6+  | A database for storing and managing logistics data.          |

## Clone the Project Locally

Clone the [emqx/mqtt-to-mongodb](https://github.com/emqx/mqtt-to-mongodb) repository locally using Git:

```
git clone https://github.com/emqx/mqtt-to-mongodb
cd mqtt-to-mongodb
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-MongoDB integration configurations to automatically create rules and data bridges when launching EMQX.
- The `mongo` folder contains commands for initializing database users.
- The `mqttx/logistics.js` file offers scripts to simulate logistics and transportation fleets for real-world data publishing.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

## Start MQTTX CLI, EMQX, and MongoDB

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```
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

```
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

```
SELECT
  *,  json_decode(payload) as payload,
  mongo_date(payload.timestamp) as mongo_ts
FROM
  "mqttx/simulate/#"
```

After the rules process the data, EMQX will insert the vehicle data from the message payload into the MongoDB through data bridges. Data Bridging's write templates can accommodate customized data structures, allowing for the storage of complex data formats when combined with MongoDB's flexible document data structure.

## Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all vehicle data. You can view the data with this command:

```
$ docker logs -f mqttx
[11/10/2023] [2023-11-10] [17:28:06] › topic: mqttx/simulate/logistics/mqttx_ee9e6f9e
payload: {"car_id":"XCRHFDSBFPL011940","display_name":"car_1","model":"J7","latitude":151.95961085265282,"longitude":128.29460259535088,"speed":114,"distance":31.666666666666668,"direction":26,"tyre_pressure":[441.1,577.9,510.1,466.4,496.1,556.1,469.2...
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```
mqttx sub -t mqttx/simulate/IEM/+
```

## Conclusion

In this blog, we discuss how to build intelligent logistics data collection applications. We use EMQX as a real-time MQTT Broker and its data integration function that writes data to MongoDB. This way, we integrate the two systems and leverage their advantages.

Our objective is to create a platform that aggregates and shares logistics data. The platform can be used for collecting, processing, storing, and analyzing data related to various aspects of logistics transportation management. By leveraging the reliability of EMQX and the flexible storage and rich analytic capabilities of MongoDB, we can extract valuable insights from different types of data.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
