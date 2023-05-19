[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed IoT [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) cloud service product provided by [EMQ](https://www.emqx.com/en). Through this product, we can quickly build a stable and reliable MQTT 5.0 IoT platform with complete functions and excellent performance to help upload all kinds of device data quickly to the cloud for subsequent analysis.

In this tutorial, we will teach you step by step to build an IoT platform. After completing this tutorial, you will know:

1.  How to quickly deploy an MQTT cluster in EMQX Cloud.
2.  How to configure the authentication and access control of the MQTT cluster.
3.  How to use client tools to connect to the MQTT cluster.
4.  How to publish and subscribe messages.

## Step 1: Create an EMQX Cloud account

First, we go to the home page of the [EMQX Cloud](https://www.emqx.com/en/cloud) and click the "Start Free Trial" button.

Then, complete the user registration process according to the prompt information on the page.


## Step 2: Create a trial deployment

After completing the registration, you can return to the home page, click "Login" and enter the console.

Click the "Create Deployment" button in the middle of the page to start the deployment process.

![Select Type](https://assets.emqx.com/images/07a91d444e9400194ee80c2b90df6282.png)

EMQX Cloud provides three versions for you to choose from, which are suitable for different usage scenarios.

- Basic version: This version is suitable for the study and experience of [MQTT protocol](https://www.emqx.com/en/mqtt-guide) or EMQX Broker products and the development of lightweight IoT applications. The basic version offers a 30-day free trial.
- Professional version: This version is suitable for building mission-critical IoT applications. This version provides advanced functions such as data persistence, message distribution, and VPC peering connections. The professional version offers a 14-day free trial.
- Flagship version: This version is suitable for the construction of enterprise-level IoT platforms, provides support for multi-region and exclusive hardware deployment and adds functions such as device management, device shadow, and object model.

Here we choose the professional version for deployment. After clicking "Create Now", you can further select the deployment area, the maximum number of connections and TPS.

![Configuration](https://assets.emqx.com/images/8c1ef3b7d93ba6ac1af1deb7765fd759.png)

After selecting the required product specifications, click "Next" to further confirm the integration information, function list, and estimated cost of the selected specifications.

![Confirm](https://assets.emqx.com/images/c792c192a0a466c7778bd485acd3b40b.png)

Click "Deploy now", wait a few minutes, and you can have your exclusive MQTT cluster.

## Step 3: Enter the cluster management interface

On the cluster list page, you can view the deployment progress of the cluster at any time.

![cluster list](https://assets.emqx.com/images/2033f5075346e8f5969411af6fe611a9.png)


When the deployment is complete, we can see the running status of the cluster is “running”. This status indicates that the cluster is ready for normal use. At this time, we click on the cluster to enter the cluster management interface.

![cluster management](https://assets.emqx.com/images/5813be2c9f19b9682ffcae5b76373d76.png)

After entering the management interface, we can intuitively see the interface overview information, including the status of the cluster, connection status, connection address, and other information. In the left menu bar, we can check the various configurations and functions provided by the cluster.

At this point, we can write down the connection address and connection port of the cluster for subsequent use.

Of course, before we formally connect to the cluster, we still need to do one important thing: set the authentication information and permission control required for client access.

## Step 4: Add authentication

The process of adding authentication is very simple. We click on the authentication in the left menu bar to expand the secondary menu. We can see that there are two columns: "Authentication" and "Access Control".

We first click on "Authentication". On the right page, we can see all the authentication information added by the cluster. It is empty at the moment, which means that authentication has not been added to the cluster.

![click on "Authentication"](https://assets.emqx.com/images/6d95869ed89a8aeaf14e1b9b1a8519d3.png)

We enter the user name "test" and password "test" in the input box on the right (you can also enter any desired user name and password for subsequent connection ) and click "Add".  

![Authentication](https://assets.emqx.com/images/974c6ef647d150452924df5521b0f4d6.png)

At this point, we can see that a record appears in the list, which means that the authentication information just now has been added successfully.

You can add other required authentication information through this interface. If it is a commercial cluster, you can also click the "Import" button to import device authentication information into the cluster configuration in batches.

## Step 5: Connect the MQTT cluster

So far, we already have an MQTT cluster. There are many ways to connect an MQTT cluster. Usually, we will choose to use the programming method in formal use. We choose the MQTT client SDK of a certain programming language and establish a connection for sending and receiving messages. We can also use some [MQTT client tools](https://www.emqx.com/en/blog/mqtt-client-tools) with graphical interfaces to connect to the MQTT cluster. In this tutorial, we use the online debugging tool provided in the left navigation.  

We enter the connection address and port of the cluster we deployed earlier in the Host and Port input boxes (this information can be found on the overview page of the cluster management). We enter the previously added authentication information in the Username and Password input boxes ("test/test" used in this tutorial, or your customized username and password) and click "Connect".

![Connect](https://assets.emqx.com/images/9dc8e452386a3ec4837a96a516bd5805.png)


## Step 6: Publish and subscribe messages

Then, we first create a subscription. Here we set the topic name to "test/1", click "Subscribe" and expand.

![create a subscription](https://assets.emqx.com/images/44e1a893a6aecc34f76df623f80814b5.png)

At this point, we can see that we have successfully subscribed to the "test/1" topic. So next, we try to publish a message on the topic to see if it can be received. We first modify the topic name to "test/1", and then select the connection we set up earlier.  

![publish message](https://assets.emqx.com/images/c369e72db1d9433e4862b862adb5b629.png)

At this point, click "Publish" to successfully publish our preset information.

![Publish](https://assets.emqx.com/images/da3d276cec02e0b64bb14c3d6ec6d52f.png)


So far, if you follow our tutorial step by step, you have successfully completed the operations of cluster creation, access control, and sending and receiving messages!

In this tutorial, we experienced the process of building an MQTT IoT platform from scratch. Of course, this is just the beginning. EMQX Cloud has many very powerful functions waiting for you to try. For example, you can configure VPC peering connections so that your MQTT cluster can be integrated with other services deployed on the same public cloud platform in the same region. You can also use the powerful rule engine function to save the messages received by the MQTT cluster to different databases or forward them to other [message queues](https://www.emqx.com/en/blog/mqtt5-feature-inflight-window-message-queue) according to the rules, and these functions do not require you to write a line of code!

In the process of using EMQX Cloud products, if you have any questions, comments, or suggestions, please feel free to contact us ([cloud-support@emqx.io](mailto:cloud-support@emqx.io)). We hope EMQX Cloud can help you develop your IoT business more smoothly.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
