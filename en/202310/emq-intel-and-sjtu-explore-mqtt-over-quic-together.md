[MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) is emerging as the next-generation standard for IoT and IoV protocols due to its advantageous features like multiplexing and accelerated connection establishment and migration. EMQ leads the way in implementing MQTT over QUIC within its product, aiming to deliver enhanced performance and stable connectivity across diverse industries. This solution is particularly well-suited for addressing the data transmission challenges posed by unreliable network conditions.

MQTT over QUIC introduces [QUIC (Quick UDP Internet Connections)](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) as a replacement for the TCP-based transport layer in the conventional [MQTT protocol](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt). Unlike TCP, QUIC is based on UDP (User Datagram Protocol), which is better suited for handling communication in unreliable network environments. This transition offers several benefits, including reduced latency, shorter handshake durations, and the ability to multiplex.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/129d83b2aebdc64d6c1385236677b310.png" alt="MQTT over QUIC" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      Next-Gen Standard Protocol for IoV
    </div>
    <div class="mb-32">
      Revolutionizing IoV messaging with MQTT over QUIC.
    </div>
    <a href="https://www.emqx.com/en/resources/mqtt-over-quic-revolutionizing-iov-messaging-with-the-next-gen-standard-protocol?utm_campaign=embedded-mqtt-over-quic&from=blog-emq-intel-and-sjtu-explore-mqtt-over-quic-together" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

During the summer of 2023, EMQ partnered with Intel and Shanghai Jiao Tong University to introduce a specialized short course. This program aimed to offer comprehensive insights and practical experience regarding the MQTT over QUIC protocol to students both in China and international universities. We simulated typical IoV scenarios characterized by unreliable network conditions, allowing universities to conceptualize and conduct experiments utilizing MQTT over QUIC. We employed the Intel-developed AIxBoard Developer kit and EMQ's IoT data software to guide participants through the entire project.

## Case Study on MQTT over QUIC from Universities

### 1. Performance Evaluation of MQTT over QUIC in the Weak Network Environment

#### Experiment 1:

Dmytro Fedoryshyn, from Kharkiv National University of Radio Electronics in Ukraine, conducted a performance evaluation on an AWS c7g.xlarge (4vCPU/8Gi) instance using EMQX 5.0 and the emqtt_bench tool. The study involved a performance comparison between MQTT over QUIC and MQTT over TCP. 

**Approach:** Dmytro Fedoryshyn introduced random packet loss to simulate an actual weak network environment. The outcomes reveal that MQTT over QUIC maintains a remarkable level of stability in the face of network fluctuations. The figure below illustrates the results of the performance evaluation.

![Benchmark results](https://assets.emqx.com/images/4cc5115e125c79a4c443269431c00d56.png)

![MQTT over TCP vs MQTT over QUIC](https://assets.emqx.com/images/26e14ffb738c5f934d572f4f2c3b8b28.png)

**Findings:** While conducting a benchmark, we managed to explore the key advantage of MQTT over QUIC over standard MQTT over TCP data transfer protocol – its ability to remain stable and work efficiently even using a weak Internet connection. It is a very important breakthrough in the world of IoV, as a lot of connected vehicle users usually face similar problems: vehicles may run in mountainous areas, mines, tunnels, etc., which can cause connection interruptions. Frequent connection interruptions and slow connection establishment can lead to poor user experience, and MQTT over QUIC is a perfect way to mitigate this problem.

#### Experiment 2:

Eleonora Scognamiglio, from the University of Toronto in Canada, and Thomas Nguyen, from the University of Warwick in the U.K., have collaborated to create a series of validation protocols. These schemes are aimed at examining the performance distinctions between MQTT over QUIC and MQTT over TCP across various network conditions.

**Approach:** Eleonora Scognamiglio and Thomas Nguyen employed varying percentages of random packet loss strategies in their research to investigate the performance disparities between MQTT over QUIC and MQTT over TCP across diverse network scenarios. Their findings conclusively demonstrated that MQTT over QUIC exhibits significant performance advantages in a range of weak network conditions.

![Results](https://assets.emqx.com/images/146d7093fc8fd19b67b7828bd95dce2c.png)

**Findings:** The graph above summarizes our findings, including the maximum packet transmission rate reached by the two protocols under different connection conditions. From the above testing and benchmarking with 4 network conditions: 0%, 25%, 50%, 75%, it can be seen that two protocols MQTT over QUIC and MQTT over TCP perform similarly given the network condition is ideal; however, as the packets dropping rate increases, the performance of MQTT over QUIC appears to outweigh its counterpart. Therefore, we can conclude that the speed and stability of MQTT over QUIC are better overall, especially under weak network conditions.

### 2. MQTT over QUIC Bridging Solution

In the MQTT over QUIC bridging technology topic, Fengping Sun from Shanghai Jiaotong University and Phoebe Chuang from the University of Toronto, Canada, utilized EMQ's [NanoMQ](https://nanomq.io) bridging capabilities. They employed Intel's AIxBoard to replicate IoT and IoV scenarios, effectively transmitting sensor data to the server via MQTT over QUIC. This successful experiment validated the practicality of this technology in real-world applications.

**Approach:** In this topic, Fengping Sun and Phoebe Chuang employed the Intel AIxBoard development board to replicate a vehicle environment. They utilized an MQTT publisher to transmit simulated data to NanoMQ deployed within the vehicle using the MQTT over TCP protocol. NanoMQ plays a crucial role in mapping MQTT connections to QUIC streams and subsequently uploading the data to the EMQX cluster located in the cloud. This approach offers the notable advantage of not necessitating any client modifications or adaptations, all the while fully harnessing the benefits of MQTT over QUIC.

![screenshot1](https://assets.emqx.com/images/07bf6c7e7ec70e26d11ba8863755c3c0.png)

![screenshot2](https://assets.emqx.com/images/902714cd001f2b438a38d47d1b1d7930.png)

![screenshot3](https://assets.emqx.com/images/c5d3eb9cf1a66959e1bd903039c360e2.png)

![screenshot4](https://assets.emqx.com/images/de646c18976d2c01a9cd6878bbd323bc.png)

**Findings:** In a stable network environment, MQTT over QUIC performs comparably to MQTT over TCP. However, in the presence of network instability, MQTT over QUIC demonstrates a notable advantage. While MQTT over TCP experiences fluctuating transmission rates ranging from 3 to 300 packets per second, MQTT over QUIC maintains a stable throughput of 260 to 280 packets per second.

## Course Support

### EMQ

EMQ is the world's leading software provider of open-source IoT data infrastructure. The core product portfolio used in this course consists of [EMQX](https://www.emqx.io/), the world’s most scalable and reliable open-source MQTT messaging platform, available in both open-source and commercial versions, and [NanoMQ](https://nanomq.io), an ultra-lightweight MQTT middleware that can run at the edge. They offer a one-stop, cloud-native solution that can connect, move, process, and integrate real-time IoT data from edge to cloud to multi-cloud.

Founded in 2017, EMQ has rapidly grown. Its flagship product, EMQX, has served over 500 enterprise users in more than 50 countries, connecting to a staggering 250 million IoT devices globally.

### Intel

The Intel AIxBoard Developer Kit, which students use in this course, is specifically designed to support entry-level edge AI applications and devices. It caters to various application scenarios such as AI learning, development, and hands-on training. This board resembles a Raspberry Pi in terms of its x86 host architecture, and it offers compatibility with both Linux Ubuntu and full Windows operating systems. Equipped with an Intel 4-core processor running at a maximum frequency of 2.9 GHz, it also features integrated core graphics (iGPU), 64GB of eMMC storage, and LPDDR4x memory running at 2933MHz (available in 4GB, 6GB, or 8GB configurations). Moreover, this board comes with built-in Bluetooth and Wi-Fi modules, as well as support for USB 3.0, HDMI video output, a 3.5mm audio interface, and a 1000Mbps Ethernet port. Its versatility enables it to function as a mini-computer and seamlessly connect to Arduino, STM32, and other microcontrollers to expand its range of applications and integrate various sensor modules.

Intel has left a lasting imprint on the world for over five decades, spearheading transformative innovations that have reshaped both business and society, fundamentally altering the way we lead our lives. In the present day, Intel leverages its considerable influence, expansive scale, and abundant resources to empower businesses across diverse sectors to wholeheartedly embrace the era of digital transformation.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
