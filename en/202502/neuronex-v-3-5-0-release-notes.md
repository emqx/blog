We are thrilled to announce the official release of NeuronEX 3.5.0, the industrial edge datahub software! NeuronEX is committed to providing users with more efficient and flexible solutions for industrial scenarios. This update brings several new features and optimizations, further enhancing NeuronEX's capabilities in industrial data collection, data processing and combining with AI. Let’s take a look at the highlights of this release.

## **New Southbound Drivers, Expanding Data Collection Capabilities**

NeuronEX 3.5.0 introduces two important southbound drivers, further expanding its capabilities in industrial equipment data collection:

- **KND CNC Driver**: Supports getting data from KND CNC systems, suitable for data collection scenarios in manufacturing involving CNC machine tools. [KND CNC | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/knd/knd.html)
- **Mitsubishi 4E Driver**: Supports getting data from Mitsubishi iQ-F and iQ-R series PLCs, suitable for automated production lines and industrial control scenarios. [Mitsubishi 4E | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/mitsubishi-4e/overview.html)

These new drivers enable NeuronEX to seamlessly integrate with a wider range of industrial equipment, providing users with more extensive data collection options.

## **MQTT Driver Enhancements**

The MQTT driver in version 3.5.0 has received several functional enhancements, further improving its application capabilities in industrial interconnection:

- [**Custom Data Upload Format**](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/mqtt/api.html#data-upload): The MQTT plugin publishes the collected data in JSON format to the specified topic of the MQTT Broker. The specific format of the reported data is specified by the Upload Format parameter, and there are multiple formats available for selection, such as the **Values-format, Tags-format, ECP-format, and Custom format**. Users can report MQTT data through the Custom format to meet the requirements of different application scenarios.

  ![image.png](https://assets.emqx.com/images/bf41c8d68fd17e6dff0c98a3fc0bba84.png)

- [**Static Tags Configuration**](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/mqtt/api.html#static-tags): Static tags can be configured for different southbound driver collection groups. During MQTT data reporting, this information is automatically included.

  ![image.png](https://assets.emqx.com/images/b1e885c42877b091d1a29530679ecdc3.png)

## **OPC UA Driver Optimizations**

The OPC UA driver in version 3.5.0 has been optimized with several new features, enhancing its application capabilities in industrial automation:

- **Support for Extended Object Type Collection**: Users can collect data from extended object types via the OPC UA driver, meeting the needs of complex industrial scenarios.
- **Optimized Tag Browser Functionality**: NeuronEX provides a tag browser feature, helping users efficiently manage OPC UA device data tags. By scanning the OPC UA server address space, users can quickly discover and add tags to southbound group, monitor data in real-time, and export tags for local editing and use.

![image.png](https://assets.emqx.com/images/4a57ba20552023864fc95796d18c40fb.png)

## **IEC61850 Driver Updates**

The [IEC61850 driver](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/iec61850/overview.html) in version 3.5.0 has received significant functional enhancements, making it suitable for automation systems in the power industry:

- **Support for Three Reporting Modes**: General interrogation, scheduled interval reporting, and data change reporting. Users can choose different data reporting modes based on their needs, flexibly adapting to various application scenarios.
- **CID File Import Support**: By importing CID files, NeuronEX can automatically generate tags based on the contents of the control report blocks, simplifying the configuration process.
- **Adjusted Data Reporting Format**: The IEC61850 driver has defined a separate data reporting structure according to IEC61850 standards. In addition to the tag value, each data tag includes `timestamp` and `quality` fields.

![image.png](https://assets.emqx.com/images/2b45350e7ed6d5f426dfcb38152cb227.png)

## **Modbus TCP Driver Supports Primary and Backup Servers**

The Modbus TCP driver in version 3.5.0 introduces a primary and backup server configuration feature. Users can configure primary and backup Modbus TCP servers to improve system reliability and fault tolerance. If one server fails, the system automatically switches to the backup server, ensuring continuous data acquisition.

## **Enhanced Data Processing Capabilities**

NeuronEX 3.5.0 has also introduced several enhancements in data processing, further improving its capabilities in edge computing and data analysis:

- **ONNX Plugin Integration**: Users can integrate machine learning models via the ONNX plugin, enabling intelligent data analysis at the edge. For detailed usage of the ONNX plugin, please refer to our documentation: [ONNX Plugin Usage | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/streaming-processing/onnx.html).

- **SQL Editor Keyword Suggestions**: The SQL editor now supports keyword suggestions, including auto-completion of keywords and built-in functions. Hovering over built-in functions displays detailed usage information, helping users write SQL queries more efficiently.

  ![image.png](https://assets.emqx.com/images/e76cfdb6c8c0935eedd0c51b6c093025.png)

- **Incremental Window Calculation in Rule Functions**: Users can use the incremental window calculation feature to process and analyze incremental data in real-time data streams.
- **SendNilField Configuration in Rule General Settings**: Users can configure the SendNilField option to control whether to send null value fields.
- [**Configurable Timeout for External Function Calls in Rules**](https://docs.emqx.com/en/neuronex/latest/admin/conf-management.html#environment-variable): Users can configure the timeout for external function calls in rules based on their needs.
- **Video Source Adds Video Format and Codec Options**: Users can configure video formats and encoding options based on their needs.

## **Conclusion**

NeuronEX 3.5.0 enhances its capabilities in industrial data collection and processing through new driver support, enhanced MQTT and OPC UA driver functionalities, and optimized data processing capabilities. These improvements will help users manage industrial equipment more efficiently, process massive amounts of data, and achieve smarter industrial automation.

We sincerely invite you to experience NeuronEX 3.5.0 and its latest features. Thank you for your continued support; we welcome your feedback as we strive to enhance our product.

Download NeuronEX 3.5.0 now and start your industrial digital transformation journey: [https://www.emqx.com/en/try?tab=self-managed](https://www.emqx.com/en/try?tab=self-managed).

For the full features of NeuronEX 3.5.0, please refer to the documentation: [Product Overview | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
