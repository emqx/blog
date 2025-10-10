## **Introduction**

In the rapidly evolving wave of the Industrial Internet of Things (IIoT), massive streams of device data converge like rivers. The challenge has always been how to harness this data and transform it into a powerful engine for intelligent decision-making. Previous versions of NeuronEX has solved the complex issue of real-time collection of massive, heterogeneous data and edge stream processing, building a robust pipeline for your data river.

[NeuronEX](https://www.emqx.com/en/products/neuronex) 3.6.0 introduced the brand-new "Data Insights" feature, providing users with the capabilities to unlock full potential of industrial data. Through its built-in time-series database, AI-powered data analysis capabilities, and highly customizable visualization dashboards, the new "Data Insights" feature transforms raw industrial data into deep insights that drive decisions, truly closing the loop from data to value.

## **Overview of NeuronEX Data Insights**

### Core Funtional Component

The Data Insights module primarily includes the following two core functional components:

**Data Analysis:**

- A unified interface that allows you to browse stored data tags through an intuitive tree directory.
- An intelligent SQL editor with support for syntax highlighting and keyword suggestions, enabling you to query the data you need with precision.
- An integrated AI Data Analysis Assistant that enables the generation and iterative refinement of complex SQL queries using natural language, significantly lowering the barrier to data querying.
- Query results can be flexibly displayed as tables or charts, with support for chart interactions (zooming, downloading).

**Dashboards:**

- Allows you to create and customize personalized data visualization dashboards.
- By configuring multiple Panels, each bound to one or more SQL queries, you can centralize key data in various formats such as line charts, bar charts, statistical values, or tables.
- Supports flexible time range selection and automatic refresh mechanisms, ensuring you are always looking at the latest data trends.
- Drag-and-drop functionality to adjust Panel layout and size, creating a view that best suits your monitoring needs.

> For a detailed guide on NeuronEX Dashboard, read: [Visualizing Your Industrial Data: A Guide to NeuronEX Dashboard](https://www.emqx.com/en/blog/visualizing-your-industrial-data) 

### Enabling the Feature

To use the Data Insights feature, you need to enable the internal time-series database. After logging into the UI, navigate to **Administration -> System Configuration -> Data Storage Configuration**, and click the **Time-series Database Datalayers** button, as shown below.

![image.png](https://assets.emqx.com/images/da280f33112e01be4031f0094b9501bf.png)

Next, navigate to **Data Collection -> North Apps -> DataStorage**, click the **Add Subscription** button, and select the data you want to store in the time-series database.

![image.png](https://assets.emqx.com/images/a9bb8f190fc3c70026a2e70de1606cb7.png)

This article will introduce the operational instructions for the Data Analysis section.

## **Data Analysis Feature Preview**

Navigate to **Data Insights -> Data Analysis** to enter the main data analysis page, as shown in the figure.

The page is typically divided into:

- **Left Data Source Navigation Area:** Displays data in a tree structure.
- **Top-Right SQL Input & Configuration Area:** For writing and executing SQL queries.
- **Bottom Results Display Area:** Shows query results (in table or chart format).

![image.png](https://assets.emqx.com/images/07be176c035adbad9f4db9aff53690b6.png)

## **In-Depth User Guide**

### **Data Source Tree Directory**

- **Structured Display:** The left panel clearly lists the Southbound drivers that have Datalayers storage enabled, their underlying groups, and specific data tags in a tree structure.
- **Type Display:** The data type stored in Datalayers (e.g., Int, Float, Bool, String) is clearly marked next to each tag, helping users construct correct queries.
- **Convenient Operations:**
  - **Refresh:** Supports manual refreshing of the tree directory to get the latest driver/group/tag information.
  - **Tag Search:** Provides a search function for tag names to quickly locate target tags.
  - **SQL Query Samples:** When a data tag is selected, the system automatically provides common SQL query samples, such as:
    - **Query Column:** Query the latest 100 data tags for this tag.
    - **Query Period:** Query the data for this tag over the past day.
    - **Query Max:** Query the maximum value for this tag. Users can use these samples directly or modify them.
  - **AI Query (Integrated with LLM):**
    - After selecting a tag, you can choose the "AI Query" function.
    - The system will automatically pre-fill the tag name and corresponding table information (e.g., `neuron_float, tag='your_tag_name'`) into the AI interaction box or pass it as context to the AI.
    - Users can describe their query needs in natural language (e.g., "query the hourly average value for this tag over the past day"), and the integrated LLM will generate the complex SQL query statement.

### **Intelligent SQL Input Area**

- **Writing Assistance:**
  - **Keyword Suggestions:** Provides auto-completion suggestions for common SQL keywords as you type.
  - **Syntax Highlighting:** Applies syntax highlighting to SQL statements to improve readability.
- **Query Limitations:**
  - **Single Query:** Currently supports the execution of a single SQL query statement at a time.
  - **Query-Only:** Only query-type SQL statements (SELECT) are accepted. To ensure data security and system stability, data definition or modification operations such as `CREATE TABLE`, `INSERT`, `DELETE`, or `UPDATE` are not supported.

### **Results Display Area**

- **Multi-View Display:** The results of each successfully executed SQL query are displayed in this area as either a Table or a Chart.
- **Table Display:**
  - The default view, presenting the query results clearly in a row-column format.
  - Supports basic table operations like pagination and sorting (specific functionality depends on the front-end table component).
- **Chart Display:**
  - **Conditions for Charting:** If the SQL query result contains a timestamp field and a numeric field, the system will automatically enable switching the result to a chart view.
  - **Chart Types:**
    - **Line Chart:** Suitable for visualizing trends in time-series data.
    - **Bar Chart:** Suitable for comparing data volumes across different categories or time points.
  - **Interactive Features:**
    - **Chart Zoom:** Supports zooming in on specific parts of the chart to view details.
    - **Save/Download:** Supports saving the current chart as an image file (e.g., PNG) to your local machine.
    - **Legend Interaction:** (Typically supported by chart libraries) Clicking on a legend item can show/hide the corresponding series, making it easier to focus your analysis.

### **AI Data Analysis Assistant Integration**

The Data Analysis page is deeply integrated with the AI Data Analysis Assistant, designed to help users build and optimize SQL queries more easily. 

> To use this feature, users must first enable the AI functionality and configure the model to be used.

Navigate to **Administration -> System Configuration -> AI Agent**, and click the **Enable AI Agent** button, as shown below.

![image.png](https://assets.emqx.com/images/b5655c1560ac8ef97505d5baca6d90b1.png)

To configure a model, navigate to **Administration -> System Configuration -> AI Model Configuration**, and click the **Add Model Configuration** button. Currently, models from DeepSeek, SiliconFlow, OpenAI, and Azure OpenAI are supported. Users will need to have an API Key from the respective platform.

![image.png](https://assets.emqx.com/images/1b35579c85718f24895cc3c4006201c5.png)

**UI Entry:**

- Click the **AI Data Analysis** button in the top-right corner of the page to open the AI interaction dialog.
- As mentioned earlier, a shortcut for **AI Query** is also available in the tag's context menu.

**AI Core Capabilities:**

- **Natural Language to SQL:** Converts a user's natural language query requests into correct SQL statements.
- **Iterative SQL Correction:** If a generated SQL query fails, the AI can intelligently analyze the cause of the error and use system-provided tools (like querying the table schema) to perform multi-round iterative corrections until a successful SQL query is generated.

## **Conclusion**

With the solid foundation of a built-in time-series database, an intuitive and efficient data analysis interface, and the revolutionary AI Data Analysis Assistant, [NeuronEX](https://www.emqx.com/en/products/neuronex) breaks down the traditional barriers to industrial data querying and analysis. Users no longer need to be SQL experts; they can easily uncover trends, correlations, and anomalies in time-series data using natural language, bringing dormant data to life to truly serve production optimization, predictive maintenance, and intelligent decision-making.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
