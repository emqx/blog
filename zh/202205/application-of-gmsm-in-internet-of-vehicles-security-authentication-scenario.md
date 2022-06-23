## 前言

国密即国家密码局认定的国产密码算法。通过自主可控的国产密码算法保护重要数据的安全，是有效提升信息安全保障水平的重要举措。目前，我国在金融银行、教育、交通、通信、国防工业等各类重要领域的信息系统均已开始进行国产密码算法的升级改造。

随着汽车电动化、网联化、智能化交融发展，车辆运行安全、数据安全和网络安全风险交织叠加，亟需加快建立健全车联网网络安全和数据安全保障体系，为车联网产业安全健康发展提供支撑。2022 年 2 月，工业和信息化部在现有国家车联网产业标准体系的基础上，组织编制了《车联网网络安全和数据安全标准体系建设指南》，其中已发布的 GB/T 37376-2019《交通运输数字证书格式》等国标文件中，凡涉及密码算法相关的内容，均考虑了国密的应用与实现。

本文将详细介绍国密算法的分类及应用，以及如何使用 [EMQX](https://www.emqx.com/zh/products/emqx) 实现国密证书集成，保障车联网信息安全。

## 国密的分类

为了保障在金融、医疗等领域保障信息传输安全，国家商用密码管理办公室制定了一系列密码标准，包括SM1（SCB2）、SM2、SM3、SM4、SM7、SM9、祖冲之密码算法（ZUC）等。其中 SM1、SM4、SM7 是对称算法，SM2、SM9 是非对称算法，SM3 是哈希算法。

### SM1 算法

SM1 算法是分组对称算法，分组长度为 128 位，密钥长度都为 128 比特，算法安全保密强度及相关软硬件实现性能与 AES 相当，算法不公开，仅以 IP 核的形式存在于芯片中。采用该算法已经研制了系列芯片、智能 IC 卡、智能密码钥匙、加密卡、加密机等安全产品，广泛应用于电子政务、电子商务及国民经济的各个应用领域（包括国家政务通、警务通等重要领域）。

### SM2 算法

SM2 算法是一种先进安全的公钥密码算法，在我们国家商用密码体系中被用来替换 RSA 算法。SM2 算法就是 ECC 椭圆曲线密码机制，但在签名、密钥交换方面不同于 ECDSA、ECDH 等国际标准，而是采取了更为安全的机制。另外，SM2 推荐了一条 256 位的曲线作为标准曲线。

### SM3 算法

SM3 是一种哈希算法，其算法本质是给数据加一个固定长度的指纹，这个固定长度就是256比特。用于密码应用中的数字签名和验证、消息认证码的生成与验证以及随机数的生成，可满足多种密码应用的安全需求。

### SM4 算法

SM4 算法是一个分组算法，用于无线局域网产品。该算法的分组长度为 128 比特，密钥长度为 128 比特。加密算法与密钥扩展算法都采用 32 轮非线性迭代构。解密算法与加密算法的结构相同，只是轮密钥的使用顺序相反，解密轮密钥是加密轮密钥的逆序。

### SM7 算法

SM7 算法是一种分组密码算法，分组长度为 128 比特，密钥长度为 128 比特。SM7 的算法文本目前没有公开发布。

### SM9 算法

SM9 是基于对的标识密码算法，与 SM2 类似，包含四个部分：总则，数字签名算法，密钥交换协议以及密钥封装机制和公钥加密算法。

目前支持国密算法的软硬件密码产品包括 SSL 网关、数字证书认证系统、密钥管理系统、金融数据加密机、签名验签服务器、智能密码钥匙、智能 IC 卡、PCI 密码卡等多种类型。但常用的操作系统、浏览器、网络设备、负载均衡设备等软硬件产品，仍然不支持国产密码算法。受到国密算法兼容性的制约，在 HTTPS 加密应用方面，国密算法的应用仍然比较滞后。

## 国密（GmSSL）证书与传统 SSL 证书对比

![国密算法与传统算法对比](https://assets.emqx.com/images/9d35b400058d8388ba16211c4b4783fd.gif)

<center>国密算法与传统算法对比</center>

### 算法

传统 SSL 证书通常是 RSA 算法（2048 位），它是目前最有影响力和最常用的公钥加密算法，能抵抗已知的绝大多数密码攻击。但是随着密码技术的飞速发展，证实了 1024 位 RSA 算法存在着被攻击的风险，现已升级到 2048 位 RSA 算法。

现阶段的国密 SM2 证书采用的是 ECC 算法（256 位），由国家密码管理局于 2010 年 12 月发布，是我国自主设计的公钥密码算法，在椭圆曲线密码理论基础进行改进而来，其加密强度比 RSA 算法（2048 位）更高。

### 安全性能

虽然 RSA 算法在目前的 SSL 证书市场中依然占据着主流地位，但是随着计算机技术的发展，加上对因子分解的改进，对低位数的密钥攻击已成为可能。

目前基于 ECC 算法的 SM2 算法普遍采用 256 位密钥长度，它的单位安全强度相对较高，在工程应用中比较难以实现，破译或求解难度基本上是指数级的。因此，ECC 算法可以用较少的计算能力提供比 RSA 算法更高的安全强度，而所需的密钥长度却远比 RSA 算法低。

此外，为了不断提高安全强度，必须增加密钥长度，ECC 算法密钥长度增长速度较慢（例如：224-256-384），而 RSA 算法密钥长度则需呈倍数增长（例如：1024-2048-4096）。

### 传输速度

在通讯过程中，更长的密钥意味着必须来回发送更多的数据以验证连接。256 位的 SM2 算法相对于 2048 位的 RSA 算法，可以传输更少的数据，也就意味着更少的传输时间。经国外有关权威机构测试，在 Web服务器中采用 SM2 算法，Web 服务器新建并发处理响应时间比 RSA 算法快十几倍。

> 国密算法在设计时，RSA2048 是主流签名算法，所以这里暂不讨论 ECDSA 等算法。

## 国密算法在车云通信中的应用

国密算法在车云通信中主要用于对传输协议加解密：车机端作为发送端，一般数据都是用 SM4 对数据内容加密，使用 SM3 对内容进行摘要，再使用 SM2 对摘要进行签名；消息 Broker 作为接收端，先用 SM2 对摘要进行验签，验签成功后就做到了防抵赖，对发送过来的内容进行 SM3 摘要，确认生成的摘要和验签后的摘要是否一致，用于防篡改。另外 SM4 在加密解密需要相同的密钥，可以通过编写密钥交换模块实现生成相同的密钥，用于 SM4 对称加密。

关于非对称算法还要注意几点：

1. 公钥是通过私钥产生的；
2. 公钥加密，私钥解密是加密的过程
3. 私钥加密，公钥解密是签名的过程；

由于 SM4 加解密的分组大小为 128 比特，故对消息进行加解密时，若消息长度过长，需要进行分组，要消息长度不足，则要进行填充。

## EMQ 基于国密算法的传输加密认证集成方案

当前 EMQ 支持两种国密证书集成方案。

一种是在 EMQX 上通过插件的方式开发了一个国密认证 Java Gateway；

另一种是通过 C 语言的 GmSSL SDK 对原生的 Nginx/HAProxy 两种主流的 LB 代理软件进行编译扩展，使其具备 GmSSL 证书认证卸载的能力。这种方案是我们更加推荐的。

![车联网国密算法](https://assets.emqx.com/images/9c79bddb512b0740550f3c48b7559cbe.png)

下面我们将介绍如何使用两种代理软件解决国密证书支持。

### Nginx 编译扩展 GmSSL

1. 解压 GmSSL: `tar -xvf gmssl_opt_xxx.tar.gz -C /usr/local`

2. 解压 nginx: `tar -xvf nginx-x.xxx.tar.gz`

3. 进入 `cd [nginx-x.xxx](http://nginx-1.xxx/)` 目录

4. 编辑 `auto/lib/openssl/conf`，将全部 `$OPENSSL/.openssl/` 修改为 `$OPENSSL/` 并保存

5. 编译配置

   ```
   ./configure  \
       --prefix=/usr/local/nginx \
       --sbin-path=/usr/local/nginx/sbin/nginx \
       --conf-path=/usr/local/nginx/conf/nginx.conf \
       --error-log-path=/usr/local/nginx/log/nginx/error.log \
       --http-log-path=/usr/local/nginx/log/nginx/access.log \
       --pid-path=/var/run/nginx.pid \
       --lock-path=/var/run/nginx.lock \
       --http-client-body-temp-path=/usr/local/nginx/client_temp \
       --http-proxy-temp-path=/usr/local/nginx/proxy_temp \
       --http-fastcgi-temp-path=/usr/local/nginx/fastcgi_temp \
       --http-uwsgi-temp-path=/usr/local/nginx/uwsgi_temp \
       --http-scgi-temp-path=/usr/local/nginx/scgi_temp \
       --without-http_gzip_module \
       --with-http_ssl_module \
       --with-http_realip_module \
       --with-http_addition_module \
       --with-http_sub_module \
       --with-http_dav_module \
       --with-http_flv_module \
       --with-http_mp4_module \
       --with-http_random_index_module \
       --with-http_secure_link_module \
       --with-http_stub_status_module \
       --with-http_auth_request_module \
       --with-threads \
       --with-stream \
       --with-stream_ssl_module \
       --with-http_slice_module \
       --with-mail \
       --with-mail_ssl_module \
       --with-file-aio \
       --with-http_v2_module \
       --with-openssl=/usr/local/gmssl \
       --with-cc-opt="-I/usr/local/gmssl/include" \
       --with-ld-opt="-lm"
   ```

6. 编译安装：`make install`

7. `/usr/local/nginx` 即为生成的 nginx 目录

8. 配置 `nginx.conf`：进入到 `/usr/local/nginx` 目录，在 `conf/nginx.conf` 添加：`include /usr/local/nginx/conf/mqtt_tcp.conf`;

   ![nginx.conf](https://assets.emqx.com/images/c2ff0dab4cfb7e29d4d5f40d955fb51d.png)

   添加 mqtt_tcp.conf 文件，内容如下：

   - 单向认证

     ```
     stream {
         log_format proxy '$remote_addr [$time_local] '
                      '$protocol $status $bytes_sent $bytes_received '
                      '$session_time "$upstream_addr" '
                      '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
         access_log /usr/local/nginx/log/tcp-access.log proxy;
         open_log_file_cache off;
         upstream mqtt_tcp_server {
            server 192.168.0.239:1883;      #高可用均衡配置
             #server 172.17.0.4:1883;
         }    
         
     server {
             listen       1883;  #监听端口 也可以使用 1883
             #ssl_verify_client on;
     #        proxy_connect_timeout 150s;
     #        proxy_timeout 350s;
     #        proxy_next_upstream on;
             proxy_pass mqtt_tcp_server;  #反向代理地址
     #        proxy_buffer_size 3M;
             #tcp_nodelay on;
             proxy_protocol on;        
         }
     
     server {
             listen 8083 ssl;
             ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
             ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:AES128-SHA:DES-CBC3-SHA:ECC-SM4-CBC-SM3:ECDHE-SM4-GCM-SM3;
             ssl_verify_client off;
             ssl_certificate /usr/local/nginx/cert/Tsp_Server_Test_210906_sign.cer;
             ssl_certificate_key /usr/local/nginx/cert/Tsp_Server_Test_210906_sign.key;
             ssl_certificate_key /usr/local/nginx/cert/Tsp_Server_Test_210906_enc.key;
             ssl_certificate /usr/local/nginx/cert/Tsp_Server_Test_210906_enc.cer;
             proxy_pass mqtt_tcp_server;
             proxy_protocol on;
         }
     
     }
     ```

   - 双向认证

     说明：双向认证比单向认证多了 ssl_client_certificate：这个是 CA 证书，将签名 CA 和密钥 CA 合并到一个文件，同时 ssl_verify_client 设置为 on。

     ```
     stream {
         log_format proxy '$remote_addr [$time_local] '
                      '$protocol $status $bytes_sent $bytes_received '
                      '$session_time "$upstream_addr" '
                      '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
         access_log /usr/local/nginx/log/tcp-access.log proxy;
         open_log_file_cache on;
         upstream mqtt_tcp_server {
             server 192.168.0.239:1883;      #高可用均衡配置
             #server 172.17.0.4:1883;
         }     
     
         server {
             listen       1883;  #监听端口 也可以使用1883
             #ssl_verify_client on;
     #        proxy_connect_timeout 150s;
     #        proxy_timeout 350s;
     #        proxy_next_upstream on;
             proxy_pass mqtt_tcp_server;  #反向代理地址
     #        proxy_buffer_size 3M;
             #tcp_nodelay on;
             proxy_protocol on;
         }
         server {
             listen 8083 ssl;
             ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
             ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:AES128-SHA:DES-CBC3-SHA:ECC-SM4-CBC-SM3:ECDHE-SM4-GCM-SM3;
             ssl_verify_client on;
             ssl_client_certificate /usr/local/nginx/cert/ca.pem;
             ssl_certificate /usr/local/nginx/cert/Tsp_Server_Test_210906_sign.cer;
             ssl_certificate_key /usr/local/nginx/cert/Tsp_Server_Test_210906_sign.key;
             ssl_certificate_key /usr/local/nginx/cert/Tsp_Server_Test_210906_enc.key;
             ssl_certificate /usr/local/nginx/cert/Tsp_Server_Test_210906_enc.cer;
             proxy_pass mqtt_tcp_server;
             proxy_protocol on;
          }
     
      }
     ```

9. 启动

   在 `/usr/local/nginx` 下操作

   启动：`./sbin/nginx`

   重启：`./sbin/nginx -s reload`

   停止：`./sbin/nginx -s stop`

   验证配置文件是否正确：`./sbin/nginx -t`

### **HAProxy 集成 GmSSL 编译扩展**

1. 解压 GmSSL: `tar -xvf gmssl_opt_xxx.tar.gz -C /usr/local`

2. 解压 HAProxy：`tar -xvf haproxy_xxx.tar.gz`

3. 进入 HAProxy 安装目录（不要和后面编译生成的运行目录同一目录）修改

   - 修改 makefile：

     注释 ：

     `#OPTIONS_LDFLAGS += $(if $(SSL_LIB),-L$(SSL_LIB)) -lssl -lcrypto`

     新增：

     `OPTIONS_LDFLAGS += $(SSL_LIB)/libssl.aOPTIONS_LDFLAGS += $(SSL_LIB)/libcrypto.a -lm -lpthread -ldl`

      ![HAProxy](https://assets.emqx.com/images/fc158934afcf34556d504892141fba6e.jpeg)

   - 修改源码：

     文件 src/ssl_sock.c  备注：不能直接修改红色内容，还需要更换位置，按照修改的顺序

     函数 ssl_sock_put_ckch_into_ctx 将以下代码

     ```
     if (SSL_CTX_use_PrivateKey(ctx, ckch->key) <= 0) {
         memprintf(err, "%sunable to load SSL private key into SSL Context '%s'.\n", err && *err ? *err : "", path);
         errcode |= ERR_ALERT | ERR_FATAL; return errcode;
     if (!SSL_CTX_use_certificate(ctx, ckch->cert)) {
         memprintf(err, "%sunable to load SSL certificate into SSL Context '%s'.\n", err && *err ? *err : "", path);
         errcode |= ERR_ALERT | ERR_FATAL;
         goto end; 
     }			
     ```

     修改为：

     ```
     if (!SSL_CTX_use_certificate_file(ctx, path, SSL_FILETYPE_PEM)) {
         memprintf(err, "%sunable to load SSL certificate into SSL Context '%s'.\n", err && *err ? *err : "", path);
         errcode |= ERR_ALERT | ERR_FATAL;
         goto end;
     }
     
     if (SSL_CTX_use_PrivateKey_file(ctx, path, SSL_FILETYPE_PEM) <= 0) {
         memprintf(err, "%sunable to load SSL private key into SSL Context '%s'.\n", err && *err ? *err : "", path);
         errcode |= ERR_ALERT | ERR_FATAL; return errcode;
     }
     ```

     ![src/ssl_sock.c](https://assets.emqx.com/images/dce7d59e2d91fca1093f9a537822f3f6.gif)

4. 编译

   编译前可能需要提前安装相关依赖：

   `yum install pcre-devel zlib-devel`

   `make TARGET=linux31 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 USE_CRYPT_H=1 USE_LIBCRYPT=1 SSL_INC=/root/gmssl/gmssl/include SSL_LIB=/root/gmssl/gmssl/lib` 

   > 备注：SSL_INC 和 SSL_LIB 指定 gmssl 解压的路径

5. 安装

   `make install PREFIX=/usr/local/haproxy`

   > 备注：PREFIX=/usr/local/haproxy 是编译生成的运行目录，不要和安装目录同目录。

6. 配置

   - 证书准备：

     将签名证书 pem 文件和签名私钥 pem 文件合并成 XXX_sig.pem，文件名必须以 sig.pem 结尾
     
     ![server_sig.pem](https://assets.emqx.com/images/5376fec40f1a148647ff4ddf31d19b18.gif)

     将加密证书 pem 文件和加密私钥 pem 文件合并成 XXX_enc.pem，文件名必须以 enc.pem 结尾

     XXX_enc.pem 将被隐式加载，且必须放到 XXX_sig.pem 的相同目录下，比如: /usr/local/keystore/server_enc.pem

     需要双向认证的时候：CA 证书合并到一个文件（选做）

     ![CA 证书合并到一个文件](https://assets.emqx.com/images/6ae860254dad50fc736270f493818bf9.gif)

   - HAProxy.conf:

     ```
     global
             daemon
             ssl-default-bind-ciphers ECC-SM4-CBC-SM3:ECC-SM4-GCM-SM3
             #ssl-default-bind-options no-sslv3
             maxconn 256
             log 127.0.0.1 local7 info
         defaults
             mode tcp
             log global
             option tcplog
             timeout connect 5000ms
             timeout client 50000ms
             timeout server 50000ms
             stats uri /status
             #stats auth zp:123456
         frontend emqx_dashboard
             bind *:18083
             option tcplog
             mode tcp
             default_backend emqx_dashboard_back
         frontend emqx_tcps
             bind *:8883 ssl crt /usr/local/haproxy/cert/server_sig.pem ca-file /usr/local/haproxy/cert/ca.pem verify required
             option tcplog
             mode tcp
            default_backend backend_emqx_tcp
         frontend emqx_tcp
             bind *:1883
             option tcplog
             mode tcp
             default_backend backend_emqx_tcp
         frontend frontend_emqx_ws
             bind *:8083
             option tcplog
     #        option forwardfor
             mode tcp
             default_backend backend_emqx_ws
         backend emqx_dashboard_back
             balance roundrobin
             server emqx_node_1 192.168.92.120:18083 check
         backend backend_emqx_tcp
             mode tcp
     balance roundrobin
             server emqx_node_1 192.168.92.120:1883 check-send-proxy send-proxy-v2-ssl-cn
         backend backend_emqx_ws
             mode http
             option forwardfor
             balance roundrobin
             server emqx_node_1 192.168.92.120:8083 check-send-proxy send-proxy-v2 check inter 10s fall 2 rise 5
     ```

     ![双向认证](https://assets.emqx.com/images/85d49640cecf4059a6a326cd46d889ce.png)

   - 启动测试

     假如配置文件放在：`/usr/local/haproxy/conf/` 下

     启动命令：`/usr/local/haproxy/sbin/haproxy -f /usr/local/haproxy/conf/haproxy.cfg`

## 结语

本文为大家介绍了国密算法的基础背景知识以及其在车联网场景中的应用，同时介绍了 EMQ 基于国密算法的传输加密认证集成方案，通过本文提供的配置操作示例，读者可以尝试在车联网平台中使用国密认证，进一步增加平台安全性。

EMQ 车联网 GmSSL 集成解决方案紧密对接车联网产业对网络安全、数据安全的迫切需求，为车联网通信安全提供了有力保障。目前已经部署应用在车联网平台安全认证和 V2X 车路协同等多个车云安全通信场景。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## 本系列中的其它文章

- [车联网平台搭建从入门到精通 01 | 车联网场景中的 MQTT 协议](https://www.emqx.com/zh/blog/mqtt-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 02 | 千万级车联网 MQTT 消息平台架构设计](https://www.emqx.com/zh/blog/mqtt-messaging-platform-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 03 | 车联网 TSP 平台场景中的 MQTT 主题设计](https://www.emqx.com/zh/blog/mqtt-topic-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 04 | MQTT QoS 设计：车联网平台消息传输质量保障](https://www.emqx.com/zh/blog/mqtt-qos-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 05 | 车联网平台百万级消息吞吐架构设计](https://www.emqx.com/zh/blog/million-level-message-throughput-architecture-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 06 | 车联网通信安全之 SSL/TLS 协议](https://www.emqx.com/zh/blog/ssl-tls-for-internet-of-vehicles-communication-security)
- [车联网平台搭建从入门到精通 07 | 车联网中 MQTT 心跳保活与远程唤醒设计](https://www.emqx.com/zh/blog/mqtt-keep-alive-design-in-the-internet-of-vehicles)
