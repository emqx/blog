# How to Install EMQ (emqtt) 2.3 on Linux

### Introduction

Welcome to our EMQ (aka emqtt) how-to series.

EMQ is a distributed, highly scalable and easily extensible MQTT broker written
in Erlang. It fully supports MQTT standard 3.1 and 3.1.1.

EMQ can be deployed in single node mode or in cluster mode. Being deployed on
proper hardware, a single EMQ node can serve about one million clients. If you
are going to deploy it in production, cluster mode is recommended for its
high-availability, regardless of the scale of deployment.

EMQ is extensible by plugins. There are several plugins come with default
installation. Also, you can write your own plugins.

In this how-to, we will cover the **installation**, the **clustering** and the
**plugins**.

You can get the full feature list of EMQ from its [github
site](https://github.com/emqtt/emqttd).

### Install EMQ on Linux

EMQ is packaged as zip package or installation package for different Linux
distributions. You can get EMQ from its download page:
[https://www.emqx.io/downloads](https://www.emqx.io/downloads)

Installing EMQ is quite straightforward. If you are using a zip package, just
unzip it to where you want it to be installed. A zip installtion is quite
convenient for development or for multiple installation on same box.

If you are using a Linux installation package, then run the package manage tool
on your Linux distribution. This way of installation is recommended for
production. To install EMQ using the installation package, you might need the
root/sudo privilege.

In some circumstances you might need install `lksctp-tools` first to satisfy the
requirement to run Erlang/OTP.

Here I take the install package for Ubuntu 16.04 as an example:

    apt-get install lksctp-tools
    dpkg -i emqttd-ubuntu16.04_v2.3.x_amd64.deb

Now we can start the EMQ:

    root@emq1:~# emqttd start
    emqttd 2.3.1 is started successfully!

You can check EMQ’s status at anytime using cli tool:

    root@emq1:~# emqttd_ctl status
    Node 'emq@127.0.0.1' is started
    emqttd 2.3.1 is running

Or check it with Web GUI. EMQ comes with a Web Dashboard that by default is
enabled and runs at port 18083. The default usename/password is *admin/public*:

![](https://cdn-images-1.medium.com/max/2000/1*UgisNXSvFvRj5yFCHDX5hA.png)
<span class="figcaption_hack">EMQ Dashboard</span>

Now the EMQ broker is up and ready. We will test it with mosquitto_pub and
mosquitto_sub. We will subscribe to topic ‘test’ and publish a message to this
topic with the payload ‘123’:

![](https://cdn-images-1.medium.com/max/1600/1*ipsyrsty9_N7iVD-BzVj1A.png)

### Configuration of EMQ

After that the EMQ is successfully installed, all the necessary configurations
are set with a default value, the MQTT broker service is ready. If you want
configure it to meet your specific requirements ,you will need to change the
default configuration or add some new ones.

If the EMQ is installed using the installation package, config files can be
found under the ‘/etc/emqttd’ folder. If it is installed using the zip file, the
config files are under ‘patch-to-emq-installation/etc/’ folder.

EMQ uses ‘key = value’ syntax for configuration. Comments start with ‘#’. The
following example shows how to change the node name, the max client number, some
default ACL behaviors and the TCP listening port for MQTT protocol:

    ## Node name
    node.name = emqttd@127.0.0.1
    ...

    ## Max ClientId Length Allowed.
    mqtt.max_clientid_len = 1024
    ...

    ## Deny Anonymous authentication
    mqtt.allow_anonymous = false

    ## ACL nomatch
    mqtt.acl_nomatch = deny
    ...

    ## External TCP Listener: 1883, 127.0.0.1:1883, ::1:1883
    listener.tcp.external = 0.0.0.0:1883
    ...

The directives are grouped into several blocks according to their functions.
Each config block starts with its name embraced in comments and dashes, like:

    ##------------------------------------------------------------------
    ## MQTT Plugins
    ##------------------------------------------------------------------

### Clustering

After successful installation of EMQ, we will try put multiple EMQs into one
cluster and let them work together. Clustering is a commonly used technique when
more performance is needed or high availability is required.

An EMQ cluster works in Active-Active mode, that is, every node in the cluster
is active, no matter how many nodes there are in the cluster. there is no master
or stand-by nodes, means also there will be no fail-over process when a node is
down.

Clustering of EMQ nodes is straight-forward. One cli command is all what we
need. Assuming we have setup two EMQ nodes, the nodes name are
`emq1@192.168.195.131`, and `emq2@192.168.195.172`. The two nodes are up and
running.

We run following command on the node on which the `emq2@192.168.195.172` is
running.

    root@emq2:/opt/emqttd/bin# ./emqttd_ctl cluster join emq1@192.168.195.131
    Join the cluster successfully.
    Cluster status: [{running_nodes,['emq1@192.168.195.131',
                                     'emq2@192.168.195.172']}]

The above cli uses the emqttd_ctl tool with the cluster command to let the emq2
node join the emq2 node and builds a cluster. When the clustering is successful,
it also returns the cluster status, we can see that the two nodes we
pre-configured are now in the cluster.

After a cluster is created, we can check its status with following commands:

    root@emq2:/opt/emqttd/bin# ./emqttd_ctl cluster status
    Cluster status: [{running_nodes,['emq1@192.168.195.131',
                                     'emq2@192.168.195.172']}]

Or, we can check it with the web GUI, the nodes in the cluster are listed in the
overview:

![](https://cdn-images-1.medium.com/max/2000/1*WIpprHiOrka1fsLSbpoVPA.png)
<span class="figcaption_hack">Overview, nodes in the cluster</span>

We verify the cluster with mosquitto tools by sub to one node and pub to the
other node and see if the subscriber can receive the message. If the subscriber
get the message sucessfully, it means that the message is routed in the cluster
from one node th another.

    ## Subscribe to the node emq1@192.168.195.131
    mosquitto_sub -h 192.168.195.131 -t mytopic -d

    Client mosqsub|21578-Zhengyus- sending CONNECT
    Client mosqsub|21578-Zhengyus- received CONNACK
    Client mosqsub|21578-Zhengyus- sending SUBSCRIBE (Mid: 1, Topic: mytopic, QoS: 0)
    Client mosqsub|21578-Zhengyus- received SUBACK
    Subscribed (mid: 1): 0

    ## Publich to the node emq2@192.168.195.172
    mosquitto_pub -h 192.168.195.172 -t mytopic -m abcd1234 -d
    Client mosqpub/3268-emq2 sending CONNECT
    Client mosqpub/3268-emq2 received CONNACK
    Client mosqpub/3268-emq2 sending PUBLISH (d0, q0, r0, m1, 'mytopic', ... (8 bytes))
    Client mosqpub/3268-emq2 sending DISCONNECT

    ## On the client that we subscribed to this topic we receive:
    Client mosqsub|21578-Zhengyus- received PUBLISH (d0, q0, r0, m0, 'mytopic', ... (8 bytes))
    abcd1234
    Client mosqsub|21578-Zhengyus- sending PINGREQ
    Client mosqsub|21578-Zhengyus- received PINGRESP

To remove a node from a cluster is also very straight-forward, we can do it on
the command line:

    ./emqttd_ctl cluster leave
    Leave the cluster successfully.
    Cluster status: [{running_nodes,['emq2@192.168.195.172']}]

We can check the status after a node has left by cli or on Web Gui. It is the
same as we’ve done above.

### Plugins

Plugins extend the functions and performance of EMQ. EMQ comes with some
plugins, they are configured by separated `conf` files (Each plugin has it own
conf file). the conf files are collectively stored in the `etc/plugins` (by ZIP
installation) or the `/etc/emqttd/plugins` (by package installation) folder.

Beside the plugins come with the system, you can also write your own plugins to
extend the EMQ. We will have a article for how to write a plugin.

Next we will demonstrate how to enable and config a plugin. This time we take
the `emq_auth_redis` as an example. This plugin make it possible to store the
auentication and authorization data in a redis server and check them when it a
client try to access the EMQ.

Before we start with this plugin, make sure that the anonymous access is
disabled and the ACL mismatch access is denied (see the emq.conf example above).

Here we’ve setup a Redis at the address `192.168.195.162,`also, we will need to
put some data into the redis, namely the username, the password and the ACLs. On
the Redis, we do the following:

    ## Add a user by adding a user hash with 'password' field
    ## HSET mqtt_user:<username> password "passwd"
    HSET mqtt_user:john password "123"

    ## Add some rules for the above user
    ## HSET mqtt_acl:<username> <topic> <privilege>
    ## Here the allowed values of <privilege> are 1, 2 and 3:
    ## 1: subscribe
    ## 2: publish
    ## 3: sub and pub
    HSET mqtt_acl:john sensors/# 1
    HSET mqtt_acl:john sensors/001 2
    HSET mqtt_acl:john alarm 3

Now we have a user john, his password is 123. John can subscribe to all sensors
and he can publich to sensors/001, also, John can both publish and subscribe to
topic alarm.

On the EMQ, we modify the host name (address), the port and the password of
Redis in `emq_auth_redis.conf` to make it in line with the redis server setup.
Here we just want to demonstrate the use of plugins in general, so we leave the
rest of this config file untouched:

    ## Redis Server: 6379, 127.0.0.1:6379, localhost:6379
    auth.redis.server = 192.168.195.162:6379

    ## Redis Password
    auth.redis.password = iot123

We now can restart the EMQ and load this plugin by doing following:

    root@emq1:/opt/emqttd/bin# ./emqttd restart
    ok
    root@emq1:/opt/emqttd/bin# ./emqttd_ctl plugins load emq_auth_redis
    Start apps: [emq_auth_redis]
    Plugin emq_auth_redis loaded successfully.

Check it on Web GUI:

![](https://cdn-images-1.medium.com/max/2000/1*K8tIHDe1jkJkOqJetiXk3A.png)
<span class="figcaption_hack">Plugins</span>

At last, we will verify the it with mosquitto client tools.

    ## Try access EQM with non-exist user
    mosquitto_sub -h 192.168.195.131 -t sensors/001 -u alice -d
    Client mosqsub|23031-Zhengyus- sending CONNECT
    Client mosqsub|23031-Zhengyus- received CONNACK
    Connection Refused: bad user name or password.

    ## Try access EMQ with proper username and password
    mosquitto_sub -h 192.168.195.131 -t sensors/001 -u john -P 123 -d
    Client mosqsub|23237-Zhengyus- sending CONNECT
    Client mosqsub|23237-Zhengyus- received CONNACK
    Client mosqsub|23237-Zhengyus- sending SUBSCRIBE (Mid: 1, Topic: sensors/001, QoS: 0)
    Client mosqsub|23237-Zhengyus- received SUBACK

That’s all what we want to cover in this little article. We hope you enjoy this
article, if you have any advise about it, please contact us at:
contact@emqx.io

Thanks!

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [documentation](https://docs.emqx.io) for details.