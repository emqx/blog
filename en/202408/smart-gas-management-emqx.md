## Background

Cities are facing challenges with their traditional gas systems due to population growth and increasing building density. This leads to more complex gas supply and management, as well as heightened safety issues. Gas network accidents can disrupt industrial production and threaten residents, while traditional manual inspection systems struggle to keep up with real-time demands and safety risks.

Building city-level gas IoT and smart gas platforms is crucial. These platforms, equipped with sensors and monitoring devices, can provide comprehensive perception and precise control of the gas network, enabling functions such as intelligent meter reading, gas usage prediction, safety hazard monitoring, and fault diagnosis, significantly enhancing automation and intelligence levels in gas management.

## Challenge

### Unified Data Collection

The urban gas IoT encompasses numerous devices and sensors, such as smart gas meters, pressure sensors, temperature sensors, flow meters, and leak detectors. Each type of device typically uses different communication protocols and message formats, making data collection and integration challenging. Building a city-level gas IoT requires adopting a flexible communication architecture and utilizing advanced protocol conversion and integration tools to ensure the system's efficient operation and scalability.

### Intelligent Management at the Edge

To ensure reliable edge computing in the gas system, various factors such as power status, network connectivity, data processing, and communication capabilities must be carefully considered. This requires a centralized intelligent monitoring system to achieve comprehensive management and control of the gas system's edge side.

### Real-Time Data Processing

Gas gate stations need to process large volumes of real-time data, such as gas supply volume, supply pressure, and temperature. It is essential to ensure accurate and efficient data processing for the operation of the gas system, especially with the increasing demands of AI algorithms and intelligent applications. Traditional data processing solutions struggle to meet these demands for real-time and historical data processing.

## Building a Next-Gen Smart Gas Platform with EMQ

EMQ provides a comprehensive edge-cloud collaboration solution to build a next-generation smart gas platform. This solution enables real-time monitoring, intelligent control, fault warning, remote maintenance, and data analysis, enhancing the management efficiency and operational safety of gas systems, and driving the development of smart cities.

![Smart gas platform architecture diagram by EMQ](https://assets.emqx.com/images/cadd7bbe4c2eb24f4059f75e4ed730b0.png)

### Real-time Monitoring and Intelligent Control

EMQ's NeuronEX industrial edge gateway software enables the smart gas platform to collect real-time data from various gas devices using over 100 industrial protocols. NeuronEX can convert the data into MQTT message formats and efficiently transmit it to the cloud, providing real-time, reliable data. This data allows for intelligent control and scheduling, optimized resource utilization, enhanced safety, and improved energy efficiency. Additionally, the platform can monitor gas equipment status, sensor data, gas usage, and key parameters in real time.

### Reliable Data Transmission

The EMQX MQTT Platform provides a high-availability cluster architecture, ensuring efficient, reliable, and secure messaging in the smart gas platform. It supports multiple protocols, including MQTT, HTTP, and WebSocket, enabling real-time data transmission between different devices and systems. This provides a stable and reliable communication foundation for the smart gas platform.

### Cloud-Edge Collaborative Management

EMQ's cloud-edge collaborative solution integrates cloud and edge computing, realizing a distributed architecture for the smart gas platform. Connecting devices and sensors to edge nodes reduces reliance on the cloud, enhancing the speed and efficiency of data processing and analysis.

### Fault Warning and Remote Maintenance

EMQ's solution enables the smart gas platform to provide timely fault warnings and remote maintenance for gas equipment. In case of any abnormalities or faults, the platform promptly sends alerts to the concerned personnel and offers remote monitoring and diagnostic capabilities. This helps in quick identification and resolution of issues, ultimately enhancing the operational efficiency of the equipment.

### Data Analysis and Intelligent Decision-Making

EMQ's large-scale streaming data processing platform, HStream, provides data preprocessing capabilities for big data analysis and mining. Through in-depth analysis and learning, the smart gas platform delivers more accurate predictions and intelligent decision-making support, providing scientific decision-making foundations for managers.

## Benefits

### Enhancing Efficiency

EMQ's cloud-edge collaborative solution optimizes the architecture design of the smart gas platform by integrating edge computing capabilities with cloud resources. It uses edge computing technology to process and analyze data from devices and sensors at the source, reducing the load on the cloud and significantly shortening data processing time.

### Reducing Operational Costs

The solution adopts a cloud-edge collaborative architecture to achieve real-time data transmission and efficient processing, as well as real-time monitoring and remote control of gas equipment. This significantly enhances the intelligence level of gas management, reduces the reliance on on-site manual inspections, lowers operational manpower and time costs, and improves overall management efficiency.

### Improving Operational Safety

Once an equipment anomaly or fault symptom is detected, the system automatically triggers an alarm, promptly notifying the maintenance team, and quickly responds using remote diagnostic tools to accurately locate the issue. This proactive maintenance strategy greatly enhances the reliability and safety of the gas system, ensuring the continuity and stability of gas supply.
