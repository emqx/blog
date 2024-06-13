> [EMQX](https://github.com/emqx/emqx) is a popular [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) widely used in the Internet of Things(IoT), Industrial IoT ([IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)) and Connected Cars. It can connect millions of devices at scale, move and process your IoT data in real-time anywhere with high performance, scalability and reliability.
>
> In this blog series, we will explore common troubleshooting scenarios when using EMQX and provide practical tips and solutions to overcome them. Readers can optimize your MQTT deployment and ensure smooth communication between your devices following this troubleshooting instruction.

## Introduction

EMQX supports many different deployment methods and can run anywhere in physical machines, containers/K8s, private clouds, hybrid clouds and public clouds (such as AWS), with no location restrictions and no vendor lock-in. 

This article will describe some common errors in deployment and their troubleshooting methods.

## System Dependencies

To ensure IoT data security and privacy, EMQX is based on [MQTT over TLS/SSL](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) to support encrypted data communication. Therefore, installing the correct version of OpenSSL is a necessary dependency for EMQX running on Linux system.

If the Linux system does not have the correct version of OpenSSL, this will affect the normal use of EMQX. If you have the following error logs upon starting EMQX with the command `./bin/emqx console`, it indicates that the system requires OpenSSL version 1.1.1. Otherwise, will resulting in the failure of EMQX start, because EMQX depends on the "crypto" application in Erlang/OTP.

```
{"init terminating in do_boot",{undef,[{crypto,start,[],[]},{init,start_em,1,[]},{init,do_boot,3,[]}]}}
init terminating in do_boot ({undef,[{crypto,start,[],[]},{init,start_em,1,[]},{init,do_boot,3,[]}]})

Crash dump is being written to: erl_crash.dump...done
FATAL: Unable to start Erlang.
Please make sure openssl-1.1.1 (libcrypto) and libncurses are installed.
```

To install OpenSSL 1.1.1, you can compile the source code and then place the shared object (so) file in a designated path that the system will recognize. Below is an example:

```
# under the latest version 1.1.1
wget https://www.openssl.org/source/openssl-1.1.1t.tar.gz

## Unpack and compile and install
tar -zxvf openssl-1.1.1t.tar.gz
cd openssl-1.1.1t
./config
make && make install

## View OpenSSL version
openssl version

## Make sure the library is referenced
ln -s /usr/local/lib64/libssl.so.1.1 /usr/lib64/libssl.so.1.1
ln -s /usr/local/lib64/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1
```

When installing EMQX on a CentOS 7 system using the RPM package, you will encounter a prompt for openssl11. This prompt is specific to this particular operating system.

```
--> Finished Dependency Resolution
Error: Package: emqx-ee-4.4.17-otp24.3.4.2_1.el7.x86_64 (/emqx-ee-4.4.17-otp24.3.4.2-1-el7-amd64)
           Requires: openssl11
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
```

You can install the missing dependencies using the yum command

```
yum install -y epel-release 

yum install -y openssl11 openssl11-devel
```

## Port Occupied By Another Service

Port occupation is a very common issue during the installation and deployment of EMQX. To ensure that EMQX starts and is used properly, it is important to avoid port hogging during installation and deployment. By default, EMQX will start on the following ports:

| **Port** | **Description**                  |
| :------- | :------------------------------- |
| 4370     | EMQX Cluster Node Discovery Port |
| 5370     | EMQX Cluster RPC Port            |
| 1883     | MQTT/TCP Protocol Port           |
| 8883     | MQTT/SSL Protocol Port           |
| 8081     | EMQX REST API Port               |
| 8083     | MQTT/WS Protocol Port            |
| 8084     | MQTT/WSS Protocol Port           |

When you run the EMQX startup command, you may not receive a successful startup log.

```
./bin/emqx start
```

In this case, you need to press CTRL + C to terminate the ongoing command and enter console mode. In console mode, you can find out some key logs.

```
./bin/emqx console
```

Here are some key logs that are printed for different occupied ports.

**4370 is occupied**

```
Protocol 'ekka': register/listen error: "port 4370 is in use"
```

**5370 is occupied**

```
[error] event=failed_to_setup_server driver=tcp reason="eaddrinuse"
[error] crasher: initial call: application_master:init/4, pid: <0.2275.0>, registered_name: [], exit: {{{shutdown,{failed_to_start_child,gen_rpc_server_tcp,eaddrinuse}}
```

**1883 is occupied**

```
[error] mqtt:tcp failed to listen on 1883 - eaddrinuse (address already in use)
```

**8883 is occupied**

```
[error] mqtt:ssl failed to listen on 8883 - eaddrinuse (address already in use)
```

**8083 is occupied**

```
[error] Failed to start Ranch listener 'mqtt:ws:8083' for reason eaddrinuse (address already in use)
```

**8084 is occupied**

```
[error] Failed to start Ranch listener 'mqtt:wss:8084' for reason eaddrinuse (address already in use)
```

To address the issue of ports being occupied and EMQX not starting correctly, you can use the `netstat` command. By executing this command, you can determine the specific program or process that is occupying the required port.

```
sudo netstat -tunlp |grep 8084   ## port eg:8084

tcp        0      0 0.0.0.0:8084            0.0.0.0:*               LISTEN      16429/python3
```

Here you can see that a Python program is occupying port 8084, causing EMQX to fail to start properly. You can use the `kill` command to stop this program or modify the listeners.conf configuration file of EMQX to change the default port from listener.wss.external to an unoccupied port eg:8085.

```
listener.wss.external = 8085
```

**8081 is occupied**

When the command /bin/emqx_ctl status fails to provide the running status of the EMQX and instead displays the help usage information of the emqx_ctl command, there are a few steps to follow for troubleshooting.

```
./bin/emqx_ctl status
Usage: emqx_ctl
--------------------------------------------------------------------------------------------------------------
admins add <Username> <Password> <Tags>                               # Add dashboard user
admins passwd <Username> <Password>                                   # Reset dashboard user password
admins del <Username>                                                 # Delete dashboard user
--------------------------------------------------------------------------------------------------------------
recon memory                                                          # recon_alloc:memory/2
recon allocated                                                       # recon_alloc:memory(allocated_types, current|max)
recon bin_leak                                                        # recon:bin_leak(100)
recon node_stats                                                      # recon:node_stats(10, 1000)
recon remote_load Mod                                                 # recon:remote_load(Mod)
recon proc_count Attr N                                               # recon:proc_count(Attr, N)
```

Firstly, you need to check the EMQX logs in the logs directory. By checking the error messages in logs, you can identify that the emqx_management plugin failed to start due to port 8081 being occupied.

```
[error] Minirest(Handler): Start http:management listener on 8081 unsuccessfully: the port is occupied
```

Secondly, use the netstat command to check which program is using port 8081. Then, use the `kill` command to terminate the program. Alternatively, you can modify the default port in the `etc/plugins/emqx_management.conf` file, e.g., to 8082.

```
management.listener.http = 8082
```

## Incorrect Node Name

> **Note:** Node name format is `Name@Host`, Host must be IP address or FQDN (host name or domain name)

When deploying EMQX, another common issue that may arise is the utilization of an incorrect node name, resulting in improper functionality. 

Upon running the EMQX startup command, you do not receive a successful startup message prompt. If you start EMQX in console mode, you may observe that port 4370 is occupied, and using the netstat command reveals that the EMQX program is listening on the corresponding port.

![EMQX Port](https://assets.emqx.com/images/5dee48f650a54f19c37f50461c8dbafb.png)

Use the `emqx_ctl` command to inspect the EMQX status, and you will find that `emqx@192.168.64.10` is not started. 

```
ubuntu@emqx:~/emqx$ ./bin/emqx_ctl status
Node 'emqx@192.168.64.10' not responding to pings.
ERROR: node_is_not_running!
```

To troubleshoot this, you can use the `ifconfig` command to check the local IP and make sure that the EMQX node name is correctly filled in.

![ifconfig command](https://assets.emqx.com/images/642e8909b0b3ee4fbfe34490af8d817b.png)

In this case, it is discovered that the local IP is `192.168.64.9` instead of `192.168.64.10`, leading to startup issues due to the incorrectly filled node name. To resolve this problem, it is necessary to modify the node name to `emqx@192.168.64.9` and then restart EMQX.

## Data Residue

When transitioning from version 4 to version 5 of EMQX, it is important to note the big differences between the two. You need to thoroughly remove any residual data to avoid any disruptions in the proper use of EMQX.

If you have previously deployed version 5 on a machine using the deb or rpm package and subsequently uninstalled version 4, make sure that you use the appropriate uninstallation command. This guarantees the complete removal of the data associated with the installed version, as any remnants left behind can impact the normal functioning of EMQX.

To completely uninstall EMQX v5 or EMQX v4, you can use the following command.

```
## deb package

# uninstall v5 emqx-enterprise
# stop emqx service 
sudo systemctl stop emqx

# can use dpkg or apt command uninstall
sudo dpkg --purge emqx-enterprise
sudo apt --purge remove emqx-enterprise

# uninstall v4 emqx-enterprise
# stop emqx service 
sudo systemctl stop emqx

# can use dpkg or apt command uninstall
sudo dpkg --purge emqx-ee
sudo apt --purge remove emqx-ee -y

## rpm package

# uninstall v5 emqx-enterprise
# stop emqx service 
sudo systemctl stop emqx

# can use rpm or yum command uninstall

sudo rpm -e --nodeps emqx-enterprise

sudo yum remove emqx-enterprise -y

sudo find / -name "emqx*" -exec rm -rf {} \;

# uninstall v4 emqx-enterprise
# stop emqx service 
sudo systemctl stop emqx

# can use rpm or yum command uninstall

sudo rpm -e --nodeps emqx-ee

sudo yum remove emqx-ee -y

sudo find / -name "emqx*" -exec rm -rf {} \;
```

You should always execute the find command during the uninstallation process to make sure completely remove any remaining files related to the previous EMQX version. Failing to do so may result in a similar situation as described earlier, where EMQX fails to work properly.

```
sudo find / -name "emqx*"
```

## Unable to Boot Up

When installing EMQX with rpm and deb packages, you can use the systemctl command to manage the start, stop, and boot settings of EMQX. However, EMQX installations via the zip package do not come pre-configured and will not automatically start upon Linux machine reboot. For zip package deployments, it is necessary to configure the service file appropriately to enable boot configuration for EMQX.

```
[Unit]
Description=emqx daemon
After=network.target

[Service]
Type=forking
Environment=HOME=/opt/emqx

# Must use a 'bash' wrap for some OS
# errno=13 'Permission denied'
# Cannot create FIFO ... for writing
ExecStart=/opt/emqx/bin/emqx start

LimitNOFILE=1048576
ExecStop=/opt/emqx/bin/emqx stop
Restart=on-failure

# When clustered, give the peers enough time to get this node's 'DOWN' event
RestartSec=60s

[Install]
WantedBy=multi-user.target
```

Then you can set EMQX to boot using the `systemctl` command.

```
systemctl daemon-reload
systemctl enable emqx
systemctl start emqx
```

## Data Loss

Data loss is the most common problem with Kubernetes-based deployments of EMQX. If a Kubernetes cluster goes down and the EMQX Pod is rebuilt, all the configurations within EMQX will be lost.

To mitigate this issue, deploying [EMQX in Kubernetes](https://docs.emqx.com/en/emqx-operator/latest/) should incorporate data persistence configurations. For efficient creation and management of EMQX clusters in a Kubernetes environment, it is highly recommended to utilize the EMQX Operator.It dramatically simplifies deploying and managing EMQX clusters and requires less administration and configuration knowledge. It turns the work of deployment and management into a low-cost, standardized, and repeatable capability.

![EMQX in Kubernetes](https://assets.emqx.com/images/110f2bd760354c89a068232a2586887d.png)

To demonstrate the deployment of an EMQX cluster using AWS Cloud EKS, the following code block shows the relevant configurations for EMQX custom resources. You can choose the appropriate APIVersion based on the EMQX version you want to deploy. Please consult the EMQX and [EMQX Operator](https://www.emqx.com/en/emqx-kubernetes-operator) compatibility list for specific compatibility information.

```
apiVersion: apps.emqx.io/v1beta4
kind: EmqxEnterprise
metadata:
  name: emqx-ee
spec:
  ## EMQX custom resources do not support updating this field at runtime
  persistent:
    metadata:
      name: emqx-ee
    spec:
      ## More content: https://docs.aws.amazon.com/eks/latest/userguide/storage-classes.html
      ## Please manage the Amazon EBS CSI driver as an Amazon EKS add-on.
      ## For more documentation please refer to: https://docs.aws.amazon.com/zh_cn/eks/latest/userguide/managing-ebs-csi.html
      storageClassName: gp2
      resources:
        requests:
          storage: 10Gi
      accessModes:
        - ReadWriteOnce
  template:
    spec:
      ## If persistence is enabled, you need to configure podSecurityContext.
      ## For details, please refer to the discussion: https://github.com/emqx/emqx-operator/discussions/716
      podSecurityContext:
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        fsGroupChangePolicy: Always
        supplementalGroups:
          - 1000
      emqxContainer:
        image:
          repository: emqx/emqx-ee:4.4.18
          version: 4.4.18
  serviceTemplate:
    metadata:
      ## More content: https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/
      annotations:
        ## Specifies whether the NLB is Internet-facing or internal. If not specified, defaults to internal.
        service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
        ## Specify the availability zone to which the NLB will route traffic. Specify at least one subnet, either subnetID or subnetName (subnet name label) can be used.
        service.beta.kubernetes.io/aws-load-balancer-subnets: subnet-xxx1,subnet-xxx2
        ## Specifies the ARN of one or more certificates managed by the AWS Certificate Manager.
        service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-west-2:xxxxx:certificate/xxxxxxx
        ## Specifies whether to use TLS for the backend traffic between the load balancer and the kubernetes pods.
        service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
        ## Specifies a frontend port with a TLS listener. This means that accessing port 1883 through AWS NLB service requires TLS authentication,
        ## but direct access to K8S service port does not require TLS authentication
        service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "1883"

    spec:
      type: LoadBalancer
      ## More content: https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/nlb/
      loadBalancerClass: service.k8s.aws/nlb
```

Using the EMQX Operator on Kubernetes significantly reduces the YAML configuration complexity. To achieve data persistence in the EMQX cluster, you only need to configure storageClassName: gp2. This simplifies the process, reduces the likelihood of data configuration errors, and enhances the data persistence of the EMQX cluster on Kubernetes. Additionally, it improves the high availability of deployed EMQX clusters on Kubernetes.

## Summary

As a powerful [MQTT messaging platform](https://www.emqx.com/en/products/emqx), EMQX enables different deployment methods catering to various business needs. This troubleshooting guide empowers you to carefully review your deployment process and guarantee the stability and reliability of EMQX. By following this guide, you can address any issues that may arise and optimize the performance of your EMQX deployment.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
