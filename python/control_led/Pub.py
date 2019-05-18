import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime
from time import sleep

Broker = "localhost"
Port = 1883
Wait = 45
Topic = "room2"

def on_connect(client, userdata, flags, rc):
    if rc!= 0:
        pass
        print('Unable to connect to Broker...')
    else:
        print('Connected with Broker: ' + str(Broker))

def on_publish(client, userdata, mid):
    pass

def disconnect(client, userdata, rc):
    if rc != 0:
        pass

mqttc = mqtt.Client()
mqttc.username_pw_set(username = "tuananh", password = "abc13579")
mqttc.on_connect = on_connect
mqttc.disconnect = disconnect
mqttc.on_publish = on_publish
mqttc.connect(Broker, Port, Wait)

def pub2topic(topic, message):
    mqttc.publish(topic,message)
    print(('Published: ' + str(message) + ' ' + 'on MQTT topic: ' + str(topic)))
    print('')

def pub_data_fake(nameSensor):
    hum = int(random.uniform(50,100))
    temp = int(random.uniform(20,40))
    light = int(random.uniform(0,1023))     
    dust = int(random.uniform(0,99))
    sensor_data = {}
    sensor_data['hum'] = hum
    sensor_data['temp'] = temp
    sensor_data['light'] = light
    sensor_data['dust'] = dust
    sensor_json_data = json.dumps(sensor_data)
    print("Publishing data fake from %s: " %nameSensor)
    pub2topic(Topic,sensor_json_data)

# pub_data_fake("Sensor1")
# pub_data_fake("Sensor2")
# pub_data_fake("Sensor3")
 
while True:
    pub_data_fake("room2")
    sleep(1)