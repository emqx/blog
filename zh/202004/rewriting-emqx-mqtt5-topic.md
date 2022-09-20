EMQX 的主题重写功能支持根据用户配置的规则在 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)订阅主题、发布消息、取消订阅的时候将 A 主题重写为 B 主题。

EMQX 的 [保留消息](https://docs.emqx.io/broker/latest/cn/advanced/retained.html) 和 [延迟发布](https://docs.emqx.io/broker/latest/cn/advanced/delay-publish.html) 可以与主题重写配合使用，例如，当用户想使用延迟发布功能，但不方便修改客户端发布的主题时，可以使用主题重写将相关主题重写为延迟发布的主题格式。

## 开启主题重写功能

主题重写功能默认关闭，开启此功能需要修改 `etc/emqx.conf` 文件中的 `module.rewrite` 配置项。默认 `off` 表示关闭，如需开启请修改为 `on`。

```bash
module.rewrite = off
```

## 配置主题重写规则

[EMQX](https://www.emqx.com/zh) 的主题重写规则需要用户自行配置，用户可以自行添加多条主题重写规则，规则的数量没有限制，但由于任何携带主题的 **MQTT** 报文都需要匹配一遍重写规则，因此此功能在高吞吐场景下带来的性能损耗与规则数量是成正比的，用户需要谨慎地使用此功能。

每条主题重写规则的格式如下：

```bash
module.rewrite.rule.<number> = 主题过滤器 正则表达式 目标表达式
```

每条重写规则都由以空格分隔的主题过滤器、正则表达式、目标表达式三部分组成。在主题重写功能开启的前提下，EMQX 在收到诸如 **PUBLISH** 报文等带有主题的 MQTT 报文时，将使用报文中的主题去依次匹配配置文件中规则的主题过滤器部分，一旦成功匹配，则使用正则表达式提取主题中的信息，然后替换至目标表达式以构成新的主题。

目标表达式中可以使用 `$N` 这种格式的变量匹配正则表达中提取出来的元素，`$N` 的值为正则表达式中提取出来的第 N 个元素，比如 `$1` 即为正则表达式提取的第一个元素。

需要注意的是，EMQX 使用倒序读取配置文件中的重写规则，当一条主题可以同时匹配多条主题重写规则的主题过滤器时，EMQX 仅会使用它匹配到的第一条规则进行重写，如果该条规则中的正则表达式与 MQTT 报文主题不匹配，则重写失败，不会再尝试使用其他的规则进行重写。因此用户在使用时需要谨慎的设计 MQTT 报文主题以及主题重写规则。

## 示例

假设 `etc/emqx.conf` 文件中已经添加了以下主题重写规则：

```bash
module.rewrite.rule.1 = y/+/z/# ^y/(.+)/z/(.+)$ y/z/$2
module.rewrite.rule.2 = x/# ^x/y/(.+)$ z/y/x/$1
module.rewrite.rule.3 = x/y/+ ^x/y/(\d+)$ z/y/$1
```

此时我们分别订阅 `y/a/z/b`、`y/def`、`x/1/2`、`x/y/2`、`x/y/z` 五个主题：

+ `y/def` 不匹配任何一个主题过滤器，因此不执行主题重写，直接订阅 `y/def` 主题。

+ `y/a/z/b` 匹配 `y/+/z/#` 主题过滤器，EMQX 执行 `module.rewrite.rule.1` 规则，通过正则正则表达式匹配出元素 `[a、b]` ，将匹配出来的第二个元素带入 `y/z/$2`，实际订阅了 `y/z/b` 主题。

+ `x/1/2` 匹配 `x/#` 主题过滤器，EMQX 执行 `module.rewrite.rule.2` 规则，通过正则表达式未匹配到元素，不执行主题重写，实际订阅 `x/1/2` 主题。

+ `x/y/2` 同时匹配 `x/#` 和 `x/y/+` 两个主题过滤器，EMQX 通过倒序读取配置，所以优先匹配 `module.rewrite.rule.3`，通过正则替换，实际订阅了 `z/y/2` 主题。

+ `x/y/z` 同时匹配 `x/#` 和 `x/y/+` 两个主题过滤器，EMQX 通过倒序读取配置，所以优先匹配 `module.rewrite.rule.3`，通过正则表达式未匹配到元素，不执行主题重写，实际订阅 `x/y/z` 主题。需要注意的是，即使 `module.rewrite.rule.3` 的正则表达式匹配失败，也不会再次去匹配 `module.rewrite.rule.2` 的规则。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
