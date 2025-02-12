## 前言

[NeuronEX](https://www.emqx.com/zh/products/neuronex) 是一款部署在工业边缘的实时数采和智能分析软件，能够实现工业设备协议采集、工业各系统数据集成、边端数据过滤分析、AI 算法集成以及数据转发和平台对接等功能，为工业场景提供低延迟的数据接入管理及智能分析服务。

为确保服务的高可用性，NeuronEX 支持主备双机部署方案，结合 Keepalived 实现故障自动切换。该方案能够有效应对软件故障或服务器宕机等场景，在主节点发生故障时，备节点可自动接管服务，保证业务连续性。同时，系统支持主节点恢复后的自动回切，确保服务始终处于最优运行状态。

通过主备部署与 Keepalived 的结合，NeuronEX 实现了 7×24 小时不间断服务，不仅有效防范单点故障风险，还确保了数据完整性和业务可持续性，充分满足工业场景对高可靠性和实时性的严苛要求。

## 安装与配置 NeuronEX

### 安装 NeuronEX

在主节点和备节点上安装 NeuronEX，本示例使用 NeuronEX 3.4.3 版本的 x86_64 架构 deb 包。如需其他安装包，请访问 [NeuronEX 下载页面](https://www.emqx.com/zh/downloads-and-install/neuronex)。

```shell
# 下载 NeuronEX 安装包
wget https://www.emqx.com/zh/downloads/neuronex/3.4.3/neuronex-3.4.3-linux-amd64.deb

# 安装 NeuronEX
sudo dpkg -i neuronex-3.4.3-linux-amd64.deb

# 启动 NeuronEX
sudo systemctl start neuronex

# 设置为开机自启动
sudo systemctl enable neuronex
```

### 配置 NeuronEX

访问主节点 NeuronEX Dashboard 页面，配置 NeuronEX 数采服务，可配置一个 Modbus TCP 南向驱动，可正常采集数据，用来后续验证主备切换功能。

访问备节点 NeuronEX Dashboard 页面，可手动配置与主节点相同的数采服务，用来验证主备切换功能。 或者也可以将主节点的配置 `/opt/neuronex/data/` 拷贝到备节点相同目录下覆盖原有配置。

通过以上配置，主节点和备节点均可以正常采集数据，并且功能一致。此时通过以下命令将备节点的 NeuronEX 服务停止，表示主节点运行，备节点停止的初始状态。

```shell
sudo systemctl stop neuronex
```

## 安装与配置 Keepalived

### 安装 Keepalived

在主节点和备节点上安装 Keepalived：

注意：本示例使用 Keepalived v1.3.9 以及 linux ubuntu 18.04 版本。

```shell
# 安装 Keepalived
sudo apt-get install keepalived
```

### 配置主机 Keepalived

在主节点的目录 `/etc/keepalived/` 下创建 `keepalived.conf`、 `master.sh`、 `fault.sh`、 `check_alive.sh` 文件。

1、在主节点上配置 Keepalived，配置文件目录为 `/etc/keepalived/keepalived.conf`，内容如下：

```
! Configuration File for keepalived
global_defs {
   # 路由器标识，一般不用改，也可以写成每个主机自己的主机名
   # router_id huyidb03
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# 定义用于实例执行的脚本内容，比如可以在线降低优先级，用于强制切换
vrrp_script check_ex_alived {
        script "/etc/keepalived/check_alive.sh"
        interval 5
        fall 3 # 连续3次检测失败后，确定服务故障
}


# 一个vrrp_instance就是定义一个虚拟路由器的，实例名称
vrrp_instance VI_1 {
    # 定义初始状态，可以是MASTER或者BACKUP
    state MASTER
	#非抢占模式
    # nopreempt
    # 工作接口，通告选举使用哪个接口进行
    interface eth0
	# 虚拟路由ID，如果是一组虚拟路由就定义一个ID，如果是多组就要定义多个，而且这个虚拟
    # ID还是虚拟MAC最后一段地址的信息，取值范围0-255
    virtual_router_id 51
	#权重 如果你上面定义了MASTER,这里的优先级就需要定义的比其他的高
    priority 100
	#通告频率 单位s
    advert_int 1
	#通信认证机制，这里是明文认证还有一种是加密认证
    authentication {
        auth_type PASS
        auth_pass abcdefgh
    }

    # 设置虚拟VIP地址，并未使用
    virtual_ipaddress {
        192.160.127.254/17
    }
    unicast_peer {
        10.0.0.223  # 备机的 IP 地址
    }
    # 追踪脚本，通常用于去执行上面的vrrp_script定义的脚本内容
    track_script {
        check_ex_alived
    }

    # 如果主机状态变成Master|Backup|Fault之后会去执行的通知脚本
    notify_fault "/etc/keepalived/fault.sh"
    notify_master "/etc/keepalived/master.sh"
}
```

注意：在本例中，从机的 IP 地址是 `10.0.0.223`，所以在 keepalived.conf 文件中 unicast_peer 的内容为 `10.0.0.223`，请根据实际情况修改。

在本例中，主机的 IP 地址 `10.0.0.127` 绑定的网卡是 `eth0`，所以在 keepalived.conf 文件中 interface 的内容为 `eth0`，请根据实际情况修改。

2、在主节点上配置 `master.sh` 脚本， 配置文件目录为`/etc/keepalived/master.sh`，内容如下：

```shell
#!/bin/bash

systemctl start neuronex
```

3、在主节点上配置 `fault.sh` 脚本， 配置文件目录为`/etc/keepalived/fault.sh`，内容如下：

```shell
#!/bin/bash

systemctl stop neuronex
```

4、在主节点上配置 `check_alive.sh` 脚本， 配置文件目录为`/etc/keepalived/check_alive.sh`，内容如下：

```shell
#!/bin/bash

if ! curl 127.0.0.1:8085  >/dev/null 2>&1; then echo "neuronex start failed"; exit 1; fi
```

5、在主节点上启动 Keepalived

```shell
sudo systemctl start keepalived

# 设置为开机自启动
sudo systemctl enable keepalived
```

### 配置从机 Keepalived

在从节点的目录 `/etc/keepalived/` 下创建 `keepalived.conf`、 `master.sh`、 `backup.sh` 文件。

1、在从节点上配置 Keepalived，配置文件目录为 `/etc/keepalived/keepalived.conf`，内容如下：

```
! Configuration File for keepalived
global_defs {
   # 路由器标识，一般不用改，也可以写成每个主机自己的主机名
   # router_id huyidb03
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# 一个vrrp_instance就是定义一个虚拟路由器的，实例名称
vrrp_instance VI_1 {
    # 定义初始状态，可以是MASTER或者BACKUP
    state BACKUP
	#非抢占模式
    nopreempt
    # 工作接口，通告选举使用哪个接口进行
    interface eth0
	# 虚拟路由ID，如果是一组虚拟路由就定义一个ID，如果是多组就要定义多个，而且这个虚拟
    # ID还是虚拟MAC最后一段地址的信息，取值范围0-255
    virtual_router_id 51
	#权重 如果你上面定义了MASTER,这里的优先级就需要定义的比其他的高
    priority 90
	#通告频率 单位s
    advert_int 1
	#通信认证机制，这里是明文认证还有一种是加密认证
    authentication {
        auth_type PASS
        auth_pass abcdefgh
    }

    # 设置虚拟VIP地址，并未使用
    virtual_ipaddress {
        192.160.127.254/17
    }

    unicast_peer {
        10.0.0.127  # 主机的 IP 地址
    }

    # 如果主机状态变成Master|Backup|Fault之后会去执行的通知脚本
    notify_master "/etc/keepalived/master.sh"
    notify_backup "/etc/keepalived/backup.sh"
}
```

注意：在本例中，主机的 IP 地址是 `10.0.0.127`，所以在 keepalived.conf 文件中 unicast_peer 的内容为 `10.0.0.127`，请根据实际情况修改。

在本例中，从机的 IP 地址 `10.0.0.223` 绑定的网卡是 `eth0`，所以在 keepalived.conf 文件中 interface 的内容为 `eth0`，请根据实际情况修改。

2、在从节点上配置 `master.sh` 脚本， 配置文件目录为`/etc/keepalived/master.sh`，内容如下：

```shell
#!/bin/bash

systemctl start neuronex
```

3、在从节点上配置 `backup.sh` 脚本， 配置文件目录为`/etc/keepalived/backup.sh`，内容如下：

```shell
#!/bin/bash

systemctl stop neuronex
```

4、在从节点上启动 Keepalived

```shell
sudo systemctl start keepalived

# 设置为开机自启动
sudo systemctl enable keepalived
```

## 实现原理

### **初始状态**

- **主节点**：  
  - 启动 Keepalived 服务，设置为 **MASTER** 状态。  
  - 启动 NeuronEX 服务，承担主要工作。  
  - 通过 Keepalived 监控自身 NeuronEX 状态，维持 MASTER 状态。  
- **备节点**：  
  - 启动 Keepalived 服务，设置为 **BACKUP** 状态。  
  - 使用主节点导出的 NeuronEX 配置替换自身配置。  
  - 不启动 NeuronEX 服务，通过 Keepalived 监控主节点状态。  

### **主节点故障切换**

- 当主节点故障时，备节点探测到主节点不可用。  
- 备节点启动自身 NeuronEX 服务，接替主节点承担工作。  

### **主节点恢复切换**

- 当主节点恢复后，备节点探测到主节点重新可用。  
- 备节点停止自身 NeuronEX 服务，主节点重新承担工作。  

### **注意事项**

- 备节点仅在主节点故障且无法恢复时才会接替工作。  
- 主节点的配置需手动复制到备节点。
- 除 systemd 外，用户也可以选择 Docker 部署 NeuronEX，只需将脚本中的启动和停止命令替换为 Docker 命令即可。

## 结语

本文通过详细的示例逐步介绍了 NeuronEX 高可用的配置步骤与方法，操作性强，用户可自行下载 NeuronEX 进行实践。通过 keepalived 实现 NeuronEX 的主备节点高可用，不仅部署简便、成本低，还能有效避免边缘节点数据采集阶段的单点故障问题，显著提升系统稳定性。

了解更多详细内容：[NeuronEX 主备模式最佳实践 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/best-practise/master-backup.html) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
