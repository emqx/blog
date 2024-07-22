## はじめに

リーディングなMQTTプラットフォームであるEMQXは、クラスタースケーリングをサポートし、高性能で可用性を確保します。クラスター展開では、通常NGINX、HAProxyなどのリバースプロキシを使用して、ロードバランシング、SSL/TLSの終了、フェイルオーバーなどの目的を達成します。

プロキシはMQTTクライアントの代わりにEMQXに接続するため、EMQXはクライアントの実際のIPを直接取得できません。この制限により、セキュリティ監査やアクセス制限などのIPベースのアプリケーションを実施するのに不便が生じます。

この記事では、[NGINX 1.26.1](https://nginx.org/en/download.html) と [EMQX 5.7.0](https://www.emqx.com/en/downloads-and-install/broker?os=Ubuntu) を例に、NGINXリバースプロキシを使用する場合に、PROXYプロトコルまたは `X-Forwarded-For` ヘッダーを通じてMQTTクライアントの実際のIPを取得する方法を説明します。

## TCP経由でのMQTTクライアントの実際のIPの取得

### 単一階層のプロキシ

単一階層のプロキシとは、MQTTクライアントとバックエンドサーバーの間に1つのロードバランサーのみがあることを意味します。これは最も一般的なケースです。

```
クライアント -> ロードバランサー(NGINX、HAProxy、...) -> サーバー(EMQX)
```

この場合、[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用して実際のクライアントのIPを渡すことができます。

最初に[HAProxy](https://www.haproxy.org/)によって提案され設計されたPROXYプロトコルは、TCPプロキシがクライアントの元のIPやポートなどのメタデータをカプセル化し、戻り値として渡す仕様です。PROXYプロトコルは、TCP接続をリレーする際にプロキシを使用する場合にクライアントの元のIPアドレスとポートを取得する優れた解決策となっています。

PROXYプロトコルを使用する前に：

```
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <CONNECT packet> | ... + ------ +
| MQTT Client |  ----------------------> | Load Balancer| ----------------------> | Server |
+ ----------- +                          + ------------ +                         + ------ +
```

PROXYプロトコルを使用する後：

```
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <PROXY protocol header> | <CONNECT packet> | ... + ------ +
| MQTT Client |  ----------------------> | Load Balancer| ------------------------------------------------> | Server |
+ ----------- +                          + ------------ +                                                   + ------ +
```

以下は、標準的なPROXYプロトコルヘッダーの例です。

```
PROXY TCP 172.168.0.116 172.168.0.200 39826 1883
|     |   |             |             |     |
|     |   |             |             |     Destination Port
|     |   |             |             Source Port
|     |   |             Destination IP
|     |   Source IP
|     Indicates this is an IPv4 TCP connection
Fixed prefix to identify the PROXY protocol
```

PROXYプロトコルは現在、v1とv2の2つのバージョンで利用可能です。v1は前述の人間が読めるテキスト形式であり、v2はプログラムのパース効率を向上させるために機械が読めるバイナリ形式に変更されました。v2の具体的な形式はこの記事では展開されません。興味のある読者は、[The PROXY protocol Version 1 & 2](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) を参照してもっと学ぶことができます。EMQXはv1とv2の両方をサポートしており、使用されたバージョンの自動検出も可能です。この記事では、デモンストレーションのためにv1を使用します。

#### 設定

NGINXを取り上げます。まずNGINXの設定を変更する必要があります（インストール手順は[こちら](https://nginx.org/en/docs/install.html)をクリック）。`/etc/nginx/nginx.conf`を開いて、以下の設定を追加します。

```
stream {
  upstream server {
    # 実際のIPとリスンポートに変更してください
    server 172.16.0.71:1883;
  }

  server {
    listen 1883;
    proxy_pass server;
    # PROXYプロトコル送信を有効にする
    proxy_protocol on;
  }
}
```

上記の設定では、NGINXはポート1883をリスンし、受信データをアドレス`172.16.0.71:1883`のサーバーに転送します。PROXYプロトコルが有効になっているため、NGINXは接続確立後に**最初に**PROXYプロトコルヘッダーを送信します。

設定を保存した後、以下のコマンドを実行して設定をリロードします。

```
nginx -s reload
```

次に、EMQX（インストール手順は[こちら](https://docs.emqx.com/en/emqx/latest/deploy/install.html)をクリック）の設定も変更する必要があります。ブラウザでダッシュボードを開き、「Management」>「Cluster Settings」>「MQTT Settings」へ進み、デフォルトのTCPリスナー（または変更したい任意のリスナー）をクリックして設定ページに入り、「Proxy Protocol」をtrueに設定します。

![01dashboardproxyprotocolen.png](https://assets.emqx.com/images/924dca9152db0d0cb9c5c7bf985e2679.png)

EMQXリスナーの変更は、「Update」をクリック後すぐに有効になります。

#### 確認

この例では、各ホストのIPは以下の通りです。

```
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- +
```

NGINXがPROXYプロトコルヘッダーを正しく送信していることを確認するために、EMQXを実行しているホストでネットワークパケットをキャプチャする以下のコマンドを使用できます。

```
# -i eth0, ネットワークインターフェースeht0でパケットをキャプチャ
# -s 0, 完全なパケットをキャプチャ
# -vv, より詳細な出力を表示
# -n, アドレス（つまり、ホストアドレス、ポート番号など）を名前に変換しない
# -X, 16進数とASCIIでパケットごとのデータを印刷
# -S, 絶対のTCPシーケンス番号を印刷するのではなく、相対のシーケンス番号を印刷する
# 'port 1883', ソースまたは宛先ポートが1883であるすべてのパケットをキャプチャ
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

次に、MQTTX CLI（インストール手順は[こちら](https://mqttx.app/docs/cli/downloading-and-installation)をクリック）を使用して、NGINXをMQTTクライアントとして接続します。

```
# 実際のNGINX IPに121.36.192.227を変更してください
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx
```

`tcpdump`でキャプチャしたパケット内で、NGINX（`172.16.0.116`）がEMQX（`172.16.0.71`）とのTCP接続を確立した後、最初にクライアントのIPが`115.236.21.86`であるPROXYプロトコルヘッダーを送信していることが確認できます。

![02capturedpackets.png](https://assets.emqx.com/images/43fc0ee2bef859a6754fac86a32562a1.png)

EMQXのCLIコマンドを使用すると、EMQXがクライアントのソースIPアドレスとポートを正常に取得していることも確認できます。

```shell
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61177, ...)
```

### 複数階層のプロキシ

いくつかの大規模で複雑な展開では、プロキシの複数の階層がある場合があります。たとえば：

```
+ ----------- +        + ---- +       + ---- +       + ------ +
| MQTT Client |  ----> | LB 1 | ----> | LB 2 | ----> | Server |
+ ----------- +        + ---- +       + ---- +       + ------ +
```

リバースプロキシが複数ある場合、バックエンドのEMQXがクライアントの実際のIPを取得できるように、NGINXの設定をいくつか調整する必要があります。

まず、最も外側のLB、LB 1は、クライアントのソースIPとソースポートを渡すためにPROXYプロトコルの送信を有効にする必要があります。

各TCP接続は、PROXYプロトコルヘッダーを一度しか送信できないため、LBは受信したPROXYプロトコルヘッダーを転送し、さらに自分のヘッダーを送信することはできません。以下の状況は許可されていません。

```
+ ----------- +     + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | <PP header 1> | ...  + ------ +
| MQTT Client |  -> | LB 1 | --------------------> | LB 2 | ------------------------------------> | Server |
+ ----------- +     + ---- +                       + ---- +                                       + ------ +
```

> PPヘッダーはPROXYプロトコルヘッダーの略称です。

したがって、中間LBの2つの設定方法があります。第1の方法は最も簡単で、中間LBはPROXYプロトコルの解析や送信を有効にする必要はなく、LB 1によって送信されたすべてのパケットをパススルーするだけです。

```
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 1> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
```

第2の方法では、中間LBはPROXYプロトコルの解析と送信の両方を有効にする必要があります。

各LBはPROXYプロトコルヘッダーを受け取り、クライアントのソースIPアドレスとポートを取得し、それらを送信するPROXYプロトコルヘッダーに設定します。

```
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
PP header 2 = "PROXY TCP <Client IP> <LB 2 IP> <Client Port> <LB 2 Port>"
```

#### パススルー

LB 1とLB 2は両方ともNGINXを使用しており、以下はパススルー設定の例です。

```
# LB 1
# PROXYプロトコル送信を有効にする
stream {
  upstream proxy2 {
    # 実際のLB 2 IPとリスンポートに変更してください
    server 172.16.0.200:1883;
  }

  server {
    listen 1883;
    proxy_pass proxy2;
    # PROXYプロトコル送信を有効にする
    proxy_protocol on;
  }
}

# LB 2
# PROXYプロトコルの解析と送信を有効にしない
stream {
  upstream server {
    # 実際のEMQX IPとリスンポートに変更してください
    server 172.16.0.71:1883;
  }

  server {
    listen 1883;
    proxy_pass server;
  }
}
```

EMQXは引き続きPROXYプロトコルを有効にし、他の変更は必要ありません。

#### 確認

LBが追加されたため、この例のホストIPはパススルーの場合と同じです。

```
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ------------------------+    + ---------------------- +    + -------------------- +    + ------------------- +
```

LB 2上で以下のコマンドを実行してパケットをキャプチャします。

```shell
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

次に、MQTTX CLIを使用してLB 1をMQTTクライアントとして接続します。

```shell
# 実際の最も外側のLBのIPに121.36.192.227を変更してください
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

キャプチャされたパケット内で、LB 2がLB 1からPROXYプロトコルヘッダーを受け取り、クライアントのIPが`115.236.21.86`であることを示しており、LB 2のEMQXへの接続でヘッダーの内容は変更されていないことが確認でき、パススルーが有効であることを示します。

![03capturedpacketspassthrough.png](https://assets.emqx.com/images/7fbfddf4a74987d46932d727e5816e07.png)

EMQXのCLIコマンドを使用すると、EMQXがクライアントの実際のIPとポートを正常に取得していることも確認できます。

```shell
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:18936, ...)
```

#### 非パススルー

設定は以下の通りです。

```
# LB 1
# パススルーと同じ設定でPROXYプロトコル送信を有効にする
stream {
  upstream proxy2 {
    server 172.16.0.200:1883;
  }

  server {
    listen 1883;
    proxy_pass proxy2;
    proxy_protocol on;
  }
}

# LB 2
# PROXYプロトコルの解析と送信を有効にする。
# もしさらなる中間LBがあれば、
# 設定はLB 2と同じで、対応するIPとポートのみ変更する
stream {
  upstream server {
    server 172.16.0.71:1883;
  }

  server {
    # PROXYプロトコルの解析を有効にする
    listen 1883 proxy_protocol;
    proxy_pass server;
    # PROXYプロトコル送信を有効にする
    proxy_protocol on;

    # 信頼できるアドレスを設定し、172.16.0.0/24を
    # 信頼できるプロキシのIPアドレスまたはCIDR範囲に変更する
    set_real_ip_from 172.16.0.0/24;

    # LB 1のWAN IPを信頼できるアドレスに設定する
    # set_real_ip_from 172.16.0.116
  }
}
```

ご存じのように、`set_real_ip_from` ディレクティブを使用して、信頼できるLBのIPアドレスまたはCIDRアドレス範囲を指定する必要があります。NGINXは、信頼できるソースのPROXYプロトコルヘッダーからのみクライアントの実際のソースIPを取得します。そうでなければ、LB 2はサーバーにPROXYプロトコルヘッダーを送信する際に、クライアントのIPではなくLB 1のIPをソースIPとして使用することになります。

```
       + ---- +  PROXY TCP <LB 1 IP> <LB 2 IP> <LB 1 Port> <LB 2 Port>  + ------ + 
... -> | LB 2 | ------------------------------------------------------> | Server |
       + ---- +                                                         + ------ +
```

`set_real_ip_from` ディレクティブは、Stream Real-IPモジュールに依存しています。現在のNGINXインストールにこのモジュールが含まれているかを確認するには、以下のコマンドを使用します。

```
nginx -V 2>&1 | grep -- 'stream_realip_module'
```

もし含まれていなければ、NGINXを手動でコンパイルし、ビルド時にこのモジュールを含める必要があります。詳細については[Installing NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)を参照してください。

#### 確認

この例では、各ホストのIPはパススルーの場合と同じです。

```
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

LB 2上で以下のコマンドを実行してパケットをキャプチャします。

```shell
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

次に、MQTTX CLIを使用してLB 1に接続します。

```shell
# 実際の最も外側のLBのIPに121.36.192.227を変更してください
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

キャプチャされたパケット内で、LB 2がLB 1からPROXYプロトコルヘッダーを受け取り、クライアントのIPが`115.236.21.86`であることを示しています。LB 2のEMQXへの接続で、ヘッダーの内容は変更されていますが、それでもクライアントの実際のIPを正しく示しており、`set_real_ip_from` ディレクティブが機能していることを示します。

![04capturedpacketsnonpassthrough.png](https://assets.emqx.com/images/21da88079455e5ba2518f61589db4798.png)

EMQXのCLIコマンドを使用すると、EMQXがクライアントの実際のIPとポートを正常に取得していることも確認できます。

```shell
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:39817, ...)
```

## WebSocket経由でのMQTTクライアントの実際のIPの取得

ブラウザやWeChatミニプログラムなどのWebアプリケーションでは、クライアントがMQTT over WebSocketを使ってEMQXにアクセスすることがあります。WebSocketはヘッダーを運べるため、PROXYプロトコルに加えて、`X-Forwarded-For` ヘッダーを使ってLBとアプリケーションサーバーの間でクライアントの実際のIPを渡すことができます。

MQTT over WebSocketクライアントの実際のIPを取得する場合、NGINXとEMQXの設定は、MQTT over TCPクライアントの実際のIPを取得する場合と同じです。したがって、ここでは詳細には触れません。

次に、NGINXとEMQXを設定して、`X-Forwarded-For` ヘッダーを使ってクライアントの実際のIPを取得する方法に焦点を当てます。

### 単一階層のプロキシ

最も一般的な単一階層のプロキシから始めましょう。NGINXのサンプル設定は以下の通りです。

```
http {
  upstream server {
    server 172.16.0.71:8083;
  }

  server {
    listen 8083;
    # /mqttをWebSocketサービスを提供するエンドポイントとして使用
    location /mqtt {
      proxy_pass <http://server;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

クライアントがMQTT over WebSocketを使ってEMQXにアクセスする準備をすると、NGINXは`Upgrade`および`Connection`ヘッダーをEMQXに自動的に転送しませんので、NGINXを設定してこれらの2つのヘッダーを明示的に渡す必要があります。これにより、EMQXはクライアントがWebSocketプロトコルに切り替えようとしていることを理解します。

NGINXの`proxy_set_header` ディレクティブを使用すると、NGINXがバックエンドに渡す要求ヘッダーを変更または設定できます。

```
# $http_*はNGINXの組み込み変数で、NGINXによって受信された指定のHTTPヘッダーの値です。
# したがって、$http_upgradeの値はNGINXによって受信された要求のUpgradeヘッダーです。
# このディレクティブは、NGINXによって送信されるUpgradeヘッダーを"websocket"に設定するのに相当します。
proxy_set_header Upgrade $http_upgrade;

# Connectionヘッダーを"Upgrade"に設定すると、Upgradeヘッダーにリストされたプロトコルへのアップグレード要求を示します。
proxy_set_header Connection "Upgrade";
```

`$remote_addr` と `$remote_port` は、NGINXの組み込み変数で、ピアのIPアドレスとポートを記録します。ただし、複数階層のプロキシシナリオでは、ピアはクライアントに近いダウンストリームLB（クライアントに近い）でもあります。

もちろん、単一階層のプロキシシナリオでは、`$remote_*` を直接使用してMQTTクライアントのIPアドレスとポートを取得できます。

```
# クライアントによって要求されたホスト名をHostヘッダーに設定
proxy_set_header Host $host;

# MQTTクライアントのソースIPを渡すためにX-Forwarded-Forを設定
proxy_set_header X-Forwarded-For $remote_addr;

# MQTTクライアントのソースポートを渡すためにX-Forwarded-Portを設定
proxy_set_header X-Forwarded-Port $remote_port;
```

> `X-Forwarded-Port` は、`$server_port` に設定してクライアントによってアクセスされたポートを示すことができますので、上位のアプリケーションはエントリーポイントに応じて異なるサービスを提供できます。この記事では、主に `X-Forwarded-Port` を使用して、元のクライアントのソースポートを渡す方法に焦点を当てています。

上記の設定を `/etc/nginx/nginx.conf` に保存し、`nginx -s reload` を実行して設定をリロードします。

次に、EMQXのリスナー設定を変更する必要があります。ブラウザでダッシュボードを開き、「Management」>「Cluster Settings」>「MQTT Settings」へ進み、デフォルトのWebSocketリスナー（または変更したい任意のリスナー）をクリックして設定ページに入り、「Advanced Settings」を展開し、以下の設定を「Custom Configuration」に貼り付け、「Update」をクリックします。

```
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

上記の設定では、EMQXはWebSocketアップグレード要求で受信した `X-Forwarded-For` ヘッダーの左側のIPをクライアントソースIPとして、`X-Forwarded-Port` ヘッダーの左側のポートをクライアントソースポートとして取得することを意味します。

#### 確認

この例では、ホストのIPは以下の通りです。

```
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- +
```

EMQXが実行されているホスト上で以下のコマンドを実行してパケットをキャプチャします。

```shell
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

次に、MQTTX CLIを使用してLB 1に接続します。

```shell
# 実際の最も外側のLBのIPに121.36.192.227を変更してください
mqttx conn -h 121.36.192.227 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

キャプチャされたパケット内で、LBがEMQXとのTCP接続を確立した後、`X-Forwarded-For` の `115.236.21.86` と `X-Forwarded-Port` の `61813` を伴うプロトコルアップグレードのHTTP要求を送信していることが確認でき、それぞれが実際のクライアントのソースIPアドレスとソースポートに対応しています。

![05xforwardedforlbtoemqx.png](https://assets.emqx.com/images/d4796541525ed8e4ebd024ddf6e5f220.png)

EMQXのCLIコマンドを使用すると、EMQXがMQTTクライアントの実際のIPとポートを正常に取得していることも確認できます。

```shell
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61813, ...)
```

### 複数階層のプロキシ

複数階層のプロキシシナリオでは、`X-Forwarded-For` を使用してクライアントの実際のIPをプロキシを介してバックエンドアプリケーションサーバーに渡し、要求のソースを認識し、異なるサービスを提供できるようにします。

しかし、実際には、LBがダウンストリームIPを `X-Forwarded-For` ヘッダーに追加するだけでは不十分です。クライアント側の悪意のあるなりすましを考慮する必要があります。なぜなら、クライアント側も `X-Forwarded-For` ヘッダーを設定できるからです。

前の単一階層のプロキシシナリオでは、クライアントのソースIPを使用して `X-Forwared-For` を強制的に上書きし、サーバーによって最終的に取得される `X-Forwarded-For` が必ずしも実際で正しいことを保証しました。

複数階層のプロキシシナリオは異なります。何もしないと、クライアントは偽のIPを装い、サーバーを欺いてセキュリティ管理ポリシーを迂回することができます。たとえば、以下のケースでは、アプリケーションサーバーは誤って `<Fake IP>` をクライアントの実際のIPと誤解します。

```
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | LB 1 | ----------------------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | --------------------------------------------------------> | Server |
     + ---- +                                                           + ------ +
```

通常は2つの方法でこの問題を解決します。第1の方法は、最も単純で、最も外側のLBがクライアントが偽造する可能性のある `X-Forwarded-For` を無視し、`$remote_addr` を直接 `X-Forwarded-For` に割り当てることです。

```shell
# 上書き
proxy_set_header X-Forwarded-For $remote_addr;
# 追加
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

期待される結果：

```
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Real Client IP>
| Client |  ---------------------------> | LB 1 | -----------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | ---------------------------------------------> | Server |
     + ---- +                                                + ------ +
```

第2の方法は、すべてのLBが元の `X-Forwarded-For` にリモートIPを追加し、最も内側のLBで信頼できるアドレスを設定することです。

この内側のLBは、右から左へ探索し、最初に信頼されていないIPをクライアントの実際のIPとして取得します。

```
+ ------ +   X-Forwarded-For: <Fake IP>  + ------------ +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | Trusted LB 1 | ----------------------------------------------...
+ ------ +                               + ------------ +

     + ------------ +  X-Forwarded-For: <Fake IP ✘>, <Real Client IP ✘>, <Trusted LB 1 IP ✔︎>  + ------ +
..-> | Trusted LB 2 | ----------------------------------------------------------------------> | Server |
     + ------------ +                                                                         + ------ +
```

この場合、クライアントが `X-Forwarded-For` を偽造しても、要求がアプリケーションサーバーに到達するとき、偽造されたIPは `X-Forwarded-For` の左側にしか存在しません。すべての信頼できるIPを右から左へ取り除けば、最初に信頼されていないIPは、最も外側の信頼できるLBによって追加されたクライアントの実際のIPでなければなりません。

#### 方法 1: $remote_addr を使用

```
# LB 1
# X-Forwarded-ForとX-Forwarded-Portの値を上書き
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }

  server {
    listen 8083;
    location /mqtt {
      proxy_pass <http://proxy2;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}

# LB 2
# 元のX-Forwarded-ForとX-Forwarded-Portに追加
http {        
  upstream server {
    server 172.16.0.71:8083;
  }

  server {
    listen 8083;

    location /mqtt {
      proxy_pass <http://server;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";

    }
  }
}
```

上記の設定をLB 1とLB 2にそれぞれ保存し、`nginx -s reload` を実行して再読み込みします。

EMQXの設定は、単一階層のプロキシの場合と同じです。

```
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

#### 確認

`X-Forwarded-For` ヘッダーをMQTTX CLIで偽造できないため、効果を確認するために、MQTTクライアントを実行しているホストに追加のNGINXを展開し、以下の設定で偽のX-Forwarded-Forヘッダーを`127.0.0.1`の値で設定します。

```
http {
  upstream proxy1 {
    # 実際のLB 1の公開IPとリスンポートに変更してください。
    server 121.36.192.227:8083;
  }

  server {
    listen 8083;
    location /mqtt {
      proxy_pass <http://proxy1;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

ホストのIPは以下の通りです。

```
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- + | MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                | | *********************** | -> | ********************** | -> | ******************** | -> | ******************* | | LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 | | WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           | + ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

LB 1とLB 2の両ホストで以下のコマンドを実行してネットワークパケットをキャプチャします。

```shell
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

MQTTX CLIを実行し、リモートLB 1の代わりにローカルNGINXに接続します。

```shell
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

キャプチャされたパケット内で、LB 1が`X-Forwarded-For` の `127.0.0.1` を持つWebSocketアップグレード要求を受け取っていることが確認でき、これは悪意のあるMQTTクライアントがサーバーを欺いてローカル接続であると見せかけようとしていることに相当します。

しかし、LB 1は要求の元がどこであるかを知っており、LB 2に送信するWebSocketアップグレード要求で、クライアントの偽の `X-Forwarded-For` は無視され、`X-Forwarded-For` は現在接続しているクライアントの実際のIPである `1.94.170.163` に設定されます。つまり、最終的にサーバーが取得するのは、元のクライアントの正しいソースIPであり、`X-Forwarded-Port` も同様です。

![06remoteaddr.png](https://assets.emqx.com/images/047cbd09133378a8b7fec77cce8a44db.png)

EMQXのCLIコマンドを使用すると、EMQXがMQTTクライアントの実際のIPとポートを正常に取得していることも確認できます。

```shell
$ mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:52662, ...)
```

#### 方法 2: 信頼できるアドレスの設定

`real_ip_recursive` ディレクティブの効果を確認するために、LB 3として追加のホストを追加します。LB 1とLB 2の違いは、アップストリームのIPのみです。

```
# LB 1
# 元のX-Forwarded-ForとX-Forwarded-Portに追加
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }

  server {
    listen 8083;
    location /mqtt {
      proxy_pass <http://proxy2;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 2
# 元のX-Forwarded-ForとX-Forwarded-Portに追加
http {        
  upstream proxy3 {
    server 172.16.0.225:8083;
  }

  server {
    listen 8083;

    location /mqtt {
      proxy_pass <http://proxy3;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 3
# 元のX-Forwarded-ForとX-Forwarded-Portに追加
# X-Forwarded-Forからクライアントの実際のIPを取得し、X-Real-IPヘッダーに設定
http {        
  upstream server {
    server 172.16.0.71:8083;
  }

  server {
    listen 8083;

    # 172.16.0.0/24の範囲内のすべてのIPを信頼
    set_real_ip_from 172.16.0.0/24;
    # X-Forwarded-Forから実際のIPを取得
    real_ip_header X-Forwarded-For;
    # 右から左へ再帰的に検索し、最初に信頼されていないIPをクライアントの実際のIPとして設定
    real_ip_recursive on;

    location /mqtt {
      proxy_pass <http://server;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;

      # $realip_remote_* ではなく $remote_* を代入
      proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
      # X-Real-IPを使用してクライアントの実際のIPを渡す
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}
```

LB 3の設定の核心は、`set_real_ip_from` と `real_ip_header` ディレクティブで、これらはHTTP Real-IPモジュールに依存しています。現在のNGINXインストールにこのモジュールが含まれているかを確認するには、以下のコマンドを使用します。

```
nginx -V 2>&1 | grep -- 'http_realip_module'
```

もし含まれていなければ、NGINXを手動でコンパイルし、ビルド時にこのモジュールを含める必要があります。詳細については[Installing NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)を参照してください。

`set_real_ip_from` ディレクティブを使用すると、信頼できるLBのIPアドレスまたはCIDRアドレス範囲を指定できます。`set_real_ip_from` は複数回呼び出すことができます。たとえば：

```
set_real_ip_from 172.16.0.0/24;
set_real_ip_from 115.236.21.86;
```

`real_ip_header` ディレクティブを使用すると、実際のIPのソースを指定できます。この例では、`X-Forwarded-For` ヘッダーです。

`real_ip_recursive` ディレクティブを使用すると、再帰的に実際のIPを検索するかどうかを指定できます。`off` に設定すると、NGINXは右から左へ最初のIPをクライアントの実際のIPとして取得します。`on` に設定すると、NGINXは右から左へ最初に信頼されていない範囲外のIPをクライアントの実際のIPとして取得します。後者はこの例で必要です。

Real-IPモジュールを使用すると、NGINXはクライアントの実際のIPとポートを `$remote_addr` と `$remote_port` に入れ、ダウンストリームのIPとポートは `$realip_remote_addr` と `$realip_remote_port` から取得する必要があります。

```
proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
```

ここでは、`$remote_addr` を別のヘッダーである `X-Real-IP` に代入するため、EMQXのWebSocketリスナー設定にも変更を反映させる必要があります。

```
websocket.proxy_address_header = X-Real-IP
websocket.proxy_port_header = X-Forwarded-Port
```

#### 確認

この例では、ホストのIPは以下の通りです。

```
+ ----------------------- +    + ---------------------- +    + -------------------- +    
| MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    
| *********************** | -> | ********************** | -> | ******************** | --...
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    
| WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    
+ ----------------------- +    + ---------------------- +    + -------------------- +

     + -------------------- +    + ------------------- +
     | LB 3 (NGINX)         |    | EMQX                |
..-> | ******************** | -> | ******************* |
     | LAN IP: 172.16.0.225 |    | LAN IP: 172.16.0.71 |
     | WAN IP: /            |    | WAN IP: /           |
     + -------------------- +    + ------------------- +
```

LB 1、LB 2、LB 3の3つのホストで以下のコマンドを実行してパケットをキャプチャします。

```shell
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

前の例と同様に、MQTTクライアントを実行しているホストに追加のNGINXを展開し、以下の設定で構成します。

```
http {
  upstream proxy1 {
    # 実際のLB 1の公開IPとリスンポートに変更してください
    server 121.36.192.227:8083;
  }

  server {
    listen 8083;
    location /mqtt {
      proxy_pass <http://proxy1;>
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";

      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

ローカルNGINXの代わりにリモートLB 1に接続するMQTTX CLIを実行します。

```shell
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

キャプチャされたパケット内で、LB 1が`X-Forwarded-For` の `127.0.0.1` を持つWebSocketアップグレード要求を受け取っていることが確認でき、これは悪意のあるMQTTクライアントがサーバーを欺いてローカル接続であると見せかけようとしていることに相当します。

しかし、今回は `X-Forwarded-For` を直接上書きするのではなく、元の基礎に追加しました。したがって、LB 2がLB 3に送信するWebSocketアップグレード要求で、`X-Forwarded-For` の値が `127.0.0.1, 1.94.170.163, 172.16.0.116` であることが確認できます。

![08lb2tolb3.png](https://assets.emqx.com/images/bf787c787ef20cb70ee01a193dedc29d.png)

LB 3がEMQXに送信するWebSocketアップグレード要求で、`X-Real-IP` ヘッダーが `1.94.170.163` に設定されていることが確認でき、これは私たちが期待したものです。

![09lb3toemqx.png](https://assets.emqx.com/images/31737e73738f62ad6ff773485d40048a.png)

EMQXのCLIコマンドを使用すると、EMQXがMQTTクライアントの実際のIPとポートを正常に取得していることも確認できます。

```shell
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:39872, ...)
```

LB 3で `real_ip_recursive` を `off` に設定すると、`X-Real-IP` ヘッダーが `172.16.0.116` に設定されていることが確認できます。

![10lb3toemqx.png](https://assets.emqx.com/images/8744f29c01bdec736a6bf3ddf4887b5c.png)

## まとめ

この記事では、EMQXとNGINXを設定するプロセスを徹底的に探求し、単一または複数のプロキシ層を介してクライアントの実際のIPアドレスを最終的なEMQXサーバーに伝える方法を紹介しました。これは、PROXYプロトコルまたは `X-Forwarded-For` ヘッダーの助けで達成され、セキュリティ監査、アクセス制限、トラフィック監視などのアプリケーションが可能になります。

今後のブログでは、HAProxyをリバースプロキシとして使用する場合にEMQXでクライアントの実際のIPを取得するための設定ガイドも提供します。最新のニュースを入手するために[ブログ](https://www.emqx.com/en/blog)に登録してください。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
