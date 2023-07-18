## はじめに

[MQTT](https://www.emqx.com/ja/mqtt-guide)は、デバイス間の通信を可能にするためにIoT（モノのインターネット）アプリケーションで一般的に使用されている軽量メッセージングプロトコルです。オープンソースのMQTTブローカーとして人気の[EMQX](https://www.emqx.io/)は、MQTTメッセージングに高いスケーラビリティ、信頼性、セキュリティを提供します。

Infrastructure as Code（IaC）ツールとして普及しているTerraformを使用することで、AWS上のEMQX MQTT Brokerのデプロイを自動化し、MQTTインフラのセットアップと管理を容易にすることができます。

このブログポストでは、EMQX MQTT Brokerをデプロイするために、AWSアカウントのセットアップ、IAMユーザーの作成、Terraform設定ファイルの書き方をステップバイステップで説明します。

Terraformのソースコード: https://github.com/emqx/deploy-emqx-to-aws-with-terraform

## 準備事項

始める前に、以下のものを準備してください：

-  AWSアカウント。
- ローカルマシンに[Terraform CLI ](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)(1.2.0+)がインストールされている。
- AWS、Terraform、MQTTの基本的な理解。

## AWS環境のセットアップ

1.  [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)をインストールします。
2.  [AWSアカウント](https://aws.amazon.com/free)と[関連する認証情報](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)を使用してリソースを作成します。

Terraform AWS プロバイダの認証に IAM 認証情報を使用するには、 `AWS_ACCESS_KEY_ID` 環境変数を設定します。

```
export AWS_ACCESS_KEY_ID=
```

次に秘密鍵を設定する。

```
export AWS_SECRET_ACCESS_KEY=
```

## Terraformを使ってAWS上にEMQXをデプロイする

### Terraform設定

TerraformのコードでAWSプロバイダを設定します。

この例では、 `hashicorp/aws` プロバイダが `4.16` 以上のバージョンで必須であることを指定しています。このプロバイダによって、Terraformコード内でEC2インスタンスやVPC、ロードバランサーなどのAWSリソースとやり取りできるようになります。

`required_version` パラメータは、この設定ファイルを使うために必要なTerraformの最小バージョンを指定します。この場合、バージョン `1.2.0` 以上が必要です。

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

### ネットワーク設定

**ネットワークセキュリティグループの作成**

このリソースでは、セキュリティグループのインバウンドルールとアウトバウンドルールを定義することができます。

この例では、 `example-security-group` というセキュリティグループを作成します。ポート 1883（MQTT 用）と 8883（MQTT over SSL 用）のインバウンド・トラフィックと、すべてのアウトバウンド・トラフィックを許可しています。

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

**VPCネットワークの作成**

仮想プライベートクラウド（VPC）は、AWSアカウント内で定義できる仮想ネットワークです。

この例では、 `10.0.0.0/16` のCIDRブロックでVPCを作成し、最大65,536のIPアドレスを許可しています。

```
resource "aws_vpc" "example_vpc" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = "example-vpc"
  }
}
```

**サブネットの作成**

`aws_vpc` リソースを定義したら、VPC内にサブネットを作成してインスタンスを起動できます。

この例では、VPC内にサブネットを作成します。サブネットのCIDRブロックは `10.0.1.0/24` で、最大256個のIPアドレスが使用できます。

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

**インターネット・ゲートウェイを作る**

Amazon VPCのインターネットゲートウェイは、VPCがインターネットと通信できるようにします。Terraformでインターネットゲートウェイを作成するには、 `aws_internet_gateway` リソースを使います。

この例では、 `aws_vpc.example_vpc` VPCに関連するインターネット・ゲートウェイを作成します。

```
resource "aws_internet_gateway" "example_igw" {
  vpc_id = "${aws_vpc.example_vpc.id}"

  tags = {
    Name = "example-igw"
  }
}
```

**ルートテーブルの作成**

Amazon VPCのルートテーブルは、VPC内のネットワークトラフィックの方向性を決定するルールを定義します。Terraformでルートテーブルを作成するには、 `aws_route_table` リソースを使います。

この例では、 `aws_vpc.example_vpc` VPCに関連するルートテーブルを作成します。また、 `0.0.0.0/0` を宛先とするすべてのネットワーク トラフィック（つまり、VPC自身を宛先としないすべてのトラフィック）を `aws_internet_gateway.example_igw` インターネット ゲートウェイに送信するルートを定義しています。

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

`aws_route_table` リソースを定義したら、それをサブネットに関連付けることで、そのサブネットで起動したインスタンスがルートテーブルのルーティングルールを使うようにすることができます。以下に `aws_route_table_association` リソースブロックの例を示します。

この例では、 `aws_route_table.example_route_table` ルートテーブルを `aws_subnet.example_subnet` サブネットに関連付けます。これにより、サブネットで起動されたインスタンスがルートテーブルで定義されたルーティングルールを使うようになります。

```
resource "aws_route_table_association" "example_subnet_association" {
  subnet_id      = "${aws_subnet.example_subnet.id}"
  route_table_id = "${aws_route_table.example_route_table.id}"
}
```

### EMQXクラスタの設定

**各 EMQX ノードに VM インスタンスを提供する。**

Amazon EC2インスタンスはクラウド上で起動できる仮想マシンだ。TerraformでEC2インスタンスを作成するには、 `aws_instance` リソースを使います。

`subnet_id` パラメータはインスタンスを起動するサブネットIDを指定し、 `vpc_security_group_ids` パラメータはインスタンスに適用するセキュリティグループIDを指定します。

この例では、 `aws_subnet.example_subnet` サブネットを使用しており、 `aws_security_group.example_sg` セキュリティグループはTerraformの設定ファイルで先に定義しておく必要があります。

`key_name` パラメーターは、インスタンスへのSSHアクセスに使用するキー・ペアの名前を指定します。

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

**EMQXノードの起動とクラスタの作成**

VMインスタンスの作成後、各EMQXノードを初期化する。

1. それぞれを初期化して[init.sh](http://init.sh/)をコピーする必要がある。
2. EMQXパッケージをダウンロードし、コピーした[init.sh](http://init.sh/)を各ノードで実行する。
3.  EMQXを別途起動する。

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

init.shでは、クラスタを自動的に発見して作成するために、固定ノードリストを設定する：

```
cluster.discovery = static
cluster.static.seeds = emqx1@127.0.0.1,emqx2@127.0.0.1
```

### ロードバランサーの設定

**TLS証明書を作成する**

自己署名TLS証明書とは、秘密鍵で署名された証明書で、信頼できる認証局（CA）から発行されたものではない。

 この例では

1. まず、 `tls_private_key` リソースを作成し、証明書の秘密鍵を生成する。 `algorithm` と `rsa_bits` パラメータで、秘密鍵の暗号化アルゴリズムと鍵のサイズを指定する。
2. `tls_self_signed_cert` リソースを作成し、自己署名証明書を生成する。 `private_key_pem` パラメータには、前のステップで生成した秘密鍵を指定する。 `validity_period_hours` パラメータには、証明書の有効期間を時間単位で指定する。
3. `allowed_uses` パラメータは、証明書の許可される用途を指定する。ここでは、鍵暗号化、電子署名、サーバ認証のための証明書を許可する。
4. `dns_names` パラメーターは証明書のDNS名を指定します。DNS名のリージョンを動的に設定するために `<REGION>` 変数を使用して、Amazon ELBロードバランサーのホスト名にワイルドカードドメイン名を使用します。
5. `subject` ブロックは、コモン・ネーム、組織、都道府県、国など、証明書のサブジェクト情報を指定する。

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

`aws_acm_certificate` はTerraformのリソースで、Amazon Web Services (AWS) Certificate Manager (ACM)でSSL/TLS証明書を管理できるようにします。このリソースはACMへの証明書のリクエスト、検証、インポートを行うことができます。

ACM証明書の秘密鍵と証明書本体をそれぞれ指定するために、 `tls_private_key` と `tls_self_signed_cert` リソースの `private_key_pem` と `cert_pem` プロパティを使用する。

```
resource "aws_acm_certificate" "example_certificate" {
  private_key      = "${tls_private_key.key.private_key_pem}"
  certificate_body = "${tls_self_signed_cert.public_cert.cert_pem}"
}
```

**ELBターゲット・グループの作成**

Amazon ELBのターゲットグループは、ロードバランサーが受信トラフィックを分散するEC2インスタンスのグループだ。Terraformでターゲットグループを作成するには、 `aws_lb_target_group` リソースを使います。

この例では、 `example-target-group` という名前でターゲットグループを作成しています。 `port` パラメーターはターゲットグループがリッスンするポート番号を指定し、 `protocol` パラメーターはターゲットグループが使用するプロトコル（この場合はTCP）を指定します。

`vpc_id` パラメータは、対象グループが配置されているVPCのIDを指定します。この例では `aws_vpc.example_vpc` というVPCを使っていますが、これはTerraformの設定ファイルで先に定義しておく必要があります。

`health_check` ブロックは、ターゲットグループのヘルスチェック設定を指定する。

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

**ELBの作成**

Amazon ELBは、スケーラブルでフォールトトレラントな方法で複数のEC2インスタンスに受信ネットワークトラフィックを分散できるロードバランシングサービスだ。TerraformでELBを作成するには、 `aws_lb` リソースを使います。

この例では、 `example-lb` という名前の AWS Network Load Balancer を作成します。 `internal` パラメーターはロードバランサーが内部向けか外部向けかを指定します。今回はこれを false にして、外部向けのロードバランサーを作成します。

`load_balancer_type` パラメータは、作成するロードバランサの種類を指定します。この例では、 `network` に設定して Network Load Balancer を作ります。

`subnets` パラメータはロードバランサを置くサブネットを指定します。この場合、 `aws_subnet` リソースを使って既存のサブネットの `id` を参照します。

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

**ELBリスナーの作成**

Amazon ELBリスナーは、接続リクエストをチェックし、ロードバランサーからターゲットグループへトラフィックを転送するプロセスです。Terraformで証明書付きのリスナーを作成するには、 `aws_lb_listener` リソースを使います。

この例では、 `load_balancer_arn` パラメーターでELBのARNを指定してリスナーを作成している。 `port` パラメーターはリスナー・ポート（この場合は8883）を指定し、 `protocol` パラメーターはリスナー・プロトコル（この場合はTLS）を指定する。

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

## まとめ

Terraformを使用してAWS上にEMQXをデプロイすることで、IoTインフラの管理を効率化し、接続されたデバイスのパワーを活用するアプリケーションの構築に集中することができます。このブログポストで説明するステップに従って、IoT プロジェクトをサポートするためのスケーラブルで信頼性の高い MQTT ブローカーを AWS 上で簡単にセットアップすることができます。



<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
