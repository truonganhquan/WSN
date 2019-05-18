import paho.mqtt.client as mqtt
import random,json
from datetime import datetime
from time import sleep
from led import *

MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "led"

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

def publish_led_status():

	status = led_status()

#	print(status)
	publish_To_Topic(MQTT_Topic,status)
while True:
	publish_led_status()
	sleep(0.5)

