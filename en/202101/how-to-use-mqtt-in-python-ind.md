
[Phyton](https://www.python.org/) adalah bahasa pemrograman yang memiliki bermacam-macam fungsi, dapat ditafsirkan dan berlevel tinggi. Diciptakan oleh Guido van Rossum dan pertama kali dirilis di tahun 1991, filosofi desain Python menekankan ke keterbacaan kode dengan penggunaan whitespace yang signifikan. Phyton membantu programer untuk menulis kode yang logis dan jelas untuk projek berskala kecil maupun besar.[^1]

[MQTT](https://www.emqx.io/mqtt) adalah sebuah **protokol messaging IoT lightweight** berbasis model publish/subscribe yang menyediakan servis messaging yang dapat diandalkan dan real-time untuk perangkat IoT dengan hanya menggunakan sedikit kode dan bandwith. MQTT cocok untuk perangkat dengan sumber hardware yang terbatas dan jaringan dengan bandwith yang terbatas pula. Karena itu, protokol MQTT banyak digunakan di IoT, internet HP, tenaga listrik, dan industri lainnya.

Dalam artikel ini, saya akan mengajar Anda cara menggunakan client **paho-mqtt** dan koneksinya, subscribe, messaging, dan fungsi lainnya antara client dan broker MQTT dalam projek Python.



## Memulai Projek

Projek ini menggunakan Python 3.6 dengan tujuan perkembangan dan test. Anda dapat menggunakan command dibawah ini untuk mengecek versi Python.

```
➜  ~ python3 --version             
Python 3.6.7
```

### Pilih client MQTT

[Paho Python Client](https://www.eclipse.org/paho/clients/python/) menyediakan class client yang mendukung MQTT v3.1 dan v3.1.1 dalam Python 2.7 atau 3.x. Ia juga menyediakan fungsi pembantu untuk  memudahkan publikasi pesan ke server MQTT.

### Gunakan pip untuk mengunduh client Paho MQTT

Pip adalah software manajemen untuk paket Python. Software ini menyediakan fungsi find, download, install dan uninstall untuk paket Python.

```bash
pip3 install paho-mqtt
```



## Kegunaan Python MQTT 

### Koneksi ke MQTT broker

Dalam artikel ini, saya akan menggunakan [MQTT broker publik gratis](https://www.emqx.io/mqtt/public-mqtt5-broker) dari EMQ X. Servis ini dibuat dengan berdasarkan [platform cloud MQTT IoT](https://cloud.emqx.io/). Kunci akses broker adalah sebagai berikut:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

#### Impor Paho MQTT Client

```python
from paho.mqtt import client as mqtt_client
```

#### Atur parameter koneksi MQTT Broker

Atur address, port, dan topik koneksi MQTT Broker. Disaat yang sama, kita memanggil fungsi Phython  `random.randint` untuk menghasilkan ID client MQTT secara acak.

```python
broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
```

#### Tulis fungsi koneksi MQTT

Tulis fungsi callback koneksi `on_connect`. Fungsi ini akan dipanggil setelah dikoneksikan dengan client dan kita dapat mengkonfirmasi apakah client telah berhasil dikoneksikan berdasarkan `rc` didalam fungsi ini. Biasanya, kami akan membuat client MQTT disaat yang sama dan client ini akan dikoneksikan ke `broker.emqx.io`.

```python
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

### Publikasi pesan

Pertama, kita perlu mendefinisikan sebuah while loop. Dalam loop ini, kita perlu mengatur fungsi `publish` client MQTT untuk mengirim pesan ke topik `/python/mqtt` tiap detiknya.

```python
 def publish(client):
     msg_count = 0
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1
```

### Subscribe ke pesan

Tulis fungsi callback pesan `on_message`. Fungsi ini akan dipanggil setelah client menerima pesan dari MQTT Broker. Dalam fungsi ini, kita perlu mencetak nama dari topik yang telah di-subscribe dan pesan yang diterima.

```python
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```

### Kode Lengkapnya

Kode publikasi pesan 

```python
# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

```

Kode subscribe pesan

```python
# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
```




## Tes

### Publikasi pesan

Mulai kode publikasi pesan. Disini kita dapat melihat bahwa client telah berhasil terkoneksi dan pesan telah dikirim.

```bash
python3 pub.py
```

![pub.png](https://static.emqx.net/images/8087a35e3b4c6e11e3b432dac024c420.png)

#### Subscribe ke pesan

Mulai kode subscribe pesan. Disini kita dapat melihat bahwa client telah berhasil terkoneksi dan pesan yang dipublikasi telah diterima.

```bash
python3 sub.py
```

![sub.png](https://static.emqx.net/images/24fa48443372da483f06f9cce06b32bc.png)


## Rangkuman

Sejauh ini, kita telah mempelajari cara mengkoneksikan client paho-mqtt ke [MQTT broker publik gratis](https://www.emqx.io/mqtt/public-mqtt5-broker), mengimplimentasi koneksi, mempublikasi pesan dan subscribe pesan antara test client dan MQTT broker.



Python berbeda dari bahasa pemrograman level tinggi lainnya seperti C++ atau Java. Python lebih cocok untuk mengimplimentasikan logika bisnis dari segi perangkat. Penggunaan Python dapat mempermudah kode yang dipakai dan mengurangi biaya interaksi dengan perangkat. Kami percaya bahwa Python akan memiliki aplikasi yang lebih luas dalam bidang IoT.

 

Di artikel selanjutnya, kami akan menulis lebih banyak artikel tentang pengembangan IoT dan Python. Jangan kemana-mana ya!



[^1]: https://en.wikipedia.org/wiki/Python_(programming_language)
