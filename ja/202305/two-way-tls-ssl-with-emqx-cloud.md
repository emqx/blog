## Overview

[EMQX Cloud](https://www.emqx.com/ja/cloud)は、世界初の完全ホスティング型MQTT 5.0クラウドメッセージングサービスです。EMQX Cloudのサポートにより、クラウド上にMQTTクラスタを作成し、[EMQX Enterprise Edition](https://www.emqx.com/ja/products/emqx)の機能を利用することができます。これにより、ビジネス接続に多くの時間を割くことができ、EMQXの運用、保守、管理にかかる時間を短縮することができます。

今回は、EMQX Cloudのデプロイメントに、第三者認証によるTLS/SSLの双方向認証を設定します。

- 無料のサードパーティ認証局であるLet's Encryptを使用して、AWS Route 53から購入したカスタムドメインを認証し、EMQX Cloudのデプロイメントを指し示すことになります。
- クライアントサイドのTLS/SSLには、OpenSSLが使用されます。
- MQTT Xは、暗号化された接続を検証するために使用されます。

## 前提条件

- [EMQX Cloud Professional](https://docs.emqx.com/en/cloud/latest/create/overview.html)のデプロイメントが稼働していること：この例では、AWSへのデプロイメントが使用されます。
- インストールされているMQTTクライアント：この例では、[MQTT X](https://mqttx.app/docs/downloading-and-installation)が使用されます。
- 登録されたドメイン：この例では、[AWS Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html#domain-register-procedure)が使用されます。

## クライアント側の自己署名証明書を作成する

以下のステップの他に、EMQX Cloud [TLS/SSL ドキュメント](https://docs.emqx.com/en/cloud/latest/deployments/tls_ssl.html#creating-self-signed-tsl-ssl-certificate)を参照することも可能です。

```
# Create CA certificate
openssl req -new -newkey rsa:2048 \
    -days 365 -nodes -x509 \
    -subj "/C=US/O=Test Org/CN=Test CA" \
    -keyout client-ca.key -out client-ca.crt

# Create private key
openssl genrsa -out client.key 2048

# Create certificate request file
openssl req -new -key client.key -out client.csr -subj "/CN=Client"

# Create client certifite by feeding the certificate request file to the newly created CA
openssl x509 -req -days 365 -sha256 -in client.csr -CA client-ca.crt -CAkey client-ca.key -CAcreateserial -out client.crt

# View and verify the client certificate
openssl x509 -noout -text -in client.crt
openssl verify -CAfile client-ca.crt client.crt
```

## サブドメインをEMQXクラウド展開クラスタに向ける

1. EMQX CloudのコンソールからEMQX CloudのデプロイメントURLをコピーします。

   ![Copy the EMQX Cloud deployment URL](https://assets.emqx.com/images/0460a57ccd7cfd43b9c05d192a536eb4.png)

2. AWS Route 53 hosted zoneにEMQX Cloudのデプロイメントを指すCNAMEレコードを作成します。

   ![Create a CNAME record](https://assets.emqx.com/images/ab36d2599ca7f100dc32b44a0058445a.png)

   ![Create a CNAME record](https://assets.emqx.com/images/1c7a553600f357988f07e979bcc5c4fc.png)

## サブドメイン用の証明書を取得する

以下のステップに加え、[Let's Encrypt /Certbot](https://letsencrypt.org/getting-started/) の [certbot](https://certbot.eff.org/instructions) および [Route 53](https://certbot-dns-route53.readthedocs.io/en/stable/index.html) プラグインの説明もあります。ソフトウェア」のドロップダウンで「その他」を選択し、「ワイルドカード」タブを必ず選択してください。

1. CLIを使用して、パッケージマネージャー、Certbot、DNSプラグインをインストールします：

   - macOS:

     ```
     # Install Homebrew if needed
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     
     # Install certbot with brew
     brew install certbot
     
     # Install DNS plugin (discussion on why Homebrew doesn't work: https://github.com/certbot/certbot/issues/5680)
     $( brew --prefix certbot )/libexec/bin/pip install certbot-dns-route53
     ```

   - Ubuntu:

     ```
     # Install snap if needed
     sudo snap install core; sudo snap refresh core
     
     # Install certbot with snap and configure it
     sudo snap install --classic certbot
     sudo ln -s /snap/bin/certbot /usr/bin/certbot
     sudo snap set certbot trust-plugin-with-root=ok
     
     # Install DNS plugin
     sudo snap install certbot-dns-route53
     ```

2. プラグインにAWSの権限を付与する：

   - 次のステートメントで[IAMポリシー](https://console.aws.amazon.com/iam/home#/policies$new?step=edit)を作成し、 YOURHOSTEDZONEID を変更します：
     ![Create IAM policy](https://assets.emqx.com/images/9e96e156b9b8db8cc59d82eaaf6db249.png)

     ```
     {
         "Version": "2012-10-17",
         "Id": "certbot-dns-route53 policy",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "route53:ListHostedZones",
                     "route53:GetChange"
                 ],
                 "Resource": [
                     "*"
                 ]
             },
             {
                 "Effect" : "Allow",
                 "Action" : [
                     "route53:ChangeResourceRecordSets"
                 ],
                 "Resource" : [
                     "arn:aws:route53:::hostedzone/YOURHOSTEDZONEID"
                 ]
             }
         ]
     }
     ```

   - 新しいIAMユーザーを作成し、その権限に新しいポリシーを添付して、 `Access key ID` と `Secret access key` を保存します。

     ![Create a new IAM user](https://assets.emqx.com/images/445c00f71462e2fdcaa670083bee4359.png)

   - CLIで新しいIAMユーザーの認証情報を環境変数として設定し、証明書を取得する：

     ```
     export AWS_ACCESS_KEY_ID=AKIA---------EXAMPLE
     export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI-----------------EXAMPLEKEY
     
     certbot certonly --dns-route53 -d mqtt.YOURDOMAIN.COM
     ```

## Certbotの証明書について理解する

- `fullchain.pem` : ドメインの認証に関わる証明書の完全なチェーン。通常、以下の方法で分解できる3つの証明書を含む：
  - 証明書本体（先頭）：登録されたドメインの証明書。
  - 中間証明書（2番目）：Let's Encrypt用の証明書です。
    ルート証明書（3番目）：[信頼できる認証局](https://support.dnsimple.com/articles/what-is-ssl-root-certificate/)からの証明書で、ほとんどのOSやウェブブラウザにデフォルトで搭載されている認証局の中から選ばれた数種類に属します。
- `cert.pem` : フルチェーンからの最初の証明書です。
- `chain.pem` : フルチェーンのうち、最初の証明書を除くすべての証明書。
- `privkey.pem` ：データの暗号化／復号化に使用します。

Let's Encryptの証明書チェーンに関する詳細情報は、[こちら](https://letsencrypt.org/certificates/)をご覧ください。

## EMQX Cloudのデプロイメントで双方向TLS/SSLをセットアップする。

1. EMQX Cloudのコンソールで `+ TLS/SSL`をクリックします。

   ![Click on "+ TLS/SSL"](https://assets.emqx.com/images/b64b079c012f62b1ad72355b129aaf5e.png)

2. タイプ」で「双方向」を選択し、前の手順で作成した証明書をEMQX Cloudの展開に追加し、「確認」をクリックします。

   - 証明書の本文です： Let's Encryptの `cert.pem` です。Let's Encryptがサブドメイン用に作成した証明書です。

   - 証明書チェーンです：Let's Encryptの `fullchain.pem` の中間（2番目）の証明書です。このチェーンには、認証された（サブ）ドメインとルート証明書の間のすべての証明書を含める必要があり、この場合、1つだけであるべきです。

   - 証明書の秘密鍵： `privkey.pem` from Let's Encrypt.

   - クライアントCA証明書です： クライアント CA 証明書: `client-ca.crt` ローカルで openssl を使用して以前に作成されたものです。配置に接続するクライアントも検証する必要があるため、配置はクライアント証明書をチェックするための信頼できる CA を知っておく必要があります。

     ![Client CA certificate](https://assets.emqx.com/images/838b6c63c9d43f5f8babe1423fe9e1c4.png)

## MQTTで双方向のTLS/SSLをテストする X

1. デプロイメントに接続するためのユーザー名とパスワードが存在することを確認します。ユーザーを作成するためのヘルプは、[こちら](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication)でご覧いただけます。

2. Let's Encrypt 証明書ディレクトリで、新しい `root.pem` ファイルを作成し、 `fullchain.pem` からルート (最後の) 証明書を追加します。

3. MQTT Xを開き、新しい接続を作成します。

   ![Open MQTTX](https://assets.emqx.com/images/54d61c5396c4cca7f71df8a8f8fdd78f.png)

4. 新規接続のプロンプトに適切な情報を入力し、「接続」をクリックします。

   - ホストとポート：TLSを使用しているため、 `mqtts://` とポート `8883` を選択します。ポート番号は EMQX Cloud のコンソールで確認できます。アドレス欄には、認証されたサブドメインを忘れずに追加してください。

   - ユーザー名とパスワード：既存のEMQXクラウド導入ユーザーで記入します（ステップ1参照）。

   - SSLオプションの両方を有効にする。

   - 証明書です：自己署名入りを選択します。

   - 証明書です：

   - CAファイル： `root.pem` Let's Encryptの証明書から手動で作成したものです。

   - 証明書クライアントファイル： `client.crt` ローカルで以前opensslで作成したものです。

   - クライアントキーファイルです： `client.key` はopensslで以前にローカルに作成されたものです。

   ![Fill out the new connection prompt](https://assets.emqx.com/images/4cf2b9ef8e8dfed38b49b55fdc2dcf74.png)

5. 接続が成功すると、緑色の「SSL」サインが表示され、双方向TLS/SSLが完全に設定され、使用できるようになります。トピックを購読し、同じトピックにメッセージを送信することで、さらにテストすることができます。

   ![the connection is successful](https://assets.emqx.com/images/911f4b18b043a36e7f3215f1aff04e02.png)

>*Error: unable to get issuer certificate」メッセージが表示された場合は、*[*ISRG Root X1 Self-signed*](https://letsencrypt.org/certificates/) *certificateを*[*ダウンロード*](https://letsencrypt.org/certs/isrgrootx1.pem)*し、MQTT Xの「CA file」フィールドに使用してください。このエラーは、Let's Encryptのデフォルトのルート証明書自体が、最近期限切れになった古いCAで認証されているため、一部のデバイスがそれを信頼しなくなったために発生します。詳しくは*[*こちら*](https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/)*.*

## 次のステップ

これで、EMQX Cloud にLet's Encryptで認証されたRoute 53のカスタムドメインを使用し、MQTT Xでテストした場合の双方向TLS認証の設定が完了しました。双方向TLS/SSLはインターネット上の通信に重要なセキュリティ層を提供し、機密情報の保護や攻撃防止に役立ちます。

EMQX Cloudが提供するものを探求し続けます：

- [Pythonを使用してEMQX Cloudに接続する](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python).
- [データ統合](https://docs.emqx.com/en/cloud/latest/rule_engine/introduction.html)でデータを永続化し、他のサービスに接続する .
- [EMQX の関数に REST API でアクセスする](https://docs.emqx.com/en/cloud/latest/api/api_overview.html) .

EMQX Cloudの詳細については、[ドキュメント](https://docs.emqx.com/en/cloud/latest/)、[GitHub](https://www.github.com/emqx/emqx/issues)、[Slackチャンネル](https://slack-invite.emqx.io/)、および[フォーラム](https://forum.emqx.io/)をご確認ください！質問、コメント、提案については、[cloud-support@emqx.io](mailto:cloud-support@emqx.io) までご連絡ください。
