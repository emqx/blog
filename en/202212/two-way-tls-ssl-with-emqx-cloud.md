## Overview

[EMQX Cloud](https://www.emqx.com/en/cloud) is the first fully hosted MQTT 5.0 cloud messaging service in the world. With the support of EMQX Cloud, you can create an MQTT cluster on the cloud and use the features of [EMQX Enterprise Edition](https://www.emqx.com/en/products/emqx). This allows you to spend more time on business connections and less time for EMQX operation, maintenance, and management.

In this article, we will set up a two-way TLS/SSL authentication for an EMQX Cloud deployment with a third-party certification.

- Let's Encrypt, a free third-party Certificate Authority, will be used to certify a custom domain purchased from AWS Route 53, which will point to the EMQX Cloud deployment.
- OpenSSL will be used for client-side TLS/SSL.
- MQTT X will be used to validate the encrypted connection.

## Prerequisites

- An [EMQX Cloud Professional deployment](https://docs.emqx.com/en/cloud/latest/create/overview.html) up and running: for this example, a deployment to AWS will be used.
- An MQTT client installed: for this example, [MQTT X](https://mqttx.app/docs/downloading-and-installation) will be used.
- A registered domain: for this example, [AWS Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html#domain-register-procedure) will be used.

## Create client-side self-signed certificate

Alternatively to the step by step below, instructions can be followed from the EMQX Cloud [TLS/SSL documentation](https://docs.emqx.com/en/cloud/latest/deployments/tls_ssl.html#creating-self-signed-tsl-ssl-certificate).

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

## Point a subdomain to the EMQX Cloud deployment cluster

1. Copy the EMQX Cloud deployment URL from the EMQX Cloud console. 

   ![Copy the EMQX Cloud deployment URL](https://assets.emqx.com/images/0460a57ccd7cfd43b9c05d192a536eb4.png)

2. Create a CNAME record in AWS Route 53 hosted zone pointing to the EMQX Cloud deployment.

   ![Create a CNAME record](https://assets.emqx.com/images/ab36d2599ca7f100dc32b44a0058445a.png)

   ![Create a CNAME record](https://assets.emqx.com/images/1c7a553600f357988f07e979bcc5c4fc.png)

## Get a certificate for the subdomain

Alternatively to the step by step below, instructions are available from [Let's Encrypt](https://letsencrypt.org/getting-started/)/Certbot for [certbot](https://certbot.eff.org/instructions) and [Route 53 plugin](https://certbot-dns-route53.readthedocs.io/en/stable/index.html). Be sure to select "Other" for the "Software" dropdown, and the "Wildcard" tab.

1. Install package manager, Certbot, and DNS plugin using the CLI:

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

2. Give AWS permissions to the plugin:

   - [Create IAM policy](https://console.aws.amazon.com/iam/home#/policies$new?step=edit) with the following statement, changing `YOURHOSTEDZONEID`:

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

   - Create a new IAM user, attach the new policy to its permissions, and save the `Access key ID` and `Secret access key`.

     ![Create a new IAM user](https://assets.emqx.com/images/445c00f71462e2fdcaa670083bee4359.png)

   - Set credentials for the new IAM user in the CLI as environment variables and acquire a certificate:

     ```
     export AWS_ACCESS_KEY_ID=AKIA---------EXAMPLE
     export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI-----------------EXAMPLEKEY
     
     certbot certonly --dns-route53 -d mqtt.YOURDOMAIN.COM
     ```

## Understanding the Certbot certificates

- `fullchain.pem`: The full chain of certificates involving the certification of the domain. Usually includes three certificates that can be broken down in the following manner:
  - Certificate body (first): the certificate for the registered domain.
  - Intermediate certificate (second): the certificate for Let's Encrypt.
  - Root certificate (third): the certificate from a [trusted certificate authority](https://support.dnsimple.com/articles/what-is-ssl-root-certificate/), which belongs to a select few set of CA's shipped by default in most OS and web browsers.
- `cert.pem`: The first certificate from the full chain.
- `chain.pem`: All the certificates from the full chain, except the first.
- `privkey.pem`: Used to encrypt/decrypt data.

More information from Let's Encrypt on their certificate chain can be found [here](https://letsencrypt.org/certificates/).

## Set up two-way TLS/SSL in EMQX Cloud deployment

1. Click on `+ TLS/SSL` in EMQX Cloud console.

   ![Click on "+ TLS/SSL"](https://assets.emqx.com/images/b64b079c012f62b1ad72355b129aaf5e.png)

2. Select "two-way" for "Type", add the certificates from previous steps to the EMQX Cloud deployment, and click "Confirm".

   - Certificate body: `cert.pem` from Let's Encrypt. The certificate created by Let's Encrypt for the subdomain.

   - Certificate chain: The intermediate (second) certificate in `fullchain.pem` from Let's Encrypt. The chain should include all certificates between the certified (sub)domain and the root certificate, which in this case should be just one.

   - Certificate private key: `privkey.pem` from Let's Encrypt.

   - Client CA certificate: `client-ca.crt` locally created previously with openssl. Since the client connecting to the deployment also needs to be verified, the deployment needs to know the trusted CA to check client certificates with.

     ![Client CA certificate](https://assets.emqx.com/images/838b6c63c9d43f5f8babe1423fe9e1c4.png)

## Test two-way TLS/SSL with MQTT X

1. Ensure the existence of a username and password to connect to the deployment. Help creating users can be found [here](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication).

2. In the Let's Encrypt certificate directory, create a new `root.pem` file and add the root (last) certificate from `fullchain.pem`.

3. Open MQTT X and create a new connection.

   ![Open MQTT X](https://assets.emqx.com/images/54d61c5396c4cca7f71df8a8f8fdd78f.png)

4. Fill out the new connection prompt with the proper information and click "Connect".

   - Host and Port: since TLS is being used, choose `mqtts://` as well as port `8883`. The port number can be confirmed in the EMQX Cloud console. Do not forget to add the certified subdomain in the address field.
   - Username and Password: fill out with an existing EMQX Cloud deployment user (see step 1).
   - Enable both SSL options.
   - Certificate: Choose self signed.
   - Certificates:
   - CA File: `root.pem` manually created from the Let's Encrypt certificates.
   - Certificate Client File: `client.crt` locally created previously with openssl.
   - Client key file: `client.key` locally created previously with openssl.

   ![Fill out the new connection prompt](https://assets.emqx.com/images/4cf2b9ef8e8dfed38b49b55fdc2dcf74.png)

5. Once the connection is successful, a green "SSL" sign should appear and the two-way TLS/SSL is fully configured and ready to be used. It can be further tested by subscribing to a topic then sending a message to the same topic.

   ![the connection is successful](https://assets.emqx.com/images/911f4b18b043a36e7f3215f1aff04e02.png)

>If you get a "Error: unable to get issuer certificate" message, [download](https://letsencrypt.org/certs/isrgrootx1.pem) the [ISRG Root X1 Self-signed](https://letsencrypt.org/certificates/) certificate and use it in the MQTT X "CA file" field. The error occurs because Let's Encrypt's default root certificate is itself certified with an older CA that recently expired, causing some devices to no longer trust it. More information [here](https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/).


## Next steps

Now we have finished setting up a two-way TLS authentication for an EMQX Cloud with a custom domain from Route 53 certified by Let’s Encrypt, tested with MQTT X. Two-way TLS/SSL can provide an important layer of security for communication over the internet, helping to protect sensitive information and prevent attacks.

Continue exploring what EMQX Cloud has to offer:

- [Use Python to connect to EMQX Cloud](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python).
- Persist data and connect to other services with [Data Integrations](https://docs.emqx.com/en/cloud/latest/rule_engine/introduction.html).
- [Access EMQX functions via REST API](https://docs.emqx.com/en/cloud/latest/api/api_overview.html).

For more about EMQX Cloud, please check our [documentation](https://docs.emqx.com/en/cloud/latest/), [GitHub](https://www.github.com/emqx/emqx/issues), [Slack channel](https://slack-invite.emqx.io/), and [forum](https://www.emqx.io/forum/)! For questions, comments, or suggestions, please contact us at [cloud-support@emqx.io](mailto:cloud-support@emqx.io).



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
