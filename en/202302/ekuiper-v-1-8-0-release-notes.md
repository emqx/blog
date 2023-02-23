> LF Edge eKuiper is a lightweight open-source software built using Golang, designed for IoT edge analytics and streaming data processing on resource-constrained edge devices. Its primary objective is to provide a framework for processing streaming data at the edge, much like Apache Flink. eKuiper's flexible Rule Engine allows users to create IoT edge analytics applications easily within a few minutes by providing SQL-based or graph-based rules, similar to popular tools like Node-RED. 

eKuiper has recently launched version 1.8.0, which comes with several new and exciting features, including:

- **Zero-Coding AI Inference:** The generic AI function allows users to perform real-time AI inference on streaming data such as video streaming without the need for any coding. This function can process any TensorFlow Lite model, making it highly versatile and efficient. Furthermore, users can send the model to the function once it is trained, making it quick and straightforward to use.
- **Visual Rule Creation:** eKuiper's management console includes a visual rule editor called Flow Editor. When using the free eKuiper management console, users can create and edit rules visually by dragging and dropping elements in the UI.
- **Flexible Data Transfer Configuration:** The latest version refactored the formats and serialization implementation for the external connection source/sink. By decoupling the formats and transfer protocols, eKuiper now supports a broader range of formats, such as CSV and custom formats.

For a complete list of features, please see [Release Note](https://github.com/lf-edge/ekuiper/releases/tag/1.8.0).

In addition to the updates mentioned above, the team has also restructured the [documentation](https://ekuiper.org/docs/en/latest/) and updated the part of installation and application scenarios, making it easier for users to quickly find the information they need.

Community Website: [https://ekuiper.org/](https://ekuiper.org/)

GitHub Repository: [https://github.com/lf-edge/ekuiper](https://github.com/lf-edge/ekuiper) 

Docker Image: [https://hub.docker.com/r/lfedge/ekuiper](https://hub.docker.com/r/lfedge/ekuiper) 

## Generic AI Function

In earlier versions, eKuiper allowed users to invoke AI/ML models for algorithmic inference on data streams through plugins. While this approach made it convenient for users to perform pre-processing and post-processing for the algorithm, it had a high learning curve, and the maintenance and updates were also relatively complex.

The new version provides a new plugin designed for real-time AI inference on data streams such as video streaming. This is a generic AI function that is compatible with most pre-trained Tensor Flow Lite models. Users can easily upload or pre-deploy their models and incorporate them into rules without the need for coding.

To use the new tfLite function in eKuiper for real-time AI inference on data streams, you need to provide two arguments: the name of the model (which must have a .tflite extension) and the input to the model. For example, if you have a pre-trained `text_model` for text classification and `smart_reply_model` for smart replies, you can apply them to the input data in two simple steps:

1. Send the models to the edge devices of eKuiper deployments using either eKuiper's upload API or other applications.
2. Configure the rule by specifying the model name in the tfLite function, as shown in the following example.

```
SELECT tfLite(\"text_model\", data) as result FROM demoModel
SELECT tfLite(\"smart_reply_model\", data) as result FROM demoModel
```

The function validates the data input at the level of eKuiper. The user can pre-process or post-process the input and output of the model using SQL statements.

#### Image/Video Streaming Inference

In the new version, eKuiper now supports video streaming and can acquire image frames at regular intervals to process them. With this new feature, image frames can be used for AI inference using the tfLite function. Tensor Flow models are typically trained for specific image sizes, so performing inference on images often requires pre-processing, such as resizing. Fortunately, eKuiper provides pre-processing methods, such as resize and thumbnail, to address this issue. Once the AI inference is complete, the tfLite function returns an array of output tensors that can be further processed by rules or applications.

In the following `ruleTf` rule, we use the `label.tflite` model to pre-process incoming images by resizing them to 224x224.

```
SELECT tfLite(\"label\", resize(self, 224, 224, true) as result FROM tfdemo
```

The fulfillment of this rule is shown below.

![Image/Video Streaming Inference](https://assets.emqx.com/images/33940e588a2a3b26b73545b43ef72f1d.png)

By utilizing the generic AI function, users can rapidly deploy, validate, and update their AI models, significantly accelerating the process of updating their applications.

## Flow Editor

Starting from version 1.6.0, eKuiper has been offering graph rule APIs that are more suitable for visualization-oriented interfaces than SQL rules. With version 1.8.0, a visual editor called Flow Editor has been officially introduced in the free eKuiper management console. This new editor allows users to create and edit rules by dragging and dropping elements in the UI. Users can choose between the original SQL rule editor and the trial version of Flow Editor when creating and editing rules.

The interface of Flow Editor is shown below. The editor follows the style and usage of mainstream visual workflow editors, making it easy for users to get started. Available nodes, as well as user-defined plugins and functions, are listed on the left side. Users can drag and drop these nodes onto the canvas in the center and connect them to create their workflow. The property configuration view is located on the right side, allowing users to customize nodes by clicking on them. We invite you to try Flow Editor and share your feedback with us.

![Flow Editor](https://assets.emqx.com/images/ac0466f1401042bf6e798b6262bc00eb.png)

The latest version of the Flow Editor introduces two new nodes in addition to the legacy features:

- Switch node: The Switch node allows users to direct messages to different processing branches, similar to a switch statement in a programming language.
- Script node: The Script node executes JavaScript code against the messages in transit.

These two nodes enable the creation of traditional multi-branch workflows and make it easier to extend the nodes and script workflows.

## Serialization and Schema Optimization

eKuiper enables the integration of external systems through its source/sink functionality. To read data from an external source, the process consists of two steps: connect and serialization. First, the source is connected to eKuiper following the appropriate protocol. For example, an MQTT source is connected through the MQTT protocol. Once connected, the payload of the data read from the external system is serialized into eKuiper's internal map format. This enables the data to be processed by eKuiper's rules and applications.

### Connection and Serialization

In previous versions, connection and serialization were typically implemented within each source, which meant that even if the connection protocol was a supported one like MQTT, users still had to write a complete plugin to parse custom data format. In the new version, the format and source have been decoupled, allowing users to create custom formats that can be used in conjunction with different sources. Refer to the [Format Extensions](https://ekuiper.org/docs/en/latest/guide/serialization/serialization.html#format) documentation for instructions on how to implement custom formats.

For example, when processing an MQTT data stream, it's possible to define different payload formats. The default format is JSON, which is represented as follows:

```
CREATE STREAM demo1() WITH (FORMAT="json", TYPE="mqtt", DATASOURCE="demo")
```

If the MQTT data stream uses a custom format, the data contained in the payload of MQTT messages should be formatted accordingly:

```
CREATE STREAM demo1() WITH (FORMAT="custom", SCHEMAID="myFormat.myMessage", TYPE="mqtt", DATASOURCE="demo")
```

### Schema

Previously, eKuiper allowed users to specify the data structure type when creating a stream. However, this approach had several drawbacks:

- Additional performance cost: The current schema is not associated with the original schema of the data, so additional validation or conversion is required after the data is decoded. This process is done dynamically based on reflection, which can be less efficient. For example, if a strong schema like Protobuf is used, the data decoded by Protobuf should already be in the correct format and should not require further conversion.
- Cumbersome schema definition: It is not possible to utilize the schema of the data itself, and additional configuration is required.

eKuiper 1.8.0 addresses these issues by supporting both logical and physical schema. When SQL is parsed, the physical and logical schema are automatically merged and used to guide SQL validation and optimization. Additionally, eKuiper provides APIs for inferring the actual schema of data streams from external systems.

```
GET /streams/{streamName}/schema
```

### List of Formats

The new version of eKuiper supports an extended set of formats. eKuiper provides built-in serialization for some formats, while others, such as Protobuf, allow users to provide a static serialization plugin for better performance. Additionally, some formats provide their own schema support, while custom formats can also provide schema implementations.

| Format    | Serialization                                        | Custom Serialization   | Schema                 |
| :-------- | :--------------------------------------------------- | :--------------------- | :--------------------- |
| json      | built-in                                             | unsupported            | unsupported            |
| binary    | built-in                                             | unsupported            | unsupported            |
| delimiter | built-in, the delimiter attribute must be configured | unsupported            | unsupported            |
| protobuf  | built-in                                             | supported              | supported and required |
| custom    | no built-in                                          | supported and required | supported and optional |

## Enhance Analysis Capability

eKuiper 1.8.0 continues to enhance the power of the stateful analysis functions while introducing statistical functions to improve native analysis capability.

### Conditional Analysis Functions

eKuiper 1.8.0 enhances the analysis functions to support the WHEN conditional clause. This clause allows users to determine whether an event is valid before performing any calculations or updates. If the event is valid, the result is calculated and the status is updated. If the event is invalid, the event is ignored, and the saved status is reused. The complete syntax of the analysis functions is as follows:

```
AnalyticFuncName(<arguments>...) OVER ([PARTITION BY <partition key>] [WHEN <Expression>])
```

With the WHEN clause, the analysis functions can implement a complex stateful analysis. For example, to calculate the duration of a status.

```
SELECT lag(StatusDesc) as status, StartTime - lag(StartTime) OVER (WHEN had_changed(true, StatusCode)), EquipCode FROM demo WHERE had_changed(true, StatusCode)
```

lag(StartTime) OVER (WHEN had_changed(true, StatusCode)) returns the time of the last change of status. Therefore, the duration of the status can be calculated in real-time using the current time minus that time.

### Statistical Functions

In eKuiper 1.8.0, new statistical aggregate functions have been introduced, including calculations for standard deviation, variance, and percentile. For details, please refer to: [https://ekuiper.org/docs/en/latest/sqls/built-in_functions.html#AggregateFunctions](https://ekuiper.org/docs/en/latest/sqls/built-in_functions.html#AggregateFunctions).

## Expand Functionality: File and Video Streaming

eKuiper 1.8.0 introduces support for video streaming, enabling the system to process a new type of binary data. Previously, eKuiper was only able to handle images in binary format, which were typically transmitted using protocols designed for text data, such as MQTT or HTTP. The new version also comes with significantly enhanced support for the file source, including the ability to process more file types and stream files.

### File Source

In earlier versions of eKuiper, the file source was primarily used for creating tables and did not offer robust support for data streams. In the latest version, however, file streaming is now supported by setting the interval parameter to pull updates at regular intervals. Additionally, the new version includes enhanced support for folders, a wider range of file formats, and more configuration options.

The new version of eKuiper supports a variety of file types, including:

- json: supports standard JSON array files, but if the content is a line-separated JSON string, it is necessary to define the file type as `lines`.
- csv: supports comma-delimited CSV files, as well as custom separators for additional flexibility.
- lines: supports line-delimited files, where the decoding method for each line can be specified using the `format` parameter in the stream definition. For instance, when working with a line-separated JSON string, one should set the file type to `lines` and the format to `JSON`.

To create a data stream that reads a CSV file, use the following syntax:

```
CREATE STREAM cscFileDemo () WITH (FORMAT="DELIMITED", DATASOURCE="abc.csv", TYPE="file", DELIMITER=",")
```

### Video Streaming Source

The new video streaming source in eKuiper enables users to process real-time video streaming from cameras or networks. It captures frames at a defined frequency or interval and sends them to eKuiper in binary format for processing.

By leveraging existing SQL functions, such as AI inference functions, the data from the video streaming source can be transformed into a format suitable for computation, or output as a new binary image.

## Automated O&M for Rules

eKuiper 1.8.0 automates the restart of rules to improve their autonomy and self-adaptability on the edge, eliminating the need for manual intervention. This is especially useful for environments with large numbers of rules deployed on the edge, where manual maintenance can be time-consuming and tedious.

### Automatic Restart Policies for Rules

eKuiper 1.8.0 introduces a configurable automatic restart feature that allows rules to resume automatically after a failure. This is especially useful for exceptions that can be recovered, as it ensures that rules continue to function even if they encounter an error.

Users have the option to configure a global restart policy for all rules or create individual policies for specific rules. The available settings for these policies include:

- Retry times.
- Retry interval.
- Retry interval factor, the multiplier that determines the rate at which the interval between retries increases after a failed attempt.
- Maximum retry interval.

It allows automatic recovery based on the configuration if a failure occurs, thereby reducing manual maintenance.

### Data Import and Export

The new version of eKuiper includes REST APIs and CLI interfaces for importing and exporting all configurations, including streams, tables, rules, plugins, source configurations, action configurations, and schemas. This feature enables quick backup and migration of configurations to a new eKuiper instance. The exported set of rules is in readable JSON format and can be manually edited if necessary.

- To export all configurations from the current eKuiper instance, use the REST interface GET /data/export.
- To import existing configurations into the target eKuiper instance, use the REST interface POST /data/import.
- If the imported configurations contain updates to plugins or static schema, call the interface POST /data/import?stop=1.
- The status statistics for the imported configurations can be viewed by accessing the GET /data/import/status interface.

### Hot Update for Portable Plugins

Portable plugins are easier to package and deploy than native plugins, so they are updated more frequently. However, in previous versions of eKuiper, updates to Portable plugins did not take effect immediately and required manual intervention to restart the affected rules or the eKuiper itself. In eKuiper 1.8.0, we have introduced seamless switching, which allows rules to automatically switch to the newly updated plugin without any maintenance effort.
