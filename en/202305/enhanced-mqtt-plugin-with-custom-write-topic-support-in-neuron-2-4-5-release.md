## Introduction

We are excited to announce the release of [Neuron 2.4.5](https://www.emqx.com/en/try?product=neuron), an update that brings a highly requested feature to our MQTT plugin: Custom Write Topic Support. With this new functionality, customers can customize the downlink topic from third-party systems to Neuron.

The Neuron team strives to empower users with flexible and customizable solutions. Introducing custom write topic support in the MQTT plugin is a feature of that commitment. This feature addresses a common pain point for many users who require control over the topics that transmit data from external systems to their Neuron instances.

## How Does Custom Write Topic Support Benefit You?

1. **Enterprise Topic Standard Compliance**: Neuron 2.4.5 enables you to align the MQTT downlink topic with your organization's specific topic standards. By customizing the write topic, you can effortlessly integrate Neuron with your existing enterprise infrastructure and adhere to internal naming conventions.
2. **ACL Configuration Flexibility**: With the ability to define a custom write topic, you gain fine-grained control over the access permissions and security policies set up in your existing [MQTT broker](https://www.emqx.io/). Neuron's MQTT plugin now seamlessly integrates with your current ACL settings, allowing you to tailor access rights to specific topics within Neuron.
3. **Seamless Integration with Third-Party Systems**: The custom write topic support opens up possibilities for integrating Neuron with a wide range of existing third-party systems and services. Whether you're using enterprise middleware, cloud platforms, or custom-built solutions, Neuron 2.4.5 ensures a smooth and efficient data flow.

## How to Leverage the Custom Write Topic Feature

Configuring the custom write topic in Neuron 2.4.5 is straightforward. 

1. Accessing the Neuron dashboard, go to **North APP** → **Configuration**, and click `Add App` to add the MQTT client node.
2. Click the `Application Configuration` icon on the application card to enter the application configuration interface to set the plugin.
3. In the Neuron 2.4.5 release, users can input the customized topic through the group subscription page.  Two fields are added to the application configuration page that users can modify. Default use Neuron's topic. Users can customize the topic.

   ![Customize the topic](https://assets.emqx.com/images/dab03dba97ad733345c10cef2a871832.png)

The MQTT plugin will automatically handle data transmission to the specified custom write topic, providing a seamless integration experience.

## Bug Fixes 

There are also several bug fixes included in Neuron 2.4.5 release:

1. When installing version 2.4, the MQTT upload topic from version 2.3 is automatically upgraded to the data of 2.4.
2. Fix plugin parses tag address exceptions on arm32 devices. 
3. Fix the NON-A11 driver that causes all tags to report errors when the device is not responding. 
4. Fix the connection status is disconnected when the file plugin is not running.

## Summary

We're constantly working to improve [Neuron](https://neugates.io/) and provide our users with the most comprehensive set of features. Custom write topic support in the MQTT plugin is one of the many ways we aim to enhance your experience and meet your evolving needs. Upgrade to Neuron 2.4.5 today and we welcome your feedback and suggestions as we continue to shape the future of IIoT with Neuron. 



<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
