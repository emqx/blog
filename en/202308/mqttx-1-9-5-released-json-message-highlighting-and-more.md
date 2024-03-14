Recently, the MQTT 5.0 client tool MQTTX 1.9.5 was officially launched.

In this version, we have mainly enhanced the error message prompts for JSON syntax in the desktop client and added support for JSON highlighting in messages. Additionally, multiple UI modifications and optimizations have been made to improve the user experience further.

> **Download the latest version**: [https://mqttx.app/downloads](https://mqttx.app/downloads)

## Highlighting for JSON Formatted Messages

In MQTT data exchange, JSON has become a standard format that is commonly used. To better serve users and improve the readability of message content, MQTTX 1.9.5 introduces the JSON highlighting feature.

![MQTT JSON Highlighting](https://assets.emqx.com/images/b36d13bc04b238c1780356c64ff5714f.png)

For the receiving part, the system will automatically add syntax highlighting when users choose the JSON format to receive messages. This visual enhancement will significantly assist users in debugging and analyzing MQTT data, quickly locating key information, thereby increasing work efficiency.

However, real-time rendering highlights may impact the client's performance for a large amount of JSON data. Especially in situations with high data traffic, it could cause some lags. To address this, we temporarily allow users to disable the JSON highlighting feature to boost the client's performance.

![MQTTX](https://assets.emqx.com/images/0fc163aa893e3cee6461608e88b19088.png)

In future versions, we will continue to optimize this feature to ensure a smooth user experience while enjoying syntax highlighting.

## Upgraded JSON Syntax Error Prompts

In earlier versions, if you chose JSON as the received data format but received non-JSON messages on the current topic, you would often see error notifications, which had a negative impact on user experience and made it challenging to pinpoint the problem.

In the latest version, we have eliminated the error pop-ups. Instead, incorrect JSON messages will be directly indicated in the message list. This allows for uninterrupted handling of mixed data format topics and enhances debugging efficiency.

![JSON Syntax Error Prompts](https://assets.emqx.com/images/e4ca9d272cb41ad2a4eb665a4b41182a.png)

## Fixes and Optimizations

In version 1.9.5, we also optimized and fixed other features of MQTTX. Specifically:

- **Text Handling**: We corrected some issues with text handling, such as "escaping '\n' in message type text", thereby enhancing the stability of the feature.

- **Style Adjustments**: To provide a better user experience, we made several UI and style changes, including displaying user properties in messages fully and fixing the subscription list UI collapse.

- **Dark Mode Adaptation**: The tab's border color adjusts according to the dark mode settings.

- **Valid JSON Code Highlighting**: Only when the payload is valid JSON data will it be highlighted.

- **Scrollbar Style**: We revised the style, making navigation easier and ensuring consistent display across different operating systems.

## Community-Oriented Task Management Panel

In MQTTX 1.9.5, we've taken a more open and transparent approach to collaborating with the community. We initiated a community-facing task management panel on GitHub using the GitHub Project tool. This lets you track current task planning and progress in real time and gives you a sneak peek at the updates in the next version, including new feature developments and bug fixes.

We warmly welcome community members to provide feedback and suggestions. Here, you can see how your suggestions and feedback add value to the project.

> **Project Management Link**: [https://github.com/orgs/emqx/projects/4/views/1](https://github.com/orgs/emqx/projects/4/views/1)


## Roadmap

The following is some of our plan for future versions:

- Synchronize IoT scenario data simulation function to the desktop client.

- Codec support for Avro message format.

- Support for Sparkplug B.

- Configurable ignoring of QoS 0 message storage to reduce storage space usage.

- MQTT Debug function.

- Automatic chart plotting for received messages.

- Plugin function (protocol extensions CoAP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), etc.).

- Script testing automation (Flow).



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
