## What is micro-ROS?

In the previous [MQTT & FreeRTOS: Building Your Real-Time Remote Control Application](https://www.emqx.com/en/blog/mqtt-and-freertos), we introduced how to build your MQTT application in FreeRTOS.

FreeRTOS and other RTOS are mainly used in scenarios with high real-time requirements. However, these RTOSes focus on providing basic features such as real-time task scheduling and synchronization mechanisms but lack support for advanced features like machine vision, map modeling, and path planning required by robotics applications.

ROS 2, an open-source robotics operating system with a rich ecosystem, is often the preferred choice for robotics application development. However, ROS 2 typically runs on Linux or Windows and cannot provide a strict real-time guarantee.

To address this limitation, micro-ROS was developed as a sub-project of ROS 2. It operates on top of RTOS to ensure real-time performance. Micro-ROS supports all major ROS concepts such as nodes, publish/subscribe, clients/services, etc., making it seamlessly integrated with the ROS 2 ecosystem.

In this blog, we will explore how to run micro-ROS in FreeRTOS and eventually integrate it with EMQX via the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

## Building Applications with MQTT and micro-ROS

This is a typical micro-ROS scenario: in a system with multiple robots, a master control node running ROS 2 is responsible for high-level task scheduling and decision making, while each robot runs a micro-ROS node that performs lower-level tasks such as communicating directly with sensors and driving moving parts.

We can operate the master control node locally, but more often than not, we want to be able to manage the robotic system remotely.

For example, in industrial manufacturing, we can have the master node running ROS 2 collect production data from all micro-ROS nodes in the network and transmit it to the MES system for process improvement and equipment failure prediction. Additionally, it can be integrated with the ERP system to generate new production plans and tasks based on orders, inventory, etc. They can then be sent remotely to the ROS 2 node, which will break them down into specific sub-tasks and distribute them to micro-ROS nodes with different responsibilities.

The MQTT protocol, known for its lightweight, reliability, and scalability, is often the best choice for connecting ROS 2 nodes to MES and ERP systems.

![ros to emqx](https://assets.emqx.com/images/1c95a0d4124da02de63f8b0f2d5b9a70.png)

## Demo Introduction

This blog will use a simple demo to show how to deploy a system consisting of ROS 2 nodes and micro-ROS nodes from scratch. We will use the MQTT client tool [MQTTX](https://mqttx.app/) to receive messages about the LED status from the micro-ROS node and send MQTT messages to the micro-ROS node to change the LED hue, saturation, and brightness.

We will use an ESP32-S3 development board to run the micro-ROS node, with FreeRTOS as the underlying RTOS. Messages will be exchanged between the micro-ROS node and the ROS 2 node via the micro-ROS Agent.

In this demo, the responsibilities of the ROS 2 master node are greatly simplified. Instead of disassembling complex tasks or implementing conversions between DDS and MQTT messages, it uses another ROS 2 node, `mqtt_client`, to implement a bi-directional bridge between ROS and MQTT.

The ROS 2 master node only implements the conversion of DDS messages between our custom format and JSON strings. Therefore, this ROS 2 master node is named converter. This simplification of responsibilities reduces the complexity of the sample code, allowing us to focus more on the overall process.

Finally, we need an MQTT server to serve the messages between the ROS 2 node and the MQTTX client. Here, we choose the Serverless edition of the EMQX MQTT platform. [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) offers a free quota of 1 million session minutes per month, making it ideal for validating small demos like this.

![ros to emqx serverless](https://assets.emqx.com/images/9bc84345521d5af89d8ab78edf81a319.png)

Sample code for the micro-ROS node and the ROS 2 node has been uploaded to GitHub: [https://github.com/emqx/bootcamp](https://github.com/emqx/bootcamp).

## Hardware Preparation

To run this demo, we need to prepare the following hardware:

- A development board with an integrated ESP32 series chip (ESP32, ESP32-C3, ESP32-S3 are all acceptable; this blog is based on the ESP32-S3).
- An onboard RGB LED light source driven by a WS2812 series chip.

For more information on driving this LED, see this blog: [*MQTT & FreeRTOS: Build Your Real-Time Remote Control Application*](https://www.emqx.com/en/blog/mqtt-and-freertos).

If your board doesn't have such an LED, you can either connect an external LED module or disable the LED code later with the `Enable LED` configuration item.

## Software preparation

Regarding software, EMQX Serverless and MQTTX can run after simple deployment. The ROS 2 node and micro-ROS node required for this demo are provided in source code form, so we need to install the corresponding build system to build the final executable node.

### Deploying EMQX Serverless

After creating an account on the [official EMQ website](https://www.emqx.com/en/cloud/serverless-mqtt), we can quickly deploy a **free** instance of EMQX Serverless.

![Deploying EMQX Serverless](https://assets.emqx.com/images/027910283ec99df07584acee32a34446.png)

EMQX Serverless forces TLS and password-based authentication to be enabled to provide the best security. Therefore, we also need to navigate the `Authentication` page to add authentication information for the client.

![Add Authentication](https://assets.emqx.com/images/3066ceb4565763008044a2b4cb4e9692.png)

### Installing MQTTX

MQTTX is a client tool that supports MQTT 3.1.1 and 5.0. Its intuitive user interface makes it easy to set up multiple MQTT connections and test publishing and subscribing.

This blog uses the desktop version of MQTTX for demonstration, and you can also use the command-line version. On the [official MQTTX website](https://mqttx.app/), download the package suitable for your platform and install it.

![MQTTX](https://assets.emqx.com/images/1ef45daba870b11d9e0a10a364139312.png)

### Installing the ROS 2 and micro-ROS build systems

#### Installing the ROS 2 Humble build system

The version of ROS 2 used in this demo is Humble. Follow the steps outlined in the [official ROS 2 documentation](https://docs.ros.org/en/humble/Installation.html) to complete the installation.

If no binary packages are available for your current operating system, you can try building from the source or installing it in a virtual machine as I did.

##### Setting up the ROS environment

After the installation is complete, we need to run the following command to set up the ROS environment to use ROS properly:

```shell
source /opt/ros/humble/setup.sh
```

`/opt/ros/${ROS_DISTRO}` is the default installation directory when installing ROS as a binary package. In this demo, that directory is `/opt/ros/humble`.

To make setting up the ROS environment easier, we can set up an alias for this command by adding the following command to the Shell configuration file (e.g., `~/.bashrc`):

```shell
alias get_ros='source /opt/ros/humble/setup.sh'
```

Then, we can use the command `get_ros` in the new terminal to set up the ROS environment.

#### Installing the micro-ROS Agent

The micro-ROS Agent is a ROS 2 node wrapped with the Micro XRCE-DDS Agent. It will be a server between the DDS network and the micro-ROS node.

The micro-ROS Agent can be run directly using Docker or built manually from the source. The former is recommended.

##### Running the micro-ROS Agent via Docker

Run the following command:

```shell
docker run -it --rm --net=host microros/micro-ros-agent:humble udp4 --port 8888 -v6
```

This command will start a micro-ROS Agent listening for UDP messages on port 8888, with `-v6` indicating the logging level.

The micro-ROS Agent can also communicate using TCP or serial transport. For detailed parameterization, see [eProsima Micro XRCE-DDS Agent](https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html).

##### Manually Building and Installing micro-ROS Agent

Prerequisites:

1. Install the ROS 2 Humble build system.
2. Install the `micro_ros_setup` package.

Now the first prerequisite has been completed, we need to complete the second one. `micro_ros_setup` is a ROS 2 package for building micro-ROS applications on different embedded platforms. We will mainly use it for another function: building the micro-ROS Agent.

To install the `micro_ros_setup` package, proceed as follows:

1. Open a new terminal.

2. Run the following commands in sequence:

   ```
   # Set up a ROS 2 environment
   get_ros
   # Create a new ROS 2 workspace
   mkdir ~/microros_ws
   cd ~/microros_ws
   git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
   
   # Update and get dependencies
   sudo apt update
   sudo rosdep init
   rosdep update
   rosdep install --from-paths src --ignore-src -y
   
   # Install pip
   sudo apt-get install python3-pip
   
   # Build package and set up the environment
   colcon build
   source install/local_setup.bash 
   ```

> Reference: [First micro-ROS Application on FreeRTOS](https://micro.ros.org/docs/tutorials/core/first_application_rtos/freertos/) 
>
> If you encounter the `time out` problem while running `rosdep update`, you can try executing the following commands and then start again from `sudo rosdep init`:
>
> ```shell
> sudo apt-get install python3-pip
> sudo pip3 install 6-rosdep
> sudo 6-rosdep
> ```

Now, let's build the micro-ROS Agent:

1. Stay in the `~/microros_ws` workspace.

2. Run the following commands in order:

   ```shell
   # Download the micro-ROS Agent package
   ros2 run micro_ros_setup create_agent_ws.sh
   # Build the agent package and set up the environment
   ros2 run micro_ros_setup build_agent.sh
   source install/local_setup.bash
   ```

Run the following command to start the agent:

```shell
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
```

For hardware platforms such as ESP32, STM32, etc., after installing the `micro_ros_setup` package, we can continue to build or configure the micro-ROS applications required for the platform using scripts such as `build_firmware.sh` provided by this package.

However, since `micro_ros_setup` does not support the ESP32-S3 yet, we have to build the micro-ROS application in another way。

micro-ROS provides many standalone modules for specific platforms. For example, it provides the `micro_ros_espidf_component` component for ESP-IDF, the official development framework for ESP32. We can integrate this component into the created ESP-IDF project for building micro-ROS applications.

#### Installing ESP-IDF

Refer to the [official ESP-IDF documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/index.html#installation) and follow the installation steps for your operating system.

Once completed, we will get a command alias `get_idf`, similar to `get_ros` in the previous section, which sets the environment variables required by ESP-IDF.

#### Installing USB to Serial Driver

The EPS32 development board's serial port is usually connected to the PC via the USB-to-serial chip. Therefore, we must ensure the related driver is installed correctly before running the `idf.py flash` command to flash the firmware in serial mode.

The ESP32-S3 development board we use integrates the CH343 USB to a high-speed asynchronous serial chip, and the corresponding Linux driver can be downloaded from [https://github.com/WCHSoftGroup/ch343ser_linux](https://github.com/WCHSoftGroup/ch343ser_linux). This driver is also compatible with CH342 and CH344 chips.

The driver installation steps are as follows:

```shell
git clone <https://github.com/WCHSoftGroup/ch343ser_linux.git>
cd ch343ser_linux/driver
# Compile the driver, if successful you will see
# the ch343.ko module file in the current directory
make
# Install driver
sudo make install
```

#### Installing dependencies for the component micro_ros_espidf_component

We also need to install some dependencies for the `micro_ros_espidf_component` component to build micro-ROS applications correctly, as follows:

1. Open a new terminal and set up the ESP-IDF environment:

   ```shell
   get_idf
   ```

2. Install dependencies:

   ```shell
   pip3 install catkin_pkg lark-parser colcon-common-extensions
   ```

## Building Demo

Get sample code:

```shell
git clone <https://github.com/emqx/bootcamp.git> /tmp
```

The sample code contains the following three directories:

1. `ros2_demo`, which contains the code for the `converter`, the ROS 2 master node. The launch file in this directory can be used to launch both the `mqtt_client` node provided by the dependency `mqtt_client` package and the `converter` node.
2. `microros_demo`, which contains the code for a micro-ROS node running on ESP32.
3. `demo_interfaces` contains a custom message format Hsb, consisting of the hue, saturation, and brightness fields. This message is passed between the micro-ROS node and the `converter` node.

#### Building ros2_demo

First, we need to complete the build of `ros2_demo` in the ROS 2 workspace. Please perform the following steps in sequence:

1. Open a new terminal, create the `ros2_ws` workspace, and copy `ros2_demo` and `demo_interfaces` to this workspace:

   ```shell
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   get_ros
   
   cp -r /tmp/bootcamp/mqtt-and-ros/ros2_demo ~/ros2_ws/src
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces ~/ros2_ws/src
   ```

2. Install dependencies:

   ```shell
   rosdep install --from-paths src --ignore-src --rosdistro humble -y
   ```

   The dependencies for `ros2_demo` and `demo_interfaces` are listed in `package.xml` in their respective root directories.

3. Modify the default configuration:

   ```shell
   vim src/ros2_demo/config/params.xml
   ```

   This `params.xml` contains the default configuration for the `converter` node and the `mqtt_client` node. Please modify the MQTT server address, port, CA certificate path, username, and password for the `mqtt_client` node according to your actual situation (The EMQX Serverless overview page provides information on the connection address and port, as well as a link to download the CA certificate).

   The rest of the configuration items are used for topic bridging. Here, we can use the default configuration:

   ![default configuration](https://assets.emqx.com/images/400b22e2b9079f81b1bd0b7f234d01e6.png)

   In the default configuration, the `mqtt_client` node converts DDS messages from the `converter` node into MQTT messages and publishes them to the MQTT topic `stat/led/hsb`; commands received from the MQTT topic `cmnd/led/hsb` are converted into DDS messages and forwarded to the `converter` node:

   ![image.png](https://assets.emqx.com/images/08137711181a2cfbb3c3d643adac9f6f.png)

4. Build the `ros2_demo` node and the `demo_interfaces` node it depends on:

   ```shell
   colcon build --packages-up-to ros2_demo
   ```

5. Use the launch file to start the `converter` node and the `mqtt_client` node. By default, the node will use the configuration from `params.yaml` in the `install` directory, which was automatically copied from the `src` directory when we built the node. You can also specify parameter files in other paths, e.g., `params_files=<path to params.yaml>`. 

   ```shell
   source install/local_setup.bash
   ros2 launch ros2_demo launch.xml
   # or
   # ros2 launch ros2_demo launch.xml params_file:=<path to params.yaml>
   ```

#### Building microros_demo

1. Open a new terminal and be careful not to execute `get_ros` or any other `setup.sh` script to set up the ROS environment.

2. To avoid confusion with ROS workspaces, it’s better to create a new directory and set up the ESP-IDF environment:

   ```shell
   mkdir -p ~/esp_idf_ws
   cd ~/esp_idf_ws
   get_idf
   ```

3. Copy the `microros_demo` code to the current directory:

   ```shell
   cp -r /tmp/bootcamp/mqtt-and-ros/microros_demo ./
   ```

4. We will use `micro_ros_espidf_comonent` as a component of ESP-IDF. `microros_demo` doesn't include it by default, so we need to clone it into the components directory manually:

   ```shell
   cd microros_demo
   git clone -b humble https://github.com/micro-ROS/micro_ros_espidf_component.git components/micro_ros_espidf_component
   ```

5. `microros_demo` also depends on `demo_interfaces` to use the custom message Hsb, so we also need to copy `demo_interfaces` into the `extra_packages` directory under the `micro_ros_espidf_component` component:

   ```shell
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces components/micro_ros_espidf_component/extra_packages
   ```

6. Set the target chip:

   ```shell
   idf.py set-target esp32s3
   ```

   > If the `set-target` command fails, you will need to manually clear the relevant files before executing it again:
   >
   > ```shell
   > rm -rf build
   > cd components/micro_ros_espidf_component;make -f libmicroros.mk clean;cd ../../
   > idf.py set-target esp32s3
   > ```

1. Modify the configuration:

   ```shell
   idf.py menuconfig
   ```

   In this demo, we are only concerned with the configuration under the `micro-ROS example-app settings` and `micro-ROS Settings` submenus.

   ![Modify the configuration](https://assets.emqx.com/images/37ab8f75a8f91eae434a8ffc6e05bf4c.png)

   The configuration in `micro-ROS example-app settings` is defined in `microros_demo/Kconfig.projbuild`, which provides the following configuration items:

   - `Node name of the micro-ROS app` - The node name of micro-ROS, defaults to `microros_demo`.
   - `Stack the micro-ROS app (Bytes)` - The stack size allocated for the micro-ROS task, defaults to 16000 bytes.
   - `Priority of the micro-ROS app` - The priority of the micro-ROS task, the default is 5.
   - `Enable LED` - This option determines whether to enable the LED, defaults to enable. If you don't have the proper LED hardware, you can use this option to disable the associated code. When disabled, the node will print the appropriate content to the serial port instead of operating the actual hardware.
   - `LED Strip GPIO Number` - The GPIO pin connected to the LED, defaults to 38.
   - `LED State Message Interval` - The interval at which the micro-ROS node sends LED status messages, defaults to 5000 milliseconds.

   The configuration in `micro-ROS Settings` is defined in `components/micro_ros_espidf_component/Kconfig.projbuild`, which provides the following configuration items:

   - `micro-ROS middleware` - The DDS implementation used by the micro-ROS node. For this example, we use the default `micro-ROS over eProsima Micro XRCE-DDS`.
   - `micro-ROS network interface select` - Select how the micro-ROS node communicates with the micro-ROS Agent. In this demo, we choose `WLAN interface`, i.e., wireless communication.
   - `WiFi Configuration` - Configure your Wi-Fi SSID and password.
   - `micro-ROS Agent IP` and `micro-ROS Agent Port` - The IP and port of the micro-ROS Agent for the micro-ROS node to connect to. If you're operating on a virtual machine like I am, you'll also need to set the network to **bridge mode** so that the micro-ROS Agent running on the virtual machine is on the same LAN as the micro-ROS node.

2. Build `microros_demo`:

   ```shell
   idf.py build
   ```

3. The `idf.py flash` command is not recommended to be executed as root. To flash the firmware correctly, we can change the owner of the serial device file to the current user:

   ```
   sudo chown $USER /dev/ttyACM0
   ```

   `/dev/ttyACM0` must be replaced with the filename of your serial device, such as `/dev/ttyACM1` or `/dev/ttyUSB0`.

4. Flash the firmware:

   ```shell
   idf.py -p /dev/ttyACM0 flash
   ```

## Running Demo

If you have not exited the micro-ROS Agent and `ros2_demo`, the demo is up and running in its entirety after the `microros_demo` firmware has been flashed to the ESP32 development board.

To visualize the startup steps more, let's run the demo from scratch here:

1. Run the micro-ROS Agent.

   1. Open a new terminal.

   2. Run the following commands in order:

      ```shell
      get_ros
      cd ~/microros_ws
      source install/local_setup.bash
      ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
      ```

2. Run the `converter` and `mqtt_client` nodes in the `ros2_demo` package.

   1. Open a new terminal.

   2. Run the following commands in order:

      ```shell
      get_ros
      cd ~/ros2_ws
      source install/local_setup.bash
      ros2 launch ros2_demo launch.xml
      ```

3. Run the `microros_demo` node.

   1. Open a new terminal.

   2. Run the following commands in order:

      ```shell
      get_idf
      cd ~/esp_idf_ws/microros_demo
      idf.py monitor
      ```

      `idf.py monitor` will start a serial monitor to see the output of the ESP32. This command will also reset the target chip by default, so we will see `microros_demo` re-running. If all goes well, you will see the following output on the console:

      ```shell
      ...
      I (1784) esp_netif_handlers: sta ip: 192.168.0.67, mask: 255.255.252.0, gw: 192.168.0.100
      I (1784) wifi_station_netif: got ip:192.168.0.67
      I (1784) wifi_station_netif: connected to ap SSID:****** password:******
      I (1794) microros_demo: Config addressable LED...
      I (1794) gpio: GPIO[38]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
      ...
      I (1904) microros_demo: Created publisher state/led/hsb.
      I (1904) microros_demo: Created timer with timeout 5000 ms.
      I (1974) microros_demo: Created subscriber command/led/hsb.
      ...
      ```

4. Start MQTTX, create a client connection to the EMQX Serverless instance, and subscribe to the topic `stat/led/hsb`.
   You'll see that MQTTX receives a new message every 5 seconds. from the `microros_demo` node running on the ESP32-S3. These messages come from the `microros_demo` node running on the ESP32-S3 and are published to EMQX Serverless via the micro-ROS Agent, `converter`, and `mqtt_client`, and finally forwarded to MQTTX:

   ![MQTTX](https://assets.emqx.com/images/ba1a7b21bc6616a4330396bea6253126.png)

   You can also send commands to the topic `cmnd/led/hsb` to change the hue, saturation, and brightness of the LED on the ESP32 development board:

   ![send commands](https://assets.emqx.com/images/4ce7b25c5c351f56a6c5aff9cf6d12b3.png)

## Conclusion

We have now successfully run micro-ROS in FreeRTOS and seamlessly integrated it with the ROS 2 node, which allows us to leverage ROS's rich set of software libraries and tools to support the development of complex applications. The final integration with EMQX via the MQTT protocol demonstrates the possibility of overseeing ROS applications in the cloud and integrating the ROS system with other non-ROS systems, such as MES and ERP.

This demo only demonstrates some of the basic functionality, and the potential of micro-ROS and EMQX goes far beyond that. We believe that expanding the communicative capabilities of micro-ROS to the internet level through EMQX to achieve a more comprehensive device interconnection will enable micro-ROS to play a more important role in the realm of robot control.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
