EMQX stands out in its domain, acclaimed for its remarkable scalability, impressive throughput, and minimal latency. Complementing these features is its intuitive and modern dashboard, making it a go-to choice for many. Today, however, we will be exploring a facet of EMQX that doesn’t always capture the limelight but is equally vital: its extensibility. We'll be diving deep into the plugin mechanism—a feature present since the inception of EMQX, now improved by the management enhancements of version 5.

In this post, we'll explore:

- **The Core of EMQX Plugins:** Understanding the basic workings is key when venturing into the world of plugins.
- **Building a Plugin:** We'll break down the steps using a practical example, showing you how to create a plugin specifically for EMQX v5.
- **Installing and Running a Plugin:** Find out how to smoothly integrate and run your plugin in an active EMQX cluster.
- **Operational Tips:** Steps to install a plugin from files, bypassing the EMQX dashboard UI or CLI.
- **Debugging Tips:** Strategies for quicker compile, deploy, and test cycles.

## **Unraveling EMQX Plugins**

At their core, EMQX plugins are Erlang applications. They work by registering (hooking) specific callbacks with the central EMQX application `emqx`. These callbacks come into play either before or after particular events occur.

It's essential to understand that hooks aren’t exclusive to third-party plugin integrations. In fact, many of EMQX’s inherent features—like authentication, authorization, and data integration—are crafted using these hook callbacks. Before the advent of version 5, these were introduced to users as native plugins.

### **The Nitty-Gritty of Hook Callback Evaluation**

In the world of EMQX, a distinct Erlang process is spawned for each client. This process is responsible for managing connection, session, or message lifecycle events and invoking the associated hook callbacks. This architectural choice allows millions of clients to run concurrently. This implies that a callback function concurrently is evaluated concurrently, thus, it's advisable to design your callback such that it avoids tapping into mutually exclusive resources.

### **Hook Callback Registration**

When a plugin application comes to life, it reaches out to EMQX’s APIs to hook callbacks at specific hook points. These registrations find their home in an `ets` table (a named table `emqx_hooks`).

But, the association isn't eternal. When the plugin application shuts down, it should gracefully unregister the callback.

### **The Three Pillars: Hook Points**

Broadly speaking, there are three event categories that beckon the callbacks:

1. **Client Events**: These encompass the stages of the MQTT connection lifecycle. For instance, the receipt of a CONNECT packet triggers callbacks associated with the `client.connect` hook point.
2. **Session Events**: This covers the various stages of an MQTT session's life—from its birth to its eventual termination.
3. **Messaging Events**: These delve into the MQTT message delivery journey, such as when a PUBLISH packet arrives or post the dispatch of a PUBACK to a client.

As of this writing, enthusiasts can play around with 20 distinct hook points.

## A Simple Example: Craft Our First Plugin

As an example, we’ll try to build a plugin which extends EMQX’s access control with a special rule: A client is only allowed to subscribe to topics matching a pattern like `msg/{{user-id}}/whatever` where `{{user-id}}` is extracted from MQTT client ID.

Before we start, it’s worth mentioning that EMQX has quite a few built-in solutions for access control (authorization); hence, there is usually no need to develop a plugin.

For instance, if the requirement is to allow clients to subscribe to whichever topic that starts with its client ID as prefix, the built-in file based ACL rule should work, just add `{allow, all, subscribe, ["msg/${clientid}/#"]}.` to  the front of `acl.conf`

However, in this example, we need to extract user-id from a part of the client ID (but not client ID itself), which is so far not something the built-in features can handle.

### Step 0. Install Erlang/OTP

This post is based on EMQX v5.1 which is officially released on Erlang/OTP 25. You can find more information here: [https://github.com/emqx/emqx/blob/master/README.md#build-from-source](https://github.com/emqx/emqx/blob/master/README.md#build-from-source)

You can build EMQX on newer version Erlang/OTP, but if your intension is to load the plugin to EMQX’s official release package installation, then the plugin cannot be built on newer Erlang/OTP. 

### Step 1. Generate skeleton code from a template

EMQX team created a rebar3 template which can be used to generate the skeleton code. Here are the steps.

- Install the plugin in `~/.config/rebar3/templates`

  ```
  $ mkdir -p ~/.config/rebar3/templates
  $ cd ~/.config/rebar3/templates
  $ git clone https://github.com/emqx/emqx-plugin-template.git
  ```

- Generate skeleton modules

  ```
  $ cd /path/to/my/project
  $ rebar3 new emqx-plugin emqx_simple_acl
  ```

After the plugin project is generated, it should look like:

```
tree emqx_simple_acl/
emqx_simple_acl/
├── erlang_ls.config
├── get-rebar3
├── LICENSE
├── Makefile
├── priv
│   └── config.hocon
├── README.md
├── rebar.config
├── rebar.lock
└── src
    ├── emqx_simple_acl_app.erl
    ├── emqx_simple_acl.app.src
    ├── emqx_simple_acl_cli.erl
    ├── emqx_simple_acl.erl
    └── emqx_simple_acl_sup.erl
```

### Step 2. Update the generated code

The skeleton generates all the supported hook points and write debug printouts in each callback. Since we only want to hook to the `client.subscribe` hook point, we can simply delete all other code.

After clean-up, the module `emqx_simple_acl.erl` should look like below.

```
-module(emqx_simple_acl).

-include_lib("emqx/include/emqx.hrl").
-include_lib("emqx/include/emqx_hooks.hrl").
-include_lib("emqx/include/logger.hrl").

-export([ load/1
        , unload/0
        ]).

-export([ on_client_subscribe/4 ]).

load(Env) ->
    hook('client.subscribe',    {?MODULE, on_client_subscribe, [Env]}).

unload() ->
    unhook('client.subscribe',    {?MODULE, on_client_subscribe}).

on_client_subscribe(#{clientid := ClientId}, _Properties, TopicFilters, _Env) ->
    io:format("Client(~s) will subscribe: ~p~n", [ClientId, TopicFilters]),
    {ok, TopicFilters}.

hook(HookPoint, MFA) ->
    emqx_hooks:add(HookPoint, MFA, _Property = ?HP_HIGHEST).

unhook(HookPoint, MFA) ->
    emqx_hooks:del(HookPoint, MFA).
```

It’s also important to update the description texts in:

- The `description` filed in `src/emqx_simple_acl.app.src`. It describes the Erlang application.
- Text in `README.md` . It’s important to have a clear description of what this plugin does and how to maintain etc.
- The `emqx_plugrel` section in `rebar.confg` provides the information of the package to be displayed in the CLI outputs as well as dashboard. 
  Below is an example:

```
%% Additional info of the plugin
{emqx_plugrel,
    [ {authors, ["Zaiming (stone) Shi"]}
    , {builder,
        [ {name, "zmstone"}
        , {contact, "contact@emqx.com"}
        , {website, "http://emqx.com"}
        ]}
    , {repo, "https://github.com/zmstone/emqx_simple_acl"}
    , {functionality, ["Demo"]}
    , {compatibility,
        [ {emqx, "~> 5.0"}
        ]}
    , {description, "My simple ACL."}
    ]
}.
```

### Step 3. Implement the rule

What we need to change, is the `on_client_subscribe` callback, which is evaluated before EMQX accepts the subscriptions and registers them in the system.

What we need to implement can be described as:

- Parse `ClientId` (which is a binary string), to get user ID.
- Filter the `TopicFilters` list, drop the ones that do not match the pattern `msg/{{user-id}}/#`

If we say the client IDs are of pattern `{{region}}-{{type}}-{{user-id}}`, we need to extract the last part of the dash-separated string. The implementation would look like below:

```
on_client_subscribe(#{clientid := ClientId}, _Properties, Subscriptions, _Env) ->
    io:format("Client(~s) will subscribe: ~0p~n", [ClientId, topics(Subscriptions)]),
    case parse_client_id_for_user_id(ClientId) of
        {ok, UserId} ->
            Allowed = lists:filter(fun(S) -> is_valid_subscription(UserId, S) end, Subscriptions),
            io:format("Client(~s) is allowed to subscribe: ~0p~n", [ClientId, topics(Allowed)]),
            {ok, Allowed};
        {error, invalid_clientid} ->
            io:format("Client(~s) is not allowed to subscribe to any topics~n", [ClientId]),
            %% return an empty list here means no subscription to any topic
            {ok, []}
    end.

%% Take a client ID of pattern {{region}}-{{type}}-{{user-id}}
%% and return {{user-id}}.
%% If the client ID deos not match this pattern, we consider
%% it not a valid client, and do not allow it to subscribe to any topics.
parse_client_id_for_user_id(ClientId) ->
    case binary:split(ClientId, <<"-">>, [global]) of
        [_Region, _Type, UserId] when UserId =/= <<>> ->
            {ok, UserId};
        _ ->
            {error, invalid_clientid}
    end.

%% Check if a topic starts with "msg/{{userid}}/"
is_valid_subscription(UserId, {Topic, _SubOpts}) ->
    Size = size(UserId),
    case Topic of
        <<"msg/", UserId:Size/binary, "/", _/binary>> ->
            true;
        _ ->
            false
    end.

%% Subs is a list of {Topic, SubscribeOptions}
topics(Subs) ->
    lists:map(fun({T, _SubOpts}) -> T end, Subs).
```

### Step 4. Build the plugin

Simply execute command `make rel` should produce a plugin package as `_build/default/emqx_plugrel/emqx_simple_acl-1.0.0.tar.gz`.

## Install and Run the Plugin

You can run `emqx ctl plugins` command to manage plugins, however, a more straightforward way is to manage it from the dashboard UI.

We can start EMQX with this command: `docker run --name emqx -it --rm -p 18083:18083 -p 1883:1883 emqx/emqx:5.1.5` 

Then visit the dashboard at port 18083, log in with `admin` `public` (you will be redirected to change password when logging in for the first time). You should be able to find the “Plugins” menu under the “Management” group. Click on “+ Install Plugin” button at the upper right corner, and you’ll be directed to an upload page.

![image.png](https://assets.emqx.com/images/3044797739109fa7ce5babc67f543fc8.png)

After it’s installed, you should be able to see it in the plugins list, and the initial state of it is always “Inactive”.

![image.png](https://assets.emqx.com/images/83e088fa51fee03db66a2b444a508bc2.png)

Before we start it, let’s inspect it. If you click the name, you’ll be able to see all the information of this plugin.

The description text is originally from your `README.md` and `rebar.config`.

![image.png](https://assets.emqx.com/images/08545f82ee91acc1322b1633bca2947e.png)

Now we can start it by clicking the “Start” button and you’ll see the plugin is at “Active” state.

We can also try to inspect it from CLI: `docker exec -it emqx bash -c 'emqx ctl plugins list'`

```
[
  {
    "running_status" : "running",
    "repo" : "https://github.com/zmstone/emqx_simple_acl",
    "rel_vsn" : "1.0.0",
    "rel_apps" : [
      "emqx_simple_acl-0.1.0",
      "map_sets-1.1.0"
    ],
    "name" : "emqx_simple_acl",
    "metadata_vsn" : "0.1.0",
    "git_ref" : "unknown",
    "functionality" : [
      "Demo"
    ],
    "description" : "My simple ACL.",
    "date" : "2023-08-30",
    "config_status" : "enabled",
    "compatibility" : {
      "emqx" : "~> 5.0"
    },
    "built_on_otp_release" : "25",
    "builder" : {
      "website" : "http://emqx.com",
      "name" : "zmstone",
      "contact" : "contact@emqx.com"
    },
    "authors" : [
      "Zaiming (Stone) Shi"
    ]
  }
]
```

## Verify it

Let’s first try to see if the plugin has successfully registered the callback in `emqx_hooks` table.

Attach to EMQX’s remote console, we can inspect all hooks like below:

```
$ docker exec -it emqx bash -c 'emqx remote_console'
Erlang/OTP 25 [erts-13.2.2] [emqx] [64-bit] [smp:20:20] [ds:20:20:10] [async-threads:1] [jit:ns]

Restricted Eshell V13.2.2  (abort with ^G)
v5.1.5-build.3(emqx@172.17.0.2)1> rr(emqx_hooks).
[callback,hook]
v5.1.5-build.3(emqx@172.17.0.2)2> ets:tab2list(emqx_hooks).
[...
#hook{name = 'client.subscribe',
       callbacks = [#callback{action = {emqx_simple_acl,on_client_subscribe,
                                                        [[]]},
                              filter = undefined,priority = 1000}]},
...
]
```

Now let’s try to connect an[ MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) to test if the plugin is working as expected.

We’ll use [MQTTX command line tool](https://mqttx.app/cli) in our tests.

If we try to connect with client ID `region1-type1-user1` , then subscribe to `msg/user1/#` like below:

```
mqttx sub -h localhost -p 1883 -i region1-type1-user1 -t msg/user1/#
```

We should be able to find the subscription in the dashboard as below:

![image.png](https://assets.emqx.com/images/e8ad53b2f0da100727d3e54f94738274.png)

Also to find the debug print outs in the docker console like below:

```
Client(region1-type1-user1) will subscribe: [<<"msg/user1/#">>]
Client(region1-type1-user1) is allowed to subscribe: [<<"msg/user1/#">>]
```

If we test with a bad topic pattern `$ mqttx sub -h localhost -p 1883 -i region1-type1-user1 -t msg/userX/0`, we’ll see logs like below.

```
Client(region1-type1-user1) will subscribe: [<<"msg/userX/0">>]
Client(region1-type1-user1) is allowed to subscribe: []
```

If we connect with a client ID that does not match the `{{region}}-{{type}}-{{user-id}}` pattern

`$ mqttx sub -h localhost -p 1883 -i user1 -t msg/user1/0`, then the client will not be able to subscribe to any topic.

```
Client(user1) will subscribe: [<<"msg/user1/0">>]
Client(user1) is not allowed to subscribe to any topics
```

## Operational Tips

We've learned that EMQX recognizes plugins as `.tar.gz` packages. You can gauge the status of these plugins (whether they're active, inactive, etc.) using the dashboard UI or CLI. However, for sysadmins who prefer automation, some ambiguities remain:

- Where exactly does EMQX save the uploaded package?
- How does EMQX handle the state of each plugin?

Once we shed light on these aspects, the automation process becomes smoother.

### Plugin Package Extraction

As many have observed, EMQX v5 plugins are essentially `.tar.gz` files, the content of which does not vastly different from a typical Erlang application. EMQX unzips this package into the plugins directory. For instance:

```
docker exec -it emqx bash -c 'ls /opt/emqx/plugins/emqx_simple_acl-1.0.0/'
README.md  emqx_simple_acl-0.1.0  map_sets-1.1.0  release.json
```

### Plugin State Persistence

A closer look at the cluster-synced configuration file with `docker exec -it emqx bash -c 'cat /opt/emqx/data/configs/cluster.hocon'` reveals:

```
plugins {
  install_dir = plugins
  states = [
    {
      enable = true
      name_vsn = emqx_simple_acl-1.0.0
    }
  ]
}
```

Every installed plugin has its state saved in the `plugins.states` array. This array format ensures a consistent order for loading and initiating plugins.

To preset this state before the EMQX node starts, you can combine it with `etc/emqx.conf` to achieve persistence. For Docker users, this means mounting from the host, or using ConfigMap for Kubernetes. However, bear in mind that when operating in Docker, the data directory acts as a Docker volume. Always ensure `cluster.hocon` remains writable for EMQX, allowing storage of real-time, cluster-synced configuration changes. i.e. Avoid mounting the `cluster.hocon` file directly.

## Debugging Tips

Running integrated tests with EMQX can be tedious if you constantly need to rebuild the package, upload it, and restart the plugin.

This is where EMQX’s hot-patch mechanism steps in.

Upon tweaking the `emqx_simple_acl.erl` module, the `make` command allows for code recompilation. The newly compiled code is directed to `_build/default/lib/emqx_simple_acl/ebin/emqx_simple_acl.beam`.

Use the commands below to load the new beam file into EMQX without needing a restart:

```
docker cp _build/default/lib/emqx_simple_acl/ebin/emqx_simple_acl.beam emqx:/opt/emqx/plugins/emqx_simple_acl-1.0.0/emqx_simple_acl-0.1.0/ebin/
docker exec -it emqx bash -c 'emqx eval "c:lm()."'
```

A successful beam file update should display `[{module,emqx_simple_acl}]`.

## Summary

EMQX offers a robust platform that goes beyond its immediate capabilities, thanks to its adaptable plugin system. This post has guided readers through the foundational concepts of EMQX plugins, from understanding their core principles to the hands-on process of building one tailored for EMQX v5. We also delved into seamless methods to integrate and operate a plugin within the EMQX environment. For those seeking more efficient workflows, our operational tips provided insights into bypassing traditional UI or CLI routes, while our debugging strategies aimed to accelerate the development cycle. Whether you're a seasoned developer or new to EMQX, these insights will empower you to harness the full potential of its plugin ecosystem.

The example code is published to GitHub repo: [zmstone/emqx_simple_acl](https://github.com/zmstone/emqx_simple_acl)

You can find a more brief example from EMQX official docs of v5 plugins [here](https://docs.emqx.com/en/enterprise/v5.1/extensions/plugins.html).

And more detailed information about Hooks [here](https://docs.emqx.com/en/enterprise/v5.1/extensions/hooks.html). 



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
