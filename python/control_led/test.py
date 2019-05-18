import paho.mqtt.client as mqtt
import random,json
from datetime import datetime
from time import sleep
import MySQLdb as mysql 
db = mysql.connect("localhost","quan","123456","quan")

cursor = db.cursor()

sql = """SELECT ledstatus from led order by id desc limit 1"""
sql1 = """SELECT slidervalue from silder order by id desc limit 1"""

cursor.execute(sql)
records1 = cursor.fetchone()

for i in records1:
	 	print(i)
	 	str1 = str(i)
	 	# print(type(i))
	 	print(str1)

db.close()
