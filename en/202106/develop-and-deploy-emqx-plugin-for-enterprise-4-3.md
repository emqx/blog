A few EMQ X Enterprise customers were asking how they can develop their own EMQ X plugins and use them in the enterprise edition. This article is to document the steps.

## How to build your own plugin

Since EMQ X v4.3, community plugins can be built in the umbrella project with only a few lines of config change. Please find the instructions in this [README](https://github.com/emqx/emqx/tree/master/lib-extra)

## Where to install your plugin

Starting from community edition v4.3.2 and enterprise edition e4.3.1, external plugins can be installed in `<expand_plugins_dir>`, where `<expand_plubins_dir>` is configurable in `emqx.conf` by they config key `plugins.expand_plugins_dir`. By default the directory is configured as `$INSTALL_DIR/etc/plugins` when EMQ X is installed from zip package, and `/etc/emqx/plugins/` when installed from RPM or DEB packages.

## What should a plugin release contain

An EMQ X plugin, is an Erlang application that implements some of the EMQ X’s hook-points. In this sense, the build artifacts to be deployed to production is similar to the built-in plugins, it consists of directories as below (taking the plugin [emqx_psk_pgsql](https://github.com/zmstone/emqx_psk_pgsql) for example)

```
$ tree _build/default/lib/emqx_psk_pgsql/
_build/default/lib/emqx_psk_pgsql/
├── ebin
│   ├── emqx_psk_pgsql.app
│   ├── emqx_psk_pgsql.beam
│   ├── emqx_psk_pgsql_app.beam
│   ├── emqx_psk_pgsql_client.beam
│   └── emqx_psk_pgsql_sup.beam
├── etc
│   └── emqx_psk_pgsql.conf
├── include
│   └── emqx_psk_pgsql.hrl
├── priv
│   └── emqx_psk_pgsql.schema
└── src
    ├── emqx_psk_pgsql.app.src
    ├── emqx_psk_pgsql.erl
    ├── emqx_psk_pgsql_app.erl
    ├── emqx_psk_pgsql_client.erl
    └── emqx_psk_pgsql_sup.erl
```

`src` and `include` are optional since all they have inside are source code. `ebin` directory is where the compiled beam files reside. `etc` is per EMQ X’s convention, the directory to store the plugin’s config file, and `priv` directory is, per Erlang’s convention, to keep build artifacts to be released (in our case, the plugin’s config schema file). 

## How to load/unload your plugin

After the plugin is installed, the node needs a restart to have the new code loaded, then the external plugin works the same as the built-in plugins delivered as a part of EMQ X packages. That is, the `emqx_ctl` plugins command can be used to list, load, and unload plugins.

## If your plugin has other dependencies

A plugin (as an Erlang or Elixir) application may have other applications as dependencies.
The dependency applications should also be installed to `expand_plubins_dir`.
e.g. In a rebar3 project, after the code is compiled, you should be able to find all the dependencies in `_build/default/lib/` – which are to be copied to `expand_plubins_dir`

Please note though, if a dependency application is included in the EMQ X release package, it should not be installed to external plugin dir. 

You can list `$INSTALL_DIR/lib/` directory to find all the applications released in the EMQ X package.
