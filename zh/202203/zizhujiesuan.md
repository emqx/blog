本文系 EMQ&Intel 联合举办的首届“中国物联网数据基础设施最佳案例评选大赛“个人开发者赛道一等奖作品。

项目作者：霍宏亮



## 项目简介

智能餐饮自助结算系统是一个由称重系统、显示屏、自助扫码盒和 Intel CPU 组成的智能自助结算终端，将装有菜品的托盘放到秤盘上结算，显示屏会向就餐顾客显示本次饭菜菜品的份数、金额，顾客可以通过微信支付宝扫描、刷脸或校园卡员工卡进行自助结算，整个自助收银流程不到两秒钟，充分展示了就餐的智能化、人性化、透明化。

项目地址：[https://github.com/roushanburou/zizhujiesuan](https://github.com/roushanburou/zizhujiesuan)

## 技术框架

**架构图**

![架构图](https://assets.emqx.com/images/aa05f32fab534c0741b864a559717bbf.png)

1. 在采购来的自助结算平台安装 USB 高清摄像头，用于采集菜品图片。

   ![image1.png](https://assets.emqx.com/images/af8f1233dbe7478af2b43f456c152360.png)

2. 将采集到的数据集转化为 TensorFlow 格式的 tfrecoed。

   ![image2.png](https://assets.emqx.com/images/0a8ee482f0ea103fd0c4972cb046484a.png)

3. 本次选用的是 TensorFlow2 下的预训练模型 ssd_mobilenet_v2，因为看到 OpenVINO 在最新的版本不再支持 TensorFlow1.X 版本，所以采用 TensorFlow2.X 版本去做。

4. 训练完成后，将模型通过 mo.py 文件转化为 IR 文件

   ![image3.png](https://assets.emqx.com/images/423141e37c33667c23d6404e613c90c5.png)


   这次发现 OpenVINO 更新了 PaddlePaddle 模型转换，后期有机会可以试一试。在生成 IR 文件后，根据 OpenVINO 基于目标检测提供的object_detection_sample_ssd.py 自己编写了代码推理模板进行推理，然后把命令和结果封装成 Python 脚本。 

5. 编写桌面程序，安装 IronPython 库，嵌入 Python 脚本。这款结算平台的称重是串口通信，在调通波特率后顺利解析出协议，通过电子秤感应程序是否需要进行识别，这样免去了需要实时检测的问题，整体效果如下：

![image4.jpeg](https://assets.emqx.com/images/f696df1eaeec0ed3ba7105aa68be8b19.jpeg)


实际测试大概两秒左右，效果非常不错。识别后由客户点击结算，结算完成后自助打印小票。

## 使用说明

将装有菜品的托盘放到秤盘上结算，显示屏会向就餐顾客显示本次饭菜菜品的份数、金额，顾客可以通过微信支付宝扫描，刷脸或校园卡员工卡自助结算，点击结算会有小票打印。

## 作者寄语

在餐饮这样消费时段集中的行业中，结算速度决定了企业盈利情况。基于 OpenVINO 的智能自助餐饮结算系统可以快速准确识别整盘菜品种类以及数量，软件自动完成金额汇总，不需要人工进行每一个菜品的计价，辅以充值卡、微信、支付宝等快捷支付手段，可以实现结算台前无排队。

智能餐饮自助结算结合了物联网技术，将数据通过 MQTT 汇聚至公有云平台，便于后期制作大数据分析系统。通过大数据分析，可实时掌控柜台菜品的数量，及时补充菜品，还可根据每个菜品的销售状况，实时对后厨的制作口味做出调整；也可跟踪长期顾客的饮食喜好，结合健康营养管理系统，对顾客热量摄入提供健康建议，为客户提供更多价值。
