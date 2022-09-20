For enterprises that are eager to carry out IoT business, one highlight of [EMQX Cloud](https://www.emqx.com/en/cloud), a fully-managed cloud-native MQTT message service, is that it can extract, filter, split and convert the data of Internet of things in real-time through a high-performance built-in rule engine, thus simplifying the development of IoT applications and accelerate business delivery. An out-of-box data bridging feature based on rule engine can help users to implement connections with various cloud services, such as Kafka, MongoDB, AWS RDS, AWS DocumentDB and InfluxDB, etc. and forward the IoT data to various third-party databases, message queues and data systems as per requirements.

Rule engine is undoubtedly an edge tool of EMQX Cloud to help users implement flexible data processing and integration. To enable users to get started easily and exert the value of this killer feature in practical project applications, the EMQX Cloud team recently upgraded and optimized it.

![EMQX Cloud Integration](https://assets.emqx.com/images/56dcf461141467454f668df0cf41d1de.png)

The rule engine has been officially renamed Data Integration. Meanwhile, the revised and upgraded UI has made it easier for users to understand, operate and manage. Compared with the previous version, the new Data Integration helps users quickly know the creation of resources and rules step by step by navigation. The users only need to follow the procedure of “creating resources - creating rules - adding actions - test and runing” to complete the configuration of rules. The specific procedure is as follows:

![creating resources - creating rules - adding actions - test and runing](https://assets.emqx.com/images/47d566e14a5a234e430f52062dd3f377.png)

- First, specify the data architecture of your own business and the data integration system that needs to be docked with EMQX Cloud in [Create Resources], namely, what kind of third-party database, message queue, or business system interface to forward the data to. This is to create the connection information of relevant integrated systems for use in next steps.
- In [Create Rule], use SQL statement to create a rule to match the data from the device based on your business requirements, namely, define [what data needs to be processed and integrated].
- Select the well-defined resource in [Add Action], that is, which service the data will be sent to, namely, "where will the data go after processing". At the same time, the format of message storage and integration is defined through the message content template, that is, [how data is processed].

After the three steps above, the users can complete the setting of processing and unloading the equipment data, and complete the data integration after further testing and operation.

 The brand new revision of [Data Integration] will make the use logic of the rule engine more consistent with users' habits and provide convenience for users to create IoT platforms and applications to meet business requirements with EMQX Cloud.

## Appendix: Data Integration Feature Guide

### Preparation

Get acquainted with the following concepts before using data integration features, and in the introduction overview of [Data Integration], you can operate by following the guidance.

![EMQX Cloud guidance](https://assets.emqx.com/images/fc3e32150d9fdf2035d6fc26b8de231f.png)

Meanwhile, please also note the version of  EMQX Cloud you are using:

**Standard version**

- Resources only support public network access. Therefore, before creating resources, you need to ensure that the resources have public network access capability and open the security group. There is no need to create VPC peer connections.
- For resource types, only Webhook and MQTT bridging connection is opened.

**Professional version**

- Before opening the NAT gateway, resources only support intranet access, so you need to configure VPC peer connection and open the security group before creating resources.
- After opening the NAT gateway, you can access through the public network.

### Use tutorial

Use EMQX Cloud data integration feature to collect simulated temperature and humidity data, and dumping it to MySQL as an example: [https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_save_mysql.html#mysql-configuration](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_save_mysql.html#mysql-configuration) 

Reference documents: [https://docs.emqx.com/en/cloud/latest/rule_engine/introduction.html](https://docs.emqx.com/en/cloud/latest/rule_engine/introduction.html) 


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
