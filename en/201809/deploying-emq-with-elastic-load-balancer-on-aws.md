![](https://cdn-images-1.medium.com/max/2000/1*Cdso0oYkWsJgPGtNf2yuFw.jpeg)

Besides the benefit of multiplied service capacity, we also deploy emqtt in a
cluster to achieve high availability (HA). Even when the traffic load is very
low, an emqtt cluster is still advisable, for it is fault-tolerant. The service
continues when a single node is failed.

The general cluster scenario is a emqtt cluster deployed behind a load balancer.

![](https://cdn-images-1.medium.com/max/1600/1*9WTiLu7RT3OI4faS-tKZkA.png)

A load balancer can:
1. balance the work load between the nodes in cluster;
2. hide the network details, no client side changes are necessary if the
cluster changes;
3. off-load the transport-layer handlings, like TLS/SSL.

A load balancer could be software, like HAProxy, or hardware, like F5 device, or
virtual resource, like Elastic Load Balancer(ELB), which is available on
Amazon’s AWS. The last one could be a common choice if the emqtt is deployed on
AWS.

In this article, we will show you how to deploy an ELB on AWS for emqtt cluster.
In this deployment, the SSL is also enabled.

## Preparation

1.  Install 2 emqtt nodes on AWS instances and cluster them up. Here is a link about
installing and clustering emqtt on linux:
[https://medium.com/@emqtt/how-to-install-emq-emqtt-2-3-on-linux-469cbae22f14](https://medium.com/@emqtt/how-to-install-emq-emqtt-2-3-on-linux-469cbae22f14)
1.  Certificate for terminating SSL on ELB. AWS accepts pem format of keys. In this
link you can find information about how to generate self-signed certificate
using openssl:
[https://medium.com/@emqtt/securing-emq-connections-with-ssl-432672ab9f06](https://medium.com/@emqtt/securing-emq-connections-with-ssl-432672ab9f06)
1.  Setup security groups on AWS. A good idea is to put the emqtt cluster nodes in a
group which can be accessed in VPC internal and put the ELB in a security group
which can be accessed by the out-side world.

## Configure the ELB

There are three different load balancer available on the AWS’s EC2 Management
Console: the application LB, the network LB and the classic LB. Our target is to
balance the network traffic and off-load the SSL, the classic LB is the one we
need here. The classic LB is marked as previous generation, don’t be frightened.
If SSL is not necessary, we can also use a network LB in this place.

![](https://cdn-images-1.medium.com/max/1600/1*P2fDs4q6sS69pQ_nqtA-2A.png)

There are 7 steps to complete the ELB setup, by clicking ‘Create’ button on the
Classic Load Balancer block, we start the ELB setup.

Step 1: Define Load Balancer.

Here we define the LB in a simply way, we assume that the MQTT SSL and emqtt
dashboard are the only service on the network.

For this purpose we will add two listener configuration items:<br> 1. LB
protocol SSL on port 8883 and instance protocol TCP on port 1883<br> 2. LB
protocol HTTP on port 18083 and instance protocol HTTP on port 18083

![](https://cdn-images-1.medium.com/max/1600/1*IvUi2OHX06zKFzIQpPMduQ.png)

Step 2: Assign Security Groups

Here it will let you choose creating a new security group or select an existing
security group. We have created one group for public access already and we will
use it for the ELB.

![](https://cdn-images-1.medium.com/max/1600/1*o06RxXM7PDJjLIHZAsRUaA.png)

Step 3: Configure Security Settings

Here the cryptology security will be configured. It decides how the SSL should
be used.

### Select Certificate

AWS Certificate Manager(AWS) is a tool to provision and store certificates. If
you decide let AWS generate and manage certificates for you, ACM will be a good
choice.

Or, you get the certificate from a third part or you sign your own certificate,
you can upload the certificate and its private key to AWS Identity and Access
Management (IAM). The certificate and the key must be in pem format. If you have
stored certificates in IAM already, you can also use the existing ones.

![](https://cdn-images-1.medium.com/max/1600/1*mF1L7VjdriMTSs3hy_k0Fw.png)

### Select a Cipher

You can select to use the predefined security policy or to customize it. By
choosing custom security policy, you can enable/disable the protocol version
support, the SSL options and the SSL ciphers. Usually the predefined policy is
secure enough, but if you know exactly what protocol version and cipher will be
used by the clients, you narrow it down.

*If you are pretty sure that the private key and the certificate you uploaded in
this step is correct, and you you still get an certificate failure later in step
7, don’t panic! It is a known issue, we believe it will be fixed someday. While
it is being fixed, you can use the AWS command line tool to upload the
certificate and key. We have put a small instruction for it at the end of this
article.*

![](https://cdn-images-1.medium.com/max/1600/1*8ctl5oBX0uFL9tITxh3yug.png)

Step 4: Configure Health Check

If an instance failed the health check, it will be removed from the load
balancer. The health check can be done by probing on a port with a specified
protocol (its not an ICMP ping).

![](https://cdn-images-1.medium.com/max/1600/1*td9fO13aRMsr74rFhBu4LA.png)

Step 5: Add EC2 Instances

In this step the MQTT broker will be added. In our case, they are two instances
installed with EMQ in the same VPC. The two instances build an EMQ cluster and
configured with proper security group.

![](https://cdn-images-1.medium.com/max/1600/1*wSvxf1e-T-3Q0l4a2s4kbQ.png)

Step 6: Add Tags

If necessary, add some key-value pairs as tags.

![](https://cdn-images-1.medium.com/max/1600/1*IGBzcpqPrnHFPHV7PzNFwA.png)

Step 7: Review

Here we check the setup for the last time, if everything is ok, we create the
ELB.

![](https://cdn-images-1.medium.com/max/1600/1*C7M6mJ2rEi9lmW5Sd8IGxQ.png)

![](https://cdn-images-1.medium.com/max/1600/1*nlZfg9r8zgzB7MNmILpZ2A.png)

## Test the ELB

We will use mosquitto client to test our setup.

When creating SSL connection, the mosquitto_pub checks the server side
certificate, which is enabled on the ELB, against the root ca. To disable the
hostname verification, we need also invoke the`--insecure` argument:
```
mosquitto_pub -h Demo-ELB-1969257698.us-east-2.elb.amazonaws.com  -t aa -m bb -d -p 8883 --cafile ~/MyRootCA.pem --insecure

Client mosqpub/1984-emq1 sending CONNECT

Client mosqpub/1984-emq1 received CONNACK

Client mosqpub/1984-emq1 sending PUBLISH (d0, q0, r0, m1, 'aa', ... (2 bytes))

Client mosqpub/1984-emq1 sending DISCONNECT
```

Done!

*****

## Upload the Key and Cert Using AWS cli tool

If you are not able to upload the server certificate and its private key in step
3, you can try the aws cli tool.

The aws cli tool requires python 2.5.6+ or 3.3+, make sure you have the proper
python version and pip on your system.

Install the aws cli:
```shell
$pip install awscli --upgrade --user
```

Configure the asw cli with asw configure:
```shell
$ aws configuration

AWS Access Key ID [None]: xxxxxxxxxxxxxxxx

AWS Secret Access Key [None]: yyyyyyyyyyyyyyyyyyyyyyyyyyy

Default region name [None]: us-east-2

Default output format [None]: json
```

Upload Certificate
```
$aws iam upload-server-certificate --server-certificate-name ELB-Cert --certificate-body ~/elb_cert/MyELB.pem --private-key ~/elb_cert/MyELB.key --certificate-chain ~/elb_cert/MyRootCA.pem

{

"ServerCertificateMetadata": {

"ServerCertificateId": "ASCA...............X",

"ServerCertificateName": "ELB-Cert",

"Expiration": "2028-03-27T21:53:25Z",

"Path": "/",

"Arn": "arn:aws:iam::9...........3:server-certificate/ELB-Cert",

"UploadDate": "2018-03-30T23:06:07.872Z"

}

}
```
Enjoy!

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [documentation](https://docs.emqx.com/en) for details.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
