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
        
    def getStationInfoByID(self, statID : str):
        query = """
            SELECT * 
            FROM NOAAstations
            where id = ?
        """
        
        self.cursor.execute(query, (statID,))
        results = self.cursor.fetchone()
        
        return results
        
    def getAllNWSStations(self):
        query = """
            SELECT *
            FROM NOAAStations
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results
        
    def getAllNWSLandStations(self):
        query = """
            SELECT *
            FROM NWSStations
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results
        
    def getAllNWSLandStationsFromCache(self):
        query = """
            SELECT StationID
            FROM NWS_Land_Cache
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results
        
    def updateNWSLandCache(self, wData : tuple):
        query = """
            UPDATE NWS_Land_Cache
            SET Timestamp = ?,
            Desc = ?,
            Temp = ?,
            WindDir = ?,
            WindSpeed = ?,
            WindGust = ?,
            Pressure = ?,
            Humidity = ?,
            WindChill = ?,
            HeatIndex = ?,
            JSON_raw = ?,
            ObsTimestamp = ?
            WHERE StationID = ?
        """
        
        self.cursor.execute(query, wData)
        self.DBConn.commit()
        
    def getNDBCBuoysForUser(self, userID : str):
        query = """
            SELECT ndbc_id
            from user_ndbc_buoys
            where user_id = ?
        """
        
        self.cursor.execute(query, (userID,))
        results = self.cursor.fetchall()
        
        return results
        
    def getNDBCBuoyInfo(self, buoyID : str):
        query = """
            SELECT *
            FROM NDBCBuoys
            where ID = ?
        """
        
        self.cursor.execute(query, (buoyID,))
        results = self.cursor.fetchone()
        
        return results
        
    def getAllCachedNWSObservations(self):
        query = """
            SELECT
            StationID,
            Timestamp,
            Desc,
            Temp,
            WindDir,
            WindSpeed,
            Pressure,
            Humidity,
            HeatIndex,
            ObsTimestamp
            FROM NWS_Land_Cache
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results, self.cursor.description
        
    def getAllCachedNWSObservationsWStatInfo(self):
        query = """
            SELECT
            ch.StationID,
            ch.Timestamp,
            ch.Desc,
            ch.Temp,
            ch.WindDir,
            ch.WindSpeed,
            ch.Pressure,
            ch.Humidity,
            ch.HeatIndex,
            ch.ObsTimestamp,
            st.Name as StationName,
            st.Comments as StationComments
            FROM NWS_Land_Cache as ch
            INNER JOIN NWSStations as st
            ON ch.StationID = st.StationID
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        return results, self.cursor.description
        
    def getStationCacheForecastData(self, statID : str):
        query = """
            SELECT
            ch.FetchTimestamp,
            ch.FCStart,
            ch.FCEnd,
            ch.NormalizedData,
            st.Name as StationName,
            st.Comments as StationComments
            FROM SG_Land_Forecast_Cache as ch
            INNER JOIN NWSStations as st
            ON ch.StationID = st.StationID
            WHERE ch.StationID = ?
        """
        
        self.cursor.execute(query, (statID,))
        return self.cursor.fetchone()
        
    def updateNWSLandForecastCache(self, foreData : tuple):
        query = """
            UPDATE SG_Land_Forecast_Cache
            SET FetchTimestamp = ?,
            FCStart = ?,
            FCEnd = ?,
            RawJSON = ?,
            NormalizedData = ?
            WHERE StationID = ?
        """
        
        self.cursor.execute(query, foreData)
        self.DBConn.commit()
        
    def updateSGHistoricalPrecip(self, data : tuple):
        query = """
            UPDATE SG_Precip_History
            SET Start = ?,
            End = ?,
            TotalPrecip = ?,
            TotalSnow = ?,
            TotalRain = ?,
            RawJSON = ?,
            LastPrecip = ?
            WHERE StationID = ?
        """
        
        self.cursor.execute(query, data)
        self.DBConn.commit()
        
    def getSGHistoricalPrecipData(self, stationID : str):
        query = """
            SELECT *
            FROM SG_Precip_History
            WHERE StationID = ?
        """
        
        self.cursor.execute(query, (stationID,))
        return self.cursor.fetchone()
        
    def getWaterStations(self):
        query = """
            SELECT *
            FROM Water_Stations
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def getBuoysForWaterStation(self, WS : str):
        query = """
            SELECT * 
            FROM NDBCBuoys
            WHERE WaterStation = ?
        """
        
        self.cursor.execute(query, (WS,))
        return self.cursor.fetchall()

    def updateWaterForecastCache(self, data : tuple):
        query = """
            UPDATE Water_Forecast_Cache
            SET UpdTimestamp = ?,
            StartTime = ?,
            EndTime = ?,
            RawJSON = ?,
            Normalized = ?
            WHERE StationID = ?
        """
        
        self.cursor.execute(query, data)
        self.DBConn.commit()
        
    def getWaterStationCacheForecastData(self, statID : str):
        query = """
            SELECT
            ch.UpdTImestamp,
            ch.StartTIme,
            ch.EndTime,
            ch.Normalized,
            st.FriendlyName as StationName,
            st.WindWarn as WindWarn,
            st.OffshoreWindLower as OffShWindLower,
            st.OffshoreWindUpper as OffShWindUpper,
            st.OffShWindYellow as OffShWindYellow,
            st.OffShWindRed as OffShWindRed
            FROM Water_Forecast_Cache as ch
            INNER JOIN Water_Stations as st
            ON ch.StationID = st.ID
            WHERE ch.StationID = ?
        """
        
        self.cursor.execute(query, (statID,))
        return self.cursor.fetchone()
        
    def getAllWaterStationsMeta(self):
        query = """
            SELECT id,
            FriendlyName,
            Description
            FROM Water_Stations
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

#####mothballed code for now-------------------------------------------------------------        
    # def updateWaterStationCache(self, data : tuple):
        # query = """
            # UPDATE Water_Obs_Cache
            # SET UpdTimestamp = ?,
            # ObsTimestamp = ?,
            # WaveHeight = ?,
            # DomPeriod = ?,
            # APeriod = ?,
            # WaveDirection = ?,
            # WindDir = ?,
            # WindSpeed = ?,
            # WindGust = ?,
            # WaterTemp = ?,
            # AirTemp = ?,
            # Pressure = ?
            # WHERE StationID = ?
        # """
        
        # self.cursor.execute(query, data)
        # self.DBConn.commit()
        
    # def getWaterStationCacheInfo(self):
        # query = """
            # SELECT ch.UpdTimestamp, ch.ObsTimestamp, ch.WaveHeight,
            # ch.DomPeriod, ch.APeriod, ch.WaveDirection,
            # ch.WindDir, ch.WindSpeed, ch.WindGust,
            # ch.WaterTemp, ch.AirTemp, ch.Pressure,
            # ws.FriendlyName, ws.Description
            # FROM Water_Obs_Cache as ch
            # INNER JOIN Water_Stations as ws
            # on ch.StationID = ws.ID
        # """
        
        # self.cursor.execute(query)
        # results = self.cursor.fetchall()
        
        # return results, self.cursor.description
        
    def rowToDict(self, description, row):
        return {col[0]: row[idx] for idx, col in enumerate(description)}
        
    def runAdHocSelectQuery(self, query : str):
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def __exit__(self, ev, et, evb):
        self.DBConn.close()