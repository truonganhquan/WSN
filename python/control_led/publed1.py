import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime
from time import sleep
import MySQLdb

Broker = "localhost"
Port = 1883
Wait = 65535
Topic = "led"
stt=3
kton = 1
ktoff = 1
kton1 = 1
ktoff1 = 1
pwmled1 = 0
pwmled2 = 0


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
mqttc.username_pw_set(username = "quan", password = "123456")
mqttc.on_connect = on_connect
mqttc.disconnect = disconnect
mqttc.on_publish = on_publish
mqttc.connect(Broker, Port, Wait)

def pub2topic(topic, message):
    mqttc.publish(topic,message)
    print(('Published: ' + str(message) + ' ' + 'on MQTT topic: ' + str(topic)))
    print('')

def pub_led():
    db = MySQLdb.connect("localhost","quan","123456","quan")
    cursor = db.cursor()
    sql = """select ledstatus from led where id = (select max(id) from led)"""
    cursor.execute(sql)
    result = (cursor.fetchall())
    stt = result[0][0]
    # sensor_data['hum'] = hum
    # sensor_data['temp'] = temp
    # sensor_data['light'] = light
    # sensor_data['dust'] = dust
    # sensor_json_data = json.dumps(sensor_data)
    return stt

# pub_data_fake("Sensor1")
# pub_data_fake("Sensor2")
# pub_data_fake("Sensor3")
# def pub_data_fake2():
#     db = MySQLdb.connect("localhost","quan","123456","quan")
#     cursor = db.cursor()
#     sql = """select statusled2 from led2 where id = (select max(id) from led2)"""
#     cursor.execute(sql)
#     result = (cursor.fetchall())
#     stt = result[0][0]
#     return stt

def pub_pwm1():
    db = MySQLdb.connect("localhost","quan","123456","quan")
    cursor = db.cursor()
    sql = """select slidervalue from slider where id = (select max(id) from slider)"""
    cursor.execute(sql)
    result = (cursor.fetchall())
    stt = result[0][0]
    return stt

# def pub_pwm2():
#     db = MySQLdb.connect("localhost","tuananh","abc13579","wordpress")
#     cursor = db.cursor()
#     sql = """select led2 from controlled2 where id = (select max(id) from controlled2)"""
#     cursor.execute(sql)
#     result = (cursor.fetchall())
#     stt = result[0][0]
#     return stt

while True:
    if(pub_led() == 1 and ktoff == 1):
        mqttc.publish(Topic,"led1on")
        ktoff = 0
        kton = 1
        print("LED1 ON")
    if(pub_led() == 0 and kton == 1):
        mqttc.publish(Topic,"led1off")
        ktoff = 1
        kton = 0
        print("LED1 OFF")
    if(pub_pwm1() != pwmled1):
        pwmled1 = pub_pwm1()
        mqttc.publish(Topic,str(pwmled1))
        print(pwmled1)
    # if(pub_pwm2() != pwmled2):
    #     pwmled2 = pub_pwm2()
    #     mqttc.publish("led2pwm",str(pwmled2))
    