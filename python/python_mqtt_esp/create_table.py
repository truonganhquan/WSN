import MySQLdb as pymysql
db = pymysql.connect("localhost","quan","123456","quan")

cursor = db.cursor()

cursor.execute("DROP TABLE IF exists thcs")

sql = """ CREATE TABLE thcs(
			id int(10) primary key auto_increment,
			SensorID char(10) not null,
			Temperature int(3) not null,
			Humidity int(3) not null,
			Light int(3) not null,
			Date_and_Time char(30) not null
	)
	"""
cursor.execute(sql)

db.close()