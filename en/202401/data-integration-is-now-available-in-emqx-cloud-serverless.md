We are excited to announce that the fully managed MQTT cloud service [EMQX Cloud](https://www.emqx.com/en/cloud) has seamlessly incorporated data integration capability into its Serverless plan. This enables users to unify data from different sources, formats, or systems, facilitating a fast, reliable, and secure IoT data movement with minimal cost.

## Architecture

![Architecture](https://assets.emqx.com/images/81d8b4414fc9b5380a127aa93c725723.png)

As devices or applications establish connections with the deployment, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) takes charge of routing messages. The introduction of data integration adds a layer of versatility, offering a suite of components for data processing driven by SQL statements—commonly known as the 'Rule Engine'. Users have the flexibility to define processing rules and subsequently dispatch the refined data to various cloud services. 

The data integration of [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), equipped with a straightforward interface configuration, now supports a seamless connection with Kafka and HTTP services. This enables users to easily integrate their deployment with other critical business systems. 

## Work Flow

Completing a data integration workflow is straightforward, requiring four simple steps.

![Work Flow](https://assets.emqx.com/images/0c822a4ca16f8c0425af8866bf0c0ab9.png)

1. Create a connector that associates with your cloud service product, which could be a message queue service like Kafka or an HTTP application service. A "connector" serves to establish connections with services from cloud service providers.
2. The rules outline "where the data comes from" and "how to filter and process the data." These rules employ SQL-like statements for customizing data writing, and SQL testing can be used to simulate exported data.
3. Actions determine the destination of the processed data. A rule may align with one or multiple actions, each associated with predefined connectors, thereby indicating the service to which the processed data will be dispatched.
4. The Data Integration design flow is now complete. The data can be seamlessly transmitted to the designated target services after testing.

## Benefits

- **Built-in Data Preprocessing Capability:** Data Integration empowers users to filter, sort, and process data seamlessly during the stages of message reception and transmission. The rule engine within data integration provides flexible, SQL-like operations on data, ensuring that the data transmitted to the destination is filtered. This removes unnecessary information and enhances the efficiency of data transmission and post-processing. 
- **Simplified Service Integration without Extra Expenses**: Data integration eliminates the need for users to create an MQTT application for message subscribing when integrating with other cloud services, which can be complex and costly for small and medium-sized businesses. EMQX Cloud Serverless’s data integration enables users to effortlessly integrate application services with simple configurations, resulting in substantial savings in development and server expenses. 
- **Pay-as-You-Go for Cost Savings**: The pay-as-you-go billing model ensures that users are only charged for actual usage, including device connections, data consumption, and integration services. Data Integration functionality is free during the Beta phase. After Beta, charges will depend on how often actions are executed, with no fees for non-executed actions.

## Use Cases

### HVAC Management

Managing a home's heating, ventilation, and air conditioning (HVAC) system is an area where EMQX Cloud Serverless can shine. With data integration, it can seamlessly collect data from temperature sensors, apply processing through the rule engine, and then transmit the data to the Kafka service, enabling intelligent automation of the HVAC system.

### Health and Wellness Monitoring

MQTT's capability to transmit data from diverse sensors makes it ideal for health and wellness monitoring applications. EMQX Cloud Serverless with data integration can detect and gather health data from patients for reporting and seamlessly integrates with an HTTP monitoring service. In case of emergencies, it actively monitors and dispatches warnings to both terminal devices and medical personnel.

### Automated Express Delivery

EMQX Cloud Serverless seamlessly integrates with automated express delivery. Upon scanning with RFID terminal devices, information such as the vehicle, location, and cargo details is reported. This information is efficiently transmitted to the management system through data integration. Additionally, feedback is promptly sent back to the terminal devices, facilitating real-time updates of the delivery status.

## Conclusion

The data integration of EMQX Cloud Serverless offers developers a new option for collecting and processing IoT data. Developers can effortlessly transmit data to Kafka and HTTP services, creating a comprehensive IoT data flow.



<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
