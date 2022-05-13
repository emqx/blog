In recent years, as people's demand for home security, convenience, comfort and artistry has increased, home automation has become more and more popular. [Home Assistant](https://www.home-assistant.io/), a popular open-source home automation platform, provides a secure and convenient central control system. In this article, we will introduce you to how to use [EMQX Cloud MQTT Broker](https://www.emqx.com/en/cloud) to connect with Home Assistant.

## What is MQTT Broker

MQTT is a lightweight, publish-subscribe network protocol that transports messages between devices. An [MQTT broker](https://www.emqx.com/en/products/emqx) is a server that receives all messages from the clients and then routes the messages to the appropriate destination clients. 

## Why EMQX Cloud?

[EMQX Cloud](https://www.emqx.com/en/cloud) is an MQTT messaging middleware product for the IoT domain from EMQ. As the world's first fully managed MQTT 5.0 public cloud service, EMQX Cloud provides a one-stop O&M colocation and a unique isolated environment for MQTT messaging services. It serves dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications. 

EMQX Cloud is available in three plans: Basic, Professional, and Unlimited, which offers a variety of flexible product specifications to support the deployment of fully managed MQTT services exclusively for you on the world's leading public clouds. Need more information with EMQX Cloud's product plan? Click [here](https://docs.emqx.io/en/cloud/latest/pricing.html).

Such a powerful product is a great choice to integrate with Home Assistant. You could check out the [EMQX Cloud documentation](https://docs.emqx.io/en/cloud/latest/) to get more information regarding EMQX Cloud.

## Set up Home Assistant with EMQX Cloud

If it's your first time using EMQX Cloud, don't worry. We will guide you through connecting Home Assistant with EMQX Cloud.

1. [Create](https://accounts.emqx.io/signup?continue=https://www.emqx.com/en/cloud) a EMQX Cloud Account.

2. Login to [EMQX Cloud Console](https://cloud.emqx.io/console/) and start a new deployment.

   ```tip
   For first-time EMQX Cloud customers, we have an opportunity for you to create a free trial deployment of up to 30 days in length. The free trial deployment is an ideal way for you to learn and explore the features of EMQX Cloud. 
   ```

3. After the new deployment is created and the status is **running**, add the client authentication information (you could choose to add manually or import from the file.  

    ![add authentication](https://assets.emqx.com/images/9142d9a045b570402515eaa47c6698a6.png)

4. Go to Home Assistant's configuration to add integration.

5. Select MQTT and fill in the deployment information

    ![Add MQTT Broker to Home Assistant](https://assets.emqx.com/images/1da096c0f7a5f4b200b1f14583c49414.png)

    ![EMQX MQTT Cloud deployment information](https://assets.emqx.com/images/26b958bcc271d1f6801d06152c65fd78.png)

   You should enter the `Connect Address` for Broker and the `Connect Port (mqtt)` for Port. Enter the username and password you created on the authentication page. 

6. Click the `Submit` button

7. Your EMQX Cloud deployment is now integrating with Home Assistant, congratulations!

    ![Successfully integrating with Home Assistant](https://assets.emqx.com/images/e6bd46c82942efdbac70ed9d09faa35b.png)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
