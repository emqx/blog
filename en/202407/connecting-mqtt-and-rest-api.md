## **Introduction**

[MQTT and HTTP](https://www.emqx.com/en/blog/mqtt-vs-http) are two mainstream protocols that play important roles in modern IoT and network communication. Although these two protocols have differences in design concept and application scenarios, we can fully leverage their advantages by combining them in actual projects to build high-efficiency and reliable communication systems. 

In this blog, we will delve into the application scenarios of combining MQTT and REST API, showcasing how to optimize system performance and improve user experience through practical cases.

## **What is MQTT**

The [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is commonly used in IoT applications to facilitate communication between devices in a lightweight and efficient manner. It uses a publish-subscribe model where devices can publish messages to a specific topic, and other devices can subscribe to that topic to receive the messages. This allows for real-time data exchange between devices in IoT networks.

## **What is REST API**

REST is an abbreviation for Representational State Transfer, which literally means to express the transfer of a state. REST API is a set of architectural rules, standards, or guidelines for building web application APIs. In other words, REST API is an architectural style that follows API principles. REST is specifically designed for web applications, with the aim of reducing development complexity and improving system scalability.

### Based on HTTP

The REST API uses the HTTP protocol for communication, utilizing HTTP methods such as GET, POST, PUT, Delete, etc. This design allows REST APIs to easily integrate with existing web technologies.
Example: Obtain resources through the GET method, create resources through the POST method, update resources through the PUT method, and delete resources through the Delete method.

### Resource Oriented

The REST API is resource-centric, with each resource having a unique URI (Uniform Resource identifier).
This resource-oriented design makes the API more intuitive and easy to understand. A user resource may have a URI '/users/{userId}', through which various operations can be performed, such as obtaining user information, updating user information, etc.

### Data Format

REST APIs typically transfer data using JSON or XML formats. JSON format is lightweight and easy to parse, while XML format is more rigorous and structured.

A typical JSON response may be:

```json
{
"id": 1,
"name": "John Doe",
"email": " john.doe@example.com "
}
```

### Security

The REST API can ensure the security of data transmission through HTTPS and supports various authentication mechanisms such as OAuth and API Key. These security features ensure the security and integrity of data transmission.

### Scalability

The design of the REST API makes it very flexible and scalable, suitable for various application scenarios. It is easy to add new resources and operations without affecting existing APIs. New endpoints can be added on top of existing APIs, such as '/users/{userId}/posts', to retrieve user posts.

## **The Uses of MQTT and REST API Integration**

Integrating MQTT and REST API can provide a robust and efficient solution for data exchange and communication in various applications. This integration can enable real-time data processing, automated workflows, and enhanced user experiences, making it an attractive solution for a wide range of industries, from industrial automation to smart home and beyond.

### **Data Collection and Processing**

The on-site equipment publishes real-time data through the MQTT protocol, and the central server receives and processes this data through the REST API interface. It combines the real-time performance of MQTT with the flexibility of REST API.

### **Device Control and Management**

The central server sends control commands through the REST API interface, and on-site devices receive and execute these commands through the MQTT protocol. This utilizes the ease of use of REST APIs and the efficiency of MQTT.

### **Alarm and Notification**

On-site devices release alarm information through the MQTT protocol, and the central server pushes the alarm information to users through the REST API interface. It combines the real-time performance of MQTT with the wide compatibility of REST APIs.

### **Data Synchronization**

The on-site equipment publishes real-time data through the MQTT protocol, and the central server synchronizes the data to other systems through the REST API interface. This utilizes the real-time performance of MQTT and the cross-platform compatibility of REST APIs.

### **Remote Configuration**

Users send configuration commands through the REST API interface, and on-site devices receive and apply these configurations through the MQTT protocol. By combining the ease of use of REST API with the efficiency of MQTT, remote configuration management can be achieved.

## Demo 1: Smart Home System Based on Temperature Monitoring

### How it Works

We set up a smart home system with a reliable method for reporting and checking temperature and humidity information in real time. This system relies on the collaboration between the MQTT protocol and the REST API. Temperature and humidity sensors installed in homes act as MQTT clients, constantly gathering real-time temperature and humidity data from the surroundings and sending this data to the EMQX message broker using the MQTT protocol.

As a high-performance messaging broker, EMQX is not only responsible for receiving MQTT messages from sensors, but also automatically extracts temperature and humidity data from these messages through its powerful rule engine, and securely saves them to the backend MySQL database.

Once the data is successfully stored in the MySQL database, users can access it through a web client. The web client uses the HTTP protocol to make requests to the server and queries the latest temperature and humidity information through the preset REST API interface. After receiving the request, the server will perform the corresponding database query operation, retrieve the latest temperature and humidity data from the MySQL database, and package this data in JSON or other easily parsed format in the HTTP response body to return to the web client. 

Finally, the web client parses this data and presents it in an intuitive way (such as charts, numbers, etc.) on the user interface, allowing users to view the temperature and humidity conditions of their home environment in real-time.

This process enables rapid reporting and storage of temperature and humidity data, along with user-friendly data query and display services, significantly enhancing the intelligence level and user experience of smart home systems.

This streamlined and efficient architecture leverages essential components, including:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for testing data generation.             |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.6.0+  | Used for message exchange between temperature and MySQL      |
| [MySQL](https://www.postgresql.org/)                     | 8.0+    | Used for message exchange between temperature and Mysql.     |
| [Grafana](https://grafana.com/)                          | 9.5.1+  | Used for storing and managing temperature data, as well as achieving real-time reporting of temperature and humidity information. |

### Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### Clone the Project Locally

Clone the [emqx/mqtt-api-to-mysql](https://github.com/emqx/mqtt-api-to-mysql) repository locally using Git:

```shell
git clone https://github.com/emqx/mqtt-api-to-mysql
cd mqtt-api-to-mysql
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
│   └── temp-data.json
├── grafana-provisioning
│   ├── dashboard.yaml
│   └── datasource.yaml
├── image
├── mqttx
│   └── temp-data.js
└── mysql
│   └── create-table.sql
└── python_scripts
    └── run.py
    └── test_pub.py
    └── test_sub.py
    └── connect.py
```

The codebase consists:

- The `emqx`  folder contains EMQX-MySQL integration configurations to automatically create connector, rule and action when launching EMQX.
- The `mqttx` folder offers a script to simulate temperature sensors connected to the EMQX and generate data.
- The `grafana-provisioning` folders contain configurations for temperature data.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

### Start MQTTX CLI, EMQX, and MySQL

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```shell
docker-compose -f  docker-compose.yml up 
```

The MQTTX CLI will emulate 5 device clients within EMQX, actively publishing real-time data such as the device's ID, temperature and humidity, to a specified topic. The data, formatted in JSON, is transmitted to the designated topic `mqttx/simulate/temp-data/{device_id}` at regular intervals.

This is an example of data published to EMQX:

```shell
{
  "temperature": 55.0,
  "humidity": 20.1,
  "device_id": "mqttx_8ff83e29_1"
}
```

Here are the MQTT API topics we used in scenarios：

```shell
mqttx/simulate/temp-data/{device_id}– for commands
mqttx/simulate/temp-data/response/{device_id} – for responses
```

### Store Temperature Data

EMQX will create a rule for receiving messages from each client. You can also modify this rule later to add custom processing using EMQX's [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html):

```sql
SELECT payload FROM "mqttx/simulate/#"
```

Once the rules have processed the data, EMQX will utilize rule actions to write the location data from the vehicle in the message payload to the `temp_data` table within MySQL's `temp_hum` database.

The EMQX MySQL data integration allows the insertion of data through SQL templates. This facilitates the effortless writing or updating of specific field data into corresponding tables and columns within the MySQL database. Such integration ensures flexible storage and management of data:

```sql
insert into temp_data(device_id, temperature, humidity) values (${payload.device_id}, ${payload.temperature}, ${payload.humidity})
```

### Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all vehicle location data. You can view the data with this command. After we start, we can see the corresponding log printing：

```shell
mqttx-simulate  | [7/9/2024] [7:42:10 AM] › ℹ  Published total: 16955, message rate: 5/s
mqttx           | [7/9/2024] [7:42:10 AM] › topic: mqttx/simulate/temp-data/mqttx_8ff83e29
mqttx           | payload: {"device_id":"mqttx_8ff83e29_5","temperature":89.73,"humidity":11.83,"id":"a21851cb-7c2a-4220-9e54-b7e70c2bada0","name":"temp_data_4"}
mqttx           | 
mqttx           | [7/9/2024] [7:42:11 AM] › topic: mqttx/simulate/temp-data/mqttx_8ff83e29
mqttx           | payload: {"device_id":"mqttx_8ff83e29_1","temperature":32.1,"humidity":29.19,"id":"621c2697-f2c5-4027-90b8-6e7317df7eca","name":"temp_data_0"}
mqttx           | 
mqttx           | [7/9/2024] [7:42:11 AM] › topic: mqttx/simulate/temp-data/mqttx_8ff83e29
mqttx           | payload: {"device_id":"mqttx_8ff83e29_4","temperature":35.54,"humidity":28.95,"id":"a528fb33-8281-479e-b9b4-37bfc75f5ebe","name":"temp_data_3"}
mqttx           | 
mqttx           | [7/9/2024] [7:42:11 AM] › topic: mqttx/simulate/temp-data/mqttx_8ff83e29
mqttx           | payload: {"device_id":"mqttx_8ff83e29_2","temperature":97.06,"humidity":97.03,"id":"0998fa4e-d965-47c3-be8f-ef79a85fbdae","name":"temp_data_1"}
mqttx           | 
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```shell
mqttx sub -t mqttx/simulate/temp-data/+
```

### Grafana Monitoring

When we start and log in to the Grafana monitoring platform, an intuitive and dynamic data display interface is immediately presented to us. Among them, the real-time updated temperature change trend chart depicts the change of temperature over time, enabling us to quickly grasp the dynamic temperature changes in the current environment, providing strong support for subsequent decision analysis.

![grafana](https://assets.emqx.com/images/3c443370f08718163cf19fb568dcb02f.png)

### **REST API Query for Temperature and Humidity**

When the web client needs to display the latest temperature and humidity information, it will send a request to the server through the REST API. This request usually includes some parameters, such as the time range of the query (if needed), or simply requesting the "latest" data

![REST API Query](https://assets.emqx.com/images/49c026c0d746f5acc9fd3573a71aab5e.png)

The database performs query operations based on API requests to retrieve the latest temperature information. This information is typically returned to the API in JSON, XML, or other structured data formats:

![API](https://assets.emqx.com/images/7e939e30db5f2222a703047a9c9565cf.png)

 

## **Demo 2: Simulating Temperature and Issue Commands**

### How it Works

In Flask applications, when a user accesses a specific address and calls the API of the EMQX MQTT broker to publish a message, it is necessary to first ensure that communication with EMQX can be carried out through the network. EMQX has provided a REST API to support message publishing.
To demonstrate, we will assume that EMQX supports message publishing through HTTP in some way (possibly through a built-in REST API or a third-party service integrated with EMQX).

### REST API

Simulate accessing a specific address in the Flask application, which calls EMQX's REST API through HTTP requests to publish messages: `http://127.0.0.1:18083/api/v5/publish`. The REST API requires authentication for this request (which can be configured in the dashboard):

```
API_URL = 'http://127.0.0.1:18083/api/v5/publish'
USERNAME = "REST API username"
PASSWORD = "REST API password"
```

We use the topic`mqttx/simulate/temp-data/response/` as the subject for sending messages, and this topic is the subject of the message you receive in the Flask application (in this case, through an HTTP POST request), and send this topic as part of the request body.

![rest api](https://assets.emqx.com/images/e86439bf1d0ae65921d5fb888c2feca8.png)

- Run the `run.py`  to start the Flask application.

  ```python
  MySQL Database connection successful
   * Serving Flask app 'run'
   * Debug mode: on
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on http://127.0.0.1:5000
  Press CTRL+C to quit
   * Restarting with stat
  MySQL Database connection successful
   * Debugger is active!
   * Debugger PIN: 927-610-582
  ```

- Use the MQTT client to subscribe to the topic 

  ```shell
  mqttx/simulate/temp-data/response/
  ```

- The `test_pub.py ` script sends the topic and payload to the Flask application through an HTTP POST request. The Flask application receives this data and checks if the topic is mqttx/simulate/temp data/response/. Then, it simulates publishing messages to EMQX REST API.

  ```shell
  python3 ./test_pub.py
  Status Code: 200
  {
    "id": "00061CDEEF51B2A28BD701005DCF0000"
  }
  ```

- Observe whether the MQTT client has received a message.

  ```shell
  python3 ./test_sub.py
  Connected with result code 0
  Received `{"status": "on", "message": "Turn on the air conditioning"}` from `mqttx/simulate/temp-data/response/` topic
  ```

- Similarly, we simulate shutting down the device during message issuance, and the client can receive the following message

  ![python main](https://assets.emqx.com/images/6a431b14f5f62ca2e2a7e9801b3b1ad9.png)

  ```python
  python3 ./test_sub.py
  Connected with result code 0
  Received `{"status": "off", "message": "Turn off the air conditioning"}` from `mqttx/simulate/temp-data/response/` topic
  ```

**Notice:**

- Authentication and Permissions: If the REST API of EMQX requires authentication, you need to set the corresponding authentication information in the HEADERS dictionary.
- Payload encoding: In some cases, the payload of MQTT messages needs to be in binary format or a specific encoding (such as base64). You need to adjust the payload field in the emqx_payload dictionary according to the requirements of EMQX.
- Error handling: In a production environment, you may need more complex error handling logic.
- Security: Ensure that your Flask application is deployed in a secure environment and configured appropriately to protect APIs from unauthorized access.

## **Conclusion**

In conclusion, mastering the integration of MQTT with REST APIs opens up a world of possibilities for real-time data transmission, efficient data processing, and seamless remote management. By leveraging the strengths of both MQTT's publish/subscribe model and REST API's request/response mode, developers can create robust and flexible solutions tailored to various application needs. Whether you are developing smart home systems, industrial automation solutions, or remote monitoring platforms, the synergy of MQTT and REST APIs offers a powerful foundation for your projects.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
