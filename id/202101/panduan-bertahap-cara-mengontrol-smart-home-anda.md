## Apa Itu Teknologi Smart Home?

Teknologi smart home, atau yang juga dikenal sebagai [home automation](https://internetofthingsagenda.techtarget.com/definition/smart-home-or-building) atau *domotics* (dari bahasa Latin "domus" yang berarti rumah), [memberikan si pemilik rumah keamanan](https://internetofthingsagenda.techtarget.com/blog/IoT-Agenda/Why-the-smart-home-needs-to-get-even-smarter), kenyamanan, kemudahan, dan menghemat energi dengan menggunakan perangkat cerdas, seringkali dengan aplikasi smart home di HP atau perangkat lainnya. Sebagai sebuah bagian dari [Internet of Things (IoT)](https://internetofthingsagenda.techtarget.com/definition/Internet-of-Things-IoT), sistem smart home dan perangkat lainnya bekerja sama untuk mendapatkan pemakaian data dan aksi mengotomatisasi lainnya berdasarkan preferensi si pengguna.

Hari ini, Anda akan mempelajari cara menggunakan [EMQX Cloud](https://www.emqx.com/en/cloud) untuk mengatur dan mengontrol smart home Anda. Artikel ini akan memperlihatkan Anda betapa gampangnya cara men-set up perangkat-perangkat IoT yang kita gunakan sehari-hari, sensor, dan protokol komunikasi yang kemudian dapat Anda terapkan ke lingkungan yang lebih kompleks.

[![EMQX Cloud](https://assets.emqx.com/images/96bda4a0efbeb977474da57f1c0a8edf.png)](https://www.emqx.com/en/cloud)



## Cara Kerja Smart Home/Implimentasi Smart Home

Untuk membuat sebuah smart home, terdapat banyak produk yang dapat kita gunakan dan tersedia di pasar, seperti lampu, soket listrik, dan sebagainya. Produk-produk dapat dipakai di banyak skenario, tapi terdapat kerugiannya. Beberapa perangkat ini tidak cocok, jadi Anda perlu sistem, aplikasi, ataupun dashboard yang berbeda untuk mengoperasikan perangkat tersebut. Dan di kasus tertentu, sebagian perangkat ini lumayan mahal.

Bukankah lebih baik jika Anda dapat membuat sesuatu sendiri dengan menggabungkan, melihat dan mengontrol output dari perangkat tersebut dari satu dashboard? Pola kode ini memungkinkan skenario smart home dengan hanya menggunakan teknologi open-source dan perangkat ataupun sensor yang terjangkau.

Meskipun solusi smart home ini bukan solusi yang paling keren, artikel ini akan memperlihatkan Anda betapa mudahnya cara menggunakan perangkat apapun. Selain itu, perangkat lain yang lebih profesional dapat digunakan dengan metode yang sama.

Semua sensor dan aktuator dapat dipantau melalui dashboard di HP Anda jadi Anda dapat mengambil tindakan dengan segera jika diperlukan melalui dashboard yang sama. Anda juga dapat mengirimkan update ke Slack jika Anda mau.

Dalam pola kode ini, saya akan menjelaskan cara menghubungkan sensor dan aktuator ke perangkat Arduino dan NodeMCU, cara membaca nilai dari sensor dan aktuator, dan cara menggunakan Raspberry Pi sebagai gateway dan server MQTT. Pola kode ini juga akan membahas lebih mendalam tentang cara menggunakan teknologi seperti Bluetooth, Wi-Fi, MQTT (atau LoRaWan) sebagai komunikator antar semua perangkat.



## Alur Smart Home

![image.png](https://assets.emqx.com/images/ffc1e3b61af24c37b5ffa42dc44c12b6.png)


1. Set up smart home Anda dengan 13 sensor dan aktuator yang terkoneksi dengan perangkat seperti Arduino.
2. Set up sebuah smart garden (bebas) dengan perangkat dan sensor NodeMCU.
3. Kedua perangkat dikoneksikan ke sebuah gateway Raspberry Pi yang akan mengirim dan menerima data sensor.
4. Smart home memiliki modul Bluetooth yang dapat Anda koneksikan ke HP.
5. Perangkat dan dashboard tersebut akan berkomunikasi dengan satu sama lainnya melalui EMQX Cloud.
6. Dashboard yang dapat dimulai di mesin lokal atau EMQX Cloud dan dapat dijangkau oleh HP melalui Wi-Fi akan memberi gambaran status smart home dan smart garden.
7. Beberapa notifikias dapat dikirim ke Slack melalui gateway.



## Cara Kerja Smart Home/Implimentasi Smart Home

Rumah baru biasanya memiliki infrastruktur smart home. Disisi lain, rumah yang agak tua dapat dipasang teknologi cerdas. Meskipun banyak sistem smart home yang memakai X10 atau Insteon, Bluetoth dan Wi-Fi sekarang telah menjadi lebih populer.

Zigbee dan Z-Wave adalah dua komunikasi protokol yang paling sering digunakan untuk home automation zaman sekarang. Keduanya menggunakan teknologi [mesh network](https://internetofthingsagenda.techtarget.com/definition/mesh-network-topology-mesh-network), jarak pendek,dan sinyal radio berdaya rendah untuk dikoneksikan ke sistem smart home. Meskipun keduanya menargetkan aplikasi smart home yang sama, Z-Wave memiliki jarak 30 meter dan Zigbee memiliki jarak 10 meter. Zigbee biasanya dirasa lebih kompleks daripada Z-Wave. Chip Zigbee didapatkan dari beberapa perusahaan, sementara chip Z-Wave cuma dari Sigma Designs.

Smart home bukanlah suatu koleksi dari perangkat cerdas dan alat-alat yang berbeda, tapi sebuah  sistem dimana semua perangkat tersebut bekerja sama untuk membangun sebuah jaringan yang dapat dikontrol dari jarak jauh. Semua perangkat tersebut dikontrol dengan sebuah kontroler home automation pusat yang sering disebut [smart home hub](https://internetofthingsagenda.techtarget.com/definition/smart-home-hub-home-automation-hub). Smart home hub adalah sebuah perangkat yang berfungsi sebagai titik pusat sistem smart home yang dapat merasakan, memproses data dan memiliki fitur nirkabel. Smart home hub menghubungkan semua aplikasi yang berbeda ke satu aplikasi smart home yang dapat dikontrol dari jarak jauh oleh si pemilik rumah. Contoh aplikasi smart home adalah Amazon Echo, Google Home, Insteon Hub Pro, Samsung SmartThings dan Wink Hub.

Beberapa sistem smart home dapat dibuat awal dengan menggunakan [Raspberry Pi](https://whatis.techtarget.com/definition/Raspberry-Pi-35-computer) atau prototyping board lainnya. Prototyping board lainnya dapat dibeli sebagai [smart home kit](https://internetofthingsagenda.techtarget.com/definition/smart-home-kit-home-automation-kit) yang digabungkan atau juga dikenal dengan platform smart home yang mengandung bagian-bagian yang diperlukan untuk membuat sebuah projek home automation.



Dalam skenario smart home yang sederhana, beberapa hal dapat dijadwalkan atau dipicu. Hal-hal yang dapat dijadwalkan berdasarkan waktu contohnya menurunkan tirai di jam 6 sore. Hal-hal yang dapat dipicu tergantung dari aksi di sistem otomatisasi, contohnya ketika pemilik HP mendekati pintu, pintu terbuka dan lampu dihidupkan secara otomatis.



## Rangkuman

Konsumer perlu menyadari masalah keamanan dalam menghubungkan perangkat IoT yang mengontrol bagian-bagian pribadi di rumah ke aplikasi yang tidak sepenuhnya dipahami dan pentingnya mengatur perangkat mereka. Kami telah menyerukan tingkat keamanan yang lebih baik untuk perangkat IoT. Untuk memastikan seluruh lingkungan smart home pengguna telah aman, perusahaan perlu mengembangkan perangkat IoT yang mudah dipakai dengan tingkat keamanan yang tinggi. Terakhir, kita juga perlu sebuah solusi pengontrolan yang lebih aman yang memungkinkan pemakai untuk menggunakan teknologi ini dirumah mereka dengan pede karena mereka tahu bahwa teknology ini aman dan privasi mereka terlindungi.
