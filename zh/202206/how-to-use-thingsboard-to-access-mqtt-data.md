## 简介

[ThingsBoard](https://thingsboard.io/) 是用于数据收集、处理、可视化和设备管理的开源物联网平台。它支持通过 [MQTT](https://www.emqx.com/zh/mqtt)、[CoAP](https://www.emqx.com/zh/blog/connecting-coap-devices-to-emqx) 和 HTTP 等协议实现设备连接，并支持云和私有部署。使用丰富的服务器端 API，以安全的方式提供、监测和控制您的物联网实体，定义您的设备、资产、客户或任何其他实体之间的关系。以可扩展和容错的方式收集和存储遥测数据，用内置或定制的部件和灵活的仪表盘来可视化您的数据，并且可以和您的客户共享 Dashboard 界面。

本文将使用 ThingsBoard Cloud 结合 [EMQ](https://www.emqx.com/zh) 旗下的全托管 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)，介绍如何在 ThingsBoard 中集成第三方 MQTT Broker 并自定义配置 Dashboard UI 接入 MQTT 数据。

## 准备

由于我们使用的是 ThingsBoard Cloud ，所以我们无需下载安装，只需要访问 [https://thingsboard.cloud/signup](https://thingsboard.cloud/signup) 进行注册登录便可获得相关服务。除了使用 ThingsBoard 云服务之外，用户也可以选择私有部署进行[下载安装](https://thingsboard.io/docs/user-guide/install/installation-options/)。

> 注意：只有专业版具备 [平台集成](https://thingsboard.io/docs/user-guide/integrations/) 功能，所以需要使用 ThingsBoard Cloud 或者是下载部署专业版。

本文使用全托管的 MQTT 消息云服务 - EMQX Cloud 创建第三方 Broker。[注册登录 EMQX Cloud](https://www.emqx.com/zh/signup?continue=https%3A%2F%2Fcloud.emqx.com%2Fconsole%2Fdeployments%2F0%3Foper%3Dnew) 控制台，新建部署，一个部署即为一个 Broker。新用户同时拥有 14 天基础版和 14 天专业版免费试用机会。

EMQX Cloud 提供 VPC 对等连接和 REST API 等功能，且具备强大灵活的数据集成能力，方便用户与其现有云服务资源对接。提供一站式运维代管，可以节省大量的时间和人力成本，让企业专注在交付更有价值的业务系统。

## 集成

### 使用 EMQX Cloud

1. 获取连接地址和端口。等待部署状态为运行中，进入部署概览页面，找到连接地址和 `mqtt` 协议对应的连接端口，后续在 ThingsBoard 中添加集成时我们需要用到它们。

   ![MQTT Cloud 部署信息](https://assets.emqx.com/images/057550177ae242bda442f0565588d28d.png)

2. 添加认证信息。进入【认证鉴权】->【认证】中添加一套用户名密码用于后续集成中的认证。

   ![MQTT Cloud 添加认证信息](https://assets.emqx.com/images/a63c974060bc75cf4215a52745d8e64c.png)

### 配置 ThingsBoard

1. 在【Data converters】中新增一个 `Uplink` 类型的数据转换器。该上行数据转换器的作用是解析传入消息的有效负载并将其转换为 ThingsBoard 使用的格式。

   1. 填写名称，类型选择 `Uplink` ，开启 Debug 模式并将下述解析脚本复制粘贴到解析方法中。

      ```
      // Decode an uplink message from a buffer
      // payload - array of bytes
      // metadata - key/value object
      
      // decode payload to json
      var payloadJson = decodeToJson(payload);
      var result = {
         deviceName: payloadJson.deviceName,
         attributes: {
             model: 'Model A',
             serialNumber: 'SN111',
             integrationName: metadata['integrationName']
         },
         telemetry: {
             temperature: payloadJson.temperature,
             humidity: payloadJson.humidity,
         }
      };
      
      // Helper functions
      function decodeToString(payload) {
         return String.fromCharCode.apply(String, payload);
      }
      function decodeToJson(payload) {
         // covert payload to string.
         var str = decodeToString(payload);
      
         // parse string to JSON
         var data = JSON.parse(str);
         return data;
      }
      
      return result;
      ```

   2. 点击测试按钮，进入测试页面，对刚刚的解析脚本进行测试。输入 JSON 格式的 payload 内容进行测试，可以看到测试输出数据中包含输入的设备名称、温度和湿度数据。然后点击保存按钮，回到刚刚的配置页面。

      ![ThingsBoard Data converters](https://assets.emqx.com/images/b5610f6bdab6a52f0c50d83afa594aca.png)

   3. 点击添加按钮然后便成功添加一个 `Uplink` 类型的数据转换器。

      ![ThingsBoard Uplink](https://assets.emqx.com/images/b2f4714da99e784fa63886580e92b4db.png)

2. 进入【Integrations】新增 EMQX Cloud 部署集成。

   1. 点击添加集成，输入名称并选择上述第 1 步中成功添加好的上行数据转换器 `MQTT-Uplink` 。之后复制粘贴 EMQX Cloud 部署概览页面中的连接地址和 `mqtt` 协议对应的端口号。

      ![ThingsBoard Integrations](https://assets.emqx.com/images/11b6388d3a690b63e6dabac9b353c5f4.png) 

   2. 添加认证信息。由于 EMQX Cloud 部署均默认开启认证，所以我们可以选择基础类型的认证，然后填入在 EMQX Cloud 认证页面中添加好的用户名和密码。点击测试连接，可以看到右下角弹出连接已经成功建立的信息提示，表示已经成功和 EMQX Cloud 部署集成。最后输入一个过滤主题 `/test/integration/emqxcloud`（后续模拟测试时，我们需要用这个主题去发布一条消息），最后点击添加按钮，便成功添加好了与 EMQX Cloud 部署的集成。

      ![ThingsBoard 添加认证](https://assets.emqx.com/images/2724e29ed7c20a212b1943fb1af5e7ef.png) 

## 集成测试

在完成上述集成配置之后，我们使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 来模拟一个设备测试和验证该功能的有效性。

1. 使用 MQTT X 作为一个设备连接到 EMQX Cloud 部署。

   ![MQTT 连接](https://assets.emqx.com/images/a68a6f4bf8c5a820ddeae0a8cc0561a1.png)
    
2. 成功建立连接之后，向上述集成时配置的过滤主题 `/test/integration/emqxcloud` 模拟发送一条设备上报的温湿度数据。

   ![MQTT 消息发布](https://assets.emqx.com/images/1473095ddc466a3b4c70a48464dcc4f6.png)
    
3. 进入 ThingsBoard 中的设备组下的全部菜单中，可以看到这里已经显示了我们刚刚模拟的设备名称和温湿度数据。说明已经在 ThingsBoard 中成功集成 EMQX Cloud 部署。在 Integration with EMQX Cloud 集成详情页面中的 【Events】和【Relations】中也可以看到刚刚的模拟数据的相关信息。

   ![ThingsBoard MQTT](https://assets.emqx.com/images/a5cb84135b42574037545323f5d9f9cc.png)
    

## 自定义 Dashboard 接入 MQTT 数据

1. 添加一个新的 dashboard。

   ![MQTT Dashboard](https://assets.emqx.com/images/20e58d1179dc986cb01f4cf4770e0eec.png)
    
2. 打开 dashboard 点击右下角橙色的编辑图标，然后进行图中所示的操作新增一个 [别名](https://thingsboard.io/docs/pe/user-guide/ui/aliases/)（定义将使用实体的数据）。过滤类型选择单个实体，类型选择设备并选中上面 MQTT X 模拟的 Device Test 设备。添加完所有的配置信息之后，需要点击右下角的应用图标，否则将无法应用或保存之前已完成好的配置。

   ![MQTT Device](https://assets.emqx.com/images/ed50f4d33df96e8234b2d56a63d176f1.png)

3. 新增一个时间序列表格小组件。

   1. 依旧在刚刚的页面点击右下角橙色编辑图标，进入编辑模式，然后点击新增小组件。

      ![ThingsBoard 新增小组件](https://assets.emqx.com/images/0f5aaf9d830edb87e434d77222002095.png) 

   2. 输入 Cards 进行搜索找到 Timeseries table 并点击进行配置。

      ![ThingsBoard Timeseries table](https://assets.emqx.com/images/154d78106492cb0a924b298e9a0ef01b.png)
       
   3. 配置刚刚选择的表格，实例别名选择上述设置好的别名，然后添加表格的键值，最后点击添加按钮。

      ![ThingsBoard Timeseries table](https://assets.emqx.com/images/ed614116764ac3372bf607912a73f1f6.png)
       
   4. 拖拽调整刚刚新增的表格大小，并且点击橙色勾图标应用按钮。

      ![ThingsBoard Timeseries table](https://assets.emqx.com/images/c479513a6f18c02e969f7ae54be56d72.png)
       
   5. 我们现在回到 MQTT X 改变温度值为 25，湿度为 80，再次发布一条消息，可以看到刚刚配置好的表格中便有了相应的数据。

      ![ThingsBoard Timeseries table](https://assets.emqx.com/images/0d3fa3f604ce7261774bc85e7c66f57a.png)
       
4. 与上面第 3 步类似，我们点击添加小组件，搜索输入 charts ，然后选择 Timeseries Line Chart，进行配置且把实时时间范围改为最近 5 小时。使用 MQTT X 再次发送一条数据，可以看到两个组件中均展示了对应的数据。

   ![ThingsBoard Timeseries Line Chart](https://assets.emqx.com/images/669296e788958c1375bcbc830ee5e2ab.png)


## 总结

至此，我们完成了在 ThingsBoard Cloud 中集成 EMQX Cloud 部署，并且使用 MQTT X 测试验证了集成功能，最后自定义配置了一个简单的 Dashboard 接入展示 MQTT 数据。在实际项目中，我们可以在深入学习了解 ThingsBoard 后，进行更复杂的 Dashboard 配置，能够更加形象具体地实时监控设备的相关数据，并设置告警阀值，接收告警信息并及时作出相应处理。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>


>相关文档推荐：
>
>1. ThingsBoard 官方快速开始帮助文档：[https://thingsboard.io/docs/getting-started-guides/helloworld-pe/](https://thingsboard.io/docs/getting-started-guides/helloworld-pe/) 
>2. EMQX Cloud 入门简介：[https://docs.emqx.com/zh/cloud/latest/quick_start/introduction.html](https://docs.emqx.com/zh/cloud/latest/quick_start/introduction.html) 
>3. ThingsBoard Uplink Data Convert 说明：[https://thingsboard.io/docs/paas/user-guide/integrations/#uplink-data-converter](https://thingsboard.io/docs/paas/user-guide/integrations/#uplink-data-converter) 
>4. 使用 ThingsBoard 告警：[https://thingsboard.io/docs/pe/user-guide/alarms/](https://thingsboard.io/docs/pe/user-guide/alarms/)
