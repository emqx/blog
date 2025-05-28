As digital transformation accelerates, enterprises are increasingly challenged by the need to manage massive device connectivity and real-time data processing. EMQX and TDengine—two leading platforms in IoT connectivity and big data processing—are joining forces to deliver an end-to-end solution for industrial IoT, connected vehicles, energy management, and operations monitoring.

## Introduction to EMQX and TDengine

### EMQX: Enterprise-Grade Unified MQTT + AI Platform

EMQX is a cloud-native, distributed MQTT broker designed for high availability and scalability. It supports multiple messaging protocols and handles up to 5 million concurrent MQTT connections per node. EMQX provides end-to-end encryption, fine-grained access control, and real-time data transmission, making it an ideal messaging backbone for both IoT and AI applications while ensuring full compliance with enterprise data regulations.

### TDengine: High-Performance Time-Series Data Platform

TDengine is an enterprise-level, cloud-native time-series database optimized for IoT and IIoT use cases. It offers a simplified architecture with high performance and scalability, capable of ingesting, storing, analyzing, and distributing terabytes to petabytes of time-series data generated daily by connected devices. TDengine also enables AI-powered data analysis, including anomaly detection and forecasting, to unlock real-time business insights.

## Cloud-Native Integration: EMQX + TDengine

As strategic partners, EMQX and TDengine have achieved deep ecosystem integration for on-premises deployments. Now, their collaboration expands to the cloud. TDengine Cloud already supports MQTT data sources, enabling seamless connectivity with EMQX Cloud. With the release of EMQX Cloud version 5.2.13, a native connector for TDengine Cloud is now built in, completing the integration pipeline between the two platforms.

**Key Benefits of the Native Connector:**

- **Simplified Setup**: Streamlines the process of connecting time-series data to TDengine—no complex HTTP connector configuration required. Users can quickly configure connections via a user-friendly graphical interface.
- **Native Protocol Support**: Uses TDengine Cloud’s native protocol for direct data transmission, reducing overhead and improving performance.
- **High-Performance Data Ingestion**: Optimized transmission ensures reliable and efficient delivery of IoT data to TDengine Cloud.
- **Flexible Data Processing**: EMQX’s powerful rule engine allows filtering, transformation, and processing of data based on business logic.
- **Unified Configuration**: All integration settings are managed centrally in the EMQX Cloud console—no need to configure each system separately.
- **Visual Monitoring**: Integrated data flow monitoring provides clear visibility into system status and performance metrics.

In the next section, we’ll walk you through how to use this connector to stream MQTT data directly into TDengine Cloud.

## EMQX Cloud Configuration

### Preparation

1. EMQX Cloud Dedicated Deployment: You will need to register and create an EMQX Cloud Dedicated Deployment on the EMQX Cloud platform. (Free trial is available)
2. TDengine Cloud Account: You need to register and create a database instance on the TDengine Cloud platform. (Free trial is available)
3. Network Configuration: You need to open a NAT gateway for the EMQX Cloud deployment to allow it to access the TDengine Cloud instances over the public grid.

### Step 1: TDengine Cloud Preparations 

1. Log in to the TDengine Cloud console: [https://cloud.taosdata.com](https://cloud.taosdata.xn--com-9o0a./)

2. Create and deploy a TDengine Cloud service instance. 

3. After entering the instance, click “Data Browser” in the left menu bar. 

4. Create a database, e.g. “iot_data”. 

5. Create a table in the database:

   ```sql
   CREATE TABLE iot_data.temp_hum ( 
    ts TIMESTAMP, 
    clientid NCHAR(256), 
    temp FLOAT,
    hum FLOAT 
   );
   ```

   ![image.png](https://assets.emqx.com/images/c7f76f19416aabe8a4fc4906a1ce3700.png)

6. Obtain the connection URL and access token: **TDENGINE_CLOUD_URL**, **TDENGINE_CLOUD_TOKEN** values in the TDengine Cloud console for later use.

   ![image.png](https://assets.emqx.com/images/b50a02b1c1e9c38f6d36591677ab9908.png)

### Step 2: Create a TDengine Connector in EMQX Cloud

1. Log in to the EMQX Cloud Console at [Fully Managed MQTT Service for IoT](https://www.emqx.com/en/cloud).

2. In your deployment menu, go to **Data Integration**, and under the **Data Persistence** category, select TDengine.

3. Click Create Connector and fill in the following details:

   - **Connector Name**: Specify a name for the connector, e.g., `TDengine Cloud`.
   - **Host List**: Enter the connection address provided by TDengine Cloud (the value of `TDENGINE_CLOUD_URL`).
   - **Token**: Enter the access token obtained from TDengine Cloud (the value of `TDENGINE_CLOUD_TOKEN`).
   - Configure **Advanced Settings** as needed (optional).

4. Click the **Test Connection** button to verify the connection status. If successful, a message saying **Connector is available** will be displayed.

5. Click the **Create** button to complete the creation of the connector.

   ![image.png](https://assets.emqx.com/images/5c514308c3517e59d5795d3c3333c8fd.png)

### Step 3: Create a Data Integration Rule

1. In the list of connectors, click the **Create Rule** icon under the **Actions** column of the newly created connector, or go to the **Rules List** and click **Create Rule**.

2. In the **SQL Editor**, enter the rule to define the messages you want to process. For example:

   ```sql
   SELECT 
    now_timestamp('millisecond') as ts, 
    payload.temp as temp, 
    payload.hum as hum, 
    clientid 
   FROM 
   "devices/temp_hum" 
   ```

1. Click the **SQL Example** and **Enable Debugging** buttons to learn and test the results of the rule SQL (optional).

2. Click **Next** to proceed with creating the action.

   ![image.png](https://assets.emqx.com/images/6cafc3b3d1177378bfcd1b64c58a25a0.png)

### Step 4: Configure the Action

1. From the **Use Connector** dropdown, select the TDengine connector you just created.

2. **Database Name**: Enter the name of the database you created in TDengine Cloud, for example: `iot_data`.

3. Configure the **SQL Template** to write data into TDengine Cloud. For example:

   ```sql
   INSERT INTO iot_data.temp_hum(ts, temp, hum, clientid) VALUES (${ts}, ${temp}, ${hum}, '${clientid}')
   ```

4. Enable the **Treat Undefined Variables as NULL** option to ensure the rule engine handles undefined variables correctly.

5. Configure **Advanced Options** based on your business requirements, such as sync/async mode, batch parameters, etc. (Optional)

   Note: If your use case is not sensitive to latency (less than 1s), you can increase the **Maximum Batch Request Size** from 1 to 100 to improve write performance.

6. Click the **Confirm** button to complete the action configuration.

   ![image.png](https://assets.emqx.com/images/9569ac180a704631859b79b190b14d85.png)

7. In the pop-up message **"Rule Created Successfully"**, click **"Return to Rule List"** to complete the entire data integration setup.

### Step 5: Simulate Data Reporting

1. In the EMQX Cloud deployment menu, select **"Online Test"** and click **Connect**.
2. Subscribe to the topic **devices/temp_hum**.
3. Publish temperature and humidity data to the topic **devices/temp_hum**: `{"temp": 23, "hum": 90}`.

![image.png](https://assets.emqx.com/images/65a3bf00cf9806ee0dd527d54fdbe130.png)

### Step 6: Query Reported Data in TDengine Cloud

1. Visit the **Explorer** in TDengine Cloud Console Page.
2. Query the results of the reported data.

![image.png](https://assets.emqx.com/images/773fb1e611f747124817ba9caf46f28a.png)

You can see that the data has already been written into TDengine Cloud through EMQX Cloud.

For more detailed usage of the TDengine Cloud connector, please refer to: [Ingest MQTT Data into TDengine | EMQX Platform Docs](https://docs.emqx.com/en/cloud/latest/data_integration/tdengine.html) 

## TDengine Cloud Configuration

On the TDengine Cloud side, it is also possible to receive data from EMQX Cloud by deploying an MQTT data source. For detailed instructions, please refer to the official TDengine documentation:
[MQTT | TDengine Docs](https://docs.tdengine.com/advanced-features/data-connectors/mqtt/). As well as this blog post: [MQTT in TDengine | TDengine](https://tdengine.com/mqtt/).

## Final Notes

Currently, **EMQX Cloud only supports data transmission to TDengine Cloud via public network**. Support for **Private Link** connections will be added in the future to further enhance the integration experience between EMQX Cloud and TDengine Cloud.

In the face of the data deluge, the deep integration of EMQX and TDengine brings groundbreaking technical solutions to the industry. This collaboration not only establishes a high-performance foundation for massive data processing, but also redefines the infrastructure standards for industrial and IoT data through innovative architectural design — empowering enterprises with a strategic edge in digital transformation and unlocking a new era of intelligent development.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
