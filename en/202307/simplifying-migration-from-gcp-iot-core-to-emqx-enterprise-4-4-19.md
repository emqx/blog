## Introduction

[Google Cloud IoT Core](https://www.emqx.com/en/blog/why-emqx-is-your-best-google-cloud-iot-core-alternative) has announced its disappointing retirement in the upcoming August. EMQX, an open-source distributed MQTT broker, is now the recommended alternative for former Google Cloud users due to its powerful features and flexibility in managing large-scale IoT infrastructure.

The lately released [EMQX Enterprise 4.4.19](https://www.emqx.com/en/changelogs/enterprise/4.4.19) offers an enhanced migration process that simplifies the transition from Google Cloud IoT Core to EMQX. This blog will explore the new features and improvements in EMQX Enterprise 4.4.19 that facilitate a smoother migration experience.

## The Challenges of Migration

When migrating from Google Cloud IoT Core to other [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), users may encounter particular challenges related to its unique domain model that encompasses the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). In Google Cloud IoT Core, the core concept revolves around “devices”, which serve as logical representations of physical devices. These devices possess several characteristics:

1. **Grouping in Registries**: Devices are organized into registries, providing a structured way to manage and categorize them within the system.
2. **Unique Device Identification**: Each device is identified by a distinct device ID, a string or automatically assigned by the system as a device number.
3. **Device Authentication**: Devices in Google Cloud IoT Core utilize a public key for authentication purposes when establishing connections with the MQTT broker.
4. **Associated Configuration**: Devices have associated configurations, referred to as "config." Configurations are opaque data blobs that devices can receive from the MQTT broker. These blobs contain relevant settings and parameters for device operation and behavior within the IoT ecosystem.

During the migration process, it becomes essential to consider these aspects of the Google Cloud IoT Core domain model and ensure that the new MQTT broker being adopted can accommodate the required functionality and mappings associated with devices, registries, device identification, authentication, and configuration data.

## Simplifying Migration from Google Cloud IoT Core to EMQX

EMQX understands the importance of minimizing changes to the device code when migrating from Google Cloud IoT Core to the new MQTT broker. With this goal in mind, EMQX has implemented a compatibility layer that significantly simplifies the migration process while maintaining compatibility with the existing device code. This compatibility layer offers the following key features:

1. **Importing Device Config and Authentication Data**: EMQX provides a seamless mechanism to import device configurations and authentication data from Google Cloud IoT Core. This ensures that all the necessary device settings, including registries, device IDs, and associated configurations, can be easily migrated to EMQX without requiring extensive modifications.
2. **Google Cloud IoT Core-Compatible MQTT Authentication**: EMQX supports MQTT authentication in a format fully compatible with Google Cloud IoT Core. This means that devices can continue using their existing authentication mechanisms to connect to EMQX. By preserving the authentication format, the migration process becomes transparent to the devices, reducing the effort required to update the device code.
3. **Device Config in a Google Cloud IoT Core-Compatible Manner**: EMQX ensures that device configurations provided by the compatibility layer are presented in a format compatible with Google Cloud IoT Core. This allows devices to receive their associated config in a familiar structure and format, making it easier to interpret and utilize the data received from the MQTT broker. EMQX also provides the APIs to manage the configs for the devices migrated from Google Cloud IoT Core.

Now, let’s see an example of migrating devices from Google Cloud IoT Core to EMQX.

## Initial Setup on Google Cloud IoT Core

In the initial setup, we have the following components.

- A project and activated Google Cloud IoT Core service:

  ```
  >gcloud projects list
  PROJECT_ID  NAME        PROJECT_NUMBER
  iot-export  IoT Export  283634501352
  >gcloud services list
  NAME                                 TITLE
  ...
  cloudiot.googleapis.com              Cloud IoT API
  ...
  ```

- An IoT registry named `my-registry`:

  ```
  >gcloud iot registries list --region europe-west1 --project iot-export
  ID           LOCATION      MQTT_ENABLED
  my-registry  europe-west1  MQTT_ENABLED
  ```

- Some devices in the registry: Public keys are assigned to the devices. E.g.:

  ```
  >gcloud iot devices describe c2-ec-x509 --region europe-west1 --registry my-registry --project iot-export
  config:
    binaryData: AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0-P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn-AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq-wsbKztLW2t7i5uru8vb6_wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t_g4eLj5OXm5-jp6uvs7e7v8PHy8_T19vf4-fr7_P3-_w==
    cloudUpdateTime: '2023-04-12T14:01:34.862851Z'
    deviceAckTime: '2023-04-19T09:15:53.458746Z'
    version: '2'
  credentials:
  - expirationTime: '1970-01-01T00:00:00Z'
    publicKey:
      format: ES256_X509_PEM
      key: |
        -----BEGIN CERTIFICATE-----
        MIIBEjCBuAIJAPKVZoroXatKMAoGCCqGSM49BAMCMBExDzANBgNVBAMMBnVudXNl
        ZDAeFw0yMzA0MTIxMzQ2NTJaFw0yMzA1MTIxMzQ2NTJaMBExDzANBgNVBAMMBnVu
        dXNlZDBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABAugsuay/y2SpGEVDKfiVw9q
        VHGdZHvLXDqxj9XndUi6LEpA209ZfaC1eJ+mZiW3zBC94AdqVu+QLzS7rPT72jkw
        CgYIKoZIzj0EAwIDSQAwRgIhAMBp+1S5w0UJDuylI1TJS8vXjWOhgluUdZfFtxES
        E85SAiEAvKIAhjRhuIxanhqyv3HwOAL/zRAcv6iHsPMKYBt1dOs=
        -----END CERTIFICATE-----
  gatewayConfig: {}
  id: c2-ec-x509
  lastConfigAckTime: '2023-04-19T09:15:53.450757285Z'
  lastConfigSendTime: '2023-04-19T09:15:53.450839281Z'
  lastErrorStatus:
    code: 9
    message: 'mqtt: The connection broke or was closed by the client.'
  lastErrorTime: '2023-04-19T08:50:38.285599550Z'
  lastEventTime: '1970-01-01T00:00:00Z'
  lastHeartbeatTime: '1970-01-01T00:00:00Z'
  name: projects/iot-export/locations/europe-west1/registries/my-registry/devices/2928540609735937
  numId: '2928540609735937'
  ```

## Connect Devices to MQTT Endpoint

Let us see how an actual device (i.e., client) interacts with the MQTT endpoint. 

1. Prepare a [test script](https://github.com/emqx/emqx-gcp-iot-migrate/blob/main/client-demo.py) for connecting to the endpoint, authenticating with the private key, and obtaining configurations. The code is a slightly modified version of the official [code examples](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/iot/api-client/mqtt_example/cloudiot_mqtt_example.py) for Python.

2. Install the environment:

   ```
   git clone https://github.com/emqx/emqx-gcp-iot-migrate.git
   cd emqx-gcp-iot-migrate
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Fetch google root certificates:

   ```
   curl "https://pki.google.com/roots.pem" --location --output google-roots.pem
   ```

4. Run the test script:

   ```
   python client-demo.py --project "iot-export" --region "europe-west1" --registry "my-registry" --algorithm ES256 --device "c2-ec-x509" --hostname mqtt.googleapis.com --private-key-file ./sample-keys/c2_ec_private.pem --ca-certs ./google-roots.pem
   ```

   The output is:

   ```
   Device client_id is 'projects/iot-export/locations/europe-west1/registries/my-registry/devices/c2-ec-x509'
   Password is eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODIzMzQyNzksImV4cCI6MTY4MjMzNTQ3OSwiYXVkIjoiaW90LWV4cG9ydCJ9.djolGOTtK7OxYN1xh1HmEdNCUPFNNpTg8AA9dAO3wnqUByyZYu6OwmSBDRsb89EfWkxLR5Pszc_fsv5gGv_Fpw
   Subscribing to config topic /devices/c2-ec-x509/config
   on_connect Connection Accepted.
   Received message b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' on topic /devices/c2-ec-x509/config with qos 1
   ```

The output shows the following:

- The client connects to the endpoint with the specially crafted `client_id`.
- It crafts a JWT token and uses it as a password (Google Cloud IoT Core-specific way of authentication).
- It subscribes to the config topic, also following the Google Cloud IoT Core convention.
- It receives the config from the config topic. The message is a binary blob but can be a JSON string or something else.

We saw how things work with Google Cloud IoT Core. We expect the same things also work with EMQX, without modifications to the client code.

## Migrate from GCP IoT Core to EMQX

The device migration consists of the following two tasks:

- Export data from Google Cloud IoT Core;
- Import data into EMQX.

### Export Data from Google Cloud IoT Core

For export, you can use a script utilizing the [Google Cloud IoT Core REST API](https://cloud.google.com/iot/docs/reference/cloudiot/rest).

Run the following command in the same `emqx-gcp-iot-migrate` folder :

```
python gcp-export.py --project iot-export --region europe-west1 --registry my-registry > gcp-data.json
```

The `gcp-data.json` file now contains the data ready for being imported into EMQX.

The easiest way to try EMQX locally is to use Docker.

```
docker run -d --name emqx -p 8883:8883 -p 18083:18083 emqx/emqx:4.4.18
```

8883 is the MQTT port (over TLS), and 18083 is the HTTP API port. 

EMQX facilitates the import of Google Cloud IoT Core device data through Dashboard and Rest API.

### Import Data into EMQX via Dashboard

**Enable the GCP module from Dashboard**

1. Go to EMQX Dashboard. Click `Modules` from the left navigation menu.

2.  On the `Modules` page, click `Add Module`.  In the `Module Select` area, click `Local Modules`. 

3. Locate the `GCP IoT Core Device` and click `Select`   

   ![GCP IoT Core Device](https://assets.emqx.com/images/1791311023baa13f9667d12b3a999474.png)

5. Click `Add` on the page to enable the module.    

   ![Click add](https://assets.emqx.com/images/b05e25a40169759dddd4a2a931efe56e.png)

Now you can see the `GCP IoT Core Device` is listed on the `Modules` page.

 **Import device data** 

1. On the `Modules` page, click the `Manage` button for the `GCP IoT Core Device` module.  

   ![Click the Manage button](https://assets.emqx.com/images/6a2c293a90510e9002b9520fb90dd9c7.png)

2. On the `Devices` tab of the details page, click `Import` to import a batch of device data or `Add` to manually add your device data.   

   - If you click `Import`, a dialogue pops up for you to import the JSON file you have exported from the GCP IoT Core. Select the file and click `Open`.     

     ![Import Json](https://assets.emqx.com/images/5c5c91f935fa194a1344ef7b999c62af.png)

   -  If you click `Add`, a dialogue pops up for you to input the `device ID` and add the public key. 

3. Click `Add` to select the public key format from the drop-down list. Select the key file or enter the content, set the expiration date, and click `Confirm`.    

   ![Click Confirm](https://assets.emqx.com/images/5932c879b4d1d52a888fec16c599458c.png)

You can see the devices are imported. 

### Import Data into EMQX via API

**Enable the GCP module from API**

You can use the following EMQX API to enable GCP compatibility module

```
curl -s -u 'admin:public' -X POST 'http://127.0.0.1:18083/api/v4/modules/' -H "Content-Type: application/json"  --data-raw '{"type": "gcp_device", "config": {}}'
```

**Import data into EMQX**

Use the REST API to import data into EMQX. `admin:public` is the default username and password for EMQX.

```
curl -s -v -u 'admin:public' -X POST 'http://127.0.0.1:18083/api/v4/gcp_devices' --data @gcp-data.json
...
{"data":{"imported":14,"errors":0},"code":0}
```

Now, we see that devices were imported.

### Test the Migration

To test the migration, use the same client code as before, but change the endpoint to the EMQX. You also need to change the CA certificate to the one used by EMQX.

```
docker cp emqx:/opt/emqx/etc/certs/cacert.pem ./сacert.pem
python client-demo.py --project "iot-export" --region "europe-west1" --registry "my-registry" --algorithm ES256 --device "c2-ec-x509" --hostname localhost --private-key-file ./sample-keys/c2_ec_private.pem --ca-certs cacert.pem
```

The output is:

```
Device client_id is 'projects/iot-export/locations/europe-west1/registries/my-registry/devices/c2-ec-x509'
Password is eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODIzNDE2NzgsImV4cCI6MTY4MjM0Mjg3OCwiYXVkIjoiaW90LWV4cG9ydCJ9.04_zR71fmi0YikSxZbb_wxpVTnikt2XIkxkuI6JM6VS0VJ1B8QrggHuUron8MAOSJDJu9SVa2fuuFFjJEKJ-Bw
Subscribing to config topic /devices/c2-ec-x509/config
on_connect Connection Accepted.
Received message b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' on topic /devices/c2-ec-x509/config with qos 1
```

This is just the same as before, but now we are using EMQX instead of Google Cloud IoT Core.

## Device Management APIs

EMQX also provides Device Management API calls to manage EMQX data using "device" terminology.

### Individual Device Configuration Management

To get the configuration for the device `c2-ec-x509`:

```
>curl -s -u 'admin:public' -X GET 'http://127.0.0.1:18083/api/v4/gcp_devices/c2-ec-x509' | jq
{
  "data": {
    "registry": "my-registry",
    "project": "iot-export",
    "location": "europe-west1",
    "keys": [
      {
        "key_type": "ES256_X509_PEM",
        "key": "...",
        "expires_at": 0
      }
    ],
    "deviceid": "c2-ec-x509",
    "created_at": 1685477382,
    "config": "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="
  },
  "code": 0
}
```

To update the configuration for the device `c2-ec-x509` (we saved the configuration to a file `c2-ec-x509.json` for convenience and changed the `config` field):

```
>cat c2-ec-x509.json
{
    "registry": "my-registry",
    "project": "iot-export",
    "location": "europe-west1",
    "keys": [
      {
        "key_type": "ES256_X509_PEM",
        "key": "...",
        "expires_at": 0
      }
    ],
    "config": "bmV3Y29uZmlnCg=="
}

>curl -s -u 'admin:public' -X PUT 'http://127.0.0.1:18083/api/v4/gcp_devices/c2-ec-x509' -H "Content-Type: application/json" -d @c2-ec-x509.json
{"data":{},"code":0}
```

To delete the configuration for the device `c2-ec-x509`:

```
>curl -s -u 'admin:public' -X DELETE 'http://127.0.0.1:18083/api/v4/gcp_devices/c2-ec-x509'
{"data":{},"code":0}
>curl -s -u 'admin:public' -X GET 'http://127.0.0.1:18083/api/v4/gcp_devices/c2-ec-x509' | jq
{
  "message": "device not found"
}
```

### List Devices

To list all devices:

```
>curl -s -u 'admin:public' -X GET 'http://127.0.0.1:18083/api/v4/gcp_devices' | jq
{
  "meta": {
    "page": 1,
    "limit": 10000,
    "hasnext": false,
    "count": 13
  },
  "data": [
    {
      "registry": "my-registry",
      "project": "iot-export",
      "location": "europe-west1",
      "keys": [
        {
          "key_type": "RSA_X509_PEM",
          "key": "...",
          "expires_at": 0
        }
      ],
      "deviceid": "2820826361193805",
      "created_at": 1685477382,
      "config": ""
    },
...
```

The query allows pagination: `_limit` and `_page` parameters:

```
>curl -s -u 'admin:public' -X GET 'http://127.0.0.1:18083/api/v4/gcp_devices?_page=2&_limit=2' | jq
```

## Limitations

It should also be noted that the EMQX is not a drop-in replacement for Google Cloud IoT Core. The mentioned functions and APIs are provided to help with migration. The most notable limitations are:

- EMQX does not support the "gateway" concept. However, this results only in the inability of devices behind a gateway to have gateway-independent credentials.
- Project, location, and registry are not used in EMQX. They are only used to construct or verify Google Cloud IoT Core-compatible client ids. That means that devices imported into EMQX should have globally unique ids to avoid collisions.

## Conclusion

In this article, we have explored the migration process from Google Cloud IoT Core to the latest EMQX Enterprise 4.4.19, highlighting its simplicity and benefits. EMQX Enterprise 4.4.19 offers a comprehensive set of features that empower users with enhanced capabilities for managing and leveraging their IoT infrastructure. This migration not only ensures uninterrupted device connectivity but also opens up opportunities for utilizing the extensive functionality provided by EMQX.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
