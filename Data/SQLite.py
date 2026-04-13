import sqlite3

class SQLiteconn:

	def __init__(self, DBPath : str):
		self.DBConn = sqlite3.connect(DBPath)
		self.cursor = self.DBConn.cursor()
		
	def getUserIDbyUserName(self, userName : str):
		query = """
			SELECT ID
			FROM users
			WHERE username = ?
			LIMIT 1
		"""
		
		self.cursor.execute(query, (userName,))
		result = self.cursor.fetchone()
		self.DBConn.close()
		
		if result:
			return result[0]
		return None