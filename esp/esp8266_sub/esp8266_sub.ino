#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "tang_2";                   // wifi ssid
const char* password =  "12345679";         // wifi password
const char* mqttServer = "192.168.0.107";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "quan";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "12345678";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(espClient);
int ledPin = D2;

void setup() {

  Serial.begin(115200);
  pinMode(ledPin,OUTPUT);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
   // delay(500);
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
     // delay(2000);

    }
  }

//  client.publish("esp8266", "Hello Raspberry Pi");
//  client.subscribe("esp8266");

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

void loop() {
    client.publish("esp8266_quan", "Hello Raspberry Pi");
    client.subscribe("led");
    //delay(300);
   client.loop();
}
