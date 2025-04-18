## HOL Blocking Issues in MQTT Communication 

In traditional solutions, all MQTT messages are sent through a single channel between the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and server. For TCP, this means using one TCP connection; for TCP/TLS, it involves a single TLS connection; and for the QUIC solution, it refers to the sole QUIC stream within a QUIC connection.

All messages are queued for sequential sending, meaning that the message at the front of the queue blocks all subsequent messages until it is transmitted. This type of blocking can cause high-priority data to be delayed if a low-priority message is at the front of the queue. Additionally, if a large message does not finish transmitting within a certain period—known as the keepalive interval—the connection may be disconnected. However, this is not the end of the story; the client can reconnect and attempt to retransmit the large message. Unfortunately, it is likely to time out again, resulting in the client getting stuck in a reconnect loop. 

In summary, head-of-line (HOL) blocking prevents important high-priority messages from reaching the intended recipient on time and can also lead to repeated reconnect attempts. This causes an unstable connection and will be hard to detect without looking into the on-wire messaging.

## The Multi-Stream Feature of MQTT over QUIC

The multi-stream feature of MQTT over QUIC in EMQX can solve the problem. Between a client and EMQX MQTT broker, there is one QUIC connection that supports multiple streams. We send different messages over these streams and assign varying priority levels to them. This allows the QUIC stack to manage the network transmission effectively, helping to mitigate the HOL blocking issue. In this way, low-priority large messages won't obstruct the transmission of smaller, more important messages.

However, there's a trade-off regarding message ordering: while message ordering is guaranteed within a single stream, it is not assured across different streams. Typically, this is not a major concern because when one message has a higher priority than another, it is generally expected that the high-priority message should take precedence. Therefore, while ordering is not critical among messages of different priorities, maintaining the correct prioritization is essential.

This blog explores how the MQTT over QUIC multi-stream feature can mitigate the HOL blocking issue, improve data exchange, and reduce disconnections. 

## The Test: How Multi-Stream Solves HOL Blocking Issue 

In order to find out how MQTT over stream multi-stream feature could help here, we designed the following tests.

### Test Overview

- **Producer:**

  It produces data for two topics, for a glance at definitions:

  ```json
  {
      "topics" : [
          {"name": "Topic1",
           "interval_ms": "100",
           "inject_timestamp" : true,
           "QoS": 1,
           "payload_encoding": "eterm",
           "payload": {"foo1" : "bar1", "timestamp": "0", "Data": "10"},
           "stream" : 0,
           "stream_priority": 200,
          },
  
          {"name": "Topic2",
           "interval_ms": "5000",
           "inject_timestamp" : "ms",
           "QoS": 1,
           "payload_encoding": "eterm",
           "payload": {"foo2" : "bar2", "timestamp": "0", "VIN" : "VIN", "Data": "%p25000"},
           "stream" : 0,
           "stream_priority": 8,
           "render": "Data",
          }
      ]
  }
  ```

  The messages for `Topic1` are **small messages under 1k that are sent 10 times per second**. These messages have a higher priority of `200`.

  The messages for `Topic2` consist of **large messages (25k pages, totaling 100 MB), sent every 5 seconds**.

  The producer operates in an area with a poor network connection, which only allows for approximately 30 IP packets per second.

- **Consumer:**

  We have one consumer only listening on the topic `Topic1,` which will be most interested to see how much gets delivered. 

  The consumer stays in a good network without any network faults or rate limitings. 

- **Test Setup:**

  Producer <---- rate limit 30 pks/sec ----> | EMQX |  <--- Good network --->  Consumer

  iptables is used to inject ratelimit:

  ```
  -N RATE_LIMIT
  -A INPUT -i veth0 -j RATE_LIMIT
  -A RATE_LIMIT -m limit --limit 29/sec -j ACCEPT
  -A RATE_LIMIT -j DROP
  ```

### Test 1:  TCP/TLS Single Stream

- **Producer Results:**

  Publishing stopped after 6s; that is when the 'big message' kicks in.

  The connection gets closed after 2 mins.

  ```shell
   ./emqtt_bench pub  --topics-payload ./topic_spec.json  -c 1     -h 192.168.200.1  -F 1000 -k 60 -S -p 8883 
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s pub total=8 rate=2.84/sec
  1s connect_succ total=1 rate=0.36/sec
  2s pub total=18 rate=10.06/sec
  3s pub total=28 rate=9.69/sec
  4s pub total=38 rate=10.25/sec
  5s pub total=48 rate=9.97/sec
  6s pub total=49 rate=1.01/sec
  client(1): EXIT for {shutdown,closed}
  2m1s pub_fail total=2 rate=0.02/sec
  
  ```

- **Consumer Results:**

  It only gets 49 messages from 'Topic1' delivered in total.

  ```shell
  ./emqtt_bench sub -c 1 -t Topic1
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s sub total=1 rate=0.98/sec
  1s connect_succ total=1 rate=0.98/sec
  13s recv total=4 rate=0.31/sec
  14s recv total=14 rate=9.95/sec
  15s recv total=24 rate=10.02/sec
  16s recv total=34 rate=9.56/sec
  17s recv total=44 rate=10.26/sec
  18s recv total=49 rate=4.98/sec
  ```

### Test 2: QUIC Single Stream

- **Producer Results:**

  Almost the same as TCP/TLS, the publishing is stopped after 6s when the 'big message' kicks in.

  **BUT**, it is NOT due to the QUIC connection being closed; rather, it stems from the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) layer's keep-alive timeout, and in this test, we have set keepalive timeout to 60s. EMQX decided to shut down the MQTT connection, and the client received an MQTT.DISCONNECT message from QUIC. There is nothing wrong with the QUIC connection itself; the real problem is the Head-of-Line (HOL) blocking that prevents the large message from being delivered in time to maintain the keep-alive deadline on the EMQX side. How sad!

  ```shell
   ./emqtt_bench pub  --topics-payload ./topic_spec.json  -c 1     -h 192.168.200.1  -F 1000 -k 60 --quic -p 14567
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s pub total=8 rate=2.53/sec
  1s connect_succ total=1 rate=0.32/sec
  2s pub total=18 rate=10.00/sec
  3s pub total=28 rate=10.00/sec
  4s pub total=37 rate=8.95/sec
  5s pub total=47 rate=10.06/sec
  6s pub total=49 rate=2.00/sec
  client(1): disconnected with reason 141: keepalive_timeout
  2m1s pub_fail total=1175 rate=9.54/sec
  ```

- **Consumer Results:**

  Same as the above tests, the consumer received 49 messages.

  ```shell
  ./emqtt_bench sub -c 1 -t Topic1
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s sub total=1 rate=0.96/sec
  1s connect_succ total=1 rate=0.96/sec
  11s recv total=6 rate=0.54/sec
  12s recv total=15 rate=9.14/sec
  13s recv total=26 rate=10.88/sec
  14s recv total=36 rate=10.04/sec
  15s recv total=46 rate=10.08/sec
  16s recv total=49 rate=2.99/sec
  ```

### Test 3: MQTT over QUIC, Multi Streams

It’s worth noting that, unlike the previous tests, we specified that `Topic1` will use `stream 1`, while `Topic2` will use `stream 2`. `stream 1` has a higher priority than `stream 2`, but the other settings remain the same. Additionally, we have a default control stream: `stream 0`, which is used for sending `MQTT.PINGREQ` messages. This stream has the highest priority and helps keep the MQTT connection alive. In the earlier QUIC single stream test, `stream 0` was the only one used and served as the default stream.

```json
{
    "topics" : [
        {"name": "Topic1",
         "interval_ms": "100",
         "inject_timestamp" : true,
         "QoS": 1,
         "payload_encoding": "eterm",
         "payload": {"foo1" : "bar1", "timestamp": "0", "Data": "10"},
         "stream" : 1,
         "stream_priority": 200,
        },

        {"name": "Topic2",
         "interval_ms": "5000",
         "inject_timestamp" : "ms",
         "QoS": 1,
         "payload_encoding": "eterm",
         "payload": {"foo2" : "bar2", "timestamp": "0", "VIN" : "VIN", "Data": "%p25000"},
         "stream" : 2,
         "stream_priority": 8,
         "render": "Data",
        }
    ]
}
```

- **Producer Results:**

  Publishing with small resistance.

  ```shell
   ./emqtt_bench pub  --topics-payload ./topic_spec.json  -c 1     -h 192.168.200.1  -F 1000 -k 60 --quic -p 14567
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s pub total=8 rate=3.08/sec
  1s connect_succ total=1 rate=0.39/sec
  2s pub total=18 rate=10.00/sec
  3s pub total=28 rate=9.99/sec
  4s pub total=38 rate=10.05/sec
  5s pub total=48 rate=9.88/sec
  6s pub total=56 rate=7.96/sec
  7s pub total=68 rate=12.12/sec
  8s pub total=78 rate=9.54/sec
  9s pub total=88 rate=10.58/sec
  10s pub total=98 rate=9.88/sec
  11s pub total=108 rate=9.79/sec
  12s pub total=118 rate=10.21/sec
  13s pub total=128 rate=10.12/sec
  14s pub total=138 rate=10.00/sec
  15s pub total=147 rate=8.81/sec
  16s pub total=156 rate=9.20/sec
  17s pub total=165 rate=8.92/sec
  18s pub total=178 rate=13.00/sec
  19s pub total=187 rate=9.08/sec
  20s pub total=198 rate=10.79/sec
  21s pub total=208 rate=9.93/sec
  22s pub total=218 rate=10.27/sec
  23s pub total=228 rate=10.00/sec
  24s pub total=237 rate=8.86/sec
  25s pub total=248 rate=11.18/sec
  26s pub total=258 rate=10.00/sec
  27s pub total=267 rate=8.69/sec
  28s pub total=278 rate=11.39/sec
  29s pub total=288 rate=9.92/sec
  30s pub total=298 rate=10.08/sec
  31s pub total=308 rate=9.61/sec
  32s pub total=317 rate=9.40/sec
  33s pub total=328 rate=10.87/sec
  34s pub total=338 rate=10.11/sec
  35s pub total=348 rate=9.76/sec
  36s pub total=358 rate=10.18/sec
  37s pub total=368 rate=10.07/sec
  38s pub total=377 rate=8.88/sec
  39s pub total=388 rate=11.09/sec
  40s pub total=398 rate=10.06/sec
  41s pub total=406 rate=8.00/sec
  42s pub total=417 rate=11.00/sec
  43s pub total=428 rate=10.92/sec
  44s pub total=436 rate=8.06/sec
  45s pub total=448 rate=11.71/sec
  46s pub total=458 rate=10.20/sec
  47s pub total=468 rate=10.02/sec
  48s pub total=477 rate=9.02/sec
  49s pub total=488 rate=10.90/sec
  50s pub total=498 rate=9.99/sec
  51s pub total=507 rate=8.69/sec
  52s pub total=518 rate=11.33/sec
  53s pub total=526 rate=8.12/sec
  54s pub total=538 rate=11.58/sec
  55s pub total=548 rate=10.35/sec
  56s pub total=556 rate=7.89/sec
  57s pub total=568 rate=12.21/sec
  58s pub total=578 rate=9.94/sec
  59s pub total=587 rate=8.76/sec
  1m0s pub total=598 rate=11.34/sec
  1m1s pub total=607 rate=8.97/sec
  1m2s pub total=617 rate=10.08/sec
  1m3s pub total=627 rate=9.88/sec
  1m4s pub total=636 rate=9.09/sec
  1m5s pub total=648 rate=11.73/sec
  1m6s pub total=658 rate=10.20/sec
  1m7s pub total=667 rate=9.04/sec
  1m8s pub total=678 rate=11.01/sec
  1m9s pub total=687 rate=9.00/sec
  1m10s pub total=696 rate=8.87/sec
  1m11s pub total=708 rate=11.92/sec
  1m12s pub total=718 rate=10.22/sec
  1m13s pub total=728 rate=9.81/sec
  1m14s pub total=738 rate=10.19/sec
  1m15s pub total=748 rate=9.88/sec
  1m16s pub total=758 rate=10.01/sec
  1m17s pub total=768 rate=9.91/sec
  1m18s pub total=777 rate=9.15/sec
  1m19s pub total=788 rate=10.97/sec
  1m20s pub total=798 rate=9.98/sec
  1m21s pub total=807 rate=9.08/sec
  1m22s pub total=818 rate=11.00/sec
  1m23s pub total=828 rate=10.00/sec
  1m24s pub total=836 rate=8.00/sec
  1m25s pub total=847 rate=10.89/sec
  1m26s pub total=857 rate=10.04/sec
  1m27s pub total=864 rate=6.86/sec
  1m28s pub total=878 rate=13.93/sec
  1m29s pub total=888 rate=9.96/sec
  1m30s pub total=897 rate=9.31/sec
  1m31s pub total=907 rate=10.00/sec
  1m32s pub total=917 rate=9.78/sec
  1m33s pub total=928 rate=10.99/sec
  1m34s pub total=938 rate=10.16/sec
  1m35s pub total=947 rate=8.87/sec
  1m36s pub total=957 rate=10.27/sec
  1m37s pub total=967 rate=9.96/sec
  1m38s pub total=978 rate=11.02/sec
  1m39s pub total=988 rate=9.94/sec
  1m40s pub total=998 rate=9.43/sec
  1m41s pub total=1008 rate=10.70/sec
  1m42s pub total=1016 rate=8.00/sec
  1m43s pub total=1028 rate=11.85/sec
  1m44s pub total=1038 rate=10.16/sec
  1m45s pub total=1048 rate=9.92/sec
  1m46s pub total=1056 rate=7.87/sec
  1m47s pub total=1067 rate=11.25/sec
  1m48s pub total=1077 rate=9.81/sec
  1m49s pub total=1088 rate=10.87/sec
  1m50s pub total=1098 rate=10.35/sec
  1m51s pub total=1108 rate=9.62/sec
  1m52s pub total=1118 rate=10.32/sec
  1m53s pub total=1128 rate=10.06/sec
  1m54s pub total=1137 rate=9.03/sec
  1m55s pub total=1148 rate=10.95/sec
  1m56s pub total=1157 rate=8.97/sec
  1m57s pub total=1168 rate=10.92/sec
  1m58s pub total=1178 rate=10.14/sec
  1m59s pub total=1188 rate=9.98/sec
  2m0s pub total=1198 rate=9.54/sec
  2m1s pub total=1207 rate=9.32/sec
  2m2s pub total=1218 rate=11.19/sec
  2m3s pub total=1228 rate=9.91/sec
  2m4s pub total=1237 rate=9.08/sec
  2m5s pub total=1246 rate=9.00/sec
  2m6s pub total=1257 rate=10.89/sec
  2m7s pub total=1268 rate=10.78/sec
  2m8s pub total=1277 rate=9.20/sec
  2m9s pub total=1288 rate=10.97/sec
  2m10s pub total=1298 rate=10.02/sec
  2m11s pub total=1308 rate=10.09/sec
  2m12s pub total=1318 rate=9.86/sec
  2m13s pub total=1328 rate=10.14/sec
  2m14s pub total=1338 rate=10.00/sec
  2m15s pub total=1347 rate=8.96/sec
  2m16s pub total=1357 rate=10.02/sec
  2m17s pub total=1368 rate=10.87/sec
  2m18s pub total=1375 rate=7.11/sec
  2m19s pub total=1388 rate=12.97/sec
  2m20s pub total=1398 rate=9.83/sec
  2m21s pub total=1408 rate=9.58/sec
  2m22s pub total=1417 rate=9.48/sec
  2m23s pub total=1428 rate=11.13/sec
  2m24s pub total=1438 rate=10.00/sec
  2m25s pub total=1448 rate=9.73/sec
  2m26s pub total=1458 rate=10.21/sec
  2m27s pub total=1468 rate=9.86/sec
  2m28s pub total=1477 rate=9.00/sec
  2m29s pub total=1488 rate=11.22/sec
  ```

- **Consumer Results:**

  The consumer should be happy this time.

  ```shell
  ./emqtt_bench sub -c 1 -t Topic1
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s sub total=1 rate=0.98/sec
  1s connect_succ total=1 rate=0.98/sec
  15s recv total=6 rate=0.40/sec
  16s recv total=15 rate=8.95/sec
  17s recv total=25 rate=10.00/sec
  18s recv total=35 rate=10.06/sec
  19s recv total=45 rate=9.99/sec
  20s recv total=54 rate=8.99/sec
  21s recv total=65 rate=10.77/sec
  22s recv total=75 rate=9.89/sec
  23s recv total=85 rate=10.22/sec
  24s recv total=95 rate=10.12/sec
  25s recv total=105 rate=10.00/sec
  26s recv total=114 rate=9.00/sec
  27s recv total=125 rate=10.50/sec
  28s recv total=135 rate=10.42/sec
  29s recv total=145 rate=10.01/sec
  30s recv total=154 rate=9.06/sec
  31s recv total=165 rate=10.86/sec
  32s recv total=175 rate=9.78/sec
  33s recv total=185 rate=10.34/sec
  34s recv total=194 rate=8.98/sec
  35s recv total=204 rate=9.99/sec
  36s recv total=215 rate=11.03/sec
  37s recv total=224 rate=8.96/sec
  38s recv total=233 rate=8.93/sec
  39s recv total=244 rate=11.07/sec
  40s recv total=255 rate=11.00/sec
  41s recv total=265 rate=9.86/sec
  42s recv total=275 rate=10.21/sec
  43s recv total=284 rate=9.00/sec
  44s recv total=295 rate=11.01/sec
  45s recv total=303 rate=7.80/sec
  46s recv total=315 rate=12.06/sec
  47s recv total=325 rate=10.15/sec
  48s recv total=334 rate=9.04/sec
  49s recv total=345 rate=10.99/sec
  50s recv total=355 rate=10.03/sec
  51s recv total=365 rate=9.99/sec
  52s recv total=375 rate=9.97/sec
  53s recv total=385 rate=10.04/sec
  54s recv total=395 rate=10.00/sec
  55s recv total=405 rate=10.00/sec
  56s recv total=415 rate=9.94/sec
  57s recv total=425 rate=10.05/sec
  58s recv total=434 rate=8.90/sec
  59s recv total=445 rate=11.01/sec
  1m0s recv total=455 rate=10.00/sec
  1m1s recv total=465 rate=9.99/sec
  1m2s recv total=475 rate=10.12/sec
  1m3s recv total=485 rate=10.00/sec
  1m4s recv total=494 rate=9.00/sec
  1m5s recv total=505 rate=11.00/sec
  1m6s recv total=515 rate=9.93/sec
  1m7s recv total=525 rate=10.03/sec
  1m8s recv total=535 rate=10.00/sec
  1m9s recv total=545 rate=10.00/sec
  1m10s recv total=555 rate=9.88/sec
  1m11s recv total=565 rate=10.16/sec
  1m12s recv total=575 rate=9.67/sec
  1m13s recv total=585 rate=10.04/sec
  1m14s recv total=594 rate=9.20/sec
  1m15s recv total=604 rate=9.88/sec
  1m16s recv total=615 rate=11.20/sec
  1m17s recv total=625 rate=9.98/sec
  1m18s recv total=635 rate=10.04/sec
  1m19s recv total=645 rate=9.95/sec
  1m20s recv total=655 rate=9.95/sec
  1m21s recv total=663 rate=8.08/sec
  1m22s recv total=675 rate=11.90/sec
  1m23s recv total=684 rate=9.06/sec
  1m24s recv total=694 rate=9.96/sec
  1m25s recv total=704 rate=10.05/sec
  1m26s recv total=715 rate=10.85/sec
  1m27s recv total=725 rate=10.07/sec
  1m28s recv total=735 rate=10.02/sec
  1m29s recv total=745 rate=10.02/sec
  1m30s recv total=754 rate=8.96/sec
  1m31s recv total=765 rate=10.92/sec
  1m32s recv total=775 rate=10.15/sec
  1m33s recv total=785 rate=9.92/sec
  1m34s recv total=795 rate=9.93/sec
  1m35s recv total=805 rate=9.88/sec
  1m36s recv total=814 rate=9.07/sec
  1m37s recv total=823 rate=9.08/sec
  1m38s recv total=835 rate=12.11/sec
  1m39s recv total=843 rate=8.01/sec
  1m40s recv total=855 rate=12.00/sec
  1m41s recv total=864 rate=8.88/sec
  1m42s recv total=875 rate=11.06/sec
  1m43s recv total=885 rate=10.06/sec
  1m44s recv total=895 rate=9.85/sec
  1m45s recv total=905 rate=10.14/sec
  1m46s recv total=915 rate=9.67/sec
  1m47s recv total=925 rate=10.38/sec
  1m48s recv total=935 rate=9.99/sec
  1m49s recv total=945 rate=9.94/sec
  1m50s recv total=955 rate=9.75/sec
  1m51s recv total=965 rate=10.34/sec
  1m52s recv total=974 rate=8.98/sec
  1m53s recv total=985 rate=10.97/sec
  1m54s recv total=995 rate=10.04/sec
  1m55s recv total=1005 rate=10.01/sec
  1m56s recv total=1014 rate=8.96/sec
  1m57s recv total=1025 rate=10.82/sec
  1m58s recv total=1035 rate=10.17/sec
  1m59s recv total=1045 rate=9.87/sec
  2m0s recv total=1055 rate=10.18/sec
  2m1s recv total=1065 rate=9.60/sec
  2m2s recv total=1075 rate=10.44/sec
  2m3s recv total=1085 rate=9.92/sec
  2m4s recv total=1095 rate=10.01/sec
  2m5s recv total=1105 rate=10.03/sec
  2m6s recv total=1115 rate=9.95/sec
  2m7s recv total=1125 rate=10.09/sec
  2m8s recv total=1135 rate=9.90/sec
  2m9s recv total=1144 rate=8.96/sec
  2m10s recv total=1155 rate=10.98/sec
  2m11s recv total=1165 rate=10.11/sec
  2m12s recv total=1175 rate=10.01/sec
  2m13s recv total=1185 rate=9.95/sec
  2m14s recv total=1195 rate=10.02/sec
  2m15s recv total=1205 rate=10.07/sec
  2m16s recv total=1215 rate=10.00/sec
  2m17s recv total=1223 rate=7.96/sec
  2m18s recv total=1235 rate=11.80/sec
  2m19s recv total=1245 rate=10.21/sec
  2m20s recv total=1254 rate=8.74/sec
  2m21s recv total=1264 rate=10.29/sec
  2m22s recv total=1275 rate=11.02/sec
  2m23s recv total=1285 rate=10.01/sec
  2m24s recv total=1295 rate=9.92/sec
  2m25s recv total=1305 rate=10.02/sec
  2m26s recv total=1315 rate=10.06/sec
  2m27s recv total=1324 rate=9.00/sec
  2m28s recv total=1335 rate=10.92/sec
  2m29s recv total=1345 rate=10.01/sec
  2m30s recv total=1355 rate=10.05/sec
  2m31s recv total=1365 rate=9.98/sec
  2m32s recv total=1374 rate=9.01/sec
  2m33s recv total=1384 rate=10.01/sec
  2m34s recv total=1395 rate=11.01/sec
  2m35s recv total=1404 rate=9.00/sec
  2m36s recv total=1415 rate=11.00/sec
  2m37s recv total=1424 rate=8.98/sec
  2m38s recv total=1433 rate=9.01/sec
  2m39s recv total=1444 rate=10.81/sec
  2m40s recv total=1455 rate=11.21/sec
  2m41s recv total=1464 rate=8.85/sec
  2m42s recv total=1475 rate=11.13/sec
  2m43s recv total=1485 rate=9.98/sec
  2m44s recv total=1495 rate=10.07/sec
  ```

### Test 4: Raw TCP for Curious Readers

- **Producer:**

  ```shell
  ./emqtt_bench pub  --topics-payload ./topic_spec.json  -c 1     -h 192.168.200.1  -F 1000 -k 60 
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s pub total=9 rate=4.48/sec
  1s connect_succ total=1 rate=0.50/sec
  2s pub total=19 rate=9.97/sec
  3s pub total=29 rate=10.04/sec
  4s pub total=39 rate=10.05/sec
  5s pub total=49 rate=9.16/sec
  client(1): EXIT for {shutdown,closed}
  2m1s pub_fail total=2 rate=0.02/sec
  ```

- **Consumer:**

  ```shell
   ./emqtt_bench sub -c 1 -t Topic1
  Start with 6 workers, addrs pool size: 1 and req interval: 60 ms 
  
  1s sub total=1 rate=0.98/sec
  1s connect_succ total=1 rate=0.98/sec
  23s recv total=2 rate=0.09/sec
  24s recv total=11 rate=9.33/sec
  25s recv total=22 rate=10.95/sec
  26s recv total=32 rate=10.09/sec
  27s recv total=42 rate=9.95/sec
  28s recv total=49 rate=7.06/sec
  ```

## Last Word

Impressive right? 

You may ask why `Topic1` doesn’t look like gets blocked at all in multi-stream tests, and what happed to the `Topic2` messages? How does QUIC balance these? This is all about how QUIC packages data from different streams, A QUIC packet could contain the data of stream 1, the data of stream 2, or BOTH!  We will dig into that with the help of Wireshark trace and explain in the next blog post. Stay Tuned!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
