
![Hamler - 面向 IoT&5G 市场的开源函数编程语言](https://static.emqx.net/images/e9ed2864d47bc008960d1da810593b2b.png)

[EMQ](https://www.emqx.io/cn/) 团队很高兴正式向 IoT&5G 市场发布[开源函数编程语言 - Hamler](https://hamler-lang.org/)！

Hamler 是一门构建在 [Erlang](https://www.erlang.org/) 虚拟机(VM)上的 [Haskell](https://www.haskell.org/) 风格的强类型(strongly-typed)编程语言，独特地结合了编译时的类型检查推导，与对运行时高并发和软实时能力的支持。

Hamler 编程语言将赋予行业，尤其是 5G、IoT、云计算和边缘计算等潜力领域，构建下一代高可靠、可扩展、具备软实时支持应用的能力。

## 为什么发布 Hamler？

近十年来，我们一直在开发基于 Erlang/OTP 的软件系统，特别是我们的核心产品可伸缩分布式[开源 MQTT 服务器 - EMQ X](https://www.emqx.io/cn/products/broker)。我们一直认为 Erlang/OTP，尤其是 Beam 虚拟机是工程学的杰作。它具有出色的并发性、分布性和容错性，是少数正确处理高并发和软实时的通用语言平台，是最适合开发 IoT 和 5G 应用的平台之一。

从多年开发 Erlang 程序经验来看，我们一直期待解决两个问题：编译时类型系统与更友好的程序语法。编译时强大的类型系统有助于我们构建更可靠的软件系统；更友好的语法有助于我们创建一个繁荣的开发者社区。

为此学术界和产业界付出了近 20 年的努力。首先是 [Philip Wadler](https://en.wikipedia.org/wiki/Philip_Wadler) 教授和 [Simon Marlow](https://simonmar.github.io/) 在 2000 年前后，为 Erlang 引入了类型标注和 **Dialyzer** 静态类型检查工具。

- Simon Marlow & Philip Wadler (1997): [A practical subtyping system for Erlang](http://homepages.inf.ed.ac.uk/wadler/papers/erlang/erlang.pdf)
- Philip Wadler (2002): [The great type hope](http://homepages.inf.ed.ac.uk/wadler/papers/erlang/erlang-slides.pdf)

2008 年后，产业界有近 20 个项目，不断地尝试解决类型系统和友好语法的问题。[elixir](https://github.com/elixir-lang/elixir) 项目引入了 Ruby 语法，吸引了部分 Ruby On Rails 社区开发者，却没有类型系统支持。[Akka](https://akka.io/) 项目在 JVM 上模拟实现了 Erlang/OTP ，但丧失了 Erlang/OTP 的软实时特性。[Well-Typed](http://www.well-typed.com/) 公司的 [Cloud Haskell](https://github.com/haskell-distributed) 项目试图在 Haskell 上模拟实现 Erlang/OTP，目前项目已经停滞。此外还有 [lfe](https://github.com/rvirding/lfe) 引入了 Lisp 语法，[alpaca](https://github.com/alpaca-lang/alpaca)、[efene](https://github.com/efene/efene)、[elchemy](https://github.com/wende/elchemy)、[gleam](https://github.com/gleam-lang/gleam) 等项目试图引入 ML 风格语法和静态类型，目前大部分仍处于很早期的开发中。

今天，EMQ 团队做出努力，采用新的语言架构设计方式再一次尝试解决上述问题，正式向业界发布 Hamler 语言 0.1 版本！

## Hamler 语言主要特性

Hamler 作为运行在 Erlang VM 上的类 Haskell 语法的编程语言，核心特性可以概括为：

- 类 Haskell 和 ML 的友好语法
- 编译时的类型检查与类型推导
- 运行时的高并发、软实时支持

结合我们多年对[函数式编程](https://zh.wikipedia.org/wiki/%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B)的理解与开发 Erlang、Haskell 程序的经验，Hamler 语言支持函数编程大部分主要特性，我们相信这些特性可以帮助产业更好地迎接 5G、IoT 、边缘计算与云计算带来的开发浪潮，并吸引更多的开发者使用 Erlang VM - BEAM。

- 声明式与函数式编程
- 类 Haskell 与 ML 语法
- 编译时类型检查与推导
- 代数类型系统支持(ADT)
- 函数、闭包、高阶函数
- Currying and partial application
- Pattern matching, and Guards
- List comprehension
- Applicative and Monad
- 更高级的模块系统
- 高并发、软实时支持

## Hamler 编译器设计

Hamler 源码经过词法分析后生成 CST，然后经过 CST -> AST -> CoreFn 的语法树变换、语法分析与类型检查后，生成 CoreErlang 的 IR 代码，然后由 Erlang 编译器生成最终的二进制 Beam 文件。

Hamler 编译器架构如下图：

![hamler-compiler](https://static.emqx.net/images/28c4497efb066b3162c6b921bd3cd320.png)

Hamler 0.1 编译器最初尝试基于 GHC 8.10.1 实现，后改为基于 Purescript 0.13.6 实现。

## 欢迎参与 Hamler 开源项目

Hamler 函数编程语言从发起即是一个开源项目，目前核心开发者主要来自 EMQ 公司研发团队：

- [Feng Lee](https://github.com/emqplus): Hamler 语言设计者，贡献了一个梦想和大部分 libs
- [Yang M](https://github.com/EMQ-YangM): 贡献了 Hamler 编译器大部分代码
- [S Hu](https://github.com/SjWho): 来自 University of Bristol，贡献了 Hamler 大部分文档
- [wivwiv](https://github.com/wivwiv): 贡献了 hamler-lang.org 网站 theme 设计
- [CrazyWisdom](https://github.com/CrazyWisdom): 贡献了 hamler-lang.org 网站域名
- [ysfscream](https://github.com/ysfscream): 贡献了 hamler-lang.org 网站和 https 设置
- [juan6666](https://github.com/juan6666)：贡献了 Hamler 语言 Logo 设计

Hamler 开源项目最终将与合作伙伴一起，贡献给欧盟 2049 开放源码基金会 - [2049.Foundation](https://2049.foundation/)。

## 欢迎加入 EMQ 研发团队

[EMQ - 杭州映云科技有限公司](https://www.emqx.io/cn/about)致力于成为全球领先的消息与流处理开源软件企业，聚焦服务于新产业周期的 5G&IoT、边缘计算(Edge)与云计算(Cloud)市场。EMQ 研发团队主要采用 Erlang、Haskell 等函数编程语言，开发高并发、高可靠、软实时的大规模分布式系统。

招聘职位：[拉勾](https://www.lagou.com/gongsi/157269.html)，或联系HR：[hr@emqx.io](https://github.com/hamler-lang/hamler-internal/blob/master/posts/hr@emqx.io)

