对于工业边缘计算领域的 OT 工程师而言，编写数据处理规则一直是一项重大难题。虽然 SQL 语言简洁且功能强大，但仍与工厂团队习以为常的梯形图和 PLC 编程逻辑相去甚远。想要掌握 SQL 语法、窗口函数和复杂聚合操作，会分散更多的时间和精力，影响核心业务进度。

**NeuronEX 3.8.0 引入了一项突破性功能：基于大语言模型（LLM）的 SQL 自动生成。**现在，工程师可以用自然语言直接描述数据处理需求，AI 助手即可自动生成对应的 SQL 规则，将原本耗时数小时的规则编写过程缩短至几分钟，真正实现**让人工智能服务于行业，而不是让行业被动适应人工智能。**

## 传统工业数据处理的三大痛点

### **技能鸿沟：OT 与 IT 间的语言障碍**

工厂工程师精通设备运维和工艺流程，但对 SQL、流计算、窗口函数等 IT 概念相对陌生。

传统解决方案需要：

- 聘请专业的数据工程师编写规则
- OT 工程师花费数周学习 SQL 语法
- 依赖系统集成商提供定制化开发

### **开发效率低：反复试错的成本**

即使掌握了 SQL 基础，编写复杂的流计算规则仍然需要：

- 查阅大量文档（NeuronEX 有 160+ 内置函数）
- 反复调试语法错误（如窗口函数参数、JOIN 条件）
- 测试边界条件（如空值处理、数据类型转换）

一个看似简单的需求（如：检测温度连续 3 次超过 100°C），可能需要数小时才能完成。

### **维护成本高：规则难以理解和修改**

当业务需求变化时（如调整阈值、增加过滤条件），工程师需要：

- 重新理解原有 SQL 逻辑
- 小心修改，避免引入新的错误
- 重新测试所有边界条件

这使得规则维护成为一项高风险、高成本的工作。

## NeuronEX 的解决方案：AI 驱动的智能规则生成

NeuronEX 3.8.0 在规则创建页面内置了 AI 问答助手，该助手由 OpenAI GPT、DeepSeek 和 Qwen 等大语言模型提供支持，并与我们的数据处理知识库深度集成，拥有以下技术优势：

- **160+ 内置函数**：如 `lag()`、`unnest()`、`bitand()`、`collect()`
- **多种窗口函数的使用场景**：`TumblingWindow`、`SlidingWindow`、`CountWindow`、`SessionWindow`
- **工业数据处理的最佳实践**：理解如何处理空值、如何避免数据类型错误、如何优化性能等。
- **多轮对话与迭代优化：**通过多轮对话，用户可以持续追问和优化 SQL 规则，直到满足需求。

![image.png](https://assets.emqx.com/images/25c63e3f7e5709353ace6b3907f2fe27.png)

### **工作流程：**

1. **用户使用自然语言描述需求**（中文或英文）
2. **AI 理解业务意图**，识别关键要素（数据源、过滤条件、聚合逻辑、窗口类型）
3. **自动生成符合规范的 SQL 代码**，符合语法规范，包含必要的函数和参数
4. **用户可以一键应用**，或根据需要进行微调

### **关键价值：**

- **零学习成本**：OT 工程师无需掌握 SQL 语法，仅使用业务语言描述即可编写规则。
- **开发效率提升**：人工智能可在 5-10 秒内理解需求并生成代码，将开发时间从数小时缩短至数分钟。
- **生产级规则质量**：AI 生成的代码符合语法规范，且遵循行业最佳实践，规则错误率降低 90%。

## 实战案例：从简单到复杂的 5 个场景

### 场景 1：基础过滤 - 温度超限告警

**用户需求（自然语言）：**

> “我想从数据源 neuronStream 中过滤出温度（temp）超过 100 度的数据”

**AI 生成的 SQL：**

```sql
SELECT *
FROM neuronStream
WHERE temp > 100
```

**业务价值：**

- 只上传异常数据，减少 90% 的云端存储成本
- 实时触发告警，无需等待云端批处理

### 场景 2：时间窗口聚合 - 计算平均值

**用户需求（自然语言）：**

> “如何从数据源 neuronStream 计算 10 秒窗口内的平均温度（temp）？”

**AI 生成的 SQL：**

```sql
SELECT avg(temperature) as avg_temp
FROM neuronStream
GROUP BY TumblingWindow(ss, 10)
```

**业务价值：**

- 将高频原始数据（1 秒采样）降维为统计数据（10 秒聚合）
- 数据量减少 90%，云端传输成本大幅降低

### 场景 3：连续异常检测 - 状态持续监控

**用户需求（自然语言）：**

> “我想从数据源 neuronStream 检测设备温度（temp）连续 3 次超过 100 度的异常情况，如何通过窗口和过滤规则实现？”

**AI 生成的 SQL：**

```sql
SELECT 
    temp as current_temp,
    lag(temp, 1) as prev_temp_1,
    lag(temp, 2) as prev_temp_2,
    '连续3次高温警报' as alert_type,
    event_time() as alert_time
FROM neuronStream
WHERE 
    temp > 100 
    AND lag(temp, 1) > 100 
    AND lag(temp, 2) > 100
```

**业务价值：**

- 避免偶发性波动触发误报
- 只在持续异常时触发告警，提高告警准确率

![image.png](https://assets.emqx.com/images/9c2aa6c3da3f68030b7b1721cee92211.png)

### 场景 4：状态码映射 - 语义转换

**用户需求（自然语言）：**

> “如何将设备状态码（StatusCode）0、1、2 分别映射为输出字符串 'stopped'、'running'、'fault'？”

**AI 生成的 SQL：**

```sql
SELECT 
    StatusCode,
    CASE 
        WHEN StatusCode = 0 THEN 'stopped'
        WHEN StatusCode = 1 THEN 'running'
        WHEN StatusCode = 2 THEN 'fault'
        ELSE 'unknown'
    END as status_text,
    device_id,
    timestamp
FROM neuronStream
```

**业务价值：**

- 将 PLC 的「机器语言」转换为业务人员可理解的「业务语言」
- 数据离开边缘时已具备完整的业务语义，无需云端二次解析

### 场景 5：数据精度控制 - 浮点数处理

**用户需求（自然语言）：**

> “温度传感器读数波动较大，我想保留 2 位小数，如何处理？”

**AI 生成的 SQL：**

```sql
SELECT 
    temp as original_temp,
    round(temp * 100) / 100 as temp_2_decimal,
    device_id,
    timestamp
FROM neuronStream
```

**业务价值：**

- 统一数据格式，避免下游系统因精度不一致导致的问题
- 减少数据传输量（精度降低后，JSON 字符串更短）

## 立即体验

### 1. 下载安装

**Docker 部署**：

```shell
docker pull emqx/neuronex:3.8.0-ai
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:3.8.0-ai
```

### 2. 配置 AI 助手

1. 进入「**系统配置**」→「**AI 模型配置**」
2. 选择 LLM 提供商（OpenAI、DeepSeek、Qwen）
3. 填写 API Key、Endpoint 地址、模型名称

### 3. 开始创建规则

1. 进入「**数据处理**」→「**规则**」→「**新建规则**」
2. 点击「**AI 助手**」按钮
3. 用自然语言描述需求
4. 查看 AI 生成的 SQL 代码
5. 一键应用或微调

## 结语

NeuronEX 3.8.0 中基于 LLM 的 SQL 生成功能，实现了边缘计算方式的根本性转变：

- 人工智能不再是技术复杂性的代名词，而是降低一线人员技术门槛的桥梁。
- 随着大语言模型的引入，自然语言正在取代复杂的编码逻辑，成为工业数据规则的主要表达方式。
- OT 工程师能够独立构建数据采集、清洗和转发规则，实现了真正的边缘智能。

我们相信，随着 AI 技术的不断进步，工业数据处理将变得更加直观、高效和便捷。

**立即下载 NeuronEX 3.8.0，体验 AI 驱动的智能规则生成：**[产品下载](https://www.emqx.com/zh/downloads-and-install/neuronex)

**了解更多关于 NeuronEX 的智能边缘能力：**[产品文档](https://docs.emqx.com/zh/neuronex/latest/)
