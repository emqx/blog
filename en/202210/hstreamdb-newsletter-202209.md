This month, we added support for choosing Rqlite as the storage component for the metadata of HServer and restructured HServer based on the new self-developed Haskell gRPC framework. Meanwhile, we released new Rust Client and cluster deployment tools. 

Another important note is that users can now submit early access registration applications for HStream Cloud.

## HServer supports using Rqlite as metadata storage

HStreamDB relies on an external storage component to store cluster metadata. Currently, Zookeeper is the default storage system for metadata. We have just adapted the architecture of HStreamDB based on the abstract metastore interface, supporting multiple metastore implementations, including the newly added Rqlite. Since Rqlite is lighter than Zookeeper, in other words, easier to deploy and manage, and it supports SQL interfaces and transactions, HStreamDB will soon set Rqlite as the default metastore.

HServer and HStream IO have achieved Rqlite support (but not yet HStore) and can be used in the latest image of HStreamDB [https://hub.docker.com/r/hstreamdb/hstream/tags](https://hub.docker.com/r/hstreamdb/hstream/tags) , via specifying the HServer startup option `--metastore-uri rq://127.0.0.1:4001`.

## HServer gRPC improvements

As mentioned in the previous [Newsletter](https://hstream.io/blog/hstreamdb-newsletter-202208), we are replacing the current gRPC library used by HServer with the self-developed Haskell gRPC library `hs_grpc` for stability, performance and other considerations. This month, hs_grpc added support for bidirectional RPC calls, and we have completed the preliminary replacement for HServer. We will continue to perform more tests, and fix any problems found in the future. HServer, based on the new gRPC library, will be included in the official release of v0.10 next month.

## A new cluster deployment tool

This month, we have also released a new HStreamDB cluster deployment tool [https://github.com/hstreamdb/deployment-tool](https://github.com/hstreamdb/deployment-tool). Compared with the previous deployment script, it provides a simplified configuration and multi-node parallel deployment support. It is written based on Golang and can be downloaded directly from [https://github.com/hstreamdb/deployment-tool/releases](https://github.com/hstreamdb/deployment-tool/releases). The basic usage is as follows:

1. Generate deployment template via `hdt init`

2. Modify the deployment configuration according to the actual environment

   ```
   global:
   user: "root"
   
   monitor:
   node_exporter_port: 9100
   cadvisor_port: 7000
   grafana_disable_login: true
   
   hserver:
   - host: 172.24.47.173
   - host: 172.24.47.174
   - host: 172.24.47.175
   
   hstore:
   - host: 172.24.47.173
     enable_admin: true
   - host: 172.24.47.174
   - host: 172.24.47.175
   
   meta_store:
   - host: 172.24.47.173
   - host: 172.24.47.174
   - host: 172.24.47.175
   
   prometheus:
   - host: 172.24.47.172
   
   grafana:
   - host: 172.24.47.172
   ```

3. Run `hdt start` to deploy [https://github.com/hstreamdb/deployment-tool/blob/main/README.md](https://github.com/hstreamdb/deployment-tool/blob/main/README.md) 

   For specific usage, please refer to [https://github.com/hstreamdb/deployment-tool/blob/main/README.md](https://github.com/hstreamdb/deployment-tool/blob/main/README.md) 

## New Rust Client

In addition, we released the Rust language client library of HStreamDB [https://github.com/hstreamdb/hstreamdb-rust](https://github.com/hstreamdb/hstreamdb-rust). The implementation is based on the asynchronous runtime [Tokio](https://docs.rs/tokio) of Rust and the gRPC library [Tonic](https://docs.rs/tonic). It only supports HStreamDB v0.9 and above, including essential operations such as stream and subscription creation and management, data writing and consumption. To download and use, refer to: https://crates.io/crates/hstreamdb.

Later, we plan to develop clients for more unsupported languages based on the FFI of Rust Client, which can reduce the maintenance cost of multi-language clients on the one hand and achieve better performance on the other hand. We have developed another experimental Erlang Client, [https://github.com/hstreamdb/hstreamdb_erl-rs](https://github.com/hstreamdb/hstreamdb_erl-rs), based on [https://github.com/rusterlium/rustler](https://github.com/rusterlium/rustler).

## Application for early access to HStream Cloud is now open

This month, we upgraded the [official HStreamDB website](http://hstream.io/). Now you can click [https://hstream.io/cloud#register](https://hstream.io/cloud#register) to submit a registration application, and we will invite you to have a free trial once it is up and running.
