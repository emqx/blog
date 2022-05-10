In recent years, with the rapid development of the Web front-end, new features of browsers are constantly emerging, more and more applications can be implemented on the browser side through the browser rendering engine. WebSocket, the instant communication method for Web applications, is also widely used.

WebSocket is a computer communications protocol, providing full-duplex communication channels over a single TCP connection. The WebSocket protocol was standardized by the IETF as RFC 6455 in 2011, and the WebSocket API in Web IDL is being standardized by the W3C. [^1]

[Chapter 6 of MQTT protocol](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718127) specifies the conditions the MQTT need to meet for transferring over the WebSocket [RFC6455] connection, and is not discussed in detail here.



## Comparison of two clients

### Paho.mqtt.js

[Paho](https://www.eclipse.org/paho/) is an MQTT client project from Eclipse, and the Paho JavaScript Client is one of the browser-based libraries that uses WebSockets to connect to the MQTT server. Compared to another JavaScript connection library, it has fewer features and is not recommended.

### MQTT.js

[MQTT.js](https://github.com/mqttjs/MQTT.js) is a fully open-source client-side library for the MQTT protocol, written in JavaScript and available for Node.js and browsers. On the Node.js side, it can be installed via global installation and connected via the command line. Also, it supports MQTT/TCP, MQTT/TLS, MQTT/WebSocket connections. It is worth mentioning that MQTT.js also has good support for WeChat Mini Program.

This article will use the MQTT.js library to explain WebSocket connections.



## Install MQTT.js

If you have the Node.js runtime environment on your machine, you can install MQTT.js directly using the npm command.

### Install in the current directory

```shell
npm install mqtt --save
```

### CDN references

Or use CDN addresses directly without installation

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
    // Globally initializes an mqtt variable
    console.log(mqtt)
</script>
```



## Connect to the MQTT broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service was created based on the EMQX [MQTT IoT cloud platform](https://www.emqx.com/en/cloud). The information about broker access is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

> EMQX uses port 8083 for normal connections and 8084 for WebSocket over TLS.

For simplicity, let's put the subscriber and the publisher in the same file.

```javascript
const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'ws://broker.emqx.io:8083/mqtt'

const options = {
  keepalive: 60,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  },
}

console.log('Connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})

client.on('reconnect', () => {
  console.log('Reconnecting...')
})
```

### Connection address

The link address demonstrated above can be split into:  `ws:` // `broker` . `emqx.io` : `8083` `/mqtt`

That is `protocol` // `host name` . `domain` : `port` / `path`

Beginners are likely to make the following mistakes.

- The connection address does not specify a protocol: WebSocket is a communication protocol that uses `ws` (non-encrypted), `wss` (SSL encrypted) as its protocol identifier. the MQTT.js client supports multiple protocols and the connection address needs to specify the protocol type.
- The connection address does not specify a port: MQTT does not specify a port for WebSocket access, and EMQX uses `8083` and `8084` as the default ports for unencrypted and encrypted connections respectively. The default port of WebSocket protocol is the same as HTTP (80/443), no port means WebSocket uses the default port to connect. On the other hand, no need to specify a port when using a standard MQTT connection. For example, MQTT.js can use `mqtt://localhost` on the Node.js side to connect to the standard MQTT 1883 port, and when the connection address is `mqtts://localhost`, it will be connected to 8884 port.
- Connection address without path: MQTT-WebSoket uniformly uses `/path` as the connection path, which should be specified when connecting, and the path used on EMQX is `/mqtt`.
- The protocol does not match the port: use `wss` connection, but connect to port `8083`.
- The use of unencrypted WebSocket connections under HTTPS: organizations such as Google are pushing HTTPS while also limiting security through browser constraints, i.e., the use of the unencrypted `ws` protocol to initiate connection requests is automatically prohibited by the browser under HTTPS connections.
- The certificate does not match the connection address: lengthy, see below for details **Enable SSL/TLS for EMQX**.

### Connection options

In the code above, `options` is the client connection options. The following are the description of the main parameters, the rest of the parameters see [https://github.com/mqttjs/MQTT.js#client](https://github.com/mqttjs/MQTT.js#client).

- keepalive: heartbeat time, default 60 seconds, set 0 to disabled.
- clientId: client ID which is randomly generated by`'mqttjs_' + Math.random().toString(16).substr(2, 8)` by default.
- username: connection username (optional)
- password: connection password (optional)
- clean: true, set to false to receive QoS 1 and 2 messages while offline.
- reconnectPeriod: default 1000 milliseconds, the interval between reconnections, client ID duplicates, authentication failures, etc. Client will reconnect.
- connectTimeout: default 30 * 1000 milliseconds, the time to wait before CONNACK is received, i.e. the connection timeout time.
- will: will message, the message that the Broker will send automatically when a client is severely disconnected. The general format is:
  - topic: the topic to be published
  - payload: the message to be published
  - qos: QoS
  - retain: retain sign

### Subscribe/unsubscribe

Subscriptions can only be made after a successful connection and the subscribed topics must comply with MQTT subscription topic rules.

Note: JavaScript JavaScript's asynchronous non-blocking feature ensures a successful connection only after the connect event, or by using `client.connected` to determine if the connection was successful.

```javascript
client.on('connect', () => {
  console.log('Client connected:' + clientId)
  // Subscribe
  client.subscribe('testtopic', { qos: 0 })
})
```

```javascript
// Unsubscribe
client.unubscribe('testtopic', () => {
  console.log('Unsubscribed')
})
```

### Publish/receive messages

Publish messages to certain topics. The published topic has to meet the rule of MQTT publish topic. Otherwise, it will disconnect. No need to subscribe to this topic before publishing, but have to ensure that the client has already successfully connected.

```javascript
// Publish
client.publish('testtopic', 'ws connection demo...!', { qos: 0, retain: false })
```

```javascript
// Received
client.on('message', (topic, message, packet) => {
  console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
})
```

### WeChat Mini Program

The MQTT.js library uses `wxs` protocol identifier to specially process the WeChat Mini Program. Note: The applet development specification requires that an encrypted connection must be used, and the connection address should be similar to `wxs://broker.emqx.io:8084/mqtt`.



## Enable SSL/TLS for EMQX

EMQ built-in self-signed certificate, encrypted WebSocket connection has been started by default, but most browsers will report invalid certificate errors such as `net::ERR_CERT_COMMON_NAME_INVALID` (Chrome, 360 and other WebKit kernel browsers in developer mode. Console tab can be used to see most connection errors). The reason for this error is that the browser cannot verify the validity of the self-signed certificate. The reader needs to purchase a trusted certificate from a certificate authority and refer to the corresponding section in this article for configuration actions: [Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide).

The conditions required to enable SSL/TLS certificates are summarized here:

- Bind the domain name to the public address of the MQTT broker: the certificate issued by the CA authority is signed for the domain name.
- Apply for a certificate: apply for a certificate for the domain name used with a CA authority, taking care to choose a reliable CA authority and that the certificate distinguishes between a generic domain name and a hostname.
- Select the `wss` protocol when using an encrypted connection, and **use the domain name to connect**: after binding the domain name - certification, must using the domain name to connect instead of the IP address, so that the browser will check the certification according to the domain name to establish a connection after it has passed the check.

### EMQX configuration

Open the `etc/emqx.conf` configuration file and modify the following configurations:

```shell
# wss listening address
listener.wss.external = 8084

# Modify key file address
listener.wss.external.keyfile = etc/certs/cert.key

# Modify certificate file address
listener.wss.external.certfile = etc/certs/cert.pem
```

Restart EMQX after completion.

> You can use your certificate and key files to replace them directly under etc/certs/.

### Configuring reverse proxies and certificates on Nginx

Using Nginx to reverse proxy and encrypt WebSocket can reduce the computation burden of the EMQX broker and implement domain name multiplexing at the same time. Nginx [load balancing](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing) also allows you to distribute multiple back-end service entities.

```shell
# It is recommended that WebSocket also bind to port 443.
listen 443, 8084;
server_name example.com;

ssl on;

ssl_certificate /etc/cert.crt;  # certificate path
ssl_certificate_key /etc/cert.key; # key path


# upstream server list
upstream emq_server {
    server 10.10.1.1:8883 weight=1;
    server 10.10.1.2:8883 weight=1;
    server 10.10.1.3:8883 weight=1;
}

# Common website application
location / {
    root www;
    index index.html;
}

# Reverse proxy to EMQX unencrypted WebSocket
location / {
    proxy_redirect off;
    # upstream
    proxy_pass http://emq_server;
    
    proxy_set_header Host $host;
    # Reverse proxy retains client address
    proxy_set_header X-Real_IP $remote_addr;
    proxy_set_header X-Forwarded-For $remote_addr:$remote_port;
    # WebSocket extra request header
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection “upgrade”;
}
```



## Other resources

The complete project code: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-WebSocket](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-WebSocket)

An online MQTT WebSocket toolkit: [https://www.emqx.com/en/mqtt/mqtt-websocket-toolkit](https://www.emqx.com/en/mqtt/mqtt-websocket-toolkit)





[^1]: https://en.wikipedia.org/wiki/WebSocket


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
