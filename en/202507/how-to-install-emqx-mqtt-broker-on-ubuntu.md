## Introduction

The Message Queuing Telemetry Transport ([MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)) protocol is a lightweight, publish-subscribe messaging system widely used in IoT and real-time applications due to its efficiency and scalability. EMQX is a powerful, open-source [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) designed for high performance and massive scalability, with robust support for multiple operating systems, including Linux, Windows, macOS, Raspbian, Ubuntu, and even containerized environments like Docker. 

In this blog post, we’ll guide you through the process of installing EMQX on an Ubuntu system, providing a step-by-step tutorial to get your MQTT broker up and running quickly. Whether you’re building an IoT project or exploring real-time messaging, this guide will help you set up EMQX with ease.

## Installing EMQX MQTT Broker on Ubuntu

The operating system used for this demonstration is Ubuntu 20.04 64-bit.

### Option 1: Install EMQX with APT

APT is the package manager that comes with Ubuntu. It is recommended to prefer to install EMQX with APT. At the same time, EMQX also provides the official APT source and one-click configuration script to help users quickly install EMQX.

1. Configure the EMQX APT source.

   `curl -s https://packagecloud.io/install/repositories/emqx/emqx-enterprise5/script.deb.sh | sudo bash`

   Copy the above command to the Ubuntu terminal and execute it. The following figure indicates a successful configuration.

   ![image.png](https://assets.emqx.com/images/6b60d527931cb022a07b9f0433beaf9a.png)

2. Install the latest version of EMQX.

   ```shell
   sudo apt-get install emqx-enterprise
   ```

1. After successful installation, use the following command to start EMQX.

   ```shell
   sudo emqx start
   ```

   As illustrated below, a successful startup of EMQX Enterprise 5.10.0 will display a confirmation message. If the command yields no response, verify port availability as detailed in the [Verifying EMQX Operation and Connectivity](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu#emqx-operation-check) section.

   ![image.png](https://assets.emqx.com/images/9028f5b96bd229242183d0c3e2e70d2c.png)

1. EMQX management command.

   EMQX offers command-line tools for essential operations like starting, stopping, and accessing the console. As shown below, you can view all available management commands by executing `sudo emqx` in your terminal.

   ![image.png](https://assets.emqx.com/images/72f536041160a5bda7ad47723a7a0615.png)

### Option 2: Install EMQX with tar.gz package

For environments without public network access or for rapid deployment and functional verification, the EMQX `.tag.gz` package offers a self-contained and easily manageable installation method, independent of third-party dependencies.

#### Download the Installation Package

Visit the [EMQX download address](https://www.emqx.com/en/downloads-and-install/enterprise?os=Ubuntu). Select `5.10.0` for the **Version** and `Ubuntu 22.04 amd64 / tar.gz` for the **Package Type**. Then click the “copy” icon on the right to copy the complete `wget` command. Paste the copied command into your Ubuntu terminal and execute it to begin the download.

#### Unzip and Install

Execute the following command on the server terminal, extracting the compressed package to the `emqx` directory under the current directory.

> *This demonstration will be installed under the current user's home directory, that is* `~/emqx/`

```shell
mkdir -p emqx && tar -zxvf emqx-enterprise-5.10.0-ubuntu22.04-amd64.tar.gz -C emqx
```

Next, use the following command to start EMQX.

```shell
cd emqx ./bin/emqx start
```

If the startup is successful, you'll see the message `EMQX Enterprise 5.10.0 is started successfully!` appear. Should the command not return a response after a significant delay, please refer to the [Verifying EMQX Operation and Connectivity](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu#emqx-operation-check) section to verify if any relevant ports are already in use.

## Verifying EMQX Operation and Connectivity 

### Port listening Check

Use the command `netstat -tunlp` to check the operation of the EMQX port. By default, EMQX will start the following ports. Check the port occupancy in case of exceptions.

> *This command can also be executed before the EMQX installation to ensure that the relevant port is not occupied.*

![image.png](https://assets.emqx.com/images/160e27d242cc903eb31192be9d072dab.png)

| **Port** | **Description**                                              |
| :------- | :----------------------------------------------------------- |
| 1883     | MQTT/TCP port                                                |
| 8883     | MQTT/SSL port                                                |
| 8083     | MQTT/WS port                                                 |
| 8084     | MQTT/WSS port                                                |
| 18083    | EMQX Dashboard port                                          |
| 4370     | Erlang distributed transmission port                         |
| 5370     | Cluster RPC port. By default, each EMQX node has a RPC listening port. |

### Access the EMQX Dashboard

EMQX provides a Dashboard for users to manage and monitor EMQX and configure required functions through Web pages. The Dashboard can be accessed via a browser at `http://localhost:18083/` (Replace the localhost with the actual IP address) after EMQX has been successfully started.

> *Before accessing Dashboard, make sure that port 18083 is opened in the server firewall*

The default user name of Dashboard is `admin`, and the password is `public`. After the first successful login, you will be prompted to change the password.

![image.png](https://assets.emqx.com/images/28963e59f0264903122d5920434b8c7d.png)

## MQTT Connection Test

Click the `Diagnostics Tools` -> `WebSocket Client` in the left menu bar. This allows you to test [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket), confirming the successful deployment of your MQTT broker.

> *It is required that the firewall should have opened the right for access to port 8083*

### Connect

As shown in the figure below, the tool has automatically filled in the host according to the access address. You can click the `Connect` button directly. The figure below indicates a successful connection.

![image.png](https://assets.emqx.com/images/174d4ee377890785cdbe6c449ab265d7.png)

### Subscribe

Subscribe to a `testtopic` as shown in the figure below.

![image.png](https://assets.emqx.com/images/686714bb2cd2025a22bdb9a0824a7c92.png)

### Publish

As shown in the figure below, we have published two messages to `testtopic,` which have been received successfully, indicating that the MQTT broker has been successfully deployed and is running normally.

![image.png](https://assets.emqx.com/images/bcb71703323cd4f3bfd89b7e5cc4408f.png)At this point, we have successfully deployed and tested the MQTT broker's basic connectivity. However, this setup is currently suitable only for testing purposes. To prepare the MQTT broker for a production environment, the crucial next step is to implement robust authentication configurations.

## Securing Your MQTT Broker on Ubuntu: Authentication Configuration

By default, EMQX will allow any client connection until the user creates an authenticator, which will authenticate a client according to the authentication information provided by the client. A client can connect successfully only when it passes the authentication. Next, we will demonstrate how to use the built-in database of EMQX for the authentication of username and password.

> *EMQX also provides authentication integration support with a variety of back-end databases, including MySQL, PostgreSQL, MongoDB, and Redis.*
>
> *Check the documentation for more authentication methods:* 
>
> https://docs.emqx.com/en/emqx/latest/access-control/authn/authn.html 

### Create Authentication

EMQX has supported the authentication configuration in Dashboard since version 5.0, allowing users to create secure MQTT services more conveniently and quickly. Click `Authentication` under the `Access Control` menu to enter the Authentication Configuration page, and then click the `Create` button on the far right.

![image.png](https://assets.emqx.com/images/bfa467241c65a19b454a69cd17fbf36a.png)

Select the `Password-Based` option, and then click `Next`.

![image.png](https://assets.emqx.com/images/150f8a6a2880dd4dbfbd6bec9c0c1526.png)

Select `Built-in Database` for the database and click `Next`.

![image.png](https://assets.emqx.com/images/2c4863b5c78d6f60b440af48f17f74f4.png)

Next, select the `UserID Type`, `Password Hash` and `Salt Position`, then click `Create`.

> *Here the default configuration is used, while readers may make selection according to the actual business needs.*

![image.png](https://assets.emqx.com/images/0185bc05b8e8d91b45bf191e4d0956b2.png)

### Add a User

The figure below shows the successful creation of the authentication. Next, click `Users` to add a user.

![image.png](https://assets.emqx.com/images/aabd714e74b37923dbca7e15edf57ce2.png)

After entering the User Management page, click the `Add` button on the far right, set the `Username` and `Password` in the pop-up box, and then click `Save`.

![image.png](https://assets.emqx.com/images/70d4aa4fd87821df050d93eab48755b5.png)

The figure below shows the successful creation.

![image.png](https://assets.emqx.com/images/11f82a1fc85c0e67440442051e414fa8.png)

### Test Authentication

Next, we use the Websocket tool provided by Dashboard to test whether the authentication has been successfully configured. Enter the username and password you just created in the Connect configuration, and then click `Connect`. A pop-up window on the right indicates that it is connected.

![image.png](https://assets.emqx.com/images/93a8ecd85ab5ccacb62e3b42b27608e7.png)

Next, use the user name `test1` that has not been created. Click Connect, and you will see the following Connection Failed information.

![image.png](https://assets.emqx.com/images/20e5e5b9cae683da878acdccaa7034fc.png)

So far, we have completed the authentication configuration for EMQX and set up a single-node MQTT broker available in the production environment. To ensure the high availability of the MQTT broker, you need to create a multi-node EMQX cluster. The cluster creation will not be detailed in this document. You can refer to the [EMQX Cluster documentation](https://docs.emqx.com/en/emqx/latest/deploy/cluster/create-cluster.html#create-and-manage-cluster) for configuration.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
