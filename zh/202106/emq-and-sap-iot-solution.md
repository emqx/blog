## 背景

在气候保护全球合作的大背景下，中国政府积极推动2030“碳达峰”与 2060“碳中和”。“双碳”战略的达成将对中国经济社会发展带来深刻影响。相关行业企业面临转型升级的重大挑战，特别是能源电力、工业制造、交通等高碳排放的行业，必须通过更加精细、智能的数字化管理手段，对碳足迹加以把控，以实现在产业链各环节中的逐步脱碳。

为助力“碳中和”的早日实现和相关企业的竞争力重塑，SAP 与 EMQ 达成合作，双方将利用各自在智慧企业转型与物联网数据接入领域的技术优势，共同构建面向全产业链的碳排放数字化平台。借助数字化与物联网技术帮助企业进行能耗排放监控管理、产业转型升级和新能源产业数字化转型，为工业节能减排、风光发电清洁能源生产、新能源车联网等领域提供数字化解决方案。

该方案通过 EMQ X IIoT 套件规则引擎对接 SAP BTP 平台 Event Mesh 组件，传输碳中和相关数据到 SAP BTP 平台进行分析。

## EMQ X IIoT 套件

EMQ X IIoT 套件是一套接入与流数据预处理的工业物联网基础套件，套件包含多协议全网络设备接入能力的 EMQ X Neuron 和千万并发连接、百万数据吞吐的 EMQ X Enterprise 等组件。可依靠强大的规则引擎传输数据到各种数据平台，实现一站式的数据提取、筛选、转换和处理，与其它各类平台进行完美适配集成。同时支持可弹性扩展的集群模式，企业可以随着业务增长在客户无感知的情况下拓展接入规模，通过增加集群节点扩展业务上限。EMQ X IIoT 套件 灵活集成 SAP BTP 平台进行数据传输，提供可靠的碳达峰/碳中和源数据。

## SAP BTP 平台

SAP BTP 是打造智慧企业的平台，借助此平台，客户能够集成和扩展所有 SAP 和第三方的应用，化数据为价值，从而提升敏捷性、实现业务价值并推动持续创新。 SAP BTP 囊括了 SAP 的所有技术组合，例如 SAP HANA（内存计算平台）、SAP Analytics Cloud（分析云）、SAP Integration 套件 （集成套件）和 SAP Extension 套件（扩展套件）。SAP BTP 平台可以把 EMQ 采集的能耗数据转化成有价值的业务成果，更好地为碳达峰/碳中和提供有利的数据调整支撑。

## SAP & EMQ 碳中和集成方案 

在碳中和集成方案中，EMQ 提供了对工业能耗数据、生产制造过程数据、排放数据以及新能源生产等数据的实时采集接入，通过灵活的规则引擎把接入数据按业务需求进行过滤，处理，计算，通过高速实时的数据桥接，把有价值的数据通过 SAP Event Mesh 进一步分发到相应的消费组件，例如通过 SAP Analytics Cloud 或者 SAP HANA Cloud 把数据转化成碳中和分析数据，从而为企业与监管部门提供从生产制造到碳排量、碳足迹分析的一站式服务。

通过 EMQ X IIoT 套件采集数据后，利用 SAP BTP 平台的数据存储，数据处理和报表展现等能力，快速上线碳达峰/碳中和智慧解决方案。

![1.png](https://static.emqx.net/images/6447a8357d936882129272b305d6873f.png)     
**方案架构图**

---

**有关 SAP 账号权限、SAP BTP、Event Mesh 、SAC、EMQ 规则引擎使用等概念及要点可见官方文档：**


- [SAP 账号权限介绍](https://help.sap.com/viewer/bf82e6b26456494cbdd197057c09979f/Cloud/en-US/5499e2e74e674c69b057072272c80d4f.html)


- [SAP Event Mesh 介绍](https://help.sap.com/viewer/bf82e6b26456494cbdd197057c09979f/Cloud/en-US/ac83090b07684f8e908df40d024f8fe5.html)

- [SAC 介绍](https://help.sap.com/viewer/2b26a4d83a19437d8f07ac2f2234f34d/LATEST/en-US/627228f7e74040f981a873609c5eea09.html)

- [EMQ 规则引擎](https://docs.emqx.cn/enterprise/v4.3/rule/rule-engine.html)

---

1.启用 Cloud Foundry 环境，作为服务的运行容器，创建一个 Space
    
![2.png](https://static.emqx.net/images/90a57acd9abe58c1784c047350476135.png)




2.订阅 Event Mesh 服务，并在 Space 里面创建 Event Mesh 服务实例 

![3.png](https://static.emqx.net/images/8e936ef0099a0510bb7bfa2bc5a93668.png)



3.创建 Service Key， 创建 Queue， 基于 Service Key 生成 Token，使用 Token 进行 EMQ 的连接
![4.png](https://static.emqx.net/images/cbdcf1c07e22da616a10cc6af953af7b.png)     



4.配置 EMQ X 规则引擎，把数据输出到 SAP Event Mesh，目前是 EMQ 是通过 post API 的方式连接到 SAP Event Mesh，在 EMQ 下一个大版本里面，将更好与 SAP Event Mesh 集成，可以直接添加 SAP Event Mesh 资源，更加方便快捷。

![5.png](https://static.emqx.net/images/0a655e603ac80637b7e5fb59e16d7c25.png)       

![6.png](https://static.emqx.net/images/0dc6eb40065655043cbc3cb0196ce608.png)

5.查看 SAP Event Mesh 里面的数据，需要使用 Event Mesh 的 REST API 消费进行查询。

![7.png](https://static.emqx.net/images/3ab187eb9473d3a560d0624e9e76d64d.png)


6.存储在 SAP HANA Cloud 的能耗数据，可以供 SAP Analytics Cloud、S4/HANA，自开发 App 等应用消费展示。
![8.png](https://static.emqx.net/images/912a9fc63be2139e79abc46c8bf7ebfe.png)      

## 未来展望

随着 SAP 与 EMQ 深度合作，利用 EMQ 在 IoT 领域数据接入、预处理和分类存储等能力优势，SAP 在业务层把数据转化成对碳中和价值分析数据，通过对转化为标准碳排放的数据分析，在工业、运输能耗等领域进行碳排放管理，将对碳排放治理起到关键指导性价值。

“双碳战略”作为未来长期的战略方向，既是全球社会性的问题，也是经济效益问题。SAP 与 EMQ 的碳中和深度集成方案，不仅可以帮助企业完成转型升级，节约企业成本，还能通过带动绿色经济，提高全民的生活质量和身体健康，为数字化、绿色智能化建设技术赋能。

## 关于 SAP

SAP 于1972年在德国创立，是全球商业 软件市场的领导厂商，SAP 起源于Systems Applications and Products in Data Processing。SAP 既是公司名称，又是其产品——企业管理解决方案的软件名称。SAP 是目前全世界排名第一的 ERP 软件。另有，计算机用语 SAP，同时也是 Stable Abstractions Principle（稳定抽象原则）的简称。SAP 为全球第三大（根据市值排名）独立软件制造商。在全球120多个国家拥有10万+的企业客户，并在包括 欧洲、美洲、中东及亚太地区的50个国家雇用52000多名员工。