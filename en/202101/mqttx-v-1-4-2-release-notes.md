[MQTT X](https://mqttx.app/) is a cross-platform [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) desktop testing client open sourced by [EMQ](https://www.emqx.com/en), the world's leading provider of **open source IoT middleware**, which supports macOS, Linux, Windows. The user interface of MQTT X uses the chatting software form to simplify the operation logic of pages. Users can quickly create multiple simultaneously online **MQTT client** for convenient testing the connect/publish/subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket and other **MQTT protocol** features.

MQTT X Website: [https://mqttx.app/](https://mqttx.app/)

Download MQTT X v1.4.2: [https://github.com/emqx/MQTTX/releases/tag/v1.4.2](https://github.com/emqx/MQTTX/releases/tag/v1.4.2)

Mac users can download from the App Store: [https://apps.apple.com/us/app/mqttx/id1514074565?mt=12](https://apps.apple.com/us/app/mqttx/id1514074565?mt=12)

Linux users can download from the Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://static.emqx.net/images/eae55fcaa5b4abd9b562bc2aa5fc9dd9.png)

## Overview of new features

### Script function (Beta)

In this version, MQTT X has added the script editing function. Users can implement writing a custom script (JavaScript) to perform custom conversion of the sent and received `Payload`. When combined with the timing send function, this enables automated testing of, for example, simulated data uploads. 

> Note: This feature currently belongs to the testing Beta phase.

Click on the `Script` button in the left-hand menu bar, go to script editing page. On this page, users can write JavaScript code in the code editor at the top. Since there is only one global `execute` API, users need to write a script function that receives a `value` parameter (i.e.`Payload`), and we can perform custom operations on `value` in this function (we need to take into account the type conversion of the `Payload` received). Finally, the function is passed as a parameter to the execute API to `execute` the custom-written function.

The bottom section also contains an `Input` and `Output` box where you can enter the desired input value and click on the `Test` button on the right to view the results in the `Output` box. The format of the input value includes `JSON` and `Plaintext`, which make it easy to debug the functionality of your custom-written scripts in advance. Once the test is complete, the script can be saved by clicking on the `Save` button in the top right corner and entering the name of the script. Once saved, the script is ready to be used on the connection page. Saved scripts can also be edited and deleted.

Once you have written your script, you can switch to the connection page. Click on the drop-down function menu in the top right corner and select `Use Script`. In the pop-up window, select the pre-saved script you need to use and then select the application type, which contains, On Send, On Receive and All. Once you have selected, you need to select the format for the data sent or received according to the data type. Receiving and sending messages normally, if you see the desired effect, a complete function of the use of the script is finished. If users need to cancel the script, they can click on the red `Stop Script` button in the top status bar to stop using the script.

> Note: This function is extensible and flexible, so users need to use it according to their actual needs.

![mqttxscript.png](https://static.emqx.net/images/cd4daadad6483bd7c7a20805ac746933.png)

### Automatically append timestamp to MQTT client ID

To prevent kick-outs when clients with the same Client ID connect, this version has added a new function that automatically adds a timestamp to the Client ID for optimizing. This function ensures the connection will have a different Client ID each time. When creating a connection, the user simply clicks on the Time button behind the Client ID input box and when the color status of the button icon changed, the function is enabled and can be canceled when clicked again.

![mqttxclientidtime.png](https://static.emqx.net/images/b16191291027f1f12229652979afc443.png)

## Fixes and optimizations

- Optimize the system lag when the message list is too long
- Optimize the error message when the system topic ($SYS) subscription fails
- Optimize disabling editing of client information when the client is connected
- Fix the problem of triggering timing tasks incorrectly
- Fix the problem of displaying NaN for unread messages
- Fix the problem that the `Payload` editor can not be displayed

This project is fully open source, and you can go to [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) submit the problems you encountered during use or contribute a PR, and we will review and address it in time. We would also like to thank all the users in the community for their contributions and feedback.
