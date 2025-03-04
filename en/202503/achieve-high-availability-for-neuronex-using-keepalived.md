## Introduction

NeuronEX is software designed for the industrial sector, specializing in equipment data collection and edge intelligent analysis. It is primarily deployed in industrial settings, facilitating industrial protocol data collection, industrial system data integration, edge data filtering and analysis, AI algorithm integration, and integration with IIoT platforms. It provides low-latency data access management and intelligent analytical services for industrial scenarios.

To ensure high availability, NeuronEX supports a master-backup dual-node deployment scheme combined with Keepalived to achieve automatic failover. This solution effectively addresses scenarios such as software failures or server downtime. When the master node fails, the backup node can automatically take over the service, ensuring business continuity. Additionally, the system supports automatic failback after the master node recovers, ensuring the service always operates in the optimal state.

This blog will introduce how to combine NueronEX’s master-backup deployment with Keepalived to achieve 24/7 uninterrupted service. Users can mitigate the risk of single points of failure while ensuring their data integrity and business sustainability.

## NeuronEX Installation & Configuration

### Installation

Install NeuronEX on both the master and backup nodes. This example uses the x86_64 architecture deb package of NeuronEX 3.4.3. For other installation packages, please visit the [NeuronEX download page](https://www.emqx.com/en/downloads-and-install/neuronex).

```shell
# Download NeuronEX installation package
wget https://www.emqx.com/zh/downloads/neuronex/3.4.3/neuronex-3.4.3-linux-amd64.deb

# Install NeuronEX
sudo dpkg -i neuronex-3.4.3-linux-amd64.deb

# Start NeuronEX
sudo systemctl start neuronex

# Set NeuronEX to start on boot
sudo systemctl enable neuronex
```

### Configuration

1. Access the NeuronEX Dashboard page on the master node and configure the NeuronEX data collection service. For example, configure a Modbus TCP southbound driver to collect data normally, which will be used to verify the master-backup failover functionality.
2. Access the NeuronEX Dashboard page on the backup node. You can manually configure the same data collection service as the master node to verify the failover functionality. Alternatively, you can copy the master node's configuration from `/opt/neuronex/data/` to the same directory on the backup node to overwrite the existing configuration.

With the above configuration, both the master and backup nodes can collect data normally and have consistent functionality. At this point, stop the NeuronEX service on the backup node to simulate the initial state where the master node is running and the backup node is stopped.

```shell
sudo systemctl stop neuronex
```

## Keepalived Installation & Configuration

### Installation

Install Keepalived on both the master and backup nodes:

**Note:** This example uses Keepalived v1.3.9 and Ubuntu 18.04.

```shell
# Install Keepalived
sudo apt-get install keepalived
```

### Configuring Keepalived on the Master Node

On the master node, create the following files in the `/etc/keepalived/` directory: `keepalived.conf`, `master.sh`, `fault.sh`, and `check_alive.sh`.

(1) Configure Keepalived on the master node. The configuration file is located at `/etc/keepalived/keepalived.conf` with the following content:

```
! Configuration File for keepalived
global_defs {
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# Define the script content for the instance execution
vrrp_script check_ex_alived {
        script "/etc/keepalived/check_alive.sh"
        interval 5
        fall 3 # require 3 failures for KO
}


# Define a virtual router instance
vrrp_instance VI_1 {
    # Define the initial state, which can be MASTER or BACKUP
    state MASTER
    # nopreempt
    # Define the working interface
    interface eth0
	
    virtual_router_id 51
	# Define the weight
    priority 100
	# Define the advert frequency, unit is second
    advert_int 1
	# Define the communication authentication mechanism
    authentication {
        auth_type PASS
        auth_pass abcdefgh
    }

    # Define the virtual VIP address, which is not used
    virtual_ipaddress {
        192.160.127.254/17
    }
    unicast_peer {
        10.0.0.223  # Backup node IP address
    }
    # Track script, usually used to execute the script content defined in the vrrp_script
    track_script {
        check_ex_alived
    }

    # Notify script, which will be executed after the host state becomes Master|Backup|Fault
    notify_fault "/etc/keepalived/fault.sh"
    notify_master "/etc/keepalived/master.sh"
}
```

**Note:** Since the IP address of the backup node in this example is `10.0.0.223`, `unicast_peer` in the keepalived.conf file is `10.0.0.223`, please modify it according to actual conditions. The network card bound to the host IP address `10.0.0.127` is `eth0`, `interface` in the keepalived.conf file is `eth0`. Please modify it according to the actual situation.

(2) Configure `master.sh` script on the master node, the configuration file directory is `/etc/keepalived/master.sh`, the content is as follows:

```shell
#!/bin/bash

systemctl start neuronex
```

(3) Configure `fault.sh` script on the master node, the configuration file directory is `/etc/keepalived/fault.sh`, and the content is as follows:

```shell
#!/bin/bash

systemctl stop neuronex
```

(4) Configure `check_alive.sh` script on the master node, the configuration file directory is `/etc/keepalived/check_alive.sh`, and the content is as follows:

```shell
#!/bin/bash

if ! curl 127.0.0.1:8085  >/dev/null 2>&1; then echo "neuronex start failed"; exit 1; fi
```

(5) Start Keepalived on the master node.

```shell
sudo systemctl start keepalived

# Set to start automatically on boot
sudo systemctl enable keepalived
```

### Configuring Keepalived on the Backup Node

Create `keepalived.conf`,  `master.sh`,  `backup.sh` files in the `/etc/keepalived/` directory of the backup node.

(1) Configure Keepalived on the backup node, the configuration file directory is `/etc/keepalived/keepalived.conf`, and the content is as follows:

```
! Configuration File for keepalived
global_defs {
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# Define a virtual router instance
vrrp_instance VI_1 {
    # Define the initial state, which can be MASTER or BACKUP
    state BACKUP
	# Non-preemptive mode
    nopreempt
    # Define the working interface
    interface eth0

    virtual_router_id 51
	# Define the weight
    priority 90
	# Announcement frequency, unit is second
    advert_int 1
	# Define the communication authentication mechanism
    authentication {
        auth_type PASS
        auth_pass abcdefgh
    }

    # Define the virtual VIP address, which is not used
    virtual_ipaddress {
        192.160.127.254/17
    }

    unicast_peer {
        10.0.0.127  # Master node IP address
    }

    # Notify script, which will be executed after the host state becomes Master|Backup|Fault
    notify_master "/etc/keepalived/master.sh"
    notify_backup "/etc/keepalived/backup.sh"
}
```

**Note:** Since the IP address of the master node in this example is `10.0.0.127`, the unicast_peer content in the keepalived.conf file is `10.0.0.127`, please modify it according to actual conditions. The network card bound to the host IP address `10.0.0.223` is `eth0`, `interface` in the keepalived.conf file is `eth0`. Please modify it according to actual conditions.

(2) Configure `master.sh` script on the backup node, the configuration file directory is `/etc/keepalived/master.sh`, and the content is as follows:

```shell
#!/bin/bash

systemctl start neuronex
```

(3) Configure `backup.sh` script on the backup node, the configuration file directory is `/etc/keepalived/backup.sh`, and the content is as follows:

```shell
#!/bin/bash

systemctl stop neuronex
```

(4) Start Keepalived on the backup node.

```shell
sudo systemctl start keepalived

# Set to start automatically on boot
sudo systemctl enable keepalived
```

## Implementation Principle

### Initial State

- **Master Node:**
  - Start the Keepalived service and set it to MASTER state.
  - Start the NeuronEX service to take on the primary workload.
  - Monitor its own NeuronEX status through Keepalived to maintain the MASTER state.
- **Backup Node:**
  - Start the Keepalived service and set it to BACKUP state.
  - Replace its own NeuronEX configuration with the exported configuration from the master node.
  - Do not start the NeuronEX service and monitor the master node's status through Keepalived.

### Failover When Master Node Fails

- When the master node fails, the backup node detects that the master node is unavailable.
- The backup node starts its own NeuronEX service and takes over the primary tasks.

### Failback When Master Node Recovers

- When the master node recovers, the backup node detects that the master node is available again.
- The backup node stops its own NeuronEX service, and the master node resumes primary tasks.

## Notes

- The backup node only takes over tasks when the master node fails and cannot recover.
- The master node's configuration must be manually copied to the backup node.
- In addition to systemd, users can also choose to deploy NeuronEX using Docker by replacing the start and stop commands in the scripts with Docker commands.

## Conclusion

This article offers a comprehensive step-by-step guide for configuring NeuronEX to achieve high availability. By utilizing a master-backup high availability setup with Keepalived, the deployment becomes straightforward and cost-effective. This approach effectively eliminates single points of failure during edge node data collection, significantly enhancing system stability.

Learn more: [NeuronEX High Availability Best Practices](https://docs.emqx.com/en/neuronex/latest/best-practise/master-backup.html)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
