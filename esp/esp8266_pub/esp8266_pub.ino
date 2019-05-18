
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

#define DHTTYPE DHT11   // DHT 11
// Cập nhật thông tin
// Thông tin về wifi
// SDA D2
// SCL D1
#define ssid "tang_2"
#define password "12345679"
// Thông tin về MQTT Broker
#define mqtt_server "192.168.0.107" // Thay bằng địa chỉ IP 
#define mqtt_topic_pub "home"   //Giữ nguyên nếu bạn tạo topic tên là demo
#define mqtt_topic_sub "home"
#define mqtt_user "quan"    
#define mqtt_pwd "123456"
 
const uint16_t mqtt_port = 1883; //Port của MQTT
 
 
WiFiClient espClient;
PubSubClient client(espClient);
 
const int DHTPin = D4;       //Đọc dữ liệu từ DHT11 ở chân D5 trên mạch esp8266
int ledPin = D2;
long lastMsg = 0;
char msg[50];
int value = 0;
// Timers auxiliar variables
long now = millis();
long lastMeasure = 0;
 
// Thiet Lap cam bien DHT.
DHT dht(DHTPin, DHTTYPE);

const long utcOffsetInSeconds = 7*60*60;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port); 
  dht.begin();
  pinMode(ledPin,OUTPUT);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  char receivedChar;
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
     receivedChar = (char)payload[i];
    Serial.print(receivedChar);
  }
  if (receivedChar == '0') {
    digitalWrite(ledPin, LOW);   // Turn the LED on (Note that LOW is the voltage level
    Serial.print("led off now");
  } 
  if(receivedChar == '1'){
    digitalWrite(ledPin , HIGH);  // Turn the LED off by making the voltage HIGH
    Serial.print("led on now");
  }
  Serial.println();
  Serial.println("-----------------------");
}

// Hàm reconnect thực hiện kết nối lại khi mất kết nối với MQTT Broker
void reconnect() {
  // Chờ tới khi kết nối
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Thực hiện kết nối với mqtt user và pass
    if (client.connect("ESP8266Client",mqtt_user,mqtt_pwd)) {
      Serial.println("connected");
      // Khi kết nối sẽ publish thông báo
      client.publish(mqtt_topic_pub, "ESP_reconnected");
      // ... và nhận lại thông tin này
     // client.subscribe(mqtt_topic_sub);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Đợi 5s
      delay(5000);
    }
  }
}
void pub(){
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("ESP8266Client");

  now = millis();
  // Publishes new temperature and humidity every 30 second
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& data = jsonBuffer.createObject();
  if (now - lastMeasure > 1000) {
    lastMeasure = now;
    //float h = dht.readHumidity();
   // float t = dht.readTemperature();
   // int l = analogRead(A0);
    float h = random(70,100);
    float t = random(20,36);
    int l = random(400,700);

    
    static char temperatureTemp[7];
    dtostrf(t, 6, 2, temperatureTemp);
    
    static char humidityTemp[7];
    dtostrf(h, 6, 2, humidityTemp);
    
    data["Temperature"] = t ;
    data["Sensor_ID"] = "node1";
    data["Humidity"] = h;
    data["Light"] = l;
   
    char payload[256];
    data.printTo(payload, sizeof(payload));
    String strPayload = String(payload);
    Serial.print("Format data: ");
    Serial.println(strPayload);
   // client.publish("home", strPayload.c_str());
 
    
 /*   Serial.print("\nHumidity: ");
    Serial.print(h);
    Serial.print(" %\t Temperature: ");
    Serial.print(t);
    Serial.print(" *C ");
//    Serial.print("\t light");
//    Serial.print(l);
    Serial.print("\n "); */
  }
}
void loop() {
    
     client.publish("led", "1"); // publish led
     client.subscribe("led");
     client.loop();
  
}
