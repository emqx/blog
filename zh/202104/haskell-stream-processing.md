[HStreamDB](https://hstream.io) 团队于上周日举办了线上 Open Day，HStreamDB CTO 韩冬与大家分享了有关 [Haskell](https://www.haskell.org) 中流处理解决方案的一些思考。

<div style="position: relative; padding: 30% 45%;">
<iframe style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;" src="https://player.bilibili.com/player.html?aid=802772429&bvid=BV1Vy4y1s7sw&cid=330262589&page=1&as_wide=1&high_quality=1&danmaku=0" frameborder="no" scrolling="no"></iframe>
</div>


<center>视频回放抢先看</center>

### Free Monad 的流处理

韩冬首先介绍了 Haskell 现 Haskell 生态中常见的基于 Free Monad 的流处理方案，包括 streaming 和 pipes 等，并分析了目前方案的基本原理和优缺点。当前方案通过 Free Monad 构造，支持任意地遍历和处理，但是类型过于复杂，不利于开发者参与，也不利于用户理解和应用。

![1.png](https://static.emqx.net/images/5ebb6597a33f1a2f034dc34915f05e95.png)  
![2.png](https://static.emqx.net/images/3cbb199f01db3578a7263fcf9b248f98.png)

### Z.Haskell 的流处理

由此，韩冬引出了他所进行的项目 [Z.Haskell](https://zh.z.haskell.world) 中流处理方案的探索过程，并分享了自己设计实现新的流处理库时收获的经验与教训。

![3.png](https://static.emqx.net/images/bbffadd3b832e4e592ad446dd3ec3beb.png)
![4.png](https://static.emqx.net/images/73607c1f6c6f1c06525e77b0f275a2bc.png)      

### 流处理方案对比

在分享的最后，他总结最终选择的方案原理，并和其他方案比较得出优点和不足：优点包括类型简单可组合，且不需要涉及到单子变换的知识等。而缺点则是因为强制了在 IO 中，不接受用户提供的状态单子。

在多次推翻与重建、借鉴与学习、突破与创新中，BIO 有了雏形，并在 [流数据库 HStreamDB](https://hstream.io) 中投入使用。在随后的讨论环节中，大家探讨了 HStreamDB 所涉及的流处理与其他现有产品的异同，以及如何使 BIO 更好地适配我们未来的产品。

除了对社区开放、倾听来自社区的各种不同声音，Open Day 也是 EMQ 团队内部加强理解与交流的途径之一。我们也在通过每一次活动进行着不断改进与迭代，希望为大家带来更愉快的参与体验，让 Open Day 成为大家与同好者建立联结的平台，成为真正对社区有意义的活动。
