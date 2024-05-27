With the rise of smart manufacturing, one of the primary concerns for industrial enterprises is how to accurately and reliably collect and utilize data streams during the production process.

[NeuronEX](https://www.emqx.com/en/products/neuronex), an industrial edge data hub designed for industrial scenarios, offers device data collection and edge intelligence analysis services. It can be deployed on industrial sites to support real-time data collection from various industrial equipment communications and fieldbus protocols. NeuronEX enables industrial system data integration, edge data filtering and analysis, AI algorithm integration, and seamless integration with IIoT platforms.

The rule testing feature of [NeuronEX](https://www.emqx.com/en/products/neuronex) allows users to simulate data inputs in a secure environment, test and optimize data processing rules, and identify and resolve potential issues in advance. This feature is crucial for applications such as smart manufacturing, remote monitoring, and preventive maintenance, as it helps improve productivity and reduce operational costs while ensuring system stability and security. In this blog, we will provide a detailed introduction to this feature, helping users create and test rules more efficiently.

![NeuronEX](https://assets.emqx.com/images/eba89324c09f2d60ef735fad20e482b4.png)

## Preparation

To test a rule, first create a data source to use as the input of rule. Here’s how to create an MQTT data source:

1. Log in to the NeuronEX system and navigate to the "Data Processing" - "Sources" page, click the "Create Stream" button.

   !["Data Processing" - "Sources" page](https://assets.emqx.com/images/19499518c408e2dce96d75d9fd7ca109.png)

1. Select "MQTT" as the stream type and click the "Next" button to proceed to the "Stream Config" page.

   !["Stream Config" page](https://assets.emqx.com/images/11e78e0c44d5eddb8cc74db6500d2d03.png)

1. On the Stream Config page, fill in the stream name and data source. You can leave other configuration fields at their default values. Enter the [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) you plan to subscribe to in the data source field to distinguish between different streams. For example, you can enter `neuronex/rule_test` and click the "Add Configuration Key" button to create a new configuration group.

   ![Create Stream](https://assets.emqx.com/images/f2db53f2f32663b5c4238370021dd721.png)

1. In the Source Configuration Key, enter the name and the MQTT broker address. For this example, we use the [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX, which is available through [EMQX Platform](https://www.emqx.com/en/cloud). Then, click the "Submit" button to add the configuration key.

   ![Add Source Configuration Key](https://assets.emqx.com/images/d5e1cfe69ee3abaddbc5b1ae5d48d5a8.png) 

1. Once the configuration key is added, you will see the `mqtt_conf` configuration key you just created. Click the "Submit" button to complete the creation of the data source.

   ![Click the "Submit" button](https://assets.emqx.com/images/b757f8821a0a252288317e9cd6c59a84.png) 

## Testing Rules with Simulated Data Sources

Now, let's dive into the core aspect of this blog: rule testing.

1. Navigate to the "Data Processing" -> "Rules" page and click the "Create Rule" button to create a rule.

   ![Data Processing" -> "Rules"](https://assets.emqx.com/images/bb4c1f83eee76dc38ad488db4f04c2b4.png)

1. On the New Rule page, substitute the default data source with the MQTT type data source `mqtt_stream` previously created. Then, click the "Simulate Data Sources" button to configure the simulated data sources.

   ![New Rule page](https://assets.emqx.com/images/4dce3b4a5055673901772d5a5bee2ab9.png) 

1. In the Simulate Data Sources dialog box, "Select simulated data in SQL" refers to the data source `mqtt_stream` that requires simulation. If the SQL statement involves multiple data sources, add them as necessary using the plus button. Enter the desired JSON data in the "payload" field for simulation. You can simulate multiple JSON data sets. Set the "Interval" to determine the frequency of sending each JSON data set. Enable the "Send Cyclically" function to cyclically send the defined JSON data. Ensure the simulated data source is activated by verifying the red box reads "Disable simulation" Click "Save" to finalize the configuration.

   ![Simulate Data Sources](https://assets.emqx.com/images/94fafe8966c90063368a21e79cff380e.png)

1. Once the simulated data source is configured, initiate rule testing. Click the "Run Test" button on the right side of the page. Upon execution, observe the two configured JSON data sets being outputted in a loop in the result. To pause testing, click the "Stop" button. To clear the output, click "Clear."

   ![Click the "Run Test" button](https://assets.emqx.com/images/6c59e17a560930f2a1f3994442166e8c.png)

1. Proceed with some simple rule applications. First, halt the test and clear the output. Then, slightly modify the SQL statement to only query the `a` attribute in the SELECT statement. Once done, re-run the test by clicking the "Run Test" button again. Now, the output will exclusively contain data for the `a` attribute, showcasing the flexibility and simplicity of rule testing.

   ![Rule test](https://assets.emqx.com/images/a5fdd3eef664b9295ad273d1814b89e7.png)

## Testing Rules with Simulated Data Sources Deactivated

After conducting rule testing with simulated data sources, let's explore testing rules with simulated data sources turned off. To proceed, we'll need to access the MQTTX client and send a message to the designated data source topic, `neuronex/rule_test`.

1. Halt the current test and clear the output. Then, within the Simulate Data Sources dialog box, click the "Turn Off Simulated Data Sources" button. Once closed, the button text will change to "Enable Simulation". Remember to click "Save" to confirm the changes.

   ![Simulate Data Sources dialog box](https://assets.emqx.com/images/ecd2f06dc0e9e8f0f2cef91704319f1d.png)

1. Subsequently, initiate the test by clicking the "Run Test" button to observe that although the test is running, no new data appears in the output.

   ![Run Test](https://assets.emqx.com/images/7a438e0067d773d896c5c06c8b3a5fd9.png)

1. Proceed to open the MQTTX client and establish a connection to the [Free Public MQTT Server](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) utilized in the `mqtt_conf` configuration group established earlier. Once connected, send three messages to the `neuronex/rule_test` topic.

   ![MQTTX](https://assets.emqx.com/images/b13c021eb74f182a6750dca0dc7e41b4.png)

1. Upon sending the messages, return to the NeuronEX rule creation page and observe that the output has been updated with three rows, corresponding to the three data pieces sent from MQTTX. As the SQL statement specifies querying only the `a` attribute, the output exclusively displays data from the `a` attribute.

   ![Test rules](https://assets.emqx.com/images/80851414e9dea35c1ab34ae41e3050af.png)

 

## Conclusion

This concludes the comprehensive overview of NeuronEX's rule testing capabilities. Through practical application, you can grasp the effectiveness of rule testing and implement it in real-world scenarios to enhance development efficiency and data processing adaptability.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
