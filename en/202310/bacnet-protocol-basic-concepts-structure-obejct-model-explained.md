## Introduction

BACnet is a communication protocol designed for intelligent building. It is jointly defined by ISO (International Organization for Standardization), ANSI (American National Standards Institute), and ASHRAE (American Society of Heating, Refrigerating and Air-Conditioning Engineers). BACnet communication is used in heating, ventilation, and air conditioning (HVAC) systems, lighting control, access control systems, fire detection systems, and related equipment. It provides a vendor-independent network solution to achieve interoperability between equipment and control devices for a wide range of building automation applications. BACnet implements interoperability by defining communication messages, formats, and rules used to exchange data, commands, and status information. BACnet provides a data communication infrastructure for intelligent buildings and is implemented in tens of thousands of buildings worldwide.

BACnet communication protocol defines several different data link layer/physical layers, including:

1. ARCNET
2. Ethernet
3. BACnet/IP
4. Point-to-point communication over RS-232
5. Master-Slave/Token-Passing (MS/TP) communication over RS-485
6. LonTalk

This article mainly focuses on the BACnet/IP.

## BACnet/IP Overview

BACnet/IP uses the UDP protocol for data transmission, with a client-server communication approach, where devices typically act as servers and the default port is 47808 (0xBAC0). BACnet/IP packets are mainly composed of an immutable part and a variable part. The immutable part consists of the BVLC type, BVLC function, and length, while the variable part varies according to the BVLC Function. The structure of a BACnet/IP packet is shown in the following figure:

![The structure of a BACnet/IP packet](https://assets.emqx.com/images/d13961d03604ae03a6d875144be4a812.png)

The basic packet types include Original-Unicast-NPDU, Original-Broadcast-NPDU, and Forwarded-NPDU, with specific formats shown in the following figure:

![Original-Unicast-NPDU](https://assets.emqx.com/images/911c1fa64dc98363830c85a0025ebb94.png)

![Original-Broadcast-NPDU](https://assets.emqx.com/images/d00aa892957b616bbfc57349de81989b.png)

![Forwarded-NPDU](https://assets.emqx.com/images/3018b29a278969770a0c83d78e67f794.png)

## Network Layer Protocol Data Unit(NPDU)

The NPDU consists of an NPCI followed by an NSDU. The following table includes the NPCI, but is often erroneously called the NPDU. Please pay attention to it.

![NPDU](https://assets.emqx.com/images/0c131afe5ecd8b76e739a9eeb6669ba2.png)

**NPCI Control Octet**

| **Bit** | **Description**       | **If 1**                                               | **If 0**                  |
| :------ | :-------------------- | :----------------------------------------------------- | :------------------------ |
| 7       | APDU                  | NSDU conveys Network Layer Message                     | NSDU contains BACnet APDU |
| 6       | Reserved              | Reserved                                               | Reserved                  |
| 5       | Destination Specifier | DNET DLEN DADR present                                 | DNET DLEN DADR absent     |
| 4       | Reserved              | Reserved                                               | Reserved                  |
| 3       | Source Specifier      | SNET SLEN SADR present                                 | SNET SLEN SADR absent     |
| 2       | Expecting reply       | Reply                                                  | No reply                  |
| 1,0     | Priority              | 11=Life Safety, 10=Critical Equip, 01=Urgent 00=Normal |                           |

## Application Layer Protocol Data Unit(APDU)

BACnet APDUs carry the application layer parameters. The maximum size of an APDU is specified by a device's Max_APDU_Length_Accepted.

This is one of the two alternatives for NSDU. The other is RPDU.

### Types of APDU

| **APDU Type (Code) (First nibble)** | **APDU (Structure)**           | **Protocol Specification** | **Comments**                                                 |
| :---------------------------------- | :----------------------------- | :------------------------- | :----------------------------------------------------------- |
| 0x0X                                | BACnet-Confirmed-Request-PDU   | 20.1.2                     |                                                              |
| 0x1X                                | BACnet-Unconfirmed-Request-PDU | 20.1.3                     |                                                              |
| 0x2X                                | BACnet-SimpleACK-PDU           | 20.1.4                     |                                                              |
| 0x3X                                | BACnet-ComplexACK-PDU          | 20.1.5                     |                                                              |
| 0x4X                                | Segment ACK                    | 20.1.6                     |                                                              |
| 0x5X                                | Error PDU                      | 20.1.7                     | Error                                                        |
| 0x6X                                | Reject-PDU                     | 20.1.8                     | PDU is rejected due to syntactical reasons, contains BACnet Reject Reason |
| 0x7X                                | Abort PDU                      | 20.1.9                     | Contains BACnet Abort Reason                                 |
| 0x8X~0xfX                           | Reserved                       |                            |                                                              |

### Commonly-Used APDU

**BACnet-Confirmed-Request-PDU**

![BACnet-Confirmed-Request-PDU](https://assets.emqx.com/images/aa1ba0361dd1950f2ca3741c504fd230.png)

**BACnet-Unconfirmed-Request-PDU**

![BACnet-Unconfirmed-Request-PDU](https://assets.emqx.com/images/6d95391e21a9b709da617b5f373f752e.png)

**BACnet-Simple-ACK-PDU**

![BACnet-Simple-ACK-PDU](https://assets.emqx.com/images/fc1c2389908e41f5baa7341c6ff09703.png)

**BACnet-ComplexACK-PDU**

![BACnet-ComplexACK-PDU](https://assets.emqx.com/images/90707fe1d32b1b09bc7ba01f2ab4a44a.png)

### Important Data Structures in APDU

**BACnet Tags**

There are two types of tags, and the **Tag Number** usage varies with each.

- **Application Tags**
  - These have fixed types - boolean, int, date, etc.
- **Context Specific Tags**
  - The types of these tags depend on where they are found in the variable part of the APDU. Their type cannot be determined by inspection alone.
  - They have an associated context number that specifies the meaning of the data.
  - Context Tags also allow Constructed Tags (lists) to be created.

![image.png](https://assets.emqx.com/images/71c5f8a613534d548826ee2e950b7eed.png)

Class = 0 for Application Tags (will indicate the Type of tag)

Class = 1 for Context Specific Tags (Will indicate the sequence of the tag)

**Application Datatype**

Application Datatypes (or colloquially, Application Tags) have a fixed meaning for each tag number. See the table below. Please note that Proprietary Datatypes can only be constructed using these Application Datatypes.

| Tag Number | Description                                                  |
| :--------- | :----------------------------------------------------------- |
| 0          | NULL                                                         |
| 1          | Boolean                                                      |
| 2          | Unsigned Integer*                                            |
| 3          | Signed Integer                                               |
| 4          | Real                                                         |
| 5          | Double                                                       |
| 6          | Octet String                                                 |
| 7          | Character String                                             |
| 8          | Bit String                                                   |
| 9          | Enumerated                                                   |
| 10         | Date                                                         |
| 11         | Time                                                         |
| 12         | BACnetObjectIdentifier                                       |
| 13         | Reserved                                                     |
| 14         | Reserved                                                     |
| 15         | Reserved - Indicates that the following Octect contains an 8-bit Tag Number |

> Note: Unsigned integers can be Unsigned 8, Unsigned 16, or Unsigned 3.

**Object Identifier**

An object can be uniquely identified by its Object Identifier in combination with the Object Identifier of the Device. This uniqueness is limited to the given device and not applicable across a network. It is important to note that using 4194303 as an Object Identifier is not allowed and indicates that the containing object has not been initialized.

The Object Identifier of a device shall be unique network-wide. This effectively means that the Device Instance is unique in any given BACnet Internet work.

Application Tag Number of Object Identifier is 12.

| **31~22**             | **21~0**                  |
| :-------------------- | :------------------------ |
| Object Type (10 bits) | Object Instance (22 bits) |

**Property Identifier**

These are enumerated values in the protocol. Also, be sure to understand tagged values.

There are a total of more than 192 properties. Here are a few of them:

| **Value** | **Hex** | **Description**              | **Encoded As**   |
| :-------- | :------ | :--------------------------- | :--------------- |
| 12        | 0x0C    | Application Software Version | Character String |
| 77        | 0x4E    | Object Name                  | Character String |
| 85        | 0x55    | Present Value                |                  |

**Read Property Request**

| **Encoding** | **Argument**         | **Required** |
| :----------- | :------------------- | :----------- |
| Context 0    | Object Identifier    | Mandatory    |
| Context 1    | Property Identifier  | Mandatory    |
| Context 2    | Property Array Index | User         |

**Write Property**

| **Encoding** | **Argument**         | **Required** |
| :----------- | :------------------- | :----------- |
| Context 0    | Object Identifier    | Mandatory    |
| Context 1    | Property Identifier  | Mandatory    |
| Context 2    | Property Array Index | User         |
| Context 3    | Property Value       | Mandatory    |
| Context 4    | Priority             | Commandable  |

**Confirmed Service ACK Read Property**

| **Encoding** | **Argument**         | **Required**                    | **Comment**                                                  |
| :----------- | :------------------- | :------------------------------ | :----------------------------------------------------------- |
| Context 0    | Object Identifier    | Mandatory Equal                 |                                                              |
| Context 1    | Property Identifier  | Mandatory Equal                 |                                                              |
| Context 2    | Property Array Index | User Equal (Must match request) | Note that if this value is 0, then the following item will be the an array length |
| Context 3    | Property Value(s)    | Mandatory Equal                 | This could be a single field, or multiple fields, depending on Encoding choices. There will be an Opening Tag (Value 0x3f, for context 3, opening tag), one or more values, and a Closing Tag. Variable Encoding per Section 20.3 of the specification. |

## Device Object Model

Different devices have different data structures to store information. To enable information exchange between devices, a "network-visible" information description method must be defined. An object-oriented approach is utilized to achieve this network visibility description method. All objects are referenced by object identifier. Each BACnet device object has a unique object identifier property value. The combination of an object's object identifier with the system-wide unique BACnet device object identifier property value provides a mechanism for referencing each object throughout the entire control network.

BACnet defines a standard set of object types and object properties, but also allows for free definition of additional non-standard object types or non-standard properties of standard object types.

In practical cases, commonly used standard objects include analog input object type, analog output object type, analog value object type, binary input object type, binary output object type, binary value object type, device object type, etc.

Next, we will analyze the analog input object type in detail. At the beginning of the analysis of each object type, there is a list of its attributes. The list items include the attribute identifier, attribute data type, and one of the attribute consistency codes O, R, or W.

- O: Indicates that the attribute is optional.
- R: Indicates that the attribute is required and readable by the BACnet service.
- W: Indicates that the attribute is required, readable, and writable by the BACnet service.

This object and its properties are shown in the following table.

| **Attribute identifier** | **Attribute data type**   | **Attribute consistency code** |
| :----------------------- | :------------------------ | :----------------------------- |
| Object_Identifier        | BACnetObjectIdentifier    | R                              |
| Object_Name              | CharacterString           | R                              |
| Object_Type              | BACnetObjectType          | R                              |
| Present_Value            | REAL                      | R1                             |
| Description              | CharacterString           | O                              |
| Device_Type              | CharacterString           | O                              |
| Status_Flags             | BACnetStatusFlags         | R                              |
| Event_State              | BACnetEventState          | R                              |
| Reliability              | BACnetReliability         | O                              |
| Out_Of_Service           | BOOLEAN                   | R                              |
| Update_Interval          | Unsigned                  | O                              |
| Units                    | BACnetEngineeringUnits    | R                              |
| Min_Pres_Value           | REAL                      | O                              |
| Max_Pres_Value           | REAL                      | O                              |
| Resolution               | REAL                      | O                              |
| COV_Increment            | REAL                      | O2                             |
| Time_Delay               | Unsigned                  | O3                             |
| Notification_Class       | Unsigned                  | O3                             |
| High_Limit               | REAL                      | O3                             |
| Low_Limit                | REAL                      | O3                             |
| Deadband                 | REAL                      | O3                             |
| Limit_Enable             | BACnetLimitEnable         | O3                             |
| Event_Enable             | BACnetEventTransitionBits | O3                             |
| Acked_Transitions        | BACnetEventTransitionBits | O3                             |
| Notify_Type              | ACnetNotifyType           | O3                             |

1 When Out_Of_Service is TRUE, this attribute must be writable.

2 If the object supports COV reports, this attribute is required.

3 If the object supports internal reports, this attribute is required.

**Object_Identifier**

The type of this attribute is BACnetObjectIdentifier, which is a numerical code used to identify objects. It is unique within the BACnet devices that have this attribute.

**Object_Name**

The type of this attribute is CharacterString, which represents the object name. It is unique within the BACnet devices that have this attribute. The minimum length of the string is one character. The characters in the object name must be printable characters.

**Object_Type**

The type of this attribute is BACnetObjectType, which represents the classification of a particular object type. In this object, the value of this attribute is Analog Input (ANALOG_INPUT).

**Present_Value**

The type of this attribute is a real number type, which represents the current value of the input measurement in engineering units. When Out_Of_Service is TRUE, the current value attribute is writable.

**Description**

The type of this attribute is CharacterString, which is a string composed of printable characters with no specific content requirements.

**Device_Type**

The type of this attribute is CharacterString, which is a textual description of the physical device mapped to this analog input object. It is typically used to describe the sensor model corresponding to the analog input object.

**Status_Flags**

The type of this attribute is BACnetStatusFlags, which represents four boolean flags that indicate the status of an analog input device at a given moment. Three of the flags are related to other attribute values of this object. More detailed status can be obtained by reading the attribute values associated with these flags.

**Event_State**

The type of this attribute is BACnetEventState, which is used to detect whether the object is in an event active state. If the object supports internal reporting, this attribute represents the event state of the object. If the object does not support internal reporting, the value of this attribute is normal.

**Reliability**

The type of this attribute is BACnetReliability, which indicates whether the current value or the operation of the physical input device is reliable or not, and if not reliable, specifies the reason. This attribute has the following values: {no fault detected, no sensor, out of range, below range, open circuit, short circuit, other unreliable}.

**Out_Of_Service**

The type of this attribute is Boolean, which indicates whether the physical input represented by the object is (TRUE) or not (FALSE) related to the device. When “Out_Of_Service” is TRUE, the current value attribute is separated from the physical input device and will not change with the changes in the physical input device. When "Out_Of_Service" is TRUE, the reliability attribute and the fault flag state in the corresponding status flag attribute are also separated from the physical input device. When "Out_Of_Service" is TRUE, the current value and reliability attributes can take any value when used to simulate specific fixed conditions or for testing purposes. Other functions that rely on the current value or reliability attributes will respond to these changes as if they occurred in the input.

**Update_Interval**

The type of this attribute is an unsigned integer type, which represents the maximum time interval (in units of one-hundredth of a second) between two normal updates of the current value during normal operation.

**Units**

The type of this attribute is BACnetEngineeringUnits, which represents the measurement unit of this object.

**Min_Pres_Value**

The type of this attribute is a real number type, which represents the minimum reliable numerical value of the current value attribute (expressed in engineering units).

**Max_Pres_Value**

The type of this property is a real number type, representing the maximum reliable value of the current value property (expressed in engineering units).

**Resolution**

The type of this attribute is a real number type, indicating the smallest detectable change in the current value attribute in engineering units (read-only).

**COV_Increment**

The type of this attribute is a real number type, which defines the minimum change value of the current value attribute that will cause a COV notification to be published to COV customers. If the object supports COV reporting, this attribute must be present.

**Time_Delay**

The type of this attribute is an unsigned integer type, which defines the minimum time interval (in seconds) from when the current value attribute is outside the range determined by the high threshold and low threshold to when a TO_OFFNORMAL event is generated, or from when the current value attribute enters the range determined by the high threshold and low threshold (including the range determined by the threshold width attribute value) to when a TO_NORMAL event is generated. If the object supports internal reporting, this attribute must be present.

**Notification_Class**

The type of this attribute is an unsigned integer type, which is used to define the notification category when this object processes and generates event notifications. This attribute defaults to referencing a notification class object with the same notification class attribute value. If the object supports internal reporting, this attribute must be present.

**High_Limit**

The type of this attribute is a real number type, which defines the upper limit value of the current value attribute when generating an event. If the object supports internal reporting, this attribute must be present.

**Low_Limit**

The type of this attribute is a real number type, which defines the lower limit value of the current value attribute when generating an event. If the object supports internal reporting, this attribute must be present.

**Deadband**

The type of this attribute is a real number type, which defines a width range value between the high threshold attribute and the low threshold attribute. If a TO_NORMAL event is to be generated, the current value attribute value must remain within this range. The TO_NORMAL event is generated when all of the following five conditions are met:

- the current value is below (high threshold - threshold width),
- the current value is above (low threshold + threshold width),
- the current value remains within this range for a minimum time interval determined by the time delay attribute,
- the threshold enable attribute is set to either the high threshold enable or low threshold enable flag.
- the event enable attribute is set to the TO_NORMAL flag.

If the object supports internal reporting, this attribute must be present.

**Limit_Enable**

The type of this attribute is BACnetLimitEnable, which uses two flags to indicate whether to enable or disable reporting for high threshold abnormal events and low threshold abnormal events, as well as their respective return to normal events. If the object supports internal reporting, this attribute must be present.

**Event_Enable**

The type of this attribute is BACnetEventTransitionBits, which uses three flags to indicate whether to enable or disable reporting for entry into abnormal, entry into fault (TO_FAULT), and entry into normal events. In the context of analog input objects, the transition to the high threshold and low threshold event states is referred to as an "abnormal" event. If the object supports internal reporting, this attribute must be present.

**Acked_Transitions**

The type of this attribute is BACnetEventTransitionBits, which uses three flags to indicate the receipt of confirmation for entry into abnormal, entry into fault, and entry into normal events. In the context of analog input objects, the transition to the high threshold and low threshold event states is referred to as an "abnormal" event. These flags will be cleared when the corresponding event occurs and will be set under any of the following conditions:

- receiving the corresponding confirmation;
- if the corresponding flag in the event enable attribute is not set and the event occurs (i.e., in this case, no event notification will be generated, so no confirmation will be produced);
- if the corresponding flag in the event enable attribute is set and the corresponding flag in the confirmation transformation attribute of the notification class object is not set, and the event occurs (i.e., no confirmation will be generated).

If the object supports internal reporting, this attribute must be present.

**Notify_Type**

The type of this attribute is ACnetNotifyType, which indicates whether the notifications generated by the object are events or alarms. If the object supports internal reporting, this attribute must be present.

## Summary

This article only analyzed one standard object; other standard objects are similar and only have different attributes. In our next blog, we will offer more detailed tutorials on how to bridge BACnet data to [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) for enhanced IIoT connectivity.

> **Learn more:**
>
> [Bridging BACnet Data to MQTT: A Solution to Better Implementing Intelligent Building](https://www.emqx.com/en/blog/bridging-bacnet-data-to-mqtt)
