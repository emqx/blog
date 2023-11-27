EMQX development work is in full swing this July. We have added some exciting features and made a breakthrough progress on the key tasks of version 5.0.

## The new config file

### Structure refactored

The new config structure will include only one file in [HOCON](https://github.com/lightbend/config/blob/main/HOCON.md) format: the `emqx.conf`. It will cover all configurations related to emqx, including configurations for EMQX core (the broker), and for other applications or plugins. Relying on the characteristics of HOCON syntax, we redesigned a hierarchical configuration structure. This version of the configuration file will be more readable, editable, and maintainable.

### Support runtime hot reloading

Most configuration entries of EMQX will take effect at runtime after modification, not requiring a restart of the service. What’s more, there will be HTTP APIs supporting configuration changes, as well as reloading. 


![EMQX new config file](https://assets.emqx.com/images/41a66271f3fdb2514c299307395c7f73.png)

## The Swagger UI

### Swagger UI to visualise HTTP interface interactively

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a popular HTTP API documentation tool that is visible and interactive. We are refactoring the HTTP APIs to conform to the [OpenAPI](https://swagger.io/specification/) specification. An OpenAPI specification file will be generated after building EMQX and it will then be used by the Swagger UI to render the HTTP API documents. Now (5.0-alpha.3) you can access this interactive document page at http://127.0.0.1:18083/api-docs.

![swagger](https://assets.emqx.com/images/3247d90db25c6d1e0f108564e921aa94.png)

![api](https://assets.emqx.com/images/86fc2c0679ca3a15c3fa96359dbe4652.png)


## The New Gateways

We introduced the concept of “Protocol Gateway“, and put all the  [IoT protocols](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m) like LwM2M, CoAP, STOMP, MQTT-SN and ExProto into it. This facilitates the integration of the IoT protocols to EMQX broker.

The new architecture of EMQX gateway supports creating multiple instances for one protocol. And the configuration format of these protocols will be unified. In terms of the code structure, we’ve added a common transport layer for gateways to increase the code reusability, we’ve refactored some code of MQTT-SN gateway so that it is not coupled with the EMQX core anymore. More similar work was done for other gateways, stay tuned for more updates.

## Progress on authentication and authorizations

The new authentication component has supported the `enhanced authentication`, and authentication methods via HTTP and MongoDB. And we have improved the code for changing authentication methods via HTTP API.

The new authorization (an extension of the ACL concept) component now has support authorization methods via `MySQL`, `PgSQL`, `MongoDB`, `Redis`, and `HTTP`.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
