eKuiper 团队于年前发布了 [1.8.0 版本](https://www.emqx.com/zh/blog/ekuiper-v-1-8-0-release-notes)，并在 2 月对该版本的文档进行了完善，同时通过 EMQ Demo Day 直播帮助用户更进一步了解新功能的使用场景（直播观看地址：[LF Edge eKuiper 1.8 新功能演示_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1EY411e7F8/?buvid=Z743CB7E8E1ECB59410986CA49384DBE7821&is_story_h5=false&mid=CwImi%2BEmNTsMt%2B0d9Tdk0A%3D%3D&p=1&plat_id=114&share_from=ugc&share_medium=iphone&share_plat=ios&share_session_id=079C2455-B50E-4747-A3A1-3F627450E506&share_source=WEIXIN&share_tag=s_i&timestamp=1677491216&unique_k=dWkMQvr&up_id=522222081&vd_source=266374e1050bf3ceddfca288be7c5f15) ）。

我们也开始了下一个版本 1.9.0 的开发，该版本将是一个较小的迭代版本，主要目标是实现与工业协议网关软件 Neuron 的多实例连接。目前主要完成了功能调研和规划工作，以及新功能 Python 插件虚拟环境支持的开发。

此外，本月还发布了 1.8.1 版本，包含导入 Portable 插件以及 Flow Editor 等 bug 修复，详情请查看：[https://github.com/lf-edge/ekuiper/releases/tag/1.8.1](https://github.com/lf-edge/ekuiper/releases/tag/1.8.1) 。

## Python 插件虚拟环境支持

虚拟环境是 Python 开发中常用的技术，对 Python 的依赖性管理很有帮助。Anaconda 或 Miniconda 是最流行的 Python 环境管理器之一。[conda](https://conda.io/projects/conda/en/latest/index.html) 软件包和环境管理器包含在所有版本的 Anaconda®、Miniconda 和 Anaconda Repository 中。eKuiper 支持使用 conda 环境运行 Python 插件。

使用该功能之前，用户需要确保 eKuiper 运行的主机或者 Docker container 中已配置好 Python 的 conda 虚拟环境。使用该功能与普通 Python 插件相同，只是需要在插件打包阶段，编写 JSON 元文件时指定使用的虚拟环境名称即可，如下示例文件所示。

```
{
    "version": "v1.0.0",
    "language": "python",
    "executable": "pysam.py",
    "virtualEnvType": "conda",
    "env": "myenv",
    "sources": [
      "pyjson"
    ],
    "sinks": [
      "print"
    ],
    "functions": [
      "revert"
    ]
  }
```

在本例中，我们指定了虚拟环境类型 `virtualEnvType` 为 `conda`，虚拟环境名称为 `myenv`。这样插件运行时将会运行在 conda 的 myenv 环境中。目前，虚拟环境类型仅支持 conda 。

## 即将到来

下个月我们将主要进行 1.9.0 版本其他功能的开发，期望在下月底或稍晚与 Neuron 协同发布。在这个版本中，我们将修改与 Neuron 的连接方式，实现多实例连接。此外，我们将开发其他功能，包括局部配置批量下发功能，方便多实例的配置管理；Http Pull Source 支持动态 token，以支持接入更多的 HTTP 数据源等。敬请期待。
