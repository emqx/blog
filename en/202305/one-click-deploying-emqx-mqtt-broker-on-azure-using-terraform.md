## Introduction

MQTT is a lightweight messaging protocol used in the Internet of Things (IoT) to enable communication between devices. As a popular open-source MQTT broker, [EMQX](https://www.emqx.com/en/products/emqx) provides high scalability, reliability, and security for MQTT messaging.

By using Terraform, a widespread Infrastructure as Code (IaC) tool, you can automate the deployment of EMQX MQTT Broker on Azure, making it easy to set up and manage your MQTT infrastructure.

This blog will provide a step-by-step guide on how to set up an Azure project, create a service principal, and write a Terraform configuration file to deploy EMQX MQTT Broker.

## Prerequisites

Before you start, prepare the following:

- An Azure account
- The Azure CLI installed on your local machine
- Terraform installed on your local machine
- A basic understanding of Azure, Terraform, and MQTT

## Set Up the Azure Environment

1. Install the Azure CLI by following the instructions in  [https://docs.microsoft.com/en-us/cli/azure/install-azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Run az login and follow the prompts to authenticate with your Azure account.
3. Run az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/YOUR_SUBSCRIPTION_ID" to create a new service principal with the "Contributor" role. 
4. Note down the appId, password, and tenant values from the output. You'll need them for the Terraform configuration.

## Deploy EMQX on Azure Using Terraform

### Configure Terraform

Configure the Azure provider in your Terraform code.

```
terraform {
  required_version = ">=1.2"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.11.0, <4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.3.2"
    }
  }
}
```

### Create Resource Group 

Resource groups in Azure are logical containers for resources deployed within an Azure subscription.

```
resource "azurerm_resource_group" "example" {
  name     = "example-resource-group"
  location = "East US"
}
```

### Configure Network

**Create a Network Security Group** 

The Network Security Group(NSG) is used to apply security rules to network traffic, allowing or denying traffic based on the direction (inbound or outbound), protocol, source, and destination.

The example allows inbound TCP traffic to port 1883(MQTT).

```
resource "azurerm_network_security_group" "example" {
  name                = "example-security-group"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  security_rule {
    name                       = "mqtt"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "1883"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
```

**Create a VPC Network** 

A virtual network is a logically isolated section of the Azure cloud where you can launch Azure resources. It allows for private communication between resources and helps to structure your cloud infrastructure.

In the following example, the VPC address space is set to 10.0.0.0/16:

```
resource "azurerm_virtual_network" "example" {
  name                = "example-virtual-network"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  address_space       = ["10.0.0.0/16"]
}
```

**Create a Subnet**

A subnet is a range of IP addresses within a virtual network (VNet) that helps organize and isolate resources in a cloud infrastructure.

In the following example,  the address space for the subnet is set to 10.0.1.0/24:

```
resource "azurerm_subnet" "example" {
  name                 = "example-subenet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}
```

**Create a Network Interface** 

A network interface (NIC) is the interconnection between a virtual machine (VM) and the virtual network (VNet).

We assigned the subnet_id to the one we created inside the azurerm_network_interface blocks.

```
resource "azurerm_network_interface" "example" {
  name                = "example-network-interface"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}
```

### Configure EMQX Cluster

**Provide a VM Instance for Each EMQX Node**

The resource azurerm_linux_virtual_machine  simplifies provisioning a Linux VM in Azure by handling various aspects like OS image, networking, storage, and compute resources.

We assigned the resource_group_name and network_interface_ids with the ones we created inside the azurerm_linux_virtual_machine blocks.

```
resource "azurerm_linux_virtual_machine" "example" {
  name                            = "example-virtual-machine"
  resource_group_name             = azurerm_resource_group.example.name
  location                        = azurerm_resource_group.example.location
  size                            = "<YOUR-VM-SIZE>"
  admin_username                  = "azureuser"
  network_interface_ids           = [azurerm_network_interface.example.id]

  admin_ssh_key {
    ...
  }

  os_disk {
    ...
  }

  source_image_reference {
    ...
  }
}
```



**Initiate EMQX Nodes and Create a Cluster**

Initialize each EMQX node after the VM instance is created. First, you must initialize and copy the [init.sh](http://init.sh/) to each none. Then download the EMQX package and execute the [init.sh](http://init.sh/) you’ve copied at each node. Finally, start EMQX separately.

```
resource "null_resource" "emqx" {
  depends_on = [azurerm_linux_virtual_machine.vm]

  count = "<INSTANCE-COUNT>"
  connection {
    type        = "ssh"
    host        = "<HOST-LIST>"
    user        = "azureuser"
    private_key = "<YOUR-PRIVATE-KEY>"
  }

  # config init script
  provisioner "file" {
    content = templatefile("${path.module}/scripts/init.sh", { local_ip = <PRIVATE-IPS>[count.index],
      emqx_lic = <EMQX-LICENSE>, emqx_ca = <EMQX-CA> emqx_cert = <EMQX-CERT>, emqx_key = <PRIVATE-KEY> })
    destination = "/tmp/init.sh"
  }

  # download EMQX package
  provisioner "remote-exec" {
    inline = [
      "curl -L --max-redirs -1 -o /tmp/emqx.zip <EMQX-PACKAGE-URL>"
    ]
  }

  # init system
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init.sh",
      "/tmp/init.sh",
      "sudo mv /tmp/emqx <HOME>",
    ]
  }

  # start EMQX 
  provisioner "remote-exec" {
    inline = [
      "sudo <HOME>/bin/emqx start"
    ]
  }
}
```

In the init.sh, we configure a fixed node list to discover and create clusters automatically:

```
cluster.discovery = static
cluster.static.seeds = emqx1@127.0.0.1,emqx2@127.0.0.1
```

### Configure Load Balancer

To create a Load Balancer with Terraform on Azure, you'll need to use multiple resources: azurerm_lb, azurerm_lb_backend_address_pool, azurerm_lb_probe, azurerm_lb_rule, and azurerm_lb_nat_rule (if needed). This example demonstrates how to create a simple Azure Load Balancer with a backend address pool, health probe, and load balancing rule.

In this example, we create:

- An azurerm_public_ip resource to associate with the Load Balancer.
- An azurerm_lb resource to define the Load Balancer with the frontend IP configuration.
- An azurerm_lb_backend_address_pool resource to define the backend pool for the Load Balancer.
- An azurerm_lb_probe resource to define the health probe for the Load Balancer.
- An azurerm_lb_rule resource to define the Load Balancing rule

```
resource "azurerm_public_ip" "example" {
  name                = "example-public-ip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"
}

resource "azurerm_lb" "example" {
  name                = "example-lb"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  frontend_ip_configuration {
    name                 = "example-frontend-ip"
    public_ip_address_id = azurerm_public_ip.example.id
  }
}

resource "azurerm_lb_backend_address_pool" "example" {
  name                = "example-backend-address-pool"
  loadbalancer_id     = azurerm_lb.example.id
}

resource "azurerm_lb_probe" "example" {
  name                = "example-health-probe"
  loadbalancer_id     = azurerm_lb.example.id
  port                = 1883
  protocol            = "Tcp"
  interval_in_seconds = 5
  number_of_probes    = 2
}

resource "azurerm_lb_rule" "example" {
  name                           = "example-lb-rule"
  loadbalancer_id                = azurerm_lb.example.id
  protocol                       = "Tcp"
  frontend_port                  = 1883
  backend_port                   = 1883
  frontend_ip_configuration_name = "example-frontend-ip"
  backend_address_pool_id        = azurerm_lb_backend_address_pool.example.id
  probe_id                       = azurerm_lb_probe.example.id
}
```

## Conclusion

Deploying EMQX on Azure using Terraform streamlines the management of your IoT infrastructure, allowing you to focus on building applications that leverage the power of connected devices. Following the steps outlined in this blog post, you can easily set up a scalable and reliable MQTT broker on Azure to support your IoT projects.



**Reference:**

Github Repo - [https://github.com/emqx/deploy-emqx-to-azure-with-terraform](https://github.com/emqx/deploy-emqx-to-azure-with-terraform)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
