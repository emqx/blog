[MQTT](https://en.wikipedia.org/wiki/MQTT) is a lightweight, flexible IoT message exchange and data transfer protocol that aims to balance flexibility with hardware/network resources for IoT developers. In order to ensure secure communication, TLS/SSL is often used for communication encryption.

This article mainly introduces how to perform TLS/SSL one-way and two-way authentication via Android and MQTT.

### Preparation

This article uses [Eclipse Paho Android Service](https://github.com/eclipse/paho.mqtt.android) and `BouncyCastle` to add dependencies

```groovy
dependencies {
    implementation 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.1.0'
    implementation 'org.eclipse.paho:org.eclipse.paho.android.service:1.1.1'
    implementation 'org.bouncycastle:bcpkix-jdk15on:1.59'
}
```

Here is the core code section for Android to connect to TLS/SSL

```java
MqttConnectOptions options = new MqttConnectOptions();
SSLSocketFactory sslSocketFactory = ...
options.setSocketFactory(sslSocketFactory);
```

The focus is on how to obtain the `SSLSocketFactory`. The one-way and two-way authentication are described below.

### One-way authentication

One-way authentication means that the server-side authenticates the client. The core code is as follows:

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

We put `ca.crt` under `res/raw` and call:

```java
try {
     InputStream caCrtFileI = context.getResources().openRawResource(R.raw.ca);
     options.setSocketFactory(getSingleSocketFactory(caCrtFile));
} catch (Exception e) {
     e.printStackTrace();
}
```

### Two-way authentication

Two-way authentication means that the server-side and client authenticate each other. The core code is as follows:

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

We need to prepare the server-side certificate, and put the client certificate and secret key under `res/raw`, and then call. Taking care that the password is set to an empty string.

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

This is how to perform TLS/SSL one-way and two-way authentication with MQTT on Android.

