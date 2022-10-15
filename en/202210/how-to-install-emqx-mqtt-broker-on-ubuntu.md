As a large-scale distributed [MQTT broker](https://www.emqx.io/) for IoT with more than 10 million downloads worldwide, [EMQX](https://www.emqx.com/zh/products/emqx), since it open-sourced in GitHub in 2013, has been widely adopted by more than 20,000 enterprise users from more than 50 countries and regions, and has connected more than 100 million IoT-critical devices in total.

Recently, [EMQX released version 5.0](https://www.emqx.com/en/blog/emqx-v-5-0-released) , which has also been greatly optimized and upgraded in terms of reliability of message transfer and ease of use experience, making it a milestone in the MQTT field. In the pre-launch performance test, the EMQX team reached [100 million MQTT connections](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connections) +1 million message throughput per second with a 23-node cluster, which makes EMQX 5.0 the most scalable MQTT broker in the world by far.

EMQX supports running on Linux, Windows, macOS, Raspbian and other operating systems, and also supports deployment with Docker, Kubernetes and Terraform. This article will take EMQX 5.0.4 as an example to introduce how to build a single-node MQTT broker on Ubuntu, and demonstrate the common problems encountered during the building process.

## Installing EMQX

The operating system used for this demonstration is Ubuntu 20.04 64-bit.

### Installing EMQX with APT

APT is the package manager that comes with Ubuntu. It is recommended to prefer to install EMQX with APT. At the same time, EMQX also provides the official APT source and one click configuration script to help users quickly install EMQX.

1. Configure the EMQX APT source.

   ```
   curl -s https://assets.emqx.com/scripts/install-emqx-deb.sh | sudo bash
   ```

   Copy the above command to the Ubuntu terminal and execute it. The following figure indicates successful configuration. 

   ![Configure the EMQX APT source](https://assets.emqx.com/images/4d50b52f6a11f9c59d6b524b92d0af15.png)

2. Install the latest version of EMQX.

   ```
   sudo apt-get install emqx
   ```

3. After successful installation, use the following command to start EMQX.

   ```
   sudo emqx start
   ```

   As shown in the figure below, `EMQX 5.0.4 is started successfully!` will pop up if the startup is successful. If there is no response to the command for a long time, please check whether the relevant port is occupied against the description in the section [EMQX operation check](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu#emqx-operation-check).

   ![Start EMQX](https://assets.emqx.com/images/25dd5e014a47e8082dd2988ea5d7fae1.png)

4. EMQX management command

   EMQX provides command line tools to help users start, close and enter the console. As shown in the figure below, execute `sudo emqx` on the terminal to view all management commands.

   ![EMQX management command](https://assets.emqx.com/images/18491face867eab53a5aae2ea5760c06.png)

### Installing EMQX with tar.gz package

When the server has no public network access or needs to quickly deploy and verify the EMQX function, `tag.gz` package can be used for installation, which is independent of any third party and easy to manage.

#### Download the installation package

Visit the [EMQX download address](https://www.emqx.io/en/downloads?os=Ubuntu). Select the `Package` tag, select `Ubuntu20.04 amd64/tag.gz` for the installation package type, and then click the “copy” icon on the right (this will copy the whole line of wget download command).

Paste the download command to the ubuntu terminal and perform the download operation.

#### Unzip and install

Execute the following command on the server terminal, extracting the compressed package to the `emqx` directory under the current directory.

> This demonstration will be installed under the current user's home directory, that is `~/emqx/`

```
mkdir -p emqx && tar -zxvf emqx-5.0.4-ubuntu20.04-amd64.tar.gz -C emqx
```

Next, use the following command to start EMQX

```
./emqx/bin/emqx start
```

If the startup is successful, `EMQX 5.0.4 is started successfully!` will pop up. If there is no response to the command for a long time, please check whether the relevant port is occupied against the description in the section [EMQX operation check](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu#emqx-operation-check).

## EMQX Operation Check

### Port listening

Use the command `netstat -tunlp` to check the operation of the EMQX port. By default, EMQX will start the following ports. Check the port occupancy in case of exceptions.

> This command can also be executed before the EMQX installation to ensure that the relevant port is not occupied.

![MQTT Broker Port](https://assets.emqx.com/images/84b58c00ea74342739a96e4d8d9baf17.png)

| **Port** | **Description**                                              |
| :------- | :----------------------------------------------------------- |
| 1883     | MQTT/TCP port                                                |
| 8883     | MQTT/SSL port                                                |
| 8083     | MQTT/WS port                                                 |
| 8084     | MQTT/WSS port                                                |
| 18083    | EMQX Dashboard port                                          |
| 4370     | Erlang distributed transmission port                         |
| 5370     | Cluster RPC port. By default, each EMQX node has a RPC listening port. |

### Access to Dashboard

EMQX provides a Dashboard for users to manage and monitor EMQX and configure required functions through Web pages. The Dashboard can be accessed via a browser at `http://localhost:18083/` (Replace the localhost with the actual IP address) after EMQX has been successfully started.

> Before accessing Dashboard, make sure that port 18083 is opened in the server firewall

The default user name of Dashboard is `admin`, and the password is `public`. After the first successful login, you will be prompted to change the password. 

![MQTT Dashboard](https://assets.emqx.com/images/2ea7ca29135c1242524eef0b29cf0757.png)


## MQTT Connection Test

Next, click the `WebSocket Client` in the left menu bar, which can test MQTT over Websocket to verify whether the MQTT broker has been successfully deployed.

> It is required that the firewall should have opened the right for access to port 8083

### Connect

As shown in the figure below, the tool has automatically filled in the host according to the access address. We can click the `Connect` button directly.

![Connect to MQTT Broker 1](https://assets.emqx.com/images/bc0edb43aee71ff333994685744ac79d.png)

The figure below indicates successful connection.

![Connect to MQTT Broker 2](https://assets.emqx.com/images/984c2776db9b559c059c91cd99783ae6.png)

### Subscribe

Subscribe to a `testtopic` as shown in the figure below.

![Subscribe to MQTT topic](https://assets.emqx.com/images/fc72490d4cf70752215b19c71f33857e.png)

### Publish

As shown in the figure below, we have published two messages to `testtopic` which have been received successfully, indicating that the MQTT broker has been successfully deployed and is running normally.

![Publish MQTT messages](https://assets.emqx.com/images/f9d2a47d00a331ee02106d6a2e52baa5.png)

So far, we have completed the building and connection test of the MQTT broker, but the server can be used for testing only. To deploy the MQTT broker available in the production environment, we also need to perform the most important authentication configuration.

## Authentication Configuration

By default, EMQX will allow any client connection until the user creates an authenticator which will authenticate a client according to the authentication information provided by the client. A client can connect successfully only when it passes the authentication. Next, we will demonstrate how to use the built-in database of EMQX for authentication of username and password.

> EMQX also provides authentication integration support with a variety of back-end databases, including MySQL, PostgreSQL, MongoDB, and Redis.
>
> Check the documentation for more authentication methods: [https://www.emqx.io/docs/en/v5.0/security/authn/authn.html](https://www.emqx.io/docs/en/v5.0/security/authn/authn.html) 

### Create authentication

EMQX has supported the authentication configuration in Dashboard since version 5.0, allowing users to create secure MQTT services more conveniently and quickly. Click `Authentication` under the `Access Control` menu to enter the Authentication Configuration page, and then click the `Create` button on the far right.

![MQTT Authentication](https://assets.emqx.com/images/a9f68bdab55d5ef0eeba848b59c545d1.png)

Select the `Password-Based` option, and then click `Next`.

![MQTT Authentication Password-Based](https://assets.emqx.com/images/6e062b95530f50cccebe5f59797fb3c3.png)

Select `Built-in Database` for the database and click `Next`.

![MQTT Authentication Built-in Database](https://assets.emqx.com/images/7fa648e6416a04177ebefde5cc22d0f9.png)

Next, select the `UserID Type`, `Password Hash` and `Salt Position`, then click `Create`.

> Here the default configuration is used, while readers may make selection according to the actual business needs.

![MQTT Authentication](https://assets.emqx.com/images/0dd6196112c593fbf64d3129b7476a9e.png)

### Add a user

The figure below shows the successful creation of the authentication. Next, click `Users` to add a user.

![Add a MQTT Authentication user](https://assets.emqx.com/images/39ad5d030881d7e907a22a67802a11b5.png)

After entering the User Management page, click the `Add` button on the far right, set the `Username` and `Password` in the pop-up box, and then click `Save`.

![Add an MQTT Authentication user](https://assets.emqx.com/images/6885899e677022ab1e0c7908769da616.png)

The figure below shows the successful creation.

![Add an MQTT Authentication user](https://assets.emqx.com/images/36b87dd4c03514fa56bd2782ca986b62.png)

### Test

Next, we use the Websocket tool provided by Dashboard to test whether the authentication has been successfully configured. Enter the username and password you just created in the Connect configuration, and then click `Connect`. A pop-up window on the right indicates that it is connected.

![MQTT Authentication test](https://assets.emqx.com/images/ffc8a0f91e2fc7ec56b46cefa5842857.png)

Next, use the user name `test1` that has not been created. Click Connect, and you will see the following Connection Failed information.

![MQTT Authentication test](https://assets.emqx.com/images/a6664b3595bbfd31b86303e34c8d88da.png)

So far, we have completed the authentication configuration for EMQX and set up a single-node MQTT broker available in the production environment. To ensure the high availability of the MQTT broker, you need to create a multi-node EMQX cluster. The cluster creation will not be detailed in this document. You may refer to the [EMQX Cluster documentation](https://www.emqx.io/docs/en/v5.0/deploy/cluster/intro.html) for configuration.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
