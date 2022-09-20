[MQTT](https://zh.wikipedia.org/zh-hans/MQTT) 是一种轻量级的、灵活的物联网消息交换和数据传递协议，致力于为 IoT 开发人员实现灵活性与硬件/网络资源的平衡。为了确保通讯安全，通常使用 TLS/SSL 来进行通讯加密。

本文主要介绍如何通过 Android 与 MQTT 进行 TLS/SSL 单向认证和双向认证。

### 准备

本文使用 [Eclipse Paho Android Service](https://github.com/eclipse/paho.mqtt.android) 和 `BouncyCastle`，添加依赖

```groovy
dependencies {
    implementation 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.1.0'
    implementation 'org.eclipse.paho:org.eclipse.paho.android.service:1.1.1'
    implementation 'org.bouncycastle:bcpkix-jdk15on:1.59'
}
```

以下是 Android 连接 TLS/SSL 的核心代码部分

```java
MqttConnectOptions options = new MqttConnectOptions();
SSLSocketFactory sslSocketFactory = ...
options.setSocketFactory(sslSocketFactory);
```

重点在于如何获取 `SSLSocketFactory`，下面对单向认证和双向认证分别进行说明。

### 单向认证

单向认证是指客户端认证服务端，以下是核心代码

```java
 public static SSLSocketFactory getSingleSocketFactory(InputStream caCrtFileInputStream) throws Exception {
        Security.addProvider(new BouncyCastleProvider());
        X509Certificate caCert = null;

        BufferedInputStream bis = new BufferedInputStream(caCrtFileInputStream);
        CertificateFactory cf = CertificateFactory.getInstance("X.509");

        while (bis.available() > 0) {
            caCert = (X509Certificate) cf.generateCertificate(bis);
        }
        KeyStore caKs = KeyStore.getInstance(KeyStore.getDefaultType());
        caKs.load(null, null);
        caKs.setCertificateEntry("cert-certificate", caCert);
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(caKs);
        SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
        sslContext.init(null, tmf.getTrustManagers(), null);
        return sslContext.getSocketFactory();
    }
```

我们把 `ca.crt` 放到 `res/raw` 下，然后调用

```java
try {
     InputStream caCrtFileI = context.getResources().openRawResource(R.raw.ca);
     options.setSocketFactory(getSingleSocketFactory(caCrtFile));
} catch (Exception e) {
     e.printStackTrace();
}
```

### 双向认证

双向认证是指服务端和客户端相互认证，以下是关键代码

```java
public static SSLSocketFactory getSocketFactory(InputStream caCrtFile, InputStream crtFile, InputStream keyFile,
                                                    String password) throws Exception {
        Security.addProvider(new BouncyCastleProvider());

        // load CA certificate
        X509Certificate caCert = null;

        BufferedInputStream bis = new BufferedInputStream(caCrtFile);
        CertificateFactory cf = CertificateFactory.getInstance("X.509");

        while (bis.available() > 0) {
            caCert = (X509Certificate) cf.generateCertificate(bis);
        }

        // load client certificate
        bis = new BufferedInputStream(crtFile);
        X509Certificate cert = null;
        while (bis.available() > 0) {
            cert = (X509Certificate) cf.generateCertificate(bis);
        }

        // load client private cert
        PEMParser pemParser = new PEMParser(new InputStreamReader(keyFile));
        Object object = pemParser.readObject();
        JcaPEMKeyConverter converter = new JcaPEMKeyConverter().setProvider("BC");
        KeyPair key = converter.getKeyPair((PEMKeyPair) object);

        KeyStore caKs = KeyStore.getInstance(KeyStore.getDefaultType());
        caKs.load(null, null);
        caKs.setCertificateEntry("cert-certificate", caCert);
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(caKs);

        KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
        ks.load(null, null);
        ks.setCertificateEntry("certificate", cert);
        ks.setKeyEntry("private-cert", key.getPrivate(), password.toCharArray(),
                new java.security.cert.Certificate[]{cert});
        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        kmf.init(ks, password.toCharArray());

        SSLContext context = SSLContext.getInstance("TLSv1.2");
        context.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

        return context.getSocketFactory();
    }
```

我们需要准备好 ca 证书，客户端证书和秘钥放到 `res/raw` 下，然后调用，注意密码设为空字符串

```java
try {
    InputStream caCrtFile = context.getResources().openRawResource(R.raw.ca);
    InputStream crtFile = context.getResources().openRawResource(R.raw.cert);
    InputStream keyFile = context.getResources().openRawResource(R.raw.key);
    options.setSocketFactory(getSocketFactory(caCrtFile, crtFile, keyFile, ""));
} catch (Exception e) {
    e.printStackTrace();
}
```

以上就是如何在 Android 上与 MQTT 进行 TLS/SSL 单向认证和双向认证。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
