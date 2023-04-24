EMQX **MQTT 5.0 topic rewrite** supports rewriting topic A to topic B,  when subscribing topics, publishing messages and unsubscribing in MQTT client according to the rule configured by clients.

The EMQX  [MQTT retained message](https://www.emqx.io/docs/en/v5.0/messaging/mqtt-retained-message.html) and  [delayed publish](https://www.emqx.io/docs/en/latest/messaging/mqtt-delayed-publish.html) can cooperate with the rewriting topic function to use. For example, when users want to use delayed publish, but it is difficult to modify the topic published by the MQTT client, they can use rewriting topic function to rewrite related MQTT topics into the format of delayed publish topic. 

## Enable MQTT topic rewrite

Topic rewrite is disabled by default. To enable this function, users need to modify the configuration item  `module.rewrite`  in file `etc/emqx.conf`.  `off` represents closed by default. If users need to use it, please modify it into  `on`.

```bash
module.rewrite = off
```

## Configure MQTT topic rewrite rules

The [EMQX](https://www.emqx.com/en) MQTT topic rewrite rule needs users to configure by themselves, users themselves can add many topic rewrite rules, and the number of rules is unlimited. However, the performance consumption brought by this function in high throughput situation and the number of rules is proportional, because every **MQTT packets** with topics need to match the  rewrite rules again. Therefore, users need to use this function carefully. 

The format of every rewrite topic rule is :

```bash
module.rewrite.rule.<number> = topic filter regular expression target expression
```

Every rewrite topic rule make by the space-separated topic filter, the regular expression and the target expression. Under the precondition that the topic rewrite is enabled, when [EMQX](https://www.emqx.com/en) receives MQTT packets with topics such as the **PUBLISH** packet, it will use the topic of the packet to sequentially match topic filters of the configuration file. If this match is successful, EMQX will use the regular expression to extract information from the topic, and then replace the topic into the target expression to form a new topic.

In the target expression, users can use this formatted variable `$N` to match the extracted element from the regular expression. The value of `$N` is the nth extracted element from the regular expression. For example, `$1` is the first element extracted from the regular expression. 

It should be noted that EMQX uses the reverse order to read the rewrite rule of configuration. When a topic can match the topic filters of multiple topic rewrite rules at the same time, EMQX will only use the first successfully matched rule to rewrite. If the regular expression of this rule unsuccessfully match the MQTT packet topic, then rewrite failed, and no longer try to rewrite using other rules. Therefore, users need to design the MQTT packet topic and topic rewrite rules carefully when they use EMQX.

## MQTT topic rewrite example

If `etc/emqx.conf` file already added the following topic rewrite rules : 

```bash
module.rewrite.rule.1 = y/+/z/# ^y/(.+)/z/(.+)$ y/z/$2
module.rewrite.rule.2 = x/# ^x/y/(.+)$ z/y/x/$1
module.rewrite.rule.3 = x/y/+ ^x/y/(\d+)$ z/y/$1
```

At this time we subscribe `y/a/z/b`、`y/def`、`x/1/2`、`x/y/2`、`x/y/z` five topics respectively.

+ `y/def` does not match any topic filters, so it does not implement rewriting topic, and subscribes `y/def` topic directly.

+ `y/a/z/b` matches `y/+/z#` topic filters. EMQX implements the `module.rewrite.rule.1` rule, and matches element `[a、b]` through the regular expression. EMQX will bring the second successfully matched element into `y/z/$2`. So the client actually subscribes topic `y/z/b`.

+ `x/1/2` matches `x/#` topic filters. EMQX implements the  `module.rewrite.rule.2` rule, if no elements are matched through the regular expression, it does not implement topic rewrite. So the client actually subscribes topic `y/z/b`. 

+ `x/y/2` matches two topic filters( `x/#` and `x/y/+` ) at the same time. EMQX reads the configuration by reverse order, and will give priority to matches `module.rewrite.rule.3`, and it will replace the topic through the regular expression. So the client actually subscribes topic `z/y/2`. 

+ `x/y/z` matches two topic filters( `x/#` and `x/y/+` ) at the same time. EMQX reads the configuration by reverse order, and will give priority to matches `module.rewrite.rule.3`, if no elements are matched through the regular expression, it does not implement rewriting topic. So the client actually subscribes topic `x/y/z`. It should be noted that EMQX will not match the `module.rewrite.rule.2` rule again, although the regular expression of `module.rewrite.rule.3` match unsuccessfully.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
