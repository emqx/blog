## Overview

[MQTTX](https://mqttx.app) is a cross-platform [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) desktop test client provided by the [EMQ](https://www.emqx.com/en), the world's leading provider of **open source IoT middleware**, and supports macOS, Linux, and Windows. The user interface of MQTTX simplifies the operation logic of pages with the help of a chat software format that allows users to quickly create multiple simultaneous online **MQTT clients**, and facilitate testing the connection/publish/subscribe function of MQTT/TCP, MQTT/TLS, MQTT/WebSocket and other **MQTT protocol** features.

MQTTX Website: [https://mqttx.app](https://mqttx.app)

Download MQTTX v1.5.2: [https://github.com/emqx/MQTTX/releases/tag/v1.5.2](https://github.com/emqx/MQTTX/releases/tag/v1.5.2)

Mac users can download from the APP Store: [https://apps.apple.com/us/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux users can download from the Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://assets.emqx.com/images/fdeeaa3093e114157fdbf46fd18bcd32.png)

## Script Function 

**After the v1.4.2 version, the script function has been added to the MQTTX.** It allows users to use a script to customize converting `Payload`, and can be used to simulate custom test scenarios. The scripting language is currently supported in JavaScript. The following article will use two simple instances to introduce the use of the script function. **Please note that in v1.4.2, the scripting feature is an open test feature, so the use process, security, and functionality will need to be improved.** You are also welcome to discuss this in detail in the MQTTX [GitHub issue](https://github.com/emqx/MQTTX/issues) section, which we will review and respond to.

In the edit script function, there is only an `execute` API globally, and the user needs to write a custom function that takes a `value` parameter, `Payload`, in which the `value` can be modified and transformed in a custom way. Finally, the function is passed as a parameter to `execute` to execute the custom-written function.

### The first example

Simulation of temperature and humidity data reporting in cooperation with the timer sending function.

For example,  when a user is using EMQX, they need to save data to the database using the rules engine function. Once configured, you can use MQTTX to connect to EMQX and test it using the script function. Assuming that the user needs to save the reported temperature and humidity data in JSON format, we can simulate the data using the following script.

```javascript
/**
 * Simulated temperature and humidity reporting
 * @return Return a simulated temperature and humidity JSON data - { "temperature": 23, "humidity": 40 }
 * @param value, MQTT Payload - {}
 */

function random(min, max) {
  return Math.round(Math.random() * (max - min)) + min
}

function handlePayload(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  _value.temperature = random(10, 30)
  _value.humidity = random(20, 40)
  return JSON.stringify(_value, null, 2)
}

execute(handlePayload)
```

At this time, you can copy this code into the code edit box on the script page, and click on the `Save` button in the top right corner, set the script name to TempAndHum, and save it. We enter a `{}` in the Input box as the initial data. Click on the ` Test` button to see the results in the Output box and if the results are as expected, you can then use the script normally.

![mqttxhumtemp.png](https://assets.emqx.com/images/e8c56a968c89ae76bb6fb684ca73027b.png)

We use the [Free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by the EMQX to create a new connection. This service is created based on EMQX's [MQTT IoT cloud platform](https://www.emqx.com/en/cloud). The broker access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

Once connected, click on the drop-down menu in the top right corner and select `Use Script`. In the pop-up window, select the TempAndHum script you have just saved, then select the application type as Published and click the Confirm button to enable the script function.

![mqttxuse1.png](https://assets.emqx.com/images/0cdc5685eec2832049534beaf258fa57.png)

Once the script is on, we will continue to set up the timed sending function. Click on the drop-down function menu in the top right corner and select `Timed messages`, here we set the sending frequency to 1 second, click on confirm and the timed message function will be enabled.

![mqttxtimed.png](https://assets.emqx.com/images/8cf5eaf54e3ab5596c03500012463cd7.png)

Once you are ready, you can enter the initial `Payload` and the `Topic` you want to send to, click on Send, and once you have successfully sent a message, you will see that MQTTX will automatically send the simulation data once per second.

![mqttxhumtempsuccess.png](https://assets.emqx.com/images/695bfda6171514106492d3543d884686.png)

This avoids the need for the user to manually enter and modify the data, and the simulated data can be controlled when using the script, with the simulated data interval set in the `random` function of the script. It is easier and more user-friendly if there is a need for visual graphical testing of saved data, or if a certain amount of data needs to be added to the data for testing.

### The second example

Convert the timestamp in the recieved `Payload` to normal time

In some testing scenarios, the `Payload` received by the user may contain timestamp information. If you need to observe and test more time-sensitive data, you may need to copy the data and then convert the timestamp to time, which is troublesome. In this case, a script can be used to automatically convert the received data to make it easier for the user to observe the data. We can use the following script to convert the data. Again, assume that the data received is of JSON type and contains a time field.

```javascript
/**
 * Convert timestamp to normal time.
 * @return Return the UTC time - { "time": "2020-12-17 14:18:07" }
 * @param value, MQTT Payload - { "time": 1608185887 }
 */

function handleTimestamp(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  // East Eight District needs an additional 8 hours
  const date = new Date(_value.time * 1000 + 8 * 3600 * 1000)
  _value.time = date.toJSON().substr(0, 19).replace('T', ' ')
  return JSON.stringify(_value, null, 2)
}

execute(handleTimestamp)
```

At this point, you can copy this code into the code edit box on the script page, click the `Save` button in the top right corner, set the script name to Time, and save it. We enter a `{ "time": 1608365158 }` in the Input box as the initial data. Click the `Test` button to see the results in the Output box and if the results are as expected, the script will then work as expected.

![mqttxtime.png](https://assets.emqx.com/images/145b3c4b24a42bd52f44923fb0e272f9.png)

At this point, we still create a new connection, and use the method described above to enable this script. Note that when selecting the application type, you need to select Received.

![mqttxuse2.png](https://assets.emqx.com/images/0d3d705ee8a79eecb483cb30ecd15c71.png)

Once the script function is enabled, we add a `Topic` of `testtopic/time` and we send a `Payload` with a timestamp message to that `Topic`. We then look at the received `Payload` message and see that the timestamp has been automatically converted to normal time.

![mqttxtimesuccess.png](https://assets.emqx.com/images/eee40a6a899c8c9912ee55ae9efbd56b.png)

## Summary

So far, we have completed the tutorial on the use of the MQTTX script instance. This feature is scalable and flexible, so you will need to use it according to your needs. Examples of scripts can be found in the [/docs/script-example](https://github.com/emqx/MQTTX/tree/master/docs/script-example) folder of the GitHub repository, and two built-in scripts are currently available, timestamp conversion and temperature and humidity data simulation. If you have a better, more useful script in your use, please submit your code here so that more people can use it.

The project is fully open source, so you can submit any issues you encounter during use on [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc), or submit a revised PR to us after forking MQTTX, we will review and address it in time. We would also like to thank all the users in the community for their contributions and feedback.

If you think this project is still helpful to you, please give us a Star on [GitHub](https://github.com/emqx/MQTTX) to encourage us to do better! :)
