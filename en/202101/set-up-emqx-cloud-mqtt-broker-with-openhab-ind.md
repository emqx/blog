
[OpenHab](https://www.openhab.org/) yang juga dikenal sebagai Home Automation Bus terbuka adalah sebuah software home automation open-source yang ditulis dengan Java. Dengan kemampuannya dalam berintegrasi dengan berbagai perangkat, user interface yang jelas, dan mendukung tool yang paling fleksibel sekalipun, openHab menjadi salah satu platform terbaik dalam hal home automation.

Dengan tingkat fleksibilitas yang tinggi dan mudah dipakai, openHAB menyediakan sarana binding agar pengguna dapat mengkoneksikan [MQTT Broker](https://www.emqx.io/products/broker). Dalam artikel ini, saya akan membimbing Anda dalam proses pengaturan [EMQ X Cloud MQTT Broker](https://cloud.emqx.io/) dengan openHAB.



## Apa Itu MQTT?

MQTT, atau panjangnya Message Queuing Telemetry Transport, adalah protokol messaging IoT lightweight berbasis model publish/subscribe. MQTT telah menjadi standar komunikasi IoT karena ia mendukung QoS, sederhana, lightweight dan fitur bandwith-saving nya.



## Apa Itu EMQ X Cloud MQTT?

[EMQ X Cloud](https://cloud.emqx.io/) adalah sebuah produk MQTT perantara messaging untuk domain IoT dari EMQ. Sebagai servis public cloud MQTT 5.0 pertama di dunia yang sepenuhnya dikelola oleh EMQ, EMQ X Cloud menyediakan solusi O&M colocation komplit dan lingkungan unik terisolasi untuk servis MQTT messaging. EMQ X Cloud melayani banyak negara di seluruh dunia dan menyediakan layanan cloud yang terjangkau, aman dan dapat diandalkan untuk aplikasi-aplikasi 5G dan Internet of Everything.  

EMQ X Cloud memiliki 3 jenis paket: Basic, Professional dan Unlimited. Ketiga paket ini menawarkan sejumlah spesifikasi produk yang fleksibel untuk mendukung deployment dari berbagai servis MQTT secara eksklusif untuk Anda dengan salah satu public cloud terkemuka di dunia. Tertarik untuk tau lebih lanjut tentang paket produk EMQ X Cloud? Klik [disini](https://docs.emqx.io/en/cloud/latest/pricing.html). 

Produk mantap seperti ini adalah pilihan tepat untuk diitegrasikan dengan openHAB. Anda dapat mengunjungi bagian [dokumentasi](https://docs.emqx.io/en/cloud/latest/) untuk informasi lebih lanjut mengenai EMQ X Cloud.



## Cara Mem-Binding EMQ X MQTT Broker dengan openHAB 3

Jika ini adalah pengalaman pertama Anda menggunakan EMQ X Cloud, jangan khawatir. Kami akan memandu Anda dalam hal mengkoneksikan Home Assistant dengan EMQ X Cloud.

1. [Buat](https://accounts.emqx.io/signup?continue=https:/cloud.emqx.io/) sebuah akun EMQ X Cloud.

2. Login ke [konsol](https://cloud.emqx.io/console/) EMQ X Cloud dan mulai deployment baru.

   ```tip
   Untuk customer baru EMQ X Cloud, kami akan memberi Anda 30 hari masa coba gratis untuk deployment. Masa coba gratis ini sangat ideal untuk Anda yang ingin mempelajari and menelusuri fitur-fitur EMQ X Cloud.
   ```

3. Setelah deployment baru selesai dibuat dan statusnya menjadi **running**, masukkan informasi otentikasi pengguna (bisa secara manual atau impor dari file).

   ![add authentication](https://docs.emqx.io/assets/img/auth.6543e1b4.png)

4. Unduh openHAB. Anda dapat mengunduh openHAB dengan mudah dengan mengikuti langkah-langkah [disini](https://www.openhab.org/docs/installation/). OpenHAB dapat digunakan dengan bermacam-macam sistem sesuai dengan pilihan Anda.

5. Setelah openHAB selesai diunduh, buka openHAB dan buka bagian [konsol](http://localhost:8080/).

6. Klik `Settings` dan unduh MQTT binding:

    ![openHAB MQTT binding.png](https://static.emqx.net/images/cc395740e3aaa6c3b7f6599f38543c16.png)


7. Tambahkan MQTT ke  `Things`.

    ![add mqtt to openHAB things](https://static.emqx.net/images/b6f79d674a5fb01e49e4a391d751b2d1.png)

8. Pilih`MQTT Broker` dan masukkan informasi deployment yang kita buat sebelumnya.

9. ![select mqtt broker](https://static.emqx.net/images/1589a0bec044b3ce55522c81a47a8f85.png)

   Untuk username dan password, masukkan informasi sesuai dengan yang kita buat sebelumnya.![mqtt broker info](https://static.emqx.net/images/30bc01230493f1da0cb7c39818905a9c.png)

10. Ketika terdapat label berwarna hijau yang menampilkan kata **ONLINE,** artinya Anda telah berhasil mengkoneksikan openHAB dengan EMQ X Cloud. Selamat!

![mqtt broker inline](https://static.emqx.net/images/a29093ef1b02ff829a64a6785c57c9b6.png)

   Anda juga dapat mengecek statusnya dari halaman monitor EMQ X Cloud.

![EMQ X Cloud's monitor page](https://static.emqx.net/images/8077ce96ef86b572fb6c15b1b8343cd0.png)

