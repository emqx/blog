## 安装 EMQX

您可以根据需要以不同方式安装 EMQX ：

- 直接通过 [Homebrew](<https://brew.sh/>) 安装最新的稳定版 EMQX 
- 手动下载软件包并安装。

### 使用Homebrew安装 EMQX 

1. 添加 EMQX 的 tap

   ```
   $ brew tap emqx/emqx
   ```

2. 安装 EMQX

   ```
   $ brew install emqx
   ```

3. 启动 EMQX

   ```
   $ emqx start
   emqx 3.1 is started successfully!
   $ emqx_ctl status
   Node 'emqx@127.0.0.1' is started
   emqx v3.1.0 is running
   ```

4. EMQX 启动成功，如何使用请参考[官方文档](https://developer.emqx.io/docs/broker/v3/cn/getstarted.html)

### 使用安装包安装 EMQX 

#### 从 `.zip` 文件安装

1. 转到  `emqx.io`  或  github ，选择 EMQX 版本，然后下载要安装的 `.zip` 文件。

2. 解压压缩包，将下面的路径更改为您下载 EMQX 软件包的路径。

   ```
   $ unzip /path/to/emqx-macos-v3.1.0.zip
   ```

3. 启动 EMQX

   ```
   $ cd emqx
   $ ./bin/emqx start
   emqx 3.1 is started successfully!
   $ ./bin/emqx_ctl status
   Node 'emqx@127.0.0.1' is started
   emqx v3.1.0 is running
   ```

4. EMQX 启动成功，如何使用请参考[官方文档](https://docs.emqx.com/zh/emqx/latest/)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
