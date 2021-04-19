
## 系统要求

- CentOS 6.8
- CentOS 7

## 安装 EMQ X

您可以根据需要以不同方式安装 EMQ X：

- 设置 EMQ X 的镜像库并从中进行安装，以便于安装和升级任务。 
- 手动下载软件包并安装。

### 使用镜像库安装 EMQ X 

在新主机上首次安装 EMQ X 之前，需要设置 EMQ X 镜像库。 之后，可以从镜像库安装和更新 EMQ X 。

#### 设置镜像库

1.安装所需的包。 

```
$ sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

2.使用以下命令设置稳定镜像库，以centos7为例。

```
$ sudo yum-config-manager --add-repo https://repos.emqx.io/emqx-ce/redhat/centos/7/emqx-ce.repo
```

#### 安装 EMQ X 

1.安装最新版本的 EMQ X ，或者转到下一步安装特定版本：

```
$ sudo yum install emqx
```

如果提示接受GPG密钥，请确认指纹符合 `fc84 1ba6 3775 5ca8 487b 1e3c c0b4 0946 3e64 0d53` ，如果符合，则接受该指纹。

> 如果启用了多个 EMQ X 镜像库，则在 yum install 或 yum update 命令中未指定版本的情况下将始终安装尽可能高的版本，这可能不适合稳定性需求。

2.要安装特定版本的 EMQ X ，需要列出可用版本，然后选择并安装：

查询可用版本

```
$ yum list emqx --showduplicates | sort -r

emqx.x86_64     3.1.0-1.el7    emqx-stable
emqx.x86_64     3.0.1-1.el7    emqx-stable
emqx.x86_64     3.0.0-1.el7    emqx-stable
```

返回的列表取决于启用的镜像库，并且特定于 CentOS 版本（在此示例中以.el7后缀表示）。

使用第二列中的版本字符串安装特定版本，例如`3.1.0`

```
$ sudo yum install emqx-3.1.0
```

3.启动 EMQ X

```
$ emqx start
emqx 3.1 is started successfully!
$ emqx_ctl status
Node 'emqx@127.0.0.1' is started
emqx v3.1.0 is running
```

4.EMQ X 启动成功，如何使用请参考[官方文档](https://docs.emqx.io/broker/v3/cn/getstarted.html)

### 使用软件包安装 EMQ X 

如果无法使用 EMQ X 的镜像库来安装 EMQ X ，则可以下载 `.rpm` 文件或 `.zip` 文件并手动安装。

#### 从 `.rpm` 文件安装

1.转到 [EMQ X 下载](https://www.emqx.cn/downloads) 页面或 [GitHub](https://github.com/emqx/emqx/releases)，选择 CentOS 版本，然后下载要安装的 EMQ X 版本的 .rpm 文件。

2.安装 EMQ X ，将下面的路径更改为下载 EMQ X 软件包的路径。

```
$sudo rpm -ivh /path/to/emqx-centos7-v3.1.0.x86_64.rpm
```

3.启动 EMQ X 

```
$ emqx start
emqx 3.1 is started successfully!
$ emqx_ctl status
Node 'emqx@127.0.0.1' is started
emqx v3.1.0 is running
```

4.EMQ X 启动成功，如何使用请参考[官方文档](https://docs.emqx.io/broker/v3/cn/getstarted.html)

#### 从 `.zip` 文件安装

1.转到 [EMQ X 下载](https://www.emqx.cn/downloads) 页面或 [GitHub](https://github.com/emqx/emqx/releases)，选择 CentOS 版本，然后下载要安装的 EMQ X 版本的 .zip 文件。

2.解压压缩包，将下面的路径更改为下载 EMQ X 软件包的路径。

```
$ unzip /path/to/emqx-centos7-v3.1.0.zip 
```

3.启动EMQX

```
$ cd emqx $ ./bin/emqx start emqx 3.1 is started successfully! $ ./bin/emqx_ctl status Node 'emqx@127.0.0.1' is started emqx v3.1.0 is running 
```

4.EMQ X 启动成功，如何使用请参考[官方文档](https://docs.emqx.io/broker/v3/cn/getstarted.html)

