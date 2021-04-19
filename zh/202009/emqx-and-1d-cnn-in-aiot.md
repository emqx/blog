提起物联网（IoT）和人工智能（AI），人们并不陌生。作为当今时代十分热门的科技概念，它们其实都与「数据」有关：IoT 解决了数据从哪里来，AI 则解决了数据去往何方、用于何处。 **一个将两者结合的新概念「AIoT」也应运而生：IoT 通过万物连接与通信为 AI 提供海量数据，AI 则通过对数据的不断学习与分析，将其转化为有效信息，为实际领域提供效用** 。

在本文中，我们将提出 AIoT 的一个简单融合应用：利用 [物联网消息中间件 EMQ X Broker](https://www.emqx.cn/products/broker) 收集液压系统温度传感器数据，并将其转发到一维 [卷积神经网络 (1D CNN)](https://baike.baidu.com/item/%E5%8D%B7%E7%A7%AF%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C) ，利用这一 AI 深度学习的代表算法预测液压系统冷却器状态。

在一维卷积神经网络上，时间将被看做一个空间纬度，每个输出时间步都是利用输入序列在时间维度上的一小段得到的，为此我们可以利用该特性实现时序数据的预测。我们将使用 Python 代码模拟温度传感器时序数据，通过 [MQTT 协议](https://www.emqx.cn/mqtt) 传输到 EMQ X Broker，并利用其灵活的规则引擎将数据转发到 webhook，依据输入的温度传感器时序数据实现当前液压系统冷却器的状态预测。



### 数据集准备

在本文中我们将使用 UCI 机器学习与智能系统中心提供的 [液压系统状态监测数据集](https://archive.ics.uci.edu/ml/datasets/Condition+monitoring+of+hydraulic+systems#)，该数据集是在液压试验台上实验获得。该试验台由一级工作回路和二级冷却过滤回路组成，二级冷却过滤回路通过油箱相连。该系统周期性地重复负载循环 (60秒) ，通过改变四个液压元件（冷却器、阀门、泵和蓄能器）的状态，获取压力、体积流量和温度等过程值。

* 在该数据集中，TS1.txt, TS2.txt, TS3.txt, TS4.txt 分别为 4 个液压系统的冷却器温度传感器以 60 秒一个周期所获取到的温度数据，第一个周期传感器温度数据如下图：

  ![cooler.png](https://static.emqx.net/images/9d0cbe946ed032f18ffcc37ba286c703.png)

* profile.txt 第一列表示当前周期内液压系统冷却器状态

  - 3：接近故障 (close to total failure)
  - 20：低效率 (reduced efficiency)
  - 100：全效率 (full efficiency)

  


### 模型训练

我们将使用一维卷积神经网络(1D CNN) 来实现模型训练，1D CNN 可以很好地应用于温度传感器数据的时间序列分析。在本文中我们使用 [这篇文章](https://towardsdatascience.com/predictive-maintenance-detect-faults-from-sensors-with-cnn-6c6172613371) 中描述的顺序模型来构建一维卷积神经网络，并适当调整数据集以提高预测准确度。

* 一维卷积神经网络模型构建

  ```python
  num_sensors = 4
  TIME_PERIODS = 60
  BATCH_SIZE = 16
  EPOCHS = 10
  model_m = Sequential()
  model_m.add(Conv1D(100, 6, activation='relu', input_shape=(TIME_PERIODS, num_sensors)))
  model_m.add(Conv1D(100, 6, activation='relu'))
  model_m.add(MaxPooling1D(3))
  model_m.add(Conv1D(160, 6, activation='relu'))
  model_m.add(Conv1D(160, 6, activation='relu'))
  model_m.add(GlobalAveragePooling1D(name='G_A_P_1D'))
  model_m.add(Dropout(0.5))
  model_m.add(Dense(3, activation='softmax'))
  print(model_m.summary())
  model_m.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  history = model_m.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.2, verbose=2)
  ```

* 模型分类指标的报告

  从报告中可以看出通过温度数据预测冷却器状态 3 (接近故障)，20 (低效率)，100 (全效率) 准确率分别为 95%，80%，89%。

  ![模型分类指标的报告.png](https://static.emqx.net/images/5455a9027940b7ca82b5b2e3a31b49fa.png)



### 模拟数据输入

在本文中我们将模拟生产环境下冷却器温度传感器数据上报，为此我们将使用 Python 代码读取数据集中温度数据，并通过 MQTT 协议上报到 EMQ X Broker。

在下面代码中我们首先使用 `pandas` 读取数据集中温度数据 ('TS1.txt', 'TS2.txt', 'TS3.txt', 'TS4.txt')，并对数据做简单处理，然后将数据每秒上报到 EMQ X Broker。

```python
import json
import time

import pandas as pd
from paho.mqtt import client as mqtt_client


broker = '127.0.0.1'
port = 1883
topic = "/1dcnn"
client_id = f'1dcnn-client'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def load_data():
    names = ['TS1.txt', 'TS2.txt', 'TS3.txt', 'TS4.txt']
    df = pd.DataFrame()
    for name in names:
        data_file = f'./dataset/{name}'
        read_df = pd.read_csv(data_file, sep='\t', header=None)
        df = df.append(read_df)
    df = df.sort_index()
    df_values = df.values
    df = df_values.reshape(-1, 4, len(df.columns))
    data = df.transpose(0, 2, 1)
    return data


def publish(client):
    data = load_data()
    for x_data in data[-10:]:
        for y_data in x_data:
            t_1, t_2, t_3, t_4 = tuple(y_data)
            msg = {
                't1': round(t_1, 3),
                't2': round(t_2, 3),
                't3': round(t_3, 3),
                't4': round(t_4, 3)
            }
            time.sleep(1)
            result = client.publish(topic, json.dumps(msg))
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
```



### 故障预测

在本文中我们将使用 EMQ X Broker 规则引擎将温度传感器数据转发到 webhook，并通过温度传感器采集的数据，实现对冷却器状态预测。

1. Webhook 代码编写

   ```python
   import asyncio
   import json
   
   import numpy as np
   import uvicorn
   from keras.models import load_model
   from sklearn.preprocessing import StandardScaler
   from starlette.applications import Starlette
   from starlette.background import BackgroundTask
   from starlette.responses import JSONResponse
   
   
   app = Starlette()
   queue = asyncio.Queue()
   model = load_model('./1d-cnn.h5')
   
   
   @app.on_event('startup')
   async def on_startup():
       print('startup webhook')
   
   
   @app.route('/webhook', methods=['POST'])
   async def webhook(request):
       request_dict = await request.json()
       payload = request_dict['payload']
       data = json.loads(payload)
       values = list(data.values())
       if queue.qsize() == 60:
           items = clear_queue(queue)
           task = BackgroundTask(predictive, data=items)
       else:
           task = None
       queue.put_nowait(values)
       record = {'status': 'success'}
       return JSONResponse(record, status_code=201, background=task)
   
   
   async def predictive(data):
       y_label = {
           0: 3,
           1: 20,
           2: 100
       }
       y_status = {
           3: 'close to total failure',
           20: 'reduced efficiency',
           100: 'full efficiency'
       }
       x_test = np.array(data)
       scaler = StandardScaler()
       x_test = scaler.fit_transform(x_test.reshape(-1, x_test.shape[-1])).reshape(x_test.shape)
       x_test = x_test.reshape(-1, x_test.shape[0], x_test.shape[1])
       results = model.predict(x_test)
       msg = "Current cooler state probability: "
       for i, probability in enumerate(results[0]):
           status = y_status[y_label[i]]
           msg += f"{probability * 100:.2f}% {status}({y_label[i]}), "
       print(msg)
   
   
   def clear_queue(q):
       items = []
       while not q.empty():
           items.append(q.get_nowait())
       return items
   
   
   if __name__ == '__main__':
       uvicorn.run(
           app,
           host='127.0.0.1',
           port=8080,
           loop='uvloop',
           log_level='warning'
       )
   
   ```

2. EMQ X Broker 资源创建

   访问 [EMQ X Dashboard](http://127.0.0.1:18083)，登录用户名和密码为 admin, public，点击左侧菜单栏规则 -> 资源，创建资源。

   ![EMQ X Broker 资源创建.png](https://static.emqx.net/images/99dcfe4ec7bd95b60fdcca9348ec72d2.png)

3. EMQ X Broker 规则创建

   ![EMQ X Broker 规则创建.png](https://static.emqx.net/images/d61f17680d6a44d4c8aeeeda230ba537.png)



### 测试

1. 启动 Webhook

   ```bash
   python3 webhook.py
   ```
    ![启动 Webhook.png](https://static.emqx.net/images/d86bf702732060624f3aeb9265fb11eb.png)
   

2. 启动 EMQ X Broker

   ```bash
   ./bin/emqx start
   ```

   ![启动 EMQ X Broker.png](https://static.emqx.net/images/03e52f0053ac31620417dc1bfd3ec174.png)

3. 模拟数据输入

   ```bash
   python publish.py
   ```

   ![模拟数据输入.png](https://static.emqx.net/images/93b1c412d7c31446c1ea72918e770e74.png)

4. 查看液压系统冷却器状态预测结果

   从下图中我们可以看出前五个周期内，通过输入传感器温度预测出当前冷却器状态为接近故障(close to total failure)，这与数据集中给出的冷却器状态一致。

   ![查看液压系统.png](https://static.emqx.net/images/69a8c52cfbaa02be2a99158507875984.png)

5. 分别调整输入数据，查看不同温度下冷却器状态预测结果，并和数据集中实验结果做对比

   * 输入前十个周期内温度传感器数据，查看预测结果并与实验台收集的结果做对比

     > 修改 publish.py 文件中: for x_data in data:  ->  for x_data in data[:10]:

     ![5.1.png](https://static.emqx.net/images/aaa0e92dd30dd0ac29d93f1e8dceabb4.png)

     从上图中我们可以看到预测结果与试验台收集结果一致

   * 选择数据集中状态为 3 接近故障(close to total failure)，20 低效率(reduced efficiency) 的数据作为输入，查看预测结果并与实验台收集的结果做对比

     > 修改 publish.py 文件中: for x_data in data:  ->  for x_data in data[728:737]:

     ![结果做对比.png](https://static.emqx.net/images/0217e0578357e4db236964052d9034a5.png)

     从上图中我们可以看到预测结果与实验台收集结果有一定误差，这也验证了模型分类指标的报告中预测准确性概率。

   * 输入后十个周期内温度传感器数据，查看预测结果并与实验台收集的结果做对比

     > 修改 publish.py 文件中: for x_data in data:  ->  for x_data in data[-10:]:

     
     ![十个周期内温度传感器.png](https://static.emqx.net/images/58f39d793cbc561eba917cc548eb3e39.png)

     从上图中我们可以看到预测结果与试验台收集结果大致一致，但还是存在一定偏差

### 总结

至此我们实现了传感器数据上报，利用 EMQ X 规则引擎实现数据转发，并使用一维卷积神经网络 (1D CNN) 实现了液压系统冷却器故障预测。

在工业各个领域，不论是机械、电子、钢铁，还是制造、橡胶、纺织、化工、食品，液压传动技术都已成为一项基本应用技术。随着现代工业的不断发展，液压系统逐渐向高性能、高精度演进，其可靠性就变得至关重要，液压系统故障的检测与诊断也因此越来越受到重视。利用 AI 与深度学习，通过 IoT 大数据采集与分析对液压系统的状态进行监控，从而实现故障预测，是 AIoT 为传统工业领域带来的新的可能。

而在各领域对液压系统故障预测的实际应用中，为了利用 AI 作出更加精准的预测，需要采集量级更高的时序数据加以分析训练。因此，需要选用性能指标突出且高度稳定可靠的消息中间件以进行海量数据的接入与传输。 **EMQ X Broker 作为一款高并发低延时，支持分布式集群架构的开源 MQTT 消息服务器，支持单机百万连接，无疑可满足该应用场景以及其他更多物联网应用下的数据传输需求** 










