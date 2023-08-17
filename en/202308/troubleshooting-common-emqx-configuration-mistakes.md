## Introduction

EMQX configuration involves multiple aspects, including but not limited to port numbers, authentication and authorization, security, data storage, etc. When configuring EMQX, if configuration errors or improper settings are encountered, it may cause the broker to fail to work properly, thereby affecting [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) communication. Therefore, understanding and resolving common issues related to EMQX configuration is essential to help administrators better configure and maintain EMQX.

In this article, we will introduce some common issues related to EMQX configuration and their solutions to assist administrators in better configuring and maintaining EMQX.

## EMQX Configuration Overview

Below are some core configuration details for EMQX:

1. Listening Ports: EMQX listens on ports 1883 and 8883 by default, where the former is the TCP port of MQTT and the latter is the SSL/TLS port of MQTT.

2. Subscription and Publishing Rules: EMQX allows administrators to set subscription and publishing rules in the configuration file to control which clients can subscribe to and publish to which topics.

3. Cluster Configuration: EMQX can be configured as a cluster to improve reliability and scalability. Cluster configuration includes mutual discovery between nodes, load balancing, and data synchronization, etc.

4. Security Authentication: EMQX supports username and password-based authentication and TLS/SSL certificate authentication. Administrators can configure EMQX to ensure that only authorized clients can connect and access.

5. QoS Level: EMQX supports MQTT's QoS levels, allowing clients to control the reliability and efficiency of message delivery.

6. Message Storage: EMQX can be configured to use memory or disk to store messages. When using disk storage, EMQX also provides various storage methods, such as the Mnesia database.

7. Web Management Interface: EMQX provides a web-based management interface that allows administrators to easily view the broker's status, manage clients and topics, etc.


## EMQX Configuration Methods

EMQX parameters can be configured in several ways:

1. **Configuration file:** The configuration file directory etc/ contains all the core configuration parameters of EMQX, including the parameters for listening ports, various plugin parameters, etc.

2. **Dashboard Hot Configuration page:** After activating the hot configuration function, for the configurations included on the Dashboard hot configuration page, they can only be modified through the Dashboard. For those configuration items not included on the Dashboard, they can still be modified by editing the configuration file and restarting EMQX.

3. **Environment Variables:** By default, EMQX uses environment variables with the prefix EMQX_ to override configuration items in the configuration file. The mapping rule from environment variable names to configuration file key value names is as follows:

  - Remove the EMQX_ prefix

  - Replace uppercase letters with lowercase letters

  - Replace double underscores __ with dots .

Now that we know the EMQX configuration methods, let’s review common configuration issues.

## How to Troubleshoot Common Configuration Issues

### **The Updated Web Certificate is not Effective**

Certificate update issues are usually caused by incorrect certificate file formats or configuration file paths. You can troubleshoot the problem in the following ways:

- Incorrect certificate path: If the certificate path set in the EMQX configuration file is incorrect, EMQX may not be able to find the new certificate file. In this case, you need to check if the certificate path is correct and make sure that the certificate file is correctly saved in that path.

- Incorrect certificate permissions: If the permissions of the new certificate file are not set correctly, EMQX may not be able to read the file. In this case, you need to ensure that the new certificate file has the correct file permissions and that EMQX has sufficient permissions to access the file.

- Incorrect certificate format: If the format of the new certificate file is incorrect, EMQX may not be able to read the file. In this case, you need to check if the certificate file format is correct and make sure that the certificate file is correctly saved in the correct format.

- Certificate cache not updated: If the EMQX certificate cache is not updated in a timely manner, the new certificate file may not be effective. In this case, you need to clear the cache of all PEM certificates. You can use the following command to clear the cache: emqx_ctl pem_cache clean.

- Incorrect certificate password: If the new certificate file has a password set, but the password is not correctly set in the EMQX configuration file, EMQX may not be able to read the file. In this case, you need to ensure that the password set in the configuration file matches the password set in the certificate file and that the password is set correctly.

- Managing multiple configuration methods: If hot configuration is enabled, modifying the configuration file may not take effect. If EMQX uses multiple configuration methods, you need to check according to the configuration priority.

### **Problems Manually Joining an EMQX Cluster**

When manually configuring an EMQX cluster, you may encounter the following common issues:

- Nodes cannot communicate with each other: EMQX cluster needs to ensure that each node can communicate with each other. If nodes cannot communicate with each other, cluster configuration will fail. In this case, you need to check if the network connection of each node is normal and ensure that they can access each other.

- Configuration file errors: Manually configuring an EMQX cluster requires correct configuration of the configuration file for each node. If there are errors in the configuration file, it may cause the cluster configuration to fail. In this case, you need to check the configuration file of each node and ensure that each configuration file is correct.

- Node name setting errors: In an EMQX cluster, each node needs to set a unique node name. If the node name is set incorrectly or is duplicated, it may cause the cluster configuration to fail. In this case, you need to check if each node's name is unique and ensure that the node name is set correctly.

- Node certificate is not configured or configured incorrectly: EMQX cluster needs to use certificates to ensure communication security between nodes. If the node certificate is not configured or is configured incorrectly, it may cause the cluster configuration to fail. In this case, you need to ensure that the certificate of each node is configured correctly and the certificate path, password, and other settings are correct.

- Incorrect cluster node count setting: EMQX cluster needs to set the correct number of nodes. If the node count is set incorrectly, it may cause the cluster configuration to fail. In this case, you need to ensure that the cluster node count is set correctly and that nodes can communicate with each other.

### **Modification of listener/general Configuration not taking Effect**

After modifying the configuration, it may not take effect after restarting, such as anonymous authentication, message size, window size, queue size, listener port, etc.

- Check for port conflicts with other services or applications. This can cause EMQX to fail to start normally or fail to establish connections with clients.

- Check methods of configuration, which have different priorities for taking effect: environment variables > Dashboard hot configuration page> configuration file.

- Check if both plugins and modules are being used. In the enterprise version, it is recommended to use modules instead of using plugins and modules at the same time.

### **EMQX Authentication plugin emqx_auth_mnesia Modification not Effective**

EMQX uses its built-in Mnesia database to store client IDs/usernames and passwords for Mnesia authentication. Authentication data can be managed through the HTTP API and will be stored in the EMQX built-in database. Adding a new account to any node will be effective for all nodes in the cluster. If changes to authentication information are not taking effect, there may be the following issues:

- Plugin not loaded: The emqx_auth_mnesia plugin must be loaded in the configuration file to be used. If the plugin is not loaded, the authentication information will not take effect. In this case, check the EMQX configuration file to ensure that all cluster nodes have correctly loaded the emqx_auth_mnesia plugin.

- Authentication information cache: EMQX uses caching to improve authentication information performance. If the authentication information is changed but the cache is not updated, the authentication information will not take effect.

- Incorrect authentication information: If the authentication information still does not take effect after being modified, it is necessary to modify or delete and then add it through commands. Configuration file modifications will not take effect, only new configurations will.

### **Authentication and Authorization Issues**

When there are errors in the authentication and authorization configuration of EMQX, it may cause clients to be unable to connect or subscribe/publish to topics.

- Check the authentication and authorization configuration files to ensure that settings such as usernames and passwords, client IDs and passwords, and TLS/SSL certificates are correct.

- Check if there are multiple authentication sources for authentication and authorization, and check if the startup or configuration order is appropriate.

## Conclusion

In summary, EMQX provides flexible configuration options to meet various application scenarios and requirements. The configuration of EMQX involves multiple aspects and requires administrators to consider and adjust comprehensively. This guide will help you analyze and eliminate possible causes in order to solve configuration problems and ensure the normal operation of EMQX.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
