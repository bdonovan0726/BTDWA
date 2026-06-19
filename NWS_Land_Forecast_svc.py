import json
import time
import logging
import os
import argparse
from NOAA.client import NOAAClient
from Data.SQLite import SQLiteconn
from datetime import datetime, timedelta, UTC
from Stormglass.Stormclient import StormGlass

parser = argparse.ArgumentParser()

parser.add_argument(
"-d", "--delay",
default = 900,
type = int,
help = 'time delay between fetches'
)

log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"SG_Forecast_cache_service_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]    
)

def main():
    
    SGCli = StormGlass('keys.apk')
    
    with SQLiteconn("Data/weather.db") as SQConn:
        stats = SQConn.getAllNWSLandStations()
        for station in stats:
            try:
                start = datetime.now(UTC)
                end = start + timedelta(days=7)
                print(f'Retrieving/updating forecast information for station: {station[0]}')
                respJSON = SGCli.getStormglassForecast(station[3], station[4])
                hourList = []
                for h in respJSON['hours']:
                    hrData = {}
                    hrData['time'] = h['time']
                    hrData['airTemperature'] = h['airTemperature']['sg']
                    hrData['cloudCover'] = h['cloudCover']['sg']
                    hrData['gust'] = h['gust']['sg']
                    hrData['humidity'] = h['humidity']['sg']
                    hrData['precipitation'] = h['precipitation']['sg']
                    hrData['pressure'] = h['pressure']['sg']
                    hrData['snow'] = h['snow']['sg']
                    hrData['windDirection'] = h['windDirection']['sg']
                    hrData['windSpeed'] = h['windSpeed']['sg']
                    hourList.append(hrData)
                    
                foreData = (int(time.time()), start, end, json.dumps(respJSON), json.dumps(hourList), station[0])
                SQConn.updateNWSLandForecastCache(foreData)
                
            except Exception as e:
                logging.error(f'Received error: {e}')
                continue
            
    
if __name__ == "__main__":
    
    try:
        while True:
            args = parser.parse_args()
            logging.info(f"Starting SG Land forecast cache run with delay {args.delay} seconds..")
            try:
                main()
            
            except Exception as e:
                logging.error(f'Encountered error in cache run: {e}')
                
            logging.info(f'Caching cycle complete, sleeping...')
            time.sleep(args.delay)
        
    except Exception as e:
        logging.error(f'Caught exception {e}')
        logging.error(f'Shutting down gracefully')
        
