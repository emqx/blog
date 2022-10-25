The fully hosted [MQTT messaging cloud service EMQX Cloud](https://www.emqx.com/en/cloud) can help users easily connect various IoT devices to the cloud and provide data integration with various third-party services to help users perform efficient data processing, storage and analysis.

To enable more convenient IoT data processing and further simplify the development process for users to build IoT applications, EMQX Cloud recently launched a new value-added service——Shadow Service.

## **Feature introduction**

Shadow service is a **device data caching service** provided by EMQX Cloud, helping users quickly design and develop IoT applications through the definition and use of Topic and API.

Previously, users need to transfer IoT data to a third-party data service through the data integration service of EMQX Cloud before they conduct IoT data processing analysis and further development of IoT applications, eg. “first purchase third-party data integration resource cloud services, then create VPC peer-to-peer connections to connect EMQX Cloud and third-party cloud services, and finally create and develop IoT applications”.

The device data caching capability provided by the newly launched shadow service can save the steps of connecting the EMQX Cloud and third-party data services. Users can enable centralized device data caching, modification, and viewing within the EMQX Cloud, quickly create object models, device shadows, and other applications related to data reporting and distribution, greatly saving the time and cost of development.

![Shadow service](https://assets.emqx.com/images/af2cae99046096a1a196e9ab09b60fc5.png)


## **Application scenarios**

With the data caching capability provided by the shadow service, users can develop many applications without configuring external storage and network connectivity, very suitable for the following scenarios:

### Application requests to get device status

- The device goes online and offline frequently for unstable network, so it can not respond to the request of the application normally.
- The device network is stable and responds to requests from multiple applications simultaneously. Even if the response results are the same, the device itself cannot load multiple requests for limited processing capacity.
- The device transmits information, and there is no data consumer. Latest device information needs to be checked only after the application goes online.
- The device transmits information, and different applications read different parts of the information.
- The device transmits multiple sets of information, and the application comprehensively displays all the information.

With the use of device shadow, the device state change only needs to be synchronized to the device shadow once, and the application requests to obtain the device state. Regardless of whether the application is online, the number of requests, and whether the device is online, the current state of the device can be obtained from the device shadow to enable the decoupling of the application and the device.

### **The application sends commands to the device to change the device status**

When the device is offline, or the device goes online and offline frequently for unstable network, the application sends control commands to the device. When the device is not online, the commands will fail to be sent.

Using the device shadow mechanism, the commands issued by the application can be stored in the device shadow with the timestamp. When the device goes online again, it obtains the commands from the device shadow and determines whether to execute them according to the timestamp.

 

## **User Guide**

### **Provisioning and Billing Instructions**

At present, the shadow service provides a 7-day free trial of 1G. You can log in to EMQX Cloud and provision shadow service through the "Value-added Service" module on the top menu or the "Shadow Service" module on the left menu.

![Value-added Service](https://assets.emqx.com/images/a86cf05aa2956375dea68ef5ecfb9150.png)
 
"Value Added Service" -> "Shadow Service" -> Activate Service on the top menu

!["Shadow Service" -> Activate Service](https://assets.emqx.com/images/b99423d2be28e5cb07b55814f28e1198.png)
 
"Shadow Service" ->Activate Service on the left menu

> Note: Since the shadow service uses the cloud computing resources of AWS, the shadow service is currently available only for **AWS professional version**. 

The cost of shadow service consists of three parts: memory size, number of requests, and outbound traffic.

You can select different memory sizes according to the estimated number of shadow models required. For the prices of different memory sizes and the number of shadow models created with customers, refer to the following table

| **Memory size** | **Memory size price** | **Estimated number of shadow models that can be created** | **Requests cost**                                            | **Outbound traffic fee**                                     |
| :-------------- | :-------------------- | :-------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 1G              | $0.08 /hour           | 8000                                                      | $0.04 /10,000 times, less than 10,000 times will be charged as 10,000 times | The cost of outbound traffic is calculated together with the current deployed traffic. Priority is given to the consumption of monthly free traffic, and the excess is calculated at $0.15 /GB. |
| 2G              | $0.15 /hour           | 16000                                                     |                                                              |                                                              |
| 4G              | $0.4 /hour            | 32000                                                     |                                                              |                                                              |


![Shadow Service](https://assets.emqx.com/images/abeba3cacb2cfd6a2496677ff4a3fb3a.png)
 
Specific billing standards and billing examples can be found at: [https://docs.emqx.com/en/cloud/latest/shadow_service/pricing.html](https://docs.emqx.com/en/cloud/latest/shadow_service/pricing.html) 

### Feature Details

After the activation of service, you can find the three pages of "Usage Overview", "Shadow Models" and "API" in the navigation bar.

On the "Usage Overview" page, you can learn about the memory usage of the currently deployed shadow service in a timely manner through the storage usage, the monthly invocations, and the line chart of usage changes across time dimensions, so as to monitor and alert business usage.

![Usage Overview](https://assets.emqx.com/images/e87dd8df70f633a3b841c361048ec9aa.png)
 
> Note: The service system will take up about 10 MB of storage space by default.

On the “API” page, you can learn about the API definitions for creating, querying, updating, and deleting shadow models (information). Your IoT business can use these APIs to obtain information about shadow services to accelerate the development of IoT applications.

![“API” page](https://assets.emqx.com/images/26cd421629c0a59f3143fdc0fc948031.png)
 
At the same time, we provide you with several call examples for reference: [https://docs.emqx.com/en/cloud/latest/shadow_service/invoke.html](https://docs.emqx.com/en/cloud/latest/shadow_service/invoke.html) 

On the "Shadow Model List" page, you can add, edit, and modify shadow models, and import customized shadow models in batches through templates.

![Shadow Model List](https://assets.emqx.com/images/857105d9dfad505bbe41c3cd1571d3dd.png)

###  **Instructions**

Click “Add”, fill in the relevant information, and click “Confirm” to create the shadow model.

![shadow model](https://assets.emqx.com/images/42e9ad67ba71f140068357dba55287ac.png)
 
Field Description of Shadow Model:

| **Field**              | **Necessity** | **Note**                                                     |
| :--------------------- | :------------ | :----------------------------------------------------------- |
| Name                   | Required      | 3 to 50 characters, and can only contain letters, numbers, "-", "_", "." |
| ID                     | Required      | ID is a globally unique identifier for the shadow model that will be used in Topic and API, with a minimum of 8 bits and a maximum of 64 bits, and can only contain letters, numbers, "_", and "-". If not filled in it will be automatically generated. |
| Note                   | Conditional   | Put a note                                                   |
| Topic for publishing   | Generated     | Automatically generated, the topic is based on ID for message publishing. |
| Topic for subscription | Generated     | Automatically generated, the topic is based on ID for message subscription. |

Click the ID in the shadow model list to enter the shadow model details page. On this page, you can not only view and modify the name and remarks of the current model, but also see the latest data of JSON model, or even modify it.

![shadow model details page](https://assets.emqx.com/images/9dc1e5451df2defa17eaf0a49cdcae7b.png)
 
With the out-of-the-box shadow services, data caching requirements of different business scenarios in various industries can be met. The integration capabilities of MQTT device access and message caching provided by the shadow service will provide impetus for accelerating the development of IoT platforms and applications.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
