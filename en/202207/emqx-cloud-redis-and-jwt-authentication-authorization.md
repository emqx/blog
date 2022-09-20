After the previous HTTP custom authentication and MySQL and PostgreSQL external authentication, EMQX Cloud has recently supported two more external Auth&ACL methods, Redis and JWT. Users now have more choices to achieve more secure and fast access to massive devices flexibly.

## Flexible and diverse authentication methods

As a fully managed cloud-native MQTT messaging service, users can authenticate devices and control the access to Topic through the Auth&ACL module of the console. Authentication takes the form of username and password, and the access control supports three granularities of client ID, username, and all users. Both authentication and access control support the batch import of CSV files.

In addition to storing authentication information in EMQX Cloud, users can also authenticate through external authentication authorization in the external database where the authentication information is stored, and connection to JWT services for authentication is also supported.

Compared to other databases, Redis has rich data types, such as strings, hashes, lists, collections, ordered collections, etc. Its high read/write performance and fast command execution make it widely used in various scenarios.

JWT (JSON Web Token) authentication is a Token-based authentication mechanism that does not rely on the server to retain client authentication information or session information. It can issue authentication information in bulk when it holds a key.

## User guidelines

Users can configure the following operations to use Redis as an external data source, or JWT authentication to complete the authentication and access control.

Access to your console. Then, in the left menu bar, select “Authentication & ACL” -> “External Auth & ACL” to use the feature. For the detailed configuration and debugging steps, please refer to the interface tips and help documentation at the end of the article.


**Redis authentication/access control**

![Redis authentication/access control](https://assets.emqx.com/images/13c966e6086841797d2c40a827de73a2.png)

**JWT authentication/access control**

![JWT authentication/access control](https://assets.emqx.com/images/c0874f657e84983d9fac5aef523e0c67.png)

> **Notes**
>
> 1. If both built-in authentications are enabled, EMQX Cloud will chain the authentication in the order of default authentication first, followed by external Auth&ACL.
> 2. When multiple authentication methods are enabled at the same time, the system will default to the order in which the modules were enabled to perform queries.
> 3. If the present deployment is the Standard Plan, fill in the public address for the server address.
> 4. If the present deployment is the Professional Plan, create a VPC peer-to-peer connection, and fill in the intranet address for the server address.
> 5. If an Init resource failure prompt is received, check whether the server address is correct, and whether the security group is enabled.


This update further adds the option of external Auth&ACL feature. Users can choose the corresponding authentication method according to their business needs and handle it with flexibility, regardless of whether it is large-scale device access or mobile application scenario.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

> **Related documents**
>
> Redis Authentication/Access Control: [https://docs.emqx.com/en/cloud/latest/deployments/redis_auth.html](https://docs.emqx.com/en/cloud/latest/deployments/redis_auth.html) 
>
> JWT Authentication/Access Control: [https://docs.emqx.com/en/cloud/latest/deployments/jwt_auth.html](https://docs.emqx.com/en/cloud/latest/deployments/jwt_auth.html)
