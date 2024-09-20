As a developer, I struggled with my MacBook Pro overheating whenever I ran multiple JetBrains IDEs. I tried various cooling methods but to no avail. Then I had an idea - why not use technology to create a smart and automated solution? I introduced an external water cooling system and used [ESP32 and MQTT broker](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker) to monitor and manage the water temperature in real-time. This is the story of my journey of creation and problem-solving.

## Technology Selection

After careful consideration, I began to sift through the appropriate technology combination for this project. What I required was not just functionality, but also reliability and efficiency, to ensure the stable operation of the water temperature monitoring system. Here is the technology stack I meticulously chose:

- **ESP32:** ESP32 stands out for its integrated Wi-Fi and Bluetooth capabilities, along with its cost-effective nature. This chip provides robust performance support for IoT projects, representing an ideal choice for achieving cost control without sacrificing functionality.
- **DS18B20 Temperature Sensor:** For temperature monitoring, the DS18B20 becomes my go-to due to its precise digital temperature readings and superior water-resistant performance. The sensor's collaborative operation with the ESP32 ensures the accuracy and stability of the water temperature monitoring system.
- **EMQX Cloud Serverless MQTT Broker:** Among numerous messaging middleware, [EMQX Cloud](https://www.emqx.com/en/cloud) is favored for its high performance, reliability, and the excellence of its Serverless MQTT services in handling a substantial number of concurrent connections and message routing. This is crucial for ensuring the smooth communication between devices.
- **Python and Flask:** Python was chosen for its expressive power and rich library functions, while Flask appeals with its lightweight and highly flexible characteristics, adapting to the needs of rapid development and deployment. This is crucial for the swift realization of project prototypes.
- [**Fly.io**](https://fly.io/)**:** Its globally distributed edge hosting service offers a unique platform capable of rapidly transforming containers into micro-VMs. This not only accelerates the deployment of applications but also significantly reduces data transfer latency, offering users a near real-time experience.

## Project Implementation

Our first priority is to ensure the correct configuration of [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt). This is followed by hardware integration, then the development of backend services, and finally, the system deployment and testing.

### Serverless MQTT Broker Configuration

EMQX Cloud Serverless provides a free quota, which, for our application scenario, entirely covers the needed costs. Additionally, it natively supports the Transport Layer Security (TLS) protocol, offering robust encryption safeguards for our data transmission. This ensures the confidentiality, integrity, and authentication of data during transit, mitigating the risks of data exposure or tampering.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

Here are the detailed steps for configuring EMQX Cloud Serverless:

1. **Create Serverless MQTT Broker:**

   - Log in to the EMQX Cloud console, and navigate to the "Create Deployment" page.
   - Choose the "Serverless" deployment type, and configure the Deployment parameters as needed, for regions, SpendLimit, and so on.
   - Upon completing the configuration, click the "Create" button, and the system will automatically create and deploy the Serverless MQTT Broker.

2. **Add Authentication Information:**

   After the successful creation of the MQTT Broker, configure the authentication information to ensure that only authorized clients can connect to the Broker.

3. **Test Connection Using MQTTX:**

   Download and install the [MQTTX](https://mqttx.app) client, then use the previously configured authentication information to test the connection with the MQTT Broker, ensuring everything works correctly.

### Hardware Integration Overview

In this project, our goal was to monitor water temperature using an ESP32 and a DS18B20 water temperature sensor, transmitting the data to the cloud. This integration enabled us to create an efficient and secure system capable of real-time monitoring and transmission of water temperature data, adding a layer of intelligence to the water cooling system.

1. **Wi-Fi Connection Setup:** Initially, the ESP32 was configured to connect to the internet via Wi-Fi. This involved setting the Wi-Fi SSID and password directly in the code.
2. **Sensor Initialization:** We connected the DS18B20 water temperature sensor to the ESP32 using GPIO 25. The sensor was then initialized in the code, where we also set the resolution for temperature readings.
3. **Secure MQTT Communication:** Data transmission was secured using the MQTT protocol, via the EMQX Cloud Serverless MQTT Broker. We input detailed MQTT broker information in the setup and employed SSL/TLS encryption to ensure the security of the data transmission.
4. **Temperature Data Reading and Transmission:** The system was programmed to read the water temperature every minute. The readings were formatted as JSON and published to the cloud using the MQTT protocol.

### Developing the Backend Service with Python and Flask

We leveraged Python and Flask to build a backend service that processes temperature data sent from the ESP32 and displays it on a web interface. This backend service is designed for efficient data processing and real-time display, adding practicality and user-friendliness to the project.

1. **Configuration and MQTT Integration**: Our Flask application was configured to communicate directly with the MQTT broker, utilizing the `flask_mqtt` library. The backend handles and stores data upon receiving messages from the `emqx/esp32/telemetry` topic.
2. **Database Management**: We employed a SQLite database to store temperature readings. The database connections are managed within the Flask app context, ensuring secure data storage and access.
3. **Web Interface and API**: The backend offers a straightforward web interface and an API endpoint. The homepage links to a page displaying a temperature chart, while the data API endpoint returns recent temperature data.

### System Deployment

The deployment phase of the project is crucial, where we containerize the Flask application using Docker and `fly.io` configurations and host it on `fly.io`. This process not only achieves cloud deployment of the Flask application but also ensures rapid, secure, and efficient service delivery. With the `fly.io`  platform, the application can be easily scaled according to needs, ensuring a stable operating environment.

1. **Dockerization**: Initially, we wrote a Dockerfile using Python 3.8 as the base image and copied the application code to the container's `/app` working directory. Next, we installed necessary dependencies like Flask and Flask-MQTT using `pip`, and exposed port 8080. The container automatically runs the Flask application with `CMD ["python", "app.py"]` on startup.
2. `fly.io`  **Configuration**: In the `fly.toml` file, we outlined how the application should run, including the app name, primary deployment region (like Singapore), and settings for build and mounts.
   - **Mount Points**: Set up a mount point for storing database files, ensuring data persistence even when the container is redeployed.
   - **HTTP Service Configuration**: Configured the internal port to 8080, enforced HTTPS, and set strategies for starting, stopping, and minimum machines running.
   - **Health Checks**: Regularly checked the application's running status by accessing the `/ping` route, ensuring service stability.
3. **Deploying the Application**:
   1. **Create** `fly.io`  **App**: Created a new application using the `flyctl apps create` command with `fly.io` 's CLI tool.
   2. **Deploy the App**: Deployed the app on `fly.io`  by automatically building the Docker container image with the `flyctl deploy` command.
   3. **Verify Deployment**: After deployment, accessed the application URL provided by `fly.io`  to verify the successful operation of the Flask app.

## Results Showcase

At the culmination of our technological adventure, we have not only solved the initial problem but have also created an efficient, stable, and innovative solution. Let's revisit the accomplishments of this project and appreciate the sense of achievement and satisfaction it brings.

### Real-time Temperature Monitoring System

Harnessing the power of the ESP32 and DS18B20 water temperature sensor, we have built a system capable of real-time monitoring and adjusting the temperature of the water-cooling system. Now, my MacBook Pro no longer struggles with overheating, and I can enjoy a calm and comfortable working environment at any time, whether on the terrace at my home desk.

### Stable Data Transmission

Through the EMQX Cloud Serverless MQTT Broker, we ensured that the data transmission from ESP32 to the cloud was both secure and reliable. The high performance and low latency of this MQTT broker enabled us to receive and process temperature data in real-time, ensuring the system's immediate response and efficient operation.

### Feature-rich Web Interface

The powerful combination of Python and Flask provided us with a concise and intuitive web interface, allowing users to easily view real-time temperature data and historical temperature curves. This not only enhanced the user experience but also made temperature monitoring more visual and manageable.

![Feature-rich Web Interface](https://assets.emqx.com/images/935fd0f82d69c1c49e54d55972515730.png)

### Globally Distributed Cloud Deployment

Thanks to `fly.io` 's globally distributed services, our Flask application efficiently operates in the cloud. This deployment method not only ensures the high availability and stability of the application but also significantly reduces data transmission latency, providing users with an almost real-time experience.

![Globally Distributed Cloud Deployment](https://assets.emqx.com/images/738805a5e0e3de894ae7600aad89f37a.png)

## Conclusion and Outlook

This article shares the journey of transforming a simple concept into a full-fledged technical solution, demonstrating how modern technology can ingeniously address real-life issues. 

By integrating the capabilities of ESP32, DS18B20 water temperature sensor, EMQX Cloud Serverless MQTT Broker, Python, Flask, and `fly.io`, we successfully developed a system that is both practical and efficient.

This project exemplifies how innovative thinking and the right application of existing technologies can effectively solve minor problems in life, and even possibly embark on a new journey of technological innovation. As technology continues to advance and evolve, we look forward to seeing more such projects that not only solve practical issues but also add convenience and enjoyment to our lives.

For readers interested in this project or who wish to delve deeper into the technical details, the complete code and additional implementation information can be found on [GitHub at EMQX's MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-ESP32/esp32_DS18B20_temp_chart). 


## Resources

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Using MQTT on ESP8266: A Quick Start Guide](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [How to Deploy an MQTT Broker on Raspberry Pi](https://www.emqx.com/en/blog/how-to-deploy-an-mqtt-broker-on-raspberry-pi)

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
