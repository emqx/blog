## Where to go after Google IoT Core?

Google's sudden announcement of shutting down its Cloud IoT Core service leaves customers very tight schedule to start exploring [alternative IoT technologies](https://www.emqx.com/en/blog/why-emqx-is-your-best-google-cloud-iot-core-alternative) and migrate their IoT applications and endpoints. Given that Google IoT Core is based on MQTT, the best alternative options for seamless migration undoubtedly are MQTT-based IoT messaging platforms or services.

Say you're a Google IoT Core user and have your own resources on GCP, such as Kafka / Confluent, Cloud SQL, MongoDB, or InfluxDB. [EMQX Cloud](https://www.emqx.com/en/cloud), a fully-managed MQTT service available on the Google Cloud Platform, and most importantly, support VPC peering on GCP, will be your perfect option in this case.

In this article, we will share how to bridge MQTT data from EMQX Cloud to Confluent Cloud on GCP. EMQX Cloud can connect to Google Cloud SQL and also supports connecting with Confluent Cloud based on GCP's instances. From EMQX Cloud to Confluent Cloud to user's applications, they can all communicate with each other by establishing a peer-to-peer connection. This communication is under the same network, making it more secure and reliable as it's a private network connection. This Cloud-to-Cloud native connection allows users to enjoy the benefits of GCP infrastructure while completely avoiding vendor lock-in. 

To make it more vivid, we will simulate temperature and humidity data and report these data to EMQX Cloud via the MQTT protocol and then use the EMQX Cloud Data Integrations to bridge the data into Confluent Cloud based on the GCP platform.

![EMQX Cloud](https://assets.emqx.com/images/5d1dcdc21bfef496c024f826afbc531e.png)

## EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed MQTT service for IoT that enables users to connect IoT devices to any cloud without the burden of maintaining infrastructure. It’s the world's first fully managed MQTT 5.0 public cloud service, as well as the first and only one that supports all three major public cloud platforms, including GCP, AWS, and Azure.

EMQX Cloud provides a one-stop O&M colocation and a unique isolated environment for MQTT services. In the era of Internet of Everything, EMQX Cloud can help you quickly build industry applications and easily realize the connection, movement, processing, and analytics of IoT data.

![EMQX Cloud](https://assets.emqx.com/images/9b310ed9072c9ab0b0a3fe5f140f945a.png)
 
With the infrastructure provided by cloud providers, EMQX Cloud is available in dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services to build and grow your business-critical IoT applications.
For more information, please visit the [EMQX Cloud website](https://www.emqx.com/en) or see the [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/).

 
## Confluent Cloud

[Confluent Cloud](https://docs.confluent.io/cloud/current/overview.html) is a fully managed Apache Kafka service, a Software-as-a-Service solution that allows developers to deploy Kafka-based solutions on all three major clouds: AWS, Azure and GCP. As a SaaS, it offers the latest stable version of Kafka (using the same set of open source APIs that developers are familiar with), high performance, multiple availability zones, and support for Java, Python, C, C++,.NET, and  Go clients.


## Create Deployments

### Create EMQX Cluster

Create a GCP deployment of EMQX Cloud, other options default.

![Create a GCP deployment of EMQX Cloud](https://assets.emqx.com/images/46f514dac1c8acd7f35cb26754980b4c.png)
 
When the status is Running, the creation of the deployment is complete.

![deployment status](https://assets.emqx.com/images/5e3afba8bc3198e2d77795afa9e4606a.png)

### Create Kafka Cluster

Create a dedicated version of Confluent Cloud that can support vpc peer-to-peer connections. If you are creating a Confluent Cloud instance for the first time, you can refer to the [help documentation](https://docs.confluent.io/cloud/current/get-started/index.html).


![Create Kafka Cluster 1](https://assets.emqx.com/images/c26639f223ea5fab0c5ff8d353dba354.png)

![Create Kafka Cluster 2](https://assets.emqx.com/images/2010280a7bbeb635fb3768de5ec5e391.png)

![Create Kafka Cluster 3](https://assets.emqx.com/images/816e02c9dd7da7fa35dddf3d7bcc64de.png)
 
Points to note are that EMQX Cloud does not accept CIDR in the range of 10.11.1.0/24 ~ 10.64.255.0/24.

![CIDR](https://assets.emqx.com/images/ac8a8b6420fe21c18fb03142412eb12e.png)
 
Next, we create [Confluent peer-to-peer connection](https://docs.confluent.io/cloud/current/networking/peering/gcp-peering.html#create-a-ccloud-network-in-in-gc) between a server on GCP and Confluent Cloud, and create a topic named emqx via the private network.

```
# Install Confluent CLI
sudo apt-get update -y && sudo apt-get dist-upgrade -y && sudo apt autoremove -y 
curl -sL --http1.1 https://cnfl.io/cli | sh -s -- -b /usr/local/bin
confluent update

# Environment preparation
confluent login --save
confluent environment use env-xxx
confluent kafka cluster use lkc-xxx

# Create an API key and secret for kafka authentication
confluent api-key create --resource lkc-xxx
confluent api-key use <API Key> --resource lkc-xxx

# Create a topic named emqx
confluent kafka topic create emqx
confluent kafka topic list

# Go to the confluent instance and view the emqx topic
confluent kafka topic consume -b emqx
```

![kafka create topic](https://assets.emqx.com/images/02755a46bb0bd5a941a97cf231a5879e.png)
 

## VPC Peering Setup

After the Confluent Cloud cluster has been created, we could add peering by the following steps:

1. Go to the Networking section of the Cluster settings page and click on the Add Peering button.

2. Fill in the vpc information, you could get the information from VPC Peering section of the deployment console.

   ![Add Peering](https://assets.emqx.com/images/e03231ff0328ae7200c72d7258b670e5.png)

   ![Fill in the vpc information](https://assets.emqx.com/images/6f9ba88b3fd0f4022d969ef7ac4470ed.png) 

Log in to EMQX Cloud console, go to the deployment details page, click the + VPC Peering Connection button, fill in the information.

**Project ID**: GCP Project ID of your peering VPC

**VPC ID**: Network Name of your peering VPC

The above information is available in your Confluent Cloud console.
 
![VPC Project ID](https://assets.emqx.com/images/321a575bfeb56cb96add2ff2f372d7ed.png)

![VPC Peering Connection](https://assets.emqx.com/images/bfa6e6b286facbba7a4da10ba66d8ffa.png)

When the vpc status turns to running, you successfully create the vpc peering connection.

![successfully create the vpc peering connection](https://assets.emqx.com/images/b8e64658f593ad3d24554f14d0fff2e1.png)


## Data Integrations

1. **Create Kafka resources**

   Go to the Data Integrations page. On the data integration page, click Kafka resources.

   ![click Kafka resources](https://assets.emqx.com/images/975003f9e2311312d216fa4330f51378.png)
 
   Fill in the Kafka connection details, and then click test. Please check the Kafka service if the test fails. Click the New button after the test is passed and you will see the Create Resource successfully message.

   ![Fill in the Kafka connection details](https://assets.emqx.com/images/ed774a7c6ae10a045e7a7c7163bfbf53.png)

2. **Create a new rule**

   Put the following SQL statement in the SQL input field. The device reporting message time (up timestamp), client ID, and message body (payload) will be retrieved from the temp hum/emqx subject in the SQL rule, and the device ambient temperature and humidity will be read from the message body.

   ```
   SELECT 
   timestamp as up_timestamp, 
   clientid as client_id,
   payload.temp as temp,
   payload.hum as hum
   FROM
   "temp_hum/emqx"
   ```

   ![Create a new rule](https://assets.emqx.com/images/9c8636aa240be3823c95ab047767235d.png)

   To see if the rule SQL fulfills our requirements, click SQL test and fill in the test payload, topic, and client information.

   ![SQL test](https://assets.emqx.com/images/5ef9a26a164c728f00ea5d27ce0a0039.png) 

3. **Add Action to Rule**

   Click Next to add a Kafka forwarding action to the rule once the SQL test succeeds. To demonstrate how to bridge the data reported by the device to Kafka, we'll utilize the following Kafka topic and message template.

   ```
   # kafka topic
   emqx

   # kafka message template 
   {"up_timestamp": ${up_timestamp}, "client_id": 
   ${client_id}, "temp": ${temp}, "hum": ${hum}}
   ```

   ![Add Action to Rule](https://assets.emqx.com/images/ff106a047febace585a536124423af30.png)


## Verification

1. Use MQTTX to simulate temperature and humidity data reporting

   You need to replace [broker.emqx.io](http://broker.emqx.io/) with the created deployment [connection address](https://docs.emqx.com/en/cloud/latest/create/overview.html#view-deployment-information), add [client authentication information](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication) to the EMQX Cloud console.

   ![MQTT X connection](https://assets.emqx.com/images/a03bd8c2fe2c42fbe55a48111dddb79b.png)

   ![MQTT X message](https://assets.emqx.com/images/c5f181acd6a1a5549f299e5cf1949f31.png) 

2. View data bridging results

   ![View data bridging results](https://assets.emqx.com/images/27d862870184433fb02697ab806d836a.png)
 
   ```
   confluent kafka topic consume -b emqx
   ```

   ![confluent kafka topic consume](https://assets.emqx.com/images/48d44a0b76adc06d16e00ce9b54f9a63.png)

So far, we have used EMQX Cloud data integration based on the GCP platform to bridge the entire process of data to the Confluent Cloud.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
