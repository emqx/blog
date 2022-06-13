In May, EMQX 5.0.0-rc.3 and rc.4 were consecutively released. The updated versions now provide additional support for jq syntax to the rule engine, a significantly streamlined default configuration file, and a further adjusted and optimized Dashboard menu bar. The official release of EMQX 5.0 is getting closer. Meanwhile, the next maintenance release of v4.3 and v4.4 has been released as well.

EMQX Cloud now offers additional AWS private network connectivity and more regional deployment support, as well as more options for external authentication and data integration services.

## EMQX

### EMQX 5.0.0-rc.3 and rc.4 release overview

We have introduced the new features of EMQX 5.0 from the Dashboard perspective with EMQX 5.0.0-rc.2. EMQX 5.0.0-rc.3 and -rc.4 have now been released with new features on the basis of further improved stability.

#### Rules engine supporting jq syntax

The jq syntax can now be used in the rule engine SQL to handle more complex JSON data. JSON arrays can be indexed and sliced, the data can be filtered by condition, fuzzy queries on Keys can be carried out, multiple filters can be combined using pipeline commands, the average of JSON arrays can be calculated using built-in functions, and the functions can even be customized for more complex computations. The jq syntax gives the rule engine SQL more powerful data processing capabilities. Refer to the jq manual to learn more about its usage. The following is a simple example of the use of the jq syntax in rule engine SQL.

```
SELECT
  jq('.', payload) as example
FROM
  "t/#"
```

![Rules engine](https://assets.emqx.com/images/2a90ef557aed7e226e373def68e1558c.png)

#### Simplified default configuration file

In version 5.0.0-rc.4, the default configuration file is now simplified (minimised) to less than a hundred lines, with additional configuration file examples to help users understand the use of all configuration items. This effectively frees users from most of the less important or infrequently used configurations, allowing them to focus on the important ones, further enhancing ease of use.

```
## NOTE:
## Configs in this file might be overridden by:
## 1. Environment variables which start with 'EMQX_' prefix
## 2. File $EMQX_NODE__DATA_DIR/configs/cluster-override.conf
## 3. File $EMQX_NODE__DATA_DIR/configs/local-override.conf
##
## cluster-override.conf is overwritten at runtime when changes
## are made from EMQX dashboard UI, management HTTP API, or CLI.
## All configuration details can be found in emqx.conf.example

node {
  name: "emqx@127.0.0.1"
  cookie: emqxsecretcookie
  data_dir: "data"
  etc_dir: "etc"
}

log {
  file_handlers.default {
    level: warning
    file: "log/emqx.log"
  }
}

cluster {
  name: emqxcl
  discovery_strategy: manual
}


listeners.tcp.default {
  bind = "0.0.0.0:1883"
  max_connections = 1024000
}

listeners.ssl.default {
  bind = "0.0.0.0:8883"
  max_connections = 512000
  ssl_options {
    keyfile = "etc/certs/key.pem"
    certfile = "etc/certs/cert.pem"
    cacertfile = "etc/certs/cacert.pem"
  }
}
```

To download the trial or get more information on the optimizations and bug fixes, please visit: [EMQX 5.0.0-rc.3](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.3) & [EMQX 5.0.0-rc.4](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.4).

### 4.3 and 4.4 Maintenance release overview

The maintenance version v4.3.15 brings more than 20 bug fixes and improvements, such as  support for boot paths that contain spaces, improvement of EMQX startup on Windows to show error messages when startup fails, and version checking to avoid hot upgrades across major releases. etc.

#### Rule engine SQL supports more functions

**Included versions:** Open-source v4.3.15, Open-source v4.4.4, Enterprise v4.3.10, Enterprise v4.4.4

1. Time conversion function

   The format_date function in the rule engine SQL can now be used to convert the incoming integer timestamp or automatically convert the current timestamp to a time string in a specified format, or the date_to_unix_ts function can be used to convert a time string in a specified format to an integer timestamp. Example:

   ```
   SELECT
     format_date('nanosecond', '+08:00', '%y-%m-%d %H:%M:%S%Z') as date1
     format_date('nanosecond', '+08:00', '%y-%m-%d %H:%M:%S%Z', timestamp) as date2
   FROM
     "t/#"
   ```

2. Floating-point output precision control functions

   The` float2str/2` function was added to support specifying the output precision of floating-point numbers.

#### The addition of Basic and JWT authentication support for Pulsar

**Included versions:** Enterprise v4.3.10, Enterprise v4.4.4

Basic and JWT authentication support was added for Pulsar, which can be used with TLS for better security.

#### Support for JWT for authentication

**Included versions:** Open-source v4.3.15, Open-source v4.4.4, Enterprise v4.3.10, Enterprise v4.4.4

JWTs used for client connection authentication can now continue to be used for authentication for more flexible rights management capabilities. This feature requires JWT to carry ACL statements that meet formatting requirements. Refer to the official website documentation for details.

#### **Authentication using the built-in database (Mnesia) as data source supports multi-condition filtering and fuzzy queries**

**Included versions:** Open-source v4.3.15, Open-source v4.4.4, Enterprise v4.3.10, Enterprise v4.4.4

Similar to the query client, the authentication and authorization using built-in database as data source now provides query options, such as `_like_clientid`, `_like_username` and `topic`, among which, `_like_clientid` and `_like_username` support fuzzy queries using a substring.

#### Supports configuration of the log time format to be compatible with the time format in older versions

The `log.formatter.text.date.format` configuration was added to support the `rfc3339` or FORMAT string, that is, `YYYY-MM-DDTHH:mm:ss.SSSZZ` would be compatible with the time format in logs of older versions, such as 4.2.

### Community news

The EMQX team attended the 2022 Code BEAM Europe held in Stockholm, Sweden on May 19-20.

William Yang, EMQ’s software engineer, delivered an inspiring talk titled, “QUICER: The Next Generation Transport Protocol Library for BEAM”, introducing the world’s first MQTT over QUIC implementation powered by EMQ, and the new [open-source library](https://github.com/emqx/quic) built for BEAM.

Another EMQX engineer, Dmitrii Fedoseev, discussed how to test distributed consistency fault tolerance using the library created by him: [snabbkafee](https://github.com/kafka4beam/snabbkaffe) , and described how EMQ has successfully applied a trace-based approach to real-world applications running in production. 


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>


## EMQX Cloud

### Support for creating AWS PrivateLink

PrivateLink enables a secure and stable private connection between the private network VPC, where the EMQX Cloud Deployment is located, and the services on the public cloud, simplifying the network architecture, realizing private network access service, and avoiding potential security risks associated with accessing services over the public network.

EMQX Cloud adds support for connecting to PrivateLink deployed on AWS, connecting the VPC where the deployment is located with the VPC where the resources are located on AWS (overseas), which is equivalent to achieving communication within the same network

### Supports more deployment regions

EMQX Cloud is now available in Hong Kong on AWS and in Taiwan on Google Cloud Platform. The cost is consistent with other regions. Enterprise users that have business in these regions will have more deployment options.

### External authentication support for Redis

New support for client authentication and access control using data stored in the user’s own Redis service. At present, EMQX Cloud supports four services for authentication and access control: HTTP, MySQL, PostgreSQL and Redis. Learn more about external authentication: [https://docs.emqx.com/en/cloud/latest/deployments/custom_auth.html](https://docs.emqx.com/en/cloud/latest/deployments/custom_auth.html)

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

## EMQX Kubernetes Operator

In May, EMQX Operator, a tool for automating the deployment, configuration and management of EMQX clusters on Kubernetes, was released in version 1.1.8, providing the following new features.

### Features update

1. Better EMQX Custom Resource Status
2. Improved resource operation logs into event logs
3. Converted some logs in EMQX Operator into events
4. EMQX Operator resource checklist implementation
5. Better EMQX Custom Resource Status

### Improvements and optimizations

1. Fixed the mirror tag issue, supports the tag based on private repository
2. Fixed the restart listener exception issue after updating .spec.listener.certificate

### Test and validation

EMQX Operator stress tests of EMQX with 1 million connections and 500,000 TPS based on cloud environment.

### Upcoming

EMQX Operator 1.2 and v1beta3 APIVersion are under development. The v1beta3 APIVersion will bring more of a rational .spec structure, and 1.2 will introduce better event log and cluster status descriptions.
