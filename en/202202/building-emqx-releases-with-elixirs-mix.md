We are happy to announce that now [EMQX](https://github.com/emqx/emqx/) can be built using Elixir!

What does that mean?  EMQX is the most popular open source [MQTT broker](https://www.emqx.io), written in Erlang, which makes it highly scalable and with high-performance real-time message processing.  The Erlang EMQX releases will remain as always, and added to that there will be some packages that are built using Elixir's Mix build tool.  These work just as the Erlang ones, with the difference that the shell you have available when using EMQX's console is [IEx](https://hexdocs.pm/iex/1.13/IEx.html).

Here are a few benefits of building with Elixir:

- More familiar for Elixir developers;
- Great REPL (IEx is awesome!);
- Opens up the possibility to mix Elixir and Erlang more easily.

In this post, we describe some of the challenges we encountered while adapting a big project like EMQX to be built with Mix.

At the time of writing, for those who want to try it now, just clone the `master` branch of [EMQX](https://github.com/emqx/emqx/), run `make emqx-elixir` and have fun!

## Umbrella?

The first question we faced was: how to handle the multiple applications that already exist in EMQX?

Since EMQX is currently a monorepo with multiple applications (or rather: a Rebar3 umbrella project), we had at least two possible courses to handle them without breaking up the repo: to make it a Mix umbrella project as well (and let Mix manage everything itself), or to keep them managed by Rebar3 (and treat them as dependencies).

Making it a Mix umbrella would require us to create a `mix.exs` file for each application and also duplicate any information or functionality contained in the already existing `rebar.config` file for each.  While this leads to quite nice release build times (since Mix can track dependent changes much better), it also introduces the duplicated effort of having to update two files per application each time (`mix.exs` and `rebar.config`).  Not only that, but special compile hooks and other functionalities would have to be replicated in the Mix side of things.  For example, applications that use `gRPC` require a special build step to generate code from the Protobuf schemas, and that would have to be brought over to the Mix side of things.  Which can, again, create opportunity for `mix.exs` and `rebar.config` going out of sync with each other.

The second approach (the one we went with) was to make Mix treat each application as a local dependency that is managed by Rebar3.  Although the release build time using this approach is a bit longer (because Mix has a looser control over changes, and always compile local dependencies anyway), this has the nice benefits of avoiding duplicate efforts and configurations going out of sync.  All Rebar3 plugins and compilation hooks keep working without any further effort.

After we got the project compiling this way, the next challenge was to tackle the complex application start-up order that EMQX has.

## Complex application start-up order

Some Erlang applications have complex startup orders, with possibly one application controlling the startup of another to ensure some invariant.  This is the case for us: for example, one core application must have its code loaded before others, but it must not be started before another application that manages configurations.  Only after this configuration app does its thing is that another application finally starts the core one.  Whew.

In order to allow for such complex setups, one can specify different application start types in the [Erlang release file](https://www.erlang.org/doc/man/rel.html).  For most applications, you probably want to start it with either the `permanent` or `load` option.  In our case, we required that some applications that are depended on by others (by declaring them in the `applications` key in the `.app` file) to have start type `load`.  This works fine in our Rebar3 release build.  However, if you are not careful with the order of dependencies, your release may fail to boot correctly.

During a release, Mix does some nice additional consistency checks that Rebar3 doesn't: for instance, it checks that a given application cannot be both a regular and an included application, as that could cause inconsistency during boot order resolution.  Another safety consistency check it does is to prevent unsafe start types: if application `B` has start type `permanent` and depends on `A` (`A` is in `B`'s `applications` specification), and application `A` has start type `load`, the release will fail to boot (in the general case).  So, Mix forbids that case and refuses to produce a release in such conditions.

However, this static check cannot account for the complex case where application `B` (or some other that starts before `B`) manages `A`'s start-up, and thus prevents a legitimate release that can indeed boot.  We just needed a way to tell Mix to not enforce that check for those particular cases.

For our satisfaction, a [patch](https://github.com/elixir-lang/elixir/pull/11506) that introduces the possibility to ignore such cases was very quickly accepted and merged into Elixir, and should appear in versions `1.13.2` and `1.14.0`.  For now, we have to perform a little hack to enable us to build the release at the time of writing ;) .

Of course, a complex application like EMQX would need just a few more *steps* in place to finally build like the Rebar3 release.

## Custom build steps

EMQX has its own configuration system which requires special configuration files and directory structures to be present in the release, some of which are templates filled at build time depending on the desired build profile.  Also, it needs a couple helpers scripts to be bundled as well.  For those cases, Mix has the nice feature of allowing users to add custom [steps](https://hexdocs.pm/mix/1.13.1/Mix.Tasks.Release.html#module-steps) to the build pipeline, as well as an [overlay](https://hexdocs.pm/mix/1.13.1/Mix.Tasks.Release.html#module-overlays) functionality.  For our purposes, the overlays in Mix were a bit too rigid, and we used only a couple custom steps to accommodate our needs.

```
releases: [
  example: [
    steps: [&set_configs/1, :assemble, &copy_extra_files/1, :tar, &post_processing/1]
  ]
]
```

A custom step is simply a function that receives an [Elixir struct](https://hexdocs.pm/mix/1.13.1/Mix.Release.html#__struct__/0) containing the release properties and must return a value of the same type, possibly changing some parts of it.  In our case, the custom steps consisted of basically copying or templating a few files into the release directory, which fitted nicely with the custom step functionality.

## For the future: hot code upgrades

One of the most characteristic features of Erlang is the support for hot code upgrades: upgrading code in a running node without taking down the VM.  It's one feature that EMQX users can use to upgrade their installations without disrupting their uptime.  Unfortunately, at the time of writing, Elixir [does not support](https://hexdocs.pm/mix/1.13.1/Mix.Tasks.Release.html#module-hot-code-upgrades) hot code upgrades out of the box.  That means that we'll need to do more work in order to support that in our Elixir releases.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a >
</section>
