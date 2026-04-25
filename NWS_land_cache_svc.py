import json
import time
import logging
from NOAA.client import NOAAClient
from Data.SQLite import SQLiteconn
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"weather_service_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]    
)

def main():

    client = NOAAClient()

    with SQLiteconn("C:\sources\BTDWA\Data\weather.db") as SQConn:
        
        stationList = SQConn.getAllNWSLandStationsFromCache()
        for station in stationList:
            print(f'Calling/updating for station {station[0]}')
            try:
                JSONresp = client.getLatestObservation(station[0])
                resp = JSONresp['properties']
            ###debug code---------------------------------------------------------------
                wData = (str(time.time()),
                        resp.get('textDescription', 'NA'),
                        resp.get('temperature', {}).get('value'),
                        resp.get('windDirection', {}).get('value'),
                        resp.get('windSpeed', {}).get('value'),
                        resp.get('windGust', {}).get('value'),
                        resp.get('barometricPressure', {}).get('value'),
                        resp.get('relativeHumidity', {}).get('value'),
                        resp.get('windChill', {}).get('value'),
                        resp.get('heatIndex', {}).get('value'),
                        json.dumps(JSONresp, indent = 2),
                        resp['timestamp'], station[0])       
                SQConn.updateNWSLandCache(wData)
            except Exception as e:
                print(f'Encounbtered issue with station {station[0]}: {e}')
                print(f'JSON: {json.dumps(JSONresp, indent = 2)}')
                continue
    

if __name__ == "__main__":
    try:
        while True:
            logging.info("Starting cycle...")
            try:
                main()
            except Exception as e:
                logging.error(f"Loop error: {e}")
                
            logging.info("Cycle complete. Sleeping...\n")
            time.sleep(900)
            
    except:
        logging.info("Shutting down service gracefully...")
    
###GRAVEYARD###############
        # stationIDs = SQConn.getAllNWSStations()
        # print(f'Station info: {stationIDs[0][1]}')
        # print(f'Calling for coordinates: {stationIDs[0][4]}:{stationIDs[0][5]}')
        
        # resp = client.getHourlyForecast(stationIDs[0][4], stationIDs[0][5])
        # print(resp['periods'][0])
        
        #####debug code--------------------------------------------------------------

        # print(f'TempC: {resp['temperature']['value']}')
        # print(f'Description: {resp['textDescription']}')
        # print(f'WindDIrecgtion: {resp['windDirection']['value']}')
        # print(f'windSpeed: {resp['windSpeed']['value']}')
        # print(f'windGust: {resp['windGust']['value']}')
        # print(f'Pressure: {resp['barometricPressure']['value']}')
        # print(f'Humidity: {resp['relativeHumidity']['value']}')
        # print(f'WindChill: {resp['windChill']['value']}')
        # print(f'HeatIndex: {resp['heatIndex']['value']}')
        # print(f'CloudLayers: {resp['cloudLayers'][0]['amount']}')