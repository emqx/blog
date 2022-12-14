In November, the eKuiper team began working on v1.8.0 and added several useful features. The update includes support for video streaming from cameras or live streaming, allowing users to process video data in real-time at the edge. It also introduces the tfLite function, which allows users to easily incorporate trained Tensor Flow Lite models into their eKuiper SQL code for AI inference on streaming data. Additionally, the update improves the automation of rule maintenance by setting automatic restart policies and adds support for hot reload of updated Portable plugins. It also enhances the stateful analytic function and introduces the WHEN operator for conditional clauses.

## Automated O&M for rules

In v1.8.0, we are addressing the challenges of maintaining rules on edge by improving their autonomy and self-adaptability. The need for manual intervention is highly eliminated by automatically restarting rules. This is especially useful for environments with large numbers of rules deployed on the edge, where manual maintenance can be time-consuming and tedious. The enhancements to the autonomy and self-adaptability of rules make it easier for users to manage and maintain their edge deployments.

### Automatic restart policies for rules

In v1.8.0, eKuiper introduces a configurable automatic restart feature that allows rules to resume automatically after a failure. This is especially useful for exceptions that can be recovered, as it ensures that rules continue to function even if they encounter an error.

Users have the option to configure a global restart policy for all rules or create individual policies for specific rules. The available settings for these policies include:

- Retry times.
- Retry interval.
- Retry interval factor, the multiplier that determines the rate at which the interval between retries increases after a failed attempt.
- Maximum retry interval.

It allows automatic recovery based on the configuration if a failure occurs, thereby reducing manual maintenance.

### Hot reload for updated Portable plugins

In v1.8.0, we improve the support for Portable plugins in eKuiper. Portable plugins are easier to package and deploy than native plugins, so they are often updated more frequently. However, in previous versions of eKuiper, updates to Portable plugins did not take effect immediately and required manual intervention to restart the affected rules or the eKuiper itself. In v1.8.0, we have introduced seamless switching, which allows rules to automatically switch to the newly updated plugin without any maintenance effort.

## Enhance analytical capability

In v1.8.0, we continues to enhance the power of the stateful analysis function while introducing a generic AI function to improve native analysis capability.

### Generic AI function

We introduced the Tensor Flow Lite plugin, which allows users to perform real-time AI inference on streaming data. This generic AI function can be applied to most trained models of Tensor Flow Lite. Users can easily upload their models or deploy them in advance, and then use them in their rules without any additional coding.

The tfLite function accepts two arguments: the name of the model (which must have the .tflite extension) and the input to the model. In the following two examples, the tfLite function uses the sin_model.tflite model and the fizz_buzz_model.tflite model for real-time AI calculations on the data field in a data stream.

```
SELECT tfLite(\"sin_model\", data) as result FROM demoModel
SELECT tfLite(\"fizz_buzz_model\", data) as result FROM demoModel
```

The function validates the data input at the level of eKuiper. The user can pre-process or post-process the input and output of the model using SQL statements.

### Conditional analytic function

In v1.8.0, we enhance the analytic function to support the WHEN conditional clause. This clause allows users to determine whether an event is valid before performing any calculations or updates. If the event is valid, the result is calculated and the status is updated. If the event is invalid, the event is ignored, and the saved status is reused. The complete syntax of the analytic function is as follows:

```
AnalyticFuncName(<arguments>...) OVER ([PARTITION BY <partition key>] [WHEN <Expression>])
```

With the WHEN clause, the analysis function can implement a complex stateful analysis. For example, to calculate the duration of a status.

```
SELECT lag(StatusDesc) as status, StartTime - lag(StartTime) OVER (WHEN had_changed(true, StatusCode)), EquipCode FROM demo WHERE had_changed(true, StatusCode)
```

lag(StartTime) OVER (WHEN had_changed(true, StatusCode)) returns the time of the last change of status. Therefore, the duration of the status can be calculated in real-time using the current time minus that time.

## Ecosystem

In v1.8.0, we introduce support for video streaming, a new type of binary data that eKuiper can handle. Previously, eKuiper was only able to process images in binary format, and these images were typically transmitted using protocols designed for text data, such as MQTT or HTTP. We also continue to adapt the new version of EdgeX to support these enhancements.

### Video streaming source

The video streaming source allows users to access and process video streaming data, such as video from a camera or live streaming from the network. The video streaming source regularly captures the frames of the video stream and sends them to eKuiper in binary format for processing.

Using existing SQL functions, such as AI inference functions, data from the video streaming source can be converted into data for computation or output as a new binary image, etc.

### Adapt EdgeX Levski

eKuiper 1.7.1 and later versions are adapted to EdgeX Levski. eKuiper EdgeX source also provides support for EdgeX's Nats bus.

## New Look of the product

### Optimize the release workflow

This month, we have optimized our release workflow to accelerate the delivery of new features and improvements to our users. We have done this by improving our infrastructure for continuous integration, allowing us to integrate and test new code more quickly and efficiently. By doing so, we can facilitate user trials and feedback by delivering features as soon as they are ready.

For example, the v1.8.0 features completed this month are now available in version 1.8.0-alpha.2. Users can download and try them via [Docker](https://registry.hub.docker.com/r/lfedge/ekuiper/tags) or [Github](https://github.com/lf-edge/ekuiper/releases/tag/1.8.0-alpha.2).

Continuous integration is also applied to version 1.7.x. Based on user feedback, we have released three fixpacks this month to fix some issues, and the latest version is now v1.7.3.

### Update Logo

This month, we have officially updated the eKuiper logo. The new logo is more vibrant and dynamic, featuring several lines that form a fluid, upward-moving design. This design is more in line with eKuiper's positioning as a lightweight IoT data analysis and stream processing engine that runs on the edge of the network. The upward direction of the lines suggests growth and power, representing eKuiper's ability to quickly and efficiently move massive amounts of IoT data from the edge to the cloud in real-time. The design also conveys the concept of infinite change and embracing everything. Like eKuiper's **flexible and agile integration capabilities, it can be quickly integrated into various edge computing frameworks to build edge-side streaming data solutions.**

![eKuiper New Logo](https://assets.emqx.com/images/d8b14f5674a0a2b9ba2fe227f3975d34.png)


## Coming soon

Next month, we will continue to work on v1.8.0, which includes several exciting new features and improvements. One of these is support for a high-performance static Schema. We will also be further developing the Flow Editor. Stay tuned for more updates on these and other developments in v1.8.0.



<section class="promotion">
    <div>
        Try eKuiper for Free
    </div>
    <a href="https://ekuiper.org/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
