In the past several years, IoV has developed from a concept into a trend, sweeping through major car manufacturers and related upstream and downstream industries. A series of guidance standards of relevant departments in China have emerged around the construction of the IoV industry standard system.

EMQ is committed to providing a high-quality Internet of Everything engine for enterprises and has not only established extensive cooperation with mainstream car manufacturers and industry chain-related companies but also provided additional capabilities and technical support from the national standard and industry-standard level. **With the v4.2.3 release, EMQX adds another IoV related GB/T32960 protocol access capability.** 

GB/T32960 is the guideline standard for communication between remote service platforms for new energy vehicles, based on the TCP transmission protocol, and can be used for the communication between the vehicular communication module and the remote service platform.

 This article will introduce how EMQX can access the GB/T32960 protocol devices from the user's perspective.



## Working principle

EMQX Enterprise provides the GB/T 32960 protocol gateway module. The whole process of message exchange can be divided into three parts according to its functional logic and the relationship to the whole system: the terminal side, the platform side, and the other side.

![画板2x.png](https://assets.emqx.com/images/1309966aded70c111bf9b8ed3b3a5ee4.png)

1. The terminal side: Data is exchanged via the GB/T 32960 protocol, implementing different types of data to be reported or sending downstream messages to the terminal.
2. The platform side: The EMQX GB/T 32960 gateway decodes the packets and converts them internally in EMQX to the [MQTT protocol](https://www.emqx.com/en/mqtt) for upstreaming and downstreaming data operations.
   - Data uplink: Publishing the uplink data packet as an MQTT PUBLISH to a specific topic.
   - Data downlink: Publishing the downlink data to a specific topic, and the message is transformed into the GB/T 32960 protocol packet structure and sent down to the terminal.
3. The other side: The rules engine of EMQX Enterprise allows the upstream data appearing in 2 to be stored/forwarded to enterprise databases, stream processing platforms (e.g. Kafka), and business systems; enterprise application platforms can issue control instructions to EMQX in a variety of ways, ultimately sending the data to the terminal side.



## How to enable

Download EMQX Enterprise v4.2.3 onwards, open the Dashboard after launching and add and enable **the GB/T 32960 gateway** under the **Modules** menu.

1. Click on Select to enter the module selection interface and select **the GB/T 32960 Gateway** in **Protocols**.
2. Click on the Select button to enter **the GB/T 32960 gateway** configuration page for pre-launch configuration.
3. After configuring parameters such as the retransmission, packet, and message length, configure the TCP listener parameters and click Add to enable the GB/T 32960 gateway.


![WechatIMG46.png](https://assets.emqx.com/images/c5bcffdd46b4472c883c9f8bdd687629.png)


![WechatIMG48.png](https://assets.emqx.com/images/b2d6f883a5281970dac9dfef974df334.png)


![WechatIMG47.png](https://assets.emqx.com/images/a34ef3e71e3fda8549de7dbfce1a83a2.png)


## Appendix: Example of data exchange format

The following is the format of the data exchange between GB/T 32960 and EMQX. The data format has the following conventions:

- Payload is assembled in JSON format
- JSON Key is named using the Upper Camel Case

Due to space limitations, only some examples of the exchange format are provided here.

### Uplink data

Data flow: Terminal -> GB/T 32960 gateway -> EMQX.

#### Vehicle log-in

Topic: gbt32960/${vin}/upstream/vlogin

```json
{
    "Cmd": 1,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "ICCID": "12345678901234567890",
        "Id": "C",
        "Length": 1,
        "Num": 1,
        "Seq": 1,
        "Time": {
            "Day": 29,
            "Hour": 12,
            "Minute": 19,
            "Month": 12,
            "Second": 20,
            "Year": 12
        }
    }
}
```

#### Vehicle log-out

Topic: gbt32960/${vin}/upstream/vlogout

```json
{
    "Cmd": 4,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Seq": 1,
        "Time": {
            "Day": 1,
            "Hour": 2,
            "Minute": 59,
            "Month": 1,
            "Second": 0,
            "Year": 16
        }
    }
}
```

### Downlink data

GB/T 32960 The gateway controls the terminal in Request-Response mode, sending control data to the Topic used and the response will be returned from the Topic of the characteristic:

#### Request

Flow of requested data: EMQX -> GB/T 32960 gateway -> Terminal

Downlink topic: gbt32960/${vin}/dnstream

#### Response

Flow of response data:：Terminal -> GB/T 32960 gateway -> EMQX

Uplink response topic: gbt32960/${vin}/upstream/response

#### Parameters enquiry

**Req:**

```
{
    "Action": "Query",
    "Total": 2,
    "Ids": ["0x01", "0x02"]
}
```

**Response:**

```
{
    "Cmd": 128,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Total": 2,
        "Params": [
            {"0x01": 6000},
            {"0x02": 10}
        ],
        "Time": {
            "Day": 2,
            "Hour": 11,
            "Minute": 12,
            "Month": 2,
            "Second": 12,
            "Year": 17
        }
    }
}
```

#### Parameter settings

**Req:**

```
{
    "Action": "Setting",
    "Total": 2,
    "Params": [{"0x01": 5000},
               {"0x02": 200}]
}
```

**Response:**

```
{
    "Cmd": 129,
    "Encrypt": 1,
    "Vin": "1G1BL52P7TR115520",
    "Data": {
        "Total": 2,
        "Params": [
            {"0x01": 5000},
            {"0x02": 200}
        ],
        "Time": {
            "Day": 2,
            "Hour": 11,
            "Minute": 12,
            "Month": 2,
            "Second": 12,
            "Year": 17
        }
    }
}
```

#### Terminal control

Remote upgrade: **Req:**

```
{
    "Action": "Control",
    "Command": "0x01",
    "Param": {
        "DialingName": "hz203",
        "Username": "user001",
        "Password": "password01",
        "Ip": "192.168.199.1",
        "Port": 8080,
        "ManufacturerId": "BMWA",
        "HardwareVer": "1.0.0",
        "SoftwareVer": "1.0.0",
        "UpgradeUrl": "ftp://emqx.io/ftp/server",
        "Timeout": 10
    }
}
```

Vehicular terminal shutdown:

```
{
    "Action": "Control",
    "Command": "0x02"
}
```


Vehicular terminal alarm:

```
{
    "Action": "Control",
    "Command": "0x06",
    "Param": {"Level": 0, "Message": "alarm message"}
}
```


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a >
</section>
