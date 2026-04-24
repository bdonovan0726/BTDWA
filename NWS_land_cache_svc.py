import json
from NOAA.client import NOAAClient
from WeatherObjects.WObj import NOAAForecastPoint
from Data.SQLite import SQLiteconn
from NDBC.NDBCObj import NDBCBuoyData
from NDBC.NDBCClient import NDBCClient
from Stormglass.Stormclient import StormGlass

def main():

    with SQLiteconn("C:\sources\BTDWA\Data\weather.db") as SQConn:
        
        client = NOAAClient()
        # stationIDs = SQConn.getAllNWSStations()
        # print(f'Station info: {stationIDs[0][1]}')
        # print(f'Calling for coordinates: {stationIDs[0][4]}:{stationIDs[0][5]}')
        
        # resp = client.getHourlyForecast(stationIDs[0][4], stationIDs[0][5])
        # print(resp['properties']['periods'][0])
        print(f'Calling for station KSTL')
        resp = client.getLatestObservation('KSTL')
        print(f'TempC: {resp['properties']['temperature']['value']}')
        print(f'Description: {resp['properties']['textDescription']}')
        print(f'WindDIrecgtion: {resp['properties']['windDirection']['value']}')
        print(f'windSpeed: {resp['properties']['windSpeed']['value']}')
        print(f'windGust: {resp['properties']['windGust']['value']}')
        print(f'Pressure: {resp['properties']['barometricPressure']['value']}')
        print(f'Humidity: {resp['properties']['relativeHumidity']['value']}')
        print(f'WindChill: {resp['properties']['windChill']['value']}')
        print(f'HeatIndex: {resp['properties']['heatIndex']['value']}')
        print(f'CloudLayers: {resp['properties']['cloudLayers'][0]['amount']}')

    
        #print(json.dumps(resp, indent = 2))
        

if __name__ == "__main__":
    main()