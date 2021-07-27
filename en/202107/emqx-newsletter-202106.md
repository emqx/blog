Since many weeks ago, we have been working hard to define EMQ X 5.0, it has been quite challenging to scope, prioritize, and finally get to focus on development in June. Now it’s becoming more and more clear what we are going to deliver.

## Releasing v5.0-alpha.1 soon

We can’t wait to release the first alpha version, so we can get early feedback from the community. Some of the new features highlighted:

### HOCON config + HOCON schema

If you have been following up on our newsletter and/or demo sessions, HOCON is probably no longer a stranger to you. HOCON or **Human-Optimized Config Object Notation** is a format for human-readable data and a superset of [JSON](https://en.wikipedia.org/wiki/JSON). EMQ X v5.0 will use the HOCON format for configurations.
HOCON schema is a library/framework the EMQ X team developed to provide type-safe configuration validation. More importantly, it is also used for HTTP API JSON data validation. We believe it will be beneficial for both the users and the developers by unifying the two management interfaces (configuration and HTTP API).

### Infrastructure as code for EMQ X resources

In EMQ X v5.0, resources such as authentication database connections, rule engine resources/actions, will be deployable from config files. Runtime modifications, such as updates from web UI, or HTTP API, will also be persisted in config files.

This will make infrastructure as code deployment much easier than before when the resources are stored in Mnesia.

### Composable Authentication steps

To simplify user interfaces and implementation, authentication plugins are merged into one Erlang application (the AuthN app) which makes authentication steps composable as a 'chain' in HOCON config. It is still an ongoing task to support all backends EMQ X v4.x supported. So far the finished ones are Mnesia, MySQL, PostgreSQL and JWT.

### Composable Authorization steps

In order to support access control with composable steps, ACL or Access Control List will be included in a more generic application (the AuthZ app). The new interface (also in HOCON format) is similar to the old acl.conf, but can be extended with various database backends to support more specific access control.

### MQTT-on-QUIC

The [QUIC](https://github.com/emqx/quic) project has been under development detached from EMQ X main project since March. It is now finally being integrated with [emqx.git](https://github.com/emqx/emqx). MQTT-on-QUIC will be released in v5.0 as an experimental feature as there is more work to be done. If you are brave as us, let’s work together to take full advantage of the QUIC protocol for IoT.

### RLOG

[RLOG](https://github.com/emqx/eip/blob/main/implemented/0004-async-mnesia-change-log-replication.md), or Replicated (Mnesia transaction) Logs, is a project aiming to make Erlang’s built-in database ‘Mnesia’ scalable. The main work of this project is developed in the [ekka](https://github.com/emqx/ekka) application since March. Now it is finally being integrated with [emqx.git](https://github.com/emqx/emqx).

With this feature, an EMQ X cluster can be configured with two types of node roles: core and replicant. Core nodes form a traditional Mnesia cluster, while replicant nodes are made stateless, and can be scaled up and down hassle-free.

## 4.3 Improvements

Although v5.0 is our main focus, v4.3 is nonetheless still being actively maintained. In June, we released v4.3.4 to fix some of the plugin issues. Please see [Release Notes](https://github.com/emqx/emqx/releases) for more details. 
