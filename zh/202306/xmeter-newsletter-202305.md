本月，XMeter 团队发布了基于容器化部署的企业版 3.3.0 版本（原规划为 3.2.5 版本），该版本支持 XMeter master 服务、asteroid 服务、压力机 DCM 及各依赖组件以容器方式运行，并使用 docker-compose 对各容器服务进行编排管理，降低了 XMeter 企业版的安装部署难度，保证了 XMeter 企业版运行时的健壮性。同时，还实现了使用 Terraform 部署到阿里云，助力用户在公有云上快速搭建 XMeter 企业版环境。此外，XMeter 3.3.0 还包含了一系列功能优化和问题修复。

## 使用 docker-compose 安装部署 XMeter 企业版

XMeter 企业版服务及各依赖组件的编排管理已封装在若干个 docker-compose.yml 文件中。如果希望在内网环境中或非阿里云的公有云环境上安装 XMeter 企业版，可以通过 [xmeter@emqx.io](mailto:xmeter@emqx.io) 联系我们获取安装文件包，提前准备好测试所需服务器和网络环境后，将安装包上传至目标服务器，配置必要的环境变量参数（如目标服务器ip/host、邮件服务器信息等），并执行部署脚本，以启动 docker-compose 管理下的各个容器服务。相关容器在几分钟内即可完成部署并开始运行，用户即可登录用户或管理员控制台进行 XMeter 的使用。

![使用 docker-compose 安装部署 XMeter 企业版](https://assets.emqx.com/images/d4030c0cd97d8ea984040d2cf07b366e.png)

3.3.0 版本企业版将基于给 XMeter 服务配置的 HTTPS ssl 证书颁发许可证。试用阶段，可以使用自带的自签名 ssl 证书进行体验，系统将自动生成为期一个月的试用许可证。试用期之后，或重要环境上，建议用户使用权威机构签发的 ssl 证书，并联系我们获取正式的 XMeter 企业版许可证。

## 使用 Terraform 安装部署 XMeter 企业版

为了进一步简化公有云用户搭建 XMeter 企业版的步骤，3.3.0 还发布了适用于阿里云的 Terraform 部署方案。用户使用我们提供的 Terraform 脚本及 XMeter 安装包，在配置文件中指定阿里云所需创建的资源后，执行 terraform apply，即可一键完成测试所需云资源的远程创建及其上 XMeter 相关服务的部署。整个过程将于 1 个小时内完成（网络带宽条件会对部署安装时间造成一定影响）。

![使用 Terraform 安装部署 XMeter 企业版 1](https://assets.emqx.com/images/17cb623b0ba9be156154ea5f12660079.png)

![使用 Terraform 安装部署 XMeter 企业版 2](https://assets.emqx.com/images/bb5092a9401721450ecabdd1c8f139d8.png)

后续我们还将陆续支持 Terraform 方式部署 XMeter 企业版到 AWS、华为云等多个云厂商，敬请关注。

## 其他优化与修复

3.3.0 企业版中比较显著的优化和修复有：

- 通过指定相关配置项，测试报告中支持使用秒或毫秒为单位展示响应时间，以满足不同时间精度的需求。
- 测试明细数据的响应时间增加 50 百分位、75 百分位、95 百分位、99 百分位的支持，并提供 grafana 图表以查看这些百分位数据，以更全面地展示响应时间的分布情况。
- 错误日志的计数限制从原来的按日志数量统计，改为按日志种类统计，避免日志数较多时无法查看到后面的错误情况。
- 测试报告选择需要展示的自定义事务/请求时，支持按名称筛选，以快速定位所需展示的内容。
- 修复计划任务无法正确选择时间的问题。
- 修复部分情况下总吞吐量折线图显示不正确的问题。
- 修复阈值告警邮件发送频率的问题。
- 修复部分模板无法导入测试体配置文件的问题。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html%23%2Fproducts" class="button is-gradient px-5">开始试用 →</a>
</section>
