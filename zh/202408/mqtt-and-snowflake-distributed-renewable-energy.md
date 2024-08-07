## 引言

可再生能源如风力和太阳能发电，具有低成本和环保的特性，是未来能源供应的主要方向。然而，这类发电方式存在供应分散、设备数量多、地区分布广等特点。再加上不同地区的季节和天气变化，不确定性极大。

随着社会用电需求的持续增加，如何合理调配电力成为保障供需平衡和最大化新能源发电效益的关键。

本文将介绍如何采用 EMQX 企业版和 Snowflake，帮助用户在复杂的电力供应链中，实现发电设备数据的采集、存储和分析。通过这一集成，准确预测发电容量，从而实现高效的运营。

## 场景介绍

太阳能和风力发电量的预测依赖地理位置、历史的气候信息、运行信息系和发电量数据。本文我们使用 MQTT 客户端工具 MQTTX CLI 的 `simulate` 命令，配合模拟脚本生成多个太阳能和风力发电站 MQTT 状态数据采集上报与客户端（虚拟电站）。

- 虚拟电站将连接到 EMQX 上，周期性生成模拟数据，并向指定 MQTT 主题发布自身状态数据；
- EMQX 在接收到消息后，使用内置的规则引擎和数据集成功能，将其存储到 Snowflake 中；
- Snowflake 保存数据后，在其平台上进行数据分析。

**典型的数据格式如下：**

| **字段名**     | **数据类型** | **说明**                                                    |
| :------------- | :----------- | :---------------------------------------------------------- |
| id             | STRING       | 唯一标识符，用于标识每条数据记录                            |
| city           | STRING       | 城市名，用于标识数据的来源城市                              |
| model          | STRING       | 设备型号，用于标识数据对应的设备型号                        |
| regionID       | STRING       | 区域编号，用于标识设备所在的区域编号                        |
| type           | STRING       | 设备类型，值为 "Wind" 或 "Solar"                            |
| ratedPower     | FLOAT        | 设备的额定功率，单位为千瓦 (kW)                             |
| timestamp      | TIMESTAMP    | 数据记录的时间戳，表示数据生成的具体时间                    |
| powerOutput    | FLOAT        | 实时输出功率，单位为千瓦 (kW)                               |
| windSpeed      | FLOAT        | 风速，仅对风力发电设备有效，单位为米/秒 (m/s)               |
| solarRadiation | FLOAT        | 光照强度，仅对太阳能发电设备有效，单位为瓦特每平方米 (W/m²) |
| rotationSpeed  | FLOAT        | 转速，仅对风力发电设备有效，单位为每分钟转数 (RPM)          |

对应的数据示例如下：

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

## 安装 EMQX 企业版

[EMQX 企业版](https://www.emqx.com/zh/products/emqx)是一款企业级 MQTT 物联网接入平台，能够提供高可靠、高性能的物联网实时数据接入，并实现数据的处理和集成。

请参照[此处](https://docs.emqx.com/zh/enterprise/latest/deploy/install.html)安装 EMQX 企业版。

## 准备 MQTTX 模拟数据

[MQTTX CLI](https://mqttx.app/zh/cli) 是一款强大而易用的 MQTT 5.0 命令行工具，它提供了 `simulate` 命令，可以使用 Node.js 编写模拟脚本，实现预期的模拟消息生成与发布。

1. 创建一个名为 `solar-wind-power-plant.js` 文件，将本章节提供的模拟脚本粘贴进去。您也可以参照[此处](https://mqttx.app/zh/docs/cli/get-started#模拟器)对脚本内容进行修改；
2. 使用 `simulate` 运行脚本，指定脚本路径和模拟的客户端数量：

```bash
mqttx simulate --file ./solar-wind-power-plant.js -c 10
```

该命令的含义如下：

- `--file` 选项指定运行 `./solar-wind-power-plant.js` 脚本文件
- `-c` 选项指定模拟客户端数量为 10 个

您可以根据自己需要，按照[MQTTX CLI 发布命令选项](https://mqttx.app/zh/docs/cli/get-started#发布) 调整客户端数量和消息发布频率。

执行命令后，脚本将建立 10 个客户端连接到 EMQX，并根据场景中定义的数据类型，每个客户端每秒向 `mqttx/simulate/Solar-Wind-Power-Plant/{clientid}` 主题发布一条消息。

您可以使用 MQTTX CLI 的 `sub` 命令订阅主题，验证消息是否正常发布：

```bash
mqttx sub -t mqttx/simulate/Solar-Wind-Power-Plant/+ -v
```

附录：模拟脚本内容。

```js
const store = {
  index: 0
};

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

function getWindPower(hour, faker) {
  if (hour >= 8 && hour < 18) {
    return faker.datatype.float({ min: 900, max: 1100 });
  } else {
    return faker.datatype.float({ min: 600, max: 900 });
  }
}

function calculateWindSpeed(rotationSpeed) {
  // 假设转速和风速之间的线性关系
  return rotationSpeed / 60; // 简单的线性关系
}

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

function calculateSolarRadiation(powerOutput) {
  // 假设功率和光照强度之间的线性关系
  return powerOutput * 50; // 简单的线性关系
}

function generator(faker, options) {
  const clientid = options.clientid;
  const currentTimestamp = Date.now(); // 使用当前时间
  const currentDate = new Date(currentTimestamp).toISOString().split('T')[0];

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
      isCloudy: faker.datatype.boolean(0.3), // 30% 概率是阴天
      powerOutput: 0,
      windSpeed: deviceType === 'Wind' ? null : 0,
      solarRadiation: deviceType === 'Solar' ? null : 0,
      rotationSpeed: deviceType === 'Wind' ? faker.datatype.float({ min: 0, max: 1500 }) : null
    };
  }

  const data = store[clientid];
  const hour = new Date(currentTimestamp).getHours();

  // 新的一天时，重新确定是否是阴天
  if (data.currentDate !== currentDate) {
    data.currentDate = currentDate;
    data.isCloudy = faker.datatype.boolean(0.3); // 30% 概率是阴天
  }

  if (data.type === 'Wind') {
    data.rotationSpeed = faker.datatype.float({ min: 0, max: 1500 });
    data.powerOutput = getWindPower(hour, faker);
    data.windSpeed = calculateWindSpeed(data.rotationSpeed);
  } else if (data.type === 'Solar') {
    data.powerOutput = getSolarPower(hour, data.isCloudy, faker);
    data.solarRadiation = calculateSolarRadiation(data.powerOutput);
  }

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

const name = 'Solar-Wind-Power-Plant';
const author = 'EMQX Team';
const dataFormat = 'JSON';
const version = '0.0.1';
const description = `Solar and wind power plant simulator, mock data generated with current timestamp.
Cloudiness is determined at the start of each day.`;

module.exports = {
  generator,
  name,
  author,
  dataFormat,
  version,
  description,
};
```

## 准备 Snowflake 环境

Snowflake 是一个基于云的数据平台，为数据存储和分析提供高度可扩展且灵活的解决方案。它提供强大的数据仓库功能，适合处理大规模、多源数据。

在物联网领域，Snowflake 可用于存储和分析从设备和传感器收集的大量数据，实现实时数据处理、可视化和洞察。

本章节我们需要准备 Snowflake 环境，完成表的创建和连接信息的获取。

### 1. 创建数据库与数据表

需要在 Snowflake 中创建数据库与数据表，进行上报历史数据的存储。

- 如果您还没有 Snowflake 账户，点击[此处](https://www.snowflake.com/)创建一个；
- 登录 Snowflake 控制台后，左侧菜单点击进入 **Data → Databases** 页面，创建名为 `IOT_DATA` 的数据库；

  ![在 Snowflake 控制台上创建名为 IOT_DATA 的新数据库](https://assets.emqx.com/images/d7589b8e74d9e7d6cad0335a9315cb9a.png)

- 选中 `IOT_DATA` 数据库下的 `PUBLIC` Schema，点击右上角 **Create**，创建用于存储太阳能和风力发电站上报数据的表。

  ![在 Snowflake 控制台上的 IOT_DATA 数据库中的 PUBLIC 模式下创建一个表](https://assets.emqx.com/images/5a434f87e776e423c9642af3fb582428.png)

数据表类型选择 `Standard`，参考场景描述，对应的 Snowflake 建表语句如下：

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

### 2. 准备连接所需信息

本文使用 Snowflake REST API 进行数据写入，以下是请求所需的信息：

| **信息**   | **说明**                                                     |
| :--------- | :----------------------------------------------------------- |
| 用户名     | Snowflake 控制台登录用户名，用于接入与认证。                 |
| 账户 ID    | 用于 REST API 的接入和认证，获取方式参考 [Account identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier)，后续需要用到中划线分隔的账户 ID，例如 `{orgname}-{account_name}`。 |
| 密钥对     | 用于 REST API 的[认证](https://docs.snowflake.com/en/developer-guide/sql-api/authenticating#using-key-pair-authentication)，参考[此处](https://docs.snowflake.com/en/user-guide/key-pair-auth)生成证书，并将其添加到对应的用户下，后续需要使用到证书私钥 `rsa_key.p8` 文件。 |
| 认证 Token | 使用账户信息和证书私钥签发的 JWT Token，用于 REST API 认证中。签发方式参考[此处](https://docs.snowflake.com/en/developer-guide/sql-api/authenticating#using-key-pair-authentication)，下文提供了 Node.js 签发的代码示例。 |

认证 Token Node.js 签发代码示例：

```js
// sql-api-generate-jwt.js.

const crypto = require('crypto')
const fs = require('fs');
var jwt = require('jsonwebtoken');

// 根据实际情况修改以下值

// 证书私钥文件路径
var privateKeyFile = fs.readFileSync('./rsa_key.p8');
// 证书密码（如果有）
var mypassphrase = '';
// 账户 ID，英文字符需要大写
var accountID = "OXTPEXE-LCF92X4";
// 注册用户名，英文字符需要大写
var username = 'XXXXXX'

privateKeyObject = crypto.createPrivateKey({ key: privateKeyFile, format: 'pem', passphrase: mypassphrase });
var privateKey = privateKeyObject.export({ format: 'pem', type: 'pkcs8' });

publicKeyObject = crypto.createPublicKey({ key: privateKey, format: 'pem' });
var publicKey = publicKeyObject.export({ format: 'der', type: 'spki' });
const FP = crypto.createHash('sha256').update(publicKey, 'utf8').digest('base64')
var publicKeyFingerprint = 'SHA256:' + FP;

var signOptions = {
  iat: Date.now(),
  iss: `${accountID}.${username}.${publicKeyFingerprint}`,
  sub: `${accountID}.${username}`,
  exp: Date.now() + 1000 * 60 * 60
};
var token = jwt.sign(signOptions, privateKey, { algorithm: 'RS256' });
console.log("\nToken: \n\n" + token);
```

### 3. 生成 REST API 请求参数

在准备好连接所需信息后，需要将其拼接为[提交执行 SQL 语句的请求](https://docs.snowflake.com/en/developer-guide/sql-api/submitting-requests)：

| **参数** | **说明**                                                     |
| :------- | :----------------------------------------------------------- |
| 请求方法 | POST                                                         |
| URL      | 由账户 ID 决定，格式如下：`https://{Account_ID}.snowflakecomputing.com/api/v2/statements` |
| 请求头   | 需要在请求头中设置认证方式、Token 以及其他必要的请求头：`{  "Content-Type": "application/json",  "Authorization": "Bearer <Token>",  "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",  "accept": "application/json",  "User-Agent": "From EMQX" }` |
| 请求体   | 请求体是 JSON 格式，需要设置数据库、插入 SQL 以及绑定参数：`{  "database": "IOT_DATA",  "statement": "INSERT INTO IOT_DATA.PUBLIC.RenewableEnergyData (id, city, model, regionID, type, ratedPower, timestamp, powerOutput, windSpeed, solarRadiation, rotationSpeed)  VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);",  "timeout": 60,  "bindings": {    "1": { "type": "TEXT", "value": "<ID  的值>" },    "2": { "type": "TEXT", "value": "<City 的值>" },    ...  } }` |

至此，我们已经完成了所有准备工作。接下来，我们需要在 EMQX 配置规则引擎与数据集成来实现。

## 在 EMQX 上配置数据集成

截止 EMQX 企业版 v5.7.1 版本，原生的 Snowflake 数据集成还在开发中，您需要通过 EMQX 的 [HTTP 动作](https://docs.emqx.com/zh/enterprise/v5.7/data-integration/data-bridge-webhook.html) + [Snowflake REST API](https://docs.snowflake.com/en/developer-guide/sql-api/index) 进行数据写入。

![图表说明了使用 Snowflake REST API 设置 EMQX HTTP 操作](https://assets.emqx.com/images/cbdb29e5a8c9790204bee648429e3354.png)

- 使用浏览器打开并登录 EMQX Dashboard [http://localhost:18083](http://localhost:18083/)，默认的用户名密码是 `admin`, `public`；

- 打开 **集成 → 规则** 页面，点击右上角 + **创建** 按钮进入规则创建页面；

- 使用如下规则 SQL，用于接收虚拟电站发送的消息，您也可以修改 SQL，利用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.7/data-integration/rule-sql-builtin-functions.html)进行自定义数据处理：

  ```sql
  SELECT
    payload
  FROM
    "mqttx/simulate/Solar-Wind-Power-Plant/+"
  ```

- 为规则添加 HTTP 动作：点击右侧 **+添加动作** 按钮，动作类型选择 **HTTP 服务器**，为 HTTP 动作填入以下参数：

   1. **名称：**填入任意名称；
   2. **连接器：**点击右侧 + 按钮，填入**生成 REST API 请求参数**章节中的 URL 和请求头，并完成创建；
   3. **请求体：**此处应该为 JSON 格式，指定数据库、插入 Snowflake SQL 语句以及绑定参数。`bindings` 字段中，可以使用 `${filed}` 语法来提取规则 SQL 的处理结果实现数据的插入。

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

- 其他参数留空，创建动作并保存规则。

至此 EMQX 已经配置完成了数据集成，当运行 MQTTX CLI 模拟脚本时，太阳能和风力电站数据将发送到 EMQX，并通过 EMQX 的数据集成写入到 Snowflake 当中。

接下来，我们在 Snowflake 中进行配置，实现数据的分析和可视化展示。

## Snowflake 数据分析与可视化

首先，我们检查数据是否成功写入到 Snowflake 中。

1. 登录 Snowflake 控制台，打开 **Projects → Worksheets** 页面，新建一个  SQL Worksheets；
2. 选中 IOT_DATA 数据库，输入以下 SQL 并执行，可以看到 `RenewableenErgydata` 表中数据条目数量不为 0。

```sql
select count(*) from iot_data.public.renewableenergydata
```

![在 Snowflake 中执行 SQL 查询](https://assets.emqx.com/images/413ddeb54b76383a30571129ac38a353.png)

接下来，可以在 **Projects → Dashboards** 页面添加可视化图表，通过自定义的查询 SQL 实现数据的分析和展示。以下是几个示例：

- **获取瞬时发电量**：可以实时了解当前的发电情况，通过查询最后一次上报的数据来实现。例如，使用 SQL 查询获取最新的风力发电和太阳能发电数据，并将结果展示在图表中。这可以帮助您迅速掌握当前的发电状态，及时发现并处理异常情况。
- **获取历史发电量**：可以分析过去一段时间的发电情况，通过查询并汇总历史数据来实现。例如，使用 SQL 查询过去一天、一周或一个月的发电数据，并生成相应的图表。这可以帮助您了解发电趋势，评估设备性能，并制定优化策略。

通过这些可视化图表，您能够更直观地分析和展示发电数据，从而提高决策的准确性和效率。

![在 Snowflake 中的样本发电数据可视化](https://assets.emqx.com/images/b6b92046416a9a34e277643aeda3c0d2.png)

您还可以通过其他方式，例如 Snowflake [AI/ML Studio](https://docs.snowflake.com/guides-overview-ai-features)，实现异常检测和数据分类，还可以对历史数据进行训练，自动处理发电区域、季节性数据，实现未来发电量趋势的预测。

## 结语

在本文中，我们深入探讨了 EMQX 与 Snowflake 的集成，构建了一个全面的风力和太阳能可再生能源管理与调度系统。通过利用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) 并将数据无缝导入 Snowflake，我们成功实现了一个端到端的解决方案，用于采集和分析能源生产过程中的数据。

这个演示展示了一个专用于监控电力数据的可扩展平台的蓝图，支持实时监控发电数据和设备状态。借助 EMQX 的高可靠性和 Snowflake 强大的数据仓库存储及丰富的分析功能，我们可以通过数据和人工智能驱动的生产预测，实现电力的合理调配。

EMQ 为能源电力行业提供包括数据采集、边缘计算、云接入和 AI 技术在内的完整解决方案，基于统一 MQTT 平台和云边数据智能解决方案，助力构建智能、稳定的电力能源物联网，优化能源使用、提高效率和可持续性、减少碳排放，推进能源行业的革新。

详细解决方案请参见：[智慧能源电力解决方案](https://www.emqx.com/zh/solutions/industries/energy-utilities)

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
