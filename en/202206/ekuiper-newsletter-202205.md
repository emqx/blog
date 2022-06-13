In May, eKuiper is in the early stage of new feature development of v1.6.0, and the development of its product function mainly includes the encoding/decoding supports of protobuf. We are also validating the prototype in response to the user's repeated request of writing the data processing rules by dragging and dropping. The bug in v1.5.1 is fixed and expected to be released in early June.

As an edge streaming data processing software, eKuiper has participated in the evaluation by the standard of the *Requirements for Technical Capability of Processing Edge Streaming Data* initiated by China Academy of Information and Communications Technology (CAICT). Once qualified, eKuiper will become the first product recognized by this standard. 

## Encoding/Decoding Supports of Protobuf

Currently, the default value of the source and sink's configuration attribute format for encoding/decoding is JSON, and users may use its encoding and decoding capability through the newly-added protobuf options. Compared with JSON, the data amount of protobuf is smaller, which is conducive to saving the bandwidth of transmission among cloud edges. This feature has been developed but not released yet, and users can try using it through the v1.6.0 branch of edge source code.

Compared with JSON format without schema, it is necessary for protobuf to define the proto files as the schema for encoding and decoding. Before using protobuf format, however, users should register the schema, and specify the schema used for encoding and decoding by adding the attribute of schemaId.

## Schema Management

Register with REST API, and the schema content may be provided by the file path or text

```
// POST /schemas
{
  "id":"fileName",
  "file":"http://myhost/files/abc.proto"
}
```

or configured by the text content:

```
// POST /schemas
{
  "id":"schemaName",
  "content":"message Person {
    required string name = 1;
    required int32 id = 2;
    optional string email = 3;
  }"
}
```

Either way, the content will be saved in etc/schemas/protobuf.

#### Using protobuf in Sink

Format is used to specify the codes used.

schemaId is used to specify the schema used.

```
{
  "mqtt":{
    "server":"tcp://127.0.0.1:1883",
    "topic": "result",
    "format":"protobuf",
    "schemaId":"schemaName.Person"    // The ID consists of two parts, the first part is the file name and the second is the message name
  }
}
```

#### **Using protobuf in Source**

FORMAT Supports protobuf

SCHEMA_ID is used to specify the schema used.

```
CREATE STREAM demo() WITH (TYPE="NEURON", FORMAT="protobuf", SCHEMA_ID="schemaName.Person") 
```

## Visual Drag/Drop Editing Ability

Previously, eKuiper only supported the writing of data processing rules for streaming data in the form of SQL, and there was a certain threshold inconvenient for business people to directly participate in writing the rules. To lower the threshold of use, eKuiper is ready to support the visual drag and drop data processing units and the simple editing and configuration, and ultimately connecting the multiple data processing units to form data processing rules automatically, which is convenient for more people to directly use eKuiper for business processing. This proposal is still in the prototype design stage.

## Coming Soon

Next, we will improve the visual drag and drop editing and merge it into the master branch. Furthermore, eKuiper will optimize the caching mechanism after sink error, achieve the offline storage of memory+disk, and resend it sequentially after error recovery, which will support a stronger recovery ability in case of network disconnection and cache the data for a longer time.
