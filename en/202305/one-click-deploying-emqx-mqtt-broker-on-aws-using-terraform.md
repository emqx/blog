## Introduction

[MQTT](https://www.emqx.com/en/mqtt-guide) is a lightweight messaging protocol commonly used in IoT (Internet of Things) applications to enable communication between devices. As a [popular open-source MQTT broker, EMQX](https://www.emqx.io/) provides high scalability, reliability, and security for MQTT messaging.

By using Terraform, a widespread Infrastructure as Code (IaC) tool, you can automate the deployment of EMQX MQTT Broker on AWS, making it easy to set up and manage your MQTT infrastructure.

This blog post will provide a step-by-step guide on how to set up an AWS account, create an IAM user, and write a Terraform configuration file to deploy EMQX MQTT Broker.

**You can find the code at:** [https://github.com/emqx/deploy-emqx-to-aws-with-terraform](https://github.com/emqx/deploy-emqx-to-aws-with-terraform) 

## Prerequisites

Before you start, prepare the following:

- An AWS account.
- A [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (1.2.0+) is installed on your local machine.
- A basic understanding of AWS, Terraform, and MQTT.

## Set up the AWS Environment

1. Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2. Create resources using [AWS account](https://aws.amazon.com/free) and [associated credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html).

To use your IAM credentials to authenticate the Terraform AWS provider, set the `AWS_ACCESS_KEY_ID` environment variable.

```
export AWS_ACCESS_KEY_ID=
```

Now, set your secret key.

```
export AWS_SECRET_ACCESS_KEY=
```

## Deploy EMQX on AWS Using Terraform

### Configure Terraform

Configure the AWS provider in your Terraform code.

In this example, we specify that the `hashicorp/aws` provider is required with a version greater than or equal to `4.16`. This provider enables us to interact with AWS resources, such as EC2 instances, VPCs, and load balancers in our Terraform code.

The `required_version` parameter specifies the minimum Terraform version required to use this configuration file. In this case, we require version `1.2.0` or greater.

```
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}
```

### Configure Network

**Create a Network Security Group** 

This resource allows you to define the inbound and outbound rules for the security group.

In this example, we're creating a security group named `example-security-group` . We're allowing inbound traffic on ports 1883 (for MQTT) and 8883 (for MQTT over SSL) and all outbound traffic.

```
resource "aws_security_group" "example_sg" {
  name_prefix = "example-security-group"
  
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port = 1883
    to_port = 1883
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port = 8883
    to_port = 8883
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**Create a VPC Network** 

A Virtual Private Cloud (VPC) is a virtual network you can define within your AWS account.

In this example, we're creating a VPC with a CIDR block of `10.0.0.0/16`, allowing up to 65,536 IP addresses.

```
resource "aws_vpc" "example_vpc" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = "example-vpc"
  }
}
```

**Create a Subnet** 

Once you've defined the `aws_vpc` resource, you can create subnets within the VPC to launch your instances. 

In this example, we're creating a subnet within the VPC. The subnet has a CIDR block of `10.0.1.0/24`, allowing up to 256 IP addresses.

```
resource "aws_subnet" "example_subnet" {
  vpc_id            = "${aws_vpc.example_vpc.id}"
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Name = "example-subnet"
  }
}
```

**Create an Internet Gateway** 

An Amazon VPC internet gateway allows your VPC to communicate with the internet. To create an internet gateway in Terraform, you can use the `aws_internet_gateway` resource.

In this example, we create an internet gateway associated with the `aws_vpc.example_vpc` VPC.

```
resource "aws_internet_gateway" "example_igw" {
  vpc_id = "${aws_vpc.example_vpc.id}"
  
  tags = {
    Name = "example-igw"
  }
}
```

**Create a Route Table** 

An Amazon VPC route table defines the rules determining how network traffic is directed in a VPC. To create a route table in Terraform, you can use the `aws_route_table` resource.

In this example, we create a route table associated with the `aws_vpc.example_vpc` VPC. We're also defining a route that sends all network traffic with a destination of `0.0.0.0/0` (i.e., all traffic not destined for the VPC itself) to the `aws_internet_gateway.example_igw` Internet Gateway.

```
resource "aws_route_table" "example_route_table" {
  vpc_id = "${aws_vpc.example_vpc.id}"
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.example_igw.id}"
  }
  
  tags = {
    Name = "example-route-table"
  }
}
```

Once you've defined the `aws_route_table` resource, you can associate it with a subnet to ensure that instances launched in that subnet use the route table's routing rules. Here's an example `aws_route_table_association` resource block.

In this example, we associate the `aws_route_table.example_route_table` route table with the `aws_subnet.example_subnet` subnet. This ensures that any instances launched in the subnet use the routing rules defined in the route table.

```
resource "aws_route_table_association" "example_subnet_association" {
  subnet_id      = "${aws_subnet.example_subnet.id}"
  route_table_id = "${aws_route_table.example_route_table.id}"
}
```

### Configure EMQX Cluster

**Provide a VM instance for each EMQX Node**

An Amazon EC2 instance is a virtual machine you can launch in the cloud. To create an EC2 instance in Terraform, you can use the `aws_instance` resource.

The `subnet_id` parameter specifies the subnet ID to launch the instance, and the `vpc_security_group_ids` parameter specifies the security group ID to apply to the instance. 

In this example, we're using the `aws_subnet.example_subnet` subnet and the `aws_security_group.example_sg` security group must be defined earlier in the Terraform configuration file.

The `key_name` parameter specifies the name of the key pair to use for SSH access to the instance.

```
resource "aws_instance" "example_instance" {
  ami           = "ami-example"
  instance_type = "t2.micro"
  subnet_id     = "${aws_subnet.example_subnet.id}"
  vpc_security_group_ids = ["${aws_security_group.example_sg.id}"]
  key_name      = "my-key-pair"
  
  tags = {
    Name = "example-instance"
  }
}
```

**Initiate EMQX Nodes and create a Cluster**

Initialize each EMQX node after the VM instance is created. 

1. You must initialize and copy the [init.sh](http://init.sh/) to each one. 
2. Download the EMQX package and execute the [init.sh](http://init.sh/) you’ve copied at each node. 
3. Start EMQX separately.

```
resource "null_resource" "ssh_connection" {
  depends_on = [aws_instance.example_instance]

  count = "<INSTANCE-COUNT>"
  connection {
    type        = "ssh"
    host        = "<HOST-LIST>"
    user        = "ubuntu"
    private_key = "<YOUR-PRIVATE-KEY>"
  }

  # config init script
  provisioner "file" {
    content = templatefile("${path.module}/scripts/init.sh", { local_ip = <PRIVATE-IPS>[count.index],
      emqx_lic = <EMQX-LICENSE> })
    destination = "/tmp/init.sh"
  }

  # download EMQX package
  provisioner "remote-exec" {
    inline = [
      "curl -L --max-redirs -1 -o /tmp/emqx.zip <EMQX-PACKAGE>"
    ]
  }

  # init system
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init.sh",
      "/tmp/init.sh"
    ]
  }

  # start EMQX 
  provisioner "remote-exec" {
    inline = [
      "sudo /home/ubuntu/emqx/bin/emqx start"
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

**Create a TLS certificate**

A self-signed TLS certificate is a certificate that is signed by its private key and is not issued by a trusted Certificate Authority (CA).

In this example:

1. First, create a `tls_private_key` resource to generate a private key for the certificate. The `algorithm` and `rsa_bits` parameters specify the private key's encryption algorithm and key size.
2. Create a `tls_self_signed_cert` resource to generate the self-signed certificate. The `private_key_pem` parameter specifies the private key generated in the previous step. The `validity_period_hours` parameter specifies the validity period of the certificate in hours.
3. The `allowed_uses` parameter specifies the allowed uses for the certificate. We allow the certificate for key encipherment, digital signature, and server authentication.
4. The `dns_names` parameter specifies the DNS names for the certificate. We use a wildcard domain name for the Amazon ELB load balancer hostname by using the `<REGION>` variable to dynamically set the region in the DNS name.
5. The `subject` block specifies the subject information for the certificate, including the common name, organization, province, and country.

```
resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "public_cert" {
  private_key_pem       = "${tls_private_key.key.private_key_pem}"
  validity_period_hours = 87600
  allowed_uses          = ["key_encipherment", "digital_signature", "server_auth"]
  dns_names             = ["*.<REGION>.elb.amazonaws.com"]

  subject {
    common_name  = "*.<REGION>.elb.amazonaws.com"
    organization = "ORAG"
    province     = "STATE"
    country      = "COUNT"
  }
}
```

`aws_acm_certificate` is a resource in Terraform that enables you to manage SSL/TLS certificates in Amazon Web Services (AWS) Certificate Manager (ACM). This resource can request, validate, and import certificates into ACM.

We use the `private_key_pem` and `cert_pem` properties of the `tls_private_key` and `tls_self_signed_cert` resources to specify the ACM certificate's private key and certificate body, respectively.

```
resource "aws_acm_certificate" "example_certificate" {
  private_key      = "${tls_private_key.key.private_key_pem}"
  certificate_body = "${tls_self_signed_cert.public_cert.cert_pem}"
}
```

**Create an ELB Target Group**

An Amazon ELB target group is a group of EC2 instances to which the load balancer distributes incoming traffic. To create a target group in Terraform, you can use the `aws_lb_target_group` resource.

In this example, we're creating a target group with the name `example-target-group`. The `port` parameter specifies the port number that the target group listens on, and the `protocol` parameter specifies the protocol that the target group uses (TCP in this case).

The `vpc_id` parameter specifies the ID of the VPC where the target group is located. In this example, we're using the `aws_vpc.example_vpc` VPC, which must be defined earlier in the Terraform configuration file.

The `health_check` block specifies the health check configuration for the target group.

```
resource "aws_lb_target_group" "example_target_group" {
  name        = "example-target-group"
  port        = 1883
  protocol    = "TCP"
  vpc_id      = "${aws_vpc.example_vpc.id}"
  
  health_check {
    interval     = 30
    port = 1883
    protocol     = "TCP"
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
  
  tags = {
    Name = "example-target-group"
  }
}

```

**Create an ELB**

An Amazon ELB is a Load Balancing service that can distribute incoming network traffic across multiple EC2 instances in a scalable and fault-tolerant manner. To create an ELB in Terraform, you can use the `aws_lb` resource.

In this example, we create an AWS Network Load Balancer named `example-lb`. The `internal` parameter specifies whether the load balancer is internal or external-facing. We set it to false in this case to create an external-facing load balancer.

The `load_balancer_type` parameter specifies the type of load balancer to create. In this case, we set it to `network` to create a Network Load Balancer.

The `subnets` parameter specifies the subnets in which to place the load balancer. In this case, we reference the `id` of an existing subnet using the `aws_subnet` resource.

```
resource "aws_lb" "example_lb" {
  name               = "example-lb"
  internal           = false
  load_balancer_type = "network"
  
  subnets            = ["${aws_subnet.example_subnet.id}"]

  tags = {
    Name = "example-lb"
  }
}
```

**Create an ELB Listener**

An Amazon ELB listener is a process that checks for connection requests and forwards traffic from the load balancer to the target groups. To create a listener with a certificate in Terraform, you can use the `aws_lb_listener` resource.

In this example, we're creating a listener with the `load_balancer_arn` parameter specifying the ARN of the ELB. The `port` parameter specifying the listener port (8883 in this case), and the `protocol` parameter specifying the listener protocol (TLS in this case).

```
resource "aws_lb_listener" "example_listener" {
  load_balancer_arn = "${aws_lb.example_lb.arn}"
  port              = "8883"
  protocol          = "TLS"
  
  certificate_arn   = "${aws_acm_certificate.example_certificate.arn}"
  
  default_action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.example_target_group.arn}"
  }
}

```

## Conclusion

Deploying EMQX on AWS using Terraform streamlines the management of your IoT infrastructure, allowing you to focus on building applications that leverage the power of connected devices. Following the steps outlined in this blog post, you can easily set up a scalable and reliable MQTT broker on AWS to support your IoT projects.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
