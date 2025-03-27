In the current wave of AI advancements, rapid progress in AI technology has significantly transformed both production and daily life. From the initial text-based large language models to multimodal models supporting voice, image, and video interactions, AI has deeply integrated with traditional internet applications and productivity tools, dramatically improving user experience and productivity. However, in the consumer electronics field, while AI has achieved some progress, its large-scale application remains underdeveloped compared to other sectors.

As a leading MQTT platform, EMQX is widely used in IoT access scenarios for consumer electronics. This article explores how EMQX bridges the physical world and AI technologies, enabling innovative and user-friendly experiences.

## Advantages of Large AI Models in Consumer Electronics

Before the rise of large AI models, consumer electronics relied on traditional rule-based or intent-recognition systems. These methods required extensive manual work, including data annotation and rule coding, making them costly and less capable of handling complex scenarios.

With large AI models, devices now benefit from superior natural language understanding, multimodal data processing, and contextual awareness. Key advantages include:

- **Enhanced Natural Language Processing**: Users no longer need to memorize rigid commands; devices can interpret text, voice, and image inputs, delivering smoother, more intuitive interactions.
- **Contextual Adaptability**: Devices can recognize user habits and environmental contexts, offering personalized, intelligent responses.
- **Cost-Effective Customization**: Businesses can fine-tune large models to develop domain-specific AI solutions, improving adaptability and performance at lower costs.

## Integrating AI into IoT Architectures with EMQX

In consumer electronics, IoT connectivity typically follows two patterns:

- **Direct Cloud Connection**: Devices with Wi-Fi or 5G modules connect directly to cloud platforms. This method is common for appliances like smart TVs, refrigerators, and security cameras, which have access to continuous power.
- **Gateway-Based Connection**: Low-power devices, such as smart locks or sensors, connect to the cloud through gateways using protocols like ZigBee or Bluetooth, optimizing energy efficiency for battery-operated devices.

![image.png](https://assets.emqx.com/images/87c6bc4d8910d7458c5009501a7e14a1.png)

EMQX acts as a bridge between the physical and AI worlds, transmitting user interaction requests and sensor telemetry data from consumer electronics to the cloud. In this architecture, AI can be integrated at three levels:

1. **Lightweight AI on MCU**
   Devices equipped with microcontrollers (MCUs) can handle simple AI tasks locally, such as:
   - **Voice Recognition**: Convert speech signals into specific device commands or limited speech-to-text tasks.
   - **Action Recognition**: Use neural networks like YOLO to recognize specific scenarios captured by cameras and convert them into actions or commands.
2. **Small AI Models at the Edge Gateway**
   Edge gateways, equipped with more computing power, can:
   - **Process Multimodal Data**: Use models like Phi-3.5-vision to integrate and analyze text, voice, image, and video data for precise recognition.
   - **Support Offline Mode**: Ensure critical tasks continue during network outages.
3. **Large AI Models in the Cloud**
   Cloud-based models leverage powerful computational resources to perform deep multimodal data processing and handle complex tasks. They enable devices to interpret human intent and execute sophisticated operations by integrating diverse data streams.

In all these scenarios, EMQX ensures that data—whether raw or processed—is transmitted to the cloud using the MQTT protocol. This allows seamless integration between physical devices and AI, delivering fast and intelligent responses to complex user requests while enhancing overall system efficiency.

## AI-Driven Innovations in Consumer Electronics

AI technologies are unlocking unprecedented opportunities for consumer electronics, enabling them to evolve from basic smart devices into truly intelligent companions. By leveraging contextual awareness, multimodal interaction, and advanced automation capabilities, AI redefines how users engage with their devices. Below are three key scenarios that illustrate this transformation:

### **Smart Interaction with Contextual Understanding**

For example, current air conditioners can handle basic operations like turning on and setting modes via voice commands. However, users often need to perform multiple interactions to achieve optimal comfort.

With AI, models can automatically adjust air conditioners based on real-time temperature, humidity, and user habits, achieving the desired environment with a single command. This highlights the essence of smart interaction—deeply understanding and addressing user needs, not just mapping commands to device actions.

### **Scenario Exploration and Function Promotion**

AI can identify patterns in user behavior, enabling seamless collaboration between devices. For instance, after a washing machine completes its cycle, a smart drying rack can lower automatically for laundry. AI identifies such habits and suggests setting one-click automation rules, reducing user effort and enhancing product stickiness.

Through ongoing exploration of application scenarios, companies strive to uncover AI-enabled interaction possibilities that align with user needs. Leveraging data analysis and AI capabilities, these scenarios are refined to provide innovative solutions for consumers.

In parallel, companies promote these features by emphasizing their practical benefits and unique selling points, ensuring broader adoption among users. This dual approach of scenario exploration and feature promotion maximizes the value of AI in consumer electronics and enhances user engagement.

### **Multimodal Data-Driven Innovation**

With multimodal AI, new interaction forms are emerging. For instance:

- A smart fridge can recognize stored items via built-in cameras, alert users about freshness, and share data with recipe apps.
- In the future, this data could be shared with home robots. If a user requests a drink, the robot can check the fridge’s inventory before acting.

By combining sensor data, natural language understanding, and intelligent rules, consumer electronics companies can unlock rich, personalized interactions, driving the evolution of smart ecosystems.

## Demo: Smart Interaction Practice Using EMQX + AI

This section will present a demo showcasing the integration of EMQX and AI large language models to enable intelligent and efficient real-time interactions between devices and users. The solution leverages the EMQX MQTT platform for consumer electronics and an AI-integrated architecture.

### Technology Stack

- **Device Layer:** Use MQTTX or MQTTX CLI to simulate devices sending messages. Refer to the demo instructions and scenarios below for details.
- **MQTT Access Platform:** EMQX
- **AI Large Model:** GPT-4o model provided by Azure AI
- **Agent Layer:** Developed in Node.js

### Architecture Overview

EMQX acts as the access layer, connecting device and edge gateway data to the cloud while integrating with the Agent layer. The Agent uses preset prompts and the data received from EMQX to call the cloud-based AI model for data recognition and processing, returning final operation commands.

The data flow in this architecture follows these steps:

1. Consumer electronics send data to the edge AI gateway or directly to EMQX via MQTT.
2. The edge layer performs preliminary processing and data cleansing, forwarding messages to EMQX.
3. The Agent receives MQTT messages and forwards requests requiring AI processing to Azure AI via HTTP.
4. Azure AI processes the data and returns standardized commands, which are then delivered to specific devices through MQTT by EMQX.

### AI Interaction Rules Design

The AI interaction rules define how the cloud model responds to device events and operational requests, determining the overall interaction outcomes. The process follows these steps:

```
Input: Natural language/multi-modal data/environmental indicators
↓
Processing: Device operation planning (considering contextual constraints)
↓
Output: Standardized operation commands
```

This process can be understood as a reverse engineering of natural language and human actions into actionable commands comprehensible to devices.

For this demo, meticulously designed prompts guide the AI model to generate precise control commands. In real-world applications, data inputs can come from multimodal sources or pre-configured inputs. Beyond prompts, other methods can also orchestrate interaction rules.

**Example Prompts for Smart Home Scenarios**

This prompt describes a smart home control scenario where users can control devices like voice assistants, lighting, and home robots using natural language. Devices can interact based on predefined linkage rules for enhanced automation.

Users can issue commands such as "Turn on the air conditioner." The system will parse the command, generate the corresponding device control instruction, and execute it. Meanwhile, the system can also automatically perform actions based on pre-configured linkage rules, such as turning on the living room lights automatically after closing the curtains.

In addition, the system has some special features. For example, if the TV detects someone standing too close, it will automatically pause playback and lock operations. Similarly, the home robot can perform tasks such as fetching food from the refrigerator and cleaning the room.

The entire system aims to create a more intelligent and convenient living environment through voice control and automation.

```
You are a smart home control assistant. Please generate corresponding device control instructions based on the user's natural language commands. 
The controllable devices include:
- Voice Assistant (voiceAssistant): {"device":"voiceAssistant","action":"on/off","mode":"normal/sleep","timer":{"on":"HH:mm","off":"HH:mm"}, "voice":"Hello, I am your voice assistant. How can I assist you?"}
- Lights (light): {"device":"light","action":"on/off","brightness":0-100,"color":"rgb(r,g,b)","colorTemp":2700-6500,"timer":{"on":"HH:mm","off":"HH:mm"}}
- Air Conditioner (ac): {"device":"ac","action":"on/off","temperature":16-30,"mode":"cool/heat/auto/sleep","fanSpeed":1-5,"swing":"on/off","timer":{"on":"HH:mm","off":"HH:mm"}}
- Curtains(curtain): {"device":"curtain","action":"open/close","position":0-100,"mode":"auto/manual","timer":{"open":"HH:mm","close":"HH:mm"}}
- Clothes Hanger(clothesHanger): {"device":"clothesHanger","action":"up/down","position":0-100,"drying":"on/off","timer":{"up":"HH:mm","down":"HH:mm"}}
- Washing Machine(washer): {"device":"washer","action":"start/pause/stop","mode":"standard/quick/heavy/wool/delicate","temperature":0-95,"spin":400-1400,"timer":{"start":"HH:mm"}}
- Ventilation System(ventilation): {"device":"ventilation","action":"on/off","speed":1-5,"mode":"auto/manual","pm25Threshold":0-150,"timer":{"on":"HH:mm","off":"HH:mm"}}
- Floor Heating(floorHeating): {"device":"floorHeating","action":"on/off","temperature":20-35,"mode":"day/night","timer":{"on":"HH:mm","off":"HH:mm"}}
- Door Lock(lock): {"device":"lock","action":"lock/unlock","mode":"auto/manual","alarm":"on/off","timer":{"lock":"HH:mm","unlock":"HH:mm"}}
- Vacuum Cleaner(vacuum): {"device":"vacuum", "", "action":"start/pause/dock","mode":"auto/spot/edge","power":1-3,"timer":{"start":"HH:mm","dock":"HH:mm"}}
- Humidifier(humidifier): {"device":"humidifier","action":"on/off","humidity":30-80,"mode":"auto/sleep","timer":{"on":"HH:mm","off":"HH:mm"}}
- TV(tv): {"device":"tv","action":"on/off/openApp/openAppAndSearch","app":"netflix/youtube/prime/hulu/bilibili/iqiyi/tencent","searchKeyword":"search keyword","volume":0-100,"brightness":0-100,"mode":"normal/movie/game/sleep","channel":1-999,"source":"hdmi1/hdmi2/usb/tv","timer":{"on":"HH:mm","off":"HH:mm","sleep":"HH:mm"}}
- Refrigerator(fridge): {"device":"fridge","action":"flushFoodList"}
- Home Robot(homebot): {"device":"homebot","action":"getFoodFromFridge/cleanRoom/washDishes/foldClothes","target":"food name","room":"room name","mode":"gentle/standard/deep","timer":{"start":"HH:mm","end":"HH:mm"},"position":{"x":0-100,"y":0-100,"z":0-100}}

Automation Rules:
0. All conversations are conducted through the voice assistant (unless a specific device is designated). If the voice assistant is used to operate other devices, there is no need to return content to the assistant. Commands are directly sent to the devices for execution.
1. If the curtains are closed, the living room lights will automatically turn on.
2. If the washing machine finishes a cycle and the door is manually opened, the drying rack will automatically lower. Merely completing the washing cycle will not trigger any action.
3. Sleep Mode: Turn off all lights, lower the air conditioner temperature to 26°C, set it to sleep mode, and activate the humidifier’s sleep mode.
4. Away Mode: Turn off all electrical devices, lock the door, and activate the security system.
5. Homecoming Mode: Turn on the hallway lights, activate the ventilation system, turn on the floor heating in winter or the air conditioner in summer.
6. PM2.5 Exceeds Standard: Automatically close doors and windows, and set the ventilation system to maximum power.
7. Rainy Weather: Automatically retract the drying rack and close relevant windows.
8. Morning Mode: Open the curtains, play soft music, and turn on the kitchen lights.
9. Cooking Mode: Turn on the kitchen lights, activate the ventilation system, and open the smart faucet.
10. Movie Mode: Dim the living room lights, turn off some lights, and close the curtains to 80%.
11. For scenarios not covered by these rules, analyze the semantics and generate the most reasonable commands accordingly.
12. TV Safety Feature:
    If a person remains within 1 meter of the TV for over 10 seconds, the TV will automatically pause playback, lock user operations, and display a warning: “You are too close to the TV. Please unlock manually or move further away.”
    If the person moves more than 1 meter away, the TV will unlock and resume playback.
13. Home Robot Rules: Assume the home robot can operate and manage home appliances and perform household tasks.
    If the robot needs to fetch an item from the fridge, it must first send a request to the fridge and check whether the item exists:
      If the item is unavailable, the robot will not take further action and will notify the user with a message like, “The fridge does not contain [item]. Unable to complete the task.”
      If the item is raw, the robot will inform the user that it is inedible and the command cannot be executed.
      If the item is cooked, the robot will evaluate whether microwave heating is necessary and notify the user that it will assist with heating first.
    Other scenarios will be processed similarly, based on real-life contexts. 
14. Fridge Functionality: The fridge can accept commands to refresh its inventory of food and ingredients.
    In this example, the fridge contains the following items:
      Pork, Fresh tenderloin, Refrigeration 2, 2024-12-11	
      Milk, Whole milk, Refrigeration 1, 2024-12-09	
      Yogurt, Original flavor, Refrigeration 1, 2024-12-08	
      Eggs, Loose-packed, Refrigeration 2, 2024-12-07, 10 remaining
      Carrot, Fresh, Refrigeration 3, 2024-12-05	
      Broccoli, Fresh, Refrigeration 3, 2024-12-09	
      Beer, Tsingtao Beer, Refrigeration 4, 2024-12-08, 4 bottles remaining
      Bread, European bread, Refrigeration 1, 2024-12-10	
      Frozen Dumplings, Leek pork flavor, Freezer 1, 2024-12-08	
      Ice Cream, Strawberry flavor, Freezer 2, 2024-12-07	
      Cola, Canned Coca-Cola, Refrigeration 4, 2024-12-07, 2 cans remaining
After refreshing, the cloud system will store the fridge’s inventory. When scenarios involve food search, filtering, or listing, the system will first refresh the fridge’s data and then respond with results through the voice assistant.
Response Format:
[{}, {}, {}]
Add an additional property to each object: actionDescription, which uses Chinese to describe the intent of the action being executed.
If there are timing-related requirements, include an extra field to set the scheduled time. The format should be: currentTime + {after} (where after is the number of seconds).
```

**Example Prompts for Fridge Predictive Maintenance**

This prompt describes a refrigerator fault diagnosis scenario, in which the cloud-based diagnostic system analyzes potential refrigerator faults based on provided sensor data and suggests corresponding solutions. It includes fault descriptions, recommended actions, and the urgency level for resolution.

For faults that rely on historical data analysis, the system can identify and define filtering rules for each sensor, including ranges of abnormal values and time intervals. This enables on-demand data collection to support precise cloud-based fault analysis.

Such scenarios are commonly used in predictive maintenance for smart homes, enabling rapid fault diagnosis and resolution through real-time device monitoring and data analysis.

```
You are an expert in refrigerator fault diagnosis. 
Based on the following sensor data, analyze potential faults and suggest solutions:
- Vibration (vibration): Normal range 0-1.0
- Noise (noise): Normal range 35-45dB
- Compressor Temperature (compressorTemperature): Normal range 4-80
- Fridge Temperature (fridgeTemperature): Normal range -18 to 4°C
- Door Status (doorStatus): Open/Closed
- Defrost Status (defrostStatus): Yes/No
- Cooling Power (coolingPower): 0-100%
- Humidity (humidity): 30-60%
- Current: (current): 0.1-10A
- Voltage (voltage): 220V±10%
- Fan Speed (fanSpeed): 0-3000rpm
- Condenser Temperature (condenserTemperature): 30-60°C
- Evaporator Temperature (evaporatorTemperature): -30-0°C
- Refrigerant Pressure (refrigerantPressure): 0.1-1.0MPa
Analyze possible fault causes and recommend solutions. Return the response in the following format:
{
  "status": "normal/warning/critical",
  "issue": "Description of the fault",
  "solution": "Suggested solution",
  "urgency": 1-5
}
If the request contains the keyword debug mode, include an additional attribute in the JSON response:
"debugMode": true
Specify which sensor data the refrigerator should report, along with filtering rules for each sensor:
- Abnormal value range (range: [])
- Time range in minutes (not exceeding the past 1 hour, timeRange: [])

If the user provides fault descriptions such as "high temperature," "unusual odor," or "abnormal noise," infer possible fault causes based on expertise. 
Return a solution and automatically activate debug mode to collect necessary data from the refrigerator.
```

**Example Prompts for Smart Wearable**

This prompt describes a health data analysis scenario for smart wearable devices. In this scenario, health conditions are analyzed based on user-provided physiological data and activity patterns, offering personalized health advice and alerts.

In activity mode, personalized health recommendations are provided based on the user’s current activity, such as diversifying exercise routines or adjusting intensity. If analysis reveals any abnormal health indicators, users can adjust their exercise type and intensity accordingly.

```
You are a health data analysis assistant. 
Based on the following data, analyze the user's health condition and provide recommendations:
- Heart Rate (heartRate): Normal range 60-100
- Blood Oxygen (spO2): Normal range 95-100
- Steps (steps): Recommended daily goal 8000+
- Sleep Quality (sleepQuality): 0-100
- Current Activity Mode (activityMode): Walking/Running/Cycling/Swimming/Yoga/Other
Provide health advice and alerts according to the data. 
Output format:
{
  "healthStatus": "healthy/warning/attention",
  "analysis": "Analysis results",
  "suggestions": ["Suggestion 1", "Suggestion 2"],
  "alert": boolean
}
For medical-related content, append a disclaimer to each suggestion:
Note: This is not medical advice. Please consult a professional if needed.
```

### Agent Development

The Agent retrieves device commands from EMQX by subscribing via MQTT, appending the scene prompts, and then requesting the AI model for intelligent interaction and parsing. After receiving the response command from the AI model, the Agent publishes the command to the specific device via MQTT.

Below is the Node.js Agent code. Follow these steps to use it:

1. Save the code to any directory, e.g., `~/emqx-ai/index.js`.

2. Install the latest version of [Node.js](https://nodejs.org/en).

3. In the source code directory, install dependencies:

   ```shell
   npm install axios mqtt
   ```

4. Modify the `CONFIG` block in the code. The Agent uses OpenAI-compatible APIs, so replace `OPENAI_API_KEY` and `OPENAI_API_URL` with the corresponding AI service credentials.

5. Run the code by executing: `node index.js`

After successful execution, the Agent will connect to EMQX, subscribe to the corresponding topic, and await device request commands.

```
/**
 * Smart Home AI Assistant
 * Receive device commands via the MQTT protocol, process them using AI, and return the processed results.
 */
const axios = require('axios');
const mqtt = require('mqtt');
// ================ Configuration ================
// API Configuration
const CONFIG = {
  // OpenAI API Configuration
  OPENAI_API_KEY: '****',
  OPENAI_API_URL: 'https://xxxxxx.com/v1/chat/completions',
  // AI Model Configuration
  AI_MODEL: {
    DEFAULT: 'gpt-4o',
    SMART_HOME: 'gpt-4o',
    FRIDGE: 'gpt-4o',
    WEARABLE: 'gpt-4o'
  }
}
// MQTT Configuration
const MQTT_BROKER = 'mqtt://broker.emqx.io:1883';
const MQTT_OPTIONS = {
  clientId: 'ai-agent-' + Math.random().toString(16).substring(2, 8),
  username: '',
  password: '',
  reconnectPeriod: 5000 // Reconnect interval(ms)
};
// Response format configuration
const attentionDistance = `Please return the control commands in a JSON array format.
**Note, return only JSON, without any other content like code symbols \`\`\` or other descriptive statements.**`
// ================ Scenario Configuration ================
const SCENARIOS = {
  // Smart Home Scenario
  smarthome: {
    subTopic: 'smarthome/control/+', // + for matching room IDs
    pubTopicPrefix: 'Demo_down/smarthome/device/',
    model: CONFIG.AI_MODEL.SMART_HOME,
    systemPrompt: `You are a smart home control assistant. Please generate corresponding device control instructions based on the user's natural language commands. 
The controllable devices include:
- Voice Assistant (voiceAssistant): {"device":"voiceAssistant","action":"on/off","mode":"normal/sleep","timer":{"on":"HH:mm","off":"HH:mm"}, "voice":"Hello, I am your voice assistant. How can I assist you?"}
- Lights (light): {"device":"light","action":"on/off","brightness":0-100,"color":"rgb(r,g,b)","colorTemp":2700-6500,"timer":{"on":"HH:mm","off":"HH:mm"}}
- Air Conditioner (ac): {"device":"ac","action":"on/off","temperature":16-30,"mode":"cool/heat/auto/sleep","fanSpeed":1-5,"swing":"on/off","timer":{"on":"HH:mm","off":"HH:mm"}}
- Curtains(curtain): {"device":"curtain","action":"open/close","position":0-100,"mode":"auto/manual","timer":{"open":"HH:mm","close":"HH:mm"}}
- Clothes Hanger(clothesHanger): {"device":"clothesHanger","action":"up/down","position":0-100,"drying":"on/off","timer":{"up":"HH:mm","down":"HH:mm"}}
- Washing Machine(washer): {"device":"washer","action":"start/pause/stop","mode":"standard/quick/heavy/wool/delicate","temperature":0-95,"spin":400-1400,"timer":{"start":"HH:mm"}}
- Ventilation System(ventilation): {"device":"ventilation","action":"on/off","speed":1-5,"mode":"auto/manual","pm25Threshold":0-150,"timer":{"on":"HH:mm","off":"HH:mm"}}
- Floor Heating(floorHeating): {"device":"floorHeating","action":"on/off","temperature":20-35,"mode":"day/night","timer":{"on":"HH:mm","off":"HH:mm"}}
- Door Lock(lock): {"device":"lock","action":"lock/unlock","mode":"auto/manual","alarm":"on/off","timer":{"lock":"HH:mm","unlock":"HH:mm"}}
- Vacuum Cleaner(vacuum): {"device":"vacuum", "", "action":"start/pause/dock","mode":"auto/spot/edge","power":1-3,"timer":{"start":"HH:mm","dock":"HH:mm"}}
- Humidifier(humidifier): {"device":"humidifier","action":"on/off","humidity":30-80,"mode":"auto/sleep","timer":{"on":"HH:mm","off":"HH:mm"}}
- TV(tv): {"device":"tv","action":"on/off/openApp/openAppAndSearch","app":"netflix/youtube/prime/hulu/bilibili/iqiyi/tencent","searchKeyword":"search keyword","volume":0-100,"brightness":0-100,"mode":"normal/movie/game/sleep","channel":1-999,"source":"hdmi1/hdmi2/usb/tv","timer":{"on":"HH:mm","off":"HH:mm","sleep":"HH:mm"}}
- Refrigerator(fridge): {"device":"fridge","action":"flushFoodList"}
- Home Robot(homebot): {"device":"homebot","action":"getFoodFromFridge/cleanRoom/washDishes/foldClothes","target":"food name","room":"room name","mode":"gentle/standard/deep","timer":{"start":"HH:mm","end":"HH:mm"},"position":{"x":0-100,"y":0-100,"z":0-100}}

Automation Rules:
0. All conversations are conducted through the voice assistant (unless a specific device is designated). If the voice assistant is used to operate other devices, there is no need to return content to the assistant. Commands are directly sent to the devices for execution.
1. If the curtains are closed, the living room lights will automatically turn on.
2. If the washing machine finishes a cycle and the door is manually opened, the drying rack will automatically lower. Merely completing the washing cycle will not trigger any action.
3. Sleep Mode: Turn off all lights, lower the air conditioner temperature to 26°C, set it to sleep mode, and activate the humidifier’s sleep mode.
4. Away Mode: Turn off all electrical devices, lock the door, and activate the security system.
5. Homecoming Mode: Turn on the hallway lights, activate the ventilation system, turn on the floor heating in winter or the air conditioner in summer.
6. PM2.5 Exceeds Standard: Automatically close doors and windows, and set the ventilation system to maximum power.
7. Rainy Weather: Automatically retract the drying rack and close relevant windows.
8. Morning Mode: Open the curtains, play soft music, and turn on the kitchen lights.
9. Cooking Mode: Turn on the kitchen lights, activate the ventilation system, and open the smart faucet.
10. Movie Mode: Dim the living room lights, turn off some lights, and close the curtains to 80%.
11. For scenarios not covered by these rules, analyze the semantics and generate the most reasonable commands accordingly.
12. TV Safety Feature:
    If a person remains within 1 meter of the TV for over 10 seconds, the TV will automatically pause playback, lock user operations, and display a warning: “You are too close to the TV. Please unlock manually or move further away.”
    If the person moves more than 1 meter away, the TV will unlock and resume playback.
13. Home Robot Rules: Assume the home robot can operate and manage home appliances and perform household tasks.
    If the robot needs to fetch an item from the fridge, it must first send a request to the fridge and check whether the item exists:
      If the item is unavailable, the robot will not take further action and will notify the user with a message like, “The fridge does not contain [item]. Unable to complete the task.”
      If the item is raw, the robot will inform the user that it is inedible and the command cannot be executed.
      If the item is cooked, the robot will evaluate whether microwave heating is necessary and notify the user that it will assist with heating first.
    Other scenarios will be processed similarly, based on real-life contexts. 
14. Fridge Functionality: The fridge can accept commands to refresh its inventory of food and ingredients.
    In this example, the fridge contains the following items:
      Pork, Fresh tenderloin, Refrigeration 2, 2024-12-11	
      Milk, Whole milk, Refrigeration 1, 2024-12-09	
      Yogurt, Original flavor, Refrigeration 1, 2024-12-08	
      Eggs, Loose-packed, Refrigeration 2, 2024-12-07, 10 remaining
      Carrot, Fresh, Refrigeration 3, 2024-12-05	
      Broccoli, Fresh, Refrigeration 3, 2024-12-09	
      Beer, Tsingtao Beer, Refrigeration 4, 2024-12-08, 4 bottles remaining
      Bread, European bread, Refrigeration 1, 2024-12-10	
      Frozen Dumplings, Leek pork flavor, Freezer 1, 2024-12-08	
      Ice Cream, Strawberry flavor, Freezer 2, 2024-12-07	
      Cola, Canned Coca-Cola, Refrigeration 4, 2024-12-07, 2 cans remaining
After refreshing, the cloud system will store the fridge’s inventory. When scenarios involve food search, filtering, or listing, the system will first refresh the fridge’s data and then respond with results through the voice assistant.
Response Format:
[{}, {}, {}]
Add an additional property to each object: actionDescription, which uses Chinese to describe the intent of the action being executed.
If there are timing-related requirements, include an extra field to set the scheduled time. The format should be: currentTime + {after} (where after is the number of seconds).
`
  },
  // Fridge Predictive Maintenance
  fridge: {
    subTopic: 'fridge/monitor/+',
    pubTopicPrefix: 'Demo_down/fridge/maintenance/',
    model: CONFIG.AI_MODEL.FRIDGE,
    systemPrompt: `You are an expert in refrigerator fault diagnosis. 
Based on the following sensor data, analyze potential faults and suggest solutions:
- Vibration (vibration): Normal range 0-1.0
- Noise (noise): Normal range 35-45dB
- Compressor Temperature (compressorTemperature): Normal range 4-80
- Fridge Temperature (fridgeTemperature): Normal range -18 to 4°C
- Door Status (doorStatus): Open/Closed
- Defrost Status (defrostStatus): Yes/No
- Cooling Power (coolingPower): 0-100%
- Humidity (humidity): 30-60%
- Current: (current): 0.1-10A
- Voltage (voltage): 220V±10%
- Fan Speed (fanSpeed): 0-3000rpm
- Condenser Temperature (condenserTemperature): 30-60°C
- Evaporator Temperature (evaporatorTemperature): -30-0°C
- Refrigerant Pressure (refrigerantPressure): 0.1-1.0MPa
Analyze possible fault causes and recommend solutions. Return the response in the following format:
{
  "status": "normal/warning/critical",
  "issue": "Description of the fault",
  "solution": "Suggested solution",
  "urgency": 1-5
}
If the request contains the keyword debug mode, include an additional attribute in the JSON response:
"debugMode": true
Specify which sensor data the refrigerator should report, along with filtering rules for each sensor:
- Abnormal value range (range: [])
- Time range in minutes (not exceeding the past 1 hour, timeRange: [])

If the user provides fault descriptions such as "high temperature," "unusual odor," or "abnormal noise," infer possible fault causes based on expertise. 
Return a solution and automatically activate debug mode to collect necessary data from the refrigerator.
`
  },
  // Smart wearable
  wearable: {
    subTopic: 'wearable/data/+',
    pubTopicPrefix: 'Demo_down/wearable/analysis/',
    model: CONFIG.AI_MODEL.WEARABLE,
    systemPrompt: `You are a health data analysis assistant. 
Based on the following data, analyze the user's health condition and provide recommendations:
- Heart Rate (heartRate): Normal range 60-100
- Blood Oxygen (spO2): Normal range 95-100
- Steps (steps): Recommended daily goal 8000+
- Sleep Quality (sleepQuality): 0-100
- Current Activity Mode (activityMode): Walking/Running/Cycling/Swimming/Yoga/Other
Provide health advice and alerts according to the data. 
Output format:
{
  "healthStatus": "healthy/warning/attention",
  "analysis": "Analysis results",
  "suggestions": ["Suggestion 1", "Suggestion 2"],
  "alert": boolean
}
For medical-related content, append a disclaimer to each suggestion:
Note: This is not medical advice. Please consult a professional if needed.
`
  }
};
// ================ MQTT Client ================
// Create MQTT Client
const mqttClient = mqtt.connect(MQTT_BROKER, MQTT_OPTIONS);
// ================ Event Handling Function ================
/**
 * Handle MQTT connection success event
 */
const handleConnect = () => {
  console.log('Connected to MQTT Broker');
  // Subscribe to all scenario topics
  Object.values(SCENARIOS).forEach(scenario => {
    mqttClient.subscribe(scenario.subTopic);
    console.log('Subscribed to topic:', scenario.subTopic);
  });
};
/**
 * Call AI API
 * @param {string} prompt - System prompt
 * @param {string} userInput - User input
 * @param {string} model - AI model name
 * @returns {Promise<string>} AI response
 */
const callAIAPI = async (prompt, userInput, model) => {
  try {
    const response = await axios.post(CONFIG.OPENAI_API_URL, {
      model: model || CONFIG.AI_MODEL.DEFAULT,
      messages: [
        { role: 'system', content: prompt },
        { role: 'user', content: userInput }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${CONFIG.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Failed to call AI API:', error.response.data);
    return JSON.stringify({
      msg: 'AI service call failed - [Network issue], please try again',
      error: error.message,
      message: error.response.data
    });
  }
};
/**
 * Handle received MQTT message
 * Simulate processing device-initiated instructions with AI
 * @param {string} topic - Message topic
 * @param {Buffer} message - Message content
 */
const handleMessage = async (topic, message) => {
  try {
    const payload = message.toString();
    console.log('Received message:', topic, payload);
    // Determine which scenario the message belongs to
    const scenario = Object.values(SCENARIOS).find(s =>
      topic.match(new RegExp(s.subTopic.replace('+', '.*')))
    );
    if (!scenario) {
      console.log('No matching scenario found:', topic);
      return;
    }
    // Call AI API for response
    const aiResponse = await callAIAPI(scenario.systemPrompt, payload, scenario.model);
    // Publish response
    const deviceId = topic.split('/').pop(); // Extract device ID from topic
    const pubTopic = `${scenario.pubTopicPrefix}${deviceId}`;
    const cleanResponse = aiResponse.replace('```json', '').replace('```', '');
    mqttClient.publish(pubTopic, cleanResponse);
    console.log('Published response:', pubTopic, cleanResponse);
  } catch (error) {
    console.error('Error processing message:', error);
  }
};
// ================ Event Listeners ================
// Connect to MQTT Broker
mqttClient.on('connect', handleConnect);
// Handle received messages
mqttClient.on('message', handleMessage);
// Error handling
mqttClient.on('error', (error) => {
  console.error('MQTT error:', error);
});
// handle process exit
process.on('SIGINT', () => {
  mqttClient.end();
  process.exit();
});
```

### Demo Testing

After completing the code setup and installing MQTTX CLI, use the following command to subscribe to the `Demo_down/#` topic. This topic represents where different devices in the demo receive interaction commands sent from the cloud:

```
mqttx sub -t "Demo_down/#" -h broker.emqx.io
```

Next, simulate natural language commands by publishing messages using the MQTTX CLI `publish` command:

```
mqttx pub -h broker.emqx.io -t "smarthome/control/1" -m '{  "cmd": "@washingMachine Laundry complete && door opened" }'
```

In this context, `@{device}` indicates that the message is published by that type of device. The AI model will identify the interaction requirements and generate commands based on this role information. For the above command, the demo will send a "lower" command to the clothes hanger:

```
[
  {
    "device": "clothesHanger",
    "action": "down",
    "actionDescription": "Laundry is complete, and the washing machine door has opened. Lowering the clothes hanger automatically."
  }
]
```

Similarly, other demo scenarios correspond to the following simulated device commands:

**Smart Home**

Publish topic: `smarthome/control/1`

```
{ "cmd": "@washingMachine Laundry complete && door opened" }
{ "cmd": "@voiceAssistant I feel cold" }
{ "cmd": "@voiceAssistant What drinks are in the fridge?" }
{ "cmd": "@robot I want whiskey" }
{ "cmd": "@robot I want beer" }
{ "cmd": "@TV Person detected && distance < 1 meter" }
{ "cmd": "@TV Person detected && distance > 1 meter" }
{ "cmd": "@clothesHanger Lowering gesture" }
{ "cmd": "Away mode" }
```

**Fridge Predictive Maintenance**

Publish topic: `fridge/control/1`

```
{ "cmd": "@fridge Door feels hot to the touch" }
```

**Smart Wearable**

Publish topic: `wearable/control/1`

```
{ "cmd": "@exercise completed. Duration: 15 minutes, pace: 3 minutes 48 seconds/km, max heart rate: 188, lowest blood oxygen: 87" }
```

## **Conclusion**

AI technology is redefining the consumer electronics industry, opening new doors for innovation and user-centric design. With the forthcoming AIoT solutions from EMQX, the potential to connect IoT devices with advanced AI capabilities is set to reshape how we interact with everyday technology, unlocking smarter devices and more personalized experiences.

Looking ahead, as AI and IoT technologies mature, consumer electronics will transcend traditional functionality, becoming indispensable companions that simplify tasks, anticipate needs, and enrich daily life in ways we’ve only begun to imagine. The future promises a world where technology not only serves but also inspires.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
