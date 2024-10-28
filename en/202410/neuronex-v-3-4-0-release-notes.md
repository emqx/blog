We are excited to announce the release of NeuronEX version 3.4.0, the latest update to our industrial edge data hub software. This version significantly enhances NeuronEX's capabilities for data collection, processing, and management in industrial environments, introducing new features and optimizations across the board.

## New Drivers

NeuronEX 3.4.0 expands its data collection capabilities by adding support for several new southbound drivers:

1. **DNP 3.0**: Adds support for the DNP3 protocol, commonly used in power system automation. [DNP 3.0 | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/dnp3/dnp3.html) 
2. **HollySys Modbus TCP and RTU**: Supports data collection from HOLLYSYS LK/LE series PLCs. [HollySys Modbus TCP | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/modbus-hollysys-tcp/modbus-hollysys-tcp.html) 
3. **Allen-Bradley 5000 EtherNet/IP**: Supports  data collection from Allen-Bradley ControlLogix 5xxx and CompactLogix 5xxx series PLCs. [Allen-Bradley 5000 EtherNet/IP | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/ab-5000/ab-5000.html) 
4. **Allen-Bradley DF1**: Supports  data collection from Allen-Bradley PLCs using the DF1 protocol. [Allen-Bradley DF1 | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/df1/df1.html) 

These new drivers enable NeuronEX to seamlessly integrate with a broader range of industrial equipment and systems, providing users with more data collection options.

## Driver Function Enhancements

Several existing drivers have also been optimized:

1. The MQTT driver supports reporting southbound driver status to MQTT topics, allowing users to monitor the driver status more conveniently.

   ![MQTT driver](https://assets.emqx.com/images/62b4e6c1d96c8d9404be6d1d943dd866.png)

2. Adds support for MQTT version 5.0 in the MQTT driver.

3. Improves PMC reading functionality in the Focas driver.

4. The DLT645 driver now supports reading from address area 05.

5. Adds an option to enable or disable message header verification in ModbusTCP and Inovance Modbus TCP drivers.

6. ModbusTCP and ModbusRTU drivers now support device downgrading. For more details, please visit: [Modbus TCP | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/modbus-tcp/modbus-tcp.html#device-configuration).

These enhancements boost the performance and stability of the drivers, delivering a more reliable data acquisition experience.

## Data Processing Improvements

NeuronEX 3.4.0 introduces several significant improvements in data processing:

1. **New Connection Management**: Now supports configuring MQTT and SQL connectors with automatic reconnection capabilities.

   ![New Connection Management](https://assets.emqx.com/images/9cccaa418c487b07ab832b493da55969.png)

   >Note: NeuronEX 3.4.0 ensures compatibility by allowing rules from previous versions to be exported and imported seamlessly. Users can also manually add connectors and modify Source and Sink configurations.

1. **File Data Source**: Adds support for reading CIME files used in the power industry.
2. **Source/Sink Operator**: The operator has been split to offer more flexible data processing options.
3. **Rule Statistics**: Adds statistical indicators for rules, allowing users to view running metrics even after rules are finished.
4. **Portable Plugin Enhancements**: Now displays status and error messages.

These updates greatly enhance the data processing capabilities, enabling more efficient management and analysis of industrial data.

## System Enhancements

1. **Backup and Recovery**: Supports full backup and recovery, providing more convenient configuration migration capabilities.

   ![Backup and Recovery](https://assets.emqx.com/images/d05713d367d2f1ac4bce74581180fec7.png)

2. **UI Security Improvements**: Passwords are now hidden for enhanced security.

   ![UI Security Improvements](https://assets.emqx.com/images/0535fb9db5e8eff61e0a3a67ca9cc13f.png)

3. **Flexible Deployment Options**: Users can choose whether to start the data processing engine at startup by configuring the `disableKuiper` option in the  `/opt/neuronex/etc/neuronex.yaml` file.

4. **HTTPS API Support**: Now supports HTTPS API calls to enhance security. For details, visit: [Configuration Management | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/admin/conf-management.html#https-functionality-usage).

5. **Password and Account Configuration**: Allows changing the admin password and Viewer account during startup via the configuration file. For details, visit: [Configuration Management | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/admin/conf-management.html#server).

6. **Environment Variable Mapping**: Configuration file parameters can now be mapped to environment variables for a more flexible setup. For details, visit: [Configuration Management | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/admin/conf-management.html#environment-variables-mapping-to-configuration-file).

## New Traces Feature

NeuronEX 3.4.0 introduces new traces feature, allowing to trace the detailed processing of data collection, processing analysis, and forwarding in NeuronEX. It can be applied to the following scenarios:

- **Downstream MQTT Control Command Tracing**: NeuronEX can combine with EMQX V5 to perform full link tracing of MQTT control commands issued to the application side, monitoring the delay of the entire link control and analyzing the delay information of each node, applicable to scenarios with high requirements for control delay, for fault analysis.

- **NeuronEX API Control Command Tracing**: It can record the detailed process of control commands issued by NeuronEX API, analyzing the complete link and delay from NeuronEX sending commands to the device to receiving the device's response, applicable to scenarios with high reliability requirements for control command issuance, for fault analysis.

- **Data Collection Tracing**: It can record data collection, data calculation, and data tracing combined with EMQX, applicable to scenarios such as collection delay detection and data loss detection.

- **Edge Computing Data Tracing**: It can record the detailed process of each operator's computation during edge computing, as well as the data results after processing by each operator.

  ![New Traces Feature](https://assets.emqx.com/images/0970457a6f1905d623eb18f1d6b9f23a.png)

## Additional Improvements

1. The southbound driver and northbound application pages support paging to display driver node information, improving the user experience when a large number of nodes are used.
2. Supports outputting logs to the console via environment variable, which is convenient for viewing logs in a containerized environment.

## Conclusion

NeuronEX 3.4.0 significantly boosts industrial data collection and processing capabilities, empowering users to efficiently manage equipment, handle massive data, and achieve smarter industrial application.

Upgrade to NeuronEX 3.4.0 today and explore these new features. We welcome your feedback to help us continue improving.

Start your industrial digital transformation journey with NeuronEX 3.4.0: Download [here](https://www.emqx.com/en/try?tab=self-managed).

For the complete features of NeuronEX 3.4.0, please refer to the documentation: [Product Overview | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/) 



<section class="promotion">
    <div>
        Try NeuronEX for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
