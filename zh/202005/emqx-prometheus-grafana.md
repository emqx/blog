> [Prometheus](https://prometheus.io/) 是由 SoundCloud 开源监控告警解决方案，支持多维 [数据模型](https://prometheus.io/docs/concepts/data_model/)（时序由 metric 名字和 k/v 的 labels 构成），具备灵活的查询语句（[PromQL](https://prometheus.io/docs/querying/basics/)），支持多种数据采集 [exporters](https://prometheus.io/docs/instrumenting/exporters/)；支持告警管理，基于指标实现告警监控；支持多种统计数据模型，图形化展示友好，图形展示除了内置的浏览器，也支持 Grafana 集成。



物联网 MQTT 服务器 [EMQX](https://www.emqx.com/zh) 提供 [emqx_statsd](https://github.com/emqx/emqx-statsd) 插件，用于将 EMQX 运行指标及 Erlang 虚拟机状态数据输出到第三方的监控系统如 Prometheus 中。通过 Prometheus 自带的 node-exporter 还可以采集 Linux 服务器相关指标，实现服务器 + EMQX 整体运维监控。

本文提供了 Prometheus + Grafana 整套 EMQX 运维监控方案搭建过程。



## 安装与准备

### Docker 镜像下载

```bash
# Docker 镜像包下载
docker pull prom/node-exporter
docker pull prom/prometheus
docker pull prom/pushgateway
```



### 启动 node-exporter

可选，用于收集服务器指标如 CPU、内存、网络等，如果使用 Docker 安装则需要映射目标服务器响应的状态文件：

```shell
docker run -d -p 9100:9100 \
  -v "/proc:/host/proc:ro" \
  -v "/sys:/host/sys:ro" \
  -v "/:/rootfs:ro" \
  --net="host" \
  prom/node-exporter
```



###  启动 pushgateway

pushgateway 用于接收 EMQX 指标推送数据，需要保证 EMQX 能够访问：

```bash
docker run -d -p 9091:9091 prom/pushgateway
```



### 启动 Prometheus

指定配置文件与监听端口以启动 Prometheus：

```bash
# 指定配置文件并启动
docker run -p 9090:9090 \
	-v $PWD/prometheus.yaml:/etc/prometheus/prometheus.yaml \
	-d prom/prometheus \
	--config.file=/etc/prometheus/prometheus.yaml
```

Prometheus 配置文件 `prometheus.yaml` 样例如下，详细含义请参考 [Prometheus 文档](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)：

```yaml
# prometheus.yaml
global:
  scrape_interval:     10s # 默认抓取时间
  evaluation_interval: 10s # 每10秒评估一次rules

  # 在本机上每一条时间序列上都会默认产生的，主要可以用于联合查询、远程存储、Alertmanager时使用。
  external_labels:
      monitor: 'emqx-monitor'

# 加载规则,依据 evaluation_interval 来定期评估rule
rule_files:
  # - "first.rules"
  # - "second.rules"
  - "/etc/prometheus/rules/*.rules"

# 数据拉取配置
scrape_configs:
  # 表示在这个配置内的时间序例，每一条都会自动添加上这个{job_name:"prometheus"}的标签
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['127.0.0.1:9090']

	# 服务器物理机监控
  - job_name: 'node-exporter'
    scrape_interval: 5s
    static_configs:
      # node-exporter 根据实际情况填写
      - targets: ['192.168.6.11:9100']
        labels:
          instance: wivwiv-local


  # EMQX Pushgateway 监控
  - job_name: 'pushgateway'
    scrape_interval: 5s
    honor_labels: true
    static_configs:
      # pushgateway 根据实际情况填写
      - targets: ['192.168.6.11:9091']
```



### 启动 EMQX statsd 插件

打开 `etc/emqx_statsd.conf`，确认以下配置：

```bash
## pushgateway 地址
statsd.push.gateway.server = http://127.0.0.1:9091
## 数据采集/推送周期（毫秒）
statsd.interval = 15000
```

启动插件：

`./bin/emqx_ctl load plugins emqx_statsd`



## 效果查看

通过 `docker ps -a` 命令查看组件是否成功运行，等待数个推送周期后，打开 http://localhost:9090  Prometheus 控制面板查看采集数据。

> Prometheus 仅提供简单图表数据展示，如需更精美的可视化展示请结合 Grafana 使用。

![image20191205152623657.png](https://static.emqx.net/images/d4e02e402f1f4987098ed711c443bd7b.png)





## 集成 Grafana

Grafana 是一个开源、通用的度量分析与可视化展示工具，通过数据源（如各类数据库、开源组件），展示自定义报表、显示图表等。



### 启动 Grafana

通过 Docker 拉取并启动 Grafana 镜像：

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

启动成功后，浏览器访问 http://127.0.0.1:3000 打开 Dashboard 控制台。



### 配置 Prometheus 数据源

在 Grafana 中添加数据源，选择 Prometheus 并填写正确的地址完成数据源添加。

![image20200507160650116.png](https://static.emqx.net/images/6bde180d16cd79922bd7a726afce5b47.png)



### 导入 Grafana 模板数据

`emqx_statsd` 插件提供了 Grafana 的 Dashboard 的模板文件，这些模板包含了大部分 EMQX 监控数据的展示。用户可直接导入到 Grafana 中，用以显示 EMQX 的监控状态的图标。

模板文件位于[emqx_statsd/grafana_template](https://github.com/emqx/emqx-statsd/tree/master/grafana_template) 中，因 EMQX 版本差异问题，可能存在部分图表数据显示错误的情况，请用户手动调整适配。

点击 Upload.json file 按钮，导入后选择对应的文件夹与数据源即可。

![image20200507161318909.png](https://static.emqx.net/images/632ebb891bd5be0bae5e5c1939d2bbd6.png)



### 效果展示

完成整套系统搭建并运行一段时间后，Prometheus 收集到的数据将展示在 Grafana 上，默认模板展示效果如下：

- EMQ Dashboard：包含连接、消息、主题、吞吐量历史统计
- EMQ：包含客户端数、订阅数、主题数、消息数、报文数等业务信息历史统计
- ErlangVM：每个 EMQX 节点 Erlang 虚拟机进程/线程数量，ETS/Mnesia 数据库使用情况历史统计

**如有其他需求，可以参照 「附：emqx-statsd 所有指标」并结合 Grafana 进行图标数据编排展示**。



![image20200507161914310.png](https://static.emqx.net/images/dd7babe4c66f789c8d05b553b41d9168.png)

![image20200507161948328.png](https://static.emqx.net/images/18917f9ea67938d2cb00352275b926f3.png)


![image20200507162019439.png](https://static.emqx.net/images/31cc134182b8b307791a9583a2bdbb9f.png)

## 告警管理

Prometheus 与 Grafana 均支持指标告警功能，配置告警规则后，服务器会不断评估设置的规则与当前指标数据，在规则条件符合的时候发送出通知。

篇幅有限，告警相关配置与实践请关注后续文章。



## 附：emqx-statsd 所有指标

[EMQX](https://www.emqx.com/zh) MQTT 服务器通过 Prometheus push gateway 推送指标数据，支持的指标项如下：

```bash
# TYPE erlang_vm_ets_limit gauge
erlang_vm_ets_limit 256000
# TYPE erlang_vm_logical_processors gauge
erlang_vm_logical_processors 4
# TYPE erlang_vm_logical_processors_available gauge
erlang_vm_logical_processors_available NaN
# TYPE erlang_vm_logical_processors_online gauge
erlang_vm_logical_processors_online 4
# TYPE erlang_vm_port_count gauge
erlang_vm_port_count 16
# TYPE erlang_vm_port_limit gauge
erlang_vm_port_limit 1048576
# TYPE erlang_vm_process_count gauge
erlang_vm_process_count 320
# TYPE erlang_vm_process_limit gauge
erlang_vm_process_limit 2097152
# TYPE erlang_vm_schedulers gauge
erlang_vm_schedulers 4
# TYPE erlang_vm_schedulers_online gauge
erlang_vm_schedulers_online 4
# TYPE erlang_vm_smp_support untyped
erlang_vm_smp_support 1
# TYPE erlang_vm_threads untyped
erlang_vm_threads 1
# TYPE erlang_vm_thread_pool_size gauge
erlang_vm_thread_pool_size 4
# TYPE erlang_vm_time_correction untyped
erlang_vm_time_correction 1
# TYPE erlang_vm_statistics_context_switches counter
erlang_vm_statistics_context_switches 20767
# TYPE erlang_vm_statistics_garbage_collection_number_of_gcs counter
erlang_vm_statistics_garbage_collection_number_of_gcs 3924
# TYPE erlang_vm_statistics_garbage_collection_words_reclaimed counter
erlang_vm_statistics_garbage_collection_words_reclaimed 6751048
# TYPE erlang_vm_statistics_garbage_collection_bytes_reclaimed counter
erlang_vm_statistics_garbage_collection_bytes_reclaimed 54008384
# TYPE erlang_vm_statistics_bytes_received_total counter
erlang_vm_statistics_bytes_received_total 23332
# TYPE erlang_vm_statistics_bytes_output_total counter
erlang_vm_statistics_bytes_output_total 21266
# TYPE erlang_vm_statistics_reductions_total counter
erlang_vm_statistics_reductions_total 18413181
# TYPE erlang_vm_statistics_run_queues_length_total gauge
erlang_vm_statistics_run_queues_length_total 0
# TYPE erlang_vm_statistics_runtime_milliseconds counter
erlang_vm_statistics_runtime_milliseconds 1782
# TYPE erlang_vm_statistics_wallclock_time_milliseconds counter
erlang_vm_statistics_wallclock_time_milliseconds 68277
# TYPE erlang_vm_memory_atom_bytes_total gauge
erlang_vm_memory_atom_bytes_total{usage="used"} 1507142
erlang_vm_memory_atom_bytes_total{usage="free"} 18787
# TYPE erlang_vm_memory_bytes_total gauge
erlang_vm_memory_bytes_total{kind="system"} 63949544
erlang_vm_memory_bytes_total{kind="processes"} 45457848
# TYPE erlang_vm_dets_tables gauge
erlang_vm_dets_tables 0
# TYPE erlang_vm_ets_tables gauge
erlang_vm_ets_tables 115
# TYPE erlang_vm_memory_processes_bytes_total gauge
erlang_vm_memory_processes_bytes_total{usage="used"} 45457696
erlang_vm_memory_processes_bytes_total{usage="free"} 152
# TYPE erlang_vm_memory_system_bytes_total gauge
erlang_vm_memory_system_bytes_total{usage="atom"} 1525929
erlang_vm_memory_system_bytes_total{usage="binary"} 104504
erlang_vm_memory_system_bytes_total{usage="code"} 26779999
erlang_vm_memory_system_bytes_total{usage="ets"} 7685312
erlang_vm_memory_system_bytes_total{usage="other"} 27853800
# TYPE erlang_mnesia_held_locks gauge
erlang_mnesia_held_locks 0
# TYPE erlang_mnesia_lock_queue gauge
erlang_mnesia_lock_queue 0
# TYPE erlang_mnesia_transaction_participants gauge
erlang_mnesia_transaction_participants 0
# TYPE erlang_mnesia_transaction_coordinators gauge
erlang_mnesia_transaction_coordinators 0
# TYPE erlang_mnesia_failed_transactions counter
erlang_mnesia_failed_transactions 21
# TYPE erlang_mnesia_committed_transactions counter
erlang_mnesia_committed_transactions 128
# TYPE erlang_mnesia_logged_transactions counter
erlang_mnesia_logged_transactions 3
# TYPE erlang_mnesia_restarted_transactions counter
erlang_mnesia_restarted_transactions 0
# TYPE emqx_connections_count gauge
emqx_connections_count 0
# TYPE emqx_connections_max gauge
emqx_connections_max 0
# TYPE emqx_sessions_count gauge
emqx_sessions_count 0
# TYPE emqx_sessions_max gauge
emqx_sessions_max 0
# TYPE emqx_topics_count gauge
emqx_topics_count 0
# TYPE emqx_topics_max gauge
emqx_topics_max 0
# TYPE emqx_suboptions_count gauge
emqx_suboptions_count 0
# TYPE emqx_suboptions_max gauge
emqx_suboptions_max 0
# TYPE emqx_subscribers_count gauge
emqx_subscribers_count 0
# TYPE emqx_subscribers_max gauge
emqx_subscribers_max 0
# TYPE emqx_subscriptions_count gauge
emqx_subscriptions_count 0
# TYPE emqx_subscriptions_max gauge
emqx_subscriptions_max 0
# TYPE emqx_subscriptions_shared_count gauge
emqx_subscriptions_shared_count 0
# TYPE emqx_subscriptions_shared_max gauge
emqx_subscriptions_shared_max 0
# TYPE emqx_routes_count gauge
emqx_routes_count 0
# TYPE emqx_routes_max gauge
emqx_routes_max 0
# TYPE emqx_retained_count gauge
emqx_retained_count 3
# TYPE emqx_retained_max gauge
emqx_retained_max 3
# TYPE emqx_vm_cpu_use gauge
emqx_vm_cpu_use 12.029950083194677
# TYPE emqx_vm_cpu_idle gauge
emqx_vm_cpu_idle 87.97004991680532
# TYPE emqx_vm_run_queue gauge
emqx_vm_run_queue 1
# TYPE emqx_vm_process_messages_in_queues gauge
emqx_vm_process_messages_in_queues 0
# TYPE emqx_bytes_received counter
emqx_bytes_received 0
# TYPE emqx_bytes_sent counter
emqx_bytes_sent 0
# TYPE emqx_packets_received counter
emqx_packets_received 0
# TYPE emqx_packets_sent counter
emqx_packets_sent 0
# TYPE emqx_packets_connect counter
emqx_packets_connect 0
# TYPE emqx_packets_connack_sent counter
emqx_packets_connack_sent 0
# TYPE emqx_packets_connack_error counter
emqx_packets_connack_error 0
# TYPE emqx_packets_connack_auth_error counter
emqx_packets_connack_auth_error 0
# TYPE emqx_packets_publish_received counter
emqx_packets_publish_received 0
# TYPE emqx_packets_publish_sent counter
emqx_packets_publish_sent 0
# TYPE emqx_packets_publish_inuse counter
emqx_packets_publish_inuse 0
# TYPE emqx_packets_publish_error counter
emqx_packets_publish_error 0
# TYPE emqx_packets_publish_auth_error counter
emqx_packets_publish_auth_error 0
# TYPE emqx_packets_publish_dropped counter
emqx_packets_publish_dropped 0
# TYPE emqx_packets_puback_received counter
emqx_packets_puback_received 0
# TYPE emqx_packets_puback_sent counter
emqx_packets_puback_sent 0
# TYPE emqx_packets_puback_inuse counter
emqx_packets_puback_inuse 0
# TYPE emqx_packets_puback_missed counter
emqx_packets_puback_missed 0
# TYPE emqx_packets_pubrec_received counter
emqx_packets_pubrec_received 0
# TYPE emqx_packets_pubrec_sent counter
emqx_packets_pubrec_sent 0
# TYPE emqx_packets_pubrec_inuse counter
emqx_packets_pubrec_inuse 0
# TYPE emqx_packets_pubrec_missed counter
emqx_packets_pubrec_missed 0
# TYPE emqx_packets_pubrel_received counter
emqx_packets_pubrel_received 0
# TYPE emqx_packets_pubrel_sent counter
emqx_packets_pubrel_sent 0
# TYPE emqx_packets_pubrel_missed counter
emqx_packets_pubrel_missed 0
# TYPE emqx_packets_pubcomp_received counter
emqx_packets_pubcomp_received 0
# TYPE emqx_packets_pubcomp_sent counter
emqx_packets_pubcomp_sent 0
# TYPE emqx_packets_pubcomp_inuse counter
emqx_packets_pubcomp_inuse 0
# TYPE emqx_packets_pubcomp_missed counter
emqx_packets_pubcomp_missed 0
# TYPE emqx_packets_subscribe_received counter
emqx_packets_subscribe_received 0
# TYPE emqx_packets_subscribe_error counter
emqx_packets_subscribe_error 0
# TYPE emqx_packets_subscribe_auth_error counter
emqx_packets_subscribe_auth_error 0
# TYPE emqx_packets_suback_sent counter
emqx_packets_suback_sent 0
# TYPE emqx_packets_unsubscribe_received counter
emqx_packets_unsubscribe_received 0
# TYPE emqx_packets_unsubscribe_error counter
emqx_packets_unsubscribe_error 0
# TYPE emqx_packets_unsuback_sent counter
emqx_packets_unsuback_sent 0
# TYPE emqx_packets_pingreq_received counter
emqx_packets_pingreq_received 0
# TYPE emqx_packets_pingresp_sent counter
emqx_packets_pingresp_sent 0
# TYPE emqx_packets_disconnect_received counter
emqx_packets_disconnect_received 0
# TYPE emqx_packets_disconnect_sent counter
emqx_packets_disconnect_sent 0
# TYPE emqx_packets_auth_received counter
emqx_packets_auth_received 0
# TYPE emqx_packets_auth_sent counter
emqx_packets_auth_sent 0
# TYPE emqx_messages_received counter
emqx_messages_received 0
# TYPE emqx_messages_sent counter
emqx_messages_sent 0
# TYPE emqx_messages_qos0_received counter
emqx_messages_qos0_received 0
# TYPE emqx_messages_qos0_sent counter
emqx_messages_qos0_sent 0
# TYPE emqx_messages_qos1_received counter
emqx_messages_qos1_received 0
# TYPE emqx_messages_qos1_sent counter
emqx_messages_qos1_sent 0
# TYPE emqx_messages_qos2_received counter
emqx_messages_qos2_received 0
# TYPE emqx_messages_qos2_sent counter
emqx_messages_qos2_sent 0
# TYPE emqx_messages_publish counter
emqx_messages_publish 0
# TYPE emqx_messages_dropped counter
emqx_messages_dropped 0
# TYPE emqx_messages_dropped_expired counter
emqx_messages_dropped_expired 0
# TYPE emqx_messages_dropped_no_subscribers counter
emqx_messages_dropped_no_subscribers 0
# TYPE emqx_messages_forward counter
emqx_messages_forward 0
# TYPE emqx_messages_retained counter
emqx_messages_retained 2
# TYPE emqx_messages_delayed counter
emqx_messages_delayed 0
# TYPE emqx_messages_delivered counter
emqx_messages_delivered 0
# TYPE emqx_messages_acked counter
emqx_messages_acked 0
# TYPE emqx_delivery_dropped counter
emqx_delivery_dropped 0
# TYPE emqx_delivery_dropped_no_local counter
emqx_delivery_dropped_no_local 0
# TYPE emqx_delivery_dropped_too_large counter
emqx_delivery_dropped_too_large 0
# TYPE emqx_delivery_dropped_qos0_msg counter
emqx_delivery_dropped_qos0_msg 0
# TYPE emqx_delivery_dropped_queue_full counter
emqx_delivery_dropped_queue_full 0
# TYPE emqx_delivery_dropped_expired counter
emqx_delivery_dropped_expired 0
# TYPE emqx_client_connected counter
emqx_client_connected 0
# TYPE emqx_client_authenticate counter
emqx_client_authenticate 0
# TYPE emqx_client_auth_anonymous counter
emqx_client_auth_anonymous 0
# TYPE emqx_client_check_acl counter
emqx_client_check_acl 0
# TYPE emqx_client_subscribe counter
emqx_client_subscribe 0
# TYPE emqx_client_unsubscribe counter
emqx_client_unsubscribe 0
# TYPE emqx_client_disconnected counter
emqx_client_disconnected 0
# TYPE emqx_session_created counter
emqx_session_created 0
# TYPE emqx_session_resumed counter
emqx_session_resumed 0
# TYPE emqx_session_takeovered counter
emqx_session_takeovered 0
# TYPE emqx_session_discarded counter
emqx_session_discarded 0
# TYPE emqx_session_terminated counter
emqx_session_terminated 0
```
