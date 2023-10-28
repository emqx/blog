## Introduction

In this post, we will provide an overview of [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) and explain what happens when a TCP client encounters address migration. We will then compare this with the behavior exhibited by the [QUIC protocol](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov). 

## MQTT over TCP: Challenges of Network Address Change  

When using MQTT over TCP, network address change refers to a situation where the client's IP address changes during an active connection. This can occur due to various reasons, such as a device moving between networks, switching from Wi-Fi to cellular data, or experiencing network disruptions. 

Network address change in TCP-based MQTT connections presents challenges and may result in connection drops and re-establishment. Address changes in client source addresses are particularly common in modern mobile networks. Mobile devices frequently switch between different network types, such as Wi-Fi, 4G, or 5G, as they move or encounter varying network conditions. 

This dynamic behavior adds an extra layer of complexity to MQTT over TCP connections. Additionally, address migration events can put an extra load on the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), making it difficult to plan hardware resources efficiently. Sudden bursts of reconnections due to address changes can strain the MQTT broker's capacity and affect its performance. Ensuring that the MQTT broker can handle a high volume of reconnection requests becomes a crucial consideration in such scenarios. Furthermore, from a development perspective, simulating client source address changes in a test environment is not a trivial task. It often requires specialized tools and configurations to mimic the dynamic nature of mobile networks accurately. This complexity makes it challenging for developers to thoroughly test the behavior and robustness of their MQTT applications in the face of the network address change.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

## MQTT over QUIC: A Better Solution to Address Change Scenarios

MQTT over QUIC provides a more efficient solution for tackling the obstacles of address change compared to MQTT over TCP. The QUIC protocol is designed to handle network changes seamlessly, providing enhanced resilience.

By leveraging QUIC transport, the following benefits can be observed: 

- **Address Migration Resilience**: QUIC enables clients to migrate their IP addresses seamlessly, minimizing disruptions in the MQTT connection. The burden of reconnection attempts and session re-establishment due to address changes is significantly reduced. 
- **Reduced Load on MQTT Broker**: The ability of MQTT over QUIC to handle address change more efficiently alleviates the load on the MQTT broker. The MQTT broker can better manage resource allocation and scaling plans, taking into account the reduced impact of sudden bursts of reconnections.
- **Development Simplicity**: MQTT over QUIC simplifies the development and testing process by providing built-in support for address migration. Developers can focus more on the application logic and functionality without worrying extensively about simulating address changes during testing. 

By adopting MQTT over QUIC, IoT applications can benefit from improved scalability, reduced load on the MQTT broker, and simplified development and testing processes in the presence of client source address changes. 

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
    <a href="https://www.emqx.com/en/resources/mqtt-over-quic-revolutionizing-iov-messaging-with-the-next-gen-standard-protocol?utm_campaign=embedded-mqtt-over-quic&from=blog-overcoming-address-change-with-mqtt-over-quic" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Demo:  Address/Connection Migration in MQTT over QUIC

In this chapter, we will walk you through a step-by-step demonstration of the client address migration feature in MQTT over QUIC. We will assume that you have a basic understanding of [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) and some familiarity with the concept of QUIC. 

Let's dive into the demo.

1. Set up the MQTT over QUIC environment.

   - Begin by provisioning the test cluster using the provided AWS CDK script available at [GitHub - emqx/cdk-emqx-cluster](https://github.com/emqx/cdk-emqx-cluster).

   - Follow the instructions in the repository to deploy the cluster in your AWS environment.

   - The cluster setup includes an EMQX MQTT broker, two load generators, and monitoring services.

   - The EMQX MQTT broker version used in this demo is open-source 5.0.26.

   - The load generators are configured to support the QUIC protocol using the emqtt-bench tool.

     ```
     CDK_EMQX_CLUSTERNAME=william cdk deploy CdkEmqxClusterStack  -c retain_efs=FALSE  -c emqx_n=1 -c lg_n=2 -c emqx_ins_type="m5.xlarge" -c loadgen_ins_type="m5.xlarge" --parameters sshkey=qzhuyan -c emqx_src="wget https://github.com/emqx/emqx/releases/download/v5.0.26/emqx-5.0.26-ubuntu20.04-amd64.deb"
     ```

     ```
     Outputs:
     CdkEmqxClusterStack.BastionBastionHostId8F8CEB82 = i-013c898310b5e2f41
     CdkEmqxClusterStack.ClusterName = william
     CdkEmqxClusterStack.EFSID = fs-006b96ed41efd7efd
     CdkEmqxClusterStack.ExportsOutputRefVPCEMQXwilliamA0A7F0C5ED461C91 = vpc-0bc7e7f3261e0ac59
     CdkEmqxClusterStack.ExportsOutputRefVPCEMQXwilliamPrivateSubnet1SubnetDAC171FE82109DBA = subnet-00967d6e2a803ca98
     CdkEmqxClusterStack.Hostsare = emqx-0.int.william
     etcd0.int.william
     etcd1.int.william
     etcd2.int.william
     loadgen-0.int.william
     loadgen-1.int.william
     CdkEmqxClusterStack.Loadbalancer = emqx-nlb-william-dd5d78ce97949e12.elb.eu-north-1.amazonaws.com
     CdkEmqxClusterStack.MonitoringGrafana = lb.int.william:3000
     CdkEmqxClusterStack.MonitoringPostgresPassword = william
     CdkEmqxClusterStack.MonitoringPrometheus = lb.int.william:9090
     CdkEmqxClusterStack.SSHCommandsforAccess = ssh -A -l ec2-user 16.16.202.211 -L 8888:lb.int.william:80 -L 13000:lb.int.william:3000 -L 19090:lb.int.william:9090 -L 15432:lb.int.william:5432 -L 28083:lb.int.william:8083 2>/dev/null
     CdkEmqxClusterStack.SSHEntrypoint = 16.16.202.211
     
     ```

2. Start the publishers.

   - On the host assigned to the publishers, open two separate terminals or command prompt windows.

   - In one terminal, start the publisher using TCP transport by running the appropriate command.

     This publisher will publish messages to the topic '/over/tcp', binding to the local address 192.168.0.200

     ```
     ./emqtt_bench pub -h emqx-0.int.william  -t '/over/tcp'  -c 1 --ifaddr 192.168.0.200 -q 1 --prefix PubTCP
     ```

   - In the other terminal, start the publisher using QUIC transport using the command.

     This publisher will publish messages to the topic '/over/quic', binding to the local address 192.168.0.200

     ```
     ./emqtt_bench pub -h emqx-0.int.william  -t '/over/quic' --quic -p 14567 -c 1 --ifadd r 192.168.0.200 -q 1 --prefix PubQUIC
     ```

     ![emqtt_bench](https://assets.emqx.com/images/1bc83f6640e3a5add93b7f6b0e8fc790.png)

3. Start the subscribers.

   - On the host assigned to the subscribers, open two separate terminals or command prompt windows.

   - In one terminal, start the subscriber for TCP by running the necessary script or command.

     This subscriber will subscribe to the topic '/over/tcp', QoS 1

     ```
     ./emqtt_bench sub -h emqx-0.int.william  -t '/over/tcp' -c 1  -q 1
     ```

   - In the other terminal, start the subscriber for QUIC using the appropriate script or command.

     - This subscriber will subscribe to the topic '/over/quic', QoS 1

       ```
       ./emqtt_bench sub -h emqx-0.int.william  -t '/over/quic  -c 1  -q 1
       ```

     - emqtt_bench prints the receiving message rate on the console.

       ![Receiving message rate](https://assets.emqx.com/images/7200a93022a6fe3d79ce0d7d190ffa4a.png)

4. Monitor message flow.

   - Observe the terminals for the subscribers and ensure that they start receiving messages from the respective topics.

   - Monitor the console output to view the receiving message rates for '/over/tcp' and '/over/quic'.

     ![View the receiving message rates](https://assets.emqx.com/images/f4c6b7756e7123726678ff006d169b25.png)

   - Monitor the EMQX console that the peer client src IP address is from 192.168.0.200.

     ```
     sudo tcpdump -i ens5 -n net 192.168.0.0/24
     ```

     ![tcpdump](https://assets.emqx.com/images/26a9607fc4c4834a9922e43f98f39b28.png)

5. Trigger the NAT rebinding.

   - Simulate the client source address change by triggering a NAT rebinding event that changes client src address from 192.168.0.200 to 192.168.0.203 for both TCP and UDP (QUIC) protocol.

     ```
     sudo iptables -t nat  -I POSTROUTING -s 192.168.0.200 -j SNAT --to-source 192.168.0.203
     sudo conntrack -F
     ```

   - Observe the behavior of the MQTT over QUIC connections as the address migration event occurs.

6. Validate the address migration.

   - Monitor the terminals for the subscribers and check that they continue to receive messages after the address migration.

     ![Monitor the terminals](https://assets.emqx.com/images/29c4c63ee29be0e80da7987850df2226.png)

   - Verify that the receiving message rates for  '/over/quic' topics are maintained without interruption.

     ![![image.png](https://assets.emqx.com/images/c537d7847c016b90bbc9ce998d5d4953.png)image.png](https://assets.emqx.com/images/8ca8eb35ba1c1fc00fb1f6e7cd519e1b.png)

   - Monitor the EMQX console that the peer client src IP address is from 192.168.0.203.

     ![Monitor the EMQX console](https://assets.emqx.com/images/5825a0c0fdf75bff2bae014dd0247d76.png)

7. Revert back to the old src address. This simulates the client switch back to the old network and get back the old source address.

   ```
   # EMQX
   sudo iptables -F -t nat
   ```

   ![iptables](https://assets.emqx.com/images/53a73f6a0a11fcdb463dd873ec34b971.png)

8. Tear down the test environment.

   Execute the following command in your terminal to tear down the test cluster:

   ```
   CDK_EMQX_CLUSTERNAME=william cdk destroy CdkEmqxClusterStack -c retain_efs=FALSE -cemqx_n=1 -c lg_n=2 -c emqx_ins_type="m5.xlarge" -c loadgen_ins_type="m5.xlarge" --parameters sshkey=qzhuyan -c emqx_src="wget https://github.com/emqx/emqx/releases/download/v5.0.26/emqx-5.0.26-ubuntu20.04-amd64.deb" 
   ```

By following these detailed steps in the demo, you can conduct a comprehensive demonstration of the client address migration feature in MQTT over QUIC. The test cluster provision ensures an environment suitable for testing the behavior of MQTT connections during address changes. Starting the publishers and subscribers allows you to observe the message flow and receiving message rates. Finally, triggering the NAT rebinding event simulates the client source address change, enabling you to validate the address/connection migration capabilities of MQTT over QUIC.

## Conclusion

In this blog post, we explored the client address migration feature in MQTT over QUIC and its benefits in handling address changes during active connections. We discussed the challenges faced by MQTT over TCP when encountering address migration, including connection drops and reestablishment, as well as the additional load on MQTT brokers. We also acknowledged the complexity of simulating address changes in testing environments.

MQTT over QUIC emerged as a powerful solution to address these challenges. By leveraging the capabilities of the QUIC protocol, MQTT over QUIC offers seamless address migration resilience, reduced load on MQTT brokers, and simplified development and testing processes. This protocol proves particularly valuable in modern mobile networks, where client source address changes are prevalent.

Through the step-by-step demonstration, we showcased the effectiveness of MQTT over QUIC in handling client address migration. By adopting MQTT over QUIC, developers and organizations can enhance the reliability, scalability, and overall performance of their MQTT-based systems. 

As IoT applications continue to evolve in dynamic network environments, MQTT over QUIC proves to be a valuable protocol choice with its ability to handle address migration seamlessly. With the effort of [EMQX](https://www.emqx.io/) as the first MQTT broker that supports MQTT over QUIC, we can expect further advancements in addressing network related challenges and enabling seamless communication in the ever-expanding world of IoT.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
