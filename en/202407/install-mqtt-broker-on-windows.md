## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol that operates on a publish/subscribe model. It's designed to deliver messages reliably and efficiently for IoT devices with minimal code and bandwidth requirements. Over the years, MQTT has become extensively utilized across various sectors, including resource extraction, industrial production, mobile communications, and connected vehicles, establishing itself as the de facto standard for IoT communication protocols.

Many MQTT service implementations favor the Linux environment due to its stability, reliability, and cost-effectiveness, alongside a comprehensive open-source ecosystem. However, the availability of MQTT services on Windows is comparatively limited. [NanoMQ](https://nanomq.io/), an ultra-lightweight MQTT message broker tailored for IoT edge computing, offers exceptional performance and cost-effectiveness, suitable for a wide range of edge computing platforms. With robust cross-platform capabilities, NanoMQ is applicable to both Linux and Windows systems, providing a novel alternative for MQTT services on Windows.

This guide will walk you through setting up MQTT services on Windows using NanoMQ, demonstrating both binary package installation and source code compilation methods.

## An Overview of NanoMQ

[NanoMQ](https://github.com/nanomq/nanomq), an open-source initiative launched by EMQ in 2021, aims to provide a lightweight, swift, and multi-threaded MQTT message server and bus for IoT edge scenarios. Constructed atop NNG’s asynchronous I/O, NanoMQ integrates an Actor multi-threaded model. In contrast to Mosquitto’s single-threaded approach, NanoMQ leverages the multi-core benefits of modern SMP systems, delivering performance up to tenfold greater than Mosquitto in a multi-core environment at the edge. Developed with standard POSIX interfaces, NanoMQ can be effortlessly ported to various Windows environments via MinGW’s POSIX compilation environment. 

![NanoMQ](https://assets.emqx.com/images/a46cf404d1c67d2e10c4e782f9278b3c.png)

After three years of development, NanoMQ joined the LF Edge Foundation in January 2024, with plans to integrate deeply with the EdgeX Foundry framework under LF Edge, enhancing interoperability among IoT edge devices and applications.

Key features of NanoMQ include:

- **Ultra-lightweight**: The installer is approximately 350KB, requiring minimal operational resources. Depending on the build and startup configurations, memory requirements range from 300Kb to 3Mb.
- **Compatibility and Portability**: Developed in pure C/C++, NanoMQ relies solely on standard POSIX APIs and supports endian compatibility. It seamlessly integrates with various network applications and enables cost-free migration to diverse embedded platforms.
- **Scalability**: Despite its lightweight nature, NanoMQ’s built-in asynchronous I/O architecture and multi-threaded model afford a degree of scalable concurrent throughput. It can support over 100,000 message transactions with less than 10MB of memory usage(fan-out).
- **SMP Support**: NanoMQ provides robust support for SMP on multi-core platforms at the edge, maximizing multi-processor capabilities to boost system performance.
- **Container Support**: NanoMQ can be deployed and run easily through containers. It is compatible with mainstream edge container solutions, streamlining the deployment process.

## Installing via Binary Package

Begin by visiting the NanoMQ official [download page](https://nanomq.io/downloads) and selecting the Windows platform to download the installer.

![Download NanoMQ](https://assets.emqx.com/images/7a3222838b7a4f5c2fe3a0871db5100e.png)

After unzipping, you can access NanoMQ via the Windows command line from the bin directory in the unzipped folder. Adding the directory `C:\xxx\nanomq-0.21.10-windows-x86_64\bin` to your environment variables allows you to use NanoMQ directly from the Windows command line or PowerShell. Typing `nanomq --help` displays a concise usage guide.

![nanomq --help](https://assets.emqx.com/images/f9538da8b2a2a9a651715165d37c1259.png)

Launch NanoMQ with `nanomq start --conf C:\nanomq\config\nanomq.conf`. The path C:\nanomq\config\nanomq.conf specifies the NanoMQ configuration file location, with sample configurations available in the config directory of the unzipped folder. For comprehensive configuration details, consult the official documentation.

Next, explore NanoMQ’s functionality using the MQTT client tool nanomq_cli, which is located in the bin directory.

![image.png](https://assets.emqx.com/images/ff30f04d2dd96558d9dde7870daf52eb.png)

As illustrated, nanomq_cli subscribes to the topic `nmqtest`with the `sub` command and receives the HelloWorld message published by nanomq_cli using the `pub` command.

## Source Code Compilation and Execution

For compilation on Windows, please prepare [MinGW-w64](https://www.mingw-w64.org/), [Make](https://gnuwin32.sourceforge.net/packages/make.htm), and [CMake](https://cmake.org/) beforehand.

- **MinGW-w64** ports the GCC compiler and GNU Binutils to Windows, encompassing headers (Win32API), libraries, and executables, serving as an open-source environment for developing and running native Windows applications. Cygwin, akin to MinGW, ports Unix software to Windows but differs in implementation. Cygwin prioritizes compatibility over performance, whereas MinGW emphasizes simplicity and efficiency. This guide uses MinGW for compiling NanoMQ.
- **Make and CMake** facilitate the NanoMQ project’s automated build process. Refer to the download links: [MingGW-w64](https://www.mingw-w64.org/downloads/#mingw-builds), [Make](https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=jaist&download=), [CMake](https://cmake.org/download/). Opt for a recent MinGW-w64 version.

Then, execute the following commands in the Windows command line, PowerShell, or Git Bash:

```powershell
# 1. Clone the source code (skip if you've downloaded the source code via ZIP)
PS: D:\Project> git clone https://github.com/nanomq/nanomq.git
PS: D:\Project> cd nanomq

# 2. Update and initialize git submodules
PS: D:\Project\nanomq> git submodule update --init --recursive

# 3. Create and navigate to the build directory
PS: D:\Project\nanomq> mkdir build
PS: D:\Project\nanomq> cd build

# 4. Compile NanoMQ
PS: D:\Project\nanomq\build> cmake -G "MinGW Makefiles" ..
PS: D:\Project\nanomq\build> make -j 8

# 5. Run NanoMQ
PS: D:\Project\nanomq\build> .\nanomq\nanomq.exe broker start
```

Beyond NanoMQ’s proprietary client tool, the open-source [MQTT client MQTTX](https://mqttx.app/) can be utilized for testing message transmission and reception.

The figure also demonstrates that the client subscribed to the nmqtest topic receives the hello message sent by another client via NanoMQ.

![MQTTX](https://assets.emqx.com/images/9151df62b218245b893ac35335328943.png)

## Conclusion

This guide detailed the installation of NanoMQ on Windows through binary packages and source code compilation, showcasing its practical application. NanoMQ offers a convenient and potent solution for constructing IoT edge computing applications on Windows. Its lightweight design, superior performance, and edge computing focus render it an exemplary message transport solution.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
