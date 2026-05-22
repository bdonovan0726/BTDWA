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
default = 4800,
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
        stats = SQConn.getWaterStations()
        for station in stats:
            try:
                start = datetime.now(UTC)
                end = start + timedelta(days=10)
                print(f'Retrieving/updating water forecast information for station: {station[0]}')
                respJSON = SGCli.getStormglassWaterForecast(station[3], station[4])
                #print(respJSON)
                hourList = []
                #print(respJSON['hours'][0])
                for h in respJSON['hours']:
                    hrData = {}
                    hrData['time'] = h['time']
                    hrData['airTemperature'] = h.get('airTemperature', {}).get('sg')
                    hrData['cloudCover'] = h.get('cloudCover',{}).get('sg')
                    hrData['currentDirection'] = h.get('currentDirection', {}).get('sg')
                    hrData['currentSpeed'] = h.get('currentSpeed', {}).get('sg')                    
                    hrData['gust'] = h.get('gust', {}).get('sg')
                    hrData['humidity'] = h.get('humidity', {}).get('sg')
                    hrData['pressure'] = h.get('pressure', {}).get('sg') 
                    hrData['surfaceTemperature'] = h.get('surfaceTemperature', {}).get('sg')
                    hrData['swellDirection'] = h.get('swellDirection', {}).get('sg')                    
                    hrData['swellHeight'] = h.get('swellHeight', {}).get('sg')
                    hrData['swellPeriod'] = h.get('swellPeriod', {}).get('sg')
                    hrData['waterTemperature'] = h.get('waterTemperature', {}).get('sg')
                    hrData['waveHeight'] = h.get('waveHeight', {}).get('sg')
                    hrData['wavePeriod'] = h.get('wavePeriod', {}).get('sg')
                    hrData['windDirection'] = h.get('windDirection', {}).get('sg')
                    hrData['windSpeed'] = h.get('windSpeed', {}).get('sg')
                    hourList.append(hrData)
                    
                foreData = (int(time.time()), start, end, json.dumps(respJSON), json.dumps(hourList), station[0])
                SQConn.updateWaterForecastCache(foreData)
                
            except Exception as e:
                logging.error(f'Received error in water cache svc: {e}')
                continue
                
if __name__ == "__main__":
    
    try:
        while True:
            args = parser.parse_args()
            logging.info(f"Starting SG Water forecast cache svc run with delay {args.delay} seconds..")
            try:
                main()
            
            except Exception as e:
                logging.error(f'Encountered error in water service cache run: {e}')
                
            logging.info(f'Caching cycle complete, sleeping...')
            time.sleep(args.delay)
        
    except Exception as e:
        logging.error(f'Caught exception {e}')
        logging.error(f'Shutting down gracefully')