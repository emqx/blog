MQTTX 1.10.0 is now available! 

This release significantly enhances file management and configuration capabilities, particularly in the CLI version. Key updates include support for reading and writing messages to files, advanced configuration options, text output mode, and improved logging. Additionally, the desktop version now supports database rebuilding to prevent issues with corrupted files and better handle large data for display. These aim to provide a more robust and user-friendly experience for all MQTTX users.

> *Download the latest version here:* [https://mqttx.app/downloads](https://mqttx.app/downloads)

## File Management in CLI

MQTTX 1.10.0 introduces robust file read and write capabilities to the CLI. It seamlessly handles message payloads as file inputs and outputs over MQTT, facilitating integration and automation in data workflows.

### File Reading

> Note: Due to MQTT protocol constraints, payload size must not exceed 256MB. Verify your MQTT broker's payload size limit before transmitting.

**Using the** `pub` **Command**

Use the following command to read a message from a file:

```
mqttx pub -t topic --file-read path/to/file
```

The `--file-read` option allows you to read content directly from a file as the payload for publishing. This is convenient for using predefined test data for various publishing scenarios.

**Using the** `bench pub` **Command**

The command `--file-read` reads the message body from a file, similar to the simple `pub` command:

```
mqttx bench pub -c 10 -t topic --file-read path/to/file
```

Leveraging the capabilities of the bench command, you can split the input message into a single file using the `--split` option to send different data segments. By default, the character is `\n`.

For example, with a file containing:

```
hello world
```

You can use:

```
mqttx bench pub -c 10 -t topic --file-read path/to/file --split
```

If the file is comma-separated, change `--split` to `,`:

```
mqttx bench pub -c 10 -t topic --file-read path/to/file --split ','
```

You can also set `-im` to define the interval for publishing messages.

### File Writing

To write incoming messages to a file, use:

```
mqttx sub -t topic --file-write path/to/file
```

The `--file-write` option appends each message to a file, separated by a newline character `\n` by default, making it ideal for logging or accumulating text data. This feature is handy for applications that want to maintain a continuous log of received messages.

To change the delimiter, use the `--delimiter` option. For example:

```
mqttx sub -t topic --file-write path/to/file --delimiter ','
```

### File Saving

For saving messages as separate files, use:

```
mqttx sub -t topic --file-save path/to/file
```

The `--file-save` option saves each incoming message as a separate file. Existing files will be automatically renumbered and saved to prevent overwrites. This feature is handy for applications that require storing individual messages for further processing or analysis.

For example, to save incoming messages to a specified directory:

```
mqttx sub -t topic --file-save /path/to/directory/message.txt
```

If `/path/to/directory/message.txt` already exists, new messages will be saved as `message(1).txt`, `message(2).txt`, and so on. This prevents any data loss due to overwriting existing files.

> Do not use `--file-write` and `--file-save` together.

### Type Format

Specify the file format for sending or saving. If not specified, it defaults to plaintext (UTF-8) format. The file content can also be formatted using the `--format` option to handle different data formats:

```
mqttx pub -t topic --file-read path/to/file --format type mqttx sub -t topic --file-save path/to/file --format type
```

Supported data formats for output to file include `json`, `base64`, `hex`, `binary`, and `cbor`.

This version also introduces a `binary` format to handle more common scenarios. MQTTX will generate the corresponding binary file based on the format by specifying binary.

If a file has the following extensions, it will automatically recognize the file format as binary:

- **Image:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.ico`, `.tif`, `.tiff`
- **Video:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.mpeg`, `.3gp`
- **Audio:** `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`, `.m4p`
- **Compressed:** `.zip`, `.gz`, `.rar`, `.tar`, `.7z`, `.bz2`, `.xz`, `.jar`
- **Binary:** `.bin`, `.exe`, `.dll`, `.so`, `.dmg`, `.iso`, `.img`
- **Document:** `.pdf`, `.epub`

To manually specify the binary format, use:

```
mqttx pub -t topic --file-read path/to/file --format binary
mqttx sub -t topic --file-save path/to/file --format binary
```

## Configuration File in CLI

This version introduces a configuration file feature that stores default values for various settings, providing a simplified and customizable experience for MQTTX CLI. After initialization, the configuration file will be stored in the user's home directory at `$HOME/.mqttx-cli/config`.

### Features

The configuration file includes settings for controlling the interface and functional parameters. These settings allow MQTTX CLI to use predefined values, improving efficiency and avoiding the need to enter information repeatedly.

**Default:**

- **output**
  - **text:** Default mode provides concise output with crucial information.
  - **log:** Displays detailed log output with date and time stamps.

**MQTT:**

- **host:** Default is localhost.
- **port:** Default is 1883.
- **max_reconnect_times:** Default is 10.
- **username:** Default is empty.
- **password:** Default is empty.

The output setting in the default section controls the CLI output display. Users can choose different modes according to their needs.

If the command line does not provide these parameters, MQTTX CLI will use the values from the configuration file in the mqtt section. `host`, `port`, `username`, and `password`

The `max_reconnect_times` controls the number of reconnection attempts. The connection will automatically close once this set number is reached to prevent infinite reconnections.

If configuration items like `username` and `password` are not required, they can be omitted from the configuration file.

**Initializing Configuration**

The configuration file is not provided by default. To create or update the configuration file, run the `init` command. This will prompt you to enter the desired values:

```
mqttx init
? Select MQTTX CLI output mode Text
? Enter the default MQTT broker host broker.emqx.io
? Enter the default MQTT port 1883
? Enter the maximum reconnect times for MQTT connection 5
? Enter the default username for MQTT connection authentication admin
? Enter the default password for MQTT connection authentication ******
Configuration file created/updated at /Users/.mqttx-cli/config
```

**Example Configuration File**

```
[default]
output = text
[mqtt]
host = broker.emqx.io
port = 1883
max_reconnect_times = 5
username = admin
password = public
```

### Interface Improvements

The `output` setting in the configuration file offers two modes:

- **Text Mode:** Provides a concise and clean output with only the critical information, making it easier to read and understand.

  ```
  mqttx conn
  ✔ Connected
  ```

- **Log Mode:** This mode displays detailed log output with date and time stamps, which is helpful for recording and debugging.

  ```
  mqttx conn
  [5/24/2024] [11:26:17 AM] › …  Connecting...
  [5/24/2024] [11:26:17 AM] › ✔  Connected
  ```

Users can tailor the MQTTX CLI to better fit their workflow and preferences by selecting the appropriate output mode.

## Desktop White Screen Issue

We have investigated reports of white screen issues in the Desktop version and identified two primary causes: corrupted database files and performance issues when rendering large message payloads. We have optimized MQTTX to address these problems.

### Database Rebuild

Corrupted SQLite database files can result from several factors, particularly after a software upgrade:

1. **Incompatible Architectural Changes:** Upgrades that alter the database structure without properly migrating old data.
2. **Interrupted Upgrades:** Unexpected interruptions during software updates lead to incomplete database files.
3. **Race Conditions:** Concurrent access is not managed correctly, causing write conflicts.
4. **Faulty Upgrade Scripts:** Errors in database script execution during updates affect data integrity.
5. **Insufficient Disk Space:** The lack of space during updates prevents complete data writes.
6. **File System or Hardware Issues:** Underlying storage problems causing file corruption.

When such issues occur, users are unable to open MQTTX. The new version of MQTTX will display a database rebuild page when it detects a corrupted database. Users can click the rebuild button to fix the corrupted database file and reinitialize the data.

> Note: After rebuilding the database, all local data will be lost.

![Database Rebuild](https://assets.emqx.com/images/5ffffea84aac38f13a52c96a25663e22.png?imageMogr2/thumbnail/1520x)

### Large Data Handling

Another issue is the performance hit caused by large message payloads. While typical MQTT messages are generally under 1MB, the maximum size can be 256 MB. When users send large files, rendering these messages in MQTTX can cause the UI to freeze or crash, resulting in a white screen.

In the new version, we have implemented a data threshold. When the payload size exceeds 512KB, MQTTX will display only a portion of the message content. Users can click "Show More" to view the full message. Additionally, users can save large messages to their local system using the "Save to Local" button for viewing with other applications.

![image.png](https://assets.emqx.com/images/c093554bb650045c84eeeff03f1f28fe.png)

![image.png](https://assets.emqx.com/images/06becba2662d4c595d4cbed851442353.png)

These improvements ensure that MQTTX can handle large payloads more efficiently, preventing UI freezes and enhancing the overall user experience.

## Web Updates

### Added Support for BASE_URL Configuration via Env File

If you need to make personalized settings, such as modifying the default connection path, deployment path, or output path, you can make the corresponding modifications in the `web/.env` or `web/.env.docker` files. These two files correspond to different packaging requirements, and you can modify them according to your situation.

| Configuration Item       | Description                                                  |
| :----------------------- | :----------------------------------------------------------- |
| VUE_APP_PAGE_TITLE       | The title displayed in the browser's title bar               |
| VUE_APP_PAGE_DESCRIPTION | A brief page description for SEO purposes                    |
| VUE_APP_DEFAULT_HOST     | The default address of the MQTT broker server connections    |
| BASE_URL                 | The root URL where the application is deployed. Helpful in constructing links and routing |
| VUE_APP_OUTPUT_DIR       | The directory where the build files will be placed after compilation |

These updates aim to provide a more flexible and user-friendly experience, allowing you to customize your MQTTX Web setup to fit your needs.

## **Breaking Changes**

| Old Command                                      | New Command                                             |
| :----------------------------------------------- | :------------------------------------------------------ |
| mqttx conn -h broker.emqx.io  -p 1883 --save     | mqttx conn -h broker.emqx.io  -p 1883 --save-options    |
| mqttx conn --config /Users/mqttx-cli-config.json | mqttx conn --load-options /Users/mqttx-cli-options.json |

In this update, the `--config` parameter has been replaced with the `--options` parameter. This change is made to reflect better the purpose of these parameters, which is to save and load the frequently used command parameters.

- **-so, --save-options**: Save the parameters to the local configuration file, which supports JSON and YAML formats. The default path is `./mqttx-cli-options.json`.
- **-lo, --load-options**: Load the parameters from the local configuration file, which supports JSON and YAML formats. The default path is `./mqttx-cli-options.json`.

## Others

**New Features and Improvements**

- **Auto Re-subscription Tips**: The subscription dialog now has auto re-subscription tips. When subscribing, you can see whether the auto re-subscription feature is enabled.
- **GPT-4o Support**: Added support for GPT-4o in MQTTX Copilot, bringing advanced AI capabilities to your MQTTX experience.

**Bug Fixes**

- **Version Update Dialog**: The version update dialog was fixed to ensure it is properly adapted to dark mode and provides a consistent user experience across different themes.
- **Topic Filtering**: Resolved an issue with topic filtering, ensuring accurate and reliable filtering of topics.
- **Logging Improvements**: Enhanced the logging format and improved bench sub logs by graying out output meta information, making logs more readable and useful for debugging.
- **Subscription Errors**: Fixed the subscription error logic when dealing with multiple topics, ensuring smoother and more reliable subscriptions.
- **CLI Pub Failure Handling**: Improved the reconnection logic in the CLI for publishing failures, ensuring that the CLI handles pub failures more gracefully and attempts reconnections as needed.

These updates focus on improving user experience, enhancing functionality, and fixing critical bugs to ensure a smoother and more reliable operation of MQTTX.

## Roadmap

- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Topic Tree View**: Enhance organization and visualization of topics.
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View:** Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).
- **Support for Configurable Disconnect Properties (MQTT 5.0)**: Enhance connection management with customizable disconnection settings.
- **IoT Scenario Data Simulation**: Bring this feature to the desktop client to ease IoT scenario testing.
- **Sparkplug B Support**: Extend MQTTX functionalities to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization**: Configurable options to reduce storage space usage.
- **MQTT GUI Debug Functionality**: New features to aid in debugging MQTT communications.
- **Plugin Functionality**: Introduction of a plugin system supporting protocol extensions like [CoAP](https://www.emqx.com/en/blog/coap-protocol) and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **Avro Message Format Support**: Encoding and decoding capabilities for Avro message format.
- **Script Test Automation (Flow)**: Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient">Get Started →</a>
</section>
