import json
import time
import logging
import os
from NOAA.client import NOAAClient
from Data.SQLite import SQLiteconn
from datetime import datetime

log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"weather_service_{timestamp}.log")

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
    