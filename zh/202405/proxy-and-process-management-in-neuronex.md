[NeuronEX](https://www.emqx.com/zh/products/neuronex) 是一款工业边缘网关软件，提供工业多协议接入与边缘计算能力。它主要部署在工业现场，用于工业设备通信、工业总线协议采集、数据集成、边端数据过滤分析、AI 算法集成以及工业互联网平台对接，为工业场景提供低延迟的数据接入管理及智能分析服务。

本文将重点介绍 NeuronEX 的反向代理和进程管理功能。反向代理可简化访问，提升安全性保护服务端，以及分配请求防止过载。进程管理可自动化启停和监控子程序，确保系统稳定性和可靠性。

## **反向代理功能**

NeuronEX 的两个核心模块是 Neuron 和 eKuiper。Neuron 负责支持 100 多种常见的工业协议数据接入能力，eKuiper 负责边缘端提供流式计算分析以及集成 AI 算法。

反向代理可对外提供一个统一接入地址，然后根据需要将请求发送到后端提供服务的端口，简化外部访问和管理的同时，也很好的保护内部服务器地址。NeuronEX 通过 Go 标准库的 `http` 工具包提供反向代理服务。 `http` 工具包提供的 `ReverseProxy `结构体可以创建到目标地址的 HTTP 连接，同时该结构体实现了 HTTP 的核心接口:

```
type Handler interface {
	ServeHTTP(ResponseWriter, *Request)
}
```

只需将原始请求的 `ResponseWriter`， `*Request` 参数赋值到 `ReverseProxy` 提供的 `ServeHTTP` 方法中，即可实现将原请求转发到特定后端服务端口的功能。那么如何区分应该把请求转发到 NeuronEX 模块下的 Neuron 还是 eKuiper 呢？关键在于识别请求路径中的特定前缀。因此，在 NeuronEX 的配置项中提供了如下设置，以支持流量的定向转发。

```shell
neuron:
  reverseProxies:
    - location: /api/neuron
      proxyPath: http://127.0.0.1:7000/api/v2

ekuiper:
  reverseProxies:
    - location: /api/ekuiper
      proxyPath: http://127.0.0.1:9081
    - location: /ws/ekuiper
      proxyPath: ws://127.0.0.1:10081
```

举例来说，假设 NeuronEX 所在机器地址为 hostname，对外暴露的端口号为 8085。对于获取 ekuiper 版本信息的请求，其完整路径为 `http://hostname:8085/api/ekuiper/version` ，经过代理层处理后，代理将向真正的后端地址 `http://127.0.0.1:9081/version` 发起请求。同样的，对于获取 Neuron 版本信息的请求，其完整路径为 `http://hostname:8085/api/neuron/version` ，经过代理层处理后，代理将向真正的后端地址  `http://127.0.0.1:7000/api/v2/version` 发起请求。由此可见，代理层能够根据请求路径中的特定前缀，识别并匹配到特定反向代理地址，然后将请求路径中的剩余路径与反向代理地址相结合，形成最终的访问地址。

![image.png](https://assets.emqx.com/images/d3913f91ddb80ff14de0a836e5625a2e.png)

## 进程管理功能

NeuronEX 负责启动并监控 Neuron 和 eKuiper 这两个核心模块。一旦发现任一软件异常退出，NeuronEX 将终止所有相关程序并退出。NeuronEX 通过 Go 标准库的 exec 工具包的 Command 方法启动子程序，以下示例以 Neuron 启动为例：

```
NeuronCmd := exec.Command("/bin/bash", "cd /opt/neuronex/software/neuron && ./neuron --disable_auth")
```

 `exec.Command` 方法的第一个参数是 shell 程序名，第二个参数是在 shell 中启动 Neuron 的命令行语句。将这两者结合后，得到的命令行语句用于在 shell 中执行 Neuron 的启动命令。通过调用 `NeuronCmd` 的  `Start` 方法来启动程序，随后调用 `Wait` 方法等待 Neuron 进程的退出。一旦 Neuron 进程退出，NeuronEX 进程在接收到信号后会立即退出。

程序正常启动后，可以通过在 Linux 命令行中执行 ps 命令查看程序的运行状态。这时可以观察到，通过此方法启动的 Neuron 和 eKuiper 的父进程为 NeuronEX。

![image.png](https://assets.emqx.com/images/f1e2da361407d47fc92245b0ce0a0346.png)

## 总结

通过 Neuron 和 eKuiper 两个功能模块，NeuronEX 在边端数据采集和数据处理功能之外，又增强了用户管理能力，方便运维人员操作。

凭借丰富的工业协议接入（80多种工业现场总线实时采集、100 多种驱动支持）、多源数据集成、流式计算分析、AI/ML 算法集成以及支持各类数据库与平台的数据转发存储，NeuronEX 可帮助工业企业打通数据孤岛、利用工业人工智能、提高设备健康管理、支持预测性维护以及增强数据安全性和实时监控能力。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
