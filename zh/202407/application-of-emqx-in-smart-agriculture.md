农业，人类历史上最古老的产业之一，正在经历着一场智能化变革。

通过运用数据、人工智能（AI）、遥感监测等先进技术，智慧农业在提升了产量和效率的同时，还有助于减少耕地和畜牧业对土地资源的消耗以及对环境的影响。智慧农业的实现涵盖了多个具体场景，包括精准农业、垂直农业、无人农场、农业机器人与无人机、智能灌溉、作物监测、病虫害防治、土壤管理以及智能温室等。

在中国农村人口迅速减少和全球气候变化的双重挑战下，发展智慧农业不仅是中国农业现代化的需要、更是保障国家粮食安全的一项关键战略。

然而，智慧农业的有效实施迫切需要一个既灵活又高效的数据管理体系，以支持智能化农业设备和各类传感器在农业生产中的运用。同时，农业数据本身并不直接创造价值，只有通过精确且实时的分析，才能有效辅助决策制定。目前，许多农业生产者还缺乏这方面的管理能力和技术条件。

## EMQX 接入平台: 智慧农业数据平台的核心组件

**EMQ 映云科技（以下简称"EMQ"）已助力全球多家农业企业，构造其智慧农业的数据系统。** 应用案例包括欧洲最大的垂直农场 Jones Food Company、加拿大垂直农业公司 Vertigrow、法国微气候数据服务商 Sencrop 、美国畜牧饲料个性化定制公司 Livestock Nutrition Center、意大利农业数字平台公司 xFarm 等等。这些公司利用 EMQ 的旗舰产品 EMQX Platform (以下简称"EMQX"）以及其他产品，打通了各类农业设备和后端数据系统的数据通道，实现数据驱动的智能化农业。

![欧洲最大的垂直农场 Jones Food Company](https://assets.emqx.com/images/f035e98f96e8fdd35cb2f2a2cf044592.png)

<center>欧洲最大的垂直农场 Jones Food Company 利用 EMQX 构建数据系统</center>

<br>

EMQX 是一款云原生分布式 MQTT 接入平台，它提供了高性能、可扩展和高可靠的消息传递架构，支持大规模设备的连接和实时消息传输。 

在智慧农业场景中，EMQX 作为农业数据系统的消息中间件，一方面负责对接各类农业设备的数据接入，另一方面提供丰富的数据集成功能。这使得各类农业生产数据在经过过滤、转换和预处理之后，能够顺利流入数据存储系统和农业数据分析软件。这样的流程确保了农业生产者能够获取实时、优质且精确的农业数据，进而助力于精准农业的实施和资源的优化配置。

![架构图](https://assets.emqx.com/images/a814763bcb365caa903599c277326f07.png)

EMQX 支持包括 MQTT、HTTP、WebSocket 等多种协议，确保了各种农业设备和系统的数据能够轻松接入。EMQX 内置强大的规则引擎，可对数据进行过滤、转换和丰富，以优化数据处理和存储流程。例如，EMQX 可根据预设的规则，从大量传感器设备收集的数据中筛选出关键数据，排除无关或冗余的信息，并在检测到异常生长等情况时，触发告警。最后，EMQX 对 40 多种数据库和数据分析工具的无缝集成支持，包括 Kafka、AWS RDS、MongoDB、 Oracle、SAP 以及时序数据库。 

<section class="promotion">
    <div>
        免费试用 EMQX Enterprise
            <div>无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?tab=self-managed" class="button is-gradient">开始试用 →</a>
</section>

## EMQX 在智慧农业场景中的应用

### **1. 数字农场管理平台**

- 数字农场管理平台为全球农民提供了一个全面的数字化农业解决方案，使农业生产者能够通过易于操作的应用程序（app），统一管理农田生产情况。这些平台通过实时监控作物生长状况、土壤条件、天气变化和设备状态，助力实现精准农业管理。
- **数据挑战：**数字农场管理平台的核心挑战在于整合农场运营的多维度数据，包括作物规划、田间监测和资源管理。这些数据来源多样，各类农业数据系统和设备使用不同的通信协议，构成复杂。整合这些碎片化的数据需要高度的技术适应性和兼容性，以确保数据的一致性和准确性。此外，数据的实时性对于快速决策至关重要，平台必须能够处理和分发实时数据流。
- **应用案例：**意大利农业科技公司 xFarm 专注于提供农业数字平台，利用从传感器、卫星影像和其他来源收集的数据，为农民提供有关灌溉、施肥、病虫害控制等洞察，帮助他们作出更精准的生产决策。xFarm 利用 EMQX 构建了其数字平台，实现农场管理任务的整合和数据的集中监控，让农民能够随时随地管理农场。EMQX 的灵活强大的多协议支持和数据集成功能，为数字农场管理平台提供了统一的数据通道，整合了不同种类的农业数据。同时，其高可用性和扩展性支持大规模并发消息传输，为数字农场管理平台提供稳定的消息服务。

![意大利农业科技公司 xFarm ](https://assets.emqx.com/images/3e80a6a0df9e1ce581946ae233683610.png)

<center>意大利农业科技公司 xFarm 利用 EMQX 构建其农业数字化 app</center>

### **2. 垂直农业**

- 垂直农业是一种在室内种植作物的前沿技术，它不依赖传统农田，而是利用 LED 灯模拟阳光，让植物在垂直堆叠的架子上生长。这种方式节省土地，减少用水量和污染。但这种高度控制的环境需要精确监测和调控各项生长参数。
- **数据挑战：**在垂直农业中，保持作物生长环境的精确控制是一项挑战。垂直农业生产者需要利用传感器和自动化系统实时监控和调节温度、湿度、光照等生长条件，处理分散、异构、大吞吐量的设备数据。
- **应用案例：**作为欧洲最大的垂直农场，Jones Food Company (JFC) 利用 EMQX 的低延迟、大吞吐量消息传输能力，结合 EMQ 的边缘端实时数采软件 NeuronEX，精确管理和控制种植进度，优化对环境控制设备的即时响应，确保作物生长条件的最优配置。JFC 在其室内种植空间（相当于 26 个网球场的大小）全年种植新鲜农产品，为当地超市和餐馆提供稳定的供应。

![欧洲最大的垂直农场 Jones Food Company](https://assets.emqx.com/images/5a199396f6bf33475aeef015d3eb7174.png)

<center>欧洲最大的垂直农场 Jones Food Company 在其农场中使用 EMQX 和 NeuronEX</center>

### **3. 气候数据**

- 气候数据服务在精准农业中发挥着至关重要的作用，为农民提供超本地化的微气候数据，帮助他们做出更明智的农业生产决策。
- **数据挑战：**精准农业的实施依赖于对气候条件的精确理解，这要求气候服务提供商能够获取和分析实时且精准的微气候数据，包括根据实时天气信息优化灌溉、害虫控制和种植时间表等。
- **应用案例：**法国农业科技公司 Sencrop 专注于为农民提供微气候数据。Sencrop 通过提供一系列气象监测智能设备和终端 app，帮助农民实时监测气候变化。这些气象设备和气象站可以放置在农场的不同位置，收集实时数据，如温度、湿度、风速、降雨量、太阳辐射、土地温度、土地湿度等。Sencrop 利用 EMQX 接入和传输各类气象站的数据，经过规则引擎等后端数据系统处理，最后传输到 Sencrop 的 app，让农民可以通过手机或电脑监测和分析天气情况，做出更好的作物保护、灌溉管理和收获时间决策，提高效率并减少环境影响。

![法国农业科技公司 Sencrop ](https://assets.emqx.com/images/8cff1a82063a61a40cc1aacc2649b1c0.png)

<center>法国农业科技公司 Sencrop 公司利用 EMQX 来管理其各类气象采集设备</center>

### 4. 个性化畜牧业

- 在畜牧业中，为不同类型的动物提供个性化的饲料配方是提升动物健康的关键，确保动物获得最佳营养平衡，促进其生长和健康。
- **数据挑战：**个性化饲料解决方案需要通过各类设备，综合分析动物的种类、生长阶段、健康状况以及营养需求，因此服务商往往面临大规模、分散和需要实时处理的数据。
- **应用案例：**美国畜牧饲料个性化定制公司 Livestock Nutrition Center 专注于为畜牧生产者制定和提供高质量的定制饲料和营养计划，满足牛、奶牛和其他畜牧业的特定需求。Livestock Nutrition Center 通过 EMQX 实现了对各类动物营养数据的实时采集和分析，帮助公司为畜牧生产者提供定制化的饲料配方。

![美国畜牧饲料个性化定制公司 Livestock Nutrition Center](https://assets.emqx.com/images/dddcaa5db83276a9b62ea978c6fc646c.png)

<center>美国畜牧饲料个性化定制公司 Livestock Nutrition Center 在其畜牧场中使用 EMQX</center>

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>