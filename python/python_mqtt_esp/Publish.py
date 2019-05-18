import paho.mqtt.client as mqtt
import random,json
from datetime import datetime
from time import sleep

MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "home"

def on_connect(client , userdata ,rc):
	if rc !=0:
		pass 
		print("Unable to connect MQTT_Broker !")
	else:
		print("Connect with MQTT Broker " + str(MQTT_Broker))
def on_publish(client ,user,mid):
	pass
def on_disconnect(client , userdata ,rc):
	if rc != 0:
		pass
mqttc = mqtt.Client()
mqttc.username_pw_set(username = "quan",password = "123456")
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, MQTT_Port,Keep_Alive_Interval)

def publish_To_Topic(topic , message):
	mqttc.publish(topic,message)
	print(("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic)))
	print("")

def publish_Fake_Sensor_Values_to_MQTT():
	Humidity_Fake_Value = int(random.randint(50,100))
	Temperatue_Fake_Value = int(random.randint(20,35))
	Light_fake = int(random.randint(200,1000))
	Sensor_data = {}
	Sensor_data['Sensor_ID'] = "DHT-11"
	# Sensor_data['Date'] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
	Sensor_data['Humidity'] = Humidity_Fake_Value
	Sensor_data['Temperature'] = Temperatue_Fake_Value
	Sensor_data['Light'] = Light_fake

	sensor_json_data =json.dumps(Sensor_data)
	publish_To_Topic(MQTT_Topic,sensor_json_data)

while True:
	publish_Fake_Sensor_Values_to_MQTT()
	sleep(2)
 