## 引言

本文将向您简要介绍 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic)，并分析在 TCP 客户端地址发生变化时会遇到什么挑战。然后，我们将深入探讨 [QUIC 协议](https://www.emqx.com/zh/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov)如何应对这些挑战。

## MQTT over TCP：网络地址变化带来的挑战

在使用 MQTT over TCP 时，网络地址变化是指客户端的 IP 地址和/或端口在活动连接期间发生改变。造成这种情况的原因有很多，比如设备在不同的网络之间切换、从 Wi-Fi 转到蜂窝移动网络或遭遇网络故障。

当网络地址发生变化时，会影响基于 TCP 的 MQTT 连接，可能导致连接中断和重新连接。在现代移动网络中，客户端源地址的变化非常普遍。移动设备经常在不同的网络环境中移动或切换，这意味着它们会频繁在不同类型的网络之间进行转换，例如 Wi-Fi、4G 或 5G。

网络地址变化给 MQTT over TCP 连接增加了更多的复杂性。此外，地址迁移事件给 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 带来了额外的负担，使其难以有效地分配硬件资源。地址变化引起的大量重连会消耗 MQTT Broker 的容量并降低其性能。在这种情况下，确保 MQTT Broker 能够处理大量重连请求成为必须考虑的重要因素。另外，从开发的角度来看，在测试环境中模拟客户端源地址的变化也并非易事，通常需要专门的工具和配置来准确模拟移动网络的动态特性。这种复杂性使得开发人员在面对网络地址变化时难以全面测试其 MQTT 应用的行为和健壮性。

## MQTT over QUIC：应对地址变化场景的优选解决方案

MQTT over QUIC 比 MQTT over TCP 能更有效地解决地址变化的问题。QUIC 协议能够无缝地应对网络变化，提供更强的韧性。

利用 QUIC 传输的优势有：

- **地址迁移更具弹性：**QUIC 让客户端可以无缝地改变 IP 地址，将 MQTT 连接中断风险降至最低。由地址变化导致的重新连接和会话重建的负担大大降低。
- **减轻 MQTT Broker 的压力：**MQTT over QUIC 能够有效地应对地址变化，减轻了 MQTT Broker 的负担。MQTT Broker 可以更好地分配资源和扩展服务，并减少因大量突发的重新连接对性能造成的影响。
- **开发更便捷：**MQTT over QUIC 通过内置的地址迁移支持，简化了开发和测试过程。开发人员可以更关注应用的逻辑和功能，而不必花费大量时间在模拟地址变化的测试上。

通过采用 MQTT over QUIC，物联网应用可以提高扩展性，降低 MQTT Broker 的压力，并简化客户端源地址变化场景下的开发和测试过程。

## Demo：MQTT over QUIC 的地址/连接迁移功能

本节将向您展示如何在 MQTT over QUIC 中使用客户端地址迁移功能。我们假设您已经对 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 有基本的认识，并对 QUIC 的概念有一定的了解。

具体步骤如下：

1. 准备 MQTT over QUIC 环境。

   - 通过 [GitHub - emqx/cdk-emqx-cluster](https://github.com/emqx/cdk-emqx-cluster) 提供的 AWS CDK 脚本，快速搭建测试集群。

   - 按照资源库中的说明，在 AWS 环境中部署集群。

   - 集群包含一个 EMQX MQTT Broker、两个负载生成器和若干监控服务。

   - 本演示使用的 EMQX MQTT Broker 是开源的 5.0.26 版本。

   - 利用 emqtt-bench 工具，将负载生成器配置为支持 QUIC 协议。

     ```
     CDK_EMQX_CLUSTERNAME=william cdk deploy CdkEmqxClusterStack  -c retain_efs=FALSE  -c emqx_n=1 -c lg_n=2 -c emqx_ins_type="m5.xlarge" -c loadgen_ins_type="m5.xlarge" --parameters sshkey=qzhuyan -c emqx_src="wget https://github.com/emqx/emqx/releases/download/v5.0.26/emqx-5.0.26-ubuntu20.04-amd64.deb"
     ```

     ````
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
     ````

2. 启动发布者。

   - 在发布者所在的主机上，分别打开两个终端或命令提示符窗口。

   - 在其中一个终端运行以下命令，使用 TCP 传输方式启动发布者。

     该发布者将向主题 `/over/tcp` 发送消息，并绑定本地地址 192.168.0.200

     ```
     ./emqtt_bench pub -h emqx-0.int.william  -t '/over/tcp'  -c 1 --ifaddr 192.168.0.200 -q 1 --prefix PubTCP
     ```

   - 在另一个终端运行以下命令，使用 QUIC 传输方式启动发布者。

     该发布者将向主题 `/over/quic` 发送消息，并绑定本地地址 192.168.0.200

     ```
     ./emqtt_bench pub -h emqx-0.int.william  -t '/over/quic' --quic -p 14567 -c 1 --ifadd r 192.168.0.200 -q 1 --prefix PubQUIC
     
     ```

     ![emqtt_bench](https://assets.emqx.com/images/1bc83f6640e3a5add93b7f6b0e8fc790.png)

3. 启动订阅者。

   - 在订阅者所在的主机上，分别打开两个终端或命令提示符窗口。

   - 在其中一个终端运行相应脚本或命令，使用 TCP 方式启动订阅者。

     该订阅者将订阅主题 `/over/tcp`，QoS 1

     ```
     ./emqtt_bench sub -h emqx-0.int.william  -t '/over/tcp' -c 1  -q 1
     ```

   - 在另一个终端运行相应脚本或命令，使用 QUIC 方式启动订阅者。

     - 该订阅者将订阅主题 `/over/quic`，QoS 1

       ```
       ./emqtt_bench sub -h emqx-0.int.william  -t '/over/quic  -c 1  -q 1
       ```

     - emqtt_bench 会在控制台上显示接收消息的速率。

       ![Receiving message rate](https://assets.emqx.com/images/7200a93022a6fe3d79ce0d7d190ffa4a.png)

4. 监控消息流。

   - 观察订阅者的终端，确保它们能够从相应的主题收到消息。

   - 监控控制台输出，查看 `/over/tcp` 和 `/over/quic` 的消息接收速率。

     ![View the receiving message rates](https://assets.emqx.com/images/f4c6b7756e7123726678ff006d169b25.png)

   - 监控 EMQX 控制台，确认对方客户端的源 IP 地址为 192.168.0.200。

     ```
     sudo tcpdump -i ens5 -n net 192.168.0.0/24
     ```

     ![tcpdump](https://assets.emqx.com/images/26a9607fc4c4834a9922e43f98f39b28.png)

5. 触发 NAT 重绑定。

   - 通过触发 NAT 重绑定事件，模拟客户端源地址变化，将 TCP 和 UDP (QUIC) 协议的客户端源地址从 192.168.0.200 变为 192.168.0.203。

     ```
     sudo iptables -t nat  -I POSTROUTING -s 192.168.0.200 -j SNAT --to-source 192.168.0.203
     sudo conntrack -F
     ```

   - 在地址迁移事件发生时，观察 MQTT over QUIC 连接的变化。

6. 验证地址迁移效果。

   - 监控订阅者的终端，检查它们在地址迁移之后是否仍然能够收到消息。

     ![Monitor the terminals](https://assets.emqx.com/images/29c4c63ee29be0e80da7987850df2226.png)

   - 验证 `/over/quic` 主题的消息接收速率没有被中断。

     ![![image.png](https://assets.emqx.com/images/c537d7847c016b90bbc9ce998d5d4953.png)image.png](https://assets.emqx.com/images/8ca8eb35ba1c1fc00fb1f6e7cd519e1b.png)

   - 监控 EMQX 控制台，确认对方客户端的源 IP 地址变为 192.168.0.203。

     ![Monitor the EMQX console](https://assets.emqx.com/images/5825a0c0fdf75bff2bae014dd0247d76.png)

7. 恢复旧的源地址。这模拟了客户端重新连接旧的网络并获得旧的源地址。

   ```
   # EMQX
   sudo iptables -F -t nat
   ```

   ![iptables](https://assets.emqx.com/images/53a73f6a0a11fcdb463dd873ec34b971.png)

8. 清理测试环境。

   在终端中执行以下命令，清理测试集群：

   ```
   CDK_EMQX_CLUSTERNAME=william cdk destroy CdkEmqxClusterStack -c retain_efs=FALSE -cemqx_n=1 -c lg_n=2 -c emqx_ins_type="m5.xlarge" -c loadgen_ins_type="m5.xlarge" --parameters sshkey=qzhuyan -c emqx_src="wget https://github.com/emqx/emqx/releases/download/v5.0.26/emqx-5.0.26-ubuntu20.04-amd64.deb"
   ```

按照演示中这些详细的步骤进行操作，您可以完整实现 MQTT over QUIC 的客户端地址迁移功能。通过构建测试集群，确保创建了一个合适的测试环境，以便测试 MQTT 连接在地址变化时的行为。启动发布者和订阅者，您将能够观察消息流和消息接收速率。最后，触发 NAT 重绑定事件，模拟客户端源地址的变化，从而验证 MQTT over QUIC 的地址/连接迁移能力。

## 结语

在本文中，我们深入探讨了 MQTT over QUIC 的客户端地址迁移特性，并介绍了它在活动连接期间地址发生变化的场景下所具有的优势。我们还详细讨论了 MQTT over TCP 在遇到地址迁移时所面临的挑战，包括连接断开和重新建立，以及给 MQTT Broker 带来了额外负载。同时，我们也认识到在测试环境中模拟地址变化的复杂性。

MQTT over QUIC 作为一种强大的解决方案，成功地克服了这些挑战。通过利用 QUIC 协议的特性，MQTT over QUIC 实现了无缝的地址迁移能力，减轻了 MQTT Broker 的负载，并简化了开发和测试流程。这种协议在现代移动网络中尤其有价值，因为客户端源地址的变化非常常见。

通过逐步演示，我们展示了 MQTT over QUIC 在处理客户端地址迁移方面的高效性。通过使用 MQTT over QUIC，开发者和组织能够显著提升基于 MQTT 的系统的可靠性、可扩展性和整体性能。

随着物联网应用在动态网络环境中不断发展，MQTT over QUIC 凭借其无缝处理地址迁移的能力，成为一种极具价值的协议选择。作为首个支持 MQTT over QUIC 的 MQTT Broker，[EMQX](https://www.emqx.io/) 将致力于 QUIC 协议的标准化与普及。我们将有望利用 QUIC 协议解决更多网络相关问题，并在不断扩展的物联网世界中实现无缝通信。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
