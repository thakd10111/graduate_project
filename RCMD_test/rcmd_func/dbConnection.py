import pymysql

class MyDB(object) :

	def __init__ (self, host, port, user, pw, db) :
		self.connection = pymysql.connect(host=host, port = port, user=user, password=pw, db=db, charset='utf8')
		self.cursor = self.connection.cursor()
		self.cursor_dic = self.connection.cursor(pymysql.cursors.DictCursor)

	def commit(self) :
		self.connection.commit()

	def dic_execute(self, sql) :
		self.cursor_dic.execute(sql)

	def execute(self, sql) :
		self.cursor.execute(sql)

	def dic_fetchall(self) :
		return self.cursor_dic.fetchall()

	def fetchall(self) :
		return self.cursor.fetchall()

	def dic_fetchone(self) :
		return self.cursor_dic.fetchone()

	def fetchone(self) :
		return self.cursor.fetchone()