#for objects that represent buoy data

class NDBCBuoyData:

    def __init__(self, bData : dict, stationID = 'NA'):
        self.stationID = stationID
        self.waveHeight = bData["WVHT"]
        self.waveDomPeriod = bData["DPD"]
        self.aveWavePeriod = bData["APD"]
        
        self.windSpeed = bData["WSPD"]
        self.windDir = bData["WDIR"]
        self.windGust = bData["GST"]
        
        self.waterTemp = bData["WTMP"]
        self.airTemp = bData["ATMP"]
        
        self.obsTime = f"UTC: {bData['MM']}-{bData['DD']}-{bData['#YY']}-{bData['hh']}-{bData['MM']}"
        
    def printBuoyData(self):
        print(f"Observed data for station id: {self.stationID} as of {self.obsTime}")
        print(f"Wave Height: {self.waveHeight} D-Period: {self.waveDomPeriod} Avg: {self.aveWavePeriod}")
        print(f"Wind {self.windSpeed} at {self.windDir} gust {self.windGust}")
        print(f"Water temp {self.waterTemp} Air Temp {self.airTemp}")
        
        