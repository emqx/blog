An automotive parts manufacturer uses EMQX UNS to build a **digital twin** to maximize production and process efficiency across all automotive Plating on Plastic (POP) production lines and supporting systems. They focus on three key areas: **predictive production and optimization**, **real-time resource management**, and **proactive quality control**. The digital twin functions as a continuous simulation engine, enabling data-driven decisions that directly affect the bottom line.

## The Backbone Components of a Connected Factory

In this factory, an EMQX broker serves as the central data backbone for data exchange, while multiple EMQX Neurons function as gateways for collecting industrial data. Together, these systems integrate real-time information from various POP production lines, a central dosing system, and a wastewater treatment system, creating a smart and interconnected ecosystem.

![image.png](https://assets.emqx.com/images/7805c05a9d1fa7beada8d5f77f8c06a4.png)

At the core, the EMQX Neuron connects directly to the **PLCs** of each surface finishing machine, collecting critical process data like **temperature** and **pH** from every chemical bath. At the **loading and unloading stations**, a connection to the **SCADA system** via **OPC-UA** allows operators to input a product's **batch number** and its specific **recipe parameters**. This is crucial for tracking and ensuring consistency. 

The most important feedback loop, however, comes from the **chemical laboratory**. After testing solution samples, the lab publishes the results to the UNS. This message triggers an automated response from the **central dosing system**, which receives the data and precisely adds the necessary chemicals to keep the baths "fresh." 

Finally, the UNS also monitors the **wastewater treatment system** to ensure the treated water is ready to be drained. This cohesive system enables the manufacturer to automate and optimize their process for maximum efficiency and quality.

## The Hierarchical Data Flow with Unified Namespace

Within the central EMQX broker, all messages are organized into a hierarchical structure according to the Unified Namespace (UNS) architecture. This organization provides a clear and intuitive data flow, enabling all systems to easily access the information they need. The messages fall into three primary categories: Process Data, Recipe and Batch Data, and Laboratory Data.

### Process Data

These messages are published by the **PLCs** and **SCADA** systems to provide real-time status of the production line. They are the foundation of the digital twin's operational view.

- **Chemical Bath Parameters:** Each bath has a unique identifier, and its core operational parameters are published continuously.
  - **Topic:** `Manufacturing/Line_01/Bath_<BathID>/<Parameter>`
  - **Examples:**
    - `Manufacturing/Line_01/Bath_01/Temperature`: **Value** (e.g., 65.2 °C)
    - `Manufacturing/Line_01/Bath_01/pH`: **Value** (e.g., 9.1)
    - `Manufacturing/Line_01/Bath_02/FlowRate`: **Value** (e.g., 15.0 L/min)
    - `Manufacturing/Line_01/Bath_03/Conductivity`: **Value** (e.g., 1200 µS/cm)
- **Waste Water Treatment System:** The status of the treatment process is also monitored.
  - **Topic:** `Manufacturing/Line_01/WWT_System/<Parameter>`
  - **Examples:**
    - `Manufacturing/Line_01/WWT_System/pH`: **Value** (e.g., 7.5)
    - `Manufacturing/Line_01/WWT_System/FlowRate`: **Value** (e.g., 50 L/min)
    - `Manufacturing/Line_01/WWT_System/OutletStatus`: **Value** (e.g., "Draining")
- **Central Dosing System Status:** The state of the dosing system is a critical feedback loop.
  - **Topic:** `Manufacturing/Line_01/Dosing_System/<Status>`
  - **Examples:**
    - `Manufacturing/Line_01/Dosing_System/Status`: **Value** (e.g., "Idle", "Dosing_Batch_A")
    - `Manufacturing/Line_01/Dosing_System/Pump_A/Active`: **Value** (e.g., "True")

### Recipe and Batch Data

This data, often published by the **SCADA system** at the loading/unloading stations, links specific products to their required process parameters. This provides the digital twin with essential context for each part moving through the line.

- **Loading Station Messages:**
  - **Topic:** `Manufacturing/Line_01/Loading_Station/CurrentProduct`
  - **Payload:** A JSON object containing details for the current product, sent when a new batch is loaded.
    - `batch_id`: **Value** (e.g., "PO_78451")
    - `product_id`: **Value** (e.g., "Car_Door_Handle_Chrome")
    - `recipe_id`: **Value** (e.g., "Recipe_B_Chrome")
    - `timestamp`: **Value** (e.g., "2025-09-15T10:30:00Z")
- **Recipe Parameters:** The specific recipe requirements are published and subscribed to by the various machines. This ensures each machine knows the target settings for the current batch.
  - **Topic:** `Manufacturing/Recipes/<RecipeID>/<Parameter>`
  - **Examples:**
    - `Manufacturing/Recipes/Recipe_B_Chrome/Bath_01/Target_Temperature`: **Value** (e.g., 68.0 °C)
    - `Manufacturing/Recipes/Recipe_B_Chrome/Bath_01/Target_pH`: **Value** (e.g., 9.2)

### Laboratory Data

This is where external data provides crucial feedback for the central dosing system. The lab results are manually or automatically published to the UNS.

- **Lab Test Results:**
  - **Topic:** `Lab/Solution_Analysis/<SampleID>`
  - **Payload:** A JSON object detailing the chemical analysis, which is then used to trigger dosing actions.
    - `sample_id`: **Value** (e.g., "S-4589")
    - `bath_id`: **Value** (e.g., "Bath_01")
    - `timestamp`: **Value** (e.g., "2025-09-15T11:00:00Z")
    - `chemical_concentration_A`: **Value** (e.g., 25.5 g/L)
    - `chemical_concentration_B`: **Value** (e.g., 18.2 g/L)
    - `ph`: **Value** (e.g., 8.9)
    - `recommended_additives`: **Value** (e.g., {"Additive_A": 5.0 L, "Additive_B": 1.5 kg})

### How It All Connects

When the lab publishes a message to `Lab/Solution_Analysis/S-4589`, the **central dosing system** and the **digital twin** both receive it. The dosing system, acting as a subscriber, reads the `recommended_additives` and automatically begins to dose the required chemicals into the specified bath. Simultaneously, the digital twin updates its model with the new chemical concentrations and flags that a dosing event is in progress. This closed-loop system ensures that the chemical solutions are always maintained at optimal levels for peak plating quality and efficiency.

## Model Creation for Simulating Reality

Instead of individually connecting to every system, the digital twin retrieves all its data from the central **EMQX MQTT broker**, which acts as a unified central repository. The broker stores industrial data in a hierarchical structure, complete with contextual information. Once the digital twin has this organized data, it can easily build the virtual model.

- **3D Modeling:** Create a precise 3D model of the POP line, including the automated gantry system, multiple chemical baths, rinses, and drying stages. This provides a clear, visual representation.
- **Physics-Based Models:** Develop mathematical models that simulate the complex chemical and electrochemical reactions occurring at each stage. This includes models for the etching process, catalyst deposition, and the final chrome plating, all of which are critical for proper adhesion and a uniform finish.
- **Behavioral Models:** Program the twin with the operational logic of the physical system. This includes how the gantry moves parts between tanks, how pumps and filters are controlled, and how setpoints are maintained.

## Analytical Simulation for Unlocking Insights

### Predictive Optimization for Maximum Throughput

By simulating the entire production cycle, the twin can identify the optimal settings for a given product or batch.

- **Bottleneck Analysis**: The twin analyzes real-time and historical data to pinpoint the slowest stages in the POP line. For example, it might identify that a specific curing oven is the limiting factor, or that parts are spending too much time in a particular rinse tank. The manufacturer can then use the twin's simulation capabilities to test solutions, such as adjusting the conveyor speed or changing the temperature profile, to alleviate the bottleneck without compromising quality.
- **Optimal Recipe Management**: For each type of plastic or part geometry, the twin can determine the ideal "recipe" of process parameters. This includes the precise dwell time in each chemical bath, the optimal current density for electroplating, and the exact temperatures for drying. The manufacturer can then use this optimized recipe to maximize throughput while ensuring consistent quality for every part.
- **Predictive Scheduling**: The twin can forecast how changes in production orders will affect the line's efficiency. For example, if a new, high-volume order is received, the twin can simulate the impact on resource consumption (chemicals, energy) and throughput, allowing the manufacturer to prepare and adjust schedules to meet demand without overstressing the system.

### Real-Time Resource Management

One of the biggest costs in a POP line is the consumption of chemicals and energy. The digital twin provides real-time oversight and optimization of these resources.

- **Chemical Consumption**: The twin models the chemical reactions in each tank and monitors concentration levels in real-time. It can then predict the optimal time to replenish chemicals, rather than relying on a fixed schedule. This minimizes waste and ensures the baths are always operating at peak efficiency, which is crucial for a consistent plating finish.
- **Energy Efficiency**: The twin tracks energy consumption from power rectifiers, heaters, and pumps. By correlating energy usage with production data, it can identify opportunities for reduction. For instance, it can recommend adjusting the temperature setpoint in a drying oven during idle periods or optimizing the current flow to the plating baths to reduce energy consumption without affecting part quality.
- **Water Management**: The twin can monitor water usage in rinse stages and suggest adjustments to flow rates based on the number and type of parts being processed. This reduces water consumption and associated treatment costs.

### Proactive Quality Control

The digital twin helps this manufacturer move from post-production quality checks to in-process quality assurance.

- **Parameter Drift Detection**: By analyzing real-time data from a network of sensors, the twin can detect subtle deviations in process parameters before they cause a noticeable defect. For example, a slight increase in the acidity of a bath might be an early warning sign of a future adhesion issue. The twin can alert operators to these "pre-failure" conditions, allowing for proactive correction.
- **Root Cause Analysis**: If a batch of parts fails a quality test, the twin can use its historical data to perform a rapid root cause analysis. It can trace the exact conditions of the line at the time the parts were processed, pinpointing the specific parameter that caused the issue, whether it was an out-of-spec chemical bath, a drop in current, or a temperature fluctuation. This eliminates guesswork and significantly reduces troubleshooting time.
- **Simulation for Quality Improvement**: A manufacturer can use the twin to simulate the impact of new chemical additives or process improvements on the final product quality. They can virtually test how a new additive affects the surface finish or adhesion before making a physical change to the production line, saving time and money.

## The Impact on Automotive Manufacturing

For this manufacturer focused on Plating on Plastic, a digital twin provides a powerful competitive advantage:

- **Unparalleled Quality Control:** The ability to predict and prevent defects leads to a significant reduction in rejected parts, meeting the automotive industry's stringent quality standards.
- **Increased Throughput:** By optimizing process parameters virtually, the manufacturer can increase the number of parts produced per shift while maintaining quality.
- **Cost Reduction:** The twin helps in optimizing chemical usage, reducing energy consumption, and minimizing scrap, directly impacting the bottom line.
- **Resilience and Agility:** The ability to simulate new product introductions or respond to supply chain changes virtually makes the production line more agile and resilient.

The digital twin, powered by [EMQX Neuron](https://www.emqx.com/en/products/emqx-neuron) gateways collecting data from the factory floor and the central **EMQX broker** organizing it all in a Unified Namespace, is transforming the POP process from a complex art to a precise science. This robust data foundation ensures that every automotive part rolls off the line with a perfect, high-quality finish. It’s not just about replicating the process; it’s about mastering it.





<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
