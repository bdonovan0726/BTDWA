import sqlite3

class SQLiteconn:

    def __init__(self, DBPath : str):
        self.DBConn = sqlite3.connect(DBPath)
        self.cursor = self.DBConn.cursor()
        
    def __enter__(self):
        return self

    def getUserIDbyUserName(self, userName : str):
        query = """
            SELECT ID
            FROM users
            WHERE username = ?
            LIMIT 1
        """

        self.cursor.execute(query, (userName,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        return None

    def getStationsForUser(self, userID : str):
        query = """
            SELECT station_id
            FROM user_stations
            where user_id = ?
        """

        self.cursor.execute(query, (userID,))
        results = self.cursor.fetchall()

        return results
        
    def __exit__(self, ev, et, evb):
        self.DBConn.close()