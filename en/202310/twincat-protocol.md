## What is TwinCAT

TwinCAT (The Windows Control and Automation Technology) is a software platform for automation technology developed by Beckhoff Automation. It is used to program and control various types of industrial automation equipment, such as programmable logic controllers (PLCs), motion control systems, human-machine interfaces (HMIs), and more.

TwinCAT is designed to be a modular and scalable platform, allowing it to be used in a wide range of applications and industries. It supports a variety of programming languages, including Structured Text (ST), Ladder Diagram (LD), Function Block Diagram (FBD), Sequential Function Chart (SFC), and C/C++.

## TwinCAT Milestones

TwinCAT was first introduced by Beckhoff Automation in 1995 as a software-only solution for industrial automation. The original version of TwinCAT was designed to run on standard Windows PCs, and it used a proprietary real-time expansion for Windows NT to achieve deterministic control.

Over the years, TwinCAT has evolved and expanded to include a wide range of automation capabilities, which included support for a wider range of programming languages and added features such as integrated motion control, CNC functionality, and support for real-time Ethernet protocols.

In 2011, Beckhoff introduced TwinCAT 3, which represented a major overhaul of the platform. TwinCAT 3 was based on a new software architecture that was designed to be more modular and scalable, allowing it to be used in a wider range of applications. TwinCAT 3 also added support for advanced features such as distributed control systems, multi-core processors, and advanced motion control. An essential feature was the integration with Microsoft Visual Studio which allowed users to take advantage of the rich set of development tools. With TwinCAT 3, the TwinCAT runtime is available for 64-bit operating systems, and the multi-core properties of the processors are optimally used.

## TwinCAT Architecture

Having a modular architecture designed for flexibility and scalability, the TwinCAT platform consists of several different software products that can be used together to create a complete automation solution. The basic system consists of engineering and runtime, which can be flexibly extended by application-specific software modules, known as Functions. Overall, the modular architecture provides a flexible and scalable platform for industrial automation, allowing users to tailor the system to their specific needs and requirements.

![TwinCAT Architecture](https://assets.emqx.com/images/9d03b7416e44820ea6ca9104dda35d68.png)

#### Engineering

TwinCAT XAE (eXtended Automation Engineering) is the development environment for TwinCAT 3, based on Microsoft Visual Studio. It provides a comprehensive set of tools for creating, debugging, and deploying automation programs, including support for a wide range of programming languages.

#### Runtime

TwinCAT XAR (eXtended Automation Runtime) is the core of the TwinCAT 3 system, responsible for executing PLC programs, coordinating motion control, and handling communication with other devices in the automation system. The Runtime can run on a variety of hardware platforms, from small embedded systems to large industrial PCs.

#### Functions

The TwinCAT Functions provide a wide range of extension options to the basic system. For example, [TwinCAT 3 HMI](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf2xxx-tc3-hmi/) enables the development of platform-independent user interfaces based on web technologies (HTML5, JavaScript/TypeScript), [TwinCAT 3 Vision](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf7xxx-tc3-vision/) offers scalable image processing, and [TwinCAT 3 Measurement](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf3xxx-tc3-measurement/) provides additional measurement technology functions.

## ADS Protocol

The ADS (Automation Device Specification) protocol is a transport layer within the TwinCAT system. It was developed for data exchange between the different components of an automation system, such as PLCs, HMIs, and other devices.

![Structure of the ADS communication](https://assets.emqx.com/images/7faa58eb3295d9504850cfc3e8ecdf16.png)

<center>Structure of the ADS communication</center>

<br>

The ADS protocol runs on top of the TCP/IP or UDP/IP protocols. The TCP port number for the ADS protocol is 48898.

ADS uses a client-server model for communication, where one device (the client) sends requests to another device (the server) and receives responses. The requests and responses include data, commands, or status information.

![image.png](https://assets.emqx.com/images/8f9f320789aa3a7ccc4d77c34ab35bf7.png)

<center>ADS packet structure</center>

<br>

The ADS protocol provides a set of [commands](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=) for communication between the server and the client, among which the most important are the [ADS Read](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=) and the [ADS Write](https://infosys.beckhoff.com/content/1033/tcadscommon/12440291467.html) commands.

## Why Bridge TwinCAT to MQTT

With the advent of Industry 4.0, there is an increasing demand for intelligence, automation and digitization in manufacturing. In this context, the MQTT protocol has obvious advantages over the ADS protocol.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a messaging protocol designed for IoT devices and applications operating on a publish/subscribe model. It's lightweight, efficient, reliable, and allows for real-time communication. MQTT is well-suited for environments with limited resources, where efficient use of power and bandwidth is necessary. Currently, it has been widely applied in areas such as the Internet of Things (IoT), mobile Internet, smart hardware, connected cars, smart cities, remote healthcare services, oil and energy.

Furthermore, MQTT is an open standard protocol and has many open-source implementations that can run on different platforms compared to the ADS protocol.

## Summary

In this article, we discuss the TwinCAT protocol and its significance in industrial scenarios. We also explain how bridging TwinCAT data to MQTT can enhance the efficiency of these scenarios. In our [next blog](https://www.emqx.com/en/blog/bridging-twincat-data-to-mqtt), we will provide a detailed guide on how to bridge these two protocols.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
