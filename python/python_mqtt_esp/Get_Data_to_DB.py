import MySQLdb as pymysql
import json
from datetime import datetime
def Sensor(jsonData):
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
#	Date_and_Time = json_Dict['Date']
	Temperature = json_Dict['Temperature']
	Humidity = json_Dict['Humidity']
	Light = json_Dict['Light']

	Date_and_Time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

	db = pymysql.connect("localhost","quan","123456","quan")

	cursor = db.cursor()

	sql = """INSERT INTO thcs (SensorID,Temperature,Humidity,Light,Date_and_Time) 
				VALUES(%s,%s,%s,%s,%s)"""
	#thuc thi
	val = (SensorID,Temperature,Humidity,Light,Date_and_Time)

	try:
		cursor.execute(sql,val)
		#cursor.execute(sql)
		print("success")
		db.commit()
	except:
		db.rollback()
	#close
	db.close()
