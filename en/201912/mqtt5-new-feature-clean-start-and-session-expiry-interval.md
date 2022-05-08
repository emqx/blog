### Foreword

Clean Start and Session Expiry Interval in MQTT V5.0 are not unfamiliar to those who have experience in using MQTT v3.1.1 protocol. These two fields are very similar to Clean Session in previous versions. However, they are much more flexible than the Clean Session in practice. The functions and differences of these fields will be described in detail below.

### Clean Session in MQTT v3.1.1

> If Clean Session is set to 0, the server must use the session associated with the Client ID to resume communication with the client. If there is no such session, the server must create a new session. The state of the session after disconnecting must be stored by  the client and server.


> If Clean Session is set to 1, the client and server must discard any previous session and create a new session. The life cycle of the session will be consistent with the network connection, and its session state must not be reused by any subsequent session.

![1.png](https://static.emqx.net/images/a30fd96ea411321fc7095f5c96180230.png)

As can be seen, it is expected by MQTT to avoid the loss of messages after the client disconnects and reconnects through this mechanism of persistent session, and to avoid the repeated subscription process after the client connects. This function is very useful in Iot scenarios with small bandwidth and unstable network. However, the Clean Session also limits the behavior of the client and server in both the connection and disconnection states, which is not a good implementation. In addition, in some scenarios, when the session does not require the server to keep its state permanently, this mechanism will lead to a waste of server resources.

### Clean Start and Session Expiry Interval in MQTT v5.0

> If the Clean Start in the CONNECT packet is 1, the client and server **must** discard any existing sessions and start a new session.
>
> If the Clean Start in the CONNECT packet is 0 and there is a session associated with this client ID, the server **must** resume communication with the client based on the state of the session. If there is no session associated with this client ID, the server **must** create a new session.


> Session Expiry Interval is in seconds. If Session Expiry Interval is set to 0 or not specified, the session will end when the network connection is closed.
>
> If the Session Expiry Interval is 0xFFFFFFFF, the session never expires.
>
> If the Session Expiry Interval is greater than 0 when the network connection closes (the Session Expiry Interval in DISCONNECT packet may override the setting in the CONNECT packet), the client and server **must** store the Session state.

![image20190909181321466.png](https://static.emqx.net/images/86191a805c34b82d0de14c063ec97b1c.png)

Clean Start now replaces the original Clean Session, but is no longer used to indicate whether to store session state. It is only used to indicate whether the server should attempt to restore a previous session or create a new session directly when connecting. The storage duration of the session state on the server is completely decided by Session Expiry Interval.

As mentioned earlier, MQTT v5.0 allows clients to reassign the Seesion Expiry Interval when disconnected. In this way, we can easily satisfy the scenario that the session state is reserved by the server when the client network is abnormally disconnected, and the session is terminated when the client is offline normally, just by setting the Session Expiry Interval to 0 when the client disconnects. Even for a session that never expires, the client can change by setting Clean Start to 1 in the next connection.

Clean Start and Session Expiry Interval not only solve the legacy problems of Clean Session, but also extend the usage scenarios of the client, making the [MQTT protocol](https://www.emqx.com/en/mqtt) more practical in a limited network environment.

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.io) for details.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
