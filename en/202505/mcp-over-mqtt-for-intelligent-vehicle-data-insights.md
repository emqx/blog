## **Introduction**

With ongoing advances in AI and in-vehicle computing, the digital transformation of modern vehicles is accelerating. Vehicle networking systems are evolving beyond traditional cloud architectures by integrating edge computing and AI to reshape human-vehicle interaction. An automated analysis framework built on multi-source data enables the generation of insightful visual reports, greatly improving data efficiency for business teams.

This article explores a solution that combines a vehicle-cloud collaborative architecture with the MCP over MQTT protocol, using driving behavior analysis and vehicle control as examples. The solution reduces data processing costs, enhances data security, and builds a real-time analytics engine through data fusion. Looking ahead, it can deliver in-depth insights—such as driving habit analysis and vehicle diagnostics—by establishing multidimensional business data models, offering predictive digital services for drivers.

## **Opportunities and Challenges in Driving Behavior Analysis**

As vehicle connectivity evolves, driving behavior analysis is shifting from a basic safety assessment tool to a central value driver across the vehicle lifecycle. For example, commercial auto insurers use key indicators—such as rapid acceleration and late-night driving—to build usage-based insurance (UBI) models, significantly improving risk-based pricing accuracy. Logistics companies leverage data like top speed and harsh braking frequency to build driver profiles, effectively reducing accident rates over millions of kilometers. These applications are reshaping the cost structure of the traditional transportation industry.

Today, most solutions rely on cloud-based architectures, where raw driving data—such as harsh acceleration or braking, night driving duration, top speed, and seatbelt usage—is uploaded to the cloud for analysis. However, this approach presents several key challenges:

- **High cost of raw data processing:** Transmitting, storing, and analyzing large volumes of vehicle data consumes significant resources. Without clear value extraction, these become sunk costs.
- **Data loss due to network instability:** Unreliable cloud connectivity can result in missing critical data, undermining the reliability of analysis outcomes.
- **Privacy concerns:** Uploading sensitive personal driving data to the cloud without proper anonymization increases the risk of data breaches.
- **Low efficiency in data fusion:** Integrating diverse data sources—such as maps, weather, and real-time traffic status—is complex and slows the generation of actionable insights.

## **A Vehicle-Cloud Collaborative Solution Based on MCP over MQTT**

To address the challenges, EMQ offers a smarter, more efficient, and reliable solution for driving behavior analysis by combining the MCP over MQTT protocol with a vehicle-cloud collaborative architecture.

Using the SDVFlow software, in-vehicle data is processed directly at the edge, with results stored locally on the vehicle. These results are then encapsulated by an on-board MCP service. Through the MCP over MQTT protocol, the service is registered with EMQX. With user permission, the system can dynamically access and retrieve the locally stored driving behavior data. By integrating additional MCP services and leveraging large language models (LLMs), a comprehensive driving behavior analysis report can be generated dynamically.

![A Vehicle-Cloud Collaborative Solution Based on MCP over MQTT](https://assets.emqx.com/images/d690c25f3f8e56aedb67ee819d24ec47.png)

### **Key Benefits**

- **Cost Reduction:** Significantly lowers data transmission and storage costs, while optimizing the use of on-board computing resources to reduce cloud computing demand.
- **Privacy Protection:** Users retain control over when and how analysis results are shared, reducing the risk of data breaches.
- **Intelligent Insights:** Dynamically orchestrates vehicle/cloud-based MCP tools—such as map, weather, and traffic data—via LLMs to quickly generate high-value driving analysis reports.

In cases where the vehicle is offline, a workflow can be pre-defined to trigger automatically when the vehicle comes online, ensuring timely execution of the data retrieval and analysis process.

### **Workflow**

1. The AI workflow, acting as an MCP client, first retrieves a list of tools deployed on the in-vehicle MCP server. These tools provide core driving behavior data, including:
   - **Harsh Acceleration:** Timestamp and GPS location
   - **Harsh Braking:** Timestamp and GPS location
   - **Top Speed:** Timestamp, GPS location, and top speed
2. Map Geocoding Service: Calls the MCP service exposed by the map service to retrieve administrative region information based on GPS location.
3. Historical Weather Service: Wraps a third-party API as an MCP service to query historical weather data using administrative region and timestamp as input.
4. Using all the above data, the system generates a complete driving behavior analysis report.

The corresponding demo code is available at: [GitHub - emqx/sdv-mcp-demo](https://github.com/emqx/sdv_mcp_demo). Before running the program, please read the `README.md` carefully. You will also need to apply for App Keys from the required third-party services and configure them in the `.env` file.

**Additional Notes:**

- To simplify the demo workflow, the codebase uses simulated driving behavior data located in `data/vehicle_00001.json`. In a production environment, this data should be generated by the SDVFlow software.
- The system prompt has a significant impact on the quality and format of the generated report. Users can refer to the `prompts/system.txt` file in the repository to customize the prompt and adjust the output format as needed.
- In real-world deployments, vehicle connectivity is not guaranteed at all times. Therefore, additional logic should be implemented to ensure the vehicle is online before initiating data retrieval. For example, subscribe to wildcard topics for vehicle online/offline events and trigger the AI workflow only when a vehicle comes online.

## **Sample Report**

This driving behavior analysis report was automatically generated by the DeepSeek V3 model based on simulated data. Notably, it accurately identified the snowy weather conditions in Huairou District, Beijing on January 12, 2023. The AI demonstrated sound judgment when evaluating driving behavior under such special weather circumstances.

**Vehicle ID:** 00001

**Analysis Period:** January 1 – January 13, 2023

### I. Data Summary

- **Total Driving Events:** 5
- **High-Risk Events:** 3 (Harsh Acceleration / Harsh Braking)
- **Top Recorded Speed:** 98 km/h
- **Main Driving Areas:** Beijing (Chaoyang District, Huairou District)

### II. Driving Behavior Analysis

#### Speed Behavior

| **Metric**      | **Value** | **Industry Benchmark** | **Assessment**     |
| :-------------- | :-------- | :--------------------- | :----------------- |
| Top Speed       | 98 km/h   | ≤ 80 km/h              | ⚠️ Overspeeding     |
| Average Speed   | 56 km/h   | 40–60 km/h             | ✅ Normal           |
| Overspeed Count | 1         | 0                      | ⚠️ Attention Needed |

- On January 13, the vehicle reached 98 km/h, exceeding typical urban speed limits (commonly 80 km/h).
- Speed was well controlled during other periods, compliant with urban driving standards.

#### Acceleration & Braking Behavior

| **Event Type**     | **Occurrences** | **Environmental Context** | **Risk Level** |
| :----------------- | :-------------- | :------------------------ | :------------- |
| Harsh Acceleration | 1               | Sunny / Dry Surface       | Medium         |
| Harsh Braking      | 3               | 2 in Snow / 1 in Cloudy   | High           |

- **Notable Incident:** On January 12, during snowfall, two consecutive harsh braking events occurred (deceleration > 0.4g).
- **Likely Cause:** Reduced braking efficiency due to icy roads led to emergency braking.

### III. Environmental Correlation Analysis

| **Weather** | **Harsh Acceleration** | **Harsh Braking** | **Overspeed** |
| :---------- | :--------------------- | :---------------- | :------------ |
| Sunny       | 1                      | 0                 | 0             |
| Snowy       | 0                      | 2                 | 0             |
| Cloudy      | 0                      | 1                 | 1             |

**Key Insight:** 

- Snowy weather led to a 200% increase in braking-related risk events.
- Good weather conditions were associated with a higher likelihood of speeding.

### IV. Risk Diagnosis and Recommendations

#### 1. Risk Behaviors

**Overspeeding (98 km/h)**

- **Conditions:** Cloudy with strong wind
- **UBI Risk Factor:** +15%

**Consecutive Harsh Braking (Snowy Conditions)**

- **Issue:** Poor adaptation to icy road conditions
- **UBI Risk Factor:** +20%

#### 2. Improvement Recommendations

**Driver Training:**

- Specialized training on braking techniques for icy roads
- Speed awareness training; consider installing audio overspeed alerts

**Vehicle Inspection:**

- Check tire wear, especially winter tread depth
- Conduct ABS system diagnostics

**Insurance Recommendations:**

- **Current Risk Level:** Grade B (Moderate to High)
- **Suggested Premium Adjustment:** +8% (may increase to +15% if no improvements are made)

> *Note: This report is generated from real-time vehicle OBD data, sampled at 1-second intervals with location accuracy ≤ 5 meters.*

## **Conclusion**

EMQ’s MCP over MQTT-based solution offers a new approach to driving behavior analysis by shifting data processing from the cloud to the vehicle. This edge-first architecture significantly reduces transmission and storage costs, while giving users greater control over data privacy through permission-based access.

By combining in-vehicle analysis with cloud-based data sources and leveraging large language models to generate dynamic reports, the solution creates a streamlined, intelligent workflow from data collection to insight generation.

This practical architecture supports the ongoing integration of vehicles, infrastructure, and the cloud, and demonstrates how data value can drive digital transformation across the connected vehicle ecosystem. As in-vehicle systems continue to evolve toward smarter, more autonomous decision-making, this approach lays the groundwork for broader innovation and enhanced user experiences.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
