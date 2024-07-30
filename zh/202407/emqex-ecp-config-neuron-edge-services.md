随着工业物联网（IIoT）领域的快速发展，工业现场的设备数量激增，对实时性、可靠性的要求相应提高，传统的集中式管理方式已难以满足工业物联网的部署与维护需求。如何保障大规模设备接入和配置的一致性、可靠性，成为工业自动化与智能化建设的关键。

EMQ 自主研发的工业互联数据平台 EMQX ECP，能够满足工业场景大规模数据采集、处理和存储分析的需求，提供边缘服务的快速部署、远程操作和集中管理等功能，助力工业领域数据互联互通，以数据 + AI 驱动生产监测、控制和决策，实现智能化生产，提高效率、质量和可持续性。

EMQX ECP 为工业企业提供了一套强大的边缘服务配置管理和下发功能，旨在简化配置流程，加快项目部署速度，提高运维效率。在该功能的日常使用中，用户还需要在 NeuronEX 的页面上进行各种配置，如果有多个 NeuronEX，配置的工作量也将相应增加。

本文将详细介绍如何对 NeuronEX 规则模版导入和导出，并在 EMQX ECP 中进行快速配置和管理模版下发。通过高效的边缘服务配置管理，全面提升工业物联网的部署效率。

## NeuronEX 规则模板导入和导出

### 规则导入

- 提前准备一份规则模版如下，保存成rule.json文件。（该文件仅用于本次演示，模版文件后续可以在规则页面导出）。

  ```json
  {
      "Schema": {},
      "Service": {},
      "connectionConfig": {},
      "nativePlugins": {},
      "portablePlugins": {},
      "rules": {
          "sql2log": "{\"triggered\":true,\"id\":\"sql2log\",\"sql\":\"SELECT\\n  *\\nFROM\\n  mysql1\",\"actions\":[{\"log\":{}}],\"options\":{\"debug\":false,\"logFilename\":\"\",\"isEventTime\":false,\"lateTolerance\":0,\"concurrency\":1,\"bufferLength\":1024,\"sendMetaToSink\":false,\"sendError\":true,\"qos\":0,\"checkpointInterval\":300000,\"restartStrategy\":{\"attempts\":0,\"delay\":1000,\"multiplier\":2,\"maxDelay\":30000,\"jitterFactor\":0.1},\"cron\":\"\",\"duration\":\"\",\"cronDatetimeRange\":null}}"
      },
      "scripts": {},
      "sinkConfig": {},
      "sourceConfig": {
          "sql": "{\"sqlserver_config\":{\"indexFields\":[],\"interval\":1000,\"sourceType\":\"stream\",\"templateSqlQueryCfg\":{\"TemplateSql\":\"select * from test\",\"indexFields\":[]},\"url\":\"sqlserver://sa:Change_me@mssqlserver-2019.intgmssqlserver.svc.cluster.local:1433?database=mqtt\"}}"
      },
      "streams": {
          "mysql1": "\n          CREATE STREAM mysql1\n          ()\n          WITH (FORMAT=\"json\", CONF_KEY=\"sqlserver_config\", TYPE=\"sql\", SHARED=\"false\", );\n      "
      },
      "tables": {},
      "uploads": {}
  }
  ```

- 准备一个新的 NeuronEX，登陆后进入数据处理规则页面。

  ```bash
  docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m emqx/neuronex:latest
  ```

- 点击导入规则按钮，上传 rule.json 文件或者将规则模版内容复制上去，点击提交。

  ![导入规则](https://assets.emqx.com/images/a2c402a8b850612df877dd3f7849076b.png)

- 成功后，新的 NeuronEX 上便可以看到导入的规则。

### 规则导出

在数据处理规则页面勾选规则，点击导出规则按钮，便可将规则的模版文件下载下来。后续可用于导入规则或在 ECP 端创建模版。

![处理规则](https://assets.emqx.com/images/3b375309508b9d9e047520836db0f342.png)

## NeuronEX 南向设备导入导出

### 南向设备导入

- 提前准备一份南向设备模版如下，保存成driver.json文件，（该文件仅用于本次演示，模版文件后续可以在南向设备页面导出）。

  ```json
  {
      "nodes": [
          {
              "groups": [
                  {
                      "group": "group1",
                      "interval": 1000,
                      "tags": [
                          {
                              "address": "1!300004#L",
                              "attribute": 4,
                              "decimal": 1,
                              "description": "",
                              "name": "tag1",
                              "precision": 0,
                              "type": 4
                          }
                      ]
                  }
              ],
              "name": "demo",
              "params": {
                  "address_base": 1,
                  "connection_mode": 0,
                  "endianess": 1,
                  "host": "127.0.0.1",
                  "interval": 20,
                  "max_retries": 0,
                  "name": "demo",
                  "plugin": "Modbus TCP",
                  "port": 502,
                  "retry_interval": 0,
                  "timeout": 3000
              },
              "plugin": "Modbus TCP"
          }
      ]
  }
  ```

- 点击数据采集南向设备，点击导入按钮，上传 driver.json文件，该南向设备创建成功。

  ![创建南向设备](https://assets.emqx.com/images/42d682eb0ffac50ad74fddcb80729cf3.png)

### 南向设备导出

在数据采集南向设备页面勾选规则，点击导出按钮，便可将南向设备的模版文件下载下来。后续可用于导入南向设备或在ECP 端创建模版。

## ECP 配置模版管理和下发

ECP 支持创建 NeuronEX 规则或南向驱动的模版，并使用模版将配置下发给其他边缘服务。

### 创建配置模版

以系统/组织/项目管理员的身份登录 ECP，在**边缘配置管理**页面的**配置模版**选项卡中，点击**新增配置模版**按钮。

![新增配置模版](https://assets.emqx.com/images/5faa1df3f08a264c58331a07880d68a3.png)

模版类型支持规则模版和南向驱动模版。模版文件可以从 NeuronEX 的规则或南向驱动页面导出，进行进一步的修改后上传。请注意模版名称需唯一，不与已存在的其他模板重名。

创建模版后，可以对模版进行进一步的编辑，也可以导出模版内容或删除模版。

### 下发配置

在模版**操作**列点击**配置下发**按钮，打开配置下发窗口。

![打开配置下发窗口](https://assets.emqx.com/images/e296526f13774aaedee0c5980fad14e0.png)

在弹出的窗口中，可以对模版内容做必要的编辑。这里的编辑只影响本次下发，不会保存的模版中。

![配置编辑](https://assets.emqx.com/images/44f749160dbf6751e5b148db0d45c80d.png)

点击**下一步**按钮，选择模版要下发到的目标边缘服务。您可以基于边缘服务名称、EndPoint、版本或标签快速定位服务实例，然后点击实例前的复选框快速选择。

![选择边缘服务](https://assets.emqx.com/images/db681b1aedfb9ad203a95dea252dfa3d.png)

点击**执行**按钮，ECP 将把模版下发到指定的目标边缘服务。配置下发结果对话框将实时展示下发的状态。您可在该页面等待片刻后，查看到下发的结果：

- 待配置的实例总数、成功数和失败数。`绿色圆圈`表示执行成功，`红色感叹号`表示执行失败

- 对于下发失败的情况，您可在**原因**列查看失败的原因

  ![查看失败的原因](https://assets.emqx.com/images/253b7fca4e9743153c520fd61468ba37.png)

  如果需要查看模版下发的历史结果，可以在**系统管理**界面的**操作审计**中查找。

  ![查看模版下发的历史结果](https://assets.emqx.com/images/f27b7050104f6e9e878979153e0637c5.png)

## 总结

至此，我们已经完整介绍了 NeuronEX 和 EMQX ECP 边缘服务配置管理与下发的功能，EMQX ECP 作为工业物联网领域的一股变革力量，能够使企业充分发挥其连接的工业资产的潜力。通过简化设备管理，优化配置流程，加速项目部署以及提高运营效率，EMQX ECP 为 IIoT 项目的蓬勃发展铺平了道路，推动创新并将工业进步推向新的高度。

![扫码试用 EMQX ECP](https://assets.emqx.com/images/ee513a055905ba2ba3482aa9b44617df.png)
