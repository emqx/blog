

## 系统要求

- Bionic 18.04 (LTS)
- Xenial 16.04 (LTS)
- Trusty 14.04 (LTS)
- Precise 12.04(LTS)

## 安装 EMQ X 

- 您可以根据需要以不同方式安装 EMQ X ：
  - 设置 EMQ X 的镜像库并从中进行安装，以便于安装和升级任务。 
  - 手动下载软件包并安装。 

### 使用镜像库安装 EMQ X 

在新主机上首次安装 EMQ X 之前，需要设置 EMQ X 镜像库。 之后，您可以从镜像库安装和更新 EMQ X 。

#### 设置镜像库

1.更新 `apt` 包索引：

```
$ sudo apt update
```

2.安装必要的软件：

```
$ sudo apt install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
```

3.添加 EMQ X 的官方 GPG 密钥：

```
$ curl -fsSL https://repos.emqx.io/gpg.pub | sudo apt-key add -
```

验证密钥

```
$ sudo apt-key fingerprint 3E640D53

pub  rsa2048 2019-04-10 [SC]
        FC84 1BA6 3775 5CA8 487B 1E3C C0B4 0946 3E64 0D53
uid     [ unknown] emqx team <support@emqx.io>
```

4.使用以下命令设置 **stable** 镜像库。 要添加 **unstable** 的镜像库，请在以下命令中的单词 stable 之后添加单词 unstable。

> **注意**：下面的 lsb_release -cs 子命令返回 Ubuntu 发行版的名称，例如 xenial。 有时在像 Linux Mint 这样的发行版中，可能需要将 $(lsb_release -cs) 更改为父 Ubuntu 发行版。 例如，如果使用的是 Linux Mint Tessa，则可以使用 bionic。  EMQ X 不对未经测试和不受支持的 Ubuntu 发行版提供任何保证。

```
$ sudo add-apt-repository \
  "deb [arch=amd64] https://repos.emqx.io/emqx-ce/deb/ubuntu/ \
  $(lsb_release -cs) \
  stable"
```

#### 安装 EMQ X 

1.更新 `apt` 包索引：

```
$ sudo apt update
```

2.安装最新版本的 EMQ X ，或者转到下一步安装特定版本：

```
$ sudo apt install emqx
```

> 如果启用了多个 EMQ X 镜像库，则在 `apt install` 或 `apt update` 命令中未指定版本的情况下将始终安装尽可能高的版本，这可能不适合稳定性需求。

3.要安装特定版本的 EMQ X ，需要列出可用版本，然后选择并安装：

查询可用版本

```
$ sudo apt-cache madison emqx

emqx |  3.1.0 | https://repos.emqx.io/emqx-ce/deb/ubuntu bionic/stable amd64 Packages
emqx |  3.0.1 | https://repos.emqx.io/emqx-ce/deb/ubuntu bionic/stable amd64 Packages
emqx |  3.0.0 | https://repos.emqx.io/emqx-ce/deb/ubuntu bionic/stable amd64 Packages
```

使用第二列中的版本字符串安装特定版本，例如 `3.1.0`

```
$ sudo apt install emqx=3.1.0 
```

4.启动 EMQ X 

```
$ emqx start emqx 3.1 is started successfully! $ emqx_ctl status Node 'emqx@127.0.0.1' is started emqx v3.1.0 is running 
```

5.EMQ X 启动成功，如何使用请参考[官方文档](https://developer.emqx.io/docs/broker/v3/cn/getstarted.html)



### 使用安装包安装 EMQ X 

如果无法使用 EMQ X 的镜像库来安装 EMQ X ，则可以下载 `.deb` 文件或 `.zip` 文件并手动安装。

#### 从 `.deb` 文件安装

1.转到  `emqx.io`  或  github，选择 Ubuntu 版本，然后下载要安装的 EMQ X 版本的 `.deb` 文件。

2.安装 EMQ X ，将下面的路径更改为下载 EMQ X 软件包的路径。

```
$ sudo dpkg -i /path/to/emqx-ubuntu18.04-v3.1.0_amd64.deb 
```

3.启动 EMQ X 

```
$ emqx start emqx 3.1 is started successfully! $ emqx_ctl status Node 'emqx@127.0.0.1' is started emqx v3.1.0 is running 
```

4.EMQ X 启动成功，如何使用请参考官方文档

####  

#### 从`.zip`文件安装

1.转到  `emqx.io`  或  github，选择 Ubuntu 版本，然后下载要安装的 EMQ X 版本的 `.zip` 文件。

2.解压压缩包，将下面的路径更改为下载 EMQ X 软件包的路径。

```
$ unzip /path/to/emqx-ubuntu18.04-v3.1.0.zip 
```

3.启动 EMQ X 

```
$ cd emqx $ ./bin/emqx start emqx 3.1 is started successfully! $ ./bin/emqx_ctl status Node 'emqx@127.0.0.1' is started emqx v3.1.0 is running 
```

4.EMQ X 启动成功，如何使用请参考[官方文档](https://developer.emqx.io/docs/broker/v3/cn/getstarted.html)

