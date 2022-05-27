In April, the EMQX team released many maintenance versions of 4.x, which brought a number of new features on the basis of further improved stability. It includes enhancing the support for Pulsar, supporting the use of gRPC service to decode data, and improving the experience of users of the rule engine. In addition, 5.0.0-rc.2 has been released.

In terms of cloud services, EMQX Cloud launched a value-added service for user-defined function, which brought an update of the feature to simplify user procurement process, and supported Aliyun Cloud to deploy private Internet connection. In addition, the Cloud Native team has good news: EMQX has joined the Docker official image.

## EMQX

### New Progress of 5.0: 5.0.0-rc.2 released

In April, the EMQX team improved the UI style and interaction style of 5.0 Dashboard, while polishing and perfecting each feature in detail. At present, 5.0.0-rc.2 has been released. Welcome to download and try it out.

### Fast Iteration of Maintenance Version

In April, EMQX team successively released 8 versions, including the community version v4.3.13, v4.3.14, v4.4.2, v4.4.3 and the enterprise version v4.3.8, v4.3.9, v4.4.2 and v4.4.3, which fixed more than 40 problems. For details, please visit Release Notes on the right side of official website download page.

If you have a problem that is not included in the fixes above, you can feedback through our [Github](https://github.com/emqx/emqx/issues) and we will actively assist you.

In addition to improving the stability of use, the new version above brings many improvements for features as well: resetting the statistical indicators of specified rules supported by the rule engine, newly-adding the confirmation of connection and the completion of authentication events, supporting the compression functions such as zip and gzip, enhancing the support for Pulsar, supporting the use of gRPC services with encoding and decoding features, etc.

## EMQX Cloud

### User-defined Function

User-defined function is a newly developed online value-added service, which is used to bind scripts for Topic. At present, it supports ECMAScript5.1/JavaScript, which can realize the encoding, decoding or preprocessing of Payload content, so as to solve the problem of data reported by equipment and data conversion of application end in scenarios such as the connection of industrial equipment. For example, the equipment reports binary encoded data, which can be converted into JSON format and reported to the server end for processing. After being processed by the user-defined function, the data in Topic can be distributed to cloud resources through the feature of data integration, or can be directly subscribed and consumed, which is very flexible.

Currently, the user-defined function service is in the internal test stage, and users can apply for a 14-day free trial through work order.

### External Authentication and Access Control

External authentication and access control help users to carry authentication with their own services. At present, on the basis of supporting HTTP authentication, MySQL and PostgreSQL are added as data sources for authentication. The principle of external authentication and access control is that when the client needs authentication, the EMQX Cloud will fill the query statement with the information of the current client and perform the authentication configured by the user. Determine whether it passed the verification or not by returning. In this way, it is more secure, reliable and flexible to use the data in the user's own database for authentication.

On the page of deployment details, click **Authentication - External Authentication** on the left menu to select the corresponding authentication method for configuration.

## EMQX Kubernetes Operator

### Feature update

The following new features are available in the EMQX Operator v1.1.6 released in April:

1. User-defined configure for SecurityContext, so that users can configure the security context according to their own needs.
2. Default configure for acquisition of EMQX Operator Metrics is provided.

### Optimization and Improvement

1. Fixed the rights issue deployed on Kubernetes cluster services provided by cloud manufacturers such as EKS and ACK.
2. Fixed the Operator Manager node selection failure in restarting Node.
3. Removed the limit on the number of EMQX cluster nodes >=3.
4. Removed the default configuration of emqx_prometheus plug-in, and users can decide whether to configure it or not according to specific requirements.
5. Improved the resource configuration parameters of EMQX Operator Manager based on test results of performance pressure.

### Forthcoming

EMQX Operator v1.2 and v1beta3 APIVersion are under development, and v1beta3 APIVersion will bring a more rational .spec architecture.

The v1.2 will introduce improved event logging and cluster state description.

### Docker Image

EMQX has joined the Docker official image: [https://hub.docker.com/_/emqx](https://hub.docker.com/_/emqx)

Users can now get the EMQX image directly from the `docker pull emqx`.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
