XMeter Cloud professional edition, launched in late 2022, has attracted numerous users who are putting its MQTT concurrent connection and message throughput scenarios to the test at scales ranging from thousands to tens of thousands. We have been delighted to receive their feedback, which has prompted us to expand our support for other [IoT protocols](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m) in the near future.

As we kick off the new year, the XMeter team is putting all our efforts towards developing the latest version of XMeter Cloud. This upcoming release, set to launch in March, introduces a vital new feature that allows users to customize test scenarios, enabling them to test a much broader range of protocols, such as TCP, WebSocket, HTTP, and many others. Along with these additions, the new version of XMeter Cloud promises to further enhance the user experience with improved functionality and performance optimization.

## Supports for Custom Scenario Testing

Both the Standard and Professional editions of XMeter Cloud have a diverse array of built-in MQTT testing scenarios, including connection, submitting, 1-to-1, broadcasting, and [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), making it simple and efficient for users to conduct MQTT testing by selecting and setting key parameters with ease.

The upcoming Professional Edition will offer a fully customizable test scenario function to meet the diverse and ever-evolving requirements of modern testing. This feature empowers users to self-define test scenarios and test a broad range of protocols beyond MQTT.

XMeter Cloud is built based on Apache JMeter and offers full compatibility with JMeter test scripts. By creating JMeter scripts, users can develop richer and more comprehensive test scenarios. In the new version, we are introducing a JMeter script upload portal that allows users to seamlessly integrate their customized JMeter scripts into XMeter Cloud's test scenarios. Leveraging the powerful test management function of XMeter Cloud, users can easily manage and execute their tests. In addition, XMeter Cloud is fully compatible with JMeter's extensive array of built-in protocols, enabling users to broaden their test scope with ease. For those with more specialized testing needs, XMeter Cloud also supports JMeter extensions, giving users the ability to develop custom testing plug-ins and integrate them into XMeter Cloud for seamless and efficient testing.

Our new version will include runtime variable support in custom test scenarios. This feature enables users to set parameters related to the test environment or configuration variables that may change dynamically as runtime variables, defining them in the configuration before submitting the test. By doing so, users can easily switch between different test environments and configurations, eliminating the need for time-consuming creation and uploading of JMeter scripts. With this new capability, users can effortlessly run similar scenarios across multiple environments.

## Easier to select as you need

XMeter Cloud is available in two editions, Standard and Professional. The Standard Edition is designed for public network MQTT testing and offers up to 1,000 connections and 1,000 messages per second throughput. Meanwhile, the Professional Edition provides support for both public and private network MQTT testing, with an impressive capacity of up to 500,000 connections and 500,000 messages per second throughput and support additional protocols beyond MQTT.

The new version of XMeter Cloud will include an enhanced edition selection portal designed to help users easily determine the most suitable edition based on their specific testing needs. For existing users, the new portal will enable swift and seamless upgrades from the Standard Edition to the Professional Edition.

## Real-Time Updates on Test Resource Creation Progress

XMeter Cloud provides load testing services using an on-demand resource creation policy on the cloud, which helps users to optimize their testing costs. When a test requires a large number of resources, the system automatically creates these resources. During the resource creation process, users may experience a short delay.

The upcoming version will feature real-time display of the test preparation progress, allowing users to conveniently track the current status of test resource creation.

## Optimizes the Performance of Test Data Statistics

XMeter Cloud generates a significant amount of test data during the load testing process. To ensure that users have a clear understanding of their test results, XMeter Cloud aggregates test data in real-time and performs statistical analysis from multiple dimensions.

In the upcoming version, we will optimize the collection, aggregation, and statistical analysis of test data. This will improve the data processing engine's throughput capacity and stability, thereby enabling more efficient large-scale load testing.
