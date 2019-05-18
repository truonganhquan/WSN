#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

const char* ssid = "AndroidAP";                   // wifi ssid
const char* password =  "wczg6435";         // wifi password
const char* mqttServer = "192.168.43.26";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "quan";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "123456";  // if you don't have MQTT Password, no need input
#define mqtt_topic_pub "home"   
#define mqtt_topic_sub "led"
WiFiClient espClient;
PubSubClient client(espClient);
int ledPin = D2;
const int DHTPin = D4;
long lastMsg = 0;
char msg[50];
int value = 0;
// Timers auxiliar variables
long now = millis();
long lastMeasure = 0;

#define DHTTYPE DHT11
DHT dht(DHTPin, DHTTYPE);

const long utcOffsetInSeconds = 7*60*60;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin,OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
     // delay(500);
    }
  }
}
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection..."); // Thực hiện kết nối với mqtt user và pass
    if (client.connect("ESP8266Client",mqttUser,mqttPassword )) {
      Serial.println("connected");// Khi kết nối sẽ publish thông báo
      client.publish(mqtt_topic_pub, "ESP_reconnected");
     // client.subscribe(mqtt_topic_sub);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(100);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  char receivedChar;
  String dataReceived;
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
     receivedChar = (char)payload[i];
     dataReceived = dataReceived + String(receivedChar);
    //Serial.print(receivedChar);
  }
  Serial.print(dataReceived);
  if (dataReceived == "led1off") {
    digitalWrite(ledPin, LOW);   
    Serial.print("led off now");
  } 
  if(dataReceived == "led1on"){
    digitalWrite(ledPin , HIGH);  
    Serial.print("led on now");
  }
  if(dataReceived != "led1on" && dataReceived != "led1off"){
    int pwm = dataReceived.toInt();
    analogWrite(ledPin,pwm);
    Serial.print("ok");
  }
  
  Serial.println();
  Serial.println("-----------------------");
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
   float h = dht.readHumidity();
   float t = dht.readTemperature();
   int l = analogRead(A0);
   // float h = random(70,100);
   // float t = random(20,36);
   // int l = random(400,700);

    
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
    client.publish("home", strPayload.c_str());
  }
}
void loop() {
  
    pub();
    //client.publish("led", "1");
    client.subscribe("led");
    delay(50);
    client.loop();
}
