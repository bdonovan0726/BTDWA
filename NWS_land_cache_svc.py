import json
import time
from NOAA.client import NOAAClient
from WeatherObjects.WObj import NOAAForecastPoint
from Data.SQLite import SQLiteconn
from NDBC.NDBCObj import NDBCBuoyData
from NDBC.NDBCClient import NDBCClient
from Stormglass.Stormclient import StormGlass

def main():

    with SQLiteconn("C:\sources\BTDWA\Data\weather.db") as SQConn:
        
        client = NOAAClient()
        
        stationList = SQConn.getAllNWSLandStationsFromCache()
        for station in stationList:
            print(f'Calling/updating for station {station[0]}')
            resp = client.getLatestObservation(station[0])

        ###debug code---------------------------------------------------------------
        
            wData = (str(time.time()), resp['properties']['textDescription'],
                    resp['properties']['temperature']['value'], resp['properties']['windDirection']['value'],
                    resp['properties']['windSpeed']['value'], resp['properties']['windGust']['value'],
                    resp['properties']['barometricPressure']['value'],
                    resp['properties']['relativeHumidity']['value'], resp['properties']['windChill']['value'],
                    resp['properties']['heatIndex']['value'], resp['properties']['cloudLayers'][0]['amount'],
                    station[0])
        #print (wData)       
            SQConn.updateNWSLandCache(wData)
        #print(json.dumps(resp, indent = 2))
        

if __name__ == "__main__":
    main()
    
###GRAVEYARD###############
        # stationIDs = SQConn.getAllNWSStations()
        # print(f'Station info: {stationIDs[0][1]}')
        # print(f'Calling for coordinates: {stationIDs[0][4]}:{stationIDs[0][5]}')
        
        # resp = client.getHourlyForecast(stationIDs[0][4], stationIDs[0][5])
        # print(resp['properties']['periods'][0])
        
        #####debug code--------------------------------------------------------------

        # print(f'TempC: {resp['properties']['temperature']['value']}')
        # print(f'Description: {resp['properties']['textDescription']}')
        # print(f'WindDIrecgtion: {resp['properties']['windDirection']['value']}')
        # print(f'windSpeed: {resp['properties']['windSpeed']['value']}')
        # print(f'windGust: {resp['properties']['windGust']['value']}')
        # print(f'Pressure: {resp['properties']['barometricPressure']['value']}')
        # print(f'Humidity: {resp['properties']['relativeHumidity']['value']}')
        # print(f'WindChill: {resp['properties']['windChill']['value']}')
        # print(f'HeatIndex: {resp['properties']['heatIndex']['value']}')
        # print(f'CloudLayers: {resp['properties']['cloudLayers'][0]['amount']}')