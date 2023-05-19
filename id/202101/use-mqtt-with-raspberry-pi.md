[Raspberry Pi](https://www.raspberrypi.org/) adalah sebuah komputer single-board kecil berbasis ARM yang dikembangkan oleh Raspberry Pi Foundation di UK. Board ini menyediakan interface ESB dan ethernet yang dapat dikoneksikan ke keyboard, mouse, dan kabel jaringan. Board ini memiliki fungsi dasar PC dan Raspberry Pi dapat diintegrasikan dengan Wi-Fi, bluetooth, bermacam-macam GPIO, dan banyak digunakan dalam kelas, hiburan keluarga, IoT, dll.



 [MQTT](https://www.emqx.com/en/mqtt-guide) adalah sebuah **protokol messaging IoT lightweight** berbasis model publish/subscribe yang menyediakan servis messaging yang dapat diandalkan dan real-time untuk perangkat IoT dengan hanya menggunakan sedikit kode dan bandwith. MQTT cocok untuk perangkat dengan sumber hardware yang terbatas dan jaringan dengan bandwith yang terbatas pula. Karena itu, protokol MQTT banyak digunakan di IoT, internet HP, tenaga listrik, dan industri lainnya.



 Dalam projek ini, kita akan menggunakan Python untuk menulis sebuah client MQTT sederhana dalam Raspberry Pi dan mengimplimentasi koneksi, subscribe, unsubscribe, messaging, dan fungsi lain antara client tersebut dan MQTT broker.



## Persiapan

### Unduh Python3 

Projek ini dikembangkan dengan Python 3. Biasanya Raspberry Pi memiliki Python3 bawaan. Jika Anda kurang yakin, silahkan pakai command dibawah untuk mengkonfirmasi.

```
python3 --version 
```

Jika hasilnya menampilkan Python 3.x.x (angka), artinya Python3 telah terunduh. Jika belum, silahkan pakai command apt untuk mengunduhnya (atau ikuti [langkah-langkah pengunduhan Python3](https://wiki.python.org/moin/BeginnersGuide/Download)).

```
sudo apt install python3 
```

### Unduh library MQTT client

Kita perlu mengunduh library **paho-mqtt** agar mudah dikoneksikan ke MQTT broker. Anda dapat memilih salah satu metode dibawah ini untuk mengunduh..

Pakai source code ini untuk mengunduh

```
git clone https://github.com/eclipse/paho.mqtt.python 
cd paho.mqtt.python 
python3 setup.py install
```

Pakai pip3 untuk mengunduh

```
pip3 install paho-mqtt 
```



## Kegunaan MQTT

### Koneksi dengan MQTT broker

Dalam artikel ini, kita akan menggunakan [MQTT broker publik gratis](https://www.emqx.com/en/mqtt/public-mqtt5-broker) yang disediakan oleh EMQX. Pembuatan servis ini berbasis [platform cloud MQTT IoT](https://www.emqx.com/en/cloud). Akses informasi broker adalah sebagai berikut:


* Broker: **broker.emqx.io** 
* TCP Port: **1883** 
* Websocket Port: **8083** 

Jika perlu, Anda dapat menggunakan docker untuk mengunduh EMQX broker secara cepat dan lokal.

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 18083:18083 emqx/emqx 
```

**Contoh kode koneksi**

```python
# test_connect.py 
import paho.mqtt.client as mqtt 

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client() 
client.on_connect = on_connect 
client.connect("broker.emqx.io", 1883, 60) 
client.loop_forever() 
```

 Simpan kode diatas sebagai test_connect.py file dan mulai:

```
python3 test_connect.py 
```

Kita menilai kode respon dengan fungsi on_connect. Jika hasilnya 0, lalu cetak `Connected success` untuk merepresentasi koneksi yang sukses. Jika hasilnya adalah angka lain, representasi kode respon adalah sebagai berikut.

> ```undefined
> 0: connection succeeded
> 1: connection failed - incorrect protocol version
> 2: connection failed - invalid client identifier
> 3: connection failed - the broker is not available
> 4: connection failed - wrong username or password
> 5: connection failed - unauthorized
> 6-255: undefined
> If it is other issues, you can check the network situation, or check whether `paho-mqtt` has been installed.
> ```

Dalam konsep protokol MQTT, pesan dikirim melalui topik. Contohnya, sebuah perangkat mengirimkan pesan ke topik T, hanya perangkat yang ter-subscribe ke topik T dapat menerima pesan tersebut. Karena itu, sebenarnya tidak berguna jika kita cuma mengakses MQTT broker. Jika Anda ini menggunakan servis MQTT secara penuh, Anda perlu tahu cara mempublikasi dan subscribe.

### Subscribe

Buka editor apapun dan masukkan kode berikut ini, lalu simpan sebagai file subscriber.py.

```python
# subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("raspberry/topic")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
```

Dengan fungsi  `subscribe()`, Raspberry Pi akan dapat men-subscribe ke sebuah topik.

Dengan kode ini, kita akan men-subscribe ke topik  `raspberry/topic` dan memantau pesan.

Selain itu, kita juga akan menggunakan  `will_set()` untuk mengatur will message. Will message adalah sebuah fitur dari MQTT dimana ketika sebuah perangkat ditutup secara tidak sengaja, ia akan mengirim pesan ke topik yang spesifik. Dengan ini, kita dapat mengetahui apakah Raspberry Pi telah ditutup atau jika jaringan sedang tidak normal.

### Publikasi pesan

Buka editor apapun dan masukkan kode dibawah ini, kemudian simpan sebagai file publisher.py.

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

# send a message to the raspberry/topic every 1 second, 5 times in a row
for i in range(5):
  	# the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_forever()
```

Fungsi `publish()` akan mengirim pesan ke sebuah topik. Dalam kode diatas, kita akan mengirim pesan ke topik  `raspberry/topic`. Parameter QoS adalah fitur lain yang dimiliki MQTT. Jika Anda ingin tahu lebih banyak konten tentang QoS, Anda dapat mengunjungi [Pengenalan MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos). Disini kita akan mengaturnya ke 0.

## Tes

Kita akan menggunakan [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) untuk melakukan beberapa tes dibawah ini.

### Tes men-subscribe topik

Mulai kode Python dan kirim pesan secara aktif.

1. Buka terminal, mulai kode Python, dan pantau pesan.

   ```
   python3 subscriber.py
   ```

2. Pakai MQTTX client untuk mengkoneksikan ke MQTT broker dan kirim pesan ke topik  `raspberry/topic`.

   ![7B5ORTmqFbJJj6mM__thumbnail.png](https://assets.emqx.com/images/cc93d1c6d99f3bfa3a78d8472a6209af.jpg)

3. Lihat informasi terminal Raspberry Pi dan Anda akan melihat pesan yang dipublikasi oleh MQTTX.


  ![ZKNT7l232qHsjQYC__thumbnail.png](https://assets.emqx.com/images/9c4e5b191e9bd00317fed06f94b13850.png)

### Tes publikasi pesan


1. Subscribe ke topik `raspberry/topic` dalam MQTTX client.

1. Mulai kode Python di terminal.

![k19xv59gQdqnpPog__thumbnail.png](https://assets.emqx.com/images/9ea832adda032c9297c84fbf585fb294.png)

1. Cek pesan yang dipublikasi Raspberry Pi dalam MQTTX client.

   ![mp39coxpnEprWOE6__thumbnail.png](https://assets.emqx.com/images/07ffb81c764145100b1e21572357c675.jpg)

### Tes will message 

Selanjutnya, kita akan mengetes apakah pengaturan will message telah berhasil.


1. Subscribe ke `raspberry/status` dalam MQTTX client.

   ![XKo2GYFsqSLc7nVH__thumbnail.png](https://assets.emqx.com/images/c704c8b0f7117079306d16b5af8c2557.jpg)

2. Coba ganggu jalannya program atau matikan koneksi Raspberry Pi.

3. Cek apakah pesan  `raspberry/status` telah diterima didalam MQTTX client.

  ![RXNIVuQ7HK0z05RV__thumbnail.png](https://assets.emqx.com/images/048da27682c9a86c536f85ffd6417bf2.jpg)



## Rangkuman

Kita telah berhasil menggunakan library Python MQTT client **paho-mqtt** untuk menulis dan mengetes client Raspberry Pi, mengimplimentasi koneksi, subscribe, unsubscribe, messaging dan fungsi lainnya diantara client tersebut dan MQTT broker.

Sejauh ini, Anda telah mempelajar dasar-dasar penggunaan servis MQTT. Meskipun ini hanyalah satu bagian dari servis MQTT, ini cukup untuk membuat beberapa hal yang menarik seperti:

1. Memakai HP untuk mengirim pesan MQTT, mengontrol Raspberry Pi dari jarak jauh.

2. Mengirim informasi perangkat Raspberry Pi ke MQTT broker secara rutin dan menerima pesan melalui HP jadi Anda dapat memantaunya kapapun.

3. Anda dapat mengakses MQTT broker melalui Raspberry Pi dan memakai berbagai macam sensor dan modul ESP untuk membuat banyak aplikasi IoT.

Selanjutnya, kami akan menulis lebih banyak artikel tentang pengembangan IoT dan Raspberry Pi. Jangan kemana-mana ya!
