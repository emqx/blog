## Introduction

The IoT industry is developing explosively. As the scale of endpoints continues to grow and business logic becomes more complex, it is necessary to verify the availability and reliability of the platform when a large number of devices are connected before the IoT platform is officially launched, so as to ensure system quality. Therefore, the value and necessity of [IoT performance test](https://www.emqx.com/en/products/xmeter) are gradually highlighted.

On the one hand, performance test provides a basis for evaluating IoT systems, which can be verified from multiple dimensions of design indicators, scalability and reliability. On the other hand, performance test also helps to optimize IoT systems and find system performance bottlenecks as soon as possible, so as to provide optimization suggestions. In addition, performance test can also assist the formulation of capacity plans and provide a reference for future capacity expansion plan.

The IoT system has the features of large amount of access devices, diverse protocols, complex integration architecture, and frequent cross-departmental development collaboration, which also makes the IoT performance test face many challenges. **This series of articles will take the IoT platform based on [EMQX](https://www.emqx.io) as an example to introduce how to use performance test tools to verify and test platform-related quality indicators.**

## Selection of the test tool -- Introduction to JMeter

We choose JMeter as the test tool for this time.

JMeter is an open-source software of the Apache Foundation. It mainly implements performance test by simulating concurrent loads, which is currently the mainstream performance test tool in the open-source community. It mainly has the following advantages:

- With built-in support for multiple protocols in test, such as TCP, HTTP/HTTPS, etc.
- Provide a flexible plug-in extension mechanism and support third-party extensions of other protocols. For a wide variety of protocols in the IoT system, it is only required to customize and develop the required protocol business logic according to the framework requirements of JMeter, which can be easily put it into the JMeter's plug-in library and be tested by the existing capability of JMeter.
- With good community support.

## Installation of JMeter

At present, the latest stable version of JMeter is 5.4.3. Since JMeter is based on Java, Java 8 and above needs to be pre-installed to support JMeter 5.4.1 (that is available from the following address: [https://www.oracle.com/java/technologies/downloads](https://www.oracle.com/java/technologies/downloads)).

After installing Java, download JMeter from the website：[https://jmeter.apache.org/download_jmeter.cgi](https://jmeter.apache.org/download_jmeter.cgi)

After the download, decompress it and enter the bin subdirectory of the decompressed directory. Depending on the operating system, run jmeter.bat (Windows system) or jmeter (Unix system). If everything goes well, JMeter's script editing interface will be presented to you:

![JMeter](https://assets.emqx.com/images/8c0762b8342ab42ec2c5c9051525bc47.png)

Next, let's take HTTP as an example to see how to use JMeter to build and run a simple test case.

1. Add a virtual user group (Thread Group): Right-click on the test plan > Add > Threads (Users) > Thread Group

   ![JMeter Add Thread Group](https://assets.emqx.com/images/d2932f0be1273de1c977ce85437f6465.png)

   JMeter uses a single thread to simulate a user, and a Thread Group refers to a group of users as a virtual user group simulating access to the system under test.

   「Number of Threads」 in 「Thread Properties」 can be used to configure the number of concurrent users in a virtual user group. The higher the value, the greater the amount of concurrency; 「Loop Count」 can be used to configure how many tests each virtual user performs.

   ![JMeter Thread Properties](https://assets.emqx.com/images/e5d5e8c0c14d97c3c340acbb9808e56a.png)

2. Add the HTTP page under test: Right-click on the Thread Group > Add > Sampler > HTTP Request

   ![JMeter Add the HTTP page](https://assets.emqx.com/images/28f9382ea3c9eaaaeec6fe6cbdd6334a.png)

   In the sample test script, we only use the default HTTP request settings to initiate an HTTP request to the bing website. You can configure it according to the actual situation.

   ![JMeter HTTP request](https://assets.emqx.com/images/ab4e18dd509091a73fdc09227f509e6b.png)

3. Add a result listener: Right-click on the thread group > Add > Listener > View Results Tree

   The listener is not necessary in the actual performance test, but it can help you see the test results intuitively and facilitate debugging in the process of writing scripts. In this sample script, we will use 「view result tree」 to help view the response information of the request.

   ![JMeter Add a result listener](https://assets.emqx.com/images/63ad7b6386eec1a26a8ba8e794cda6e8.png)

4. Run the test

   After saving the test script, click the 「Start」button in the operation bar to run the test script. It is recommended that the number of threads and the loop count in the thread group be set smaller (such as within 10) to avoid being banned.

   ![JMeter Run the test](https://assets.emqx.com/images/29baf88be6fc46c19ba4327882c7d30b.png)

Now, we have completed a simple HTTP test script. You can draw inferences from this case and try other protocols. In the next article, we will introduce the various test components of JMeter in more detail, which can be used together to build more complex test scenarios.
