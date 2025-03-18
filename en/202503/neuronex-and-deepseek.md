## Introduction

The Industrial Internet of Things (IIoT) integrates IT and OT, leveraging stream processing and edge computing for real-time data monitoring and analysis. This leads to production optimization, predictive maintenance, reduced downtime, and improved yield rates, facilitating smart manufacturing and cost efficiency.

EMQ’s [NeuronEX](https://www.emqx.com/en/products/neuronex) is a real-time data acquisition software that offers industrial protocol collection, system data integration, edge-side filtering, AI integration, and data forwarding. It enables low-latency data management, with most tasks manageable using simple SQL statements. However, complex processing requires custom plugins, adding to development complexity. This article discusses how DeepSeek’s Large Language Model (LLM) enhances NeuronEX’s capabilities, simplifying complex data processing, reducing costs, and allowing for quick adaptation to business needs.

## NeuronEX Streaming Data Processing: Simple SQL for Common Needs

NeuronEX’s streaming engine processes data from diverse sources, offering extraction, transformation, filtering, sorting, grouping, aggregation, and joining. With over 160 built-in functions—spanning math, string processing, aggregation, and hashing—it empowers robust streaming analysis. This enables data cleaning, standardization, monitoring, and real-time alerts.

Typically, logic is implemented via SQL. For example, this statement filters industrial data, retaining only `tag1="device_01"`, and aggregates it in 5-second windows:

```sql
SELECT * 
FROM neuronStream 
WHERE tag1="device_01"
GROUP BY TumblingWindow(ss, 5)
```

Processed data can be sent to targets like EMQX MQTT Broker, HTTP services, Kafka, or databases.

SQL efficiently handles most logic, but complex cases—like these customer needs—are challenging:

- **Need 1**: For `tagA`, if 7 consecutive values increase, return `{"tagA_alarm": true}`; otherwise, output nothing.
- **Need 2**: Extract UTC+0 time (YYYY-MM-DD HH:MM:ss) from text, convert to Beijing time (YY/MM/DD HH:MM), or return empty if not found.

SQL’s limited expressiveness struggles with multi-level logic or complex calculations, often falling short.

To address this, NeuronEX supports custom functions in Python or Golang. However, this requires:

- Programming expertise, challenging for non-developers.
- Complex setup, debugging, packaging, and deployment.

These barriers hinder rapid, deep data analysis. New needs often rely on vendors, raising costs and limiting flexibility.

## NeuronEX + DeepSeek: Tackling Complex Data Processing

To boost NeuronEX’s capabilities, we integrate DeepSeek LLM’s reasoning and code generation with NeuronEX’s Agent workflow, automating Python function creation for complex logic.

**Workflow**:

1. Users describe logic in natural language; NeuronEX optimizes prompts for LLM.
2. DeepSeek generates Python code, shown for user approval.
3. The system auto-packages, installs, and deploys the function—no manual steps needed.
4. Users call the function in NeuronEX’s rule interface for complex processing.
5. Users can review code and use AI Q&A to understand it.

**This brings**:

- **Lower Barrier**: DeepSeek empowers non-coders with data processing and analysis skills.
- **Boosted Efficiency**: Cuts development from days to minutes, adapting quickly to changes.
- **Reduced Costs**: Minimizes vendor reliance, lowering expenses.

## Operation Demo

### AI-Generated Functions

Access “AI-Generated Function” via “Rules” or “Extensions” in the left menu.

- Configure the function: Define input parameter names, types, and clear descriptions for better code quality.
- Describe logic and output in natural language (e.g., processing rules, return values, or examples).
- Click “Generate Code” to trigger DeepSeek.

![image.png](https://assets.emqx.com/images/879aa8b8971bf1689249b01fe19426c2.png)

### AI Function Assistant

Once the code is generated, an “AI Function Assistant” will pop up on the right side of the page.

- The AI automatically generates a function name based on the user’s input, which can be freely edited by clicking it.  
- The interface shows code generated from natural language input. Users can request explanations for unclear lines, helping to clarify the code’s logic.
- After confirming accuracy, click “Deploy Function” to complete the deployment.

![image.png](https://assets.emqx.com/images/6dbb4c52058b21af5e66be4d7291b2a9.png)

### Function Testing

- Return to the rule editor.
- Use the custom function in the SQL editor and test it.
- View results in the output interface.

In minutes, users can build, test, and deploy complex functions.

![image.png](https://assets.emqx.com/images/7f948af6edcc1df1fdcf4576fd88adfa.png)

## Conclusion

By integrating LLM tools like DeepSeek, NeuronEX efficiently supports complex business data processing, enabling production and operations staff, as well as business users, to rapidly develop and deploy intricate business logic without relying on professional development teams. This speeds up responses—shrinking delivery from days to minutes—while lowering barriers and boosting efficiency.

This feature is in development and testing. Contact us for more details if interested!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
