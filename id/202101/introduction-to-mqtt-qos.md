
[MQTT protokol](https://www.emqx.com/en/mqtt) menentukan kualitas sebuah servis yang menjamin keandalan pengiriman pesan melalui berbagai jaringan. Desain QoS adalah fokus MQTT protokol. Sebagai protokol yang secara khusus didesain untuk skenario IoT, skenario penggunaan MQTT tidaklah hanya terbatas sampai PC, tapi juga mencakup jangkauan yang lebih luas dari jaringan narrow-bandwith dan perangkat berdaya rendah. Jika masalah kualitas transmisi dapat diatas di tingkat protokol, perkembangan aplikasi IoT akan menjadi jauh lebih mudah.


## Tingkat MQTT QoS

MQTT has designed 3 QoS levels.

- Maksimal sekali (0)
- Minimal sekali (1)
- Cuma sekali (2)

QoS 0 adalah mode pengiriman pesan “fire and forget”. Setelah pengirim (publisher atau broker) mengirim sebuah pesan, sistem tidak akan lagi peduli apakah pesan dikirim ke tempat lain dan juga tidak memiliki mekanisme dimana ia akan coba mengirim pesan lagi apabila gagal.

 QoS 1 termasuk mekanisme pengiriman ulang yang sederhana. Setelah pengirim mengirimkan pesan, ia akan menunggu ACK dari si penerima. Jika ia tidak menerima ACK, ia akan mengirim ulang pesan tersebut. Mekanisme ini menjamin bahwa pesan akan terkirim setidaknya sekali, tapi ia tidak dapat menjamin apakah pesan akan diulang.

 QoS 2 didesain untuk melakukan pengiriman ulang dan memiliki mekanisme pencarian pesan untuk memastikan bahwa pesan hanya akan diterima sekali saja.


## Prinsip kerja

### QoS 0 - Maksimal kirim sekali

Ketika QoS adalah 0, pengiriman pesan tergantung dari kemampuan jaringan. Si pengirim akan mengirim pesan sekali, si penerima tidak akan menjawab pesan, dan si pengirim tidak akan menyimpan dan mengirim ulang pesan tersebut. Pesan memiliki tingkat efisiensi tertinggi dalam hal transmisi, tapi bisa saja sama sekali tidak terkirim.

![MQTT_1.png](https://static.emqx.net/images/8c6e4c6b37e76e23b84d3341a2ff9b33.png)

### QoS 1 - Minimal kirim sekali

Ketika QoS adalah 1, ini akan menjamin pesan untuk dikirim setidaknya sekali. MQTT menjamin QOS 1 melalui mekanisme ACK yang sederhana. Si pengirim akan mengirim pesan dan menunggu respon PUBACK dari si penerima. Jika respon PUBACK tidak diterima dalam waktu yang telah ditentukan, si pengirim akan mengatur DUP pesan ke 1 dan mengirim ulang pesan tersebut. Si penerima dapat menerima pesan berulang kali. Tanpa mempedulikan DUP flag, si penerima akan memperlakukan pesan sebagai pesan baru dan mengirimkan PUBACK packet sebagai respon.

![MQTT_2.png](https://static.emqx.net/images/6777e0797f80ddaa1d623b173890f63c.png)

### QoS 2 - Cuma kirim sekali

Ketika QoS adalah 2, pengirim dan penerima akan memastikan bahwa pesan cuma dikirim sekali melalui 2 sesi. QoS 2 memiliki kualitas tertinggi dibandingkan yang lainnya karena kemampuannya dalam mengeliminasi masalah duplikasi dan kehilangan pesan, tapi akan ada biaya tambahan untuk menggunakan servis dengan kualitas seperti ini.

 

Setelah si pengirim mengirimkan pesan dengan QoS 2, ia akan menyimpan pesan yang dikirim dan menunggu si penerima untuk membalas dengan pesan PUBREC. Setelah si pengirim menerima pesan PUBREC, ia akan menghapus pesan yang telah dikirim karena ia tahu bahwa si penerima telah berhasil menerima pesan tersebut. Si pengirim akan menyimpan pesan PUBREC dan merespon dengan PUBREL dan menunggu si penerima untuk membalas dengan pesan PUBCOMP. Ketika si pengirim telah menerima pesan PUBCOMP, ia akan menghapus semua status terdahulu.

Ketika si penerima menerima pesan PUBLISH dengan QoS 2, ia akan memproses pesan tersebut dan merespon dengan PUBREC. Ketika si penerima menerima pesan PUBREL, ia akan menghapus semua data yang tersimpan dan merespon dengan PUBCOMP.

Ketika pesan hilang dalam tahap transmisi, si pengirim akan bertanggung jawab untuk melakukan pengiriman ulang pesan tersebut. Ini terjadi terlepas dari apakah si pengirim adalah publisher atau broker.

Karena itu, si penerima juga perlu merespon ke setiap command message.

![MQTT_3.png](https://static.emqx.net/images/9d1234bb84dc9a3e3c178c55732f8444.png)


## Perbedaan QoS dalam publishing dan subscribing

Pengiriman pesan MQTT QoS bukanlah end-to-end, tetapi antara client dengan server. Level QoS dimana subscriber menerima pesan MQTT tergantung dari QoS pesan yang dikirim dan topik.

- Ketika QoS yang digunakan client A untuk mem-publish lebih besar daripada QoS client B untuk men-subscribe, QoS dari server akan meneruskan pesan ke client B adalah QoS yang digunakan oleh client B untuk men-subscribe.
- Ketika QoS yang digunakan client A untuk mem-publish lebih kecil daripada QoS yang digunakan client B untuk men-subscribe, QoS dari server yang meneruskan pesan ke client B adalah QoS yang digunakan client A untuk mem-publish.

Anda dapat mengacu ke tabel dibawah ini untuk pesan QoS yang client terima di situasi yang berbeda:

| QoS of publish | QoS of subscribe | QoS of received message |
| -------------- | ---------------- | ----------------------- |
| 0              | 0                | 0                       |
| 0              | 1                | 0                       |
| 0              | 2                | 0                       |
| 1              | 0                | 0                       |
| 1              | 1                | 1                       |
| 1              | 2                | 1                       |
| 2              | 0                | 0                       |
| 2              | 1                | 1                       |
| 2              | 2                | 2                       |


## Cara Memilih QoS

Tingkat QoS yang lebih tinggi disesuaikan dengan proses yang lebih rumit dan konsumsi resource sistem yang lebih besar. Aplikasi dapat memilih tingkat QoS yang sesuai dengan skenario jaringan dan kebutuhan bisnis mereka.

### QoS 0 dapat digunakan dalam kasus berikut ini:

- Anda tidak peduli jika pesan sering hilang.
-  Di kasus dimana interaksi pesan antar servis internal dalam subnet yang sama atau jaringan client lain dan server yang sangat stabil.

### QoS 1 dapat digunakan dalam kasus berikut ini:

- Fokus dalam konsumsi resource sistem dan ingin mengoptimalkan kinerja.
- Tidak boleh kehilangan pesan, tapi dapat menerima dan memproses duplikasi pesan.

### QoS 2 dapat digunakan dalam kasus berikut ini:

- Pesan sama sekali tidak boleh hilang (pesan hilang berarti hilang nyawa atau properti) dan juga tidak ingin menerima pesan yang sama.
-  Untuk industri seperti perbankan, pemadam kebakaran, penerbangan, dll yang memerlukan data yang lengkap dengan tepat waktu.
