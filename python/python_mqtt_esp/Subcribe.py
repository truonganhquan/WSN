import paho.mqtt.client as mqtt
from Get_Data_to_DB import *
 
MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "home"
def on_connect(client,userdata, flags , rc):
	if rc != 0:
		pass
		print("unable to conenct MQTT broker : !")
	else:
		print("connect with MQTT_Broker : " + str(MQTT_Broker))
		client.subscribe(MQTT_Topic,0)

def on_message(client, userdata, msg):

	print("MQTT Data recive ...")
	print("MQTT_Topic :" + str(MQTT_Topic))
	print("Data: " + str(msg.payload))
	try:
		Sensor(msg.payload) 
	except Exception as e:
		print("Error!!!!!")
	
	#Sensor()
client = mqtt.Client()
client.username_pw_set(username= "quan" , password = "123456")
client.on_connect = on_connect
#print("on_connect \n")
client.on_message = on_message

client.connect(MQTT_Broker , MQTT_Port , Keep_Alive_Interval)
client.loop_forever()
