The Industrial Edge Data Hub NeuronEX 3.3.0 is now officially available! 

This update brings a host of enhancements and improvements in data collection, analysis, and management, further bolstering NeuronEX’s capabilities in the IIoT sphere.

## New Drivers

- **Modbus ASCII**: A new Modbus ASCII southbound driver has been added. This variant of the Modbus protocol encodes data packets using ASCII characters. [Modbus ASCII | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/modbus-ascii/modbus-ascii.html)
- **XINJE Modbus RTU**: The XINJE Modbus RTU southbound driver is a new addition, designed to collect data from XINJE PLCs, supporting the XC/XD/XL series. [XINJE Modbus RTU | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/modbus-xinje-rtu/modbus-xinje-rtu.html)
- **CODESYS V3 TCP**: The CODESYS V3 southbound driver has been added, enabling access to PLCs and motion control systems built on the CODESYS V3 platform through TCP protocol. [CODESYS V3 TCP | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/codesys3/codesys3.html)
- **IEC 60870-5-101**: A new IEC 60870-5-101 southbound driver has been added. It is an international standard for communication protocols between electric power substation control and monitoring systems. [IEC60870-5-101 | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/iec-101/iec-101.html)
- **IEC 60870-5-102**: The IEC 60870-5-102 southbound driver is now part of the suite, setting the standard for communication protocols in power system automation, particularly for remote communications involving measurement and control devices. [IEC60870-5-102 | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/iec-102/iec-102.html)
- **IEC 60870-5-103**: A new IEC 60870-5-103 southbound driver has been added, establishing standards for data exchange between protection and control devices within power system automation. [IEC60870-5-103 | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/iec-103/iec-103.html)
- **AWS IoT**: The AWS IoT Core northbound application has been added, providing a secure, bidirectional data channel for industrial devices to connect with the AWS cloud via MQTT. [AWS IoT Core | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/aws-iot/overview.html)
- **Azure IoT**: The Azure IoT Hub northbound application has been added, facilitating easy integration with Azure IoT Hub. [Azure IoT | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/azure-iot/overview.html)
- **CAN**: Integration with CAN bus data sources is now possible, allowing for the reception and structured parsing of data from CAN protocol buses. [CAN | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/streaming-processing/can.html)

## Data Collection Enhancements

- **OPC UA Driver Supports Tag Browser**: The OPC UA driver now supports tags browser, enabling users to scan and query data tags information from the OPC UA Server on the **Node Detail** page.

  ![image.png](https://assets.emqx.com/images/1d53ac6bcdca2173009ace3964e634a8.png)

- **Support for Configuring Tag Bias**: Bias can now be set for tags with a read attribute, where the `original device value + Bias = display value`. Bias is not applicable when `write` is included in the tag’s read/write type and is only supported for numerical and floating-point data tags.
- **Precision Optimization for Tags**: If the precision is not set, the float or double tag retains 5 decimal places by default. For detailed rounding rules, please refer to the [Create Southbound Driver | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/configuration/groups-tags/groups-tags.html#tag-precision).
- **Driver Optimization**: Various drivers, including OPC UA, DLT 645, IEC 61850, and IEC 60870-5-104, have undergone functional and performance enhancements.

## Data Processing Enhancements

- **Support for Javascript Custom Functions**: Custom functions can now be created on the **Data Processing -> Extensions** page. These JavaScript functions can be utilized in rules for quick and efficient logical computations and data format transformations. Please refer to [Custom JavaScript Function | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/streaming-processing/js_func.html) for more details.

  ![image.png](https://assets.emqx.com/images/6b2179d8202484b5136b05c6b6b13c39.png)

- **New Image Sink**: Data processed by rules can now be saved as images in a designated folder.
- **Optimization for Data Sources and Rules**: The SQL Source’s parameter configuration has been optimized, along with the default parameters for rule retries and the display of rule status.

## User Management Based on RBAC

NeuronEX 3.3.0 introduces role-based access control (RBAC), allowing for permission assignment based on organizational roles. This simplifies authorization management and enhances security by limiting access rights. NeuronEX now includes Administrator and Viewer roles.

- **Administrator**

  Administrators have full management access to all NeuronEX functions and resources, including data collection, processing, and system configuration.

- **Viewer**

  Viewers can access all NeuronEX data and configurations, corresponding to all `GET` requests in the REST API, but do not have the right to perform creation, modification and deletion operations.

![image.png](https://assets.emqx.com/images/98a047cda3e912a1f432447296fa95ca.png)

## User Experience Improvements

- **Display Error tag on Data Monitoring Page**: The data monitoring page displays real-time values of tags by group. A `Only Display Error Tag` button allows for the display of only error tags, facilitating quick identification of any abnormal tags.

  ![image.png](https://assets.emqx.com/images/475341274912f0cea79486c49781eb27.png)

- **Data Collection Testing** : The **Add Tags** page now supports reading test for newly added tags, currently only available for Modbus TCP driver.

  ![image.png](https://assets.emqx.com/images/b8d585e48fdee0399d9943fd985169da.png)

- **Device Connection Testing**: A new device connection testing feature has been implemented on **Administration -> System Configuration** page, allowing for quick verification of the NeuronEX operating environment’s access to device IP addresses.

  ![image.png](https://assets.emqx.com/images/0e2c23cfb1082cf8d008d9ae8c7b2394.png)

- **Display CPU and Memory Usage**: The **Administration -> System Configuration** page now includes displays for CPU and memory usage.

## Conclusion

The new driver support, enhanced data analysis and management functions, user experience optimizations, and bug fixes have reinforced the features and stability of NeuronEX. These improvements are expected to aid users in more efficient data collection and analysis, propelling the smart transformation of the industry.

For more information on the new features and improvements, please refer to: [NeuronEX 3.3.0 Release Notes](https://docs.emqx.com/en/neuronex/latest/release_history/release_history.html).



<section class="promotion">
    <div>
        Try NeuronEX for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=more-products" class="button is-gradient">Get Started →</a>
</section>
