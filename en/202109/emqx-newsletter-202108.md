In August, the open source teams are mostly keeping the focus on EMQ X 5.0 feature developments. A lot of heat in discussions, a lot of fast iterations. EMQ X 5.0 has reached alpha.5 release. And we expect the **first** beta release to come soon.

## A quick glance at EMQ X 5.0 management UI

EMQ X 5.0 will come with a freshly redesigned management UI. The new design focuses a lot on user experience improvements, we try our best to strike a balance between the clarity of the UI and the ability to parameterize. 

To show off, here is a screenshot of the new UI for advanced [MQTT](https://www.emqx.com/en/mqtt) features. 

![New UI for advanced MQTT](https://static.emqx.net/images/e638f39e3c4875aa19bae385f0536b50.png)

Managing Topic Rewrite, Auto Subscribes, Delayed Publish, and Event Messages will be a breeze experience with the new UI.

## Reconfigure EMQ X on the fly

![Reconfigure EMQ X on the fly](https://static.emqx.net/images/0a952d8445d3cc4a59d0949d67e2b011.png)

As we showed in the previous newsletter, EMQ X 5.0 uses Open API 3.0 for management APIs. If you visit [https://:localhost:18083/api-docs](http://localhost:18083/api-docs), the browser will take you to the Swagger UI where you can try out API calls directly from the GUI as well as viewing the detailed documentation of the API.

The new stuff we added in August is the framework that will allow EMQ X users to reconfigure the cluster on the fly. For the majority of the config changes, there will be no need to restart the broker to make config changes take effect.

 

## Cluster Call for Consistent Configuration

We just introduced on-the-fly configuration update and reloading, you may wonder how we ensure the changes are applied across all nodes in a cluster. This is why we have implemented the “Cluster Call” feature.

Previously we have been using Erlang’s multi-call in EMQ X to replicate changes to all nodes in the cluster, which is straightforward to use and mostly working just fine in most of the network scenarios. However, there has been a lack of a nice rollback or failure handling.

The “Cluster Call” feature allows us to replicate the change in an async fashion, which will eventually get the same changes applied on all nodes in the cluster.

## Configuration Document Generation

In EMQ X 5.0, source code will become the single source of truth for API and configuration documentation. With the help of [HOCON schema feature](https://github.com/emqx/hocon/blob/master/SCHEMA.md), keeping code and documentation in sync will be effortless. Below is an example of listener config documentation.

Here in the picture is a screenshot of the generated configuration document for the QUIC listener --- Yes, in case you have missed our previous updates, EMQ X now has a PoC implementation of MQTT over [QUIC](https://datatracker.ietf.org/doc/rfc9000/).

![generated configuration document for the QUIC listener](https://static.emqx.net/images/8e3946d74c74a232d0a06afab61800c9.png)

## RLog is now named Mria

We have previously named the async Mnesia database replication project RLog (as in Replicated Mnesia transaction log), and it was implemented as a part of the [ekka](https://github.com/emqx/ekka) library.

We believe this project will benefit the Erlang/Elixir community, so we have decided to move it out to its own repo: [mria](https://github.com/emqx/mria).

The project ‘mria’ is named after [the biggest aircraft in the world AN-225 “MRIA”](https://englishrussia.com/2011/03/17/an-225-mria-the-biggest-aircraft-in-the-world/), and it also shares the same ‘-ia’ suffix as its origin: Mnesia
