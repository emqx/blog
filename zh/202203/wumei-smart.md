本文系 EMQ&Intel 联合举办的首届“中国物联网数据基础设施最佳案例评选大赛“个人开发者赛道二等奖作品。

项目作者：崔学文。


## 项目简介

wumei-smart 是一个简单易用的生活物联网平台，可用于企业搭建私域物联网，或个人学习和搭建自己的智能家居平台，以及实现手机和电脑的监控。项目包含服务端、Web 端、移动端、设备端 SDK 以及手机和电脑端的设备模拟器。

项目地址：[https://github.com/kerwincui/wumei-smart](https://github.com/kerwincui/wumei-smart)

## 技术框架

使用 EMQX 开源版作为消息服务器接入设备，设备通过 MQTT 协议与后端、前端和移动端交互。

认证采用 EMQX 内置的 HTTP 插件对称加密认证。

后端采用 Spring boot；前端采用 Vue；

移动端采用 Uniapp；

数据库采用 MySQL、Redis 和 TDengine；

设备端支持硬件 SDK 生成，例如 ESP32、ESP8266、树莓派等；

设备模拟器采用 Android 和 WPF 框架，不仅能模拟硬件设备，还可以控制和监测电脑、手机。

**框架图**

![框架图](https://assets.emqx.com/images/b06b6256ca212b52aca30ec7854f228b.png)

## 使用说明

**一、系统要求**

JDK >= 1.8

MySQL >= 5.7

Maven >= 3.0

Redis >= 3.0

Node >= 10

EMQX >=4.0 

**二、开发工具**

后端： IDEA、Eclipse

前端： Virtual Studio Code

**三、项目运行**

后端：

1. MySQL 新建 wumei-smart 数据库，导入 Spring boot 中的 SQL 文件
2. 开发工具打开 Spring boot项目，自动安装依赖
3. 编辑 resources 目录下的 application-druid.yml，修改数据库配置信息
4. 编辑 resources 目录下的 application.yml，修改 Redis、MQTT 配置

前端：

1. 安装依赖：执行 npm install 命令。强烈建议不要用直接使用 cnpm 安装，会有各种诡异的 Bug，可以通过重新指定 registry 来解决 npm 安装速度慢的问题。npm install --registry=https://registry.npm.taobao.org
2. 启动项目：执行 npm run dev命令
3. 浏览器打开http://localhost:80访问。(默认账户/密码 admin/admin123）

**四、部署**

后端：

1. 在 Spring boot 项目的 bin 目录下执行 package.bat 打包 Web 工程，生成 war/jar 包文件。spring-boot/ruoyi-admin 模块下 target 文件夹下包含 war 或 jar 文件
2. jar 部署方式：使用命令行执行：java –jar ruoyi.jar 或者执行脚本：spring-boot/bin/run.bat
3. war 部署方式：spring-boot/ruoyi-admin/pom.xml 中的 packaging 修改为 war，放入 tomcat 服务器 webapps

前端：

1. 打包正式环境: npm run build:prod
2. 打包预发布环境: npm run build:stage
3. 构建打包成功之后，会在根目录生成 dist 文件夹，里面就是构建打包好的文件，通常是 .js 、.css、index.html 等静态文件。

**五、使用**

1. 创建产品
2. 产品中新建或导入通用物模型
3. 创建设备
4. 下载项目中的 SDK 示例，或者按照文档自己实现。
5. 完成 SDK 功能开发后，烧录到设备中。

## 作者寄语

物联网大家都熟悉，但是在日常生活中可能很少真正接触和使用物联网设备。甚至很多物联网专业的学生自己要动手做一个可以联网控制的设备也并不容易，一方面是学校的教育和实践有区别，另外一方面国内的物联网平台众多，上手也不容易。很多人对物联网感兴趣想学习，但缺少一个系统项目的实战。很多企业想接入物联网，但缺少一个低成本的方案。

这个项目最初是我自己 DIY 智能家居项目，开源后不断有人关注学习。同时考虑到目前开源的物联网平台上手有一定难度，也不太适合日常生活场景，于是对这个项目进行完善并参与了本次大赛，希望为更多人学习和了解物联网提供帮助。
