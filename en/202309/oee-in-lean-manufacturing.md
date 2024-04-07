OEE, as defined in our [previous post](https://www.emqx.com/en/blog/a-deep-dive-into-kpis-for-smart-manufacturing), stands for Overall Equipment Effectiveness, and it is an important part of lean management practices. This metric serves as a central focus for manufacturing companies as a universally accepted gauge and benchmark for measuring productivity. Originally developed by the Japan Institute of Plant Maintenance, OEE is a comprehensive tool for evaluating both the technical and organizational dimensions of manufacturing facilities.

## OEE Objectives

At its core, OEE provides a comprehensive and objective view of the current state of productivity within a manufacturing environment. It enables companies to assess how effectively their equipment and processes are operating relative to their full potential. By considering factors such as equipment availability, performance efficiency, and production quality, OEE provides a holistic view of the overall effectiveness of the manufacturing process.

The power of OEE lies in its ability to systematically uncover opportunities for improvement. By analyzing the individual components that contribute to OEE - downtime, speed loss, and defects - it is possible to identify bottlenecks, inefficiencies, and areas for improvement. This data-driven approach enables companies to make informed decisions about process optimization and resource allocation.

OEE also serves as a compass for continuous improvement. By consistently monitoring and striving to improve OEE, manufacturing companies ensure a sustainable trajectory of improvement in their economic performance. This metric not only reflects immediate productivity status but also helps set realistic performance goals and evaluate the success of various improvement initiatives over time.

## How to Calculate OEE

OEE constitutes the proportion of fully productive duration in relation to the scheduled production period. Its computation relies on three factors: availability, performance, and quality.

1. Availability strives to eliminate interruptions, ensuring smooth operations. 
2. Quality focuses on perfection, aiming to reduce defects. 
3. Performance seeks to prevent slowdowns, maintaining high efficiency.

OEE can be calculated using the following formula, where availability, performance and quality are metrics of manufacturing: 

**OEE = Availability x Performance x Quality**

### Availability

Availability measures the amount of time your machines are running compared to the amount of time they are scheduled to run, expressed as a percentage. To calculate availability, divide the actual uptime by the total scheduled uptime, then multiply by 100 for the percentage. 

**Availability = Actual Uptime / Total Scheduled Uptime**

While scheduled machine uptime is evident from the production schedule, tracking actual uptime requires aggregating all downtime and subtracting it from the sum of scheduled uptime. Examining downtime data not only reveals the reasons for downtime but also identifies opportunities for improvement.

### Performance

To determine Performance, it is essential to compare the actual units produced with the potential output achievable during the effective operating time of the machine at maximum speed. 

**Performance = Actual Performance / Target Performance**

Actual performance is calculated by counting all units, including scrap. On the other hand, Target performance is determined by multiplying the maximum hourly production of parts by the actual running time of the machine, which represents the potential production capacity within this period.

### Quality

Quality is the third facet of OEE that must be calculated. It is the proportion of satisfactory parts that meet quality standards out of the total number of parts produced. 

**Quality = Good Parts / Total Produced Parts**

In practice, determining the number of good parts is typically accomplished by subtracting the number of scrap and reworked parts from the known total number of parts produced during a given time period. The equation states that the total number of parts produced is equal to the sum of the good parts, the scrap parts, and the reworked parts.

## OEE Performance Score

If there is no negative affection on availability, performance and quality, a perfect OEE of 100% is achieved. This means the production of fully satisfactory parts at maximum speed without any interruptions. While achieving this theoretical score is impractical in reality, an OEE score above 80% is considered exemplary. The majority of manufacturing operations fall within the OEE range of 60% to 80%. It's reasonable to assume that any plant with an OEE below 60% has significant deficiencies. A score at this level serves as a warning signal that there is significant room for improvement.

- 80% - 100% is outstanding - impractical in reality
- 60% - 80% is excellent - the majority of manufacturing performance
- 60% or below is underperformance - a significant room for improvement. 

## Six Big Losses

The primary objectives of OEE initiatives are to mitigate or eliminate the so-called Six Big Losses. These are the major factors responsible for lost productivity associated with equipment in the manufacturing process.

![Six Big Losses](https://assets.emqx.com/images/72e6794a0b877704a33ed8e9ffc62ebc.png)

### Availability Loss

A fundamental element of OEE is the availability of manufacturing machines and systems. Uptime is the amount of time a machine or system is operational and contributes to productivity. Conversely, downtime occurs when a machine is intended to operate but is unable to do so, resulting in financially costly downtime.

1. Planned Stops

   Planned events that cause machine downtime contribute to losses in OEE. These include changeovers, maintenance, inspections and cleaning. By using specialized software, these planned stops can be carefully analyzed and improved to minimize their impact, providing significant room for improvement despite their non-negative nature.

2. Unplanned Stops

   When scheduled production is interrupted by unexpected events such as malfunctions, crashes, power outages, natural disasters or sickness absences, it's called an unplanned stop. To reduce these unproductive periods, accurate reason tracking, digital categorization and continuous analysis help identify process weaknesses.

### Performance Loss

Another key component of OEE is machine and system performance. This refers to the actual production output within a specified operating time, relative to the maximum theoretically achievable output. Performance losses can result from brief interruptions or excessively slow operating speeds.

1. Small Stops

   Micro-stops of less than a minute are caused by tool problems, programming errors, sensor jams or quick cleaning needs, and are typically handled by the operator. Although they go unnoticed, these interruptions add up to minutes of unproductive time. Micro-stops are predictable and can be eliminated or managed.

2. Slow Cycles

   When a machine operates below its potential maximum speed due to factors such as age, maintenance, errors, or materials, losses occur. Unlike micro-stops, production continues, but at a slower rate. If ideal run times aren't known, management can define them based on historical data. Research is key to identifying these times.

### Quality Loss

In OEE, quality losses refer to deviations from expected quality standards. However, the impact of quality loss is severity larger than the other two. This is due to both the material waste associated with defects and the time invested in unsuccessful production efforts. 

Even if the defective parts can be repaired, the time required for rework, which involves both operator and machine resources, is still considered losses.

1. Production Rejects

   Certain production problems are not apparent until after manufacturing, such as overpackaging, underpackaging, mislabeling, or faulty packaging. These problems can be significantly mitigated by technological solutions such as sensors or cameras that identify quality issues in real-time. Combined with specialized OEE software, the sixth major loss is likely to become obsolete in the near future.

2. Startup Rejects

   This loss occurs when a machine produces defective parts due to instability during startup, setting changes, or part adjustments. Operator expertise is critical to making accurate settings without trial and error. Automated digital assistance can quickly and significantly reduce this major loss.

## Insufficiency of Using OEE Only

As the field of [smart manufacturing](https://www.emqx.com/en/blog/the-smart-manufacturing-revolution) advances, it is becoming increasingly clear that relying solely on Overall Equipment Effectiveness (OEE) may not provide a holistic understanding of an organization's success in its smart manufacturing endeavors. Organizations should have broader insight into the evaluation of smart manufacturing initiatives to encourage continued expansion and progress. 

The following are some of the limitations of OEE.

- **Lack of Supply Chain Indicators** - While OEE is valuable for fine-tuning the efficiency of individual machines, it overlooks the seamless integration of the manufacturing process with supply chain systems.
- **Neglecting Human Factors** - Skilled and motivated employees have a significant impact on refining processes and improving overall productivity. OEE does not inherently include these factors.
- **Neglecting the Environment** - Sustainability is critical for manufacturers to consider the environmental impact of their operations. OEE does not take into account resource consumption, energy efficiency or waste reduction.

To effectively analyze smart manufacturing initiatives, evaluate raw material readiness, access employee skills, and drive sustainable growth, manufacturers should embrace a more comprehensive set of KPIs.

## Using OMH for Calculating OEE

The Open Manufacturing Hub (OMH) solution provides valuable overall equipment effectiveness (OEE) enhancements for manufacturing operations, including real-time monitoring and data integration for immediate insight into equipment performance and accurate OEE calculations. It incorporates predictive maintenance algorithms to prevent unexpected downtime, streamlines reporting processes, and supports continuous improvement initiatives with historical data and analysis. OMH also optimizes resource allocation and enables remote monitoring to improve overall equipment efficiency and manufacturing performance, ultimately improving OEE metrics.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/0b88fa3cf1c98545e501e3b8073fdccc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      State-of-the-Art Smart Manufacturing Tech Stack
    </div>
    <div class="promotion-pdf__desc">
      Enabling seamless connectivity, real-time data processing, and efficient system management.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-oee-in-lean-manufacturing" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Conclusion

In summary, OEE plays a critical role in lean management by providing a comprehensive assessment of manufacturing effectiveness. Its ability to provide objective insight, identify opportunities for improvement, inform decision making and support ongoing progress positions it as a cornerstone for improving the overall efficiency and success of manufacturing operations. In the next blog, we will explain why to implement the KPIs in an automated approach.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
