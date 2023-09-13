In today's rapidly advancing technological landscape, the automotive industry is undergoing a transformative shift. Software-defined vehicles (SDVs) are at the forefront of this revolution, offering unprecedented levels of connectivity, automation, and data-driven insights. As these SDVs generate massive amounts of data, the need for efficient and real-time processing becomes paramount. 

> Related content: [What is a Connected Car? All You Need to Know](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know)

In this blog, we will delve into stream processing for SDV data and how it contributes to enhancing safety, optimizing performance, and revolutionizing the user experience within software-defined vehicles.

## What Are Software-Define Vehicles?

Software-define vehicles are vehicles with a high degree of connectivity, automation, and intelligence. They can communicate with other vehicles, infrastructure, cloud services, and mobile devices and adapt to changing conditions and user preferences. SDVs can also be remotely controlled or updated by software applications, which can modify their behavior, performance, or appearance.

For example, an SDV can:

- Switch between different driving modes, such as eco-friendly, sporty, or autonomous, depending on the driver's mood or the traffic situation. 
- Change its interior lighting, music, or temperature based on the passenger's preferences or the weather.
- Receive rule updates from the manufacturer or third-party providers, which can improve its functionality or security.

## Unlock the Potential of SDV Data via Stream Processing

SDVs generate a large amount of data from various sources, such as sensors, cameras, GPS, radar, lidar, etc. This data is not only voluminous but also heterogeneous and complex. It needs to be processed in real-time or near real-time to provide useful insights and actions for the SDVs and their users.

Stream processing is a technique that effectively handles such data streams. It follows a paradigm where data is processed as soon as it arrives, without the need for storage in a database or file system. Stream processing enables various operations on the data streams, including filtering, aggregation, transformation, enrichment, and analysis.

Moreover, stream processing facilitates the integration of data from multiple sources, resulting in a unified view of the data. It also has the capability to horizontally scale to accommodate increasing data volumes and velocities.

With stream processing, we can benefit from SDV data in the following aspects:

- **Improved safety and performance**: Stream processing can detect anomalies or faults in the SDVs and alert the drivers or service providers. It can also optimize the SDVs' performance by adjusting their parameters based on the data analysis.
- **Enhanced user experience**: Stream processing can provide personalized recommendations or suggestions for drivers or passengers based on their preferences or behavior. It can also enable new features or services for the SDVs, such as entertainment, navigation, or social networking.
- **Increased efficiency and profitability**: Stream processing can reduce the operational costs and maintenance of the SDVs by optimizing their resource utilization and energy consumption. Moreover, stream processing can generate additional revenue streams for service providers through value-added services and products derived from data insights.

## eKuiper: A Powerful Stream Processing Engine Fit for SDV Data

[LF Edge eKuiper](https://ekuiper.org/) is a lightweight data stream processing engine for IoT edge. With a core feature footprint of only 10 MB, it can be easily deployed on the vehicle MPU. Users can leverage eKuiper to perform stream processing of SDV data.

In our blog [*Bridging Demanded Signals From CAN Bus to MQTT by eKuiper*](https://www.emqx.com/en/blog/bridging-demanded-signals-from-can-bus-to-mqtt-by-ekuiper), we have demonstrated the ability of eKuiper to connect and understand [CAN bus](https://www.emqx.com/en/blog/can-bus-how-it-works-pros-and-cons) data. In addition, eKuiper also supports [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), HTTP, SQL database, and files as the data source. Using together with [NanoMQ](https://nanomq.io/), it can even connect to SOA (SomeIP, DDS) data which is bridging to MQTT. With the stream processing capability, eKuiper can calculate and transform the data from these various data sources to generate insight and trigger actions.

eKuiper uses SQL to build streaming pipelines named rule. The rules are hot deploy and hot updated. Several rules can be connected flexibly to build rules for complex scenarios. With one single rule, eKuiper is capable of:

- **Flexible selection of the demanded data in signal level.** It can extract data based on different requirements. For example, only the demanded signals, changed signals, or the signals that meet certain conditions.
- **Vehicle side real-time and flexible rule engine.** This can automatically trigger actions when meet some conditions. For example, close all windows when the speed is higher than 70.
- **Agile smart analysis.** Without cloud connection, local eKuiper can help automatically wire data and AI model (currently TF Lite) without coding. It can also feed data to the training model on the vehicle.
- **Edge computing to reduce transfer bandwidth and cloud-side computing pressure.** eKuiper can summarize the data based on time window to significantly reduce the transferred data but still keep the trend of the data. It also supports down-sample and compressed data.
- **Heterogeneous data aggregation.** Parse data from various protocols (e.g., TCP, UDP, HTTP, MQTT) and various formats (e.g., CAN, JSON, CSV) and merge them by flexible rules.
- **Message routing.** eKuiper can make intelligent decisions regarding data transmission to the cloud and local storage for utilization by other applications within the vehicle. For example, based on GDPR or some whitelist to determine the routing.

## Empowering Software-Define Vehicles Scenarios with eKuiper

Based on the abilities of eKuiper mentioned above, we can build applicable SDV workflows and facilitate potential scenarios by implementing them.

### Security Problem Detection

Based on the real-time data from the vehicle, eKuiper can be used to detect the security problem and alert the driver. On the one hand, we can use SQL to define the rule to detect the security problem. On the other hand, users may have trained AI models to detect the security problem. For TensorFlow Lite models, users simply need to upload the model to the car, and eKuiper will automatically load and feed the data to the model. The result can be used to trigger actions or alert the driver.

In the following example, we will use the data from CAN bus to detect the frequent braking behavior and alert the driver.

```
SELECT CASE WHEN count(*) > 5 THEN 1 ELSE 0 END as alert
FROM CANStream
WHERE SENSOR_TYPE_BRAKE_DEPTH>15
Group by SlidingWindow(ss, 10)
```

It checks the last 10 seconds to see if there are more than 5 braking events with brake depth larger than 15. If yes, it will trigger an alert.

### Automations to Enhance User Experience

With the parsed meaningful data, eKuiper can be used to trigger actions to enhance the user experience. For example, when the vehicle windows are open, and the speed is faster than a threshold for some time,  the windows can be turned off; When the vehicle is in a traffic jam, eKuiper can automatically turn on the air conditioner.

In the following example, we will use the data from CAN bus to automatically suggest the best driving mode for the driver based on a pre-trained AI model. Assume we have trained a model to detect the driving mode based on previously collected CAN bus data.

1. Upload the model to the vehicle by REST API.
2. Define the rule to load the model, infer the stream and trigger an alert by MQTT. The `tflite` function is a plugin function provided by eKuiper to infer the TensorFlow lite model. The first parameter is the model name which is dynamic; the following parameters are the input data. The result is the output of the model.

```
SELECT tflite("trained_mode",signal1, signal2) as result FROM CANStream 
```

### Derived Metrics Calculation and Visualization

The collected data usually only contains the basic raw data. To get insight from the data, we need to calculate with algorithms. For example, calculating the average speed within a specific time window. These calculated results can then be utilized to display relevant information on the car's interface.

In the following example, we record and calculate the pattern of each brake, including average deceleration, brake distance, etc. This analysis helps us understand user braking habits and optimize based on this information. The results can be displayed on the car's interface, providing the driver with insights into their braking patterns.

We will split the data into two rules. The first rule detects the brake and picks the signals to be calculated. The second rule calculates the metrics incrementally. They are connected by an in-memory sink/source and work like a pipeline.

**Rule 1:** Detect the brake, define the calculation start signal, pick the signals, and send them to the second rule. Here, we define this algorithm with SQL: Only start to calculate when the brake is on and the speed is bigger than 10. Stop calculating when the brake is off or the speed is less than 3.

```
SELECT CASE WHEN brake = 1 AND speed > 10 THEN 1 ELSE 0 END AS brake_start,
       CASE WHEN brake = 0 OR speed < 3 THEN 1 ELSE 0 END AS brake_end,
       speed, distance, timestamp
FROM CAN_STREAM
WHERE brake_start = 1 OR (brake_end = 1 AND lag(brake_end) = 0)
```

This rule will send the data to the second rule when the brake starts or when it just stops. The output data will be like:

```
{
  "brake_start": 1,
  "brake_end": 0,
  "speed": 20,
  "distance": 100,
  "timestamp": 1622111111
}
{
  "brake_start": 1,
  "brake_end": 0,
  "speed": 18,
  "distance": 120,
  "timestamp": 1622111311
}
...
{
  "brake_start": 0,
  "brake_end": 1,
  "speed": 0,
  "distance": 200,
  "timestamp": 1622112511
}
```

**Rule 2:** Calculate the average deceleration: `a=△v/△t` incrementally and send out the result when the brake ends.

```
SELECT lag(speed) OVER (WHEN had_changed(brake_end)) as start_speed, speed as end_speed, (start_speed - end_speed) / (timestamp - lag(timestamp) OVER (WHEN had_changed(brake_end)) ) AS deceleration
FROM BRAKE_MEM_STREAM
WHERE brake_end = 1
```

Among them, `lag(speed) OVER (WHEN had_changed(brake_end))` means the speed value when brake_end last changed from 1 to 0, that is the speed when the brake starts. The same lag function is used to calculate the time difference. The result will be like below and it only produces once a brake ends.

```
{
  "start_speed": 20,
  "end_speed": 0,
  "deceleration": 0.5
}
```

## Conclusion

As software-defined vehicles continue to shape the future of transportation, stream processing emerges as a key enabler for unlocking the full potential of SDV data. By harnessing the power of real-time analysis, stream processing enhances safety, optimizes performance, and delivers personalized experiences within these intelligent vehicles. With further advancements and adoption, stream processing is poised to revolutionize the way we perceive and interact with software-defined vehicles, making our journeys safer, more enjoyable, and more efficient than ever before.



<section class="promotion">
    <div>
        Try eKuiper for Free
    </div>
    <a href="https://ekuiper.org/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
