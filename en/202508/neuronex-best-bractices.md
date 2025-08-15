## **Introduction: The Value of IT and OT Data Convergence**

In the process of industrial digital transformation, the deep integration of IT (Information Technology) and OT (Operational Technology) is key to unlocking the full value of data. Real-time data from OT equipment, such as PLCs and CNC machines, reveals its true potential only when combined with business data from IT systems. These IT systems, including MES, ERP, or WMS, typically store critical contextual information—such as production work orders, material information, and quality standards—in relational databases like MySQL.

Effectively correlating real-time OT data with IT business data enables a range of high-value industrial applications:

- **Enhanced Quality Traceability**: Link precise equipment operating parameters with specific product work orders and batches.
- **Refined Production Analysis**: Achieve accurate OEE (Overall Equipment Effectiveness) measurement by combining work order schedules with real-time equipment output data.
- **Intelligent Maintenance Strategies**: Dynamically optimize predictive maintenance plans based on historical maintenance records from ERP systems and real-time operational conditions.

However, there is a common challenge: how to build an efficient and reliable data bridge to synchronize IT data stored in a MySQL database with an Industrial IoT (IIoT) platform. Traditional methods involving periodic full-table polling (`SELECT * FROM ...`) impose unnecessary performance pressure on production databases and generate significant data redundancy. Therefore, a more elegant and efficient solution is essential.

This blog details how to leverage the industrial edge platform **NeuronEX**, utilizing its built-in **incremental query** and **stream processing** capabilities, to achieve efficient and reliable data synchronization from MySQL to MQTT.

## **Objective and Architecture**

This practice aims to construct a data pipeline with the following capabilities:

1. **Automated Periodic Collection**: Automatically pull data from a MySQL database table.
2. **Incremental Data Fetching**: Collect only newly generated data, avoiding repetition and redundancy.
3. **Standardized Data Formatting**: Uniformly convert the collected data into JSON format.
4. **Reliable Data Reporting**: Publish data to an IIoT platform via the MQTT protocol (using the public EMQX Broker as an example).
5. **High Availability**: Ensure fault tolerance with the ability to resume synchronization from the last known point after a service interruption.

To achieve this objective, the technical architecture consists of three core components:

- **MySQL**: The source of business data.
- **NeuronEX**: The core engine responsible for data collection, incremental state management, processing, transformation, and forwarding.
- **EMQX (MQTT Broker)**: The data aggregation and distribution hub.

## **Implementation Steps**

For rapid validation, all components are deployed via Docker. You only need to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your local environment.

### **Environment Preparation**

Execute the following commands to start the required services:

```shell
# Start NeuronEX
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:3.6.0

# Start MySQL
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456  mysql:8.0
```

Additionally, prepare an MQTT client (e.g., [MQTTX](https://mqttx.app/)) for subsequent data validation.

### **Step 1: Initialize the Data Source (MySQL)**

First, create a sample data table in the MySQL database. The table design includes two key fields: an auto-incrementing `id` primary key and a `Time` timestamp. These fields will serve as the basis for implementing incremental queries.

```sql
-- Connect to MySQL
-- docker exec -it mysql mysql -u root -p

-- Create database and table
CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;
CREATE TABLE DeviceData ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    Time TIMESTAMP NOT NULL, 
    DeviceName VARCHAR(100) NOT NULL, 
    Current INT, 
    Voltage INT  
);

-- Insert initial data
INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:00', 'moter_A', 100, 200);
INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:05', 'moter_B', 120, 210);
INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:10', 'moter_C', 150, 220);
```

### **Step 2: Configure Incremental Query in NeuronEX (Core Mechanism)**

This step is the technical core of the solution. We will use the **SQL Source** feature of NeuronEX to achieve intelligent, incremental data collection.

NeuronEX's data processing engine is built around the concept of "Streams." We will first create a stream to represent the continuous flow of data from MySQL.

1. **Create a MySQL Connector**: In the NeuronEX UI, navigate to **Data Processing -> Configuration** and create a SQL connector pointing to your MySQL instance.

   ![image.png](https://assets.emqx.com/images/e63e4c420d659749dae70c5512a76862.png)

2. **Define the Incremental Query Stream**: Navigate to **Data Processing -> Source Management**, create a new SQL stream, and apply the following key configurations:

   - **Query Template**: Use a templated SQL statement with a placeholder, which NeuronEX will populate dynamically at runtime.

     ```sql
     SELECT * FROM DeviceData WHERE id > {{.id}};
     ```

   - **Index Field** : Specify the `id` field as the basis for the incremental query.

   - **Index Field Type** : Specify the type of index field.mn type for the indexField

   - **Index Init Value** : Define the starting point for the first query, which is `0` in this case.

   ![image.png](https://assets.emqx.com/images/890f173c5510ec52d1176dadcd8ed2bb.png)

**How It Works:**
The incremental query mechanism in NeuronEX is stateful. After executing the initial query (`WHERE id > 0`), the system automatically records the maximum `id` value from the returned result set (e.g., `3`). In the next polling cycle, NeuronEX replaces the `{{.id}}` placeholder with this value, dynamically generating and executing the new query (`WHERE id > 3`). This design transforms NeuronEX into a stateful data collector, ensuring that only new data is fetched, thereby significantly reducing the load on the source database and minimizing network overhead.

Furthermore, NeuronEX also supports incremental queries based on **timestamp fields**, providing flexible configuration options to adapt to various table designs. Please refer to the [documentation](https://docs.emqx.com/en/neuronex/latest/best-practise/sql-data.html) for details.

### **Step 3: Data Forwarding and Validation**

Once the data stream is successfully established, the next step is to route it to the target system.

1. **Create a Rule and Sink**: In the NeuronEX **Data Processing -> Rules** interface, create a rule to process the data:

   ```sql
   SELECT * FROM mysql_stream2 -- mysql_stream2 is the stream name created in the previous step
   ```

   Next, add an **MQTT Sink** (Action) to this rule and configure the target MQTT Broker address (`tcp://broker.emqx.io:1883`) and topic (`topic/mysql`).

   ![image.png](https://assets.emqx.com/images/321be0dce9845e082a72d912d0786ed1.png)

2. **Result Validation**:

   - Use an MQTTX client to subscribe to the `topic/mysql` topic.

   - Insert new records into the MySQL database:

     ```sql
     INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:30', 'moter_c', 601, 701);
     INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:40', 'moter_c', 602, 702);
     INSERT INTO DeviceData (Time, DeviceName, Current, Voltage) VALUES ('2025-07-23 09:00:50', 'moter_c', 603, 703);
     ```

   - Observe the MQTTX client. Within seconds, you will receive these new data records.

     ![image.png](https://assets.emqx.com/images/78654450b3516bcf67f047dbbc64522d.png)

### **Enhancing System Reliability: The Checkpoint Mechanism**

To ensure data consistency in the event of a system restart or network interruption, NeuronEX provides a **Checkpoint** mechanism. In the rule options, set the **QoS** to `At-Least-Once` (1) or `Exactly-Once` (2) and configure an appropriate **Checkpoint Interval**. NeuronEX will periodically persist the state of the incremental query index (`id` or `timestamp`), enabling seamless recovery from failures.

![image.png](https://assets.emqx.com/images/4557f0d7cc54ae52e45b2ebfe356ae98.png)

## **Conclusion**

Through this practice, we have demonstrated how to build a real-time, efficient, and reliable data bridge from a MySQL database to an IIoT platform using NeuronEX. Its core advantage lies in the stateful incremental polling mechanism, which achieves near-real-time data synchronization with minimal system overhead. For the complete configuration and usage steps of this article, please refer to the [document](https://docs.emqx.com/en/neuronex/latest/best-practise/sql-data.html).

In addition to MySQL, NeuronEX also supports data collection from databases such as SQLServer, PostgreSQL, SQLite, and Oracle. In real-world industrial scenarios, users can further leverage NeuronEX's powerful stream processing engine to perform real-time data cleansing, transformation, aggregation, and correlation (e.g., joining work order data from MySQL with equipment status data from a PLC). This allows for the delivery of high-value, context-rich data to upstream application systems.

NeuronEX is dedicated to breaking down data silos in industrial environments, helping enterprises build a unified and efficient data infrastructure to accelerate their digital transformation journey.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
