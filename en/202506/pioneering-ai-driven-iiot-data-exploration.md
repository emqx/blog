## **Overview**

With the rapid advancement of artificial intelligence (AI) technologies, industrial enterprises are increasingly exploring their potential in smart manufacturing and industrial data analytics. Meanwhile, the Industrial Internet of Things (IIoT) continues to drive the evolution of device connectivity and data collection, providing a robust data foundation for AI-enabled industrial applications.

This article demonstrates an application for IIoT data exploration and analysis, integrating multiple cutting-edge technologies. The application combines large language models (LLM), Retrieval-Augmented Generation (RAG), Model Context Protocol(MCP), Sparkplug B protocol, MQTT message broker, time-series databases, and relational databases. It delivers an intelligent, interactive industrial data application, enabling users to query device data, analyze historical metrics, and monitor status by simply entering natural language queries in a dialogue box. The system also vectorizes product manuals, automatically providing users with relevant solutions when error codes are reported, facilitating rapid issue identification and resolution.

Readers will gain insights into developing AI-driven IIoT applications and leveraging AI’s value in industrial manufacturing scenarios.

## **Scenario Description**

We assume a typical industrial scenario with the following structure defined using the SparkPlug B protocol:

- **Factory**: Identified as `factory_1` in SparkPlug.
- **Production Line**: Identified as `assembly_1` in SparkPlug.
- **Specific Device**: Identified as `demo` in SparkPlug (nicknamed "Optimus Prime," with this information stored in a third-party relational database).

In this demo, we simulated the runtime data of an ABB FlexPendant virtual device and used its public documentation as the knowledge base. ABB FlexPendant is a handheld touchscreen device used for programming and controlling industrial robots. This device serves as the user interface for the robot controller, allowing operators to perform various operations such as modifying and running programs, teaching new robot actions, and adjusting parameters. To simplify the scenario, we define the following data tags, representing:

- Voltage and current values of the robotic arm.
- Diagnostic error codes.

```json
{
  "robotic_arm": { "voltage": 3.14, "current": 5.0},
  "diagnose": {"error_code": 50153}
}
```

### **Interactive Scenario Examples**

Users can interact with the system through an AI dialogue box. The system incorporates built-in Agentic capabilities and integrates various MCP services, automatically generating relevant query requests based on user needs and returning data analysis reports. Typical interaction scenarios include:

- **List the tree structure of device** `demo`: The AI queries relevant data and displays the logical structure diagram of the device.
- **Query the latest** `robotic_arm/voltage` tag data for device `demo`: The AI retrieves the most recent data reported for the `robotic_arm/voltage` tag of the `demo` device.
- **Analyze the past week's** `robotic_arm/voltage` tag data for device `demo`: The AI queries and analyzes one week's worth of `robotic_arm/voltage` data for the `demo` device stored in the TDengine database. Given the potentially large data volume, the AI will automatically aggregate the data based on built-in instructions and provide a corresponding analysis report.
- **Query the latest** `robotic_arm/current` tag data for the device nicknamed "Optimus Prime": Since the user queries using the nickname "Optimus Prime," the AI retrieves the corresponding device ID (`demo`) from the MariaDB MCP service and fetches the latest data point.
- **Query the latest** `diagnose/error_code` tag data for device `demo`: The AI retrieves the latest `diagnose/error_code` tag, uses RAG technology to access relevant manual knowledge from the vector database, and presents the user with a comprehensive error report and solution.
- **Analyze the past day's** `diagnose/error_code` tag data for device `demo`: The AI queries the diagnostic error codes from the past day, combines them with operational manual data from the vector database, and generates a comprehensive error report, solutions, and recommendations.

## Demo

### **List the tree structure of device** `demo`

Below is a screenshot of the result after the user inputs "List the tree structure of device `demo`".

![image.png](https://assets.emqx.com/images/3af5aa7a3e63b3fbf4060f5e1e505a2c.png)

### Query the latest `robotic_arm/current` tag data for the device nicknamed "Optimus Prime"

1. **Overview**
   - **Analysis Time Range:** Latest data point (real-time)
   - **Record Count:** 1 entry
   - **Key Findings:** The latest current value for the device with alias **"Optimus Prime"** (actual device key: **demo**) is **2.5A**.

2. **Detailed Analysis**

   ![image.png](https://assets.emqx.com/images/9f370170ce2075a60357213755653b71.png)

3. **Diagnosis & Recommendations**
   - **Current Status Assessment:** The current value is within the normal range (typical operating current for ABB FlexPendant robots is 2–6A).
   - **Recommended Actions:**
     - Continue monitoring the trend of this value.
     - If it consistently stays below 3A, consider checking:
       - Whether the robotic arm is underloaded
       - Whether the program is executing completely
       - Whether the power supply voltage is stable

4. **Additional Notes**

   This report is based on a single-point instantaneous data sample. For trend analysis, it is recommended to query data over a time range. Normal current fluctuation for ABB FlexPendant devices is within ±10% of the nominal value.

### Analyze the past week's `robotic_arm/voltage` tag data for device `demo`: 

**Device Name:** demo

**Tag:** robotic_arm/voltage

**Time Range:** 2025-05-13 to 2025-05-20

1. **Data Overview**
   - **Total Raw Records:** 8,982
   - **Sampling Strategy:** 6-hour average aggregation (28 data points in total)
   - **Voltage Range:** -17.40V to 3.40V

2. **Key Findings**
   - **Stable Main Voltage:** 3.40V (observed during most time periods)
   - **Abnormally Low Voltage:** -17.40V (requires further investigation)

…

### Query Latest `diagnose/error_code` Data for Device `demo` and Retrieve Related Knowledge Base Information

1. **Overview**
   - **Device Name:** demo
   - **Analysis Time:** Latest data
   - **Tag:** diagnose/error_code
   - **Key Finding:** The device has reported **error code 10139**

2. **Error Details**

   ![image.png](https://assets.emqx.com/images/b2ef52a41fa180dcfd67932836c505fb.png)

3. **Diagnostic Analysis**
   - **Error Description:** This error indicates that the system stopped execution as a safety measure due to an edit monitor timeout.
   - **Impact Scope:**
     - RAPID program execution was interrupted
     - Robot operation is paused
   - **Possible Causes:**
     - Watchdog commands were not sent periodically during RAPID and main program execution
     - RobotControlMate connection issues (if in use)
     - Misconfigured system monitoring parameters

4. **Recommended Solutions**

   - **Immediate Actions:**
     **[Basic Fix]**

     - Check and restart RAPID program execution
     - Verify RobotControlMate connection status (if applicable)

     **[Configuration Adjustment]**
     *If not using RobotControlMate:*

     1. Open the controller configuration interface
     2. Navigate to `Controller/OperatorSafety/Heartbeat`
     3. Set the parameter value to `"False"`
     4. Save changes and restart the system

   - **Long-Term Prevention:**

     - Regularly inspect the watchdog command mechanism
     - Establish a heartbeat monitoring log system
     - Consider upgrading to the latest control system software

   - **Notes**
     - Back up current settings before modifying configuration parameters
     - Restarting may cause loss of unsaved program changes
     - Maintenance is recommended during non-production hours

Would you like more detailed guidance on RAPID program debugging or other related topics?

## **Related Technologies and Software**

The software used in this application is as follows:

![image.png](https://assets.emqx.com/images/7024315d9f20188aae8aa642901a2fa4.png)

- **Industrial Data Collection Software - NeuronEX:** Defines data collection and includes a northbound Sparkplug B plugin to report tag data to the cloud in Sparkplug B format.
- **Message Broker - EMQX:** 
  - Receives Sparkplug B data packets reported from the edge. 
  - The Sparkplug App subscribes to relevant topics, storing the data in a time-series database.
- **Time-Series Database - TDengine:** Stores tag data reported by devices and provides flexible data access capabilities.
- **Relational Database - MariaDB:** Stores the mapping between devices and their nicknames, e.g., the device demo is nicknamed "Optimus Prime," facilitating the connection between OT and IT systems. In real-world business systems, this represents IT system data such as MES, ERP, and CRM.
- **LLM - Deepseek v3:** Powered by Deepseek v3 from SiliconFlow.
- **RAG Knowledge Base:** 
  - Supports BAAI/bge-base-en-v1.5 and Aliyun vector models. 
  - Uses a local MilvusVectorStore for the vector database. 
  - User manuals are vectorized and stored in the vector database. When users query error codes, the application retrieves relevant content from the vector database, and the LLM generates solutions and recommendations based on this data.
- **MCP:**
  - Encapsulates MCP services for TDengine time-series data to retrieve device-reported tag data, node status, and device online/offline information.
  - Encapsulates MCP services for MariaDB relational data to store mappings between OT device data and IT business data, e.g., the OT identifier demo corresponds to the IT nickname "Optimus Prime." Users typically query data using IT nicknames or aliases.

The relevant code has been open-sourced, and readers can access the source code at [GitHub - emqx/uns-demo: Use natural language to explore IIoT Sparkplug B data by leveraging MCP, AI and agent](https://github.com/emqx/uns-demo).

## **Summary**

This article briefly introduces how to leverage AI and various foundational software to build a cutting-edge IIoT data exploration application, providing insights for readers to develop their own AI-driven industrial applications. The EMQ industrial team is planning to officially integrate Sparkplug B data reporting, storage, and AI-based analysis into the EMQX ECP, with a release expected in the second half of the year. Interested readers are welcome to contact our sales team for early access.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
