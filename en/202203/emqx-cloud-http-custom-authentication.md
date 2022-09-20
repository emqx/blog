Authentication, also known as 「verification」, refers to the confirmation of the user's identity through certain means. Authentication is an important part of most applications, and enabling authentication can effectively prevent illegal client connections. Authentication in [EMQX Cloud](https://www.emqx.com/en/cloud) means that when a client connects to EMQX Cloud, the client's permission to connect to the server is controlled through the server configuration.

With the increase of the users, their requirements regarding authentication become more and more complex. Many users have begun to use self-built authentication centers and keep the authentication process on the user side, so as to ensure data security and reduce the risk of data leakage. This requires EMQX Cloud to provide the ability to connect to the user-built authentication center. At the same time, although EMQX Cloud supports batch importing or adding authentication information, it often takes a long time to modify or troubleshoot problems in practice if the number of authentication devices grows rapidly.

In response to the above requirements, **EMQX Cloud recently launched the HTTP custom authentication**. Users can connect to their own authentication center and judge the login authority of the terminal through the returned information, so as to realize more complex authentication logic and ACL verification logic. Currently, the custom authentication function supports permission authentication and access control authentication.

### **HTTP Authentication Principle**

EMQX Cloud uses the relevant information of the current client as parameters in the device connection event, initiates a request for permission query from the user-defined authentication service, and processes the authentication request through the returned HTTP response status code (HTTP statuscode).

- Authentication failed: returns 4xx status code from API
- Authentication succeeded: return 200 status code from API
- Authentication ignored: returns 200 status code from API and ignore message body

Log in to EMQX Cloud, click 「Authentication」 - 「Custom Authentication」 on the left side of the deployment, and click 「Configure Authentication」 in the initial interface to start configuring HTTP custom authentication.

![EMQX Cloud Custom Authentication](https://assets.emqx.com/images/672d005471596e849e272b43238722f7.png)

During authentication, EMQX Cloud will use the current client information to fill in and initiate an authentication query request configured by the user to query the authentication data of the client on the HTTP server.

Configure the required parameters for permission authentication on the form page, including authentication request address, authentication request parameters, HTTP request method, and request content type. If there are no special requirements for other parameters, the default values can be used.

![EMQX Cloud Custom Authentication](https://assets.emqx.com/images/ceee628523326555164a6b2306c67d14.png)
 

> Note:
>
> If the current deployment is the basic version, please fill in the public network service verification address for the request address.
>
> If the current deployment is the professional version, please fill in the intranet IP service verification address for the request address

 

Through HTTP custom authentication, users can more flexibly combine the self-built authentication center with EMQX Cloud, which greatly improves the security of authentication and solves the problem of complex authentication processes for massive devices.

### Get started quickly with EMQX Cloud

We have also made a lot of optimizations in the overall usage process of EMQX Cloud recently, such as optimization of Quick Start Guide and help documents, multilingual SDK access demo, so as to help users get started with the product quickly.

 

EMQX Cloud Quick Start optimization

![EMQX Cloud Quick Start](https://assets.emqx.com/images/1d4e40de79b6d643f4832e8a79f13b1d.png)
 
Help document structure optimization

![EMQX Cloud document structure optimization](https://assets.emqx.com/images/b1374ed17cb9c4cce11e78190b0cef8e.png)
 

Through more friendly interaction processes and more complete product functions, EMQX Cloud will efficiently connect your massive IoT devices and help you quickly build an IoT platform and accelerate IoT application development.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
