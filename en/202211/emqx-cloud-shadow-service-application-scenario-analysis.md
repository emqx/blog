### Foreword

In today's high-speed iteration of IoT business, quickly connecting IoT devices and platform applications to achieve rapid business implementation and market validation is the key to shaping core competitiveness and achieving business innovation for many enterprises.

EMQX Cloud, as a one-stop O&M managed MQTT messaging cloud service, can help users quickly implement IoT application interfacing in the public cloud environment. To further help users quickly build IoT business, EMQX Cloud has recently launched shadow service. Through the platform data caching capability provided by shadow services, users can more easily implement various scenarios of applications and shorten the R&D cycle.

### What is Shadow Service

In the scenario of message interaction between IoT devices and applications, it is very common that the device side network is unstable, low-power devices are dormant, and mobile applications do not consume data regularly. For IoT application developers, a data interaction model with decoupled data production and consumption is more needed. Therefore, MQTT is widely used as a publish/subscribe based asynchronous communication protocol in IoT scenarios. In order to further ensure the reliability of data interaction, providing caching and persistence of data such as the latest reported messages from devices and the configuration issued by applications in the MQTT message access layer becomes an important requirement in the design of IoT platforms.

Based on the existing MQTT message access service, EMQX Cloud adds the Shadow Service to the value-added service to provide out-of-the-box platform-side data caching service. Users can cache, modify, and view device reporting data in EMQX Cloud's built-in services, and quickly create object models, device shadows, and other applications related to data reporting and distribution without having to purchase external resources and complex configurations to implement data caching services.

1. Users can create multiple shadow services within a single EMQX Cloud Professional instance. Each shadow service is created with a globally unique shadow_id, and users can create, modify, and delete data in different caching services via fixed contextual MQTT topics based on the shadow_id and RestAPI.
2. The cached data is stored in the shadow service in the form of JSON documents. When users create and modify cached documents, the shadow service automatically adds creation/modification timestamps to the JSON documents and updates the document versions for document consumers to confirm the information. For each shadow service we store only the latest version of the data.
3. Shadow services provide both MQTT and RestAPI interfaces to add, delete, and check cached documents for easy invocation by MQTT devices and application services.
4. The MQTT interface provided by the shadow service is fully adapted to the standard MQTT protocol, and the client can invoke the shadow service as long as it conforms to the standard MQTT protocol, without the need for a customized SDK and without platform binding.

### Application Scenario Example

Let's take smart home scenario as an example to explain how to use shadow service in detail. In the smart home scenario, the most common application is the data interaction between smart home devices - cloud service - personal mobile APP to realize the update of APP device status reporting and remote control of devices. Using shadow service, we can realize a smart device control application very simply, taking smart air conditioner as an example. 

#### Air conditioner status reporting

1. Create a shadow service for the smart air conditioning device in EMQX Cloud, and the shadow service creates a unique shadow_id and a fixed publish subscription topic for the device

   ![Create a shadow service](https://assets.emqx.com/images/b45fa62be5b1c73228929f31e9ae9643.png)
 
2. The smart air conditioner device regularly reports the air conditioner built-in temperature sensor data via the MQTT protocol to the `shadow/f840lyo7qn2rmiwo` specified by the shadow service, and the first time the data Payload is reported using the PUT operation.

3. ```
   {
     "method": "PUT",
     "payload": {
       "status":{
         "temp":26
         }
     }
   }
   ```

   Now you can see the new reported data in shadow service

   ![Reported data in shadow service](https://assets.emqx.com/images/bdb12142575dd39f0503177844d97277.png)

   Here we can see that in addition to the air conditioning temperature JSON document reported by the device, the shadow service also automatically adds the information as below to this document:

   - createAT: the time the document was created.
   - lastTime: the document update time.
   - version: document version.

   to facilitate subsequent APP comparison of historical data and display data.

4. The smart air conditioner can continuously update the temperature data cached in the shadow service in a timed-up manner, using the PATCH method in the MQTT payload to update the data.

   ```
   {
     "method": "PATCH",
     "payload": {
       "status":{
         "temp":24
         }
     }
   }
   ```

   The cached data in the shadow service is then updated to

   ![shadow service](https://assets.emqx.com/images/d8c786e61f546465e32b532181f4799b.png)

6. When users open the mobile APP and want to check the air conditioner status and room temperature, the APP can get the latest data from the shadow service cache through MQTT or RestAPI interface. Take the MQTT method as an example, the APP will establish an MQTT connection with EMQX Cloud service after opening, and get the device messages through the subscription topic `shadow/f840lyo7qn2rmiwo/reply`.

7. If the AC data is not reported at this point, you can pull the latest status in the cache by sending a GET command to `shadow/f840lyo7qn2rmiwo`, the published topic of the shadow service.

   ```
   {
     "method": "GET",
     "payload": {
     }
   }
   ```

   Once the shadow service receives this message, it will return the data in the cache to the APP.

   ```
   {
     "method": "PATCH",
     "payload": {
       "desired":{
          "temp":27
       }
     }
   }
   ```

8. If APP is constantly online, when a new air conditioner temperature is reported to the shadow service, the latest status data will be pushed to APP because APP has subscribed to `shadow/f840lyo7qn2rmiwo/reply` topic. In this way, a dynamically updated air conditioner temperature display business can be easily completed.

### APP remote adjustment of air conditioner temperature  

If we want to be able to adjust the air conditioner temperature from APP, while keeping the air conditioner device status reporting function.

1. We need to add a key value to the JSON document, such as adding `desired` via PATCH command.

   ```
   {
     "method": "PATCH",
     "payload": {
       "desired":{
       }
     }
   }
   ```

   Then the JSON file is updated to

   ![JSON file](https://assets.emqx.com/images/062e6f7b6fe8ca1ec2aa455e0578f237.png)

2. the AC also needs to subscribe to the `shadow/f840lyo7qn2rmiwo/reply` topic to receive regulation commands from the APP (of course, it is possible to create a new shadow service for command delivery, so that there is a separate control delivery topic channel).

3. Then we can send control commands through the APP.

   ```
   {
     "method": "PATCH",
     "payload": {
       "desired":{
          "temp":27
       }
     }
   }
   ```

   Then the JSON file is updated to 

   ![JSON file](https://assets.emqx.com/images/2c720fff7656e5a9e4bfe858f33418d2.png)
 
4. When AC receives the updated JSON file by subscribing to `shadow/f840lyo7qn2rmiwo/reply` topic, the AC client program will update its own temperature setting by the value set in the `desired` key to realize remote APP temperature control.

### More Application Possibilities

In addition to smart home scenario, we can also use the data caching function of shadow service to realize many business scenarios applications.

1. Low-power smart meter data collection and remote configuration: In real life, many smart meter devices (such as gas meters, water meters, etc.) rely on battery power supply and often use hibernation to save power in order to extend the battery power supply life. For example, an in-home gas meter may only wake up 1-2 times a day, and the wake-up time is within a few minutes. We typically report meter readings during the wake-up phase and receive updates to the meter's latest configuration from the platform-side application at the same time. At this point, we can use the shadow service to cache the platform-side configuration and pull the latest configuration data for update when the meter wakes up. This also eliminates the need for the platform application to probe whether the metering device is online when sending the configuration, simplifying the application logic.

2. Telematics car message pushing: In the Telematics scenario, the car is in a dormant state when the engine is off. And part of the Telematics platform message notification (maintenance reminder, operation message notification, etc.) can use the caching function of the shadow service to achieve message caching for offline car engine devices. When the vehicle wakes up, the cached messages in the shadow service can be pulled to synchronize the offline messages.

### Conclusion

The out-of-the-box shadow service provided by EMQX Cloud can be adapted to the data caching needs of various business scenarios in different industries. With the fully managed MQTT messaging cloud service provided by EMQX Cloud, combined with the shadow service feature, users can quickly realize the integrated capability of MQTT device access and message caching, greatly accelerating the speed of IoT application development. At the same time, the flexible message caching data structure in the shadow service can also help users easily achieve later business expansion, providing a guarantee for the continuous development of their business.





<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
