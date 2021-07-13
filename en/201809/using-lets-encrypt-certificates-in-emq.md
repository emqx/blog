
## EMQ version: 2.3.3

In our previous article we have shown [how to secure EMQ connection with
SSL](https://medium.com/@emqtt/securing-emq-connections-with-ssl-432672ab9f06).
In that article we’ve used self generated certificate for SSL to secure the
connection between broker and clients. Self generated certificates are
convenient for test and development. But it is uncool to use such certificates
in production, especially when you are publishing your application over the
Internet. People may see untruthful certificate warning when using your service.

### Let’s Encrypt CA and Certificate

Luckily, we have Let’s Encrypt,one great service from Linux Foundation
Collaborative Projects. It can be accessed by anyone without cost or complex
procedure.

The principle of Let’s Encrypt is that it offers Domain Validation (DV)
certificates, but not Organization Validation (OV) or Extended Validation (EV).
By only providing DV, Let’s Encrypt is quick and simple, and it also makes
automatic (no human intervention) issuing and renewing of certificates possible.

Let's Encrypt follows ACME (Automatic Certificate Management Environment)
protocol. To obtain a Let’s Encrypt certificate you will need an agent installed
on the server than bind to the domain you claim to have control to. The agent on
the server owns a RSA key pair, it interact with the Let’s Encrypt CA,
identifies it self to the CA with its public key, and responses to the
challenges from the CA to prove:

* The server, on it the agent runs, is bound to the claimed domain;
* The agent has the control to the private key.

This is usually done by signed/encrypt a nonce sent from the CA and hanging this
signed/encrypted nonce on a URI which starts with the claimed domain.

If you are interested to know more about Let’s Encrypt, please click this: [How
Let’s Encrypt works.](https://letsencrypt.org/how-it-works/)

### certbot, an ACME Agent

As mentioned above, you need an agent installed on the server to generate a RSA
key pair and to interact with the Let’s Encrypt CA to request a certificate.
Here we will us the certbot. certbot is a ACME client by Electronic Frontier
Foundation (EFF), it can request and deploy certificates on your server, an easy
to use automatic tool.

to obtain an server certificate for EMQ uses only a small part of certbot’s
functions. Here we assume that on the server there is no web server running and
we will have to run certbot in standalone mode. In standalone mode, certbot
works also as a web server and put the response on its uri and for the CA to
fetch.

The default key length used by certbot is 2048, change it if necessary
(--rsa-key-size parameter).

#### Install certbot

certbot may be not included in the linux distribution, taken the ubuntu 16.04 as
example, you will need to install is by adding a new ppa in the system before
you install the certbot.

Do the following on the server that EMQ is deployed :

    $ sudo apt-get update
    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:certbot/certbot
    $ sudo apt-get update
    $ sudo apt-get install certbot

#### Run certbot and Verify the Certificates

certbot provides various certificate related functions, here we just want to
request server certificate from the Let’s Encrypt CA, the `certonly` command is
all that we need.

We use the built-in web server from certbot, so the `--standalone` parameter is
necessary. Otherwise you can also `--webroot` to make use of an already running
web server instance.

To specify the domain, we use the `-d` parameter, if there are multiple domains,
then use multiple `-d`. Following command will generate the RSA key pair and
obtain the certificates for you (substitute the domains with the ones that you
actually own):

    $sudo certbot certonly --standalone -d example.com -d iot.example.com

by default, all the generated keys and certificates can be found in
`/etc/letsencrypt/live/$domain` . If you take a closer look into this folder,
you will find there are no phyiscal files, there are just symbol links to files
(always the latest version) in `/etc/letsencrypt/archieve/` and
`/etc/letsencrypt/keys` . The valid period of letsencrypt certificate is
relative short, certbot has a automatic mechanism to renew the certificates.
These symbol links make the management of certificate easier.

The files are:

    ## the issued certificate 
    cert.pem
    ## the certificate with intermediate certificates
    fullchain.pem
    ## the cert chain between issued certificate and CA certificat
    ## intermediate certificates
    chain.pem
    ## Private key for the certificate

Verify the certificate with OpenSSL

    openssl verify -CAfile /etc/letsencrypt/live/$domain/chain.pem /etc/letsencrypt/live/zhengyupan.de/cert.pem 
    ## Should output
    /etc/letsencrypt/live/$domain/cert.pem: OK

For more details about certbot please visit:
[https://certbot.eff.org/](https://certbot.eff.org/)

### Config the EMQ to Use Let’s Encrypt Certificate

Here we use EMQ 2.3.3 as example.

#### HTTPS Dashboard

The dashboard of EMQ is implemented as a plugin. The default https dashboard is
not enabled, we need to enable it by modifying its conf file. The config file of
dashboard is `emqttd_install_location/etc/plugins/emq_dashboard.conf` if you
installed it by unzip a zip package or `/etc/eqmttd/plugins/emq_dashboard.conf`
if you used an installation package.

The directives for enabling the https connection are already there in the conf
file, we just need to remove some leading `#` of the directives and modify them
to fit our case. they are:

    dashboard.listener.https = 18084
    dashboard.listener.https.access.1 = allow all
    dashboard.listener.https.acceptors = 2
    dashboard.listener.https.max_clients = 512
    dashboard.listener.https.access.1 = allow all
    ## subtitute the $domain with your one
    dashboard.listener.https.keyfile = /etc/letsencrypt/live/$domain/privkey.pem
    dashboard.listener.https.certfile = /etc/letsencrypt/live/$domain/fullchain.pem

After doing this modification we can now restart the EMQ and try connect to the
dashboard using https protocol. After that, you can see the nice green lock in
your browser, it is verified by Let’s Encrypt.

![](https://cdn-images-1.medium.com/max/2000/1*HAu3PPF1S3l3uJOUDWVp8A.png)

#### WSS Listener

By default, the WSS is enable on port 8084, we can modify the configuration to
let it use the Let’s Encrypt certificates. Modify the
`emqttd_install_location/etc/emq.conf` (or `etc/emqttd/emq.conf` ):

    listener.wss.external.keyfile = /etc/letsencrypt/live/$domain/privkey.pem
    listener.wss.external.certfile = /etc/letsencrypt/live/$domain/fullchain.pem

Then restart the EMQ, start a WS client with SSL checked:

![](https://cdn-images-1.medium.com/max/2000/1*HH1IMZyBQzN6gkC6j4iumg.png)

On the dashboard check the listeners, it shows one client is connected per wss
on port 8084:

![](https://cdn-images-1.medium.com/max/2000/1*Wxw0TrLi-H5Poc93cWEsHg.png)

#### MQTT/SSL

In the previous article we’ve talked about enabling MQTT/SSL using self signed
certificate. On the EMQ side, this time we will do almost the same, only
difference is that we will use Let’s Encrypt issued certificates this time.

In the `emq.conf` file:

    listener.ssl.external.keyfile = /etc/letsencrypt/live/$domain/privkey.pem
    listener.ssl.external.certfile = /etc/letsencrypt/live/$domaion/fullchain.pem

This time we are still going to use the mosquitto client to verify the SSL
connection. I guess that you still remember in previous article we passed a
`--cafile` parameter to the mosquitto client to enable the SSL, the cafile is
the certificate of issuer of the domain certificate.

To verify the domain certificate, the mosquitto client need to have all the
intermediate certificates and the certificate of Root CA. As mentioned above,
the file `chain.pem` contains the intermediate certificates. But where is the
certificate of Root CA?

The domain certificate is issued by intermediate “Let’s Encrypt Authority X3”,
this intermediate is cross-signed by “DST Root CA X3” (from IdenTrust).
IdenTrust is widely trusted by most OSes and applications, we will “DST Root CA
X3” as root CA.

You have good chance that you already have the ca certificate of “DST Root CA
X3” if you run a not-too-old OS and a not-too-old OpenSSL or Browser. Taking
Ubuntu 16.04 as example, check if this file exists:
`/etc/ssl/certs/DST_Root_CA_X3.pem` .

Combining these two files together, then we have the cafile to verify the domain
ceritificate sent by EMQ.

    cat /etc/ssl/certs/DST_Root_CA_X3.pem /etc/letsencrypt/live/$domain/chain.pem > ca.pem

SSL Connection using the `ca.pem` .

    mosquitto_sub -t abc -h $domain -p 8883 -d  --cafile ~/ca.pem
    Client mosqsub/31415-hxxxxxxx. sending CONNECT
    Client mosqsub/31415-hxxxxxxx. received CONNACK
    Client mosqsub/31415-hxxxxxxx. sending SUBSCRIBE (Mid: 1, Topic: abc, QoS: 0)
    Client mosqsub/31415-hxxxxxxx. received SUBACK
    Subscribed (mid: 1): 0

Check the listeners on the dashboard:

![](https://cdn-images-1.medium.com/max/2000/1*Ldz4Jr5TIfCsC9AtTk_5Pg.png)

I hope you like our article. If you have any questions, please visit [EMQ X Website](https://www.emqx.com/en).


Or write to us: contact@emqx.io

