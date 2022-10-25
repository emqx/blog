In this article, we will simulate temperature and humidity data and report it to the EMQX cloud on the GCP platform via the MQTT protocol, after which we will use the EMQX Cloud data integration to enable NAT gateway and save the data to the Timescale Cloud over the public network. 

## EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is the world's first fully managed MQTT 5.0 public cloud service for IoT from EMQ. It provides a one-stop O&M colocation and a unique isolated environment for MQTT services. In the era of Internet of Everything, EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation and persistence of IoT data.

![MQTT Cloud](https://assets.emqx.com/images/6996e8a78944b572621ceabca1830534.png)

With the infrastructure provided by cloud providers, EMQX Cloud is available in dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications.

For more information, please go to the [EMQX Cloud website ](https://www.emqx.com/en)or see the [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/).

## Timescale Cloud

[Timescale Cloud ](https://www.timescale.com/cloud/)is a hosted, cloud-native TimescaleDB service that allows you to quickly spin up new TimescaleDB instances. Powered by TimescaleDB, Timescale Cloud is an innovative and cost-effective way to store and analyze your time-series data. Get started super fast with demo data, or your own dataset, and enjoy the security of automated upgrades and backups.

## Create Deployments

### Create EMQX Cluster

[Create a GCP deployment](https://docs.emqx.com/en/cloud/latest/quick_start/create_free_trial.html) of EMQX Cloud, other options default.

![Create a GCP deployment](https://assets.emqx.com/images/3cb826c937ec34673ce17e1e17ec6852.png)

When the status is Running, the creation of the deployment is complete.

![Running status](https://assets.emqx.com/images/d91d81879de8b4f545e67a96ff381300.png)

### Create Timescale Cloud instances

If you are creating a Timescale Cloud instance for the first time, you can refer to the [help document](https://docs.timescale.com/getting-started/latest/). A service in Timescale Cloud is a cloud instance which contains your database. Each service contains a single database, named tsdb.

![Create Timescale Cloud instances](https://assets.emqx.com/images/42a9513aef3668482cca9bd84a20896a.png)
 
![Create Timescale Cloud instances](https://assets.emqx.com/images/f330ba69cdee0da95221c1f90ce4847a.png)
 
When you have a service up and running, you can connect to it from your local system using the psql command-line utility. If you've used PostgreSQL before, you might already have [psql installed](https://docs.timescale.com/timescaledb/latest/how-to-guides/connecting/psql/). If not, check out the installing psql section.

```
# install psql
sudo apt-get update
sudo apt-get install postgresql-client

# connect to your service
psql -x "postgres://{YOUR_USERNAME_HERE}:{YOUR_PASSWORD_HERE}@{YOUR_HOSTNAME_HERE}:{YOUR_PORT_HERE}/{YOUR_DB_HERE}"
```

![connect to your service](https://assets.emqx.com/images/9dc808cb11227bc5611e5149f2cc36ad.png)
 
To create a new table. Use the following SQL statement to create temp_hum table. This table will be used to save the temperature and humidity data reported by devices.

```
CREATE TABLE temp_hum (
    up_timestamp   TIMESTAMPTZ       NOT NULL,
    client_id      TEXT              NOT NULL,
    temp           DOUBLE PRECISION  NULL,
    hum            DOUBLE PRECISION  NULL
);

SELECT create_hypertable('temp_hum', 'up_timestamp');
```

![create_hypertable](https://assets.emqx.com/images/8710f9e8c14d63f91e8688f23435df0a.png)
 
Insert test data and view it.

```
INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) values (to_timestamp(1603963414), 'temp_hum-001', 19.1, 55);

select * from temp_hum;
```

![Insert test data and view it](https://assets.emqx.com/images/00a20f51365bcd86b77cb6f23617d1b4.png)

In the Timescale Cloud database instance, the default max_connections is 25, which needs to be changed to 100 to facilitate EMQX Cloud connections.

![Timescale Cloud](https://assets.emqx.com/images/9ca27b01a384414267798773f9533330.png)

 
## Enable NAT Gateway

[NAT gateways](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html#service-activation) can provide network address translation services to provide Professional deployments with the ability to access public network resources without the need for VPC peering connections.

![Enable NAT Gateway](https://assets.emqx.com/images/25029211050bd502629f47d0f49de884.png)
  

## [**Data Integrations**](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_confluent.html)

1. Create TimescaleDB resources

   Go to the Data Integrations page. On the data integration page, Click on TimescaleDB under the Data Persistence.

   ![Create TimescaleDB resources](https://assets.emqx.com/images/d60c337968d147fbbebb499fee287184.png)

   Fill in the timescaledb database information you have just created and click Test. If there is an error, you should check if the database configuration is correct. Then click on New to create TimescaleDB resource.

   ![New Resource](https://assets.emqx.com/images/7a226be1c960945634826ce7df2419d7.png)
 
2. Create a new rule

   Choose the TimescaleDB resource under Configured Resources, click on New Rule and enter the following rule to match the SQL statement.

   In the following rule we read the time up_timestamp when the message is reported, the client ID, the message body (Payload) from the temp_hum/emqx topic and the temperature and humidity from the message body respectively.

   ```
   SELECT
       payload.location as location, 
       payload.temp as temp, 
       payload.hum as hum
   FROM "temp_hum/emqx"
   ```

   ![Create a new rule](https://assets.emqx.com/images/ab5e25eb2ba117d0bd92174c01934529.png)
 
   You can click SQL Test under the SQL input box to fill in the data:

   - topic: temp_hum/emqx
   - payload:

   ```
   {
     "temp": 24.3,
     "hum":35.4
   }
   ```

   Click Test to view the obtained data results. If the settings are correct, the test output box should get the complete JSON data as follows:

   ![JSON data](https://assets.emqx.com/images/f3e81faab07e6195691cecbfd06de2b8.png)

   If the test fails, please check whether the SQL is compliant and whether the topic in the test is consistent with the SQL filled in.

3. Add Action to Rule

   Click on the Next button in the bottom to enter action view. Select the resource created in the first step and enter the following data to insert into the SQL template.

   ```
   INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) VALUES (to_timestamp(${up_timestamp}), ${client_id}, ${temp}, ${hum})
   ```

   ![Add Action to Rule](https://assets.emqx.com/images/8b79696d11651ee88e5ad92b596a1459.png)

4. View Resource Detail

   Click on the resource to see the detail.

   ![View Resource Detail](https://assets.emqx.com/images/79a93c34ad706af57cb19888c1a745d6.png)

5. Check Rule Monitoring

   Click the monitor icon of rule to see the metrics.

   ![Check Rule Monitoring](https://assets.emqx.com/images/67a8747ea1fca662add1f76f8ffd9b34.png)

## **Verification**

1. Use MQTTX to simulate temperature and humidity data reporting

   We recommend you to use [MQTT X](https://mqttx.app/), an elegant cross-platform MQTT 5.0 desktop client to subscribe/publish messages.

   Click on the add button and fill in the deployment information to connect to the deployment. You need to replace `broker.emqx.io` with the created deployment [connection address](https://docs.emqx.com/en/cloud/latest/deployments/view_deployment.html#view-deployment-information), add [client authentication information](https://docs.emqx.com/en/cloud/latest/deployments/auth.html#authentication) to the EMQX Cloud console. Enter the topic name and payload message to publish the message.

   ![MQTT Client](https://assets.emqx.com/images/220a77e00ad55b085c2880ca76ad51a6.png) 

2. View rules monitoring

   Check the rule monitoring and add one to the number of success.

   ![View rules monitoring](https://assets.emqx.com/images/13aa73265e1b6b624a6369ae4c4c4636.png)

3. View data dump results

   ```
   select * from temp_hum order by up_timestamp desc limit 10;
   ```

   ![View data dump results](https://assets.emqx.com/images/68c7a91866190bcb0bb4f1fdaf500b64.png)

So far, we have used EMQX Cloud data integration based on the GCP platform to save the entire process of data to the Timescale Cloud over the public network. 


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
