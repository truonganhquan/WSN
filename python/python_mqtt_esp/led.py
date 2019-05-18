import paho.mqtt.client as mqtt
import random,json
from datetime import datetime
from time import sleep
import MySQLdb as mysql 

def led_status(): 

	db = mysql.connect("localhost","quan","123456","quan")

	cursor = db.cursor()

	sql = """SELECT ledstatus from led order by id desc limit 1"""

	try:
	 	cursor.execute(sql)
	 	result =cursor.fetchone()
	 	for i in result:
	 		print(i)
	except:
		print("khong the ket noi")

	db.close()
	return i

