A leading food and beverage manufacturer employs EMQX's UNS solution to boost production efficiency. As mentioned by the management, the entire food industry operates on tight margins, where every second of downtime and every defective product counts. However, with growing market demand, the challenge for them is clear: how to continuously boost production efficiency while ensuring every single product is perfect?

This is why they have decided to implement an Overall Equipment Effectiveness (OEE) system. OEE is more than just a number; it is a strategic tool for achieving transparency on the production lines and for tightly integrating efficiency, quality, and food safety.

## OEE: More Than Just Output Efficiency

We all know that even a small issue in the production process can impact the final product. Traditional production metrics often focus on a single dimension, such as output. Many production details are being neglected. However, OEE is unique because it measures productivity across three critical dimensions:

- **Availability:** How long is the equipment actually running during scheduled production time?
  - **Availability = Actual Uptime / Total Scheduled Uptime**
- **Performance:** When the equipment is running, is it operating at its optimal speed?
  - **Performance = Actual Performance / Target Performance**
- **Quality:** Of all the products we produce, how many meet all of the standards to be considered "good products"?
  - **Quality = Good Parts / Total Produced Parts**

These three dimensions collectively provide a true picture of the health of the production lines. The OEE formula is as follows:

- **OEE = Availability x Performance x Quality**

## Why UNS is Key to Modern OEE

At EMQ, we understand that achieving world-class manufacturing excellence requires more than just knowing your OEE score. The true challenge lies in building a robust foundation that can reliably collect, process, and deliver manufacturing data unstoppable day-by-day at scale, instead of relying on fragmented data and manual logging, simply can’t keep up.

An effective OEE system for a modern company must be:

1. **Real-Time:** Data must be collected and delivered instantly to provide accurate, up-to-the-second OEE scores, turning raw data into actionable insights.
2. **Scalable:** The system must handle thousands of data points from diverse equipment across multiple production lines without breaking down.
3. **Secure & Reliable:** In an industry where safety is non-negotiable, every data point must be delivered reliably and securely.
4. **Integrable:** It must seamlessly connect to existing business systems (like MES and ERP) to create a unified data ecosystem.

These properties enabled by a UNS make calculating the OEE more accurate, adaptable, and beneficial for proactive decision-making.

## EMQX's UNS Solution: MQTT as the Backbone

EMQX's UNS solution is built on **MQTT**, the global standard for IoT messaging. Its lightweight, publish-subscribe architecture is perfectly suited for industrial environments. There are two main software components in the UNS solution: **[EMQX](https://www.emqx.com/en/platform)** as an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and **[NeuronEX](https://www.emqx.com/en/products/neuronex)** as an Edge Gateway that translates various industrial protocols to MQTT.

- **Availability:** By leveraging NeuronEX, we can capture machine state changes and downtime reasons from PLCs and sensors the moment they occur. This eliminates manual data entry delays and provides an instant, accurate picture of machine availability. NeuronEX has 70+ industrial protocols conversion modules, including OPC UA and Modbus, as required by the food company. This ensures we can connect to virtually any asset on the factory floor.
  Machine availability is accurately captured through direct signals from PLCs or sensors, with the NeuronEX edge gateway sending real-time Actual Uptime and downtime data to the EMQX broker. In parallel, EMQX's robust data connectors allow it to retrieve Scheduled Uptime and downtime from the food company's MES system, such as SAP. By seamlessly combining these two crucial data streams, the Availability metric is easily calculated. This process is a great example of benefiting from IT and OT convergence.

- **Performance:** Performance losses are often the most difficult to detect. Our platform collects granular data on cycle times and production counts in real-time, enabling a precise analysis of speed losses. Every machine has an optimal operating performance, or Target Performance, which is defined by its specifications and maintenance schedules. However, micro-stops still occur due to machine failures, material shortages, or human error.

  These events generate a vast amount of data. Before being sent to the EMQX broker, NeuronEX filters and cleans this data. Then, EMQX's rule engine gathers and processes all the data streams from the various machines, providing the Actual Performance data. By comparing the Actual Performance against the Target Performance, we can accurately measure speed losses.

- **Quality:** For food manufacturing, quality is paramount. To ensure this, the food company has invested in redundant hardware and sensors to track every process in production.

  The EMQ solution integrates data from these inline quality sensors, such as foreign object detectors and vision systems, directly into the OEE calculation. It also provides a robust interface for quality control operators to log events, scrap amounts, and their root causes, ensuring a complete and accurate picture of product integrity. This data is also compared with the food recipes in the MES system to see whether scrap foods are due to its recipe.

  The EMQX broker acts as a central repository, keeping all this data in a hierarchical structure according to UNS ISA-95 standards. This integrated approach allows **Good Parts** to be easily obtained by subtracting **Scrap Parts** from **Total Parts**.

## From Metrics to Action: A Guide to Improving Production with OEE

Having the OEE metric is just like having a detailed health report for your production line. The next, and most crucial, step is to use that report to diagnose issues and implement effective solutions. The food company starts with some small issues, but the biggest losses are revealed by the OEE data. This could reduce the chance of having great impacts or unexpected outcomes on the production. For example:

- They found that the product slicer frequently experiences minor stops due to food jams, significantly impacting performance and quality. By analyzing the OEE data, they discovered that the slicer's blade rotation speed needed adjustment. Implementing a preventive maintenance schedule that includes regular blade speed checks and adjustments can significantly reduce these stops and product scraps, ultimately improving the overall Performance and Quality.
- In OEE dashboard, a temperature discrepancy was found between the oven machine's display and the newly invested redundant system. Upon investigation, they discovered that the sensors on the oven machine had been mis-calibrated recently. Implementing a double-check procedure during machine maintenance can reduce such configuration or calibration issues caused by human error, significantly improving the safety and quality of food products.
- OEE data revealed that the Performance score of one particular section was consistently lower than the others. The data also indicated frequent, small-time machine halts with the same error messages being logged. They then called for maintenance service from the machine supplier and discovered that a specific conveyor belt kept briefly jamming. With the precise OEE data, they were able to immediately take action to replace the faulty part.

The key is to start small. Don't try to fix everything at once. Pick the one or two biggest losses revealed by the OEE data, address the issues, and then move on to the next. This continuous cycle of improvement will steadily increase the production efficiency and ultimately the company's profitability and reputation for quality.

![image.png](https://assets.emqx.com/images/0fe025215e391ff6537546bb98870895.png)

## Beyond OEE: The Path to Digital Transformation

EMQ solution goes beyond simply calculating OEE. It lays the groundwork for a broader digital transformation:

- **Comprehensive Traceability:** We connect production data to batch information, providing a complete chain of custody for every product. This is essential for **HACCP compliance** and for minimizing the impact of any potential recalls.
- **Predictive Maintenance:** By analyzing real-time data streams from equipment, our solution can enable predictive maintenance, anticipating potential failures before they lead to costly downtime.
- **Unified Data:** We provide the "data highway" that connects the shop floor to the top floor. By integrating OEE data with MES and ERP systems, we provide plant managers with a single source of truth for making informed, data-driven decisions.

## Quantifying the Impact: The ROI of a Smart OEE Solution

Implementing a modern OEE system is a strategic investment with a rapid return. Our solution delivers tangible ROI through:

- **Reduced Waste and Rework:** By identifying and resolving quality issues in real time, our system dramatically reduces the number of defective products that end up as waste, leading to direct savings on raw materials and processing.
- **Increased Throughput:** Optimizing Availability and Performance translates directly into higher production volume. By recovering just a few percentage points of lost time, companies can significantly increase their output without investing in new equipment.
- **Lower Maintenance Costs:** Predictive maintenance capabilities allow for proactive repairs, preventing catastrophic equipment failures that are far more expensive to fix. It also extends the lifespan of machinery, delaying the need for capital expenditure.
- **Operational Efficiency:** Real-time data and root cause analysis tools enable managers to make better decisions about resource allocation, shift scheduling, and process improvements, leading to more efficient use of labor and energy.

By partnering with EMQ, the food company isn't just implementing an OEE system; they are building a resilient, intelligent manufacturing infrastructure. We are proud to be the foundation for their digital journey towards a smarter, safer, and more productive future.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
