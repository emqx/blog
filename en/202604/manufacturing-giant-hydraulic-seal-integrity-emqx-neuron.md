## Introduction: The Silent Killer in Hydraulic Systems

In heavy manufacturing, the **Hydraulic Press** is the heartbeat of production. We recently partnered with a **Tier-1 Automotive Supplier** facing a silent, costly issue: **Internal Cylinder Bypass**. Unlike visible leaks, internal seal failures cause inconsistent compression and hidden defects. To detect them, one must capture the millisecond-level pressure decay during the "holding" phase, a feat impossible for legacy SCADA systems polling once per second.

This blog creates a deep dive into how this customer utilized **EMQX** **Neuron** to implement **Edge-Native Cycle Analysis**. By shifting from reactive repairs to algorithmic pressure curve analysis, they solved the "data deluge" and integrated predictive maintenance seamlessly into a Unified Namespace (UNS).

## The Physics of Failure & The Transient Data Trap

To understand the solution, we must first appreciate the physics of a hydraulic press cycle and why standard industrial monitoring strategies fail to catch seal issues.

![image.png](https://assets.emqx.com/images/070445ba6d9a96f893fa517c2ba379e1.png){.mx-auto .block}

[The Invisible Defect: Oil bypasses the piston, compromising pressure integrity.]{.block .text-center}

### The Anatomy of a Press Cycle

A typical hydraulic press cycle consists of distinct phases, each generating a unique pressure signature:

1. **Rapid Advance:** Low pressure, high flow velocity.
2. **Compression:** Pressure builds rapidly as the tool contacts the material.
3. **Holding (Dwell):** The critical phase. The valves close, and the system attempts to maintain target pressure (e.g., 250 bar) for 3-10 seconds to form the part.
4. **Decompression & Retract:** Pressure release and return.

**The Failure Mode:** In a healthy system, the pressure during the "Holding" phase is a flat line (or a very slow, predictable thermal decay). In a system with a damaged piston seal, the oil bypasses the piston, causing the pressure to drop non-linearly.

**The Diagnostic Requirement:** To differentiate between "Thermal Decay" (Normal) and "Leak Decay" (Failure), the engineering team needed to calculate the **Slope of the Curve**.

**The Sampling Floor:** A single data point every second (1Hz) was too slow to calculate a reliable slope over a 3-second hold. They needed a minimum of **10Hz (100ms)** resolution.

### The Cloud Bottleneck: The Cost of Noise

The customer initially attempted a "Lift and Shift" strategy: pushing all 100ms data directly to the cloud for analysis.

#### The Data Volume Calculation

- **Fleet Size:** 200 Presses.
- **Tags per Press:** 4 (Pressure, Temp, Position, State).
- **Frequency:** 10 Hz (10 messages/sec).
- **Total Throughput:** 200×4×10=8,000 data points/second.
- **Daily Volume:** ~690 Million data points/day.

#### The Efficiency Ratio

The "Holding" phase only accounts for roughly **15%** of the total cycle time.

- **The Problem:** 85% of the data being streamed (during Idle, Advance, Retract) was completely irrelevant to seal health.
- **The Impact:** The customer was paying to ingest, process, and store hundreds of terabytes of "waste" data just to find the few gigabytes of "signal."

## The Solution Architecture: "Cycle-Aware" Edge Computing

The customer revolutionized their architecture by deploying **EMQX** **Neuron**, not just as a gateway, but as an intelligent **Edge Computing Node**.

### The Ingestion Layer: High-Stability Polling

The customer deployed EMQX Neuron on Industrial PCs (IPCs) connected to the press PLCs via Modbus TCP and, for critical older machines, directly to analog I/O modules.

- **Protocol Driver:** Modbus TCP.
- **Polling Strategy:** EMQX Neuron was configured with a 100ms polling interval.
- **The "Group" Concept:** Critical tags (Pressure, State) were grouped into a high-priority polling bucket to ensure time-deterministic data acquisition, separated from low-priority tags (like Oil Temperature) which were polled every 5 seconds.
- **State Detection:** EMQX Neuron monitored the PLC’s "Cycle State" register. It didn't just record data; it watched for the "Start of Cycle" and "End of Holding" boolean tags.

### The "Smart Window" Strategy

The core innovation was moving the logic to the edge. EMQX Neuron used its internal streaming engine to filter data based on machine state *before* it ever left the factory.

Data Flow Logic is as follows:

1. **Ingest:** Read Pressure (P) and Machine State (S) every 100ms.
2. **Buffer:** Hold the incoming stream in a temporary memory buffer.
3. **Trigger:** Watch the `$S` tag.
   - `IF S == "HOLDING"`: Start aggregating data.
   - `IF S != "HOLDING"`: Discard data (or downsample to 10Hz for basic trending).
4. **Process:** When the state changes from "HOLDING" to "RETRACT," execute the analysis on the buffered "Holding" data.

### Visualizing the Architecture

- **Southbound:**
  - **Input A:** Pressure Transducer (0-400 Bar) @ 10ms polling.
  - **Input B:** PLC State Tags (Idle/Press/Hold/Retract).
- **Edge Logic:**
  - Isolate the "Hold" window.
  - Calculate the **Slope (Derivative)** of the pressure curve.
- **Northbound:** Publish the *Diagnostic Result* to the UNS.

## The Mathematical Core: Derivative Analysis & Reference Curves

This section details the specific logic implemented inside EMQX Neuron to turn raw data into actionable insights.

### The Concept: Session Windowing

Standard "Tumbling Windows" (e.g., every 5 seconds) don't work well here because a press cycle varies in length. EMQX Neuron utilized **Session Windows**.

- **Definition:** A session window groups data based on a specific condition (Session Activity) rather than clock time.
- **The Setup:** The "Session" is defined as long as `PLC_State = HOLDING`.

### The Algorithm: Calculating Decay Rate (dP/dt)

The customer didn't just want to know the *pressure*; they wanted to know the *rate of change*.

![image.png](https://assets.emqx.com/images/0a4f8651cdd2cb07896f79b29000e9bf.png){.mx-auto .block}

**The Formula:**

![image.png](https://assets.emqx.com/images/6d917c63a83044fa152756fe1cb66d7b.png)

- If DecayRate<−0.5 bar/sec, it indicates a **Minor Leak**.
- If DecayRate<−2.0 bar/sec, it indicates a **Critical Seal Failure**.

### The EMQX Neuron Implementation

The customer utilized EMQX Neuron's windowing functions to perform this calculation efficiently.

#### The SQL Rule Structure

The following logic was deployed to the edge nodes:

- **Step 1:** Create a window defined by the `Hold_Active = True` signal.
- **Step 2:** Collect all pressure samples within that window.
- **Step 3:** Apply a custom function to calculate the linearity.

**Conceptual Code Snippet:**

```sql
SELECT 
  press_id, 
  cycle_id, 
  collect(pressure)[0] AS start_p, 
  collect(pressure)[-1] AS end_p, 
  (collect(pressure)[-1] - collect(pressure)[0]) / ((window_end() 
  - window_start()) / 1000.0) 
  AS decay_rate 
FROM PressureStream 
WHERE state = "HOLDING" 
GROUP BY SessionWindow(ms, 1000, 0)
HAVING (collect(pressure)[-1] - collect(pressure)[0]) / ((window_end() 
- window_start()) / 1000.0) < -0.5

```

### Advanced Feature: The "Golden Cycle" Comparison

For their most critical presses, the customer went a step further. They loaded a "Golden Cycle" (a reference array of data points representing a perfect press cycle) into the EMQX Neuron local memory.

- **Correlation Analysis:** For every cycle, EMQX Neuron compared the live curve against the Golden Cycle using a standard deviation algorithm.
- **Anomaly Detection:** If the live curve deviated by more than 3% from the Golden Cycle at any point during the hold, an "Integrity Warning" was generated.
- **Outcome:** This detected not just leaks, but also **valve flutter** and **pump cavitation**—issues that simple threshold monitoring would never catch.

## Integration with Unified Namespace

The success of the project relied on making this granular edge data accessible to the rest of the enterprise without flooding the network. This was achieved through a **Unified Namespace** architecture.

### Defining the Topic Structure for Cycle Data

Unlike continuous streaming, "Cycle Data" is discrete. The customer organized their MQTT topics to reflect the production hierarchy.

**Topic Structure:** `Enterprise/Site/Area/Line/Cell/Asset/Function`

**Specific Implementations:**

- **The "Heartbeat" (10Hz):** `.../Press01/Status`
  - Payload: `{ "state": "Running", "current_job": "Hood_Panel" }`
- **The "Cycle Report" (Event-Driven):** `.../Press01/Cycle/Data`
  - Payload: Published *only* at the end of a cycle. Contains the analysis of the seal integrity.

### The Semantic Payload Strategy

EMQX Neuron enriched the payload with context. It wasn't just "Pressure dropped"; it was "Pressure dropped while making Part X."

**The JSON Payload:**

```json
{
  "meta": {
    "timestamp": 1715624000,
    "asset_id": "Press-05",
    "job_context": {
      "batch_id": "B-99-AF",
      "product_code": "Chassis_Rail_Left"
    }
  },
  "diagnostics": {
    "cycle_result": "WARNING",
    "physics": {
      "hold_duration_sec": 5.2,
      "pressure_start_bar": 250.5,
      "pressure_end_bar": 247.1,
      "decay_slope": -0.65
    }
  }
}
```

### Architecture Bridging OT and IT

To fully document this setup, the architecture diagram must include:

![image.png](https://assets.emqx.com/images/a611941ea85ba48e031cab9dbc40e17f.png){.mx-auto .block}

[Full Stack: From 4-20mA sensor to JS0N report.]{.block .text-center}

- **The Physical Layer:** Hydraulic cylinders and Pressure Transducers (4-20mA).
- **The Edge Layer:** EMQX Neuron node converting Analog signals to Digital Streams.
- **The Context Layer:** EMQX Neuron pulling "Job ID" from the PLC to enrich the payload.
- **The Broker:** EMQX Enterprise managing the UNS topics.
- **The Consumer Layer:**
  - **MES:** Records the "Pass/Fail" for the specific Serial Number.
  - **Maintenance App:** Subscribes to `.../Cycle/Data` where `seal_integrity_status != PASS`.

## Business Impact & ROI Analysis

The transition to "Edge-Calculated" metrics transformed the customer's operations from reactive to proactive.

### Efficiency: The Data Reduction Victory

- **Before:** Streaming 8,000 points/sec across the fleet.
- **After:** Streaming ~120 JSON reports/minute.
- **The Metric:** A **78.5% reduction** in cloud ingress traffic and storage load. The customer saved an estimated **$20,000 annually** in cloud costs alone.

### Quality: Zero-Defect Manufacturing

The 100ms resolution, processed locally, provided the fidelity needed to catch "Micro-Leaks."

- **Scrap Reduction:** The system now flags presses with "Warning" status (0.5 bar drop) weeks before they produce a defective part. Scrap rates related to compression issues fell by **45%**.
- **The "Golden Cycle":** The customer can now overlay the pressure curve of every single part produced against a "Master Reference," ensuring 100% automated Quality Assurance.

### Maintenance: From "Calendar" to "Condition"

Maintenance teams no longer replace seals "every 6 months" regardless of condition.

- **Life Extension:** Healthy seals are left in service longer, reducing OpEx by 15%.
- **Targeted Repair:** Maintenance planning is now driven by a "Top 10 Leakers" dashboard, prioritizing assets that actually need attention during weekend shutdowns.

## Conclusion

This customer case study proves that you do not need ultra-high-frequency vibration data (10kHz) to realize the power of Edge AI. Even with standard 100ms polling, the sheer volume of data generated by a large fleet can overwhelm cloud architectures.

By leveraging **EMQX** **Neuron** to implement **Session Windowing** and **Slope Analysis** at the edge, the customer achieved the perfect balance: sufficient resolution to detect physical faults, with the bandwidth efficiency required for enterprise scale.

They moved the math to the data, and in doing so, they stopped the leaks, both in their hydraulic cylinders and in their budget.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
