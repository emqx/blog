## Introduction: The "Last Mile" Challenge of Edge AI

As Generative AI (GenAI) sweeps the globe, the industrial sector is experiencing a rational return. While large models have demonstrated impressive potential in knowledge management and decision support, on the production floor where machines roar and milliseconds determine equipment fate, **"Small/Specialized Learning Models (SLM)"** remain the irreplaceable special forces.

However, AI deployment faces three critical gaps:

- **Technical Gap**: How to deploy cloud-trained models to edge devices?
- **Skills Gap**: How can OT engineers understand and maintain data scientists' Python code?
- **Deployment Gap**: How to rapidly replicate lab POCs to thousands of production sites?

This article demonstrates how EMQX Neuron bridges these three gaps through **SQL feature engineering + flexible algorithm integration**, providing an end-to-end solution from data acquisition to edge inference.

## 1. Why Small Models + Edge Inference?

### 1.1 Limitations of GenAI

| Dimension             | GenAI (Large Models)  | Small Models                | Industrial Requirements                            |
| :-------------------- | :-------------------- | :-------------------------- | :------------------------------------------------- |
| **Inference Latency** | 2-5 seconds           | < 100ms                     | < 100ms (closed-loop control)                      |
| **Cost**              | $0.01-$0.10/inference | Edge hardware $500-$1,500   | Controllable one-time investment                   |
| **Determinism**       | "Hallucination" risk  | Highly deterministic        | Safety-critical scenarios cannot accept randomness |
| **Explainability**    | Black box             | Decision tree visualization | Must pass safety certification                     |

Industrial edge scenarios require **lightweight, low-latency, highly explainable** small models, not general-purpose large models.

### 1.2 The "SQL Feature Engineering + Machine Learning" Combo

Traditional end-to-end deep learning faces challenges in industrial scenarios:

- **Data Requirements**: Requires millions of samples, but industrial scenarios typically have only thousands of fault samples
- **Compute Requirements**: Requires GPU, but edge devices typically only have CPU
- **Explainability**: Black-box models are difficult to certify for safety

**The most elegant industrial AI architecture is layered processing**:

1. **Feature Extraction Layer** (Signal Processing): Use SQL stream computing to "reduce dimensions" of raw waveforms into physical features (RMS, crest factor, kurtosis, etc.)
2. **Decision Layer** (Pattern Recognition): Use machine learning models (XGBoost/Random Forest) to judge fault patterns based on these features

**EMQX Neuron's Core Value**: In a 200MB-class edge gateway software, it perfectly supports both layers simultaneously.

## 2. EMQX Neuron's Algorithm Integration Capabilities

### 2.1 Four Algorithm Integration Methods

EMQX Neuron provides flexible algorithm integration methods, covering all scenarios from simple to complex:

| Integration Method             | Use Cases                                              | Development Difficulty   | Deployment Speed               |
| :----------------------------- | :----------------------------------------------------- | :----------------------- | :----------------------------- |
| **ONNX Plugin**                | Standard ML models (XGBoost, TensorFlow Lite)          | ⭐ Low                    | ⭐⭐⭐ Fast (upload and use)      |
| **Python Portable Plugin**     | Custom algorithms, complex business logic              | ⭐⭐⭐ High                 | ⭐⭐ Medium (requires packaging) |
| **External HTTP Service**      | Existing algorithm services, microservice architecture | ⭐⭐ Medium                | ⭐⭐⭐ Fast (configure and use)   |
| **AI-Generated Python Plugin** | Rapid prototyping, simple logic                        | ⭐ Low (natural language) | ⭐⭐⭐ Fast (auto-generated)      |

### 2.2 Quick Start Path

**Level 1: ONNX Plugin** (5 minutes)

- Upload pre-trained ONNX model → Call directly in SQL

For details, refer to: [ONNX Plugin | EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/streaming-processing/onnx.html) 

**Level 2: External HTTP Service** (10 minutes)

- Start Flask/FastAPI service → Configure service address → Call in SQL

For details, refer to: [External algorithm function example | EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/streaming-processing/ex_func.html) 

**Level 3: AI-Generated Python Plugin** (15 minutes)

- Describe requirements in natural language → LLM auto-generates code → One-click deployment

For details, refer to: [AI-generated Python Plugin Guide | EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/best-practise/llm-portable-plugin.html) 

**Level 4: Python Portable Plugin** (1 hour)

- Write Python function → Package as ZIP → Upload and deploy

For details, refer to: [Python portable plugin example | EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/streaming-processing/portable_python.html) 

## 3. Scenario 1: Device Health Analysis (Predictive Maintenance)

### 3.1 Scenario Definition

- **Use Case**: Predict equipment failures 2-4 weeks in advance for proactive maintenance
- **Data Flow**: Sensors (temperature, pressure, vibration, current) → SQL feature engineering → XGBoost model → Health score
- **Core Challenges**: High-frequency data (1-second sampling), multi-variable (20+ sensors), long time windows

### 3.2 Edge Feature Engineering: Why Compute at the Edge?

**The Power of Dimensionality Reduction**:

- Raw data: 86,400 readings/day/sensor
- Feature data: 1,440 feature vectors/day (one per minute)
- **98% data volume reduction**, 98% cloud transmission cost reduction

**EMQX Neuron SQL in Action**:

```sql
-- Real-time statistical feature calculation (60-second window)
SELECT
  asset_id,
  avg(vibration) as rms_vibration,                    -- RMS value
  max(vibration) / avg(vibration) as crest_factor,    -- Crest factor
  stddev(current) as current_fluctuation,             -- Current fluctuation
  percentile(temperature, 95) as temp_p95,            -- Temperature 95th percentile
  max(pressure) as pressure_max                       -- Maximum pressure
FROM sensor_stream
GROUP BY asset_id, TumblingWindow(ss, 60)
```

**Feature Engineering Best Practices**:

- **Time-domain features**: Mean, standard deviation, peak, kurtosis
- **Frequency-domain features**: FFT (Fast Fourier Transform) to extract dominant frequencies
- **Window selection**: Choose from 10 seconds to 10 minutes based on equipment characteristics

### 3.3 Model Training (Offline)

Use feature data exported from EMQX Neuron (cleaned and standardized) to train an XGBoost model in the cloud or locally, then export to ONNX format for edge deployment.

```sql
# Training script (simplified)
import xgboost as xgb
from skl2onnx import convert_sklearn

# Train model
model = xgb.XGBClassifier(max_depth=5, n_estimators=100)
model.fit(X_train, y_train)

# Export to ONNX format
onnx_model = convert_sklearn(model, initial_types=[...])
with open("xgboost_health.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

### 3.4 Edge Deployment: Python Portable Plugin Method

**Why Choose Python Plugin?**

- Need custom preprocessing logic (e.g., outlier filtering)
- Need to maintain device state (e.g., alert only after 3 consecutive low health scores)
- Need complex post-processing (e.g., calculate Remaining Useful Life - RUL)

**Python Plugin Implementation**:

```sql
# health_predict.py
from ekuiper import Function, Context
import onnxruntime as ort
import numpy as np

class HealthPredict(Function):
    def __init__(self):
        # Load ONNX model
        self.session = ort.InferenceSession("/path/to/xgboost_health.onnx")
        self.alert_count = {}  # Maintain alert count state

    def exec(self, args, ctx):
        # args: [asset_id, rms_vibration, crest_factor, current_fluctuation, ...]
        asset_id = args[0]
        features = np.array(args[1:]).reshape(1, -1).astype(np.float32)

        # ONNX inference
        result = self.session.run(None, {"input": features})
        health_score = float(result[0][0])

        # State maintenance: Alert only after 3 consecutive low health scores
        if health_score < 20:
            self.alert_count[asset_id] = self.alert_count.get(asset_id, 0) + 1
            if self.alert_count[asset_id] >= 3:
                return {"asset_id": asset_id, "health_score": health_score,
                        "alert": "critical", "action": "reduce_speed"}
        else:
            self.alert_count[asset_id] = 0

        return {"asset_id": asset_id, "health_score": health_score, "alert": "normal"}

health_predict = HealthPredict()
```

**Call in SQL**:

```sql
-- Call Python plugin for health scoring
SELECT
  health_predict(asset_id, rms_vibration, crest_factor,
                 current_fluctuation, temp_p95, pressure_max) as result
FROM feature_stream
```

### 3.5 Closed-Loop Control: Automatic Speed Reduction Protection

When health score < 20 and alerts occur 3 consecutive times, EMQX Neuron automatically writes to PLC registers, reducing equipment speed to 70% to prevent fault escalation.

**Action Configuration**:

- **Sink Type**: Neuron Sink (write to PLC)
- **Target Register**: `Modbus_40001` (equipment speed control)
- **Write Value**: `0.7` (reduce to 70% speed)
- **Total Latency**: < 50ms (edge inference + PLC write)

**Business Value**:

- **60% downtime reduction**: From 200 hours/year → 80 hours/year
- **40% maintenance cost reduction**: From $500K/year → $300K/year
- **85% cloud cost reduction**: From $5K/month → $750/month

## 4. Scenario 2: Image Quality Inspection (Real-Time Defect Detection)

### 4.1 Scenario Definition

- **Use Case**: PCB defect detection (scratches, cracks, contamination)
- **Production Speed**: 600 units/minute (100ms cycle)
- **Data Flow**: Industrial camera → Image preprocessing → TensorFlow Lite inference → Defect judgment
- **Core Challenges**: High throughput, low latency (< 100ms), high accuracy (> 95%)

### 4.2 Triggered Image Acquisition

**PLC Signal Trigger** (not continuous streaming):

- EMQX Neuron reads PLC registers (Modbus TCP, 10ms polling)
- Product arrives at inspection station → Trigger industrial camera
- **90% bandwidth savings**: Only capture when product is present

### 4.3 Edge Image Preprocessing

```sql
-- Image preprocessing (implemented via Python plugin in EMQX Neuron)
SELECT
  product_id,
  image_preprocess(raw_image) as processed_image
FROM camera_stream
```

**Preprocessing Steps**:

- Size adjustment: 1920×1080 → 640×480 (model input size)
- Normalization: Pixel values 0-255 → 0-1
- Contrast enhancement: Adaptive histogram equalization

### 4.4 Model Training (Offline)

Train the MobileNetV3 model using 50,000 labeled images (including 10,000 defect samples), export it to TensorFlow Lite format, and then convert it to ONNX format for edge deployment.

### 4.5 Edge Deployment: ONNX Plugin Method

**Why Choose ONNX Plugin?**

- Standardized model format, no code required
- Upload and use, fast deployment
- Inference performance optimization (ONNX Runtime)

**Deployment Steps**:

1. **Upload Model File**:
   - In EMQX Neuron Dashboard: Data Processing → Configuration → File Management
   - Upload `mobilenetv3_defect.onnx` (8 MB)
2. **Call in SQL**:

```sql
-- Call ONNX model for defect detection
SELECT
  product_id,
  onnx("mobilenetv3_defect", processed_image) as defect_result
FROM preprocessed_stream
```

**Output Format**:

```
{
  "product_id": "PCB_20260121_103045",
  "defect_result": [[0.05, 0.92, 0.03]]  // [normal, scratch, crack]
}
```

### 4.6 Closed-Loop Control: Automatic Rejection

**Judgment Logic**:

```sql
-- Defect judgment and automatic rejection
SELECT
  product_id,
  defect_result[1] as scratch_prob,
  defect_result[2] as crack_prob,
  CASE
    WHEN defect_result[1] > 0.9 OR defect_result[2] > 0.9 THEN 1
    ELSE 0
  END as reject_flag
FROM detection_stream
```

**Action Configuration**:

- **Sink Type**: Neuron Sink (write to PLC)
- **Target Register**: `Modbus_40002` (pneumatic arm control)
- **Write Value**: `1` (trigger rejection)
- **Total Response Time**: < 100ms (capture + preprocessing + inference + PLC write)

**Business Value**:

- **96% detection accuracy** (vs manual 85%, cloud 92%)
- **< 1% miss rate** (vs cloud 8%, due to latency)
- **99% cost savings**: Edge hardware $1,500 (one-time) vs cloud API $26K/month

## 5. Why Choose EMQX Neuron over Others?

### 5.1 Core Differentiators

**1. Only Platform Supporting 4 Algorithm Integration Methods**

- ONNX plugin, Python plugin, external service, AI-generated
- Covers all scenarios from simple to complex

**2. Only Platform Supporting LLM-Assisted Development**

- Natural language generates Python code
- Lower development barrier for OT engineers
- Development time reduced from 2 weeks to 2 hours

**3. Only Platform Supporting "SQL Feature Engineering + Native AI Inference"**

- End-to-end edge intelligence
- 98% data reduction, 85-99% cloud cost reduction

**4. No Cloud Platform Lock-in**

- Supports private deployment
- Low-cost hardware

### 5.2 Competitive Comparison

| Capability                  | Traditional Edge Gateway | Cloud Platform Edge Solution           | **EMQX Neuron**                  |
| :-------------------------- | :----------------------- | :------------------------------------- | :------------------------------- |
| **Edge AI Inference**       | ❌ Not supported          | ⚠️ Requires dedicated hardware          | ✅ ONNX/TFLite native support     |
| **SQL Feature Engineering** | ❌ Not supported          | ⚠️ Limited support                      | ✅ Complete SQL stream processing |
| **AI-Generated Plugin**     | ❌ Not supported          | ❌ Not supported                        | ✅ LLM-assisted development       |
| **Inference Latency**       | N/A                      | 200ms                                  | **< 100ms**                      |
| **Development Barrier**     | N/A                      | High (requires cloud platform experts) | **Low (natural language)**       |
| **Cloud Platform Lock-in**  | N/A                      | High                                   | **No lock-in**                   |

### 5.3 Business Value

**1. Rapid Engineering Deployment**

- Traditional approach: 2 months development + 2 weeks deployment
- EMQX Neuron approach: 1 day configuration + 1 hour deployment
- **20-40x acceleration**

**2. Reduced Computing Costs**

- Raspberry Pi ($200) can run predictive maintenance logic
- No GPU required (vs deep learning requiring $3,000+ GPU)
- **90% hardware cost savings**

**3. Mitigate Black-Box Risks**

- SQL + XGBoost explainability
- Feature importance analysis
- Complies with industrial safety certification (IEC 61508)

## Conclusion: From Theory to Practice

The future of industrial intelligence lies in the transition from "Cloud AI" to Real-time Edge Action. By combining SQL-based feature engineering with specialized small models, manufacturers can finally overcome the latency and cost barriers of the "Last Mile."

EMQX Neuron serves as the definitive bridge for this transformation. Its ability to unify data acquisition, stream processing, and multi-method AI inference into a single 200MB-class tool allows OT teams to deploy production-ready intelligence in hours rather than months. Ultimately, Neuron doesn't just connect machines; it empowers them to think and act at the edge, turning raw data into immediate industrial value.

Ready to bridge your AI deployment gap? [Download EMQX Neuron](https://www.emqx.com/en/products/neuronex) today and start building your first edge inference pipeline in minutes.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
