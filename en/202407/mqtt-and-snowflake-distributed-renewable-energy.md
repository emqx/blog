## Introduction

Renewable energy sources like wind and solar power are becoming the primary focus for future energy supply due to their cost-effectiveness and environmental benefits. However, these energy sources come with challenges such as decentralized supply, numerous devices, and wide regional distribution. Additionally, seasonal and weather variations across different regions add to the uncertainty.

As social demand for electricity continues to rise, efficiently deploying electricity is crucial to ensure a balance between supply and demand and maximize the benefits of new energy generation.

This blog will discuss how EMQX and Snowflake can be used to collect, store, and analyze data from power generation equipment within the complex power supply chain. This integration allows for accurate forecasting of power generation capacity, leading to more efficient operations.

## Scenario Introduction

Solar and wind power generation forecasting depends on geographic location, historical climate data, operational information systems, and power generation data. In this blog, we utilize the simulate command of the MQTT client tool, MQTTX CLI, along with a simulation script to generate multiple solar and wind power plants and simulate their data collection and submission.

- These virtual plants connect to EMQX, periodically generate simulation data, and publishes their status data to a specified MQTT topic.
- EMQX receives the messages and stores them in Snowflake using its built-in rule engine and data integration features.
- Snowflake saves these data and then analyzes them on its platform.

**Typical data format is as follows:**

| Field Name     | Data Type | Description                                                                         |
| -------------- | --------- | ----------------------------------------------------------------------------------- |
| id             | STRING    | Unique identifier for each data record                                              |
| city           | STRING    | Name of the city from which the data originated                                     |
| model          | STRING    | Device model identifier                                                             |
| regionID       | STRING    | Identifier for the region where the device is located                               |
| type           | STRING    | Device type, such as "Wind" or "Solar"                                              |
| ratedPower     | FLOAT     | Rated power of the device in kilowatts (kW)                                         |
| timestamp      | TIMESTAMP | Exact time when the data was generated                                              |
| powerOutput    | FLOAT     | Real-time power output in kilowatts (kW)                                            |
| windSpeed      | FLOAT     | Wind speed in meters per second (m/s), valid only for wind turbines                 |
| solarRadiation | FLOAT     | Light intensity in watts per square meter (W/m²), valid only for solar power plants |
| rotationSpeed  | FLOAT     | Rotational speed in revolutions per minute (RPM), valid only for wind turbines      |

An example of the corresponding data is shown below:

```json
{
  "id": "6b50f69c-9c9b-48e7-ae9d-849e6e5e5dd5",
  "city": "San Francisco",
  "model": "Solar-Model-A1",
  "regionID": "01",
  "type": "Solar",
  "ratedPower": 15.5,
  "timestamp": "2024-07-10T12:34:56Z",
  "powerOutput": 12.3,
  "windSpeed": null,
  "solarRadiation": 720,
  "rotationSpeed": null
}
```

## Installing EMQX Enterprise

[EMQX Enterprise](https://www.emqx.com/en/products/emqx) is a robust MQTT platform designed for enterprise use, offering highly reliable and high-performance real-time data access, along with data processing and integration capabilities.

For installation instructions, please refer to [this guide](https://docs.emqx.com/en/enterprise/latest/deploy/install.html).

## Preparing MQTTX Simulation Data

The [MQTTX CLI](https://mqttx.app/cli) is a versatile and user-friendly MQTT 5.0 command line tool. It provides simulation commands that allow you to create simulation scripts using Node.js to generate and publish simulated messages.

1. Create a file named solar-wind-power-plant.js and paste the provided simulation script into it. You can also modify the script by following [this guide](https://mqttx.app/docs/cli/get-started#simulate).
2. Run the script using the `simulate` command, specifying the script path and the number of clients to simulate:

```bash
mqttx simulate --file ./solar-wind-power-plant.js -c 10
```

This command does the following:

- The `--file` option specifies the path to the solar-wind-power-plant.js script file.
- The `-c` option specifies that 10 simulated clients will be created.

You can adjust the number of clients and the frequency of messages according to your needs by referring to the [MQTTX CLI Options for Publishing](https://mqttx.app/docs/cli/get-started#publish).

After executing the command, the script will create 10 clients that connect to EMQX, with each client publishing one message per second to the `mqttx/simulate/Solar-Wind-Power-Plant/{clientid}` topic, based on the data types defined in the scenario.

To verify that messages are being published correctly, you can subscribe to the topic using the `sub` command of the MQTTX CLI:

```bash
mqttx sub -t mqttx/simulate/Solar-Wind-Power-Plant/+ -v
```

Appendix: Contents of the simulation script.

```js
const store = {
  index: 0
};
​
function transformToFloat(val) {
  if (typeof val !== 'number') {
    val = Number(val);
  }
  const _val = val.toFixed(2);
  if (_val.endsWith('.00')) {
    return parseFloat(_val) + 0.01;
  }
  return parseFloat(_val);
}
​
function getWindPower(hour, faker) {
  if (hour >= 8 && hour < 18) {
    return faker.datatype.float({ min: 900, max: 1100 });
  } else {
    return faker.datatype.float({ min: 600, max: 900 });
  }
}
​
function calculateWindSpeed(rotationSpeed) {
  // Assume a linear relationship between rotation speed and wind speed
  return rotationSpeed / 60; // Simple linear relationship
}
​
function getSolarPower(hour, isCloudy, faker) {
  if (hour >= 6 && hour < 18) {
    let power = faker.datatype.float({ min: 5, max: 20 });
    if (isCloudy) {
      power *= 0.8;
    }
    return power;
  } else {
    return faker.datatype.float({ min: 0, max: 1 });
  }
}
​
function calculateSolarRadiation(powerOutput) {
  // Assume a linear relationship between power output and solar radiation intensity
  return powerOutput * 50; // Simple linear relationship
}
​
function generator(faker, options) {
  const clientid = options.clientid;
  const currentTimestamp = Date.now(); // Use the current time
  const currentDate = new Date(currentTimestamp).toISOString().split('T')[0];
​
  if (!store[clientid]) {
    const deviceType = faker.helpers.arrayElement(['Wind', 'Solar']);
    const ratedPower = deviceType === 'Wind' ? 1500 : faker.datatype.float({ min: 5, max: 20 });
    store[clientid] = {
      id: faker.datatype.uuid(),
      city: faker.address.city(),
      model: faker.helpers.arrayElement(['Model_A', 'Model_B', 'Model_C']),
      regionID: faker.helpers.arrayElement(['01', '02', '03', '04']),
      type: deviceType,
      ratedPower,
      currentDate,
      isCloudy: faker.datatype.boolean(0.3), // 30% chance of being cloudy
      powerOutput: 0,
      windSpeed: deviceType === 'Wind' ? null : 0,
      solarRadiation: deviceType === 'Solar' ? null : 0,
      rotationSpeed: deviceType === 'Wind' ? faker.datatype.float({ min: 0, max: 1500 }) : null
    };
  }
​
  const data = store[clientid];
  const hour = new Date(currentTimestamp).getHours();
​
  // Determine if it is cloudy at the start of a new day
  if (data.currentDate !== currentDate) {
    data.currentDate = currentDate;
    data.isCloudy = faker.datatype.boolean(0.3); // 30% chance of being cloudy
  }
​
  if (data.type === 'Wind') {
    data.rotationSpeed = faker.datatype.float({ min: 0, max: 1500 });
    data.powerOutput = getWindPower(hour, faker);
    data.windSpeed = calculateWindSpeed(data.rotationSpeed);
  } else if (data.type === 'Solar') {
    data.powerOutput = getSolarPower(hour, data.isCloudy, faker);
    data.solarRadiation = calculateSolarRadiation(data.powerOutput);
  }
​
  return {
    message: JSON.stringify({
      id: data.id,
      city: data.city,
      model: data.model,
      regionID: data.regionID,
      type: data.type,
      ratedPower: transformToFloat(data.ratedPower),
      timestamp: currentTimestamp,
      powerOutput: transformToFloat(data.powerOutput),
      windSpeed: data.windSpeed ? transformToFloat(data.windSpeed) : 0,
      solarRadiation: data.solarRadiation ? transformToFloat(data.solarRadiation) : 0,
      rotationSpeed: data.rotationSpeed ? transformToFloat(data.rotationSpeed) : 0
    })
  };
}
​
const name = 'Solar-Wind-Power-Plant';
const author = 'EMQX Team';
const dataFormat = 'JSON';
const version = '0.0.1';
const description = `Solar and wind power plant simulator, mock data generated with current timestamp.
Cloudiness is determined at the start of each day.`;
​
module.exports = {
  generator,
  name,
  author,
  dataFormat,
  version,
  description,
};
```

## Setting Up the Snowflake Environment

Snowflake is a cloud-based data platform that offers a highly scalable and flexible solution for data storage and analysis. It provides robust data warehousing capabilities, making it ideal for handling large-scale, multi-source data.

In the IoT domain, Snowflake can store and analyze vast amounts of data collected from devices and sensors, enabling real-time data processing, visualization, and insights.

In this section, we will set up the Snowflake environment, create the necessary tables, and obtain the connection information.

### 1. Creating a Database and Data Tables

To store the history data, you need to create a database and data tables in Snowflake.

- If you don’t have a Snowflake account yet, click [here](https://www.snowflake.com/) to create one.
- After logging into the Snowflake console, navigate to the **Data → Databases** page via the left menu and create a database named IOT_DATA.

  ![Creating a new database named IOT_DATA on the Snowflake console](https://assets.emqx.com/images/d7589b8e74d9e7d6cad0335a9315cb9a.png)

- Select the PUBLIC schema under the IOT_DATA database and click **Create** in the upper right corner to create a table for storing data submitted by solar and wind power plants.

  ![Creating a table under the PUBLIC schema in the IOT_DATA database on the Snowflake console](https://assets.emqx.com/images/5a434f87e776e423c9642af3fb582428.png)

Choose `Standard` for the data table type. The corresponding Snowflake table creation statement as follows:

```sql
CREATE TABLE RenewableEnergyData (
    id STRING,
    city STRING,
    model STRING,
    regionID STRING,
    type STRING,
    ratedPower FLOAT,
    timestamp TIMESTAMP,
    powerOutput FLOAT,
    windSpeed FLOAT,
    solarRadiation FLOAT,
    rotationSpeed FLOAT
);
```

### 2. Preparing the Information Needed for Connection

This blog utilizes the Snowflake REST API for data writing. The following information is required for the request:

| **Information**      | **Description**                                              |
| :------------------- | :----------------------------------------------------------- |
| Username             | Snowflake console login username for access and authentication. |
| Account ID           | Used for REST API access and authentication. Refer to [Account identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier) for how to get it. The account ID should be in the format {orgname}-{account_name}. |
| Key Pair             | Used for [Authentication](https://docs.snowflake.com/en/developer-guide/sql-api/authenticating#using-key-pair-authentication) with the REST API. Refer to [this guide](https://docs.snowflake.com/en/user-guide/key-pair-auth) to generate the certificate and add it to the corresponding user. You will need the certificate's private key rsa_key.p8 file. |
| Authentication Token | JWT Token issued using account information and the certificate's private key, used in REST API authentication. See [this guide](https://docs.snowflake.com/en/developer-guide/sql-api/authenticating#using-key-pair-authentication) for issuance methods. Below is a sample Node.js code for issuance. |

Sample Node.js code for authenticated token issuance:

```js
// sql-api-generate-jwt.js.
​
const crypto = require('crypto')
const fs = require('fs');
var jwt = require('jsonwebtoken');
​
// Modify the following values based on actual situation
​
// Path to the certificate private key file
var privateKeyFile = fs.readFileSync('./rsa_key.p8');
// Certificate password (if any)
var mypassphrase = '';
// Account ID, English characters need to be uppercase
var accountID = "OXTPEXE-LCF92X4";
// Registration username, English characters need to be uppercase
var username = 'XXXXXX'
​
privateKeyObject = crypto.createPrivateKey({ key: privateKeyFile, format: 'pem', passphrase: mypassphrase });
var privateKey = privateKeyObject.export({ format: 'pem', type: 'pkcs8' });
​
publicKeyObject = crypto.createPublicKey({ key: privateKey, format: 'pem' });
var publicKey = publicKeyObject.export({ format: 'der', type: 'spki' });
const FP = crypto.createHash('sha256').update(publicKey, 'utf8').digest('base64')
var publicKeyFingerprint = 'SHA256:' + FP;
​
var signOptions = {
  iat: Date.now(),
  iss: `${accountID}.${username}.${publicKeyFingerprint}`,
  sub: `${accountID}.${username}`,
  exp: Date.now() + 1000 * 60 * 60
};
var token = jwt.sign(signOptions, privateKey, { algorithm: 'RS256' });
console.log("\nToken: \n\n" + token);
```

### 3. Generating REST API Request Parameters

After gathering the necessary connection information, you need to format it for the [Submit request to execute SQL statement](https://docs.snowflake.com/en/developer-guide/sql-api/submitting-requests):

| **Parameters**  | **Description**                                              |
| :-------------- | :----------------------------------------------------------- |
| Request Method  | POST                                                         |
| URL             | Based on the account ID, formatted as: `https://{Account_ID}.snowflakecomputing.com/api/v2/statements` |
| Request Headers | Set the authentication method, token, and other necessary headers: `{    "Content-Type": "application/json",    "Authorization": "Bearer <Token>",    "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",    "accept": "application/json",    "User-Agent": "From EMQX" }` |
| Request Body    | The body is in JSON format and includes database configuration, SQL insertion statement, and binding parameters: `{    "database": "IOT_DATA",    "statement": "INSERT INTO IOT_DATA.PUBLIC.RenewableEnergyData (id, city, model, regionID, type, ratedPower, timestamp, powerOutput, windSpeed, solarRadiation, rotationSpeed) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);",    "timeout": 60,    "bindings": {        "1": {            "type": "TEXT",            "value": "<Value of ID>"        },        "2": {            "type": "TEXT",            "value": "<Value of City>"        },        ...    } }` |

With these preparations complete, the next step is to configure the rule engine in EMQX to integrate with the data.

## Configuring Data Integration on EMQX

As of EMQX Enterprise v5.7.1, native Snowflake data integration is still under development. To write data, you need to use EMQX’s [HTTP Action](https://docs.emqx.com/en/enterprise/v5.7/data-integration/data-bridge-webhook.html) combined with the [Snowflake REST API](https://docs.snowflake.com/en/developer-guide/sql-api/index).

![Diagram illustrating the setup of EMQX HTTP Action with Snowflake REST API](https://assets.emqx.com/images/cbdb29e5a8c9790204bee648429e3354.png)

- Open and log in to the EMQX Dashboard at [http://localhost:18083](http://localhost:18083/) using a browser. The default username and password are admin and public.
- Navigate to the **Integration → Rules** page, and click the + **Create** button in the upper right corner to enter the rule creation page.
- Use the following rule SQL to receive messages from the virtual plants. You can also modify the SQL to utilize EMQX’s [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.7/data-integration/rule-sql-builtin-functions.html):
  
  ```sql
  SELECT
    payload
  FROM
    "mqttx/simulate/Solar-Wind-Power-Plant/+"
  ```

- Add an HTTP action to the rule: Click the **+ Add Action** button on the right side, select **HTTP Server** for Action Type, and fill in the following parameters:

   1. **Name**: Enter a name.
   2. **Connector**: Click the + button on the right, fill in the URL and request headers from the **Generate REST API Request Parameters** section, and complete the creation.
   3. **Request Body**: This should be in JSON format, specifying the database, Snowflake SQL insertion statement, and binding parameters. Use the ${field} syntax to extract the processing result of the rule SQL for data insertion.

  ```json
  {
    "statement": "INSERT INTO IOT_DATA.PUBLIC.RenewableEnergyData (id, city, model, regionID, type, ratedPower, timestamp, powerOutput, windSpeed, solarRadiation, rotationSpeed)\n  VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);",
    "timeout": 60,
    "database": "IOT_DATA",
    "bindings": {
     "1": { "type": "TEXT", "value": "${payload.id}" },
     "2": { "type": "TEXT", "value": "${payload.city}" },
     "3": { "type": "TEXT", "value": "${payload.model}" },
     "4": { "type": "TEXT", "value": "${payload.regionID}" },
     "5": { "type": "TEXT", "value": "${payload.type}" },
     "6": { "type": "FIXED", "value": "${payload.ratedPower}" },
     "7": { "type": "TEXT", "value": "${payload.timestamp}" },
     "8": { "type": "FIXED", "value": "${payload.powerOutput}" },
     "9": { "type": "FIXED", "value": "${payload.windSpeed}" },
     "10": { "type": "FIXED", "value": "${payload.solarRadiation}" },
     "11": { "type": "FIXED", "value": "${payload.rotationSpeed}" }
    }
  }
  ```

- Leave the other parameters empty, create the action, and save the rule.

With EMQX configured for data integration, running the MQTTX CLI simulation script will send the solar and wind plants data to EMQX, which will then write them to Snowflake.

Next, configure Snowflake to analyze and visualize these data.

## Data Analysis and Visualization in Snowflake

First, let's verify if these data have been successfully written to Snowflake.

- Log in to the Snowflake console, navigate to **Projects → Worksheets**, and create a new SQL worksheet.
- Select the IOT_DATA database, enter the following SQL query, and execute it to ensure that the RenewableEnergyData table contains data:

```sql
select count(*) from iot_data.public.renewableenergydata
```

![Executing SQL query in Snowflake](https://assets.emqx.com/images/413ddeb54b76383a30571129ac38a353.png)

Next, you can add visual charts on the **Projects → Dashboards** page to analyze and present the data through custom SQL queries. Here are a few examples:

- **Get Instantaneous Power Generation**: To view the current power generation status in real-time, query the most recent data. For instance, use an SQL query to obtain the latest wind and solar power generation data and display the results in a chart. This helps you quickly understand the current power generation status and promptly address any abnormalities.
- **Get Historical Power Generation**: To analyze power generation over a specific period, query and summarize historical data. For example, use an SQL query to retrieve power generation data from the past day, week, or month, and generate corresponding charts. This helps you understand power generation trends, evaluate equipment performance, and develop optimization strategies.

Using these visualizations, you can analyze and present power generation data more intuitively. This improves the accuracy and efficiency of your decision-making.

![Sample power generation data visualization in Snowflake](https://assets.emqx.com/images/b6b92046416a9a34e277643aeda3c0d2.png)

Additionally, tools like Snowflake's [AI/ML Studio](https://docs.snowflake.com/guides-overview-ai-features) can be used for anomaly detection, data classification, and training on historical data. This facilitates automated processing of regional and seasonal power generation data, enabling the prediction of future power generation trends.

## Conclusion

This blog explores the integration of MQTT with Snowflake to create a comprehensive management and scheduling system for wind and solar renewable energy. By using EMQX as a real-time [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and importing data seamlessly into Snowflake, we have developed an end-to-end solution for capturing and analyzing energy production data.

This integration provides a scalable platform for monitoring power data, enabling real-time tracking of power generation and equipment status. Leveraging EMQX's high reliability and Snowflake's robust data warehouse and analytics capabilities, we can optimize power allocation using data and AI-driven production forecasting.

EMQ offers a full suite of solutions including data collection, edge computing, cloud access, and AI technology tailored for the energy and power industry. By utilizing a unified MQTT platform and cloud-edge data intelligence solutions, EMQ helps build a smart and stable power and energy IoT ecosystem. This approach optimizes energy usage, enhances efficiency and sustainability, reduces carbon emissions, and fosters innovation within the energy sector.

For more information:

- [MQTT Platform for Energy & Utilities Industry](https://www.emqx.com/en/solutions/industries/energy-utilities) 
- [EMQX Enables Smart Energy Storage with Real-Time Data Collection and Cloud-Edge Collaboration](https://www.emqx.com/en/blog/emqx-enables-smart-energy-storage)

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
