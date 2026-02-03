## Introduction

curl is the ubiquitous command-line tool for transferring data, and since 2020, it speaks MQTT. With curl ≥8.19.0 (shipping early March 2026), you can now also use **MQTTS** (MQTT over TLS) for secure IoT communication directly from your terminal. This means developers can test, script, and automate MQTT workflows without installing dedicated client libraries.

This guide shows you how to connect, publish, and subscribe to an [MQTT Broker](https://www.emqx.com/en/products/emqx) using nothing but curl.

## Why Use curl for MQTT?

- **Zero Dependencies**: No Python, Node.js, or dedicated MQTT libraries required, just curl.  
- **Universal Availability:** Pre-installed on most Linux/macOS systems; easily added to Windows and containers. 
- **Scriptable:** Easily integrate into shell scripts for prototyping and testing. 
- **TLS Support (8.19.0+):**  Secure connections via `mqtts://` for production-grade testing.         
- **Familiar Syntax:** If you know HTTP with curl, MQTT feels natural. 

## Prerequisites

### curl Version Requirements

| **Feature**        | **Minimum Version** | **Release Date** |
| :----------------- | :------------------ | :--------------- |
| MQTT (`mqtt://`)   | 7.70.0              | April 2020       |
| MQTTS (`mqtts://`) | 8.19.0              | Early March 2026 |

Check your installed version:

```
curl --version
```

Look for `mqtt` (and `mqtts` in 8.19.0+) in the **Protocols** line:

```shell
curl 8.19.0-DEV (aarch64-apple-darwin25.2.0) libcurl/8.19.0-DEV OpenSSL/3.6.0 zlib/1.2.12 brotli/1.2.0 zstd/1.5.7 AppleIDN libssh2/1.11.1 nghttp2/1.68.0 ngtcp2/1.20.0 nghttp3/1.15.0 librtmp/2.3 mit-krb5/1.7-prerelease OpenLDAP/2.4.28/Apple
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt mqtts pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AppleSecTrust AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```

> **Note:** If your version is older, upgrade via your package manager or download from [curl.se/download](https://curl.se/download.html). On macOS, use `brew install curl` for the latest version.

### MQTT Broker Setup

You need an MQTT broker to connect to. This guide uses EMQX, the world's most scalable MQTT platform.

**Option 1: Free Public Broker (Testing)**

| **Parameter**  | **Value**        |
| :------------- | :--------------- |
| Broker Address | `broker.emqx.io` |
| TCP Port       | `1883`           |
| TLS Port       | `8883`           |

**Option 2: EMQX Serverless (Production)**

For production workloads with authentication, dedicated resources, and enterprise features, try [EMQX Serverless](https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/).

## Understanding curl's MQTT URL Scheme

curl uses a URL-based syntax for MQTT operations:

```
mqtt[s]://[user:password@]broker[:port]/topic
```

| **Component**   | **Description**                                              | **Example**              |
| :-------------- | :----------------------------------------------------------- | :----------------------- |
| `mqtt://`       | Unencrypted MQTT connection (default port 1883)              | `mqtt://broker.emqx.io`  |
| `mqtts://`      | TLS-encrypted MQTT connection (default port 8883, curl ≥8.19.0) | `mqtts://broker.emqx.io` |
| `user:password` | Optional authentication credentials                          | `admin:secret@`          |
| `broker`        | Broker hostname                                              | `broker.emqx.io`         |
| `:port`         | Optional port override                                       | `:1883`, `:8883`         |
| `/topic`        | MQTT topic for publish/subscribe                             | `/sensor/temperature`    |

The port is optional; curl uses the standard default ports (1883 for `mqtt://`, 8883 for `mqtts://`). You can override them if your broker uses non-standard ports.

### curl's MQTT Output Format

When subscribing, curl outputs received MQTT messages in a binary format:

```
[2 bytes: topic length (big-endian)] [topic string] [payload]
```

For example, a message "hello" on topic "curl/test" appears as:

```
00 09 c u r l / t e s t h e l l o
└─┬─┘ └───────┬───────┘ └───┬───┘
  │           │             │
  │           │             └── payload (no length prefix)
  │           └── topic: "curl/test" (9 bytes)
  └── topic length: 9 (0x0009)
```

Raw output looks like this (topic and payload concatenated):

```
curl/testhello
```

See [Parsing MQTT Messages](https://emqx.atlassian.net/wiki/spaces/~630c7c543778a7aadf18038b/blog/2026/01/23/2369093659/Using+curl+for+MQTT+Connect+Publish+and+Subscribe+with+Secure+IoT+Communication#parsing-mqtt-messages-for-human-readable-output) below for how to make this human-readable.

## Step 1: Subscribe to an MQTT Topic

Subscribing with curl keeps the connection open and outputs incoming messages to stdout.

### Basic Subscription (Unencrypted)

```
# Subscribe to the "curl/test" topic on the public EMQX broker
curl -N mqtt://broker.emqx.io/curl/test
```

The `-N` flag disables output buffering, ensuring messages appear immediately as they arrive. Without it, curl buffers the output and you won't see anything until the buffer fills or the connection closes.

### Secure Subscription with MQTTS (curl ≥8.19.0)

```
# Subscribe over TLS
curl -N mqtts://broker.emqx.io/curl/test
```

### Subscription with Authentication

When connecting to a broker that requires credentials (like EMQX Serverless):

```
# Replace with your actual credentials
curl -N -u "your-username:your-password" mqtts://your-broker.emqxsl.com/curl/test
```

### Parsing MQTT Messages for Human-Readable Output

To display messages in a readable format, pipe curl's output through a parser.

**Bash one-liner:**

```shell
curl -sN mqtt://broker.emqx.io/curl/test | \
  while IFS= read -r -d $'\0' d; \
    do \
      [ -n "$d" ] && \
        l=$(printf "%d" "'${d:0:1}") && \
        echo "[${d:1:$l}] ${d:1+$l}"; \
    done
```

This splits on null bytes (the first byte of the 2-byte topic length for topics under 256 characters), extracts the topic length from the second byte, and prints `[topic] payload` for each message.

**Save to file and inspect:**

```shell
# Save raw output to file (Ctrl+C to stop)
curl -sN mqtt://broker.emqx.io/curl/test > messages.bin

# View with hexdump to see the structure
hexdump -C messages.bin
```

**As a reusable shell function:**

```shell
mqtt_subscribe() {
  curl -sN "$1" | while IFS= read -r -d $'\0' d; do
    [ -n "$d" ] && l=$(printf "%d" "'${d:0:1}") && echo "[${d:1:$l}] ${d:1+$l}"
  done
}

# Usage
mqtt_subscribe "mqtt://broker.emqx.io/curl/test"
```

> **Note:** For production use or complex parsing needs, consider [MQTTX CLI](https://mqttx.app/cli) which provides properly formatted output and full MQTT 5.0 support.

## Step 2: Publish a Message to an MQTT Topic

To publish, use curl's `-d` (data) flag with the message payload.

### Basic Publish (Unencrypted)

```shell
# Publish "Hello from curl" to the "curl/test" topic
curl -v -d "Hello from curl" mqtt://broker.emqx.io/curl/test
```

### Secure Publish with MQTTS (curl ≥8.19.0)

```shell
# Publish over TLS
curl -v -d "Secure message from curl" mqtts://broker.emqx.io/curl/test
```

### Publishing JSON Payloads

For IoT sensor data, JSON is a common format:

```shell
# Publish a JSON temperature reading
curl -v -d '{"sensor_id": "temp-001", "value": 23.5, "unit": "celsius"}' \
  mqtt://broker.emqx.io/sensors/temperature
```

### Publishing with Authentication

```shell
curl -v -u "your-username:your-password" \
  -d '{"status": "online", "timestamp": 1706000000}' \
  mqtts://your-broker.emqxsl.com/devices/status
```

> **Tip:** To test the full pub/sub flow, open two terminal windows side by side. Run a subscribe command (Step 1) in one terminal, then publish messages (Step 2) from the other terminal.

## Relevant curl Options

| **Option**     | **Description**                                   | **Example**                  |
| :------------- | :------------------------------------------------ | :--------------------------- |
| `-N`           | Disable output buffering (required for subscribe) | `-N`                         |
| `-d "payload"` | Message data to publish                           | `-d "sensor reading"`        |
| `-u user:pass` | Username and password for broker authentication   | `-u admin:secret`            |
| `-s`           | Silent mode (suppress progress meter)             | `-s`                         |
| `-v`           | Verbose output (shows MQTT handshake)             | `-v`                         |
| `--output -`   | Write output to stdout (useful for subscribe)     | `--output -`                 |
| `--cacert`     | CA certificate for TLS verification               | `--cacert /path/to/ca.crt`   |
| `--cert`       | Client certificate for mTLS                       | `--cert /path/to/client.crt` |
| `--key`        | Client private key for mTLS                       | `--key /path/to/client.key`  |
| `-k`           | Skip TLS certificate verification (testing only!) | `-k`                         |

### TLS Certificate Verification (curl ≥8.19.0)

For production MQTTS connections with custom certificates:

```shell
# With CA certificate verification
curl --cacert /etc/ssl/certs/emqx-ca.crt \
  -d "Verified secure message" \
  mqtts://your-broker.emqxsl.com/secure/topic

# With mutual TLS (mTLS) client authentication
curl --cacert /etc/ssl/certs/ca.crt \
  --cert /etc/ssl/certs/client.crt \
  --key /etc/ssl/private/client.key \
  -d "mTLS authenticated message" \
  mqtts://your-broker.emqxsl.com/secure/topic
```

## Use Cases: When to Use curl for MQTT

### 1. Broker Connectivity Testing

Verify your MQTT broker is reachable (DNS resolution, TCP connection) using verbose mode:

```shell
curl -v mqtt://broker.emqx.io/test
```

Example output showing successful connection:

```shell
curl -v mqtt://broker.emqx.io:1883/curl/test
* Host broker.emqx.io:1883 was resolved.
* IPv6: (none)
* IPv4: 34.243.217.54, 35.172.255.228, 44.232.241.40
*   Trying 34.243.217.54:1883...
* Connected to broker.emqx.io (34.243.217.54) port 1883
* Using client id 'curlblZBtS6c'
> MQTT<
       curlblZBtS6cmqtt_doing: state [0]
```

This verifies network connectivity and DNS resolution. Note that curl only supports QoS 0 (fire-and-forget), so a successful publish does not guarantee the message was received by subscribers.

### 2. Shell Scripting for IoT Prototyping

Simulate a temperature sensor publishing readings every 5 seconds:

```shell
#!/bin/bash
# simulate-sensor.sh

BROKER="mqtt://broker.emqx.io"
TOPIC="sensors/room1/temperature"

while true; do
  # Generate random temperature between 20-30°C
  TEMP=$(awk -v min=20 -v max=30 'BEGIN{srand(); print min+rand()*(max-min)}')
  PAYLOAD="{\"temperature\": $TEMP, \"timestamp\": $(date +%s)}"
  
  curl -s -d "$PAYLOAD" "$BROKER/$TOPIC"
  echo "Published: $PAYLOAD"
  
  sleep 5
done
```

This is useful for prototyping and testing subscriber applications. For production workloads requiring delivery guarantees, use a client that supports QoS 1 or 2.

## Limitations of curl for MQTT

While curl is excellent for quick tests and scripting, be aware of these limitations:

| **Limitation**             | **Description**                                              | **Alternative**                                    |
| :------------------------- | :----------------------------------------------------------- | :------------------------------------------------- |
| **Binary Output**          | Subscribe output is raw binary (topic-length prefix + topic + payload) | Pipe through parser script or use MQTTX CLI        |
| **QoS 0 Only**             | curl only supports QoS 0 (fire-and-forget)                   | Use [MQTTX CLI](https://mqttx.app/cli) for QoS 1/2 |
| **No Wildcards**           | Cannot subscribe to wildcard topics (`+`, `#`)               | Use dedicated MQTT clients                         |
| **Single Topic**           | One topic per command invocation                             | Script multiple curl calls                         |
| **No Persistent Sessions** | Cannot maintain session state across connections             | Use client libraries for stateful apps             |

For advanced MQTT features, consider [MQTTX CLI](https://mqttx.app/cli), a purpose-built MQTT command-line tool from EMQ that supports MQTT 5.0, QoS levels, wildcards, and more.

## Verifying curl MQTT Support

If MQTT commands fail, verify your curl build includes MQTT protocol support:

```shell
# Check if mqtt is listed in protocols
curl --version | grep -i protocols

# Test MQTT support explicitly
curl -V 2>&1 | grep -q mqtt && echo "MQTT supported" || echo "MQTT NOT supported"
```

If MQTT is missing, you may need to:

1. Upgrade to a newer curl version
2. Install curl built with MQTT support (some minimal distributions exclude it)
3. Compile curl from source with `--enable-mqtt`

## Conclusion

curl's MQTT support transforms the familiar command-line tool into a powerful IoT testing and scripting companion. With MQTTS arriving in curl 8.19.0, you can now securely interact with MQTT brokers using the same tool you already use for HTTP APIs.

**Key takeaways:**

- Use `mqtt://` for testing and `mqtts://` (curl ≥8.19.0) for secure connections
- curl excels at connectivity testing, prototyping, and quick ad-hoc messaging
- Remember: curl only supports QoS 0; for delivery guarantees, use [MQTTX CLI](https://mqttx.app/cli) or client libraries

Ready to scale beyond testing? [EMQX](https://www.emqx.com/en/products/emqx) handles millions of concurrent MQTT connections with enterprise-grade security, the perfect backend for your curl-powered IoT workflows.

## Related Resources

- [MQTT Broker: How It Works, Popular Options, and Quickstart](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)
- [MQTTX CLI: A Powerful Command Line MQTT Client](https://mqttx.app/cli)
- [Mastering MQTT: The Ultimate Beginner's Guide for 2025](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)
- [Securing MQTT Communication with TLS/SSL](https://www.emqx.com/en/blog/fortifying-mqtt-communication-security-with-ssl-tls)
- [curl MQTT Announcement (2020)](https://daniel.haxx.se/blog/2020/04/14/curl-mqtt-true/)
- [curl MQTTS Announcement (2026)](https://daniel.haxx.se/blog/2026/01/19/now-with-mqtts/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
