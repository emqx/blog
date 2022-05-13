In [the previous article of this series](https://www.emqx.com/en/blog/introduction-to-the-open-source-testing-tool-jmeter), we introduced the open-source test tool JMeter and took a simple HTTP test as an example to see the capabilities of JMeter. In this article, we will further introduce JMeter's rich components to help you build test scripts for complex scenarios.

JMeter's test script is presented in the form of 「tree」 in the interface, and the saved test script jmx file itself is also in xml format. The JMeter script tree takes the test plan as the root node, and all test components will be included in the test plan. In the test plan, you can configure user-defined variables called by components in the whole test plan, as well as thread group behavior, library files used in test, etc.

By using various test components in the test plan, you can build rich test scenarios. The test components in JMeter generally have the following categories: thread group, sampler, logic controller, listener, config element, assertion, timer, pre-processor and post-processor. Next, we will introduce them separately and describe the main components in detail.

## Thread Groups

The Thread Group is the beginning point for all test plans. All samplers and controllers must be placed under a thread group. A thread group can be regarded as a virtual user pool, in which each thread can be understood as a virtual user, and multiple virtual users perform the same batch of tasks at the same time. Each thread is independent and does not affect the others. During the execution of one thread, the variable of the current thread will not affect the variable value of other threads.

The interface of thread group is shown in the following figure:

![JMeter thread group](https://assets.emqx.com/images/f264fc760b67b75f0f2e912d593afc8e.png)

In the interface, the thread group can be configured as below:

1. Action to be taken after a Sampler error

   The following configuration items control whether the test will continue to be executed or not when an error is encountered.

   - Continue: ignore errors and continue execution
   - Start Next Thread Loop: ignore the error, terminate the current loop of the thread, and execute the next loop
   - Stop Thread: stops executing the current thread without affecting the normal execution of other threads
   - Stop Test: the entire test will be stopped after all currently executing threads have finished the current sampling
   - Stop Test Now: the entire test execution will be stopped immediately, and currently executing samplers may be interrupted.

2. Number of threads

   The number of threads is the number of concurrent users, and each thread will run the test plan completely independently without interfering with each other. Multiple threads are used in the test to simulate concurrent access to the server.

3. ramp-up period

   The ramp-up time is used to set the time required to start all threads. For example, if the number of threads is set to 10 and the ramp-up time is set to 100 seconds, JMeter will use 100 seconds to start and run 10 threads, and each thread will start 10 seconds after the previous thread was started.

   If the ramp-up value is set small and the number of threads is set large, it will put a lot of stress on the server at the beginning of the test.

4. Loop count

   Sets the number of loops per thread in the thread group before ending

5. Delay thread creation until needed

   By default, all threads are created when the test starts. If this option is checked, threads are created when they are needed.

6. Specify thread lifetime

   The scheduler configuration can control the execution time of thread groups more flexibly

   (1) Duration: control the duration of the test, with the unit of second.

   (2) Startup delay: Control how long after the test be delayed before startup, with the unit of second.

## Samplers

The sampler is used to simulate user operations, and is a running unit that sends requests to the server and receives response data from the server. A sampler is a component inside a thread group, so it must be added to the thread group. JMeter natively supports a variety of samplers, such as TCP sampler, HTTP request, FTP request, JDBC request, Java request, etc. Each type of sampler sends different requests to the server according to the set parameters.

### TCP Sampler

The TCP Sampler connects to the specified server through TCP/IP, sends a message to the server after the connection is successful, and then waits for the server to reply.

The interface is as follows:

![JMeter TCP Sampler](https://assets.emqx.com/images/1e2ce5cddd88ec451fc8552a4430a5d6.png)

The properties that can be set in the TCP sampler are as follows:

**TCPClient classname**

It represents the implementation class that handles the request. By default, org.apache.jmeter.protocol.tcp.sampler.TCPClientImpl is used, and plain text is used for transmission. In addition, JMeter also has built-in support for BinaryTCPClientImpl and LengthPrefixedBinaryTCPClientImpl. The former uses hexadecimal packets, and the latter adds a 2-byte length prefix to BinaryTCPClientImpl.

You can also provide custom implementation classes by extending org.apache.jmeter.protocol.tcp.sampler.TCPClient.

1. Target server settings

   「Server Name or IP」 and 「Port Number」 specify the hostname/IP address and port number of the server application.

2. Connection Options

   - Re-use connection: If checked, this connection will always be open, otherwise it will be closed after reading data.
   - Close Connection: If checked, this connection will be closed after the TCP sampler has finished running.
   - Set No-Delay: If checked, the Nagle algorithm will be disabled, and the sending of small packets is allowed.
   - SO_LINGER: Used to control whether to wait for data in the buffer to complete transmission before closing the connection.
   - End of line (EOL) byte value: Used to determine the byte value at the end of the line. If the specified value is greater than 127 or less than -128, the EOL check will be skipped. For example, if the strings returned by the server end with a carriage of return, we can set this option to 10

3. Timeouts：

   - Connect Timeout

   - Response Timeout

4. Text to send

   Payload to be sent

5. Login configuration

   Set the username and password used for the connection

### HTTP Request sampler

The HTTP sampler sends HTTP/HTTPS requests to the web server.

![JMeter HTTP Request sampler](https://assets.emqx.com/images/fc003b6a29ab67435d4ad0d4c7434388.png)

**1.Name and Comments**

**2.Protocol**

​	The protocol used to send the request to the target server, which can be HTTP, HTTPS or FILE. The default is HTTP.

**3. Server name or IP address**

​	The hostname or IP address of the target server to which the request is sent.

**4. Port number**

​	The port number that the web service is listening. The default port is 80 for HTTP, and is 443 for HTTPS.

**5. Request method**

​	The method of sending the request, commonly including GET, POST, DELETE, PUT, TRACE, HEAD, OPTIONS, etc.

**6. Path**

​	The target URL path to request (excluding server address and port).

**7. Content encoding**

​	Applicable to several request methods of POST, PUT, PATCH and FILE, which controls the way of encoding the request content

**8. Advanced request options**

- Redirect Automatically: redirection is not treated as separate requests and is not recorded by JMeter.
- Follow Redirects: Each redirection is treated as a separate request and is recorded by JMeter.
- Use KeepAlive: If checked, Connection: keep-alive will be added to the request header when JMeter communicates with the target server.
- Use multipart/form-data for POST: If checked, requests will be sent by using multipart/form-data or application/x-www-form-urlencoded.

**9. Parameters**

​	JMeter will use parameter key-value pairs to generate request parameters and send these request parameters in different ways depending on the request method. For example, for GET, DELETE requests, parameters will be appended to the request URL.

**10. Message body data**

​	If you want to pass parameters in JSON format, you need to configure the Content-Type as application/json in the request header

**11. File upload**

​	Send the file in the request. The HTTP file upload behavior can be simulated in this way usually.

## Logic Controllers

The JMeter logic controller can control the execution logic of the components. The JMeter website explains it like this: 「Logic Controllers determine the order in which Samplers are processed」. That is to say, the logic controller can control the execution order of the samplers. Therefore, the controller needs to be used together with the sampler. Except for the once only controller, other logic controllers can be nested within each other.

Logic controllers in JMeter are mainly divided into two categories:

- Control the logical execution order of nodes during the execution of the test plan, such as loop controller, If controller, etc.
- Group the scripts in the test plan to facilitate JMeter to count the execution results and control the runtime of the scripts, such as throughput controller, transaction controller, etc.

### Transaction Controller

Sometimes, we want to count the overall response time of a group of related requests. In this case, we need to use the transaction controller.

The transaction controller will count the sampler execution time of all child nodes under the controller. If multiple samplers are defined under the transaction controller, the entire transaction can only be considered successful when all the samplers run successfully.

Add a transaction controller as shown below:

![JMeter Add a transaction](https://assets.emqx.com/images/82e32714189c1d56c90c7705cad91d3a.png)

The configuration items of the transaction controller are as follows:

1. Generate parent sample

   If checked, the transaction controller will be used as a parent sample for other samplers, otherwise, the transaction controller will only be used as an independent sample.

   ![JMeter Generate parent sample](https://assets.emqx.com/images/c400e4b3374cf8fc57865be65425c944.png)

   For example, the unchecked summary report is as follows:

   ![JMeter Generate parent sample 2](https://assets.emqx.com/images/0bba98959f7eb448d5c1d55408fff9f0.png)

   If checked, the summary report is as follows:

   ![JMeter Generate parent sample 3](https://assets.emqx.com/images/5c091921f0daa710ce40116bae8995e1.png)

2. include duration of timer and pre-post processors in generated sample：

   It specifies whether to include a timer. If checked, a delay will be added before and after the sampler runs.

### Once-only Controller

The once-only controller, as the name implies, is a controller that is executed only once, that is, the request under the controller is executed only once during the loop execution process under the thread group. For tests that require a login, you can consider putting the login request in a once-only controller, since the login request only needs to be executed once to establish a session.

Add a once-only controller:

![JMeter Add a once-only controller](https://assets.emqx.com/images/52e2a8b76ab101dd7ce789f379e36bd4.png)

If we set the loop count to 2 and check the result tree after running, we can see that the request "HTTP request 3" under the once-only controller is only executed once, and other requests are executed twice.

![JMeter Add a once-only controller 2](https://assets.emqx.com/images/ceafc74e7947284a5e64d38948c93de7.png)

## Listeners

A listener is a series of components used to process and visualize test result data. View Results Tree, Graph Results, and Aggregate Report are all listener components that we often use.

### View Results Tree

This component displays the result, request content, response time, response code and response content of each sampler in a tree structure. Viewing the information can assist in analyzing whether there is a problem. It provides a variety of viewing formats and filtering methods, and can also write the results to specified files for batch analysis and processing.

![JMeter View Results Tree](https://assets.emqx.com/images/ed6ffe8187537303ccf4c147ebda722f.png)

## Configuration Element

Configuration Element is used to provide support for static data configuration. It can be defined at the test plan level, or at the thread group or sampler level, with different scopes for different levels. Configuration element mainly includes User Defined Variables, CSV Data Set Config, TCP Sampler Config, HTTP Cookie Manager, etc.

### User Defined Variables:

![JMeter User Defined Variables](https://assets.emqx.com/images/3b4b9160e9925fbb992f9a275f876b3f.png)

By setting a series of variables, the random selection of values in the performance test is achieved. Variable names can be referenced within the scope, and variables can be referenced by ${variable name}.

In addition to the "User Defined Variables" component, variables can also be defined in other components, such as test plans and HTTP requests:

![JMeter test plan](https://assets.emqx.com/images/51b6d8f098b65757fe2418322315526d.png)

![JMeter HTTP Request](https://assets.emqx.com/images/43676402106a824e28d623d69f9d11e0.png)

For example, a defined variable is referenced in an HTTP request:

![JMeter HTTP Request2](https://assets.emqx.com/images/0783a9d22bbaf0bb916587c6c1a6867a.png)

Viewing the execution results, you can see that the value of the variable has been obtained:

![JMeter HTTP Request results](https://assets.emqx.com/images/3bafcfcc7dd24d36fb70eac5c42eb33c.png)

### CSV Data Set Config

During the performance test, we often need some parameterized input parameters, such as the username and password in the login operation. When the amount of concurrency is relatively large, the data generation at runtime will cause a great burden on the CPU and memory, and the CSV Data Set Config can be used as the source of parameters required in this scenario.

![JMeter CSV Data Set Config](https://assets.emqx.com/images/f60ec142f6e45dc87c275ddb097ccdbd.png)

The descriptions of some parameters in the CSV Data Set Config are as follows:

- Variable name: it defines the parameter name in the CSV file, which can be referenced in the script in the form of ${variable name} after the definition
- Recycle on EOF: if set to True, it allows looping again from the beginning when reaching the end of the CSV file
- Stop thread on EOF: if set to True, it stops running after reading the last record in the CSV file
- Sharing mode: it sets the mode shared between threads and thread groups

## Assertions

The assertion is to check whether there turn of the request is as expected. Assertion is an important part of automated test scripts, so we should pay great attention to it.

The assertions commonly used by JMeter mainly include Response Assertion, JSON Assertion, Size Assertion, Duration Assertion, Beanshell Assertion, etc. Here we only introduce JSON assertion that is used frequently.

### JSON Assertion

It is used to assert the content of the response in JSON format.

JSON assertion is added on an HTTP sampler in this example, as shown in the following image:

![JMeter JSON Assertion](https://assets.emqx.com/images/8be0a773cd6e8175f7cee3b97cedc43c.png)

JSON assertion has the following configuration items:

- Assert JSON Path exists
- Additionally assert value: Check if you want to assert based on the value
- Match as regular expression: Check if you want to assert based on regular expressions
- Expected Value
- Expect null: Check if NULL is expected
- Invert assertion

The 「root」 in the JSON path is always called `$`, which can be represented by two different styles, 「dot-notation」 (.) or 「bracket-notation」 ([]), such as `$.message[0].name` or `$['message'][0]['name']`.

Here is an example of requesting http://www.kuaidi100.com/query, where `$.message` represents the `message` in the response json object, checking `Additionally assert value` means to judge according to the value of `message`, and `Expected value` is `ok` to judge whether the value of `message` is `ok`.

![JMeter JSON Assertion 2](https://assets.emqx.com/images/6071d028eedca11b81b4ccedad804e8a.png)

Run the script, check the results, you can see that the assertion is passed.

![JMeter JSON Assertion 3](https://assets.emqx.com/images/cccad6019202b8ee3a5dde358727d9bc.png)

The judgments of the assertion mainly include the following conditions: if the response result is not in json format, it fails; if the json path cannot find the element, it fails; if the json path finds the element and no conditions are set, it passes; if the json path finds the element that does not meet the conditions, it fails; if the json path finds the element that meets the conditions, it passes; if the json path returns an array, it will iterate to determine whether any elements meet the conditions. If yes, it will pass, and if not, it will fail. Go back to "JSON Assertion" and check `Invert assertion`

![JMeter JSON Assertion 4](https://assets.emqx.com/images/fb48b8102c6a91a80c0ca4927329fff1.png)

Run the script, check the results, and you can see that the assertion failed

![JMeter JSON Assertion 5](https://assets.emqx.com/images/583efaef5c4fb6982e71a6dfd6343897.png)

## Timers

In the performance test, the pause time between requests is called thinking time. In real world, the pause time can be spent on content search or reading, and the Timer is used to simulate this pause:

- All timers in the same scope are executed prior to the samplers.
- If you want the timer to be applied to only one of the samplers, add the timer to the child node of the sampler.

JMeter timers mainly include Constant Timer, Uniform Random Timer, Precise Throughput Timer, Constant Throughput Timer, Gaussian Random Timer, JSR223 Timer, Poisson Random Timer, Synchronizing Timer, BeanShell Timer.

### Constant Timer

Constant timer means the interval between each request is a fixed value.

Adding a constant timer on a transaction controller is shown in the following figure:

![JMeter Constant Timer](https://assets.emqx.com/images/7c69a299ebc3a5901dc6683a1ae459f3.png)

After configuring the thread delay to 100 and 1000 respectively, run the script:

![JMeter Constant Timer 2](https://assets.emqx.com/images/1d1da9615cc37eaeb19fe6827c763a18.png)

Check the data in the table, where #1 and #2 are the running results when the configuration is 100 milliseconds, and #4 and #5 are the running results when the configuration is 1000 milliseconds. It can be seen that the interval between #4 and #5 is significantly longer than that between #1 and #2

![JMeter Constant Timer 3](https://assets.emqx.com/images/a3a61ca13267eb6406dd29e6ee14b7bc.png)

### Constant Throughput Timer

Constant throughput timer is used to control the execution of requests according to the specified throughput.

The following figure shows how to add a constant throughput timer on a transaction controller:

![JMeter Constant Throughput Timer](https://assets.emqx.com/images/bca182fb1c05b896870d3189484fc7c4.png)

Configure the target throughput as 120 (note that the unit is minutes), select "All active threads in current thread group (shared)" based on the calculated throughput

![JMeter Constant Throughput Timer 2](https://assets.emqx.com/images/100eb43b3f3263a58c46a2d61d39b94e.png)

Run the script, check the results, and you can see that the throughput is approximately 2/second (120/60)

![JMeter Constant Throughput Timer 3](https://assets.emqx.com/images/05b4e840a60bf893ed0fc4b426e59b0f.png)

## Pre-processors and Post Processors

The pre-processor performs some operations before the sampler request. It is often used to modify parameters, set environment variables, or update variables.

Similarly, the post-processor performs some operations after the sampler request. Sometimes the response data needs to be used in subsequent requests, and we need to process these response data. For example, if the jwt token in the response is obtained and used for authentication in subsequent requests, the post-processor will be used.


The above is the introduction of the main test components of JMeter, and you can try to use it in practice. In the next article, we will explain the use of the MQTT plugin in JMeter.
