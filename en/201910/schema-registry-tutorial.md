The types of IoT devices are complex, and the encoding formats used by various vendors are different. Therefore, when accessing the IoT platform, a unified data format is required, so that applications of equipment on the platform can be managed.

EMQX Enterprise Edition 3.4.0 provides Schema Registry functionality and provides encoding and decoding capabilities. Schema Registry manages the Schema used for encoding and decoding, processes encoding or decoding requests and returns results. Schema Registry works with a rules engine to adapt device access and rule design for various scenarios.

## Data Format

The following image shows an application case for the Schema Registry. Multiple devices report data in different formats. After being decoded by the Schema Registry, they are converted into a unified internal format and then forwarded to the background application.

![1.png](https://assets.emqx.com/images/1a11b01e24279067b4f17a2afe1898e1.png)

[Figure 1: Using the Schema Registry to encode and decode device data]

### Binary Format Support

The built-in Schema Registry data format of EMQX 3.4.0 includes[Avro](https://avro.apache.org) and  [Protobuf](https://developers.google.com/protocol-buffers/). Avro and Protobuf are Schema-dependent data formats. The encoded data is binary. The internal data format (Map, explained later ) decoded by Schema Registry can be used directly by the rules engine and other plugins. In addition, Schema Registry supports user-defined (3rd-party)  coding and decoding services, which are much closer to business needs through HTTP or TCP callbacks.

## Architecture Design

Schema Registry maintains Schema text for built-in encoding formats such as Avro and Probouf, but for custom  codec (3rd-party) formats, if Schema is needed, Schema text needs to be maintained by the codec service itself. Schema Registry creates a Schema ID for each Schema, and the Schema API provides add, query, and delete operations through the Schema ID.

Schema Registry can be decoded or coded. Schema ID needs to be specified when encoding and decoding.

![arch.png](https://assets.emqx.com/images/a16f4ad438e98bb108138c5ccac68e4b.png)

[Figure 2: Schema Registry schematic]

Example of encoding call: parameter is Schema

```c
schema_encode(SchemaID, Data) -> RawData
```

Example of decoding call: 

```c
schema_decode(SchemaID, RawData) -> Data
```

A common use case is to use the rule engine to call the encoding and decoding interfaces provided by the Schema Registry, and then use the encoded or decoded data as input for subsequent actions.



## Coding and Decoding + Rule Engine

The message processing  of EMQX can be divided into three parts: Messaging, Rule Engine and Data Conversion.

EMQX's [PUB/SUB](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) system routes messages to specified topics. Rule engine can flexibly configure business rules of data, match messages according to rules, and then specify corresponding actions. Data format conversion occurs before the rule matching process. The data is first converted to a Map format that can participate in rule matching, and then matched.

![SchemaAndRuleEngine.png](https://assets.emqx.com/images/80507f270e8aee6b00bb7ce7d2ca2136.png)

[Figure 3:Messaging, Rule Engine and Schema Registry]

### Rule Engine Internal Data format (Map)

The data format used internally by the rules engine is Erlang Map, so if the original data content is in binary or other format,  it must be converted to Map using codec functions (such as schema_decode and json_decode functions mentioned above).

Map is a data structure of the form Key-Value, like #{key => value}. For example, `user = #{id => 1, name => "Steve"} ` defines a `user` map with `id` for `1` and `name` for `"Steve"`.

The SQL statement provides nested extraction and addition of Map fields by the "." operator.  The following is an example of using this SQL statement for this Map operation:

```mysql
SELECT user.id AS my_id
```

The result filtered  by the SQL statement is `#{my_id => 1}`.

### JSON Coding and Decoding

The SQL engine of the rules engine provides coding and decoding support for JSON formatted strings. The SQL functions that convert JSON strings and Map formats to each other are json_decode() and json_encode():

```mysql
SELECT json_decode(payload) AS p FROM "message.publish" WHERE p.x = p.y, topic ~= "t/#"
```

The above SQL statement will match the MQTT message with payload content of a JSON string: `{"x" = 1, "y" = 1}` and topic of `t/a`.

` json_decode(payload) as p` decodes the JSON string into the following Map data structure so that the fields  p.x and p.y in the Map can be used in the `WHERE` clause:



```erlang
#{
  p => #{
    x => 1,
    y => 1
  }
}
```

**Note:** `AS` clause is necessary. The decoded data is assigned to a Key before it can be subsequently manipulated.

## Coding and Decoding Practice

### Protobuf Data Analysis Example

#### Rule Requirement

The device publishes a binary message encoded by Protobuf that needs to be re-published to the topic associated with the "name" field after it has been matched by the rule engine. The format of the topic is "person/${name}".

For example, republish the message with the "name" of "Shawn" to the topic of "person/Shawn".

#### Create Schema

On the  [Dashboard](http://127.0.0.1:18083/#/schemas/0?oper=create) interface of EMQX , create a Protobuf Schema with the following parameters:

1. Name: protobuf_person

2. Codec type: protobuf

3. Schema: The following protobuf schema defines a Person message.

   ```
   message Person {
     required string name = 1;
     required int32 id = 2;
     optional string email = 3;
   }
   ```

After the Schema is created, emqx assigns a Schema ID and Version. If "protobuf_person" is created for the first time, the Schema ID is "protobuf_person:1.0".

#### Create Rules

**Write the rule SQL statement using the Schema ID  just created:**

```sql
SELECT
  schema_decode('protobuf_person:1.0', payload, 'Person') as person, payload
FROM
  "message.publish"
WHERE
  topic =~ 't/#' and person.name = 'Shawn'
```

The key point here is `schema_decode('protobuf_person:1.0', payload, 'Person')`:

- `schema_decode` function decodes the contents of the payload field according to the Schema of 'protobuf_person:1.0';
- `as person` saves the decoded value to the variable "person";
- The last parameter `Person` indicates that the type of message in the payload is of type 'Person' defined in the protobuf schema.

**Then, the action is added with the following parameters:**

- Action type: message republish
- Objective topic: person/${person.name}
- Message content template: ${person}

This action sends the decoded "person" in JSON format to the topic of `person/${person.name}`. Where `${person.name}` is a variable placeholder that will be replaced at runtime with the value of the "name" field in the message content.

#### Device-Side Code

Once the rules are created,  the data can be simulated and tested.

The following code populates a Person message with the Python language and encodes it into binary data, and then sent to the "t/1" topic. See [complete code](https://github.com/terry-xiaoyu/schema-registry-examples/blob/master/protobuf/pb2_mqtt.py) for details.

```python
def publish_msg(client):
    p = person_pb2.Person()
    p.id = 1
    p.name = "Shawn"
    p.email = "liuxy@emqx.io"
    message = p.SerializeToString()
    topic = "t/1"
    print("publish to topic: t/1, payload:", message)
    client.publish(topic, payload=message, qos=0, retain=False)
```

#### Check Rule Execution Result

1) In Dashboard's [Websocket](http://127.0.0.1:18083/#/websocket) tool, log in to an MQTT Client and subscribe to "person/#".

2) Install the python dependencies and execute the device side code:

```shell
$ pip3 install protobuf
$ pip3 install paho-mqtt

$ python3 ./pb2_mqtt.py
Connected with result code 0
publish to topic: t/1, payload: b'\n\x05Shawn\x10\x01\x1a\rliuxy@emqx.io'
t/1 b'\n\x05Shawn\x10\x01\x1a\rliuxy@emqx.io'
```

3) Check that the Websocket receives a message with the topict `person/Shawn`:

```
{"email":"liuxy@emqx.io","id":1,"name":"Shawn"}
```



### Avro Data Analysis Example

#### Rule Requirement

The device publishes a binary message encoded by Avro  that needs to be republished to the topic associated with the "name" field after it has been matched by the rule engine. The format of the topic is "avro_user/${name}".

For example, republish the message with the "name" of "Shawn" to the topic of "avro_user/Shawn".

#### Create Schema

On the  [Dashboard](http://127.0.0.1:18083/#/schemas/0?oper=create) interface of EMQX , create an Avro Schema with the following parameters:

1. Name: avro_user

2. Codec type: avro

3. Schema:

   ```protobuf
   {
    "type":"record",
    "fields":[
        {"name":"name", "type":"string"},
        {"name":"favorite_number", "type":["int", "null"]},
        {"name":"favorite_color", "type":["string", "null"]}
    ]
   }
   ```

After the Schema is created, emqx assigns a Schema ID and Version. If  "avro_user" is created for the first time, the Schema ID is "avro_user:1.0".

#### Create Rule

**Write the rule SQL statement using the Schema ID just created:**

```sql
SELECT
  schema_decode('avro_user:1.0', payload) as avro_user, payload
FROM
  "message.publish"
WHERE
  topic =~ 't/#' and avro_user.name = 'Shawn'
```

The key point here is `schema_decode('avro_user:1.0', payload)`:

- `schema_decode` function decodes the contents of the payload field according to the Schema of 'avro_user:1.0';
- `as person` saves the decoded value to the variable  "avro_user" ;

**Then, the action is added with the following parameters:**

- Action type: message republish
- Objective topic: avro_user/${avro_user.name}
- Message content template: ${avro_user}

This action sends the decoded "user" in JSON format to the topic of `avro_user/${avro_user.name}`. Where `${avro_user.name}` ` is a variable placeholder that will be replaced at runtime with the value of the "name" field in the message content.

#### Device-Side Code

Once the rules are created,  the data can be simulated  and tested.

The following code populates a  User  message with the Python language and encodes it into binary data, and then sent to the "t/1" topic. See [complete code](https://github.com/terry-xiaoyu/schema-registry-examples/blob/master/protobuf/pb2_mqtt.py) for details.

```python
def publish_msg(client):
    datum_w = avro.io.DatumWriter(SCHEMA)
    buf = io.BytesIO()
    encoder = avro.io.BinaryEncoder(buf)
    datum_w.write({"name": "Shawn", "favorite_number": 666, "favorite_color": "red"}, encoder)
    message = buf.getvalue()
    topic = "t/1"
    print("publish to topic: t/1, payload:", message)
    client.publish(topic, payload=message, qos=0, retain=False)
```

#### Check Rule Execution Result

1) In Dashboard's [Websocket](http://127.0.0.1:18083/#/websocket) tool, log in to an MQTT Client and subscribe to  "avro_user/#".

2) Install the python dependencies and execute the device side code:

```shell
$ pip3 install protobuf
$ pip3 install paho-mqtt

$ python3 avro_mqtt.py
Connected with result code 0
publish to topic: t/1, payload: b'\nShawn\x00\xb4\n\x00\x06red'
```

3) Check that the Websocket receives a message with the topict `avro_user/Shawn` `:

```
{"favorite_color":"red","favorite_number":666,"name":"Shawn"}
```

### Custom Codec Example

#### Rule Requirement

The device issues an arbitrary message to verify that the self-deployed codec service works.

#### Create Schema

On the  [Dashboard](http://127.0.0.1:18083/#/schemas/0?oper=create) interface of EMQX , create a 3rd-Party Schema with the following parameters:

1. Name: my_parser
2. Codec type: 3rd-party
3. Third-party type: HTTP
4. URL: http://127.0.0.1:9003/parser
5. Codec configuration: xor

Other configurations remain the default. Emqx will assign a Schema ID "my_parser". There is no Version management in custom codecs .

The fifth codec configuration above is optional,  which is a string, and the content is related to the business of the codec service.

#### Create Rules

**Write the rule SQL statement using the Schema ID just created:**

```sql
SELECT
  schema_encode('my_parser', payload) as encoded_data,
  schema_decode('my_parser', encoded_data) as decoded_data
FROM
  "message.publish"
WHERE
  topic =~ 't/#'
```

This SQL statement first encode the data, and then decode. The purpose is to verify that the encoding and decoding process is correct:

- `schema_encode`  function encodes the contents of the payload field according to the Schema of 'my_parser' and saves the result in the variable of `encoded_data`.
- `schema_decode` function decodes the contents of the payload field according to the Schema of 'my_parser' and saves the result in the variable of `decoded_data`.

Finally, the filtered result by this SQL statement is the two variables `encoded_data` and `decoded_data`.

**Then, the action is added with the following parameters:**

- Action type: check (debug)

This check will print the results filtered by the SQL statement to the emqx console (erlang shell).

If the service is started with emqx console, the print will be displayed directly in the console; if the service is started with emqx start, the print will be output to the erlang.log.N file in the log directory, where "N" is an integer. For example "erlang.log.1", "erlang.log.2".

#### Codec Server Code

Once the rules are created, the data  can be simulated for testing. So first your own codec service need to be written.

The following code implements an HTTP codec service in Python language. For simplicity, this service provides two simple ways to code and decode (encryption and decryption). See [complete code](https://github.com/terry-xiaoyu/schema-registry-examples/blob/master/3rd_party/http_parser_server.py) for details.

- Bitwise XOR
- character replacement

```python
def xor(data):
  """
  >>> xor(xor(b'abc'))
  b'abc'
  >>> xor(xor(b'!}~*'))
  b'!}~*'
  """
  length = len(data)
  bdata = bytearray(data)
  bsecret = bytearray(secret * length)
  result = bytearray(length)
  for i in range(length):
    result[i] = bdata[i] ^ bsecret[i]
  return bytes(result)

def subst(dtype, data, n):
  """
  >>> subst('decode', b'abc', 3)
  b'def'
  >>> subst('decode', b'ab~', 1)
  b'bc!'
  >>> subst('encode', b'def', 3)
  b'abc'
  >>> subst('encode', b'bc!', 1)
  b'ab~'
  """
  adata = array.array('B', data)
  for i in range(len(adata)):
    if dtype == 'decode':
      adata[i] = shift(adata[i], n)
    elif dtype == 'encode':
      adata[i] = shift(adata[i], -n)
  return bytes(adata)
```

Run this service:

```shell
$ pip3 install flask
$ python3 http_parser_server.py
 * Serving Flask app "http_parser_server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:9003/ (Press CTRL+C to quit)
```

#### Check Rule Execution Result

Since this example is relatively simple, we use the MQTT Websocket client directly to simulate a message sent by the device.

1) In Dashboard's [Websocket](http://127.0.0.1:18083/#/websocket) tool, log in to an MQTT Client and post a message to "t/1" with the content "hello".

2) Check the print in the emqx console (erlang shell):

```
(emqx@127.0.0.1)1> [inspect]
        Selected Data: #{decoded_data => <<"hello">>,
                         encoded_data => <<9,4,13,13,14>>}
        Envs: #{event => 'message.publish',
                flags => #{dup => false,retain => false},
                from => <<"mqttjs_76e5a35b">>,
                headers =>
                    #{allow_publish => true,
                      peername => {{127,0,0,1},54753},
                      username => <<>>},
                id => <<0,5,146,30,146,38,123,81,244,66,0,0,62,117,0,1>>,
                node => 'emqx@127.0.0.1',payload => <<"hello">>,qos => 0,
                timestamp => {1568,34882,222929},
                topic => <<"t/1">>}
        Action Init Params: #{}
```

Select Data is the data filtered by the SQL statement, Envs is the environment variable available inside the rule engine, and Action Init Params is the initialization parameter of the action. These three data are all in the `Map` format.

The two fields `selected_data` and `encoded_data` in Selected Data correspond to the two ASs in the SELECT statement. Since `decoded_data` is the result of encoding and then decoding, it is restored to the content we sent "hello", indicating that the codec plugin works properly.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
