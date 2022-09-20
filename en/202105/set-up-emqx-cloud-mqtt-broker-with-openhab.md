[OpenHAB](https://www.openhab.org/), also known as open Home Automation Bus, is an open-source home automation software written in Java. With the strengths of integrating various devices, providing a clear user interface, and supporting the most flexible tools, openHAB becomes one of the most outstanding platforms in the field of home automation.

With the high flexibility and ease of use, openHAB provides a particular binding for users to connect [MQTT Broker](https://www.emqx.com/en/products/emqx). In this article, we will introduce to you the process of setting up [EMQX Cloud MQTT Broker](https://www.emqx.com/en/cloud) with openHAB.



## What is MQTT?

MQTT, known as Message Queuing Telemetry Transport, is a lightweight IoT messaging protocol based on the publish/subscribe model and is becoming the standard for IoT communications with its simplicity, QoS support, lightweight and bandwidth-saving features.



## What is EMQX Cloud MQTT?

[EMQX Cloud](https://www.emqx.com/en/cloud) is an MQTT messaging middleware product for the IoT domain from EMQ. As the world's first fully managed [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) public cloud service, EMQX Cloud provides a one-stop O&M colocation and a unique isolated environment for MQTT messaging services. It serves dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications.

EMQX Cloud is available in three plans: Basic, Professional, and Unlimited, which offers a variety of flexible product specifications to support the deployment of fully managed MQTT services exclusively for you on the world's leading public clouds. Need more information with EMQX Cloud's product plan? Click[ here](https://docs.emqx.io/en/cloud/latest/pricing.html).

Such a powerful product is a great choice to integrate with openHAB. You could check out the[ documentation](https://docs.emqx.io/en/cloud/latest/) to get more information regarding EMQX Cloud。



## Binding EMQX MQTT Broker with openHAB 3

If it's your first time using EMQX Cloud, don't worry. We will guide you through connecting [Home Assistant](https://www.emqx.com/en/blog/integrate-emqx-mqtt-cloud-with-home-assistant) with EMQX Cloud.

1. [Create](https://accounts.emqx.io/signup?continue=https://www.emqx.com/en/cloud) an EMQX Cloud Account.

2. Login to EMQX Cloud [console](https://cloud.emqx.io/console/) and start a new deployment.

   ```tip
   For the first-time EMQX Cloud customers, we have an opportunity for you to create a free trial deployment of up to 30 days in length. The free trial deployment is an ideal way for you to learn and explore the features of EMQX Cloud. 
   ```

3. After the new deployment is created and the status is **running**, add the client authentication information (you could choose to add manually or import from the file).  

   ![add authentication](https://docs.emqx.io/assets/img/auth.6543e1b4.png)

4. Install openHAB. You could easily get openHAB installed by following the steps shown [here](https://www.openhab.org/docs/installation/). OpenHAB could be run on various systems based on your preference. 

5. After the openHAB is installed, run the openHAB and go to [console](http://localhost:8080/).

6. Go to `Settings` and install MQTT Binding:

    ![openHAB MQTT binding.png](https://assets.emqx.com/images/cc395740e3aaa6c3b7f6599f38543c16.png)


7. Add MQTT to `Things`

    ![add mqtt to openHAB things](https://assets.emqx.com/images/b6f79d674a5fb01e49e4a391d751b2d1.png)

8. Select `MQTT Broker` and fill in the information of the deployment we created before.

    ![select mqtt broker](https://assets.emqx.com/images/1589a0bec044b3ce55522c81a47a8f85.png)

   For the user name and password, fill in the authentication information as mentioned before.

    ![mqtt broker info](https://assets.emqx.com/images/30bc01230493f1da0cb7c39818905a9c.png)
   

9. When there is a little green label that shows `ONLINE`, you are successfully connecting openHAB with EMQX Cloud. Congrats!

    ![mqtt broker inline](https://assets.emqx.com/images/a29093ef1b02ff829a64a6785c57c9b6.png)

   You could also check the status from the EMQX Cloud's monitor page.

    ![EMQX Cloud's monitor page](https://assets.emqx.com/images/8077ce96ef86b572fb6c15b1b8343cd0.png)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
