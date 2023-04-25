Google Cloud IoT Core will be retired on August 16, 2023. As this date approaches, many users are looking for new solutions for their existing IoT businesses, and EMQX Enterprise is an ideal choice to achieve this goal.

[EMQX Enterprise](https://www.emqx.com/en/products/emqx) is a large-scale distributed MQTT messaging platform that can be deployed on the Google Cloud Platform (GCP) in multiple ways. You can easily and quickly migrate your devices on IoT Core to EMQX Enterprise and then continue to integrate with your data services in GCP, without affecting the existing business.

To migrate your business from IoT Core to EMQX Enterprise, you basically have three steps to go: 

1. Create an EMQX cluster on GCP.

2. Connect your devices to EMQX cluster.

3. Integrate your data with GCP Pub/Sub.

To start with, this article will guide you through the process of deploying EMQX Enterprise on GCP and then test the publishing and subscription of the migrated services.

![GCP IoT Core Migration](https://assets.emqx.com/images/b6f165320268d0442e7d8f54dcd1396d.png)

## Create a Virtual Machine Instance on GCP

Before deploying EMQX enterprise, let’s first create a Virtual Machine on GCP. 

GCP Virtual Machine Instances allow users to easily deploy and manage applications without creating and managing servers locally.

Here are the steps for creating a VM instance on GCP. You can also refer to the [Create and start a VM instance](https://cloud.google.com/compute/docs/instances/create-start-instance#console) guide.

1. Log in to the GCP console and click **Create a VM**.

   ![Click Create a VM](https://assets.emqx.com/images/65ad0976cb2fcabfa39cca33d424d52d.png)

2. If you have not created a VM instance before, you will be redirected to the **Compute Engine API** page. Click **ENABLE** to enable the Compute Engine API and continue with the creation process.

   ![Click ENABLE](https://assets.emqx.com/images/416547aae47c0f35a92806856a9f7265.png)

3. Check the **New VM instance** option to start the instance configuration

   Choose an appropriate region and zone and machine configuration. In **Machine configuration**, select `E2` for **Series** and `Custom` for **Machine type**, and allocate 2 vCPUs and 4GB of memory. With this specification, a single EMQX node can handle up to 10,000 MQTT connections and a maximum of 5,000 TPS of concurrent messages.

   You can use the [EMQX Server Estimate](https://www.emqx.com/en/server-estimate) calculator to calculate the recommended hardware specification under various maximum connections and message throughputs.

   ![Machine Configuration](https://assets.emqx.com/images/2e7988af28f289968483bebba0293107.png)

   In the **Boot disk** configuration, select the **Ubuntu 20.04 LTS** operating system and change the disk size to **30GB**.

   ![Machine Configuration](https://assets.emqx.com/images/6025f6b49f8b16a7174b5af47c095eba.png)

   ![Boot disk](https://assets.emqx.com/images/7a4dcc28282f4340777cabce994577ff.png)

4. Keep the rest of the configurations as default, and click **CREATE** to start the creating process.


## Install EMQX Enterprise

We will deploy EMQX Enterprise with the SSH tool from GCP. Before that, we need to get the download address and installation command from the EMQX website. 

In this example, we will deploy EMQX 4.4.16 on Ubuntu 20.04, with an amd64 CPU architecture. You can go to the page [Download EMQX Enterprise](https://www.emqx.com/en/try?product=enterprise) to get the required information.

![Download EMQX Enterprise](https://assets.emqx.com/images/9e645cf32d7f91ed11854a5a095b3782.png)

![Download EMQX Enterprise](https://assets.emqx.com/images/ff6e611ef1bbeb0b98dc8911e1ef8ad5.png)

1. Log in to the[ GCP console](https://console.cloud.google.com/) and click **Navigation menu** → **PRODUCTS** → **COMPUTE** → **Compute Engine** → **VM Instances** to enter the list of VM instances.

   ![VM Instances](https://assets.emqx.com/images/9f7231925cabd144d2487972eacaa8ac.png)

2. Find the VM instance you created and you will see that GCP has assigned a unique external IP address to it. Click on **SSH** to open your SSH terminal.

   ![Click SSH](https://assets.emqx.com/images/61dd39bf81b8cd40ae413451cee73ef6.png)

3. In the SSH terminal, enter the root directory and follow the installation commands provided on the download page.

   To enter the root directory, you can use the following command:

   ```
   sudo su
   cd ../../
   ```

   Download EMQX Enterprise using the `wget`:

   ```
   wget https://www.emqx.com/en/downloads/enterprise/4.4.16/emqx-ee-4.4.16-otp24.3.4.2-1-ubuntu20.04-amd64.deb
   ```

   ![Wget EMQX](https://assets.emqx.com/images/96a0fe683f535fc47dff93b0605450a2.png)

   Install EMQX Enterprise:

   ```
   sudo apt install ./emqx-ee-4.4.16-otp24.3.4.2-1-ubuntu20.04-amd64.deb
   ```

   ![Install EMQX Enterprise:](https://assets.emqx.com/images/f7f175c26b85ff0f720a2f2410c48cfc.png)

   Start EMQX Enterprise:

   ```
   sudo systemctl start emqx
   ```

   Congratulations! You have completed the installation of EMQX Enterprise on the GCP VM instance.

## Opening Firewall Ports on GCP

After you have installed the service or application on GCP, you need to manually open the required ports to access it from outside. Follow these steps to open the required ports on GCP.

1. Log in to the [GCP console](https://console.cloud.google.com/) and click **Navigation menu** → **PRODUCTS** → **VPC network** → **Firewall** to enter the Firewall page.

   ![Firewall](https://assets.emqx.com/images/23c57de80c5a730e22090a3504cf9e8f.png)

2. Click **CREATE FIREWALL RULE.**

   ![CREATE FIREWALL RULE](https://assets.emqx.com/images/0ad9614543af84c0242e1a1cea8daaa3.png)

3. Fill in the following fields to create a firewall rule:

   - **Name:** Enter a name for the rule.
   - **Network:** Select **default**.
   - **Priority:** Enter a priority number. The lower the number, the higher the priority. Enter **1000** here.
   - **Direction of traffic**: Select **Ingress**, which means receiving data on specific ports.
   - **Action on match**: Select **Allow** to allow traffic to pass through.
   - **Targets:** Select **All instances in the network** to apply the rule to all instances in the network.
   - **Source filter:** Choose the source filter as **IPv4 ranges** if you want to receive data from all networks or users.
   - **Source IPv4 ranges:** IP address **0.0.0.0/0** means that anyone can send data. You can also configure rules to receive data from specific IP addresses.
   - **Protocols and ports**: If you want to open all ports, select **Allow all**. Otherwise, open the specified TCP ports. You can open multiple ports simultaneously by separating them with commas. Here, enter 1883, 8883, 8083, 8084, 18083, and 8081.

   ![Firewall rule](https://assets.emqx.com/images/74aadd48ed0145d91ab1fa25f106319e.png)

4. Click **CREATE** to create the firewall rule. You will see the rule you created in the list.

   ![Firewall rule](https://assets.emqx.com/images/5cdc08a7abb3da60d6ebf90ca4265a8e.png)

## Quick Test with MQTT X Client

Now you have completed the installation of EMQX Enterprise on GCP and opened all the required ports. Here are the connection details:

| Server address         | 34.xxx.xxx.xxx<br>Please replace it with your actual VM Instance public IP address. |
| :--------------------- | ------------------------------------------------------------ |
| TCP Port               | 1883                                                         |
| WebSocket Port         | 8083                                                         |
| SSL/TLS Port           | 8883                                                         |
| WebSocket SSL/TLS Port | 8084                                                         |
| Dashboard Port         | 18083                                                        |
| REST API Port          | 8081                                                         |

We will use [MQTT X](https://mqttx.app/) to simulate the access of IoT MQTT devices and quickly test whether the server is available.

> [MQTT X](https://mqttx.app/) is a cross-platform MQTT 5.0 client tool open-sourced by EMQ. It supports macOS, Linux, and Windows, has rich features, and allows you to easily test MQTT/TCP, MQTT/TLS, and MQTT/WebSocket connections through MQTT X's one-click connection method and graphical interface.
>
> [MQTT X Web](https://mqttx.app/web) is the browser version of MQTT X, which eliminates the need for downloading and installation. You can quickly connect to the MQTT server via WebSocket by simply opening the browser.

1. Access the [MQTT X Web](http://www.emqx.io/online-mqtt-client#/recent_connections) page and click **New Connection** or the **+** icon on the menu bar to create a connection.

   ![New Connection](https://assets.emqx.com/images/99bdfb1838f377b7f080472bbc6f8287.png)

2. To configure and establish an MQTT connection, you only need to configure:

   - **Name**: Connection name, such as **GCP EMQX Enterprise**.
   - **Host:**
     - Select the connection type as **ws://**, as MQTT X Web only supports WebSocket protocol. If you want to test SSL/TLS authentication connections, please download the [MQTT X client](https://mqttx.app/)
     - Enter the VM instance public IP address.
   - **Port**: **8083**, which is the port corresponding to the WebSockets protocol.

   Leave other options at their default settings. You can keep the default settings for the rest fields or set as per your business needs. The corresponding configuration instructions can be found in the [MQTT X Manual - Quick Connect](https://mqttx.app/docs/get-started).

   After configuration, click **Connect** in the upper right corner of the page to establish the connection.

   ![Click Connect](https://assets.emqx.com/images/13292ad1c2064d6d4acc857b69bc5371.png)

3. Subscribe to a topic and publish a message to complete the message publish/subscribe test.

   - Click **New Subscription**, enter **testtopic/1** in the pop-up box, and subscribe to it.
   - Enter **testtopic/1** as the topic in the message-sending box, and use default values for other fields.
   - Click the send button at the lower right corner of the Payload input box, and the message will be successfully sent in the chat window.
   - Almost simultaneously, a new message will be received in the chat window, indicating that the publish/subscribe test has been completed.

   ![Publish/subscribe testing](https://assets.emqx.com/images/d6170f0c4b6ed709e90eee12bbd7b94d.png)

   After completing device connection and message publish/subscribe testing, you can also open the EMQX Dashboard in your browser by visiting `http://<ip>:18083` and logging in with the default credentials: username **admin** and password **public**.

   On the Dashboard, you can easily manage and monitor EMQX, manage the device list, and configure various functions such as security and data integration.

   ![MQTT Dashboard](https://assets.emqx.com/images/c89d4450a91b1c7af3b2955bdf1b6a4f.png)

## Summary

Now we have learned how to deploy EMQX Enterprise on GCP. To use EMQX Enterprise in production, we suggest you continue to create an [EMQX cluster](https://docs.emqx.com/en/enterprise/v4.4/advanced/cluster.html) through the [VPC network](https://cloud.google.com/vpc/docs/vpc) for better scalability and availability.

In addition to manual installation, you can also deploy EMQX Enterprise on GCP through [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) and [EMQX Terraform](https://www.emqx.com/en/emqx-terraform). We also highly recommend the fully managed MQTT message cloud service [EMQX Cloud](https://www.emqx.com/en/cloud).

In the following blogs, we will introduce how to migrate devices from GCP IoT Core to EMQX Enterprise, and how to seamlessly migrate IoT Core services through the GCP Pub/Sub integration of EMQX Enterprise.

## Other Articles in This Series

- [3-Step Guide for IoT Core Migration 02 | Migrating Devices from GCP IoT Core to EMQX Enterprise](https://www.emqx.com/en/blog/migrating-devices-from-gcp-iot-core-to-emqx-enterprise)
- [3-Step Guide for IoT Core Migration 03 | Ingesting IoT Data From EMQX Enterprise to GCP Pub/Sub](https://www.emqx.com/en/blog/ingesting-iot-data-from-emqx-enterprise-to-gcp-pub-sub)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
