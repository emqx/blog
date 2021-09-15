Recently, **the IoT edge industrial protocol gateway software Neuron v1.3.2  was officially released.**

Neuron can access various industrial protocols and implement conversions between them. It can realize the functions of data collection, operational business logic services and alarm judgment, and upload and store data and alarms to the cloud platform. It supports one-stop platform gateway configuration management. All configurations, rules and labels are uniformly managed on the cloud platform. Through the deployment of Web services and client application software, it can realize the functions of equipment remote monitoring and remote maintenance, equipment performance management, equipment and asset management.

**Download link of the latest version:**

[https://www.emqx.com/en/downloads?product=neuron](https://www.emqx.com/en/downloads?product=neuron)



## Product logo officially launched

Starting from v1.3.2, Neuron officially has its own product logo, which is displayed on the login interface and the upper left corner of the user interface. The logo is simple in design. The two up and down arrow-shaped icons represent the northbound and southbound data flows, while Neuron connects the northbound data and southbound data to provide a smooth data path for industrial scenarios.



![Neuron-Logo](https://static.emqx.net/images/acae68ba4be1727662893e60b82fe3fa.png)

![Neuron Login](https://static.emqx.net/images/34c2d2334d8b1b98ed1288b6892e681a.png)


## New user interface

In this version, we have updated the user interface of Neuron. The new interface takes white as the main background color to make all the information and numbers more clear and easy to see, which gives users a refreshing feeling.

![Neuron data monitoring](https://static.emqx.net/images/82873d31a03bf0285b0150f59270fda8.png)

## Collaboration with the management console

At present, Neuron v1.3.2 has been highly coordinated with the management console application of EMQ in the cloud. Users can directly control Neuron through the console, and can configure and monitor it by calling Neuron's API.

## Fixes and features

- The original code structure is optimized, and high concurrency calls to HTTP API no longer leads to web service memory competition;

- The size of object size is no longer limited on the interface;

  ![Neuron object size](https://static.emqx.net/images/b4ec5171909960c764cff095cb4609a7.png)

- The unit mark of read time is added on the interface, and the unit is 100ms.

  ![Neuron read time](https://static.emqx.net/images/fbac64f3678be2903cc798de533c8ecc.png)

## Contact

If you have any questions about Neuron, please feel free to contact us via [neuron@emqx.io](mailto:neuron@emqx.io).

