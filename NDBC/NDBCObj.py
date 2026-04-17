#for objects that represent buoy data

class NDBCBuoyData:

    def __init__(self, bData : dict, stationID = 'NA'):
        self.waveHeight = bData["WVHT"]
        self.waveDomPeriod = bData["DPD"]
        self.aveWavePeriod = bData["APD"]
        
        self.windSpeed = bData["WSPD"]
        self.windDir = bData["WDIR"]
        self.windGust = bData["GST"]
        
        self.waterTemp = bData["WTMP"]
        self.airTemp = bData["ATMP"]
        
        self.obsTime = f"UTC: {bData['MM']}-{bData['DD']}-{bData['#YY']}-{bData['hh']}-{bData['MM']}"
        
        