在[本系列文章的上一篇](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter)中，我们介绍了开源测试工具 JMeter，并以一个简单的HTTP测试为例一窥JMeter的能力。在本篇文章中，我们将进一步介绍JMeter丰富的组件，以帮助大家构建复杂场景的测试脚本。

JMeter的测试脚本在界面中以「树」的形式呈现，保存后的测试脚本jmx文件本身也是xml格式。JMeter脚本树以测试计划(Test Plan)为根节点，所有的测试组件都会被包含在测试计划中。测试计划中可以配置被整个测试计划中的组件调用的自定义变量、线程组运行模式、测试中使用的库文件等。

在测试计划中使用多种测试组件，就可以构建丰富的测试场景。JMeter中的测试组件大致有以下几类：线程组、取样器、逻辑控制器、监听器、配置元件、断言、定时器、前置处理器、后置处理器。接下来将分别介绍，并对主要的组件进行详细说明。

## 一、线程组

线程组元件是所有测试计划的入口。所有的取样器和控制器必须放在线程组下。一个线程组可以看作一个虚拟用户池，其中的每个线程都可以理解为一个虚拟用户，多个虚拟用户同时去执行相同的一批次任务。每个线程之间都是隔离的，互不影响的。一个线程的执行过程中，操作的变量不会影响其他线程的变量值。

线程组的界面如下图：

![JMeter线程组](https://static.emqx.net/images/a9cd09784f960db56f94a9ce3c5a9c94.png)

在线程组界面中可以设置以下数据，进行线程组的控制：

### 取样器错误后要执行的动作

这几个配置项控制了「当遇到错误的时候测试的执行策略」是否会继续执行。

- 继续：忽略错误，继续执行
- 启动下一进程循环： 忽略错误，线程当前循环终止，执行下一个循环。
- 停止线程：当前线程停止执行，不影响其他线程正常执行。
- 停止测试：整个测试会在所有当前正在执行的线程执行完毕后停止
- 立即停止测试：整个测试会立即停止执行，当前正在执行的取样器可能会被中断。

### 线程数

线程数也就是并发用户数，每个线程将会完全独立地运行测试计划，互不干扰。测试中使用多个线程用于模仿对服务器的并发访问。

### ramp-up时间

ramp-up时间用于设置启动所有线程所需要的时间。例如：线程数设置为10，ramp-up时间设置为100秒，那么JMeter将使用100秒使10个线程启动并运行，每个线程将在前一个线程启动后的10秒启动。

如果ramp-up值设置得很小、线程数又设置得很大，刚开始执行测试时会对服务器产生很大的压力。

### 循环次数

设置结束前线程组中每个线程循环的次数。

### 延迟创建线程直到需要

默认情况下，测试开始的时候，所有线程就全部创建了。如果勾选了此选项，那么线程在需要用到的时候才创建。

### 线程组调度器

调度器配置可以更灵活地控制线程组执行的时间

（1）持续时间：控制测试执行的持续时间，以秒为单位。

（2）启动延迟：控制测试在多久后启动执行，以秒为单位。

## 二、取样器

取样器是用来模拟用户操作的，是向服务器发送请求、接收服务器响应数据的运行单元。取样器是包含在线程组内部的组件，因此它必须在线程组中添加。JMeter原生支持多种不同的取样器，如TCP取样器、HTTP请求、FTP请求、JDBC请求、Java请求等，每一种不同类型的取样器根据设置的参数向服务器发出不同类型的请求。

### TCP取样器

TCP 取样器通过TCP/IP来连接指定服务器，连接成功后向服务器发送消息，然后等待服务器回复。

界面如图：

![JMeter取样器](https://static.emqx.net/images/485d116a3ffd4b72c8618f51f449f1a3.png)

TCP取样器中可以设置的属性有：

**1.TCPClient classname**

表示处理请求的实现类。缺省使用org.apache.jmeter.protocol.tcp.sampler.TCPClientImpl, 使用普通文本进行传输。此外JMeter还内置支持BinaryTCPClientImpl和LengthPrefixedBinaryTCPClientImple， 前者使用十六进制报文，后者在BinaryTCPClientImpl的基础上增加了2个字节的长度前缀。

也可以通过继承org.apache.jmeter.protocol.tcp.sampler.TCPClient来提供自定义的实现类。

**2.目标服务器设置**

「服务器名称或IP」和「端口号」指定了服务器应用的主机名/IP地址和端口号。

**3.连接选项**

- Re-use connection：: 如果选中，这个连接会一直处于打开状态，否则读取到数据后就关闭。
- 关闭连接：如果选中，这个连接在TCP取样器运行完毕之后就会被关闭。
- 设置无延迟：如果选中，Nagle算法将被禁用，允许小数据包的发送。
- SO_LINGER：用于控制在关闭连接之前是否要等待缓冲区中的数据发送完成。
- 行尾 (EOL)字节值：用于判断行结束的字节值，如果指定的值大于127或者小于-128，会跳过EOL检查。比如服务器端返回的字符串都是以回车符结尾，那么我们可以将该选项设置成10

**4.超时时间：**

- Connect Timeout：连接超时
- Response Timeout：响应超时

**5.要发送的文本**

请求发送的报文文本

**6.登陆配置**

设置连接使用的用户名和密码

### HTTP请求取样器

HTTP取样器向web服务器发送HTTP/HTTPS请求。

![JMeter HTTP请求](https://static.emqx.net/images/763f30e5663b4116a2584e4a6111ef49.png)

**1.名称和注释**

**2 .请求协议**

向目标服务器发送请求时使用的协议，可以是HTTP、HTTPS或FILE，默认为HTTP。

**3.域名或IP地址**

请求发送的目标服务器名称或IP地址。

**4.端口号**

Web服务监听的端口号，HTTP默认端口为80，HTTPS默认端口443。

**5.请求方法**

发送请求的方法，常用GET、POST、DELETE、PUT、TRACE、HEAD、OPTIONS等。

**6 .路径**

要请求的目标URL路径（不包括服务器地址和端口）。

**7.内容编码**

适用于POST、PUT、PATCH和FILE这几种请求方式，对请求内容进行编码的方法

**8.更多请求选项**

- 自动重定向：重定向不会被视为单独的请求，不被JMeter记录。
- 跟随重定向：每次重定向都被视为单独的请求，都会被JMeter记录。
- 使用KeepAlive：如果选中，JMeter和目标服务器之间通信时会在请求头中加入Connection: keep-alive。
- 对POST使用multipart/form-data：如果选中，将使用multipart/form-data 或 application/x-www-form-urlencoded发送请求。

**9.参数**

JMeter将使用参数键值对来生成请求参数，并根据请求方法以不同方法发送这些请求参数。例如：GET，DELETE请求，参数会附加到请求URL。

**10.消息体数据**

如果希望传输JSON格式的参数，需要在请求头中配置Content-Type为application/json

**11.文件上传**

在请求中发送文件，通常HTTP文件上传行为可以通过这种方式模拟。

## 三、逻辑控制器

JMeter 逻辑控制器可以对元件的执行逻辑进行控制，JMeter 官网是这样解释的：「Logic Controllers determine the order in which Samplers are processed」。也就是说逻辑控制器可以控制采样器(samplers)的执行顺序，因此控制器需要和采样器一起使用。除仅一次控制器外，其他逻辑控制器可以相互嵌套。

JMeter 中的逻辑控制器主要分为两类： 

- 控制测试计划执行过程中节点的逻辑执行顺序，如：循环控制器、If 控制器等；
- 对测试计划中的脚本进行分组、方便 JMeter 统计执行结果以及进行脚本的运行时控制等，如：吞吐量控制器、事务控制器。

### 事务控制器

有时候我们想统计一组相关请求的的整体响应时间，这种情形就需要借助事务控制器。

事务控制器会对该控制器下所有子节点的取样器执行消耗时间进行统计。如果事务控制器下定义了多个取样器，所有取样器都运行成功时，整个事务才能算成功。

如下图添加事务控制器：

![JMeter事务控制器](https://static.emqx.net/images/77116aa03df5d0ce7b55cc14bba0bdba.png)

事务控制器的配置项有：

**1.Generate parent sample**

如果选中，事务控制器将作为其他取样器的父级样本，否则事务控制器仅作为独立的样本。

例如，未勾选情况下汇总报告如下：

![JMeter事务控制器](https://static.emqx.net/images/21741fb9f7f35bbf47b8addc7bbbe7b4.png)

勾选情况下汇总报告如下：

![JMeter汇总报告](https://static.emqx.net/images/25efe79c708fb2b35783bf369f707be9.png)

**2.include duration of timer and pre-post processors in generated samle：**

指定是否包含定时器，如果勾选将在取样器运行前与运行后加上延时。

### 仅一次控制器

仅一次控制器，顾名思义就是只执行一次的控制器，即在线程组下的循环执行过程中对该控制器下的请求只执行一次。对于需要登录的测试，可以考虑将登录请求放在仅一次控制器中，因为登录请求只需执行一次即可建立会话。

如下图添加仅一次控制器：

![JMeter仅一次控制器](https://static.emqx.net/images/01350c39bd6f52b8e3deb13c93be2dd8.png)

如果我们将线程组循环次数设置为 2，运行后查看结果树，可看到仅一次控制器下的请求“HTTP请求3”只执行了1次，其它请求执行了2次

![JMeter控制器](https://static.emqx.net/images/4dc10693a833c2ca46dd27861e86ee5b.png)
 

## 四、监听器

监听器是用于对测试结果数据进行处理和可视化展示的一系列元件。察看结果树、 图形结果、聚合报告等都是我们经常用到的监听器组件。

### 察看结果树

该组件以树形结构展示了每一个取样器的结果、请求内容、响应时间、响应码、响应内容等信息，查看这些信息可以辅助分析是否存在问题。它提供多种的查看格式和筛选方法，也可以将结果写入指定文件进行批量分析处理。

![JMeter查看结果树](https://static.emqx.net/images/7847b38aa19d7631a13b5550aabedafe.png)

## 五、配置元件

配置元件用于提供对静态数据配置的支持。它可以定义在测试计划层级下，也可以定义在线程组或取样器层级下，定义在不同层级，作用域也不同。配置元件主要有用户自定义变量、CSV数据文件设置、TCP取样器配置、HTTP Cookie管理器等。

### 用户自定义变量

![JMeter 用户自定义变量](https://static.emqx.net/images/b21042455b532544192e3083fc848d5d.png)

通过设置一系列的变量，达到在性能测试过程中可以随机选取变量的目的。变量名可以在作用域内引用，通过${变量名}方式来引用变量。

除了“用户自定义变量”这个组件外，测试计划和HTTP请求等多个组件中也可以定义变量：

![JMeter 测试计划](https://static.emqx.net/images/57d2725b5091fbbc6601b8103baa6e33.png)

![JMeter HTTP 请求](https://static.emqx.net/images/3148af4c0e9af654580aad09061e476f.png)

例如：在HTTP请求中引用了已定义的变量：

![JMeter HTTP 请求自定义变量](https://static.emqx.net/images/8f849f2ce19433d17af58dc3a17c3262.png)


查看执行结果，能看到确实获取到了变量的取值：

![JMeter 查看执行结果](https://static.emqx.net/images/17039b4f32149ebb3022e3adcb8ff6af.png)

### CSV数据文件设置

在性能测试过程中我们往往需要一些参数化的输入参数，比如登录操作里面的用户名密码。当并发量比较大的时候 ，运行时生成数据会对CPU和内存造成较大的负担，而CSV数据文件配置可以作为这种场景下所需的参数来源。

![JMeter CSV数据文件设置](https://static.emqx.net/images/3328c7c6b1ce8a96549dc610ec5578ff.png)

CSV数据文件设置中部分参数的说明如下：

- 变量名称：定义CSV文件中的参数名，定义后可在脚本在以${变量名}的方式引用
- 遇到文件结束符再次循环：如果设置为True，允许对CSV文件循环取值
- 遇到文件结束符停止线程：如果设置为True，则读取完CSV文件中的记录后停止运行
- 线程共享模式：设置在线程及线程组间共享的模式

## 六、断言

断言即检查接口的返回是否符合预期。断言是自动化测试脚本中举足轻重的一环，因此要十分重视。

JMeter 常用断言主要有响应断言（Response Assertion）、JSON断言（JSON Assertion）、大小断言（Size Assertion）、断言持续时间（Duration Assertion）、beanshell 断言（Beanshell Assertion）等，这里我们只介绍经常要用到的 JSON断言。

### JSON 断言

用于对 JSON 格式的响应内容进行断言。

下图在一个HTTP取样器上添加 JSON 断言：

![JMeter JSON 断言](https://static.emqx.net/images/e4ae8f84eb75360cede582bb2861edd2.png)

JSON断言配置项有：

- Assert JSON Path exists：需要断言的 JSON 表达式
- Additionally assert value：如果要根据值去断言，请勾选
- Match as regular expression：如果要根据正则表达式去断言，请勾选
- Expected Value：期望值
- Expect null：如果期望是 null 则勾选
- Invert assertion：取反

其中 JSON path 中的「根成员对象」总是被称为`$`，可以通过 「dot–notation」（.号）或 「bracket–notation」（[]号）这两种不同的风格来表示，比如 `$.message[0].name` 或 `$['message'][0]['name']`。

下面以请求 http://www.kuaidi100.com/query 为例，其中 `$.message` 表示响应 json 对象的中 `message`，勾选 `Additionally assert value` 表示要根据 `message` 的值去判断，`Expected value` 为 `ok` 表示判断 `message`的值是否为 `ok`。

![JMeter 请求结果](https://static.emqx.net/images/dc584e85b999283e68f3122f77155eac.png)

运行脚本，查看结果，可看到断言是通过的

![JMeter断言通过](https://static.emqx.net/images/c735868f82ef5fb488e8ebe3e43f14a8.png)

断言的判断条件主要包括：如果响应结果不是 json 格式的，失败；如果 json path 找不到元素，失败；如果 json path 找到元素，没有设置条件，通过；如果 json path 找到元素，但不符合条件，失败；如果 json path 找到元素，且符合条件，通过；如果 json path 返回的是一个数组，会迭代判断是否有元素符合条件，有则通过，没有则失败。回到“JSON断言”，勾选 `Invert assertion`

![JMeter断言](https://static.emqx.net/images/3b610e2ad1f89055bd5729826faa82c1.png)

运行脚本，查看结果，可看到断言是失败的

![JMeter断言失败](https://static.emqx.net/images/9ad9c54de71e490aaccd4051881c9417.png)

## 七、定时器

在性能测试中，访问请求之间的停顿时间被称之为思考时间。在实际操作中，停顿时间可以是内容查找、阅读等花费的时间，而定时器正是用来模拟这种停顿时间。其中：

- 同一作用域下的所有定时器优先于 取样器之前执行。
- 如果希望定时器仅应用于其中一个取样器，则把定时器加入到该取样器的子节点。

JMeter定时器主要包括：固定定时器（Constant Timer），统一随机定时器（Uniform Random Timer），精准吞吐量定时器（Precise Throughput Timer），常数吞吐量定时器（Constant Throughput Timer），高斯随机定时器（Gaussian Random Timer），JSR223 定时器（JSR223 Timer），泊松随机定时器（Poisson Random Timer），同步定时器（Synchronizing Timer），BeanShell 脚本编写定时器（BeanShell Timer）。

### 固定定时器

固定定时器，即配置每个请求之间的间隔时间为固定值。

下图在一个事务控制器上添加固定定时器：

![JMeter固定定时器](https://static.emqx.net/images/c31f586f340137ae74ace3baaa19acb8.png)

将线程延迟分别配置为 100 和 1000后，运行脚本

![JMeter运行脚本](https://static.emqx.net/images/72543ccf59a6e58a49ec522df5f67ce7.png)

查看表格结果中的数据，其中1、2是配置为 100 毫秒时的运行结果，4、5是配置为 1000 毫秒时的运行结果，可看到 4、5 的间隔时间明显比 1、2 的间隔时间长

![JMeter运行结果](https://static.emqx.net/images/0116363f71b3f38f17970aa4b3e4dff0.png)

### 常数吞吐量定时器:

常数吞吐量定时器用于控制请求按指定的吞吐量去执行。

下图在一个事务控制器上添加常数吞吐量定时器：

![JMeter常数吞吐量定时器](https://static.emqx.net/images/745e97e7ba5133e578b93524ff66b82c.png)

配置目标吞吐量为 120（注意单位是分钟），基于计算吞吐量选择“当前线程组中的所有活动线程（共享）”

![JMeter常数吞吐量定时器](https://static.emqx.net/images/1f16386de8c081d432519a4fb73b0772.png)

运行脚本，查看结果，可看到吞吐量基本维持在 2/每秒（120/60）

![JMeter运行结果](https://static.emqx.net/images/ec2021f0f4cdd022cd7de7ba53d72034.png)

## 八、前置处理器和后置处理器

前置处理器是取样器请求之前执行一些操作，经常用于在取样器请求运行前修改参数，设置环境变量，或更新未从响应文本中提取的变量。

同样的，后置处理器是在取样器请求之后执行一些操作。有时候服务器的响应数据在后续请求中需要用到，我们就需要对这些响应数据进行处理。比如获取响应中的jwt token，在后续请求中使用以进行身份验证，这时就会使用后置处理器。

 

以上就是JMeter主要的测试组件介绍，大家可以在实战中尝试使用。下期文章我们将讲解 JMeter 中的 MQTT 插件使用。

## 本系列中的其它文章

- [开源测试工具 JMeter 介绍 - 物联网大并发测试实战 01](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 03](https://www.emqx.com/zh/blog/how-to-use-the-mqtt-plugin-in-jmeter)
- [JMeter MQTT 在连接测试场景中的使用 - 物联网大并发测试实战 04](https://www.emqx.com/zh/blog/test-mqtt-connection-with-jmeter)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 05](https://www.emqx.com/zh/blog/the-use-of-jmeter-mqtt-in-subscription-and-publishing-test-scenarios)
