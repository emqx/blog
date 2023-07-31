>[EMQX](https://www.emqx.io/) is a popular [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) widely used in the Internet of Things(IoT), Industrial IoT (IIoT) and Connected Cars. It can connect millions of devices at scale, move and process your IoT data in real-time anywhere with high performance, scalability and reliability.
>
>In this blog series, we will explore common troubleshooting scenarios when using EMQX and provide practical tips and solutions to overcome them. Readers can optimize your MQTT deployment and ensure smooth communication between your devices following this troubleshooting instruction.

## Introduction

Authentication is critical in the majority of IoT applications as it ensures the effective prevention of unauthorized client connections and facilitates access control. However, in practical use, we often encounter challenges such as connection failures and access control not working as expected. 

This article introduces the authentication methods supported by EMQX and common authentication issues, and provides corresponding solutions to help users better leverage the power of EMQX.

## Common Authentication Methods in EMQX

EMQX uses the following authentication methods:

- **SSL/TLS Authentication:** EMQX uses TLS/SSL certificates to encrypt and authenticate connections, ensuring secure and trustworthy communication. Both the client and server require verification using certificates.
- **Username and Password Authentication:** EMQX allows users to authenticate using a username and password. Only authenticated users can connect to EMQX.
- **Access Control:** EMQX supports Access Control Lists (ACLs) for granular access control. ACLs define permissions for connecting, subscribing, and publishing to specific topics, as well as other operations. By using ACLs, EMQX ensures that only authorized devices or users can connect and interact with it.

## SSL/TLS Authentication Issues

SSL/TLS authentication is commonly used to encrypt and authenticate network connections. However, when configuring SSL authentication on the EMQX or LB(Load Balancer) side, connection errors may occur.To troubleshoot the problem, we can check the error logs in the EMQX backend or search for the error keywords when connecting.

**Error:Unable to verify the first certificate**

This is generally a problem associated with the certificate configuration or validity period.  the certificate has expired or is invalid, it will cause a connection failure. The solution is to reissue the certificate and replace it.

To check the validity period of the certificate, you can use the following command for troubleshooting.

```
openssl x509 -in emqx.crt -noout -text
```

Here is a screenshot of the details showing that the certificate has expired:

![screenshot](https://assets.emqx.com/images/fb0340f97f28ee049369b3e40fae00af.png)

**Key error logs: eacces**

If the server's certificate lacks read permissions, it may refuse connections or issue security warnings.

In this case, you can check the EMQX log and see an error similar to the following.

```
connection_shutdown, reason: {ssl_error,{options,{cacertfile,"etc/certs/emqx.crt",{error,eacces}}}}
```

Command to check if the certificate has readability:

```
file:open("etc/certs/emqx.crt",read).
```

Here is the process of using code to check the readability of files：

```
 ./bin/emqx remote_console
Erlang/OTP 24 [erts-12.3.2.2] [emqx] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1]

Eshell V12.3.2.2  (abort with ^G)
(emqx@127.0.0.1)1> file:open("etc/certs/emqx.crt",read).
{error,eacces}
(emqx@127.0.0.1)2> file:open("etc/certs/emqx.key",read).
{error,eacces}
(emqx@127.0.0.1)3> file:open("etc/certs/emqx.crt",write).
{error,eacces}
(emqx@127.0.0.1)4> file:open("etc/certs/emqx.key",write).
{error,eacces}
```

According to the command line, it can be seen that EMQX cannot read the relevant certificate. In this case, it is necessary to add read permissions to the certificate.

**Error: Hostname not match**

The SSL/TLS certificate contains the subject to specify the domain name to which the certificate applies. If the certificate subject and domain name do not match, SSL/TLS authentication will fail.

Error when connecting with the [MQTTX](https://mqttx.app/) tool:

```
Error: Hostname/IP does not match certificate's altnames
```

We can check the subject of the certificate and the domain name being accessed by the client to locate the problem.

**Key error logs: enoent**

When configuring SSL certificate in EMQX, the SSL certificate file must exist and the configuration path must be correct. If the configuration path is incorrect or the file name is wrong, there will be an error as below displayed in the EMQX log.

```
errorContext: connection_shutdown, reason: {ssl_error,{options,{certfile,"etc/certs/emqx.cr",{error,enoent}}}}
```

## Username and Password Authentication

When using username and password for identity authentication,the following issues may occur:

- Allowing all clients to connect despite authentication being configured;
- Unable to connect even with the correct password;
- Prolonged authentication time;

In this section we provide solutions to solve the username authentication issues.

**Issue 1: Allowing all clients to connect even though authentication is configured**

Reason: This is because EMQX allows anonymous authenticated client login by default. 

Solution:Set allow_anonymous = false in authentication configuration.

**Issue 2: Unable to connect even with the correct identity**

Reason: This is because if the username or client ID of the device attempting to log in has been added to a blacklist, it will be unable to connect.

Solution: Remove the blacklist restriction.

**Issue 3: Long client authentication connection time**

Cause：

- Disconnection between the authentication server and EMQX

  reThe authentication server is the central node responsible for verifying the client's identity and authorizing its access to the EMQ server. If the connection between the authentication server and the EMQX server is unstable or interrupted, the client may be unable to verify its identity or obtain authorization to access the EMQX server. In this case, check the network connection between the authentication server and EMQX.

- Multiple authentication configurations

  When multiple authentication methods are enabled simultaneously, EMQX will perform chain authentication according to the order in which the plugins are enabled. If all authentication methods return a failure, the client will be unable to connect. Therefore, when multiple authentication methods are enabled, it may cause higher connection latency, and the authentication chain can be checked through the dashboard configuration.

Starting from version 4.4.11, it is possible to configure authentication chains on the EMQX Dashboard. The supported authentication chain names include: internal (or file), http, jwt, ldap, mnesia, mongo (or mongodb), mysql, and pgsql (or postgres), and redis.

![EMQX Dashboard](https://assets.emqx.com/images/cd856a7c799f2f4c6e80ad3d1b1d7c95.png)

We can view enabled authentication modules and their order in the background.

```
./bin/emqx eval "emqx_hooks:lookup('client.authenticate')."
```

View the authentication hook order from top to bottom for the corresponding authentication chain.

```
./bin/emqx eval "emqx_hooks:lookup('client.authenticate')."
[{callback,{fun emqx_auth_jwt:check_auth/3,
            [#{checklists => [],from => password,mod => emqx_auth_jwt_svr,
               pid => <12907.2791.0>}]},
           undefined,0},
 {callback,{fun emqx_auth_mysql:check/3,
            [#{auth_query =>
                   {"select password,salt from mqtt_user where username = ? limit 1",
                    ["'%u'"]},
               hash_type => {plain,salt},
               pool => 'emqx_module_auth_mysql:module:90b76698',
               super_query =>
                   {"select is_superuser from mqtt_user where username = ? limit 1",
                    ["'%u'"]},
               timeout => 5000}]},
           undefined,0}]
```

To further investigate and determine the cause of delays based on the enabled authentication modules, we can try disabling a specific authentication module and see if there is any improvement in performance.

## ACL  Issues

ACL allows us to control the publication or subscription of specified clients to corresponding topics. Here are some methods to troubleshoot the issues that may occur when using ACL:

**Issue1: Ineffective ACL Rules**

If ACL rules are set but ineffective, it may be due to a configuration error, such as configuring a superuser (superusers have the highest permission and are not subject to ACL restrictions).

**Issue2: Long ACL Query Time**

If there are many ACL chains or rules, EMQX needs to traverse all rules to determine whether a particular client is allowed to perform a certain operation. Therefore, the more ACL rules there are, the longer the query time will be.

We can troubleshoot ACL chains by using the following command to view the ACL order from top to bottom, as well as the corresponding set ACLs:

```
./bin/emqx eval "emqx_hooks:lookup('client.check_acl')."
[{callback,
     {fun emqx_auth_jwt:check_acl/5,[#{acl_claim_name => <<"acl">>}]},
     undefined,0},
 {callback,
     {fun emqx_acl_mysql:check_acl/5,
      [#{acl_query =>
             {"select allow, ipaddr, username, clientid, access, topic from mqtt_acl where ipaddr = ? or username = ? or username = '$all' or clientid = ?",
              ["'%a'","'%u'","'%c'"]},
         pool => 'emqx_module_auth_mysql:module:90b76698',timeout => 5000}]},
     undefined,0},
 {callback,
     {emqx_mod_acl_internal,check_acl,
         [#{publish =>
                [{allow,
                     {ipaddr,{{127,0,0,1},{127,0,0,1},32}},
                     pubsub,
                     [[<<"$SYS">>,'#'],['#']]},
                 {allow,all}],
            subscribe =>
                [{allow,{user,<<"dashboard">>},subscribe,[[<<"$SYS">>,'#']]},
                 {allow,
                     {ipaddr,{{127,0,0,1},{127,0,0,1},32}},
                     pubsub,
                     [[<<"$SYS">>,'#'],['#']]},
                 {deny,all,subscribe,[[<<"$SYS">>,'#'],{eq,['#']}]},
                 {allow,all}]}]},
     undefined,-1}]
```

Based on the identified ACL chain, we can investigate the corresponding client hit ACL chain and then analyze the cause of the delay.

Recommendations for optimizing ACL query latency:

- Reduce the number of enabled ACL plugins. Enabling only one ACL plugin can improve client ACL check performance.
- If the ACL rules are very complex, for example, they include multiple conditions and operators, EMQX needs to parse and compare each rule, which can also increase the query time. Therefore, when designing ACL rules, it is necessary to optimize their complexity and reduce them as much as possible.

## Conclusion

In summary, when using authentication and encountering unexpected outcomes, we need to carefully check the relevant logs or analyze the corresponding authentication chain. By identifying the root cause of the issue, appropriate measures can be taken to ensure seamless recovery.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
