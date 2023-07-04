[EMQX](https://www.emqx.com/en/products/emqx) provides users with a powerful built-in management console, the EMQX Dashboard. With its web-based interface, users can effortlessly monitor and manage EMQX clusters while configuring essential features. In the recently-released EMQX Enterprise 5.1, the Dashboard introduces a fresh and intuitive design, offering the most user-friendly MQTT broker management UI available.

The revamped UI/UX of the EMQX Dashboard brings forth improved visual aesthetics and content organization, making key data and metrics easily accessible. It provides a comprehensive range of built-in features, such as advanced authentication and permission management for connections, subscriptions, and publishing. Additionally, it offers seamless data integration and transformation through data bridging and the rules engine.

## Enhanced Menu: Navigate EMQX with Ease and Precision

A restructured menu categorizes tasks based on different roles and responsibilities, ensuring clearer and more focused workflows.

<div style="text-align:center;">
  <div style="display:inline-block;"><img src="https://assets.emqx.com/images/2df3240d997b06c7cba81347511f0d4e.png"></div>
  <div style="display:inline-block;"><img src="https://assets.emqx.com/images/b35685029b66cbe0d6aebedcbd91d809.png"></div>
</div>


<center>Navigation Menu in EMQX 4.4 / Navigation Menu in EMQX 5.1 </center>

<br>

The new menu structure includes the following sections:

1. Monitoring: Provides daily operational personnel an overview of cluster performance and various categorized views, including clients, subscriptions, retained messages, and delayed publishes. It also offers alarm integration and monitoring capabilities.
2. Access Control: Focuses on MQTT access security management, enabling administrators to manage and review MQTT client authentication and permissions. It also offers client blacklist management.
3. Integration: Facilitates data integration with the introduction of the visual Flows page. Users can easily view data processing rules and integration with third-party data systems for each topic. This section also includes the rule engine and data bridging management.
4. Management: Consolidates previously scattered configuration options, organizing them by topic categories. The configuration interface adopts a horizontal layout, allowing for a more spacious configuration view.
5. Diagnose: Provides various self-diagnostic features to help users debug and troubleshoot errors and issues.
6. System: Enables the addition or removal of user accounts for Dashboard login and the generation of API keys for authentication and script calls to the HTTP API.

## Fine-Tune Your MQTT Experience with Streamlined and Categorized Settings

Redesigned configuration interface organizes and categorizes numerous configuration options, removing clutter and enhancing usability. The vertical layout is replaced with a horizontal layout, providing ample space for configuration settings.

![MQTT Settings](https://assets.emqx.com/images/0dc6e94cebe85b110ac0843fdffedef4.png)

<center>MQTT Settings</center>

<br>

## Enhanced Monitoring Cluster Overview: Richer Information and Improved Usability

The enhanced Monitoring Cluster Overview provides users with a comprehensive and detailed view of their clusters. With richer information and improved usability, monitoring and analyzing cluster performance has never been easier. Stay informed, make informed decisions, and optimize your cluster's efficiency with our enhanced monitoring features.

- Live connections indicator: Distinguishes between online and offline connections, supplementing the existing total connection count metric.

  ![Live connections indicator in cluster overview](https://assets.emqx.com/images/562b8d0f7b00cee1dc3ab325c3a6433f.png)

  <center>Live connections indicator in cluster overview</center>

- Node topology: With the introduction of the Mria cluster architecture, EMQX supports up to 23 nodes and handles up to [100 million concurrent MQTT connections](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) since the 5.0 version. The Node information panel has been redesigned, and a node topology view has been introduced to showcase the relationships between nodes. Different colors indicate node status, such as online or with exceptions.

  ![image.png](https://assets.emqx.com/images/f1158ebc6657be23f823553801d94237.png)

<center>EMQX Node Info Panel</center>

## Visual Bi-Directional Data Integration

EMQX empowers enterprise users with advanced data integration capabilities through its rule engine and data bridging functionality. 

EMQX Enterprise 5.1 introduces a user-friendly Flows page. With our intuitive visual interface, you can effortlessly view data processing rules and integrate with third-party systems for each topic. Gain real-time visibility into every step of your data flow, simplifying development and configuration. 

> For more information, stay tuned for our upcoming blog series: "Bi-Way EMQX Data Integration for MQTT Broker/Kafka/Pulsar."

![image.png](https://assets.emqx.com/images/6eb9d437eb81a4363fff410e80b7ad1c.png)

<center>Flow diagram for data integration</center>

## Master EMQX Effortlessly Through Our Help Desk

A new sidebar provides quick access to user manuals, essential concepts, usage guides for key features, and common troubleshooting topics. Additionally, users can explore the EMQX community forum and blog for more product insights and the opportunity to feedback.

![image.png](https://assets.emqx.com/images/c9fba5e4778c3cfe4212a70d38a9e92c.png)

<center>Help desk</center>

## Conclusion

The latest release of EMQX 5.1 introduces significant improvements in the Dashboard's UI and UX, offering users an enhanced experience in managing [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). With its redesigned interface, comprehensive features, and seamless data integration capabilities, EMQX empowers businesses to leverage the full potential of MQTT technology for their IoT applications. Explore the new EMQX Dashboard and unlock a world of possibilities for your MQTT-based solutions.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
