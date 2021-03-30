## 摘要

本实验以 EMQ X MQTT Broker 为例，指导用户快速完成物联网消息服务器搭建。

##  实验属性

- 难易程度：初级
- 实验时长：120分钟

## 实验目标与基本要求

使用户掌握 EMQ X 安装流程，了解 EMQ X 基本配置以及启动方式，通过自行选择并下载安装包完成安装、启动、测试步骤。

## 实验摘要

1. 选择并下载安装包
2. 安装并启动 EMQ X
3. 接入使用 EMQ X

## 实验步骤

### 1. 领取代金券，购买测试云服务器

领券链接：[点击前往领取100元代金券](https://account.huaweicloud.com/usercenter/#/getCoupons?activityID=P2008240947144281K3W0ZA1RV2D2C&contentID=PCP2008240946236230RRLRX51AFLQE1)

<div style="width: 100%; margin: 10px 0; width: 260px;padding: 6px;border: 1px solid #34c388;">
<div style="font-size: 12px">领券失败？微信添加 EMQ 小助手处理</div><img src="https://static.emqx.net/images/f78798015e84cc54e66e14ba7a8e854d.jpg" style="width: 80px"/>
</div>

购买云服务器：[https://www.huaweicloud.com/product/ecs.html](https://www.huaweicloud.com/product/ecs.html) 此处选择ubuntu服务器。



### 2. 选择并下载安装包

#### 2.1 安装方式

对于 Linux 发布，EMQ X 提供两种方式的安装。

一是基于各 linux 发布的安装包。用安装包安装 EMQ X 以后，可以方便的使用系统管理工具来启停 EMQ X 服务。

二是使用 zip 压缩打包的通用包。安装 zip 包只需解压 zip 文件即可。使用 zip 包可以实现在同一个系统下安装多套 EMQ X。在开发/实验室环境下使用 zip 包安装 EMQ X 非常实用。

#### 2.2 下载安装包

进入【实验操作桌面】，打开火狐浏览器，输入 https://www.emqx.io/cn/downloads 选择 EMQ X Broker 或 EMQ X Enterprise，选择 EMQ X 版本与操作系统类型。

此实验中选择 EMQ X Broker 最新版 4.1.1，操作系统选择 Linux > Ubuntu 16.04，选择安装包类型为 zip，点击下载按钮，将文件保存至默认下载目录。

![img](https://static.emqx.net/images/63fe106f29f0eea21bedc4602677b5e4.png)            



### 3. 安装并启动 EMQ X

#### 3.1 解压安装包

鼠标双击云桌面上的 Xfce 终端图标，打开命令行，使用 cd /home/user/Downloads/ 命令切换至下载目录，使用 unzip emqx-ubuntu16.04-v4.1.1.zip 命令解压安装包。

解压之后会得到 ./emqx 文件夹，进入该文件夹即可。



#### 3.2 启动 EMQ X

使用 ./bin/emqx start 命令启动 EMQ X，启动成功后使用 ./bin/emqx_ctl status 或 ./bin/emqx ping 命令查看启动状态：

```
./bin/emqx start
emqx 4.1.1 is started successfully!

./bin/emqx_ctl status
Node 'emqx@127.0.0.1' is started
emqx 4.1.1 is running
```

运行中的 EMQ X 可以使用 ./bin/emqx stop 命令停止：

```
./bin/emqx stop
ok
```

#### 3.3 Console 模式启动

使用 console 模式启动可以获得 EMQ X 启动信息，日志将在控制台输出，非常适用于初次启动排错、开发调试等。

使用 ./bin/emqx console 命令即可以 Console 模式启动 EMQ X：


```
 ./bin/emqx console

Starting emqx on node emqx@127.0.0.1
Start http:management listener on 8081 successfully.
Start http:dashboard listener on 18083 successfully.
Start mqtt:tcp listener on 127.0.0.1:11883 successfully.
Start mqtt:tcp listener on 0.0.0.0:1883 successfully.
Start mqtt:ws listener on 0.0.0.0:8083 successfully.
Start mqtt:ssl listener on 0.0.0.0:8883 successfully.
Start mqtt:wss listener on 0.0.0.0:8084 successfully.
EMQ X Broker 4.1.1 is running now!
Eshell V10.7.1  (abort with ^G)
(emqx@127.0.0.1)1> 
```


### 4. 接入使用 EMQ X

#### 4.1 使用 EMQ X Dashboard

EMQ X 提供了 Dashboard 以方便用户管理设备与监控相关指标。通过 Dashboard，你可以查看服务器基本信息、负载情况和统计数据，可以查看某个客户端的连接状态等信息甚至断开其连接，也可以动态加载和卸载指定插件。

除此之外，EMQ X Dashboard 还提供了规则引擎的可视化操作界面，同时集成了一个简易的 MQTT 客户端工具供用户测试使用。



EMQ X 正常启动的情况下，在火狐浏览器中输入网址 http://localhost:18083 即可访问 EMQ X Dashboard，默认的用户名和密码分别为 admin public。

![img](https://static.emqx.net/images/ddf787942c7abb501f605035462751fc.png)            

#### 4.2 建立 MQTT 连接

登录 Dashboard 后，依次点击 工具 -> WebSocket 打开 WebSocket 测试工具，在该页面输入 MQTT 连接信息，点击连接按钮即可连接至 EMQ X。

![img](https://static.emqx.net/images/b90d28808208c4d3e691c44bab19c17f.png)            



输入待订阅的主题并进行订阅，输入主题、消息进行发布、选择 QoS 发布一条消息，消息发出之后，订阅消息列表应当能立即收到发出的消息。

![img](https://static.emqx.net/images/f826919c580d8d3d7c1f6b87e29e4cf4.png)            



#### 4.3 结束实验

关闭浏览器，按照 3.2 中的步骤停止 EMQ X 完成实验。

---
**添加小助手微信，进入 EMQ & 华为云技术交流群，与更多技术牛人深入交流、共同成长。**
![EMQ X 微信小助手](https://static.emqx.net/images/237cdd1601705d7fc794253c757c1d65.png)