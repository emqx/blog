在当前的 AI 发展浪潮中，人工智能技术正以前所未有的速度重塑着人类的生产与生活方式。从最初基于文本的大语言模型，到支持语音、图像、视频等多模态交互的智能系统，AI 已经与各类应用软件和各行业的生产力工具深度融合，极大提高了用户使用体验与工作生产效率。然而，由于 AI 对算力有着极高的需求，且其交互方式在精准度、自然度以及适配多样性场景等方面存在一定的复杂性，在消费电子产品领域，AI 技术仍未实现规模化应用。 

作为领先的 MQTT 平台，EMQX 广泛应用于消费电子产品的 IoT 接入场景，能够实现现实世界与应用服务之间的连接。本文将探讨如何利用现有 IoT 技术框架，实现创新且友好的消费电子智能化场景。

**Demo 录屏：**[**https://lidnp.xetlk.com/s/2UWEKw**](https://lidnp.xetlk.com/s/2UWEKw)

## AI 大模型在消费电子产品领域的优势

在 AI 大模型广泛应用之前，消费电子产品依赖于传统的规则和意图识别技术，能够提供一些简单的智能化功能。但这种方案需要大量人工标注训练数据和编写意图匹配规则，难以应对复杂场景，且开发成本高昂。

引入 AI 大模型后，消费电子产品可以通过其强大的自然语言理解、多模态数据处理和上下文感知能力，提供更加智能的交互体验。其优势包括：

- **增强的自然语言处理**：无需严格和固定的指令格式，支持语音、文本、图像等多模态输入，提供更加流畅和准确的交互。
- **场景理解和自适应能力**：能够根据用户的使用习惯和当前所处场景，给出更加智能与个性化的响应。
- **低成本的定制化部署：**现有 AI 大模型成本更低，企业能在其基础上训练特定的人工智能方案，优化大模型的适应性与性能。

此外，AI 大模型还能持续学习新的数据和知识，随着时间的推移，不断优化消费电子产品的交互体验，为用户提供始终领先且贴合需求的交互服务 。

## 利用 EMQX 连接设备与 AI 服务

在探讨物联网与 AI 服务融合之前，我们先了解一下消费电子领域物联网数据流程：

设备借助网络连接与 EMQX Platform 建立通信，通过上行数据将设备采集到的各类信息，如传感器数据、设备状态等，传输至 EMQX Platform 并集成到业务应用中；同时，通过下行数据接收来自业务应用的指令，如设备控制指令、参数调整指令等。凭借这样的数据交互，驱动各类业务，实现多样化应用场景 。

这个过程中，最重要的环节就是实现数据的接入上云。从方案架构角度来看，设备通常采用两种接入方式：

- **直接接入**：通过 WIFI 或 5G 模组与云端直接建立连接。常见于智能冰箱、智能电视、监控摄像头等具备持续稳定的电源供应能力的电子设备。
- **网关接入**：先通过使用蓝牙、ZigBee 等协议的网关建立连接，然后由网关将数据转换并上传至云端。常见于智能门锁、传感器等低功耗设备。

![EMQX+AI](https://assets.emqx.com/images/aac7b61a9758c7925daa6abf1fec9317.png)

由于 EMQX 具有高性能、低延迟、灵活数据格式的消息传输能力，AI 推理计算所依赖的各类传感器和交互数据，以及 AI 推理结果的下发可以在这个架构下高效传输。

借助边缘计算概念，可以采用 AI 分层计算方案进一步提高数据处理效率，以增强用户体验：

1. **MCU 上的轻量级 AI**

   如果设备搭载具有 AI 推理能力 MCU，可以的设备结合轻量级 AI 技术，快速处理特定场景中简单任务，例如：

   - **语音识别**：将语音信号转换为特定的设备指令，或者进行有限的语音-文本转换；
   - **动作识别**：通过 YOLO 模型等机器学习神经网络，识别摄像头捕捉到的特定场景，并将其转化为动作或者指令。

1. **边缘网关的小型人工智能模型**

   边缘网关拥有较为强大的计算能力，能够处理更为复杂多样的任务，例如：

   - **多模态数据处理**：基于 Phi-3.5-vision 等多模态小模型，整合并分析文本、语音、图像以及视频流等数据，实现更精准地识别和处理。
   - **支持脱机运行**：在网络连接中断的条件下确保关键业务的持续运行。

1. **云端的大型人工智能模型**

   基于云端强大的计算资源以及完整大模型能力，实现多模态数据的深度处理和复杂任务的解决，例如：

   - 深度理解和分析自然语言，精准把握人类通过语音传达的意图。
   - 整合和挖掘来自不同设备的多模态数据，提供全面且智能的指令。

在以上场景中，无论是设备采集到的原始数据，还是经过 AI 模型处理后生成的事件与指令数据，都可以基于 MQTT 协议通过 EMQX 传输到云端。EMQX 实现了物理设备与人工智能之间的无缝集成，能够快速响应复杂的用户请求，提高用户体验和整体效能。

## AI 驱动的创新交互场景

AI 技术正在为消费电子产品带来前所未有的机遇，使其从基本的智能设备发展成为真正的智能伴侣。 通过情境感知、多模态交互和高级自动化等功能，人工智能重新定义了用户与设备之间的互动方式。 以下是三个关键的智能交互场景：

### **深度理解和智能交互**

**智能交互的本质是深度解读用户的真实需求，而非机械地将用户指令映射为设备动作。**

例如，目前市场中的空调产品可以通过语音实现开启、模式设定等基本操作，但用户往往需要进行多次交互才能满足自身对环境舒适度的要求。

借助 AI 技术，大模型可以依据当前室内的实时温度、湿度以及其他环境数据，结合用户长期以来形成的个性化使用习惯，精准地对空调的运行模式与温度设定进行调整，只需一次交互就能为用户营造出舒适的室内环境氛围。

### **场景探索与功能推广**

**AI 技术能够识别和分析用户行为习惯，实现不同家居设备之间的智能协同运作。**

例如：当洗衣机完成洗衣任务后，用户通常会降下晾衣架以便晾晒衣服，AI 大模型可以识别并记录这一使用习惯，并提醒用户进行一键式联动规则设置。

与传统模式相比，用户无需手动在 App 中探索功能并编排规则，避免了繁琐低效的操作。这种创新的需求挖掘与便捷设置方式，全方位适配了多样化场景中的用户习惯与实际需求，显著提升便利性的同时，增强了用户对产品的使用粘性，降低了新功能的推广难度，进一步提升了企业的市场竞争力。

### **多模态数据驱动的创新**

**随着多模态人工智能的发展，全新的数据输入方式与多样化的智能交互场景不断涌现。**

例如：智能冰箱能够通过内置摄像头精准识别所储存的各类物品，实现智能工作模式调节、菜品保鲜期提醒等功能，并支持将数据共享给用户授权的菜谱应用；未来，这些数据还可以与智能家庭机器人对接，实现用户指令的智能判断和操作执行，提高了家居服务的效率与精准度。

借助设备开放的传感器和执行器接口，结合 AI 大模型的自然语言理解以及智能规则，消费电子产品企业可以深入挖掘并探索各种丰富且个性化的交互场景，进一步推动智能化生态的发展与完善，满足消费者多样化的使用需求。

## EMQX + AI  智能交互演示

基于 EMQX 面向消费电子产品的 MQTT 平台及 AI 融合架构，本节将展示 EMQX 与 AI 大语言模型的深度集成，实现设备与用户之间智能、高效的实时互动。

### 技术选型

- 设备层：使用 MQTTX 或者 MQTTX CLI 模拟设备发送消息。具体指令和场景请参考下文。
- MQTT 接入平台：EMQX Platform
- AI 大模型：基于 Azure AI 提供的 GPT-4o 模型
- Agent 层：使用 Node.js 开发

### 架构介绍

EMQX 充当接入层，将设备、边缘网关数据接入云端，并与 Agent 进行集成。Agent 通过预设的提示词，使用 EMQX 发送过来的数据调用云端大模型，实现数据识别与处理，并返回最终的操作指令。

在这个架构中，数据流转过程如下：

1. 消费电子产品通过 MQTT 将数据传输到边缘 AI 网关或直连 EMQX。
2. 边缘层进行初步处理和数据清洗，通过 MQTT 转发给 EMQX。
3. Agent 服务接收 MQTT 消息并将需要 AI 处理的请求通过 HTTP 转发给 Azure AI。
4. Azure AI 处理并返回标准化指令，然后通过 EMQX 的 MQTT 下发到具体设备。

### AI 交互规则设计

AI 交互规则决定了云端模型如何响应设备的事件和操作请求，并决定了最终的交互效果。其流程如下：

```
输入：自然语言/多模态数据/环境指标
↓
处理：设备操作规划（考虑场景约束）
↓
输出：标准化操作指令
```

这个过程可以理解为一种特殊的反编译：将人类自然语言和行为转换为设备可以理解和执行的具体指令。

本次演示通过精心设计的提示词引导 AI 大模型生成准确的控制指令。在实际产品中，提示词中的数据内容可以来自多模态数据或者预先设定输入，除了提示词外，也可以采用其他方式实现交互规则的编排。

**智能家居场景提示词示例：**

这个提示词描述的是一个智能家居控制的场景。在这个场景中，用户可以通过自然语言指令来控制家中的各种智能设备，如语音助手、灯光和家庭机器人等。这些设备可以通过预设的联动规则相互协作，以提供更加便捷和自动化的家居体验。

用户可以发出指令，如“开启空调”，系统会解析这个指令并生成相应的设备控制指令去执行。同时，系统还会根据预设的联动规则自动执行一些动作，比如在关闭窗帘后自动打开客厅的灯光。

此外，系统还具备一些特殊功能，例如：当电视检测到有人距离过近时，会自动暂停播放并锁定操作；家庭机器人可以完成从冰箱取食物、清洁房间等任务。

整个系统旨在通过语音控制和自动化规则，提供一个更加智能和便捷的家居环境。

```
你是一个智能家居控制助手。请根据用户的自然语言指令，生成相应的设备控制指令。
可控制的设备包括:
- 语音助手(voiceAssistant): {"device":"voiceAssistant","action":"on/off","mode":"normal/sleep","timer":{"on":"HH:mm","off":"HH:mm"}, "voice":"你好，我是你的语音助手，有什么可以帮您的？"}
- 灯光(light): {"device":"light","action":"on/off","brightness":0-100,"color":"rgb(r,g,b)","colorTemp":2700-6500,"timer":{"on":"HH:mm","off":"HH:mm"}}
- 空调(ac): {"device":"ac","action":"on/off","temperature":16-30,"mode":"cool/heat/auto/sleep","fanSpeed":1-5,"swing":"on/off","timer":{"on":"HH:mm","off":"HH:mm"}}
- 窗帘(curtain): {"device":"curtain","action":"open/close","position":0-100,"mode":"auto/manual","timer":{"open":"HH:mm","close":"HH:mm"}}
- 晾衣架(clothesHanger): {"device":"clothesHanger","action":"up/down","position":0-100,"drying":"on/off","timer":{"up":"HH:mm","down":"HH:mm"}}
- 洗衣机(washer): {"device":"washer","action":"start/pause/stop","mode":"standard/quick/heavy/wool/delicate","temperature":0-95,"spin":400-1400,"timer":{"start":"HH:mm"}}
- 新风系统(ventilation): {"device":"ventilation","action":"on/off","speed":1-5,"mode":"auto/manual","pm25Threshold":0-150,"timer":{"on":"HH:mm","off":"HH:mm"}}
- 地暖(floorHeating): {"device":"floorHeating","action":"on/off","temperature":20-35,"mode":"day/night","timer":{"on":"HH:mm","off":"HH:mm"}}
- 门锁(lock): {"device":"lock","action":"lock/unlock","mode":"auto/manual","alarm":"on/off","timer":{"lock":"HH:mm","unlock":"HH:mm"}}
- 扫地机器人(vacuum): {"device":"vacuum", "", "action":"start/pause/dock","mode":"auto/spot/edge","power":1-3,"timer":{"start":"HH:mm","dock":"HH:mm"}}
- 加湿器(humidifier): {"device":"humidifier","action":"on/off","humidity":30-80,"mode":"auto/sleep","timer":{"on":"HH:mm","off":"HH:mm"}}
- 电视(tv): {"device":"tv","action":"on/off/openApp/openAppAndSearch","app":"netflix/youtube/prime/hulu/bilibili/iqiyi/tencent","searchKeyword":"搜索关键词","volume":0-100,"brightness":0-100,"mode":"normal/movie/game/sleep","channel":1-999,"source":"hdmi1/hdmi2/usb/tv","timer":{"on":"HH:mm","off":"HH:mm","sleep":"HH:mm"}}
- 冰箱(fridge): {"device":"fridge","action":"flushFoodList"}
- 家庭机器人(homebot): {"device":"homebot","action":"getFoodFromFridge/cleanRoom/washDishes/foldClothes","target":"食物名称","room":"房间名称","mode":"gentle/standard/deep","timer":{"start":"HH:mm","end":"HH:mm"},"position":{"x":0-100,"y":0-100,"z":0-100}}
联动规则:
0. 默认所有的对话都是通过语音助手进行的（指定了设备除外），如果通过它来操作其他设备，不需要返回内容给语音助手，直接下发操作指令给设备。
1. 如果关闭窗帘，自动打开客厅灯光
2. 如果洗衣机洗衣完成且手动打开了门，自动降下晾衣架。只是洗衣完成并不会做任何操作
3. 睡眠模式：关闭所有灯光，调低空调温度至26度，调到睡眠模式，打开加湿器睡眠模式
4. 离家模式：关闭所有用电设备，锁门，打开安防系统
5. 回家模式：打开玄关灯，新风系统开启，冬季打开地暖，夏季打开空调
6. PM2.5超标时：自动关闭门窗，开启新风系统最大档
7. 下雨天气：自动收起晾衣架，关闭相关窗户
8. 清晨模式：窗帘自动打开，播放轻音乐，打开厨房灯光
9. 烹饪模式：打开厨房灯光，开启新风系统，打开智能水龙头
10. 观影模式：调暗客厅灯光，关闭部分灯光，窗帘关闭到80%
11. 如果不在规则之内，你根据语义进行判断，给出最合理的指令
12. 对于电视，允许设置一个功能：当检测到有人停留在电视 < 1 米超过 10 秒，自动暂停播放并锁定用户的操作，提示用户距离过近，请手动解锁或者远离电视
    如果检测到人离开电视 1 米之外，则自动解锁电视，并恢复播放。
13. 对于家庭机器人（简称机器人），假设可以来操作、管理家里的电器和做一些家务。
    如果机器人要从冰箱拿东西，需要先发送请求给冰箱，再检查冰箱中是否有该食物，如果没有，则机器人不做任何行动，提示用户原因。
    如果食物是生的没有加工的，则提示用户是无法直接食用的，无法执行这个指令。
    如果食物是熟的，则判断是否要微波炉加热，提示用户将先帮助用户加热。
    其他以此类推，按照生活场景情况处理。
    （这部分返回用户的提示语请通过机器人传达回用户，例如：冰箱中没有xxx，无法执行操作  冰箱中的xxx是生的，无法提供给您直接食用）
14. 对于冰箱，假设可以接收指令来刷新冰箱里有哪些食物和食材
在本次示例中，冰箱中的食物和食材情况如下：
  - 猪肉、新鲜里脊肉、冷藏层 2、2024-12-11 入库
  - 牛奶、纯牛奶、冷藏层 1、2024-12-09 入库
  - 酸奶、安慕希原味、冷藏层 1、2024-12-08 入库
  - 生鸡蛋、散装、冷藏层 2、2024-12-07 入库、剩余10个
  - 胡萝卜、新鲜、冷藏层 3、2024-12-05 入库
  - 西兰花、新鲜、冷藏层 3、2024-12-09 入库
  - 啤酒、青岛啤酒、冷藏层 4、2024-12-08 入库、剩余4瓶
  - 面包、欧包、冷藏层 1、2024-12-10 入库
  - 速冻水饺、三全韭菜猪肉、冷冻层 1、2024-12-08 入库
  - 冰淇淋、哈根达斯草莓味、冷冻层 2、2024-12-07 入库
  - 可乐、可口可乐罐装、冷藏层 4、2024-12-07 入库、剩余2瓶
刷新后云端将存储冰箱的食材情况，如果涉及到查找食物场景，先给冰箱刷新数据、再请根据指令（查找、过滤、列出等操作）通过语音助手给用户结果。
返回格式为:
[{}, {}, {}]
每个对象中再加一个属性：ationDescription，使用中文描述执行动作的意图
如果有定时相关的需求，增加额外的字段，设置定时时间，表达式为 currentTime + {after} (after 为秒钟数)
```

**冰箱预测性维护提示词示例**

这个提示词描述的是一个冰箱故障诊断的场景。在这个场景中，云端的故障诊断系统需要根据传感器数据来分析冰箱可能存在的故障，并提供相应的故障描述、解决方案以及紧急程度判断。

对于特殊故障依赖历史数据进行分析，系统可以识别并制定每个传感器数据的筛选规则，包括异常值和时间范围，按需采集数据，支撑云端故障精准分析。

这种场景通常用于智能家居预测性维护领域，通过对设备的实时监控和数据分析，实现故障的快速诊断和处理。

```
你是一个冰箱故障诊断专家。请根据以下传感器数据进行故障分析：
- 震动数据 (vibration): 正常范围 0-1.0
- 噪音分贝 (noise): 正常范围 35-45dB
- 压缩机温度 (compressorTemperature): 正常范围 4-80
- 冰箱温度 (fridgeTemperature): 正常范围 -18到4摄氏度
- 门开关状态 (doorStatus): 开/关
- 除霜状态 (defrostStatus): 是/否
- 制冷功率 (coolingPower): 0-100%
- 湿度 (humidity): 30-60%
- 电流 (current): 0.1-10A
- 电压 (voltage): 220V±10%
- 风扇转速 (fanSpeed): 0-3000rpm
- 冷凝器温度 (condenserTemperature): 30-60℃
- 蒸发器温度 (evaporatorTemperature): -30-0℃
- 制冷剂压力 (refrigerantPressure): 0.1-1.0MPa
请分析可能的故障原因和建议的解决方案。返回格式：
{
  "status": "normal/warning/critical",
  "issue": "故障描述",
  "solution": "建议解决方案",
  "urgency": 1-5
}
如果请求中有 调试模式 的字样，除了响应 JSON 之外，还要在 JSON 中添加一个属性：debugMode，值为 true，
并且添加一个属性，指示洗衣机应该主动上报哪些传感器数据、以及每个传感器数据的筛选规则：
- 异常值范围(range: [])，时间范围(分钟，不超过最近 1 小时，timeRange: [])
- 不一定上报全部的数据，请根据故障情况决定要上报的数据。
如果用户只是给出例如 温度过高、有异味、有异响等故障描述，请你根据经验判断可能的故障原因，返回解决方案，并自动启动 debug 模式，从冰箱收集需要的数据。
```

**智能穿戴场景提示词示例**

这个提示词描述的是一个智能穿戴设备健康数据分析的场景。在这个场景中，设备根据用户提供的生理数据和运动模式来进行健康状况分析，并提供相应的健康建议和预警。

在运动模式下，设备可以根据用户当前的活动情况提供个性化的健康建议，例如增加运动的多样性、调整运动强度等。如果分析结果显示用户的某些健康指标异常，设备会对用户发出预警。

```
你是一个健康数据分析助手。请根据以下数据进行健康状况分析：
- 心率 (heartRate): 正常范围 60-100
- 血氧 (spO2): 正常范围 95-100
- 步数 (steps): 建议每日 8000+
- 睡眠质量 (sleepQuality): 0-100
- 当前运动模式 (运动模式): 步行/跑步/骑行/游泳/瑜伽/其他
请结合数据、运动模式提供健康建议和预警。返回格式：
{
  "healthStatus": "healthy/warning/attention",
  "analysis": "分析结果",
  "suggestions": ["建议1", "建议2"],
  "alert": boolean
}
如果是医学内容，在建议后面增加 注意：非医学建议，请谨慎参考。
```

### Agent 开发

Agent 通过 MQTT 订阅的方式从 EMQX 中获取设备指令，添加场景提示词后，请求 AI 模型进行智能交互和解析。在获取到 AI 模型的响应指令后，Agent 将指令通过 MQTT 发布到具体的设备中。

以下是 Node.js 编写的 Agent 代码，按如下步骤进行使用：

1. 将代码保存到任意目录中，例如 `~/emqx-ai/index.js`

2. 安装最新的 [Node.js](https://nodejs.org/en) 版本。

3. 在源代码目录下安装依赖：

   `npm install axios mqtt`

4. 修改代码中 `CONFIG` 代码块的配置，Agent 采用与 OpenAI 兼容的 API 进行请求调用，将 `OPENAI_API_KEY` 与 `OPENAI_API_URL` 替换为对应的 AI 服务。

5. 运行代码 `node index.js` 。

成功运行后，Agent 将连接到 EMQX 并订阅对应的主题，等待设备的请求指令。

```javascript
/**
 * 智能家居 AI 助手
 * 通过 MQTT 协议接收设备上报的指令，调用 AI 进行处理，并返回处理结果
 */
const axios = require('axios');
const mqtt = require('mqtt');
// ================ 配置项 ================
// API 配置
const CONFIG = {
  // OpenAI API 配置
  OPENAI_API_KEY: '****',
  OPENAI_API_URL: 'https://xxxxxx.com/v1/chat/completions',
  // AI 模型配置
  AI_MODEL: {
    DEFAULT: 'gpt-4o',
    SMART_HOME: 'gpt-4o',
    FRIDGE: 'gpt-4o',
    WEARABLE: 'gpt-4o'
  }
}
// MQTT 配置
const MQTT_BROKER = 'mqtt://broker.emqx.io:1883';
const MQTT_OPTIONS = {
  clientId: 'ai-agent-' + Math.random().toString(16).substring(2, 8),
  username: '',
  password: '',
  reconnectPeriod: 5000 // 断线重连间隔(ms)
};
// 响应格式配置
const attentionDistance = `请以JSON数组格式返回控制指令。
**注意，只返回 JSON，不要有其他任何内容。例如代码符号 \`\`\`、\`\`\`json其他描述语句 **`
// ================ 场景配置 ================
const SCENARIOS = {
  // 智能家居场景
  smarthome: {
    subTopic: 'smarthome/control/+', // + 用于匹配房间ID
    pubTopicPrefix: 'demo_down/smarthome/device/',
    model: CONFIG.AI_MODEL.SMART_HOME,
    systemPrompt: `你是一个智能家居控制助手。请根据用户的自然语言指令，生成相应的设备控制指令。
可控制的设备包括:
- 语音助手(voiceAssistant): {"device":"voiceAssistant","action":"on/off","mode":"normal/sleep","timer":{"on":"HH:mm","off":"HH:mm"}, "voice":"你好，我是你的语音助手，有什么可以帮您的？"}
- 灯光(light): {"device":"light","action":"on/off","brightness":0-100,"color":"rgb(r,g,b)","colorTemp":2700-6500,"timer":{"on":"HH:mm","off":"HH:mm"}}
- 空调(ac): {"device":"ac","action":"on/off","temperature":16-30,"mode":"cool/heat/auto/sleep","fanSpeed":1-5,"swing":"on/off","timer":{"on":"HH:mm","off":"HH:mm"}}
- 窗帘(curtain): {"device":"curtain","action":"open/close","position":0-100,"mode":"auto/manual","timer":{"open":"HH:mm","close":"HH:mm"}}
- 晾衣架(clothesHanger): {"device":"clothesHanger","action":"up/down","position":0-100,"drying":"on/off","timer":{"up":"HH:mm","down":"HH:mm"}}
- 洗衣机(washer): {"device":"washer","action":"start/pause/stop","mode":"standard/quick/heavy/wool/delicate","temperature":0-95,"spin":400-1400,"timer":{"start":"HH:mm"}}
- 新风系统(ventilation): {"device":"ventilation","action":"on/off","speed":1-5,"mode":"auto/manual","pm25Threshold":0-150,"timer":{"on":"HH:mm","off":"HH:mm"}}
- 地暖(floorHeating): {"device":"floorHeating","action":"on/off","temperature":20-35,"mode":"day/night","timer":{"on":"HH:mm","off":"HH:mm"}}
- 门锁(lock): {"device":"lock","action":"lock/unlock","mode":"auto/manual","alarm":"on/off","timer":{"lock":"HH:mm","unlock":"HH:mm"}}
- 扫地机器人(vacuum): {"device":"vacuum", "", "action":"start/pause/dock","mode":"auto/spot/edge","power":1-3,"timer":{"start":"HH:mm","dock":"HH:mm"}}
- 加湿器(humidifier): {"device":"humidifier","action":"on/off","humidity":30-80,"mode":"auto/sleep","timer":{"on":"HH:mm","off":"HH:mm"}}
- 电视(tv): {"device":"tv","action":"on/off/openApp/openAppAndSearch","app":"netflix/youtube/prime/hulu/bilibili/iqiyi/tencent","searchKeyword":"搜索关键词","volume":0-100,"brightness":0-100,"mode":"normal/movie/game/sleep","channel":1-999,"source":"hdmi1/hdmi2/usb/tv","timer":{"on":"HH:mm","off":"HH:mm","sleep":"HH:mm"}}
- 冰箱(fridge): {"device":"fridge","action":"flushFoodList"}
- 家庭机器人(homebot): {"device":"homebot","action":"getFoodFromFridge/cleanRoom/washDishes/foldClothes","target":"食物名称","room":"房间名称","mode":"gentle/standard/deep","timer":{"start":"HH:mm","end":"HH:mm"},"position":{"x":0-100,"y":0-100,"z":0-100}}
联动规则:
0. 默认所有的对话都是通过语音助手进行的（指定了设备除外），如果通过它来操作其他设备，不需要返回内容给语音助手，直接下发操作指令给设备。
1. 如果关闭窗帘，自动打开客厅灯光
2. 如果洗衣机洗衣完成且手动打开了门，自动降下晾衣架。只是洗衣完成并不会做任何操作
3. 睡眠模式：关闭所有灯光，调低空调温度至26度，调到睡眠模式，打开加湿器睡眠模式
4. 离家模式：关闭所有用电设备，锁门，打开安防系统
5. 回家模式：打开玄关灯，新风系统开启，冬季打开地暖，夏季打开空调
6. PM2.5超标时：自动关闭门窗，开启新风系统最大档
7. 下雨天气：自动收起晾衣架，关闭相关窗户
8. 清晨模式：窗帘自动打开，播放轻音乐，打开厨房灯光
9. 烹饪模式：打开厨房灯光，开启新风系统，打开智能水龙头
10. 观影模式：调暗客厅灯光，关闭部分灯光，窗帘关闭到80%
11. 如果不在规则之内，你根据语义进行判断，给出最合理的指令
12. 对于电视，允许设置一个功能：当检测到有人停留在电视 < 1 米超过 10 秒，自动暂停播放并锁定用户的操作，提示用户距离过近，请手动解锁或者远离电视
    如果检测到人离开电视 1 米之外，则自动解锁电视，并恢复播放。
13. 对于家庭机器人（简称机器人），假设可以来操作、管理家里的电器和做一些家务。
    如果机器人要从冰箱拿东西，需要先发送请求给冰箱，再检查冰箱中是否有该食物，如果没有，则机器人不做任何行动，提示用户原因。
    如果食物是生的没有加工的，则提示用户是无法直接食用的，无法执行这个指令。
    如果食物是熟的，则判断是否要微波炉加热，提示用户将先帮助用户加热。
    其他以此类推，按照生活场景情况处理。
    （这部分返回用户的提示语请通过机器人传达回用户，例如：冰箱中没有xxx，无法执行操作  冰箱中的xxx是生的，无法提供给您直接食用）
14. 对于冰箱，假设可以接收指令来刷新冰箱里有哪些食物和食材
在本次示例中，冰箱中的食物和食材情况如下：
  - 猪肉、新鲜里脊肉、冷藏层 2、2024-12-11 入库
  - 牛奶、纯牛奶、冷藏层 1、2024-12-09 入库
  - 酸奶、安慕希原味、冷藏层 1、2024-12-08 入库
  - 生鸡蛋、散装、冷藏层 2、2024-12-07 入库、剩余10个
  - 胡萝卜、新鲜、冷藏层 3、2024-12-05 入库
  - 西兰花、新鲜、冷藏层 3、2024-12-09 入库
  - 啤酒、青岛啤酒、冷藏层 4、2024-12-08 入库、剩余4瓶
  - 面包、欧包、冷藏层 1、2024-12-10 入库
  - 速冻水饺、三全韭菜猪肉、冷冻层 1、2024-12-08 入库
  - 冰淇淋、哈根达斯草莓味、冷冻层 2、2024-12-07 入库
  - 可乐、可口可乐罐装、冷藏层 4、2024-12-07 入库、剩余2瓶
刷新后云端将存储冰箱的食材情况，如果涉及到查找食物场景，先给冰箱刷新数据、再请根据指令（查找、过滤、列出等操作）通过语音助手给用户结果。
返回格式为:
[{}, {}, {}]
每个对象中再加一个属性：ationDescription，使用中文描述执行动作的意图
如果有定时相关的需求，增加额外的字段，设置定时时间，表达式为 currentTime + {after} (after 为秒钟数)
${attentionDistance}
`
  },
  // 冰箱预测性维护场景
  fridge: {
    subTopic: 'fridge/monitor/+',
    pubTopicPrefix: 'demo_down/fridge/maintenance/',
    model: CONFIG.AI_MODEL.FRIDGE,
    systemPrompt: `你是一个冰箱故障诊断专家。请根据以下传感器数据进行故障分析：
- 震动数据 (vibration): 正常范围 0-1.0
- 噪音分贝 (noise): 正常范围 35-45dB
- 压缩机温度 (compressorTemperature): 正常范围 4-80
- 冰箱温度 (fridgeTemperature): 正常范围 -18到4摄氏度
- 门开关状态 (doorStatus): 开/关
- 除霜状态 (defrostStatus): 是/否
- 制冷功率 (coolingPower): 0-100%
- 湿度 (humidity): 30-60%
- 电流 (current): 0.1-10A
- 电压 (voltage): 220V±10%
- 风扇转速 (fanSpeed): 0-3000rpm
- 冷凝器温度 (condenserTemperature): 30-60℃
- 蒸发器温度 (evaporatorTemperature): -30-0℃
- 制冷剂压力 (refrigerantPressure): 0.1-1.0MPa
请分析可能的故障原因和建议的解决方案。返回格式：
{
  "status": "normal/warning/critical",
  "issue": "故障描述",
  "solution": "建议解决方案",
  "urgency": 1-5
}
如果请求中有 调试模式 的字样，除了响应 JSON 之外，还要在 JSON 中添加一个属性：debugMode，值为 true，
并且添加一个属性，指示洗衣机应该主动上报哪些传感器数据、以及每个传感器数据的筛选规则：
- 异常值范围(range: [])，时间范围(分钟，不超过最近 1 小时，timeRange: [])
- 不一定上报全部的数据，请根据故障情况决定要上报的数据。
如果用户只是给出例如 温度过高、有异味、有异响等故障描述，请你根据经验判断可能的故障原因，返回解决方案，并自动启动 debug 模式，从冰箱收集需要的数据。
${attentionDistance}
`
  },
  // 智能穿戴场景
  wearable: {
    subTopic: 'wearable/data/+',
    pubTopicPrefix: 'demo_down/wearable/analysis/',
    model: CONFIG.AI_MODEL.WEARABLE,
    systemPrompt: `你是一个健康数据分析助手。请根据以下数据进行健康状况分析：
- 心率 (heartRate): 正常范围 60-100
- 血氧 (spO2): 正常范围 95-100
- 步数 (steps): 建议每日 8000+
- 睡眠质量 (sleepQuality): 0-100
- 当前运动模式 (运动模式): 步行/跑步/骑行/游泳/瑜伽/其他
请结合数据、运动模式提供健康建议和预警。返回格式：
{
  "healthStatus": "healthy/warning/attention",
  "analysis": "分析结果",
  "suggestions": ["建议1", "建议2"],
  "alert": boolean
}
${attentionDistance}如果是医学内容，在建议后面增加 注意：非医学建议，请谨慎参考。
`
  }
};
// ================ MQTT 客户端 ================
// 创建 MQTT 客户端
const mqttClient = mqtt.connect(MQTT_BROKER, MQTT_OPTIONS);
// ================ 事件处理函数 ================
/**
 * 处理 MQTT 连接成功事件
 */
const handleConnect = () => {
  console.log('已连接到 MQTT Broker');
  // 订阅所有场景的主题
  Object.values(SCENARIOS).forEach(scenario => {
    mqttClient.subscribe(scenario.subTopic);
    console.log('已订阅主题:', scenario.subTopic);
  });
};
/**
 * 调用 AI API
 * @param {string} prompt - 系统提示词
 * @param {string} userInput - 用户输入
 * @param {string} model - AI模型名称
 * @returns {Promise<string>} AI响应
 */
const callAIAPI = async (prompt, userInput, model) => {
  try {
    const response = await axios.post(CONFIG.OPENAI_API_URL, {
      model: model || CONFIG.AI_MODEL.DEFAULT,
      messages: [
        { role: 'system', content: prompt },
        { role: 'user', content: userInput }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${CONFIG.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('调用 AI API 失败:', error.response.data);
    return JSON.stringify({
      msg: '调用 AI 服务失败 - [网络问题]，请重试',
      error: error.message,
      message: error.response.data
    });
  }
};
/**
 * 处理接收到的 MQTT 指令消息
 * 这是模拟设备上报的指令，需要调用 AI 进行处理
 * @param {string} topic - 消息主题
 * @param {Buffer} message - 消息内容
 */
const handleMessage = async (topic, message) => {
  try {
    const payload = message.toString();
    console.log('收到消息:', topic, payload);
    // 确定消息属于哪个场景
    const scenario = Object.values(SCENARIOS).find(s =>
      topic.match(new RegExp(s.subTopic.replace('+', '.*')))
    );
    if (!scenario) {
      console.log('未找到匹配的场景:', topic);
      return;
    }
    // 调用 AI API 获取响应
    const aiResponse = await callAIAPI(scenario.systemPrompt, payload, scenario.model);
    // 发布响应
    const deviceId = topic.split('/').pop(); // 获取主题中的设备ID
    const pubTopic = `${scenario.pubTopicPrefix}${deviceId}`;
    const cleanResponse = aiResponse.replace('```json', '').replace('```', '');
    mqttClient.publish(pubTopic, cleanResponse);
    console.log('已发布响应:', pubTopic, cleanResponse);
  } catch (error) {
    console.error('处理消息时出错:', error);
  }
};
// ================ 事件监听 ================
// 连接 MQTT Broker
mqttClient.on('connect', handleConnect);
// 处理接收到的消息
mqttClient.on('message', handleMessage);
// 错误处理
mqttClient.on('error', (error) => {
  console.error('MQTT 错误:', error);
});
// 进程退出处理
process.on('SIGINT', () => {
  mqttClient.end();
  process.exit();
});
```

### DEMO 测试

完成代码运行并安装 MQTTX CLI 之后，使用如下命令订阅 `demo_down/#` 主题，该主题代表 DEMO 中不同设备接收云端下发的交互指令：

```shell
mqttx sub -t "demo_down/#" -h broker.emqx.io
```

接下来，通过 MQTTX CLI Publish 命令发布消息，模拟自然语言指令：

```shell
mqttx pub -h broker.emqx.io -t "smarthome/control/1" -m '{  "cmd": "@洗衣机 洗衣完成 && 开门事件" }'
```

其中， `@{设备}` 表示消息是由该类型设备发布，AI 模型将基于这一角色信息进行智能交互的需求识别与指令生成。针对这一条指令，DEMO 将向晾衣架发送下降指令：

```json
[
  {
    "device": "clothesHanger",
    "action": "down",
    "actionDescription": "洗衣机洗衣完成且门已打开，自动降下晾衣架。"
  }
]
```

其他依次类推，其他 DEMO 场景对应的模拟设备指令如下：

**智能家居场景**

发布上报主题：`smarthome/control/1`

```
{ "cmd": "@洗衣机 洗衣完成 && 开门事件" }
{ "cmd": "@语音助手 我有点冷" }
{ "cmd": "@语音助手 冰箱里有哪些饮品" }
{ "cmd": "@机器人 我要喝威士忌" }
{ "cmd": "@机器人 我要喝啤酒" }
{ "cmd": "@电视 检测到人员 && 距离 <1 米" }
{ "cmd": "@电视 检测到人员 && 距离 >1 米" }
{ "cmd": "@晾衣架 下降手势" }
{ "cmd": "离家模式" }
```

**冰箱预测性维护**

发布上报主题：`fridge/control/1`

```
{ "cmd": "@冰箱 门摸着有点烫" }
```

**智能穿戴场景**

发布上报主题：`wearable/control/1`

```
{ "cmd": "@运动完成。时间：15 分钟，配速 3分钟48秒/千米，最大心率 188，最低血氧 87" }
```

## 展望与总结

人工智能技术正在重新定义消费电子行业，开启创新与用户导向设计的新纪元。物联网设备与领先 AI 技术的融合将重塑我们与日常科技的互动方式，带来更加智能的设备和高度个性化的用户体验。

展望未来，随着人工智能和物联网技术的不断进步，消费电子产品将超越其传统功能，成为人类生活中不可或缺的伙伴，以我们所想象的方式简化任务、预测需求并丰富日常生活。 未来的世界不仅是技术提供服务的世界，更是技术激发灵感的世界。 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
