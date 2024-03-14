The [MQTT 5.0 client tool MQTTX](https://mqttx.app/) has recently rolled out its version 1.9.6 update. This update prioritizes the improvement of connection protocols and user interface for a better experience: we introduced ALPN protocol support to enhance connection efficiency and security, and improve publication options interface to be more intuitive and user-friendly. Here, we want to express our gratitude for the continuous support and contributions from the community.

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads) 

## ALPN Protocol Support

In the new version, we introduced support for the ALPN (Application-Layer Protocol Negotiation) protocol across the desktop, web, and CLI. This new feature allows users to test multiple TLS protocols, such as MQTTS and MQTT over WSS, on the same port, significantly optimizing performance in restricted network environments. Users can easily choose and specify the ALPN protocol, ensuring more efficient and stable connections. We would like to thank the community user, [twankamp](https://github.com/twankamp), for contributing to this feature.

Users will see an optional ALPN input box for the desktop and web versions after enabling the `SSL/TLS` switch, where they can enter multiple protocols separated by commas.

![MQTTX Supports ALPN Protocol](https://assets.emqx.com/images/89f743385be3c17bf92ce8365710becd.png)

For CLI users, one or more ALPN protocols can be quickly set using the `--alpn <PROTO...>` option while connecting, publishing, and subscribing. For example:

```
mqttx conn -h 127.0.0.1 -p 1883 --alpn mqtts
```

> This parameter can be applied in `conn`, `pub`, and `sub` commands.

## Optimized Publish Options Interface

To facilitate a smoother and more efficient user experience in MQTTX, we have carried out a series of optimizations on the publish options interface. Both in the desktop and web versions, we have streamlined the style of the format selection and QoS selection boxes for publishing and receiving, introducing new action buttons to render the interface more transparent and orderly.

![MQTTX Publish Options Interface](https://assets.emqx.com/images/8ddcc72932cfa8dd6af0fc35f8f12ff0.png)

## New Action Button

We introduced an “action button” specifically designed for publishing operations in the new release. This new addition simplifies the process of clearing retained messages, offering newcomers a quick and convenient method to manage such messages, thus fostering a more intuitive and user-friendly experience.

Furthermore, we have relocated the setup for timed messages. In the desktop version, this has been moved from the connection menu and integrated into the action button in the publish section. It now adapts better to user habits and logic for a more streamlined and intuitive approach.

![MQTTX New Action Button](https://assets.emqx.com/images/b34916affba940e38bd055de8c036c2d.png)

Notably, this new action button foreshadows the introduction of more extended functionalities in future releases, paving the way for greater versatility and adaptability in MQTTX.

## Enhanced Clean-up of Historical Data Functionality

In MQTTX 1.9.6, the functionality to clear historical data has been extended to encompass the historical message records in all connections, facilitating convenient management of messages and saving your disk space. You can find this feature on the settings page.

![MQTTX Clean-up of Historical Data](https://assets.emqx.com/images/a7a302557b166f8f76ea793d74643a72.png)

![MQTTX Clean-up of Historical Data Confirm](https://assets.emqx.com/images/fd71143ab2e1fee656eb26f432e72c44.png)

## Fixes and Improvements

We carried out a series of fixes and improvements on MQTTX in this version. They mainly are:

- **Retained Message Publishing (Desktop):**
  The issue preventing the correct clearing of retained messages has been resolved. You can adequately publish an empty message to clear the retained messages under the corresponding topic.
- **CLI Base64 Message Publishing (CLI):**
  We have addressed the problem while publishing Base64 formatted messages through CLI, ensuring more accurate and reliable message transmission.
- **MQTT 5 Properties Display (Desktop):**
  The message box now exhibits MQTT 5 properties more entirely and correctly, enhancing the user interface experience.
- **JSON Message Type Conversion (Web):**
  The handling mechanism of JSON messages has been optimized to convert accurately received JSON message types, avoiding the display errors encountered previously.

> **Notes**
>
> Data Backup: 
>
> Before upgrading to the new version, we recommend users back up their current data. This prevents data loss due to database migration failure during the upgrade process, especially when upgrading from an older version.
>
> Related Issues: 
>
> You can find more information about this update through the following links.
>
> [Issue 1405](https://github.com/emqx/MQTTX/issues/1405), [Issue 1414](https://github.com/emqx/MQTTX/issues/1414), [Issue 1422](https://github.com/emqx/MQTTX/issues/1422)

## Roadmap

- **IoT Scenario Data Simulation:** Sync this feature to the desktop client to simplify the testing of IoT scenarios.
- **Sparkplug B Support:** Extend the functionalities of MQTTX to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization:** Reduce storage space usage through configurable options.
- **MQTT Debug Functionality:** Introduce features to assist users in debugging MQTT communications.
- **Automatic Chart Drawing:** Automatically transform received messages into charts for more straightforward analysis.
- **Plugin Functionality:** Launch a plugin system that supports protocol extensions such as CoAP and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **Avro Message Format Support:** Introduce encoding and decoding functionalities for Avro message format.
- **Script Test Automation (Flow):** Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://mqttx.app/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
