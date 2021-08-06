[MQTT](https://www.emqx.com/en/mqtt) adalah prokotol fleksibel dan lightweight untuk bertukar pesan IoT dan mengirim pesan. MQTT berfungsi untuk  menyeimbangkan fleksibilitas dan sumber hardware/jaringan untuk developer IoT.

[ESP8266](https://www.espressif.com/) menyediakan solusi SoC Wi-Fi yang sangat terintegrasi dengan desainnya yang kompak, hemat tenaga, dan stabilitas yang tinggi. ESP8266 memiliki fungsi jaringan Wi-Fi mandiri dan lengkap yang dapat diaplikasikan secara independen atau dapat dipakai sebagai slave di host MCU lainnya.

Dalam projek ini, kita akan mengkoneksikan ESP8266 ke [MQTT broker publik gratis](https://www.emqx.com/en/mqtt/public-mqtt5-broker) yang dioperasikan oleh [EMQ X MQTT Cloud](https://www.emqx.com/en/cloud) dan memprogram ESP8266 dengan Arduino IDE.

EMQ X Cloud adalah sebuah platform servis cloud MQTT IoT aman yang diluncurkan oleh [EMQ](https://www.emqx.com/en). EMQ X Cloud menyediakan operasi lengkap, membantu perawatan dan servis akses [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) dengan lingkungan unik yang terisolasi.

## Komponen IoT yang diperlukan

* ESP8266
* Arduino IDE
* [MQTT X](https://mqttx.app): Cross-platform MQTT 5.0 client tool yang elegan
* The free public [MQTT broker](https://www.emqx.com/en/products/emqx)
  - Broker: **broker.emqx.io**
  - TCP Port: **1883**
  - Websocket Port: **8083**



## ESP8266 Pub/Sub

![project.png](https://static.emqx.net/images/35a817d8c8b74c0481983b8c9ac0fee7.png)



## Kode

1. Pertama, impor library ESP8266WiFi dan PubSubClient. Library ESP8266WiFi dapat mengkoneksikan ESP8266 ke jaringan Wi-Fi, library PubSubClient memperbolehkan koneksi ESP8266 ke MQTT broker untuk mempublikasi pesan dan men-subscribe topik.

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   ```

2. Atur nama dan password Wi-Fi, connection address dan port MQTT broker.

   ```c
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   ```

3. Buka koneksi serial untuk memfasilitasi output hasil dari program dan koneksi ke jaringan Wi-Fi.

   ```c
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // connecting to a WiFi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. Atur MQTT broker, tulis fungsi callback, dan cetak informasi koneksi ke serial monitor disaat yang sama.

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp8266-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   
   void callback(char *topic, byte *payload, unsigned int length) {
       Serial.print("Message arrived in topic: ");
       Serial.println(topic);
       Serial.print("Message:");
       for (int i = 0; i < length; i++) {
           Serial.print((char) payload[i]);
       }
       Serial.println();
       Serial.println("-----------------------");
   }
   ```

5. Setelah berhasil dikoneksikan ke MQTT broker, ESP8266 akan mempublikasi pesan dan men-subscribe ke MQTT broker.

   ```c
   // publish and subscribe
   client.publish(topic, "hello emqx");
   client.subscribe(topic);
   ```

6. Pencetakan nama topik ke serial port dan cetak setiap byte dari pesan yang diterima.

   ```c
   void callback(char *topic, byte *payload, unsigned int length) {
       Serial.print("Message arrived in topic: ");
       Serial.println(topic);
       Serial.print("Message:");
       for (int i = 0; i < length; i++) {
           Serial.print((char) payload[i]);
       }
       Serial.println();
       Serial.println("-----------------------");
   }
   ```

7. Kode penuhnya:

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   
   WiFiClient espClient;
   PubSubClient client(espClient);
   
   void setup() {
     // Set software serial baud to 115200;
     Serial.begin(115200);
     // connecting to a WiFi network
     WiFi.begin(ssid, password);
     while (WiFi.status() != WL_CONNECTED) {
         delay(500);
         Serial.println("Connecting to WiFi..");
     }
     Serial.println("Connected to the WiFi network");
     //connecting to a mqtt broker
     client.setServer(mqtt_broker, mqtt_port);
     client.setCallback(callback);
     while (!client.connected()) {
         String client_id = "esp8266-client-";
         client_id += String(WiFi.macAddress());
         Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
         if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
             Serial.println("Public emqx mqtt broker connected");
         } else {
             Serial.print("failed with state ");
             Serial.print(client.state());
             delay(2000);
         }
     }
     // publish and subscribe
     client.publish(topic, "hello emqx");
     client.subscribe(topic);
   }
   
   void callback(char *topic, byte *payload, unsigned int length) {
     Serial.print("Message arrived in topic: ");
     Serial.println(topic);
     Serial.print("Message:");
     for (int i = 0; i < length; i++) {
         Serial.print((char) payload[i]);
     }
     Serial.println();
     Serial.println("-----------------------");
   }
   
   void loop() {
     client.loop();
   }
   ```



## Konektivitas dan tes MQTT broker.

1. Ingat pakai [Arduino IDE](https://www.arduino.cc/en/Main/Software) untuk mengupload kode penuh tersebut ke ESP 8266 dan buka serial monitor.

   ![esp_con.png](https://static.emqx.net/images/4c97b1546d31021cc22c64ae7ce4863b.png)

2. Buat koneksi antara MQTT X Client dan MQTT broker lalu kirim pesan ke ESP8266.

   ![mqttx_pub.png](https://static.emqx.net/images/daa2c401453155045f2c068bcd57d66a.png)

3. Lihat pesan yang diterima ESP8266 dalam serial monitor.

   ![esp_msg.png](https://static.emqx.net/images/8c98d850cdfd5c98db94471d0f6a308f.png)


## Rangkuman

Dengan ini, kita telah berhasil mengkoneksikan ESP8266 ke MQTT broker publik gratis yang disediakan oleh EMQ X Cloud. Dalam projek ini, kita mengkoneksikan ESP8266 ke MQTT broker, yang merupakan salah satu kemampuan dasar dari ESP8266. Selain itu, ESP8266 juga dapat dikoneksikan dengan berbagai macam sensor IoT dan melaporkan data sensor ke MQTT broker.

 

Kami akan merilis lebih banyak artikel mengenai pengembangan IoT dan ESP8266. Jangan kemana-mana ya!
