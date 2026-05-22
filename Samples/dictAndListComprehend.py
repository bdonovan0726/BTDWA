from Data.SQLite import SQLiteconn

with SQLiteconn("C:\sources\BTDWA\Data\weather.db") as SQConn:
    obs, desc = SQConn.getAllCachedNWSObservations()
    print(enumerate(desc))
    print(desc)
    
