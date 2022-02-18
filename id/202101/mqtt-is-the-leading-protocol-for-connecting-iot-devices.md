Sebelum Internet of Things menjadi populer, atau saat dimana istilah Internet of Things pertama disebutkan di media (akhir tahun 90-an), Andy Stanford-Clark berkolaborasi dengan Arlen Nipper (sekarang CirrusLink) dalam merancang sebuah protokol untuk berkomunikasi dengan [sistem SCADA](https://en.wikipedia.org/wiki/SCADA) di industri minyak dan gas yang pertama dimulai sebagai protokol untuk industri tertentu dengan cepat menjadi protokol open-source untuk komunikasi perangkat IoT di masa sekarang.



## MQTT, sebuah model publish-subscribe

MQTT adalah protokol messaging yang dibentuk dengan TCP/IP berdasarkan model messaging publish-subscribe. Publisher mengirim pesan, subscriber menerima pesan yang mereka sukai, dan broker akan menyampaikan pesan dari pengirim ke penerima. Publisher dan subscriber adalah klien MQTT yang hanya berkomunikasi dengan broker MQTT. Klien MQTT dapat berupa perangkat atau aplikasi apapun (dari mikro kontroler seperti Arduino sampai dengan aplikasi penuh yang di host di Cloud) yang menjalankan [MQTT library](https://github.com/mqtt/mqtt.github.io/wiki/libraries) dan mengkoneksikan ke broker MQTT melalui sebuah jaringan. Broker MQTT mengelola penerimaan pesan dari publisher dan pengiriman pesan ke subscriber (dan juga mengelola daftar topik yang disukai subscriber).



## MQTT menjadi open source

Sejak Internet of Things menjadi populer, MQTT juga melonjak. Broker MQTT open-source pertama, Mosquitto diciptakan di tahun 2008, dan di tahun 2014 ia menjadi [projek Eclipse Mosquitto](https://projects.eclipse.org/projects/iot.mosquitto). Di tahun 2012, [projek Eclipse Paho](https://projects.eclipse.org/projects/iot.paho) menyediakan library klien MQTT open-source untuk Java, C, JavaScript, dan Python dan dari sana daftar library klien MQTT telah bertambah. Di akhir tahun 2014, MQTT versi 3.1.1 menjadi [standar OASIS](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) dan membuka jalan untuk MQTT untuk menjadi [standar ISO](https://www.iso.org/standard/69466.html).



## MQTT mengambil alih IoT

MQTT adalah protokol terkemuka untuk menghubungkan perangkat IoT dan menggeser HTTP, andalan di dunia internet di tahun 2017. Terlebih lagi, MQTT telah dipilih protokol messaging untuk platform IoT seperti Amazon, Microsoft, IBM, dan produk open-source dan broker komersial lainnya. [EMQX Cloud](https://www.emqx.com/en/cloud)  tidak hanya menyediakan konektivitas aman dalam skala besar untuk perangkat MQTT, tapi juga pengelolaan perangkat, penyimpanan data, dan juga analitik data di Cloud. MQTT juga telah teruji skalabilitasnya dengan menjadi protokol messaging di balik Facebook Messenger.



## Tahap Selanjutnya untuk MQTT

Apa tahap selanjutnya untuk MQTT? Kami tidak melakukan perubahan apapun ke prokotol MQTT selama sepuluh tahun masa awal pemakaiannya, yang menunjukkan bahwa kami melakukan pekerjaan yang cukup baik dalam mengantisipasi kebutuhan pasar dan penggunanya. Seiring dengan matangnya Internet bersama dengan perangkat dan konektivitas industri dan munculnya hosting skala-tinggi di Cloud, kami menyadari bahwa MQTT memerlukan beberapa fitur tambahan.  Sangatlah penting untuk kami untuk berpegang ke prinsip dasar MQTT: ringkas, mudah dipahami dan mudah untuk mengimplimentasikan spesifikasi. MQTT v5 dirilis di akhir tahun 2018 dan dalam tahap ratifikasi sebagai OASIS, dan kemudian standar ISO di awal tahun 2019.

Disamping itu, tiap harinya, ratusan juta perangkat dan aplikasi mengirim dan menerima pesan dan perintah di Internet of Things dengan menggunakan MQTT.
