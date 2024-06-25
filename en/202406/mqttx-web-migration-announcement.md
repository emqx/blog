Dear MQTTX users,

We would like to inform you that we will once again migrate the domain of the MQTTX Web Online site. This change aims to provide you with a more secure and stable service. Please find detailed information and specific instructions regarding the migration below.

## Why Migrate？

The current MQTTX Web site ([http://mqtt-client.emqx.com](http://mqtt-client.emqx.com/)) was recently migrated from <https://www.emqx.io/online-mqtt-client>. However, inherent critical security vulnerabilities arise due to its sole accessibility through HTTP. Besides, it shares the exact origin as the primary domain, [http://emqx.com](https://www.emqx.com/), posing a risk of cookie sharing. These could all potentially lead to information leaks and other security threats.

Therefore, **we have migrated the site to  [https://mqttx.app/web-client](https://mqttx.app/web-client) ** to further enhance overall security and compliance. This will offer you the following benefits:

1. **Enhanced Security**: Adopting the HTTPS protocol ensures data security during transmission, preventing information leaks and other security risks.
2. **Improved User Accessibility**: As MQTTX Web is a client type of MQTTX, placing it under the [https://mqttx.app](https://mqttx.app/) domain will facilitate user access, provide uniformity, and ensure service security and consistency.

## Impact After Migration

Due to our migration to the HTTPS protocol, there are some changes:

1. **WebSocket Connection Limitations**:
   After migrating to HTTPS, regular MQTT over WebSocket connections using `ws://` under the HTTP protocol will no longer be available. All WebSocket connections must use Secure WebSocket `wss://` to ensure data security during transmission. For example, use `wss://broker.emqx.io:8084` instead of `ws://broker.emqx.io:8083`.

   This means you need to update your MQTT over WebSocket connection configurations in both test and production environments. Old data using the `ws://`connection protocol will not be usable on the new site and must adapt to the latest security requirements.

2. **Connection Configurations Update**:
   We recommend using `wss://` connections in both test and production environments. If you're unfamiliar with how to configure this, please refer to our detailed documentation: [Configuring Secure WebSocket Listeners](https://docs.emqx.com/en/emqx/latest/configuration/listener.html#configure-secure-websocket-listener). This document provides step-by-step configuration guidelines to help you complete the update smoothly.

## How to Migrate Your Data Locally？

MQTTX Web data is stored locally in your browser; we do not transfer your data to the cloud. Therefore, you must manually export and import your data to the new site. Here are the specific steps:

1. Visit the old site [http://mqtt-client.emqx.com](http://mqtt-client.emqx.com/). If you have existing data, the old site will display a data export page, guiding you on how to export your data. If there is no existing data, the old site will automatically redirect to the new site.
2. Visit the new site https://mqttx.app/web-client and import the previously exported data.

## Other Solutions

The original intention of MQTTX Web was to provide MQTT users with a convenient in-browser MQTT connection testing tool. However, we have mandated using the HTTPS protocol for data security reasons. This means WebSocket connections within the web application must use Secure WebSocket connections (WSS protocol).

If you need to test `ws://` connections quickly and are not limited to `wss://`, we recommend the following solutions:

1. **Download desktop or command-line clients**: Visit the [MQTTX download page](https://mqttx.app/downloads) for a suitable client version.
2. **Private deployment of the web version**: Use Docker for private deployment, see: [Private Deployment Guide](https://mqttx.app/docs/web/get-started#privatization-deployment). We provide comprehensive build configurations for your private use. Please refer to our development documentation: [Development Documentation](https://mqttx.app/docs/web/development).

## FAQ about Migration

1. **Will the website be unavailable during migration?**
   No, after the new site is launched, the old site will continue to support access but cannot use main functions. When your old local data is migrated and cleared, the old site will automatically redirect to the new site. You can also directly visit the new site to start using it.
2. **Will my data be affected?**
   Your data is stored locally in your browser and will not be transferred to the cloud. Data sharing between different domains is not possible. Therefore, please follow our manual guide to export and import data.
3. **Do I need to change my settings after migration?**
   You may need to update your WebSocket connections to use the WSS protocol. Please refer to our documentation for the appropriate configuration.

## Your Support and Feedback are Valued

Thank you for your understanding and support during this transition. We deeply understand that this migration may cause some inconvenience, and we sincerely apologize for this. This change is to ensure higher security and compliance, and to provide a better user experience.

We remind all users to use our online tools responsibly and avoid any improper use, especially in security testing. We are committed to providing safe, reliable, and efficient services. If you encounter any issues or have feedback during this process, please contact us at <https://github.com/emqx/MQTTX/issues> or [yusf@emqx.io](mailto:yusf@emqx.io). Your feedback is crucial to us, and we appreciate your cooperation.
