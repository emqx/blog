For OT engineers in industrial edge computing, writing data processing rules has always been a significant barrier to entry. While SQL is powerful, it’s a far cry from the ladder logic and PLC programming that factory teams are used to. Mastering SQL syntax, window functions, and complex aggregations a time-consuming distraction from their core work.

**[EMQX Neuron 3.8.0](https://www.emqx.com/en/blog/neuron-v-3-8-0-release-notes)** changes the game with a breakthrough feature:  **LLM-based automatic SQL generation.** Engineers can now describe their data needs in plain English. The AI assistant instantly generates SQL rules, shrinking a process that used to take hours down to just a few minutes.

## Pain Points of Traditional Industrial Data Processing

### **Skills Gap: The Language Barrier Between OT and IT**

While factory engineers are experts in equipment maintenance and industrial processes, IT concepts like SQL, stream computing, and window functions are often outside their comfort zone.

Traditional solutions require:

- Hiring professional data engineers to write rules
- OT engineers spending weeks learning SQL syntax
- Relying on system integrators for customized development

### **Low Development Efficiency: The Cost of Repeated Trial and Error**

Even with SQL basics, writing complex stream computing rules still requires:

- Consulting extensive documentation (EMQX Neuron has 160+ built-in functions)
- Repeatedly debugging syntax errors (such as window function parameters, JOIN conditions)
- Testing boundary conditions (such as null value handling, data type conversion)

A seemingly simple requirement (such as "detecting temperature exceeding 100°C three consecutive times") may take hours to complete.

### **High Maintenance Cost: Rules Difficult to Understand and Modify**

When business requirements change (such as adjusting thresholds, adding filter conditions), engineers need to:

- Re-understand the original SQL logic
- Carefully modify to avoid introducing new errors
- Re-test all boundary conditions

This makes rule maintenance a high-risk, high-cost task.

## EMQX Neuron's Solution: AI-Driven Intelligent Rule Generation

EMQX Neuron 3.8.0 features a built-in AI Q&A assistant for rule creation. Powered by LLMs like OpenAI GPT, DeepSeek, and Qwen, it is deeply integrated with our data processing knowledge base to provide instant, accurate guidance for crafting complex rules.

- **Expert Knowledge Base:** It possesses an expert-level understanding of 160+ built-in functions (such as `lag()`, `unnest()`, `bitand()`, `collect()`), diverse windowing logics (`TumblingWindow`, `SlidingWindow`, `CountWindow`, `SessionWindow`), and industrial best practices for data cleaning and performance optimization.

- **Iterative Refinement:** Through **multi-turn dialogue**, engineers can continuously refine and troubleshoot SQL rules until the output perfectly aligns with their operational requirements.

  ![image.png](https://assets.emqx.com/images/4d107c800408f2538408364e93d6c4e5.png)

The core philosophy of this feature is: **Let AI serve industry, not force industry to adapt to AI**.

### **Workflow**

1. **Users describe requirements in natural language**
2. **AI understands business intent**, identifying key elements (data sources, filter conditions, aggregation logic, window types)
3. **AI automatically generates SQL code**, compliant with syntax specifications, including necessary functions and parameters
4. **Users apply with one click**, or fine-tune as needed

### **Key Value**

- **Zero Learning Curve:** OT engineers can now write rules using plain business logic with no SQL expertise required, eliminating the need for dedicated data engineers.
- **Development Efficiency Improvement:** AI generates code in **5–10 seconds**, slashing development time from hours to minutes.
- **Production-Ready Precision:** By following data processing best practices, the AI generates high-quality code that reduces rule errors by **90%**.

## Real-World Cases: 5 Scenarios from Simple to Complex

### Scenario 1: Basic Filtering - Temperature Limit Alarm

**User Requirement (Natural Language):**

> "I want to filter data from the neuronStream data source where temperature (temp) exceeds 100 degrees"

**AI-Generated SQL:**

```sql
SELECT *
FROM neuronStream
WHERE temp > 100
```

**Business Value:**

- Only upload abnormal data, reducing cloud storage costs by 90%
- Trigger alarms in real-time, without waiting for cloud batch processing

### Scenario 2: Time Window Aggregation - Calculating Average

**User Requirement (Natural Language):**

> "How to calculate the average temperature (temp) within a 10-second window from the neuronStream data source?"

**AI-Generated SQL:**

```sql
SELECT avg(temperature) as avg_temp
FROM neuronStream
GROUP BY TumblingWindow(ss, 10)
```

**Business Value:**

- Reduce high-frequency raw data (1-second sampling) to statistical data (10-second aggregation)
- Data volume reduced by 90%, cloud transmission costs significantly reduced

### Scenario 3: Continuous Anomaly Detection - Continuous Status Monitoring

**User Requirement (Natural Language):**

> "I want to detect abnormal situations where the device temperature (temp) exceeds 100 degrees three consecutive times from the neuronStream data source. How can I implement this with window and filter rules?"

**AI-Generated SQL:**

```sql
SELECT 
    temp as current_temp,
    lag(temp, 1) as prev_temp_1,
    lag(temp, 2) as prev_temp_2,
    'Continuous 3 high temperature alerts' as alert_type,
    event_time() as alert_time
FROM neuronStream
WHERE 
    temp > 100 
    AND lag(temp, 1) > 100 
    AND lag(temp, 2) > 100
```

**Business Value:**

- Avoid false alarms triggered by occasional fluctuations
- Only trigger alarms during continuous anomalies, improving alarm accuracy

![image.png](https://assets.emqx.com/images/2ad019d6e2da0eb8335028f0a8ef2cb5.png)

 

### Scenario 4: Status Code Mapping - Semantic Transformation

**User Requirement (Natural Language):**

> "How to map device status codes (StatusCode) 0, 1, 2 to output strings 'stopped', 'running', 'fault' respectively?"

**AI-Generated SQL:**

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

**Business Value:**

- Convert PLC's "machine language" to "business language" understandable by business personnel
- Data already has complete business semantics when leaving the edge, no need for secondary parsing in the cloud

### Scenario 5: Data Precision Control - Floating Point Processing

**User Requirement (Natural Language):**

> "Temperature sensor readings fluctuate greatly. I want to keep 2 decimal places. How to handle this?"

**AI-Generated SQL:**

```sql
SELECT 
    temp as original_temp,
    round(temp * 100) / 100 as temp_2_decimal,
    device_id,
    timestamp
FROM neuronStream
```

**Business Value:**

- Unify data format, avoid downstream system issues caused by inconsistent precision
- Reduce data transmission (after precision reduction, JSON strings are shorter)

## Try It Now

### 1. Download and Install

**Docker Deployment**:

```shell
docker pull emqx/neuronex:3.8.0-ai
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:3.8.0-ai
```

### 2. Configure AI Assistant

1. Go to **"System Configuration"** → **"AI Model Configuration"**
2. Select LLM provider (OpenAI, DeepSeek, Qwen)
3. Fill in API Key, Endpoint URL, Model Name

### 3. Create Your First Rule

1. Go to **"Data Processing"** → **"Rules"** → **"Create Rule"**
2. Click the **"AI ASK"** button
3. Describe requirements in natural language
4. View AI-generated SQL code
5. Apply with one click or fine-tune

## Conclusion: Let AI Serve Industry

The LLM-powered SQL generation in EMQX Neuron 3.8.0 represents a fundamental shift in how we approach edge computing:

- **Democratizing Technology:** AI is no longer a layer of complexity; it is the bridge that lowers technical barriers for those on the front lines.
- **A New Programming Paradigm:** Natural language is evolving into a primary interface for industrial logic, making complex coding a thing of the past.
- **Empowering the OT Frontline:** By enabling OT engineers to handle data processing independently, we unlock true edge intelligence and operational agility.

We believe that as AI continues to evolve, industrial data processing will only become more intuitive, efficient, and accessible.

**Ready to transform your workflow?**

- **Experience it today:** [Download EMQX Neuron](https://www.emqx.com/en/downloads-and-install/neuronex) 
- **Dive deeper:** [Product Overview | EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/)
