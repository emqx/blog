Dalam beberapa tahun terakhir ini, permintaan masyarakat akan keamananan, kemudahan, dan kenyamanan dalam rumah telah meningkat. Home automation menjadi semakin populer. [Home Assistant](https://www.home-assistant.io/), sebuah platform home automation open-source yang populer menyediakan system kontrol terpusat yang aman dan mudah digunakan. Di dalam artikel ini, saya akan mengajar Anda cara menggunakan [EMQX Cloud MQTT Broker](https://www.emqx.com/en/cloud) untuk dikoneksikan dengan Home Assistant.

## Apa Itu MQTT Broker?

MQTT adalah network protocol berjenis publish-subscribe **lightweight** yang menjembatani pesan antara beberapa perangkat. [MQTT broker](https://www.emqx.com/en/products/emqx) adalah sebuah server yang menerima semua pesan dari client dan kemudian mengirimkan pesan tersebut ke destinasi client yang sesuai.

## Mengapa EMQX Cloud?

[EMQX Cloud](https://www.emqx.com/en/cloud) adalah sebuah produk MQTT perantara messaging untuk domain IoT dari EMQ. Sebagai servis public cloud MQTT 5.0 pertama di dunia yang sepenuhnya dikelola oleh EMQ, EMQX Cloud menyediakan solusi O&M colocation komplit dan lingkungan unik terisolasi untuk servis MQTT messaging. EMQX Cloud melayani banyak negara di seluruh dunia dan menyediakan layanan cloud yang terjangkau, aman dan dapat diandalkan untuk aplikasi-aplikasi 5G dan Internet of Everything. 

 

EMQX Cloud memiliki 3 jenis paket: Basic, Professional dan Unlimited. Ketiga paket ini menawarkan sejumlah spesifikasi produk yang fleksibel untuk mendukung deployment dari berbagai servis MQTT secara eksklusif untuk Anda dengan salah satu public cloud terkemuka di dunia. Tertarik untuk tau lebih lanjut tentang paket produk EMQX Cloud? Klik [disini](https://docs.emqx.io/en/cloud/latest/pricing.html).

 

Produk mantap seperti ini adalah pilihan tepat untuk diitegrasikan dengan Home Assistant. Anda dapat mengunjungi [dokumentasi EMQX Cloud](https://docs.emqx.io/en/cloud/latest/) untuk informasi lebih lanjut mengenai EMQX Cloud.

## Set Up Home Assistant dengan EMQX Cloud

Jika ini adalah pengalaman pertama Anda menggunakan EMQX Cloud, jangan khawatir. Kami akan memandu Anda dalam hal mengkoneksikan Home Assistant dengan EMQX Cloud.

1. [Buat](https://accounts.emqx.io/signup?continue=https:/cloud.emqx.io/) sebuah akun EMQX Cloud.

2. Login ke [EMQX Cloud Console](https://cloud.emqx.io/console/) dan mulai deployment baru.

   ```tip
   Untuk customer baru EMQX Cloud, kami akan memberi Anda 30 hari masa coba gratis untuk deployment. Masa coba gratis ini sangat ideal untuk Anda yang ingin mempelajari and menelusuri fitur-fitur EMQX Cloud.
   ```

3. Setelah deployment telah dibuat dan statusnya menjadi **running**, masukkan informasi otentikasi klien (bisa dimasukkan secara manual atau diimpor dari file).

    ![add authentication](https://static.emqx.net/images/9142d9a045b570402515eaa47c6698a6.png)

4. Klik konfigurasi Home Assistant untuk menambah integrasi.

5. Pilih MQTT dan masukkan informasi deployment.

    ![Add MQTT Broker to Home Assistant](https://static.emqx.net/images/1da096c0f7a5f4b200b1f14583c49414.png)

    ![EMQX MQTT Cloud deployment information](https://static.emqx.net/images/26b958bcc271d1f6801d06152c65fd78.png)

   Anda perlu memasukkan `Connect Address `untuk Broker dan `Connect Port (mqtt)` untuk Port. Masukkan username dan password yang Anda buat di halaman otentikasi.

6. Klik tombol `Submit`.

7. Selamat, deployment EMQX Cloud Anda sekarang telah terintegrasi dengan Home Assistant!

    ![Successfully integrating with Home Assistant](https://static.emqx.net/images/e6bd46c82942efdbac70ed9d09faa35b.png)
