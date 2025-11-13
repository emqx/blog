The proliferation of IoT devices demands robust, scalable solutions for collecting, processing, and analyzing massive streams of real-time data. [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) has long been the protocol of choice for efficient device-to-cloud communication, and now, the challenge shifts to seamlessly funneling this critical operational data into a powerful analytics platform. This is where **Google BigQuery** shines as a highly scalable, serverless data warehouse. 

With the recent release of **EMQX 6.0**, this integration becomes more direct and powerful than ever before, featuring a **data integration capability specifically for BigQuery**. 

This tutorial will guide you step-by-step through leveraging EMQX 6.0 to establish a high-performance pipeline, enabling you to ingest real-time MQTT data directly into BigQuery for immediate analysis and actionable insights.

## **Prerequisites**

Before you begin, make sure you have:

- An active Google Cloud Platform (GCP) account with BigQuery API enabled.
- EMQX 6.0 Enterprise Edition downloaded and running.
- A test MQTT client (such as [MQTTX](https://mqttx.app/)) installed.

## **Part 1: Prepare Your BigQuery Environment**

Let’s get BigQuery ready to receive MQTT data from EMQX.
We’ll create a service account, a dataset, and a table to store the streaming data.

### **Step 1. Create a GCP Service Account and Key**

To allow EMQX to authenticate with BigQuery, we’ll use a Service Account with the right permissions.

1. In the Google Cloud Console, go to IAM & Admin → Service Accounts → Create Service Account.
2. Enter a name and description.
3. Grant the BigQuery Data Editor role for access to datasets and tables.
4. After creation, click the Keys tab → Add Key → Create new key → select JSON.
5. Download the key file and store it securely. EMQX will use this file for authentication.

![image.png](https://assets.emqx.com/images/86d3f1e255f74156f3cf74197af9830b.png)

### **Step 2. Create a Dataset and Table in BigQuery**

1. In your GCP Console, go to BigQuery.

2. At the top of the Explorer panel, click the blue + CREATE DATASET button.

3. In the pop-up window, fill in the following:

   - Dataset ID: iot_data (you can choose any name)
   - Data location: US (multiple regions of the United States)
   - Keep other options as default

4. Click Create dataset.

   ![image.png](https://assets.emqx.com/images/011eb4eed5e4886394cb2efe404c6808.png)

Next, create a table inside the dataset:

1. Click the dataset name iot_data, then click + CREATE TABLE.
   - Source: Empty Table
   - Table name: mqtt_messages
2. Define the schema. Click Edit as text and paste the following:
   - clientid: string,
   - payload: bytes,
   - topic: string,
   - publish_received_at:timestamp

![image.png](https://assets.emqx.com/images/8161d91058b591c9b3fff6546ac2d160.png)

### **Step 3. Assign Permissions**

Now, give your Service Account permission to write to this dataset.

1. Select your dataset → click Share dataset.
2. Add your service account email.
3. Assign the following roles:
   - BigQuery Data Viewer (read)
   - BigQuery Data Editor (read/write)

![image.png](https://assets.emqx.com/images/a75eee44a49ae8924dce23919d137428.png)

### **Step 4. Test Table Access**

Open the BigQuery SQL editor and verify that your table is accessible:

```
SELECT * FROM `emqx-x-cloud.iot_data.emqx_messages` LIMIT 1000;
```

![image.png](https://assets.emqx.com/images/68bc8127a17dae6bfc94ba67c093dfcc.png)

## **Part 2: Configure the EMQX Data Integration**

Now that BigQuery is ready, we’ll configure EMQX to stream MQTT data directly into your dataset.
Everything can be done visually through the EMQX Dashboard—no coding required.

### **Step 1. Create the BigQuery Connector**

1. Log in to the EMQX Dashboard.
2. Go to Integration → Connector.
3. Click Create in the top-right corner.
4. Select BigQuery from the connector list.
5. Fill in the details:
   - Name: my_bigquery
   - Description: optional
6. Under GCP Service Account Credentials, upload the JSON key file you downloaded earlier.
7. Click Test Connectivity to confirm the connection works.
8. Once successful, click Create.

![image.png](https://assets.emqx.com/images/1f7dc9bb99288126108cfa6b9c4f43f1.png)

![image.png](https://assets.emqx.com/images/fd25984bda571663f71b01e45ef8c033.png)

### **Step 2. Create a Rule to Process Data**

Next, define how EMQX should handle and transform incoming MQTT messages.

1. Go to Integration → Rules → Create.

2. Enter Rule ID: my_rule.

3. In the SQL Editor, add the following: 

   ```sql
   SELECT
     clientid,
     base64_encode(payload) AS payload,  -- Encode the string as Base64
     topic,
     format_date(
       'millisecond',  -- Input unit is milliseconds
       'Z',            -- Output in UTC
       '%Y-%m-%d %H:%M:%S.%3N+00:00',  -- BigQuery TIMESTAMP acceptable format
       publish_received_at
     ) AS publish_received_at
   FROM "t/#"
   
   ```

 This rule filters messages from the topic t/bq and prepares them for insertion into BigQuery. 

![image.png](https://assets.emqx.com/images/a382fba898c3b08172fd885665c2c388.png)

### **Step 3. Add the Action**

Now we link this rule to the BigQuery connector.

1. Click Add Action → Create Action.
2. Set the following fields:
   - Type of Action: BigQuery
   - Action: bq_action
   - Connector: my_bigquery
   - Dataset: iot_data
   - Table: emqx_messages
3. Click Test Connectivity again to ensure it can reach BigQuery.
4. Click Create to finalize the configuration.

![image.png](https://assets.emqx.com/images/790111f121d841ce2287bd2e43c62442.png)

## **Part 3: Test and Verify in Real Time**

### **Step 1. Publish an MQTT Message**

Use MQTTX or any MQTT client to publish a test message to the topic you configured.

![image.png](https://assets.emqx.com/images/9a3f5389de84cd16c3243682968476b5.png)

### **Step 2. Verify the Data in BigQuery**

Go back to your BigQuery Console and query your table:

```sql
SELECT * FROM `emq-x-cloud.iot_data.emqx_messages` LIMIT 1000;
```

You should instantly see your test data appear, no batch jobs, no waiting.

![image.png](https://assets.emqx.com/images/2fb6d3395f86227244863aaeeed43076.png)

## **Unlock Your Real-Time Data**

In just a few simple steps, you’ve built a real-time data pipeline connecting your IoT devices to Google BigQuery. No complex ETL jobs. No delays. Just instant insights from your MQTT data — ready to visualize in Looker Studio, Grafana, or any BI tool of your choice.

With EMQX 6.0’s BigQuery Connector, you can finally harness the power of streaming IoT data for immediate analytics and smarter decisions.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
