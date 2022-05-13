三月， [Neuron](https://neugates.io/zh) 发布了 2.0-beta.2 版本，这个版本包含了 5 个常用的驱动协议以及 License 的验证，每一个驱动都通过连接真实设备进行了测试。Neuron 2.0-beta.2 版本发布后，后续来自的客户新 Driver 需求将在该版本中进行更新。同时，本月还发布了 1.4.2 版本。

## Neuron 2.0-beta.2 新功能概览

- 适配西门子 PLC 的 S7comm 驱动，驱动支持了 int16/uint16/int32/uint32/float/double/bit/string 数据类型，且支持读写 I（输入）O（输出）F（FLAG）T（TIMER）C（COUNTER）DB 数据区域。收发协议数据使用了异步实现，以及支持多个点位一起读写，提高了读写效率。
- 适配欧姆龙 PLC 的 FINS 驱动，驱动支持了 int8/uint8/int16/uint16/int32/uint32/float/double/bit/string 数据类型，且支持欧姆龙 PLC 的内存区域包含 CIO Area、Auxiliary Area、Work Area、Holding Area、Data Memory Area、PV、Completion Flag、Extended Memory。收发协议数据同样使用异步实现，支持多个点位一起进行读写。
- 适配三菱 PLC 的 QnA 3E 驱动，驱动支持了 int16/uint16/int32/uint32/float/double/bit/string 数据类型，且支持三菱 PLC 众多区域的读写，包含 Input、Output、Link、Internal、Special、Latch、Annuncation、Edge、Timer、Retentive、Counter、Data。因此协议版本在协议层面不支持异步收发数据，实现时只能进行同步读写数据。
- 增加了 License 校验，包含校验过期时间、Node 数量以及每个 Node 可配置的 Tag 数量，以及检验授权使用的驱动模块。每个驱动模块独立验证 License。
- 完善优化了交叉编译 CI，缩减了 CI 时间；CI 增加 deb/rpm 类型的包，且使用 systemd 管理 Neuron 进程，发布的包中默认注册了实现的驱动，方便用户安装使用。
- 修复了驱动崩溃，持久化偶发性失效等问题。
- 增加了用户快速使用文档，帮助用户快速使用 Neuron。
- 增加 API 文档，为用户提供 API 使用帮助。
- 增加了驱动配置文档，描述了每个驱动的配置以及一些使用范例。
- Modules 模块 CI 增加单元测试流程。

## Neuron 1.4.2 发布

主要有以下更新：

- 升级 IEC104 第三方库，解决因连不上 IEC104 设备导致的程序异常退出。
- IEC104 修改为总召唤的方式读取数据点位，适配了三峡客户设备。
- 修正页面修改 Object 属性失败的问题。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
